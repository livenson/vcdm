from vcdm import c
from vcdm.interfaces.blob import IBlob

import boto
from boto.s3.key import Key
from boto.s3.connection import Location

cdmi_bucket_name = c('aws', 'aws.bucket_name')
# change to Location.USWest for the corresponding zone
AWS_BUCKET_LOCATION = Location.EU

class S3Blob(IBlob):
    
    conn = None
    backend_type = 's3'
    
    def __init__(self):
        self.conn = boto.connect_s3(c('aws', 'credentials.username'), 
                                    c('aws', 'credentials.password'))    
        # create a new bucket - just in case
        # TODO: validate return code in reality
        self.conn.create_bucket(cdmi_bucket_name, location = Location.EU)

    def read(self, fnm, rng=None):
        b = self.conn.get_bucket(cdmi_bucket_name)
        k = Key(b)    
        k.key = fnm
        return k.get_contents_as_string()
    
    def create(self, fnm, content):
        b = self.conn.get_bucket(cdmi_bucket_name)
        k = Key(b)
        k.key = fnm
        k.set_contents_from_string(content)
        
    def update(self, fnm, content):
        self.create(fnm, content)
    
    def delete(self, fnm):
        b = self.conn.get_bucket(cdmi_bucket_name)
        k = Key(b)    
        k.key = fnm
        k.delete()