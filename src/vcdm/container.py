import datetime
import vcdm

ds = vcdm.datastore_backends[vcdm.config.get('general', 'ds.backend')]

def create(path):
    docid = ds.write({'container_name': path, 
		      'creation_data': str(datetime.datetime.now())})
    return docid


def update(smth):
	pass 

def read(fnm): 
    """ Return contents of a file."""
    uid = ds.find_uid(fnm)
    if uid is None:
        return (vcdm.NOT_FOUND, None)
    else:
        return (vcdm.OK, backend.read(uid))    


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


