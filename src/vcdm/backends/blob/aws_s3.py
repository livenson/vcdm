import os
from tempfile import NamedTemporaryFile

from vcdm import c

from twisted.python import log

try:
    import boto
    from boto.s3.key import Key
    from boto.s3.connection import Location
    from boto.exception import S3CreateError
except ImportError:
    print "AWS blob plugin missing"


class S3Blob(object):

    conn = None
    backend_type = 's3'

    def __init__(self, backend_name):
        self.backend_name = backend_name
        self.conn = boto.connect_s3(c(backend_name, 'credentials.username'),
                                    c(backend_name, 'credentials.password'))
        # create a new bucket - just in case
        self.cdmi_bucket_name = c(backend_name, 'aws.bucket_name')
        # change to Location.USWest for the corresponding zone
        try:
            self.conn.create_bucket(self.cdmi_bucket_name,
                                    location=Location.EU)
        except S3CreateError:
            log.msg("S3 bucket already created. Using it.")

    def read(self, fnm):
        b = self.conn.get_bucket(self.cdmi_bucket_name)
        k = Key(b)
        k.key = fnm
        # read in the content to a temporary file on disk
        fp = NamedTemporaryFile(prefix="aws_s3",
                               suffix=".buffer",
                               delete=True)
        k.get_contents_to_file(fp)
        fp.seek(0)  # roll back to start
        return fp

    def create(self, fnm, content):
        input_stream, _ = content
        b = self.conn.get_bucket(self.cdmi_bucket_name)
        k = Key(b)
        k.key = fnm
        k.set_contents_from_file(input_stream)
        input_stream.close()
        return "http://%s/%s/%s" % (self.cdmi_bucket_name, fnm, self.conn.DefaultHost)

    def update(self, fnm, content):
        return self.create(fnm, content)

    def delete(self, fnm):
        b = self.conn.get_bucket(self.cdmi_bucket_name)
        k = Key(b)
        k.key = fnm
        k.delete()
        return "http://%s/%s/%s" % (self.cdmi_bucket_name, fnm, self.conn.DefaultHost)

    def move_to_tre_server(self, fnm):
        b = self.conn.get_bucket(self.cdmi_bucket_name)
        k = Key(b)
        k.key = fnm
        # read in the content to a temporary file on disk
        fp = NamedTemporaryFile(prefix="aws_s3",
                               suffix=".buffer",
                               delete=False)
        k.get_contents_to_file(fp)

        source = os.path.join(c(self.backend_name, 'blob.datadir'), fp.name)
        target = os.path.join(c('general', 'tre_data_folder'), fnm)

        try:
            os.symlink(os.path.abspath(source), os.path.abspath(target))
        except OSError, ex:
            if ex.errno == 17:
                pass
