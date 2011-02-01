import datetime
import vcdm

backend = vcdm.blob_backends[vcdm.config.get('general', 'blob.backend')]
ds = vcdm.datastore_backends[vcdm.config.get('general', 'ds.backend')]

def write(fnm, content, metadata = None):
    """Write or update content."""
    try:
        uid = ds.find_uid(fnm)
        print "uid is now: ", uid
        # if uid is None, it shall create a new entry, update otherwise        
        uid = ds.write({'filename': fnm, 
                            'date_created': str(datetime.datetime.now()), 
                            'acl': '777',
                            'size': len(content),
                            'backend_type': backend.backend_type}, uid)
        backend.write(uid, content)
        return (vcdm.CREATED, uid)
    except:
        # TODO: do a cleanup?
        import sys
        print "====================="
        print sys.exc_info()
        print "====================="
        return (vcdm.CONFLICT, None)

def read(fnm, rng=None):
    """ Return contents of a file."""
    uid = ds.find_uid(fnm)
    if uid is None:
        return (vcdm.NOT_FOUND, None)
    else:
        return (vcdm.OK, backend.read(uid, rng))

def delete(fnm):
    """ Delete a file. """
    uid = ds.find_uid(fnm)
    if uid is None:
        return (vcdm.NOT_FOUND, None)
    else:
        try:
            backend.delete(uid)
            ds.delete(uid)
            return (vcdm.OK, None)
        except:
            #TODO - how do we handle failed delete?            
            return (vcdm.CONFLICT, None)

def readdir(path):
    # TODO: return a list of tuples (name, attrs, offset)
    uidlist = ds.find_uid_match(path)
    return uidlist

def find(path, pattern):
    uidlist = ds.find_uid_pattern(path, pattern)
    if uidlist is None:
        return (vcdm.NOT_FOUND, None)
    else:
        return (vcdm.OK, uidlist)
