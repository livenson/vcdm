import datetime
import vcdm

from vcdm import container
from vcdm.errors import ProtocolError

def write(container_path, filename, mimetype, metadata, content):
    """Write or update content of a blob"""
    fullpath = ''.join(container_path) + filename
    uid = vcdm.env['ds'].find_uid(fullpath)
    if not container.check_path(container_path):
        raise ProtocolError("Container path is wrong.")
            
    # if uid is None, it shall create a new entry, update otherwise
    # TODO: collect correct metadata        
    uid = vcdm.env['ds'].write({
                        'object': 'blob',
                        'fullpath': '/'.join(container_path) + filename,
                        'mimetype': mimetype,
                        'metadata': metadata, 
                        'filename': filename, 
                        'date_created': str(datetime.datetime.now()), 
                        'size': len(content),
                        'backend_type': vcdm.env['blob'].backend_type}, 
                        uid)
    vcdm.env['blob'].create(uid, content)
    return (vcdm.CREATED, uid)

def read(fnm, rng=None):
    """ Return contents of a file."""
    uid, vals = vcdm.env['ds'].find_uid(fnm, ['metadata', 'mimetype'])    
    if uid is None:
        return (vcdm.NOT_FOUND, None, uid, None, None)
    else:
        return (vcdm.OK, vcdm.env['blob'].read(uid, rng), uid, vals['metadata'], vals['mimetype'])

def delete(fnm):
    """ Delete a file. """
    uid = vcdm.env['ds'].find_uid(fnm)
    if uid is None:
        return vcdm.NOT_FOUND
    else:
        try:
            vcdm.env['blob'].delete(uid)
            vcdm.env['ds'].delete(uid)
            return vcdm.OK
        except:
            #TODO - how do we handle failed delete?            
            return vcdm.CONFLICT

def readdir(path):
    # TODO: return a list of tuples (name, attrs, offset)
    uidlist = vcdm.env['ds'].find_uid_match(path)
    return uidlist

def find(path, pattern):
    uidlist = vcdm.env['ds'].find_uid_pattern(path, pattern)
    if uidlist is None:
        return (vcdm.NOT_FOUND, None)
    else:
        return (vcdm.OK, uidlist)
