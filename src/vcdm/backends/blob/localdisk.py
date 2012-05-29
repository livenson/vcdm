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
from twisted.python import log

import os

import vcdm
from vcdm.utils import copyStreamToStream, mkdir_p
from vcdm.encryption import encrypt_file, decrypt_file
from tempfile import NamedTemporaryFile

conf = vcdm.config.get_config()


class POSIXBlob(object):

    backend_type = 'posix'
    location = None

    def __init__(self, backend_name):
        self.backend_name = backend_name
        self.location = conf.get(backend_name, 'blob.datadir')
        if not os.path.exists(self.location):
            mkdir_p(self.location)

    def create(self, uid, content):
        """Write the content to a file"""
        input_stream, input_length = content
        fnm = os.path.join(self.location, uid)
        log.msg("Saving blob to %s" % fnm)
        key = None
        try:
            key = conf.get(self.backend_name, 'encryption_key').strip()
        except:
            pass
        with open(fnm, 'wb') as output_file:
            if not key:
                copyStreamToStream(input_stream, output_file, input_length)
            else:
                encrypt_file(key, input_stream, output_file, input_length)
            input_stream.close()
        return fnm

    def read(self, uid):
        """Read the contents of a file, possibly a certain byte range"""
        fnm = os.path.join(self.location, uid)
        log.msg("Reading a blob '%s'" % fnm)
        key = None
        try:
            key = conf.get(self.backend_name, 'encryption_key').strip()
        except:
            pass
        if not key:
            return open(fnm, 'rb')
        else:
            tmp_file = NamedTemporaryFile(prefix="lb_dec",
                                          suffix=".buffer",
                                          delete=True)
            decrypt_file(key, fnm, tmp_file)
            tmp_file.seek(0)

            return tmp_file

    def update(self, uid, content):
        """Update contents of a file"""
        return self.create(uid, content)

    def delete(self, uid):
        """Delete a specified file"""
        fnm = os.path.join(self.location, uid)
        log.msg("Deleting '%s'" % fnm)
        os.remove(fnm)
        return fnm

    def move_to_tre_server(self, fnm):
        source = os.path.join(conf.get(self.backend_name, 'blob.datadir'), fnm)
        target = os.path.join(conf.get('general', 'tre_data_folder'), fnm)
        try:
            os.symlink(os.path.abspath(source), os.path.abspath(target))
        except OSError, ex:
            if ex.errno == 17:
                pass
