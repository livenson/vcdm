from vcdm.interfaces.blob import IBlob

from vcdm import c
from libcdmi.cdmi import CDMIConnection 
from StringIO import StringIO

class CDMIBlob(IBlob):
    
    backend_type = 'cdmi'
    conn = None
    
    def __init__(self):
        self.conn = CDMIConnection(c('cdmi', 'cdmi.endpoint'), 
                                   {'user': c('cdmi', 'credentials.username'),
                                    'password': c('cdmi', 'credentials.password')})

    def create(self, fnm, content):
        self.conn.create_blob(StringIO(content), fnm)
    
    def read(self, fnm, rng=None):
        return self.conn.read_blob(fnm)
    
    def update(self, fnm, content):
        self.conn.update_blob(StringIO(content), fnm)
    
    def delete(self, fnm):
        self.conn.delete_blob(fnm)
    
