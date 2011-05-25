from twisted.web import resource
from twisted.python import log
from vcdm.server.cdmi.cdmi_content_types import CDMI_CAPABILITY

CDMI_VERSION = '1.0.1h'
CDMI_SERVER_HEADER = "VCDM/" + CDMI_VERSION

import blob, queue, container, capabilities
from cdmi_content_types import CDMI_QUEUE, CDMI_CONTAINER, CDMI_OBJECT

cdmi_objects = {CDMI_QUEUE: queue.Queue,
                CDMI_OBJECT: blob.Blob,
                CDMI_CONTAINER: container.Container,
                CDMI_CAPABILITY: capabilities.Capability}

class RootCDMIResource(resource.Resource):
    """
    A root CDMI resource. Handles initial request parsing and decides on the specific request processor.
    """
    def getChild(self, path, request):     
        content = request.getHeader('content-type')        
        version = request.getHeader('x-cdmi-specification-version')
        accept = request.getHeader('accept')

        if version is not None:
            return self._decide_cdmi_object(content, version, accept)
        else:
            return self._decide_non_cdmi_object(request.path)

    def render(self, request):
        return "Unsupported request: %s", request
    
    def _decide_non_cdmi_object(self, path):
        # if we have a normal http request, there are two possibilities - either we are creating a new container or a new object
        # we distinguish them based on a trailing slash                
        if path.endswith('/'):
            return container.NonCDMIContainer()
        else:
            return blob.NonCDMIBlob()

    def _decide_cdmi_object(self, content, version, accept):
        ## Current CDMI version is a bit inconsistent wrt to accept/content-types. Picking a processing object 
        ## is not an obvious step. For now, we abuse the specification and require some of the optional fields to be present.
        if version is None or CDMI_VERSION not in version:
            return self
        
        # decide on the object to be used for processing the request
        if content ==  CDMI_OBJECT and accept == CDMI_OBJECT \
            or accept == CDMI_OBJECT and content == CDMI_OBJECT:  # create | update | delete
            return cdmi_objects[CDMI_OBJECT]()
        
        # for queues            
        if content ==  CDMI_QUEUE and accept == CDMI_QUEUE:
            return cdmi_objects[CDMI_QUEUE]()
        
        # for containers
        if content == CDMI_CONTAINER or accept == CDMI_CONTAINER \
            or content is None and accept == CDMI_CONTAINER:
            return cdmi_objects[CDMI_CONTAINER]()    
        
        # capabilities           
        if content == CDMI_CAPABILITY:
            return cdmi_objects[CDMI_CAPABILITY]()
        
        log.err("Failed to decide which CDMI object to use: %s, %s, %s" % (content, version, accept))
        return self