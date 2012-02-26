"""
Venus-C Data Management module
"""

from vcdm.config import get_config
config = get_config()


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

blob_backends = {}
# mq is a non-compulsory object
mq_backends = {}
datastore_backends = {}

env['tre_enabled'] = config.getboolean('general', 'tre_enabled')
