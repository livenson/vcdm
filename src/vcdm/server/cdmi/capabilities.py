from twisted.web import resource
from vcdm.server.cdmi.cdmi_content_types import CDMI_CAPABILITY, CDMI_DATA
from vcdm.server.cdmi.root import CDMI_VERSION
from vcdm.server.http_status_codes import BAD_REQUEST, OK


try:
    import json
except ImportError:
    import simplejson as json


class Capability(resource.Resource):
    isLeaf = True 
    allowedMethods = ('GET') 

    def render_GET(self, fixed_path, request):
        # for now only support top-level capabilities
        if request.postpath[0] != 'cdmi_capabilities':
            return BAD_REQUEST 
      
        # construct response
        request.setResponseCode(OK)
        request.setHeader('Content-Type', CDMI_CAPABILITY)
        request.setHeader('X-CDMI-Specification-Version', CDMI_VERSION)
        request.setHeader('Accept', CDMI_DATA)
        # XXX return corresponding capability
        #return json.dumps(...)
        