from interfaces.blob import IBlob


from lib import winazurestorage
import urllib2

class AzureBlob(IBlob):
    
    backend_type = 'azure'
    
    conn = None

    def __init__(self, initialize_storage=False):
        self.conn = winazurestorage.BlobStorage()
        if initialize_storage:
            self.conn.create_container('vcdm')

    def read(self, fnm, rng=None):
        return self.conn.get_blob(u'vcdm', unicode(fnm))
    
    def write(self, fnm, content):
        self.conn.put_blob(u'vcdm', unicode(fnm), content, 'text/plain')
    
    def delete(self, fnm):
        try:
            self.conn.delete_blob(u'vcdm', unicode(fnm))
        except urllib2.HTTPError:
            # TODO: winazure lib seems to be passing also positive responses via exceptions. Need to clarify
            import sys
            print "====================="
            print sys.exc_info()
            print "====================="