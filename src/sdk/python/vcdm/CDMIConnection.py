
class CDMIConnection():
    
    credentials = None
    endpoint = None
    
    def __init__(self, credentials, endpoint):
        self.credentials = credentials
        self.endpoint = endpoint
        
        
    def create_blob(self, remotefile, localfile,  mimetype=None, metadata=None):
        """Create a new blob from a local file"""
        pass
    
    def update_blob(self, remoteblob, localfile = None, mimetype=None, metadata=None):
        """Update a remote blob with new data."""
        pass
    
    def read_blob(self, remoteblob):
        """Read contents of a blob"""
        pass
    
    def delete_blob(self, remoteblob):
        """Delete specified blob"""
        pass