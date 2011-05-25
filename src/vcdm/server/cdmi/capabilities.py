from twisted.web import resource
from vcdm.server.cdmi.cdmi_content_types import CDMI_CAPABILITY
from vcdm.server.cdmi.root import CDMI_VERSION
from vcdm.server.cdmi.generic import parse_path, get_common_body
from vcdm.server.cdmi import current_capabilities
from httplib import OK


try:
    import json
except ImportError:
    import simplejson as json
    
capability_objects = {'system': current_capabilities.system,
                      'dataobject': current_capabilities.dataobject,
                      'mq': current_capabilities.mq,
                      'container': current_capabilities.container} 

class Capability(resource.Resource):
    isLeaf = True 
    allowedMethods = ('GET') 

    def render_GET(self, request):
        # for now only support top-level capabilities
        _, __, fullpath = parse_path(request.path)
        
        # TODO: how to handle the missing UID? Perhaps, store capabilities in datastore?
        body = get_common_body(request, None, fullpath) 
        # is it request for a system-level capability?
        if fullpath == '/cdmi_capabilities':
            body['capabilities'] = capability_objects['system'] 
            body.update({
                    'childrenrange': "0-1",
                    'children': [
                            "dataobject/",
                            "container/",
                            "mq/"
                        ]
                })           
        elif fullpath.startswith('/cdmi_capabilities/dataobject'):
            body['capabilities'] = capability_objects['dataobject']
        elif fullpath.startswith('/cdmi_capabilities/mq'):
            body['capabilities'] = capability_objects['mq']
        elif fullpath.startswith('/cdmi_capabilities/container'):
            body['capabilities'] = capability_objects['container']                
        
        # construct response
        request.setResponseCode(OK)
        request.setHeader('Content-Type', CDMI_CAPABILITY)
        request.setHeader('X-CDMI-Specification-Version', CDMI_VERSION)        
        return json.dumps(body)
        