from BlobOperations import BlobOperations


class CDMIConnection():
    
    credentials = None
    endpoint = None
    blob_proxy = None
    container_proxy = None
    mq_proxy = None
    
    def __init__(self, credentials, endpoint):
        self.credentials = credentials
        self.endpoint = endpoint
        self.blob_proxy = BlobOperations(credentials, endpoint)
        
        
    def create_blob(self, remotefile, localfile,  mimetype=None, metadata=None):
        """Create a new blob from a local file"""
        
    
    def update_blob(self, remoteblob, localfile = None, mimetype=None, metadata=None):
        """Update a remote blob with new data."""
        pass
    
    def read_blob(self, remoteblob):
        """Read contents of a blob"""
        pass
    
    def delete_blob(self, remoteblob):
        """Delete specified blob"""
        pass