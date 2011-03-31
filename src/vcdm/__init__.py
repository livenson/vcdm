"""
Venus-C Data Management module
"""
# read in configuration
import ConfigParser
config = ConfigParser.RawConfigParser()
# TODO: if no vcdm.conf available -> assume default values?
config.read('vcdm.conf')

def c(group, field):
    """Shorthand for getting configuration values"""
    return config.get(group, field)

from vcdm.backends.blob.localdisk import POSIXBlob
from vcdm.backends.blob.azure import AzureBlob
from vcdm.backends.blob.aws_s3 import S3Blob
from vcdm.backends.blob.cdmi import CDMIBlob

from vcdm.backends.mq.amqp import AMQPMQ
from vcdm.backends.mq.aws_sqs import AWSSQSMessageQueue
from vcdm.backends.mq.azure import AzureQueue
from vcdm.backends.mq.cdmi import CDMIQueue

from vcdm.backends.datastore.couchdb_store import CouchDBStore
from vcdm.backends.datastore.azure_store import AzureStore

# shared environment variables
env = {'ds': None,
       'blob': None,
       'mq': None
       }


blob_backends = {'local': POSIXBlob, 
                 'aws': S3Blob,
                 'azure': AzureBlob,
                 'cdmi': CDMIBlob
                 }

mq_backends = {'local': AMQPMQ,
               'aws': AWSSQSMessageQueue,
               'azure': AzureQueue,
               'cdmi': CDMIQueue
               }

datastore_backends = {'local': CouchDBStore,
                      'azure': AzureStore}

# import exit codes
from vcdm.server.http_status_codes import *
