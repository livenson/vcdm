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
