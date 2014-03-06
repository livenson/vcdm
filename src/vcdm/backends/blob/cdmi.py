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

import base64
import tempfile
import os

class CDMIBlob(object):
    """Implementation of the backend for blob operations on CDMI-compliant servers"""

    backend_name = 'cdmi'
    backend_type = 'cdmi'
    conn = None

    def __init__(self, backend_name):
        self.backend_name = backend_name
        self.conn = CDMIConnection(get_config().get(backend_name, 'cdmi.endpoint'),
                                   {'user': get_config().get(backend_name, 'credentials.username'),
                                    'password': get_config().get(backend_name, 'credentials.password')})
        
    def create(self, fnm, content):
        body, length=content
        encoded_body = base64.b64encode(body.getvalue())
        local_file = tempfile.NamedTemporaryFile(prefix="cdmi_intm",
                                          suffix=".tmp",
                                          delete=False)
        local_file.write(encoded_body)
        local_file.close()
        self.conn.blob_proxy.create(local_file.name, fnm)
        os.unlink(local_file.name)
        

    def read(self, fnm, rng=None):
        """ Read the content from the remote blob and return file object with content """
        json_obj=self.conn.blob_proxy.read(fnm)
        
        # read in the content to a temporary file on disk
        fp = tempfile.NamedTemporaryFile(prefix="cdmi",
                               suffix=".buffer",
                               delete=True)
        content=base64.b64decode(json_obj['value'])
        fp.write(content)
        fp.seek(0)
        return fp

    def update(self, fnm, content):
        body, length=content
        encoded_body = base64.b64encode(body.getvalue())
        local_file = tempfile.NamedTemporaryFile(prefix="cdmi_intm",
                                          suffix=".tmp",
                                          delete=False)
        local_file.write(encoded_body)
        local_file.close()
        # CHECK: remote CDMI service returns empty response even in the case
        # of CDMI access  therefore, using Non-CDMI call here
        self.conn.blob_proxy.update(local_file.name, fnm)
        os.unlink(local_file.name)

    def delete(self, fnm):
        self.conn.blob_proxy.delete(fnm)
