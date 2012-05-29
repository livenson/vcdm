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
    from pyazure.blob import BlobStorage
except ImportError:
    print "Azure blob plugin missing"

import urllib2

config = get_config()


class AzureBlob(object):

    backend_type = 'azure'
    conn = None

    def __init__(self, backend_name):
        self.backend_name = backend_name
        self.cdmi_bucket_name = config.get(backend_name, 'azure.bucket_name')
        self.conn = BlobStorage(config.get(backend_name, 'credentials.blob_url'),
                                 config.get(backend_name, 'credentials.account'),
                                 config.get(backend_name, 'credentials.password'))
        self.conn.create_container(self.cdmi_bucket_name)

    def read(self, fnm):
        return self.conn.get_blob(self.cdmi_bucket_name, fnm)

    def create(self, fnm, content):
        input_stream, input_length = content
        self.conn.put_blob(self.cdmi_bucket_name, fnm, input_stream, input_length)
        return "%s/%s/%s" % (self.conn.get_base_url(), self.cdmi_bucket_name, fnm)

    def update(self, fnm, content):
        return self.create(fnm, content)

    def delete(self, fnm):
        try:
            self.conn.delete_blob(self.cdmi_bucket_name, fnm)
            return "%s/%s/%s" % (self.conn.get_base_url(), self.cdmi_bucket_name, fnm)
        except urllib2.HTTPError:
            # TODO: winazure lib seems to be passing also positive responses via exceptions. Need to clarify
            import sys
            print "Error:", sys.exc_info()[0]
            import traceback
            traceback.print_exc()
