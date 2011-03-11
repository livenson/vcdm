from interfaces.blob import IBlob

import boto
from boto.s3.key import Key

from vcdm import c

class S3Blob(IBlob):
    
    conn = None
    backend_type = 's3'
    
    def __init__(self):
        self.conn = boto.connect_s3(c('aws', 'credentials.username'), 
                                    c('aws', 'credentials.password'))    

    def read(self, fnm, rng=None):
        b = self.conn.get_bucket('vcdm')
        k = Key(b)    
        k.key = fnm
        return k.get_contents_as_string()
    
    def create(self, fnm, content):
        b = self.conn.get_bucket('vcdm')
        k = Key(b)
        k.key = fnm
        k.set_contents_from_string(content)
        
    def update(self, fnm, content):
        self.create(fnm, content)
    
    def delete(self, fnm):
        b = self.conn.get_bucket('vcdm')
        k = Key(b)    
        k.key = fnm
        k.delete()