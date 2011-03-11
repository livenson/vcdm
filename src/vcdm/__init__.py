"""
Venus-C Data Management module
"""
# read in configuration
import ConfigParser
from backends.mq.amqp import AMQPMQ
from backends.mq.aws_sqs import AWSSQSMessageQueue
from backends.mq.azure import AzureQueue
from backends.mq.cdmi import CDMIQueue

config = ConfigParser.RawConfigParser()
# TODO: if no vcdm.conf available -> assume default values?
config.read('vcdm.conf')


def c(group, field):
    """Shorthand for getting configuration values"""
    return config.get(group, field)


# load backends

blob_backends = {'local': backends.blob.localdisk, 
                 'aws': backends.blob.aws_s3,
                 'azure': backends.blob.azure,
                 'cdmi': backends.blob.cdmi
                 }

mq_backends = {'local': AMQPMQ,
               'aws': AWSSQSMessageQueue,
               'azure': AzureQueue,
               'cdmi': CDMIQueue
               }

datastore_backends = {'local': backends.datastore.couchdb_store,
                      'azure': backends.datastore.azure_store}

# import exit codes
from vcdm.server.http_status_codes import *
