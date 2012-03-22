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

conf = vcdm.config.get_config()


class SimpleRealm(object):
    """
    A realm which gives out L{RootResource} instances for authenticated users.
    """
    implements(IRealm)

    def requestAvatar(self, avatarId, mind, *interfaces):
        if resource.IResource in interfaces:
            return resource.IResource, RootCDMIResource(avatarId), lambda: None
        raise NotImplementedError()


def load_blob_backends():
    # compulsory localdisk backend
    from vcdm.backends.blob.localdisk import POSIXBlob
    vcdm.blob_backends = {'local': POSIXBlob}
    # optional backends, some require presence of additional plugins
    try:
        from vcdm.backends.blob.aws_s3 import S3Blob
        vcdm.blob_backends['aws'] = S3Blob
    except ImportError:
        print "AWS back-end type not available"
    try:
        from vcdm.backends.blob.azure import AzureBlob
        vcdm.blob_backends['azure'] = AzureBlob
    except ImportError:
        print "Azure back-end type not available"
    try:
        from vcdm.backends.blob.cdmi import CDMIBlob
        vcdm.blob_backends['cdmi'] = CDMIBlob
    except ImportError:
        print "CDMI back-end type not available"


def load_mq_backends():
    if conf.getboolean('general', 'support_mq') and \
            conf.get('general', 'mq.backend') == 'local':
        from vcdm.backends.mq.amqp import AMQPMQ
        vcdm.mq_backends['amqp'] = AMQPMQ

    if conf.getboolean('general', 'support_mq') and \
            conf.get('general', 'mq.backend') == 'aws':
        from vcdm.backends.mq.aws_sqs import AWSSQSMessageQueue
        vcdm.mq_backends['aws'] = AWSSQSMessageQueue


def load_ds_backends():
    # datastore backends
    if conf.get('general', 'ds.backend') == 'couchdb':
        from vcdm.backends.datastore.couchdb_store import CouchDBStore
        vcdm.datastore_backends['couchdb'] = CouchDBStore


def main():
    # setup logging
    log.startLogging(open(conf.get('general', 'common_log'), 'a'), setStdout=False)
    acclog = AccountingLogObserver(open(conf.get('general', 'accounting_log'), 'a'))
    log.addObserver(acclog.emit)

    # load backends
    load_blob_backends()
    load_mq_backends()
    load_ds_backends()

    # initialize backends
    vcdm.env['ds'] = vcdm.datastore_backends[conf.get('general', 'ds.backend')]()

    # load all backends
    for blob_backend in conf.get('general', 'blob.backends').split(','):
        blob_backend = blob_backend.strip()
        log.msg("Activating %s backend." % blob_backend)
        backend_type = conf.get(blob_backend, 'type')
        vcdm.env['blobs'][blob_backend] = vcdm.blob_backends[backend_type](blob_backend)

    # set default
    def_backend = conf.get('general', 'blob.default.backend')
    print "Setting default backend to %s (%s)" % (def_backend, conf.get(def_backend, 'type'))
    vcdm.env['blob'] = vcdm.env['blobs'][def_backend]
    # initiate accounting logging
    task.LoopingCall(vcdm.blob.get_stored_size_all_avatars). \
                    start(conf.getfloat('general', 'accounting.total_frequency'))  #in seconds

    # do we want queue backend? just a single one at the moment
    if conf.getboolean('general', 'support_mq'):
        vcdm.env['mq'] = vcdm.mq_backends[conf.get('general', 'mq.backend')]()
        current_capabilities.system['queues'] = True

    def _hash(name, clearpsw, hashedpsw):
        import hashlib
        return  hashlib.md5(clearpsw).hexdigest()

    used_checkers = []
    authn_methods = []
    interface_for_binding = conf.get('general', 'server.endpoint').split(":")[0]

    if conf.has_option('general', 'usersdb.plaintext'):
        print "Using plaintext users DB from '%s'" % conf.get('general', 'usersdb.plaintext')
        used_checkers.append(FilePasswordDB(conf.get('general', 'usersdb.plaintext'),
                                            cache=True))
        authn_methods.append(guard.DigestCredentialFactory('md5',
                                            conf.get('general', 'server.endpoint')))
    elif conf.has_option('general', 'usersdb.md5'):
        print "Using md5-hashed users DB from '%s'" % conf.get('general', 'usersdb.md5')
        used_checkers.append(FilePasswordDB(conf.get('general', 'usersdb.md5'),
                                                       hash=_hash, cache=True))
        authn_methods.append(guard.BasicCredentialFactory(conf.get('general', 'server.endpoint')))

    wrapper = guard.HTTPAuthSessionWrapper(Portal(SimpleRealm(), used_checkers),
                                           authn_methods)

    print "Binding to interface %s" % interface_for_binding
    # unencrypted/unprotected connection for testing/development
    if conf.getboolean('general', 'server.use_debug_port'):
        reactor.listenTCP(conf.getint('general', 'server.debug_port', 2364),
                          server.Site(resource=RootCDMIResource()), interface=interface_for_binding)
        reactor.listenTCP(conf.getint('general', 'server.debug_port_authn', 2365),
                          server.Site(resource=wrapper), interface=interface_for_binding)

    # 1-way SSL for production
    from twisted.internet import ssl
    sslContext = ssl.DefaultOpenSSLContextFactory(conf.get('general', 'server.credentials.key'),
                                                  conf.get('general', 'server.credentials.cert'))
    reactor.listenSSL(int(conf.get('general', 'server.endpoint').split(":")[1]),
                      server.Site(resource=wrapper), contextFactory=sslContext, interface=interface_for_binding)

    reactor.run()

if __name__ == '__main__':
    main()
