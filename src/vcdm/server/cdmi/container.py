from  twisted.web import resource

from  vcdm import container
from vcdm.server.cdmi.cdmi_content_types import CDMI_CONTAINER
from vcdm.server.cdmi.root import CDMI_VERSION, CDMI_SERVER_HEADER
from vcdm.server.http_status_codes import OK
from vcdm.server.cdmi.generic import parse_path, set_common_headers,\
    get_common_body

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
        name, container_path, fullpath = parse_path(request.path)
        
        # contact the backend
        status, uid, children, metadata = container.read(fullpath)
        
        # create a header                
        request.setResponseCode(status)
        request.setHeader('Content-Type', CDMI_CONTAINER)
        set_common_headers(request)
        
        # and a body       
        response_body = {
                         'completionStatus': 'Complete', 
                         'metadata': metadata,
                         'children': children,
                         'capabilitiesURI': '/cdmi_capabilities/container'   
                         }   
        response_body.update(get_common_body(request, uid, fullpath))
        
        return json.dumps(response_body)
    
    def render_PUT(self, request):        
        name, container_path, fullpath = parse_path(request.path)
        
        length = int(request.getHeader('Content-Length'))        
        request.content.seek(0, 0)
        
        # process json encoded request body
        body = json.loads(request.content.read(length))        
        
        metadata = {}
        if 'metadata' in body:
            metadata = body['metadata']
        status, uid, children = container.create_or_update(name, container_path, fullpath, metadata)
        
        request.setResponseCode(status)
        request.setHeader('Content-Type', CDMI_CONTAINER)
        set_common_headers(request)
         
        # and a body
        response_body = {
                         'completionStatus': 'Complete', 
                         'metadata': metadata,
                         'children': children
                         }  
        response_body.update(get_common_body(request, uid, fullpath))
        
        return json.dumps(response_body)
    
    def render_DELETE(self, request):
        name, container_path, fullpath = parse_path(request.path)
        status = container.delete(fullpath)
        request.setResponseCode(status)
        request.setHeader('Server', CDMI_SERVER_HEADER)   
        return ""

