import urllib2
from vcdm.common import CDMI_CONTAINER, CDMIRequestWithMethod, CDMI_OBJECT

try:
    import json
except ImportError:
    import simplejson as json
   
class ContainerOperations():
        
    endpoint = None
    
    def __init__(self, endpoint):
        self.endpoint = endpoint
        
    def create(self, remote_container, metadata={}):
        """Create a new container. """
        
        # put relevant headers
        headers = {
                   'Accept': CDMI_CONTAINER,
                   'Content-Type': CDMI_CONTAINER,
                   }
                
        data = {
                'metadata': metadata                
                }
        
        req = CDMIRequestWithMethod(self.endpoint + remote_container, 'PUT', json.dumps(data), headers)
        f = urllib2.urlopen(req);
        return f.read()
    
    def update(self, remote_container, metadata={}):
        """Update a remote container with new data."""
        # XXX for now we don't differentiate between update and create
        return self.create(remote_container, metadata)
    
    def read(self, remote_container):
        """Read children of a container."""
        # put relevant headers
        headers = {
                   'Accept': CDMI_CONTAINER,
                   'Content-Type': CDMI_OBJECT,
                   }        
        
        req = CDMIRequestWithMethod(self.endpoint + remote_container, 'GET', None, headers)
        res = urllib2.urlopen(req)
        
        return json.loads(res.read())['children']
        
    
    def delete(self, remote_container):
        """Delete specified container."""
        headers = {
                   'Accept': CDMI_CONTAINER,
                   'Content-Type': CDMI_CONTAINER,
                   }
        
        req = CDMIRequestWithMethod(self.endpoint + remote_container, 'DELETE', None, headers)
        urllib2.urlopen(req)
