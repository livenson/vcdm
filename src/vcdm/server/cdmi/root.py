from twisted.web import resource, http

import blob, queue
from cdmi_content_types import CDMI_DATA, CDMI_QUEUE
from vcdm.server.cdmi.cdmi_exit_codes import BAD_REQUEST

cdmi_objects = {CDMI_QUEUE: queue.Queue,
                CDMI_DATA: blob.Blob}

CDMI_VERSION = '1.0'

class RootCDMIResource(resource.Resource):
    """
    A root resource which is protected by guard and requires authentication in order to access.
    """
    def getChild(self, path, request):     
        content = request.getHeader('content-type')
        accept_field = request.getHeader('accept')
        version = request.getHeader('x-cdmi-specification-version')
        ## Request validation. 
        # TODO: possibly move to a separate function            
        if content != accept_field or CDMI_VERSION not in version or content not in cdmi_objects.keys():
            return BAD_REQUEST               
        return cdmi_objects[content]()            

    def render(self, request):
        return "Unforeseen error for request: %s", request
