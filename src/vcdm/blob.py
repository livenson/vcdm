import datetime
import vcdm

from vcdm import container
from twisted.python import log
from vcdm.container import _append_child, _remove_child
from vcdm.server.cdmi.generic import get_parent

from httplib import NOT_FOUND, CREATED, OK, CONFLICT, NO_CONTENT, FORBIDDEN
from vcdm.authz import authorize


def write(avatar, name, container_path, fullpath, mimetype, metadata, content):
    """ Write or update content of a blob. """
    parent_container = get_parent(fullpath)
    
    uid, vals = vcdm.env['ds'].find_by_path(fullpath, object_type = 'blob', fields = ['parent_container'])
    # assert that we have a consistency in case of an existig blob
    if uid is not None and parent_container != vals['parent_container']:
        log.err("Inconsistent information about the object! path: %s, parent_container in db: %s" % (fullpath, vals['parent_container']))
        return (FORBIDDEN, uid)    

    # assert we can write to the defined path
    # TODO: expensive check for consistency, make optional 
    if not container.check_path(container_path):
        log.err("Writing to a container is not allowed. Container path: %s" % '/'.join(container_path))
        return (FORBIDDEN, uid)
    
    # authorize call, take parent permissions     
    _, cvals = vcdm.env['ds'].find_by_path(parent_container, object_type = 'container', fields = ['metadata'])
    acl = cvals['metadata'].get('cdmi_acl', None)
    if not authorize(avatar, parent_container, "write_blob", acl):
        log.err("Authorization failed.")
        return (FORBIDDEN, uid)
    
    # if uid is None, create a new entry, update otherwise
    if uid is None:         
        uid = vcdm.env['ds'].write({
                        'object': 'blob',
                        'fullpath': fullpath,
                        'mimetype': mimetype,
                        'metadata': metadata, 
                        'filename': name,
                        'parent_container': parent_container, 
                        'ctime': str(datetime.datetime.now()), 
                        'mtime': str(datetime.datetime.now()),
                        'size': len(content),
                        'backend_type': vcdm.env['blob'].backend_type},                                    
                        uid)
        # update the parent container as well
        _append_child(parent_container, uid, name)
        
        vcdm.env['blob'].create(uid, content)
        return (CREATED, uid)
    else:
        uid = vcdm.env['ds'].write({                        
                        'metadata': metadata,
                        'mimetype': mimetype,
                        'mtime': str(datetime.datetime.now()), 
                        'size': len(content),
                        'backend_type': vcdm.env['blob'].backend_type}, 
                        uid)        
        vcdm.env['blob'].update(uid, content)
        return (OK, uid)

def read(avatar, fullpath, range = None):
    """ Return contents of a blob."""
    uid, vals = vcdm.env['ds'].find_by_path(fullpath, object_type = 'blob', fields = ['metadata', 'mimetype', 'ctime', 'size'])
    log.msg("Reading path %s, uid: %s" % (fullpath, uid))
    if uid is None:
        return (NOT_FOUND, None, None, None, None)
    else:        
        # authorize call    
        acls = vals['metadata'].get('cdmi_acl', None)    
        if not authorize(avatar, fullpath, "read_blob", acls):
            log.err("Authorization failed.")        
            return (FORBIDDEN, None, None, None, None)
        ##print datetime.datetime.strptime(vals['ctime'], "YYYY-MM-DD HH:MM:SS.mmmmmm")        
        return (OK, vcdm.env['blob'].read(uid, range), uid, vals['mimetype'], vals['metadata'])

def delete(avatar, fullpath):
    """ Delete a blob. """
    log.msg("Deleting %s", fullpath)
    uid, vals = vcdm.env['ds'].find_by_path(fullpath, object_type = 'blob', fields = ['parent_container', 'metadata'])
    if uid is None:
        return NOT_FOUND
    else:
        try:
            # authorize call
            acls = vals['metadata'].get('cdmi_acl', None)    
            if not authorize(avatar, fullpath, "delete_blob", acls):
                log.err("Authorization failed.")
                return FORBIDDEN
            vcdm.env['blob'].delete(uid)
            vcdm.env['ds'].delete(uid)
            # find parent container and update its children range
            _remove_child(vals['parent_container'], uid)
            return NO_CONTENT
        except:
            #TODO: - how do we handle failed delete?     
            return CONFLICT
