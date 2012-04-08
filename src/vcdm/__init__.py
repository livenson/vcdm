"""
Venus-C Data Management module
"""

from vcdm.config import get_config
conf = get_config()


def c(group, field):
    """Shorthand for getting configuration values"""
    return conf.get(group, field)


# shared environment variables
global env
env = {'ds': None,
       'blob': None,
       'mq': None,
       'blobs': {},
       'authn_methods': None
       }

blob_backends = {}
# mq is a non-compulsory object
mq_backends = {}
datastore_backends = {}

env['tre_enabled'] = conf.getboolean('general', 'tre_enabled')
