from vcdm.interfaces.blob import IBlob
from libazure.azure_storage import BlobStorage

import urllib2
from vcdm import c



class AzureBlob(IBlob):
    
    backend_type = 'azure'
    conn = None

    def __init__(self, backend_name):
        self.cdmi_bucket_name = c(backend_name, 'azure.bucket_name')
        self.conn = BlobStorage(c(backend_name, 'credentials.blob_url'),
                                 c(backend_name, 'credentials.account'), 
                                 c(backend_name, 'credentials.password'))
        # TODO: validate in real life        
        self.conn.create_container(self.cdmi_bucket_name)

    def read(self, fnm):
        return self.conn.get_blob(self.cdmi_bucket_name, fnm)
    
    def create(self, fnm, content):
        input_stream, input_length = content
        self.conn.put_blob(self.cdmi_bucket_name, fnm, input_stream, input_length)
    
    def update(self, fnm, content):
        self.create(fnm, content)
        
    def delete(self, fnm):
        try:
            self.conn.delete_blob(self.cdmi_bucket_name, fnm)
        except urllib2.HTTPError:
            # TODO: winazure lib seems to be passing also positive responses via exceptions. Need to clarify
            import sys
            print "====================="
            print "something happened:", sys.exc_info()[0]
            import traceback
            traceback.print_exc()
            print "====================="
