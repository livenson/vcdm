from zope.interface import implements

from twisted.python import log
from twisted.internet import reactor
from twisted.web import server, resource, guard
from twisted.cred.portal import IRealm, Portal
from twisted.cred.checkers import FilePasswordDB 

import vcdm
from vcdm import c
from vcdm.server.cdmi.root import RootCDMIResource
from vcdm.server.cdmi import current_capabilities

class SimpleRealm(object):
    """
    A realm which gives out L{RootResource} instances for authenticated users.
    """
    implements(IRealm)

    def requestAvatar(self, avatarId, mind, *interfaces):
        if resource.IResource in interfaces:
            return resource.IResource, RootCDMIResource(), lambda: None
        raise NotImplementedError()
    
def main():
    log.startLogging(open('vcdm.log', 'a'), setStdout=False)
    
    # initialize backends
    vcdm.env['ds'] = vcdm.datastore_backends[c('general', 'ds.backend')]()
    vcdm.env['blob'] = vcdm.blob_backends[c('general', 'blob.backend')]()
    # do we want queue backend?
    if c('general', 'support_mq') == 'yes':
        vcdm.env['mq'] = vcdm.mq_backends[c('general', 'mq.backend')]()
        current_capabilities.system['queues'] = True
    # for now just a small list of 
    checkers = [FilePasswordDB('users.db')]
    
    wrapper = guard.HTTPAuthSessionWrapper(
        Portal(SimpleRealm(), checkers),
        [guard.DigestCredentialFactory('md5', c('general', 'server.endpoint'))])
    
    # TODO: configure reactor to use
    # http://twistedmatrix.com/documents/current/core/howto/choosing-reactor.html
    
    # unencrypted/unprotected connection for testing/development
    if c('general', 'server.use_debug_port') == 'yes':      
        reactor.listenTCP(int(c('general', 'server.debug_port')), server.Site(resource=RootCDMIResource()))
    
    # 1-way SSL for production
    from twisted.internet import ssl
    sslContext = ssl.DefaultOpenSSLContextFactory('server_credentials/key.pem','server_credentials/cert.pem')
    reactor.listenSSL(int(c('general', 'server.endpoint').split(":")[1]), server.Site(resource=wrapper), contextFactory = sslContext)
        
    # connector for providing quick metainfo
    #from vcdm.server.meta.info import InfoResource
    # TODO: fix InfoResource
    #reactor.listenTCP(8083, server.Site(resource = InfoResource()))
    
    reactor.run()

if __name__ == '__main__':
    main()
