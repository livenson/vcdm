import datetime
import vcdm

ds = vcdm.datastore_backends[vcdm.config.get('general', 'ds.backend')]

def create(path):
    docid = ds.write({'container_name': path, 
		              'creation_data': str(datetime.datetime.now())})
    return docid

def read(fnm): 
    """ Return contents of a file."""
    uid = ds.find_uid(fnm)
    # TODO: return container metadata
    return (vcdm.OK, None)  


def write(fnm, content, metadata = None):
    """Write or update container."""
    try:
        uid = ds.find_uid(fnm)
        print "uid is now: ", uid
        # if uid is None, it shall create a new entry, update otherwise        
        uid = ds.write({'container_name': fnm,
                        'date_created': str(datetime.datetime.now())}, 
                        uid)
        return (vcdm.CREATED, uid)
    except:
        # TODO: do a cleanup?
        import sys        
        print sys.exc_info()
        return (vcdm.CONFLICT, None)

def delete(fnm):
    """ Delete a container. """
    uid = ds.find_uid(fnm)
    if uid is None:
        return (vcdm.NOT_FOUND, None)
    else:
        try:        
            ds.delete(uid)
            return (vcdm.OK, None)
        except:
            #TODO - how do we handle failed delete?            
            return (vcdm.CONFLICT, None)


