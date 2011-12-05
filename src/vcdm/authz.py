from twisted.python import log

from vcdm import c


def authorize(avatar, resource, action, acls=None):
    """ Top-level authorize function dispatching calls to the configured authZ mechanism."""
    try:    
        result = mechanisms[c('general', 'server.authz')](avatar, resource, action, acls)
        log.err("Authorized request: %s" %result)
        return result
    except KeyError:
        log.err("Requested authZ mechanism %s was not found.")
        return False # default failover 

### Implementations ###
def dummy(avatar, resource, action, acls):
    log.msg("Dummy authorization of %s to perform %s on %s. ACLs: %s" %(avatar, action, resource, acls))
    return True

def strict(avatar, resource, action, acls):
    """Only allows operation if a user has the corresponding bit set"""
    log.msg("Strict authorization of %s to perform %s on %s. ACLs: %s" %(avatar, action, resource, acls))
    if resource == '/':
        return True # allow everything for the root folder
    if acls is None:
        return False # disallowed by default
    for prefix in ['read','write','delete']:
        if action.startswith(prefix):
            user_acls = acls.get(avatar)
            if user_acls is None:
                return False # disallowed by default
            return rights[prefix] in user_acls
    return False

# map of all possible mechanisms
mechanisms = {'dummy': dummy,
              'strict': strict}

rights = {'read': 'r',
          'write' : 'w',
          'delete': 'd'}
