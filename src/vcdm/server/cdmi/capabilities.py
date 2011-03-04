from twisted.web import resource
from vcdm.server.cdmi.cdmi_content_types import CDMI_CAPABILITY
from vcdm.server.cdmi.root import CDMI_VERSION
from vcdm.server.cdmi.cdmi_exit_codes import BAD_REQUEST

class Capability(resource.Resource):
    isLeaf = True 
    allowedMethods = ('GET') 

    def render_GET(self, fixed_path, request):
        # for now only support top-level capabilities
        if request.postpath[0] != 'cdmi_capabilities':
            return BAD_REQUEST
        
        
        
        # construct response
        request.setResponseCode(200)
        request.setHeader('Content-Type', CDMI_CAPABILITY)
        request.setHeader('X-CDMI-Specification-Version', CDMI_VERSION)
        request.setHeader('Accept', CDMI_DATA)
        return "%s" % "result"