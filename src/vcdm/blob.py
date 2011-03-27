import datetime
import vcdm

from vcdm import container
from vcdm.errors import ProtocolError, InternalError
from vcdm.interfaces.objects import Blob
from vcdm.container import append_child, remove_child

def write(container_path, filename, mimetype, metadata, content):
    """Write or update content of a blob"""
    parent_container = '/'.join(container_path)
    if parent_container == '':
        parent_container = '/' # a small hack for the top-level container
    fullpath = parent_container + '/' + filename
        
    uid, vals = vcdm.env['ds'].find_by_path(fullpath, object_type = 'blob', fields = 'parent_container')
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
                        'path': filename,
                        'fullpath': fullpath,
                        'mimetype': mimetype,
                        'metadata': metadata, 
                        'filename': filename,
                        'parent_container': parent_container, 
                        'ctime': str(datetime.datetime.now()), 
                        'mtime': str(datetime.datetime.now()),
                        'size': len(content),
                        'backend_type': vcdm.env['blob'].backend_type}, 
                        uid)
        # update the parent container as well
        append_child(parent_container, uid, filename)
        
        vcdm.env['blob'].create(uid, content)
        return (vcdm.CREATED, uid)
    else:
        uid = vcdm.env['ds'].write({                        
                        'metadata': metadata,
                        'mimetype': mimetype,
                        'mtime': str(datetime.datetime.now()), 
                        'size': len(content),
                        'backend_type': vcdm.env['blob'].backend_type}, 
                        uid)        
        vcdm.env['blob'].update(uid, content)
        return (vcdm.OK, uid)

def read(fullpath, range = None):
    """ Return contents of a blob."""
    uid, vals = vcdm.env['ds'].find_by_path(fullpath, object_type = 'blob', fields = ['metadata', 'mimetype'])    
    if uid is None:
        return (vcdm.NOT_FOUND, None, None, None, None)
    else:        
        return (vcdm.OK, vcdm.env['blob'].read(uid, range), uid, vals['mimetype'], vals['metadata'])

def delete(fullpath):
    """ Delete a blob. """
    uid, vals = vcdm.env['ds'].find_by_path(fullpath, object_type = 'blob', fields = ['parent_container'])
    if uid is None:
        return vcdm.NOT_FOUND
    else:
        try:
            vcdm.env['blob'].delete(uid)
            vcdm.env['ds'].delete(uid)
            # find parent container and update its children range
            remove_child(vals['parent_container'], uid)
            return vcdm.OK
        except:
            #TODO - how do we handle failed delete?     
            return vcdm.CONFLICT
