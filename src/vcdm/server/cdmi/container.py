from  twisted.web import resource
from twisted.python import log

from  vcdm import container
from vcdm.server.cdmi.cdmi_content_types import CDMI_CONTAINER
from vcdm.server.cdmi.root import CDMI_SERVER_HEADER
from vcdm.server.cdmi.generic import parse_path, set_common_headers,\
    get_common_body

try:
    import json
except ImportError:
    import simplejson as json

class Container(resource.Resource):
    isLeaf = True
    allowMethods = ('PUT', 'GET', 'DELETE')
    
    def __init__(self, avatarID = None):        
        resource.Resource.__init__(self)
        self.avatarID = avatarID

    def render_GET(self, request):
        """GET operation corresponds to reading container's data"""
        # parse the request
        _, __, fullpath = parse_path(request.path)

        # contact the backend
        status, uid, children, metadata = container.read(self.avatarID, fullpath)

        # create a header
        request.setResponseCode(status)
        request.setHeader('Content-Type', CDMI_CONTAINER)
        set_common_headers(request)

        # and a body
        response_body = {
                         'completionStatus': 'Complete', 
                         'metadata': metadata,
                         'children': children,
                         'childrenrange': '' if len(children) == 0 else '0-%s' % len(children),
                         'capabilitiesURI': '/cdmi_capabilities/container'   
                         }
        response_body.update(get_common_body(request, uid, fullpath))

        return json.dumps(response_body)
    
    def render_PUT(self, request):        
        name, container_path, fullpath = parse_path(request.path)
        log.msg("Creating container %s" % fullpath)
        req_length = int(request.getHeader('Content-Length'))    
        request.content.seek(0, 0)    
        # process json encoded request body
        body = json.loads(request.content.read(req_length))                
        metadata = {}
        if 'metadata' in body:
            metadata = body['metadata']
        status, uid, children = container.create_or_update(self.avatarID, name, container_path, fullpath, metadata)

        request.setResponseCode(status)
        request.setHeader('Content-Type', CDMI_CONTAINER)
        set_common_headers(request)

        # and a body
        response_body = {
                         'completionStatus': 'Complete', 
                         'metadata': metadata,
                         'children': children,
                         'childrenrange': '' if len(children) == 0 else '0-%s' % len(children),
                         }
        response_body.update(get_common_body(request, uid, fullpath))

        return json.dumps(response_body)

    def render_DELETE(self, request):
        _, __, fullpath = parse_path(request.path)
        status = container.delete(self.avatarID, fullpath)
        request.setResponseCode(status)
        request.setHeader('Server', CDMI_SERVER_HEADER)   
        return ""


class NonCDMIContainer(resource.Resource):
    isLeaf = True
    allowMethods = ('PUT', 'GET', 'DELETE')

    def __init__(self, avatarID = None):        
        resource.Resource.__init__(self)
        self.avatarID = avatarID
    
    def render_GET(self, request):
        """GET operation corresponds to reading a container's data."""
        # parse the request        
        _, __, fullpath = parse_path(request.path)

        # contact the backend
        status, _, children, metadata = container.read(self.avatarID, fullpath)

        # create a header
        request.setResponseCode(status)
        request.setHeader('Content-Type', 'application/json')

        # and a body
        # this is not a completely correct implementation of a non-cdmi reply.
        # TODO: change to more specific fields once fields separation is implemented
        response_body = {
                         'metadata': metadata,
                         'children': children,
                         }

        return json.dumps(response_body)

    def render_PUT(self, request):
        name, container_path, fullpath = parse_path(request.path)
        status, _, __ = container.create_or_update(self.avatarID, name, container_path, fullpath, {})
        request.setResponseCode(status)
        return ""

    def render_DELETE(self, request):
        _, __, fullpath = parse_path(request.path)
        status = container.delete(self.avatarID, fullpath)
        request.setResponseCode(status)
        request.setHeader('Server', CDMI_SERVER_HEADER)
        return ""

