from twisted.web import resource
from twisted.python import log

import blob
import queue
import container
import capabilities

from vcdm.server.cdmi.cdmi_content_types import CDMI_CAPABILITY
from cdmi_content_types import CDMI_QUEUE, CDMI_CONTAINER, CDMI_OBJECT
from vcdm.server.cdmi.generic import CDMI_VERSION

cdmi_objects = {CDMI_QUEUE: queue.Queue,
                CDMI_OBJECT: blob.Blob,
                CDMI_CONTAINER: container.Container,
                CDMI_CAPABILITY: capabilities.Capability}


class RootCDMIResource(resource.Resource):
    """
    A root CDMI resource. Handles initial request parsing and decides on the
    specific request processor.
    """

    def __init__(self, avatarID='Anonymous'):
        ## Twisted Resource is a not a new style class, so emulating a super-call
        resource.Resource.__init__(self)
        self.avatarID = avatarID
        log.msg("User: %s" % avatarID)

    def getChild(self, path, request):
        log.msg("Request path received: %s, parameters: %s" %
                (request.path, request.args))
        version = request.getHeader('x-cdmi-specification-version')
        self.delegated_user = request.getHeader('onbehalf')
        if self.delegated_user:
            log.msg("Delegated user: %s" % self.delegated_user)

        if version is not None and CDMI_VERSION not in version:
            return self

        if version is not None:
            return self._decide_cdmi_object(request)
        else:
            return self._decide_non_cdmi_object(request.path)

    def render(self, request):
        return "Unsupported request: %s" % request

    def _decide_non_cdmi_object(self, path):
        # if we have a normal http request, there are two possibilities -
        # either we are creating a new container or a new object
        # we distinguish them based on a trailing slash
        if path.endswith('/'):
            return container.NonCDMIContainer(self.avatarID, self.delegated_user)
        else:
            return blob.NonCDMIBlob(self.avatarID, self.delegated_user)

    def _decide_cdmi_object(self, request):
        content = request.getHeader('content-type')
        accept = request.getHeader('accept')

        # decide on the object to be used for processing the request

        # for DELETE we have a special case: either a container or a blob.
        # Difference - trailing slash.
        if request.method == 'DELETE':
            if request.path.endswith('/'):
                return cdmi_objects[CDMI_CONTAINER](self.avatarID, self.delegated_user)
            else:
                return cdmi_objects[CDMI_OBJECT](self.avatarID, self.delegated_user)

        # for blobs
        if content == CDMI_OBJECT and accept == CDMI_OBJECT \
            or accept == CDMI_OBJECT and content is None:
            return cdmi_objects[CDMI_OBJECT](self.avatarID, self.delegated_user)

        # for queues
        if content == CDMI_QUEUE and accept == CDMI_QUEUE:
            return cdmi_objects[CDMI_QUEUE](self.avatarID, self.delegated_user)

        # for containers
        if content == CDMI_CONTAINER or accept == CDMI_CONTAINER \
            or content is None and accept == CDMI_CONTAINER:
            return cdmi_objects[CDMI_CONTAINER](self.avatarID, self.delegated_user)

        # capabilities
        if accept == CDMI_CAPABILITY:
            return cdmi_objects[CDMI_CAPABILITY](self.avatarID, self.delegated_user)

        log.err("Failed to decide which CDMI object to use: %s, %s"
                % (content, accept))
        return self


class StorageResource(resource.Resource):
    """Common parent for all resources representing storage objects"""

    def __init__(self, avatar='Anonymous', delegated_user=None):
        resource.Resource.__init__(self)
        self.avatar = avatar
        self.delegated_user = delegated_user
