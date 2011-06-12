from twisted.python import log
from vcdm import c

def authorize(avatar, resource, action, acls=None):
    """ Top-level authorize function dispatching calls to the configured authZ mechanism."""
    try:    
        return mechanisms[c('general', 'server.authz')](avatar, resource, action, acls)
    except KeyError:
        log.err("Requested authZ mechanism %s was not found.")
        return False # default failover 

### Implementations ###
def dummy(avatar, resource, action, acls):
    log.msg("Authorizing %s to perform %s on %s. ACLs: %s" %(avatar, action, resource, acls))
    return True

# map of all possible mechanisms
mechanisms = {'dummy': dummy}