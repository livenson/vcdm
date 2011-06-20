from vcdm import c
from vcdm.interfaces.blob import IBlob
from twisted.python import log

import boto
from boto.s3.key import Key
from boto.s3.connection import Location
from boto.exception import S3CreateError
from StringIO import StringIO
import tempfile
from tempfile import NamedTemporaryFile

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
        try:
            self.conn.create_bucket(cdmi_bucket_name, location = Location.EU)
        except S3CreateError:
            log.msg("S3 bucket already created. Using it.")

    def read(self, fnm):        
        b = self.conn.get_bucket(cdmi_bucket_name)
        k = Key(b)    
        k.key = fnm
        # read in the content to a temporary file on disk
        fp = NamedTemporaryFile(prefix="aws_s3", 
                               suffix=".buffer",
                               delete=True)        
        k.get_contents_to_file(fp)
        fp.seek(0) # roll back to start
        return fp
    
    def create(self, fnm, content):
        input_stream, _ = content
        b = self.conn.get_bucket(cdmi_bucket_name)
        k = Key(b)
        k.key = fnm
        k.set_contents_from_file(input_stream)
        input_stream.close()
        
    def update(self, fnm, content):
        self.create(fnm, content)
    
    def delete(self, fnm):
        b = self.conn.get_bucket(cdmi_bucket_name)
        k = Key(b)    
        k.key = fnm
        k.delete()