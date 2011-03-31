from twisted.web import resource
from vcdm.server.cdmi.cdmi_content_types import CDMI_CAPABILITY, CDMI_DATA
from vcdm.server.cdmi.root import CDMI_VERSION
from vcdm.server.http_status_codes import BAD_REQUEST, OK
from vcdm.server.cdmi.generic import parse_path, get_common_body
from vcdm.server.cdmi import current_capabilities


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

    def render_GET(self, fixed_path, request):
        # for now only support top-level capabilities
        name, container_path, fullpath = parse_path(request.path)
        
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
        request.setHeader('Accept', CDMI_DATA)
        return json.dumps(body)
        