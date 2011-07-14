from twisted.web import resource
from twisted.python import log
from vcdm.server.cdmi.cdmi_content_types import CDMI_CAPABILITY

CDMI_VERSION = '1.0.1'
CDMI_SERVER_HEADER = "CDMI-Proxy/" + CDMI_VERSION

import blob, queue, container, capabilities
from cdmi_content_types import CDMI_QUEUE, CDMI_CONTAINER, CDMI_OBJECT

cdmi_objects = {CDMI_QUEUE: queue.Queue,
                CDMI_OBJECT: blob.Blob,
                CDMI_CONTAINER: container.Container,
                CDMI_CAPABILITY: capabilities.Capability}

class RootCDMIResource(resource.Resource):

    def __init__(self, avatarID = None):
        ## Twisted Resource is a not a new style class, so emulating a super-call
        resource.Resource.__init__(self)
        self.avatarID = avatarID
        log.msg("Authenticated user: %s" % avatarID)

    """
    A root CDMI resource. Handles initial request parsing and decides on the specific request processor.
    """
    def getChild(self, path, request):
        log.msg("Request path received: %s, parameters: %s" %(request.path, request.args))
        version = request.getHeader('x-cdmi-specification-version')

        if version is not None and CDMI_VERSION not in version:
            return self

        if version is not None:
            return self._decide_cdmi_object(request)
        else:
            return self._decide_non_cdmi_object(request.path)

    def render(self, request):
        return "Unsupported request: %s" % request

    def _decide_non_cdmi_object(self, path):
        # if we have a normal http request, there are two possibilities - either we are creating a new container or a new object
        # we distinguish them based on a trailing slash
        if path.endswith('/'):
            return container.NonCDMIContainer(self.avatarID)
        else:
            return blob.NonCDMIBlob(self.avatarID)

    def _decide_cdmi_object(self, request):
        content = request.getHeader('content-type')
        accept = request.getHeader('accept')

        # decide on the object to be used for processing the request

        # for DELETE we have a special case: either a container or a blob. Difference - trailing slash.
        if request.method == 'DELETE':
            if request.path.endswith('/'):
                return cdmi_objects[CDMI_CONTAINER](self.avatarID)
            else:
                return cdmi_objects[CDMI_OBJECT](self.avatarID)

        # for blobs
        if content == CDMI_OBJECT and accept == CDMI_OBJECT \
            or accept == CDMI_OBJECT and content is None:
            return cdmi_objects[CDMI_OBJECT](self.avatarID)

        # for queues
        if content ==  CDMI_QUEUE and accept == CDMI_QUEUE:
            return cdmi_objects[CDMI_QUEUE](self.avatarID)

        # for containers
        if content == CDMI_CONTAINER or accept == CDMI_CONTAINER \
            or content is None and accept == CDMI_CONTAINER:
            return cdmi_objects[CDMI_CONTAINER](self.avatarID)

        # capabilities
        if accept == CDMI_CAPABILITY:
            return cdmi_objects[CDMI_CAPABILITY](self.avatarID)

        log.err("Failed to decide which CDMI object to use: %s, %s" % (content, accept))
        return self
