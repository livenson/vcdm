from twisted.web import resource
from httplib import BAD_REQUEST


class StorageResource(resource.Resource):
    """Common parent for all resources representing storage objects"""

    def __init__(self, avatar='Anonymous', delegated_user=None):
        resource.Resource.__init__(self)
        self.avatar = avatar
        self.delegated_user = delegated_user

    def render(self, request):
        actual_render = getattr(self, 'render_%s' % request.method)
        try:
            return actual_render(request)
        except ValueError as e:
            typical_message = 'No JSON object could be decoded'
            if e.message == typical_message:
                request.setResponseCode(BAD_REQUEST, message='CDMI Request body is malformed')
                return ''
            else:
                raise e
