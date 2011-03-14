import datetime
import vcdm

def write(fnm, content, metadata = None):
    """Write or update content."""
    try:
        uid = vcdm.env['ds'].find_uid(fnm)
        print "uid is now: ", uid
        # if uid is None, it shall create a new entry, update otherwise
        # TODO: collect correct metadata        
        uid = vcdm.env['ds'].write({'filename': fnm, 
                            'date_created': str(datetime.datetime.now()), 
                            'acl': '777',
                            'size': len(content),
                            'backend_type': vcdm.env['blob'].backend_type}, uid)
        vcdm.env['blob'].create(uid, content)
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
    uid = vcdm.env['ds'].find_uid(fnm)
    if uid is None:
        return (vcdm.NOT_FOUND, None)
    else:
        return (vcdm.OK, vcdm.env['blob'].read(uid, rng))

def delete(fnm):
    """ Delete a file. """
    uid = vcdm.env['ds'].find_uid(fnm)
    if uid is None:
        return (vcdm.NOT_FOUND, None)
    else:
        try:
            vcdm.env['blob'].delete(uid)
            vcdm.env['ds'].delete(uid)
            return (vcdm.OK, None)
        except:
            #TODO - how do we handle failed delete?            
            return (vcdm.CONFLICT, None)

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
