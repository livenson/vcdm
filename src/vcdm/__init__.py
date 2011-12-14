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


# shared environment variables
global env
env = {'ds': None,
       'blob': None,
       'mq': None,
       'blobs': {}
       }

# compulsory localdisk backend
from vcdm.backends.blob.localdisk import POSIXBlob
blob_backends = {'local': POSIXBlob}

# optional backends, some require presence of additional plugins
try:
    from vcdm.backends.blob.aws_s3 import S3Blob
    blob_backends['aws'] = S3Blob
except ImportError:
    print "AWS back-end type not available"

try:
    from vcdm.backends.blob.azure import AzureBlob
    blob_backends['azure'] = AzureBlob
except ImportError:
    print "Azure back-end type not available"
    
try:
    from vcdm.backends.blob.cdmi import CDMIBlob
    blob_backends['cdmi'] = CDMIBlob
except ImportError:
    print "CDMI back-end type not available"

# mq is a non-compulsory object
mq_backends = {}

if c('general', 'support_mq') == 'yes' and c('general', 'mq.backend') == 'local':
    from vcdm.backends.mq.amqp import AMQPMQ
    mq_backends['amqp'] = AMQPMQ

if c('general', 'support_mq') == 'yes' and c('general', 'mq.backend') == 'cdmi':
    from vcdm.backends.mq.cdmi import CDMIQueue
    mq_backends['cdmi'] = CDMIQueue

if c('general', 'support_mq') == 'yes' and c('general', 'mq.backend') == 'aws':
    from vcdm.backends.mq.aws_sqs import AWSSQSMessageQueue
    mq_backends['aws'] = AWSSQSMessageQueue

if c('general', 'support_mq') == 'yes' and c('general', 'mq.backend') == 'azure':
    from vcdm.backends.mq.azure import AzureQueue
    mq_backends['azure'] = AzureQueue

# datastore backends
datastore_backends = {}
if c('general', 'ds.backend') == 'couchdb':
    from vcdm.backends.datastore.couchdb_store import CouchDBStore
    datastore_backends['couchdb'] = CouchDBStore  

env['tre_enabled'] = c('general', 'tre_enabled') == 'yes'
