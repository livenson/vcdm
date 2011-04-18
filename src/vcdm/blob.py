import datetime
import vcdm

from vcdm import container
from vcdm.errors import ProtocolError, InternalError
from vcdm.container import append_child, remove_child
from vcdm.server.cdmi.generic import get_parent
from httplib import NOT_FOUND, CREATED, OK, CONFLICT

def write(name, container_path, fullpath, mimetype, metadata, content):
    """ Write or update content of a blob. """
    parent_container = get_parent(fullpath)
    
    uid, vals = vcdm.env['ds'].find_by_path(fullpath, object_type = 'blob', fields = ['parent_container'])
    # assert that we have a consistency in case of an existig blob
    if uid is not None and parent_container != vals['parent_container']:
        raise InternalError("Inconsistent information about the object! path: %s, parent_container in db: %s") % (fullpath, vals['parent_container'])

    # assert we can write to the defined path
    if not container.check_path(container_path):
        raise ProtocolError("Writing to a container is not allowed. Container path: %s" % '/'.join(container_path))
            
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
        append_child(parent_container, uid, name)
        
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

def read(fullpath, range = None):
    """ Return contents of a blob."""
    uid, vals = vcdm.env['ds'].find_by_path(fullpath, object_type = 'blob', fields = ['metadata', 'mimetype'])    
    if uid is None:
        return (NOT_FOUND, None, None, None, None)
    else:        
        return (OK, vcdm.env['blob'].read(uid, range), uid, vals['mimetype'], vals['metadata'])

def delete(fullpath):
    """ Delete a blob. """
    uid, vals = vcdm.env['ds'].find_by_path(fullpath, object_type = 'blob', fields = ['parent_container'])
    if uid is None:
        return NOT_FOUND
    else:
        try:
            vcdm.env['blob'].delete(uid)
            vcdm.env['ds'].delete(uid)
            # find parent container and update its children range
            remove_child(vals['parent_container'], uid)
            return OK
        except:
            #TODO: - how do we handle failed delete?     
            return CONFLICT
