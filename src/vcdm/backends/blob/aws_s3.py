backend_type = 's3'

import boto
from boto.s3.key import Key

import vcdm
c = boto.connect_s3(vcdm.config.get('aws', 'credentials.username'), vcdm.config.get('aws', 'credentials.password'))

def read(fnm, rng=None):
    b = c.get_bucket('vcdm')
    k = Key(b)    
    k.key = fnm
    return k.get_contents_as_string()

def write(fnm, content):
    b = c.get_bucket('vcdm')
    k = Key(b)
    k.key = fnm
    k.set_contents_from_string(content)

def delete(fnm):
    b = c.get_bucket('vcdm')
    k = Key(b)    
    k.key = fnm
    k.delete()