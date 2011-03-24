from blob_operations import BlobOperations

import urllib2
from vcdm.container_operations import ContainerOperations

class CDMIConnection():
    
    credentials = None
    endpoint = None
    blob_proxy = None
    container_proxy = None
    mq_proxy = None
    
    def __init__(self, endpoint, credentials):
        self.credentials = credentials
        self.endpoint = endpoint
        
        # install authenticated opener for all of the urllib2 calls
        auth_handler = urllib2.HTTPDigestAuthHandler()
        auth_handler.add_password(realm=None,
                          uri=endpoint,
                          user=credentials['user'],
                          passwd=credentials['password'])
        opener = urllib2.build_opener(auth_handler, urllib2.HTTPSHandler()) 
        urllib2.install_opener(opener)
        
        self.blob_proxy = BlobOperations(endpoint)
        self.container_proxy = ContainerOperations(endpoint)
        
        
    def create_blob(self, localfile, remoteblob, mimetype=None, metadata={}):
        """Create a new blob from a local file"""
        return self.blob_proxy.create(localfile, remoteblob, mimetype, metadata)
        
    
    def update_blob(self, localfile, remoteblob, mimetype=None, metadata={}):
        """Update a remote blob with new data."""
        return self.blob_proxy.update(localfile, remoteblob, mimetype, metadata)
    
    def read_blob(self, remoteblob):
        """Read contents of a blob"""
        return self.blob_proxy.read(remoteblob)
    
    def delete_blob(self, remoteblob):
        """Delete specified blob"""
        self.blob_proxy.delete(remoteblob)
        
    def create_container(self, remote_container, metadata={}):
        return self.container_proxy.create(remote_container, metadata)
    
    def read_container(self, remote_container):
        #XXX for now only return children of a container
        return self.container_proxy.read(remote_container)
    
    def update_container(self, remote_container):
        return self.container_proxy.update(remote_container)
    
    def delete_container(self, remote_container):
        self.container_proxy.delete(remote_container)
