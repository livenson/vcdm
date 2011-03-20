from  twisted.web import resource

from  vcdm import container
from vcdm.server.cdmi.cdmi_content_types import CDMI_CONTAINER
from vcdm.server.cdmi.root import CDMI_VERSION

try:
    import json
except ImportError:
    import simplejson as json

class Container(resource.Resource):
    isLeaf = True
    allowMethods = ('PUT', 'GET', 'DELETE')

    def render_GET(self, request):
        """GET operation corresponds to reading container's data"""
        # parse the request        
        fullpath = request.path
        tmp = fullpath.split('/')
        container_path = tmp[:-1]
        
        # contact the backend
        status, uid, children, metadata = container.read(fullpath)
        
        # create a header                
        request.setResponseCode(status)
        request.setHeader('Content-Type', CDMI_CONTAINER)
        request.setHeader('X-CDMI-Specification-Version', CDMI_VERSION)
        
        # and a body
        response_body = {'objectURI': request.uri,
                         'objectID': uid,                         
                         'domainURI': request.host[1] + ":" + str(request.host[2]),
                         'parentURI': request.uri + container_path[-1],
                         'capabilitiesURI': None, 
                         'completionStatus': 'Complete', 
                         'metadata': metadata,
                         'children': children
                         }  
        return json.dumps(response_body)
    
    def render_PUT(self, request):        
        fullpath = request.path
        tmp = fullpath.split('/')
        container_path = tmp[:-1]
        filename = tmp[-1]
        
        length = int(request.getHeader('Content-Length'))        
        request.content.seek(0, 0)
        
        # process json encoded request body
        body = json.loads(request.content.read(length))        
        metadata = body['metadata']
                
        status, uid, children = container.create_or_update(container_path, fullpath, metadata)
        
        request.setResponseCode(status)
        request.setHeader('Content-Type', CDMI_CONTAINER)
        request.setHeader('X-CDMI-Specification-Version', CDMI_VERSION)
         
         # and a body
        response_body = {'objectURI': request.uri,
                         'objectID': uid,                         
                         'domainURI': request.host[1] + ":" + str(request.host[2]),
                         'parentURI': request.uri + container_path[-1],
                         'capabilitiesURI': None, 
                         'completionStatus': 'Complete', 
                         'metadata': metadata,
                         'children': children
                         }  
        return json.dumps(response_body)
    
    def render_DELETE(self, request):
        fullpath = request.path
        status = container.delete(fullpath)
        request.setResponseCode(status)                   
        return ""

