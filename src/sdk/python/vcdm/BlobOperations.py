import urllib2

class BlobOperations():
    
    credentials = None
    endpoint = None
    
    def __init__(self, credentials, endpoint):
        self.credentials = credentials
        self.endpoint = endpoint
            
    def create(self, remotefile, localfile,  mimetype=None, metadata=None):
        """Create a new blob from a local file"""
        pass        
    
    def update(self, remoteblob, localfile = None, mimetype=None, metadata=None):
        """Update a remote blob with new data."""
        pass
    
    def read(self, remoteblob):
        """Read contents of a blob"""
        pass
    
    def delete(self, remoteblob):
        """Delete specified blob"""
        pass