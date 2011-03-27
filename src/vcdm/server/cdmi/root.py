from twisted.web import resource
from vcdm.server.http_status_codes import BAD_REQUEST

CDMI_VERSION = '1.0'
CDMI_SERVER_HEADER = "VCDM/" + CDMI_VERSION

import blob, queue, container
from cdmi_content_types import CDMI_DATA, CDMI_QUEUE, CDMI_CONTAINER, CDMI_OBJECT

cdmi_objects = {CDMI_QUEUE: queue.Queue,
                CDMI_DATA: blob.Blob,
                CDMI_CONTAINER: container.Container}

class RootCDMIResource(resource.Resource):
    """
    A root CDMI resource. Handles initial request parsing and decides on the specific request processor.
    """
    def getChild(self, path, request):     
        content = request.getHeader('Content-Type')        
        version = request.getHeader('X-CDMI-Specification-Version')
        accept = request.getHeader('Accept') 
        
        ## == Request validation. == 
        # TODO: possibly move to a separate function      
        ## Current CDMI version is a bit inconsistent wrt to accept/content-types. Picking a processing object 
        ## is not an obvious step. For now, we abuse the specification and require some of the optional fields to be present.    
        if version is None or CDMI_VERSION not in version:
            return BAD_REQUEST
        
        # decide on the object to be used for processing the request
        if content ==  CDMI_DATA and accept == CDMI_DATA \
            or accept == CDMI_DATA and content == CDMI_OBJECT:  # create | update | delete
            return cdmi_objects[CDMI_DATA]()
        
        # for queues            
        if content ==  CDMI_QUEUE and accept == CDMI_QUEUE:
            return cdmi_objects[CDMI_QUEUE]()
        
        # for containers
        if content == CDMI_OBJECT and accept == CDMI_CONTAINER \
            or content == CDMI_CONTAINER and accept == CDMI_CONTAINER:
            return cdmi_objects[CDMI_CONTAINER]()       
        
        return "Unknown object requested: %s, %s" %(content, accept) # if nothing matches            

    def render(self, request):
        return "Unforeseen error for request: %s", request
