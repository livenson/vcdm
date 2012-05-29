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
from vcdm.config import get_config

try:
    from libcdmi.cdmi import CDMIConnection
except ImportError:
    print "CDMI blob backend missing"


class CDMIBlob(object):
    """Implementation of the backend for blob operations on CDMI-compliant servers"""

    backend_name = 'cdmi'
    conn = None

    def __init__(self, backend_name):
        self.backend_name = backend_name
        self.conn = CDMIConnection(get_config().get(backend_name, 'cdmi.endpoint'),
                                   {'user': get_config().get(backend_name, 'credentials.username'),
                                    'password': get_config().get(backend_name, 'credentials.password')})

    def create(self, fnm, content):
        self.conn.create_blob(content, fnm)

    def read(self, fnm, rng=None):
        return self.conn.read_blob(fnm)

    def update(self, fnm, content):
        self.conn.update_blob(content, fnm)

    def delete(self, fnm):
        self.conn.delete_blob(fnm)
