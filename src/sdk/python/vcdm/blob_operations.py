import urllib2
from vcdm.common import CDMIRequestWithMethod, CDMI_DATA, CDMI_OBJECT
   
try:
    import json
except ImportError:
    import simplejson as json
   
class BlobOperations():
        
    endpoint = None
    
    def __init__(self, endpoint):
        self.endpoint = endpoint
            
    def create(self, localfile, remoteblob, mimetype=None, metadata={}):
        """Create a new blob from a local file"""
        
        # put relevant headers
        headers = {
                   'Accept': CDMI_DATA,
                   'Content-Type': CDMI_DATA,
                   }
        
        # read-in the value
        f = open(localfile, "rb")
        content = f.read()
        f.close()
        data = {'value': content,
                'mimetype': mimetype,
                'metadata': metadata                
                }
        
        req = CDMIRequestWithMethod(self.endpoint + remoteblob, 'PUT', json.dumps(data), headers)
        f = urllib2.urlopen(req);
        return f.read()
    
    def update(self, localfile, remoteblob , mimetype=None, metadata={}):
        """Update a remote blob with new data."""
        # XXX for now we don't differentiate between update and create
        return self.create(localfile, remoteblob, mimetype, metadata)
    
    def read(self, remoteblob):
        """Read contents of a blob"""
        # put relevant headers
        headers = {
                   'Accept': CDMI_DATA,
                   'Content-Type': CDMI_OBJECT,
                   }        
        
        req = CDMIRequestWithMethod(self.endpoint + remoteblob, 'GET', None, headers)
        res = urllib2.urlopen(req)
        
        return json.loads(res.read())['value']
        
    
    def delete(self, remoteblob):
        """Delete specified blob"""
        headers = {
                   'Accept': CDMI_DATA,
                   'Content-Type': CDMI_DATA,
                   }
        
        req = CDMIRequestWithMethod(self.endpoint + remoteblob, 'DELETE', None, headers)
        urllib2.urlopen(req).read();
