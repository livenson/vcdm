##
# Copyright 2002-2012 Ilja Livenson, PDC KTH
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##
import time
from uuid import uuid4

from twisted.python import log

import vcdm
from vcdm.utils import check_path
from vcdm.authz import authorize

from httplib import NOT_FOUND, OK, CONFLICT, NO_CONTENT, FORBIDDEN, \
    UNAUTHORIZED, NOT_IMPLEMENTED, FOUND, INTERNAL_SERVER_ERROR, CREATED


config = vcdm.config.get_config()


def write(avatar, name, container_path, fullpath, mimetype, metadata, content,
          valueencoding, on_behalf=None, desired_backend=None):
    """ Write or update content of a blob. """
    from vcdm.server.cdmi.generic import get_parent
    parent_container = get_parent(fullpath)

    uid, vals = vcdm.env['ds'].find_by_path(fullpath, object_type='blob',
                                            fields=['parent_container'])
    # assert that we have a consistency in case of an existig blob
    if uid is not None and parent_container != vals['parent_container']:
        log.err("ERROR: Inconsistent information! path: %s, parent_container in db: %s" %
                                                    (fullpath,
                                                     vals['parent_container']))
        return (INTERNAL_SERVER_ERROR, uid)

    # assert we can write to the defined path
    # TODO: expensive check for consistency, make optional
    if config.getboolean('general', 'check_for_existing_parents'):
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
    blob_backend = vcdm.env['blobs'].get(desired_backend, vcdm.env['blob'])

    # add default acls
    if avatar is None:
        avatar = 'Anonymous'
    blob_acl = metadata.get('cdmi_acl')
    if blob_acl is None:
        metadata['cdmi_acl'] = acl  # append parent ACLs for a new folder
    metadata['cdmi_acl'].update({avatar: 'rwd'})  # and creator's ACLs just in case

    # if uid is None, create a new entry, update otherwise
    if uid is None:
        uid = uuid4().hex
        actual_uri = blob_backend.create(uid, content)
        vcdm.env['ds'].write({
                        'object': 'blob',
                        'owner': avatar,
                        'fullpath': fullpath,
                        'mimetype': mimetype,
                        'metadata': metadata,
                        'valuetransferencoding': valueencoding,
                        'filename': name,
                        'actual_uri': actual_uri,
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
        log.msg(type='accounting', avatar=avatar if not on_behalf else on_behalf,
                    amount=int(content[1]), acc_type='blob_creation')
        return (CREATED, uid)
    else:
        actual_uri = blob_backend.update(uid, content)
        uid = vcdm.env['ds'].write({
                        'metadata': metadata,
                        'mimetype': mimetype,
                        'mtime': str(time.time()),
                        'actual_uri': actual_uri,
                        'atime': str(time.time()),
                        'size': int(content[1]),  # length
                        'backend_type': blob_backend.backend_type,
                        'backend_name': blob_backend.backend_name},
                        uid)
        log.msg(type='accounting', avatar=avatar if not on_behalf else on_behalf,
                amount=int(content[1]), acc_type='blob_update')

        return (OK, uid)


def read(avatar, fullpath, tre_request=False, on_behalf=None):
    """ Return contents of a blob.
    Returns:
    (HTTP_STATUS_CODE, dictionary_of_metadata)
    """
    uid, vals = vcdm.env['ds'].find_by_path(fullpath, object_type='blob',
                                            fields=['metadata', 'mimetype',
                                                      'mtime', 'size', 'actual_uri',
                                                    'valuetransferencoding'])
    log.msg("Reading path %s, uid: %s" % (fullpath, uid))
    if uid is None:
        return (NOT_FOUND, None)
    else:
        # authorize call
        acls = vals['metadata'].get('cdmi_acl')
        if not authorize(avatar, fullpath, "read_blob", acls):
            log.msg("Authorization failed for %s on %s (%s)" % (avatar, fullpath, acls))
            return (UNAUTHORIZED, None)
        vals['content'] = vcdm.env['blob'].read(uid)
        # update access time
        vcdm.env['ds'].write({
                        'atime': str(time.time()),
                        },
                        uid)
        log.msg(type='accounting', avatar=avatar if not on_behalf else on_behalf,
                amount=vals['size'], acc_type='blob_read')
        vals['uid'] = uid
        # TRE-request?
        if tre_request:
            if not vcdm.env['tre_enabled']:
                return (NOT_IMPLEMENTED, None)
            # XXX only local blob backend supports that at the moment
            vcdm.env['blob'].move_to_tre_server(uid)
            return (FOUND, vals)
        return (OK, vals)


def delete(avatar, fullpath, on_behalf=None):
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
            log.msg(type='accounting', avatar=avatar if not on_behalf else on_behalf,
                    amount=1, acc_type='blob_delete')
            return NO_CONTENT
        except:
            #TODO: - how do we handle failed delete?
            return CONFLICT


def get_stored_size(avatar='Anonymous'):
    """
    Emit into the accounting log total size of all registered blobs
    for an avatar.
    """
    end_time = time.time()
    start_time = end_time - vcdm.conf.getfloat('general', 'accounting.total_frequency')

    total_size = vcdm.env['ds'].get_total_blob_size(start_time, end_time, avatar)
    log.msg(type='accounting', avatar=avatar, amount=total_size, start_time=start_time, end_time=end_time,
            acc_type='blob_total_size')


def get_stored_size_all_avatars():
    """
    Emit into the accounting log total size of requested blobs for each avatar.
    """
    for av in vcdm.env['ds'].get_all_avatars():
        get_stored_size(av)
