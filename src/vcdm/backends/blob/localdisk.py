import os
from vcdm.interfaces.blob import IBlob

from vcdm import c
from vcdm.utils import copyStreamToStream

class POSIXBlob(IBlob):
    
    backend_type = 'posix'    
    location = None
    
    def __init__(self, backend_name): 
        self.backend_name = backend_name
        self.location = c(backend_name, 'blob.datadir')

    def create(self, fnm, content):
        """Write the content to a file"""
        input_stream, input_length = content
        with open(self.location + os.sep + fnm, 'wb') as output_file:
            copyStreamToStream(input_stream, output_file, input_length)
            input_stream.close()
                
    def read(self, fnm):
        """Read the contents of a file, possibly a certain byte range"""        
        name = self.location + os.sep + fnm
        return open(name,'rb')
        
    def update(self, fnm, content):
        """Update contents of a file"""
        # XXX: should it be different from write?
        self.create(fnm, content)
    
    def delete(self, fnm):
        """Delete a specified file"""
        os.remove(self.location + os.sep + fnm)
        
