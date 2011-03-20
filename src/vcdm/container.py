import datetime
import vcdm
from vcdm.errors import ProtocolError, InternalError

def read(fullpath): 
    """ Read a specified container."""
    uid, vals = vcdm.env['ds'].find_by_path(fullpath, object_type = 'container', fields = ['children', 'metadata'])
    if uid is None:
        # XXX refactor return of the result
        return (vcdm.NOT_FOUND, None, None, None)    
    else:
        return (vcdm.OK, uid, vals['children'], vals['metadata'])

def create_or_update(container_path, path, metadata = None):
    """Create or update a container."""
    parent_container = '/'.join(container_path)
    fullpath = parent_container + path
    
    uid, vals = vcdm.env['ds'].find_by_path(path, object_type = 'container', fields = ['children', 'parent_container'])
    
    # XXX duplication of checks with blob (vcdm). Refactor.
    
    if uid is not None and parent_container != vals['parent_container']:
        raise InternalError("Inconsistent information about the object! path: %s, parent_container in db: %s") % (fullpath, vals['parent_container'])
    
    # assert we can write to the defined path
    if not check_path(container_path):
        raise ProtocolError("Writing to a container is not allowed. Container path: %s" % '/'.join(container_path))
    
    if uid is None:
        # if uid is None, it shall create a new entry, update otherwise        
        uid = vcdm.env['ds'].write({
                        'object': 'container',            
                        'container_name': path,
                        'children': [],
                        'ctime': str(datetime.datetime.now())},                        
                        uid)
        # update the parent container as well
        append_child(parent_container, uid)
        return (vcdm.CREATED, uid, [])
    else:
        # update container
        uid = vcdm.env['ds'].write({
                        'metadata': metadata,
                        'mtime': str(datetime.datetime.now())},
                        uid)
        
        return (vcdm.OK, uid, vals['children'])

def delete(path):
    """ Delete a container."""
    uid, vals = vcdm.env['ds'].find_by_path(path, object_type = 'container', fields = ['children', 'parent_container'])
    if uid is None:
        return vcdm.NOT_FOUND
    else:
        # fail if we are deleting a non-empty container
        if len(vals['children']) != 0:
            raise ProtocolError("Cannot delete a non-empty container '%s'" %path)
        vcdm.env['ds'].delete(uid)  
        remove_child(vals['parent_container'], uid)          
        ## XXX: delete all children?
        return vcdm.OK

####### Support functions dealing with container logic #########

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

def append_child(container_path, child_uid):
    cuid, cvals = vcdm.env['ds'].find_by_path(container_path, object_type = 'container', fields = ['children'])
    vcdm.env['ds'].write({
                    'children': cvals['children'].append(child_uid)},
                    cuid)
    
def remove_child(container_path, child_uid):
    cuid, cvals = vcdm.env['ds'].find_by_path(container_path, object_type = 'container', fields = ['children'])
    vcdm.env['ds'].write({
                    'children': cvals['children'].remove(child_uid)},
                    cuid)
    