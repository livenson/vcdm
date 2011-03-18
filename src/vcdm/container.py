import datetime
import vcdm

from vcdm import c


def read(fnm): 
    """ Return contents of a file."""
    uid = vcdm.env['ds'].find_uid(fnm)
    # TODO: return container metadata
    return (vcdm.OK, None)  


def create_or_update(fnm, content, metadata = None):
    """Create or update a container."""
    try:
        uid = vcdm.env['ds'].find_uid(fnm)
        print "uid is now: ", uid
        # if uid is None, it shall create a new entry, update otherwise        
        uid = vcdm.env['ds'].write({
                        'object': 'container',            
                        'container_name': fnm,
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
    uid = vcdm.env['ds'].find_uid(fnm)
    if uid is None:
        return (vcdm.NOT_FOUND, None)
    else:
        try:
            vcdm.env['ds'].delete(uid)
            return (vcdm.OK, None)
        except:
            #TODO - how do we handle failed delete?            
            return (vcdm.CONFLICT, None)

def check_path(container_path):
    # XXX: probably not the best way to do the search, but seems to work
    # construct all possible fullpaths of containers and do a search for them
    all_paths = []
    for i in len(container_path):
        all_paths.append('/'.join(container_path[0:i]))
    # For now ignore all the permissions/etc. Just make sure that all path are there
    # TODO: add permission checking, probably would mean changing a query a bit to return more information        
    if len(vcdm.env['ds'].find_path_uids(all_paths)) != len(container_path):
        return False
    else:
        return True

    
    