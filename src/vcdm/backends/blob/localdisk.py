from twisted.python import log

import os

import vcdm
from vcdm.utils import copyStreamToStream, mkdir_p

conf = vcdm.config.get_config()


class POSIXBlob():

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
        with open(fnm, 'wb') as output_file:
            copyStreamToStream(input_stream, output_file, input_length)
            input_stream.close()
        return fnm

    def read(self, uid):
        """Read the contents of a file, possibly a certain byte range"""
        fnm = os.path.join(self.location, uid)
        log.msg("Reading a blob '%s'" % fnm)
        return open(fnm, 'rb')

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
