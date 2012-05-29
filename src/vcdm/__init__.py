##
# Copyright 2002-2012 Ilja Livenson, PDC KTH
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##
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
