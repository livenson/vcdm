from vcdm.interfaces.blob import IBlob
from libazure.azure_storage import BlobStorage

import urllib2
from vcdm import c

cdmi_bucket_name = c('azure', 'azure.bucket_name')

class AzureBlob(IBlob):
    
    backend_type = 'azure'
    conn = None

    def __init__(self, initialize_storage=False):
        self.conn = BlobStorage(c('azure', 'credentials.blob_url'),
                                 c('azure', 'credentials.account'), c('azure', 'credentials.password'))
        # TODO: validate in real life        
        self.conn.create_container(cdmi_bucket_name)

    def read(self, fnm, rng=None):
        return self.conn.get_blob(unicode(cdmi_bucket_name), unicode(fnm))
    
    def create(self, fnm, content):
        self.conn.put_blob(unicode(cdmi_bucket_name), unicode(fnm), content)
    
    def update(self, fnm, content):
        self.create(fnm, content)
        
    def delete(self, fnm):
        try:
            self.conn.delete_blob(unicode(cdmi_bucket_name), unicode(fnm))
        except urllib2.HTTPError:
            # TODO: winazure lib seems to be passing also positive responses via exceptions. Need to clarify
            import sys
            print "====================="
            print sys.exc_info()
            print "====================="
