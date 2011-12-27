from zope.interface import implements

from twisted.python import log
from twisted.internet import reactor
from twisted.web import server, resource, guard
from twisted.cred.portal import IRealm, Portal
from twisted.cred.checkers import FilePasswordDB 
from twisted.internet import task

import vcdm
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
    log.startLogging(open(vcdm.config.get('general', 'common_log'), 'a'), setStdout=False)
    acclog = AccountingLogObserver(open(vcdm.config.get('general', 'accounting_log'), 'a'))
    log.addObserver(acclog.emit)

    # initialize backends
    vcdm.env['ds'] = vcdm.datastore_backends[vcdm.config.get('general', 'ds.backend')]()

    # load all backends
    for blob_backend in vcdm.config.get('general', 'blob.backends').split(','):
        blob_backend = blob_backend.strip()
        log.msg("Activating %s backend." % blob_backend)
        backend_type = vcdm.config.get(blob_backend, 'type')
        vcdm.env['blobs'][blob_backend] = vcdm.blob_backends[backend_type](blob_backend)

    # set default
    vcdm.env['blob'] = vcdm.env['blobs'][vcdm.config.get('general', 'blob.default.backend')]
    # initiate accounting logging
    task.LoopingCall(vcdm.blob.get_stored_size_all_avatars). \
                    start(float(vcdm.config.get('general', 'accounting.total_frequency'))) #in seconds
    
    # do we want queue backend? just a single one at the moment
    if vcdm.config.getboolean('general', 'support_mq'):
        vcdm.env['mq'] = vcdm.mq_backends[vcdm.config.get('general', 'mq.backend')]()
        current_capabilities.system['queues'] = True
    # for now just a small list of 
    def _hash(name, clearpsw, hashedpsw):
        import hashlib
        return  hashlib.md5(clearpsw).hexdigest()

    used_checkers = []
    authn_methods = []
    if vcdm.config.has_option('general', 'usersdb.plaintext'):
        used_checkers.append(FilePasswordDB(vcdm.config.get('general', 'usersdb.plaintext'),
                                            cache=True))
        authn_methods.append(guard.DigestCredentialFactory('md5', 
                                            vcdm.config.get('general', 'server.endpoint')))

    if vcdm.config.has_option('general', 'usersdb.md5'):
        used_checkers.append(FilePasswordDB(vcdm.config.get('general', 'usersdb.md5'),
                                                       hash=_hash, cache=True))
        authn_methods.append(guard.BasicCredentialFactory(vcdm.config.get('general', 
                                                                          'server.endpoint')))

    wrapper = guard.HTTPAuthSessionWrapper(Portal(SimpleRealm(), used_checkers),
                                           authn_methods)

    # unencrypted/unprotected connection for testing/development
    if vcdm.config.getboolean('general', 'server.use_debug_port'):
        reactor.listenTCP(vcdm.config.getint('general', 'server.debug_port', 2364),
                          server.Site(resource=RootCDMIResource()))
        reactor.listenTCP(vcdm.config.getint('general', 'server.debug_port_authn', 2365), 
                          server.Site(resource=wrapper))
    
    # 1-way SSL for production
    from twisted.internet import ssl
    sslContext = ssl.DefaultOpenSSLContextFactory('server_credentials/key.pem',
                                                  'server_credentials/cert.pem')
    reactor.listenSSL(int(vcdm.config.get('general', 'server.endpoint').split(":")[1]),
                      server.Site(resource=wrapper), contextFactory = sslContext)

    reactor.run()

if __name__ == '__main__':
    main()
