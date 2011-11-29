from zope.interface import implements

from twisted.python import log
from twisted.internet import reactor
from twisted.web import server, resource, guard
from twisted.cred.portal import IRealm, Portal
from twisted.cred.checkers import FilePasswordDB 
from twisted.internet import task

import vcdm
from vcdm import c
from vcdm.server.cdmi.root import RootCDMIResource
from vcdm.server.cdmi import current_capabilities
from vcdm.utils import AccountingLogObserver

class SimpleRealm(object):
    """
    A realm which gives out L{RootResource} instances for authenticated users.
    """
    implements(IRealm)

    def requestAvatar(self, avatarId, mind, *interfaces):
        if resource.IResource in interfaces:
            return resource.IResource, RootCDMIResource(avatarId), lambda: None
        raise NotImplementedError()
    
def main():
    # setup logging
    log.startLogging(open(c('general', 'common_log'), 'a'), setStdout=False)
    acclog = AccountingLogObserver(open(c('general', 'accounting_log'), 'a'))
    log.addObserver(acclog.emit)

    # initialize backends
    vcdm.env['ds'] = vcdm.datastore_backends[c('general', 'ds.backend')]()
    
    # load all backends
    for blob_backend in c('general', 'blob.backends').split(','):
        blob_backend = blob_backend.strip()
        log.msg("Activating %s backend." % blob_backend)
        type = c(blob_backend, 'type')
        vcdm.env['blobs'][blob_backend] = vcdm.blob_backends[type](blob_backend)
    
    # set default
    vcdm.env['blob'] = vcdm.env['blobs'][c('general', 'blob.default.backend')]  
    # initiate blob logging
    task.LoopingCall(vcdm.blob.get_stored_size_all_avatars).start(float(c('general', 'accounting.total_frequency'))) #in seconds
    
    # do we want queue backend? just a single one at the moment
    if c('general', 'support_mq') == 'yes':
        vcdm.env['mq'] = vcdm.mq_backends[c('general', 'mq.backend')]()
        current_capabilities.system['queues'] = True
    # for now just a small list of 
    def _hash(name, clearpsw, hashedpsw):
        import hashlib
        return  hashlib.md5(clearpsw).hexdigest()

    checkers = [FilePasswordDB(c('general', 'usersdb.plaintext'), cache=True), 
                FilePasswordDB(c('general', 'usersdb.md5'), hash=_hash, cache=True)]
    
    wrapper = guard.HTTPAuthSessionWrapper(
        Portal(SimpleRealm(), checkers),
        [guard.BasicCredentialFactory(c('general', 'server.endpoint')),
         guard.DigestCredentialFactory('md5', c('general', 'server.endpoint'))])
    
    # TODO: configure reactor to use
    # http://twistedmatrix.com/documents/current/core/howto/choosing-reactor.html
    
    # unencrypted/unprotected connection for testing/development
    if c('general', 'server.use_debug_port') == 'yes':      
        reactor.listenTCP(int(c('general', 'server.debug_port')), server.Site(resource=RootCDMIResource()))
        reactor.listenTCP(2365, server.Site(resource=wrapper))
    
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
