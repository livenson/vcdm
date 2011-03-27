from  twisted.web import resource

from  vcdm import container
from vcdm.server.cdmi.cdmi_content_types import CDMI_CONTAINER
from vcdm.server.cdmi.root import CDMI_VERSION, CDMI_SERVER_HEADER
from vcdm.server.http_status_codes import OK

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
        fullpath = request.path.rstrip('/')         
        tmp = fullpath.split('/')
        if len(tmp) != 1: # if it's not a top-level container
            container_path = tmp[:-1]
        else:
            container_path = ['']
        
        # contact the backend
        status, uid, children, metadata = container.read(fullpath)
        
        # create a header                
        request.setResponseCode(status)
        request.setHeader('Content-Type', CDMI_CONTAINER)
        request.setHeader('X-CDMI-Specification-Version', CDMI_VERSION)
        request.setHeader('Server', CDMI_SERVER_HEADER)
        
        # and a body
        server = request.host[1] + ":" + str(request.host[2])
        
        response_body = {'objectURI': server + request.uri,
                         'objectID': uid,                         
                         'domainURI': server,
                         'parentURI': server + "/".join(container_path),
                         'capabilitiesURI': None, 
                         'completionStatus': 'Complete', 
                         'metadata': metadata,
                         'children': children
                         } #XXX not sure what to do if status in not ok. if status == OK else {}  
        return json.dumps(response_body)
    
    def render_PUT(self, request):        
        fullpath = request.path.rstrip('/') 
        tmp = fullpath.split('/')
        container_path = tmp[:-1]
        
        length = int(request.getHeader('Content-Length'))        
        request.content.seek(0, 0)
        
        # process json encoded request body
        body = json.loads(request.content.read(length))        
        metadata = body['metadata']
                
        status, uid, children = container.create_or_update(container_path, tmp[-1], metadata)
        
        request.setResponseCode(status)
        request.setHeader('Content-Type', CDMI_CONTAINER)
        request.setHeader('X-CDMI-Specification-Version', CDMI_VERSION)
        request.setHeader('Server', CDMI_SERVER_HEADER)
         
         # and a body
        server = request.host[1] + ":" + str(request.host[2])
        response_body = {'objectURI': server + request.uri,
                         'objectID': uid,                         
                         'domainURI': server,
                         'parentURI': server + "/".join(container_path),
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
        request.setHeader('Server', CDMI_SERVER_HEADER)   
        return ""

