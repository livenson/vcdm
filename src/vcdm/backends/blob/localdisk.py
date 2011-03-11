import os
from interfaces.blob import IBlob

from vcdm import c

class POSIXBlob(IBlob):
    backend_type = 'posix'    
    location = None
    
    def __init__(self): 
        self.location = c('local', 'blob.datadir')

    def write(self, fnm, content):
        """Write the content to a file"""
        f = open(self.location + os.sep + fnm, 'w')
        f.write(content)        
        f.close()
    
    def read(self, fnm, rng=None):
        """Read the contents of a file, possibly a certain byte range"""
        f = open(self.location + os.sep + fnm, 'r')
        d = None
        if rng is None:
            d = f.read()
        else:
            f.seek(rng[0])
            d = f.read(rng[1] - rng[0])
        f.close()
        return d 
    
    def delete(self, fnm):
        """Delete a specified file"""
        os.remove(self.location + os.sep + fnm)
        
