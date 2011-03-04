"""
Venus-C Data Management module
"""
# read in configuration
import ConfigParser
config = ConfigParser.RawConfigParser()
# TODO: if no vcdm.conf available -> assume default values?
config.read('vcdm.conf')

# load backends
import backends.blob
blob_backends = {'local': backends.blob.localdisk, 
                 'aws': backends.blob.aws_s3,
                 'azure': backends.blob.azure,
                 'cdmi': backends.blob.cdmi
                 }

import backends.mq
mq_backends = {'local': backends.mq.amqp,
               'aws': backends.mq.aws_sqs,
               'azure': backends.mq.azure
               }

import datastore
datastore_backends = {'local': datastore.couchdb_store,
                      'azure': datastore.azure_store}


# import exit codes
from vcdm.server.http_status_codes import *
