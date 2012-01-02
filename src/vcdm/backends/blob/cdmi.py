from vcdm.interfaces.blob import IBlob

from vcdm import c
from libcdmi.cdmi import CDMIConnection 

class CDMIBlob(IBlob):
    
    backend_name = 'cdmi'
    conn = None
    
    def __init__(self, backend_name):
        self.backend_name = backend_name
        self.conn = CDMIConnection(c(backend_name, 'cdmi.endpoint'), 
                                   {'user': c(backend_name, 'credentials.username'),
                                    'password': c(backend_name, 'credentials.password')})

    def create(self, fnm, content):
        self.conn.create_blob(content, fnm)
    
    def read(self, fnm, rng=None):
        return self.conn.read_blob(fnm)
    
    def update(self, fnm, content):
        self.conn.update_blob(content, fnm)
    
    def delete(self, fnm):
        self.conn.delete_blob(fnm)
    
