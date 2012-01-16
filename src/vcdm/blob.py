import time

from twisted.python import log

import vcdm
from vcdm.utils import check_path
from vcdm.authz import authorize

from httplib import NOT_FOUND, CREATED, OK, CONFLICT, NO_CONTENT, FORBIDDEN, \
    UNAUTHORIZED, NOT_IMPLEMENTED, FOUND


def write(avatar, name, container_path, fullpath, mimetype, metadata, content):
    """ Write or update content of a blob. """
    from vcdm.server.cdmi.generic import get_parent
    parent_container = get_parent(fullpath)

    uid, vals = vcdm.env['ds'].find_by_path(fullpath, object_type='blob',
                                            fields=['parent_container'])
    # assert that we have a consistency in case of an existig blob
    if uid is not None and parent_container != vals['parent_container']:
        log.err("Inconsistent information! path: %s, parent_container in db: %s" %
                                                    (fullpath,
                                                     vals['parent_container']))
        return (FORBIDDEN, uid)

    # assert we can write to the defined path
    # TODO: expensive check for consistency, make optional
    if not check_path(container_path):
        log.err("Writing to a container is not allowed. Container path: %s" %
                '/'.join(container_path))
        return (FORBIDDEN, uid)

    # authorize call, take parent permissions
    _, cvals = vcdm.env['ds'].find_by_path(parent_container,
                                           object_type='container',
                                           fields=['metadata'])
    acl = cvals['metadata'].get('cdmi_acl', {})
    if not authorize(avatar, parent_container, "write_blob", acl):
        return (UNAUTHORIZED, uid)

    # ok, time for action
    # pick a blob back-end - if request_backend is specified in the metadata and
    # available in the system - use it. Else - resolve to default one.
    blob_backend = vcdm.env['blobs'].get(metadata.get('desired_backend', None),
                                         vcdm.env['blob'])

    # add default acls
    if avatar is None:
        avatar = 'Anonymous'
    blob_acl = metadata.get('cdmi_acl')
    if blob_acl is None:
        metadata['cdmi_acl'] = acl  # append parent ACLs for a new folder
    metadata['cdmi_acl'].update({avatar: 'rwd'})  # and creator's ACLs just in case

    # if uid is None, create a new entry, update otherwise
    if uid is None:
        uid = vcdm.env['ds'].write({
                        'object': 'blob',
                        'owner': avatar,
                        'fullpath': fullpath,
                        'mimetype': mimetype,
                        'metadata': metadata,
                        'filename': name,
                        'parent_container': parent_container,
                        'ctime': str(time.time()),
                        'mtime': str(time.time()),
                        'atime': str(time.time()),
                        'size': int(content[1]),  # length
                        'backend_type': blob_backend.backend_type,
                        'backend_name': blob_backend.backend_name},
                        uid)
        # update the parent container as well
        from vcdm.container import _append_child
        _append_child(parent_container, uid, name)
        blob_backend.create(uid, content)
        log.msg(type='accounting', avatar=avatar, amount=int(content[1]),
                acc_type='blob_creation')
        return (CREATED, uid)
    else:
        uid = vcdm.env['ds'].write({
                        'metadata': metadata,
                        'mimetype': mimetype,
                        'mtime': str(time.time()),
                        'atime': str(time.time()),
                        'size': int(content[1]),  # length
                        'backend_type': blob_backend.backend_type,
                        'backend_name': blob_backend.backend_name},
                        uid)
        blob_backend.update(uid, content)
        log.msg(type='accounting', avatar=avatar, amount=int(content[1]),
                acc_type='blob_update')

        return (OK, uid)


def read(avatar, fullpath, tre_request=False):
    """ Return contents of a blob.
    Returns:
    (HTTP_STATUS_CODE, dictionary_of_metadata)
    """
    uid, vals = vcdm.env['ds'].find_by_path(fullpath, object_type='blob',
                                            fields=['metadata', 'mimetype',
                                                      'mtime', 'size'])
    log.msg("Reading path %s, uid: %s" % (fullpath, uid))
    if uid is None:
        return (NOT_FOUND, None)
    else:
        # authorize call
        acls = vals['metadata'].get('cdmi_acl')
        if not authorize(avatar, fullpath, "read_blob", acls):
            return (UNAUTHORIZED, None)
        # update access time
        vcdm.env['ds'].write({
                        'atime': str(time.time()),
                        },
                        uid)
        log.msg(type='accounting', avatar=avatar, amount=vals['size'],
                acc_type='blob_read')
        vals['uid'] = uid
        # TRE-request?
        if tre_request:
            if not vcdm.env['tre_enabled']:
                return (NOT_IMPLEMENTED, None)
            # XXX only local blob backend supports that at the moment
            vcdm.env['blob'].move_to_tre_server(uid)
            return (FOUND, vals)
        vals['content'] = vcdm.env['blob'].read(uid)
        return (OK, vals)


def delete(avatar, fullpath):
    """ Delete a blob. """
    log.msg("Deleting %s" % fullpath)
    uid, vals = vcdm.env['ds'].find_by_path(fullpath, object_type='blob',
                                            fields=['parent_container',
                                                    'metadata'])
    if uid is None:
        return NOT_FOUND
    else:
        try:
            # authorize call
            acls = vals['metadata'].get('cdmi_acl', None)
            if not authorize(avatar, fullpath, "delete_blob", acls):
                return UNAUTHORIZED
            vcdm.env['blob'].delete(uid)
            vcdm.env['ds'].delete(uid)
            # find parent container and update its children range
            from vcdm.container import _remove_child
            _remove_child(vals['parent_container'], uid)
            log.msg(type='accounting', avatar=avatar, amount=1,
                    acc_type='blob_delete')
            return NO_CONTENT
        except:
            #TODO: - how do we handle failed delete?
            return CONFLICT


def get_stored_size(avatar='Anonymous'):
    """
    Emit into the accounting log total size of all registered blobs
    for an avatar.
    """
    total_size = vcdm.env['ds'].get_total_blob_size(avatar)
    log.msg(type='accounting', avatar=avatar, amount=total_size,
            acc_type='blob_total_size')


def get_stored_size_all_avatars():
    """
    Emit into the accounting log total size of requested blobs for each avatar.
    """
    for av in vcdm.env['ds'].get_all_avatars():
        get_stored_size(av)
