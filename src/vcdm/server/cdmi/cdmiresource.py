from twisted.web import resource


class StorageResource(resource.Resource):
    """Common parent for all resources representing storage objects"""

    def __init__(self, avatar='Anonymous', delegated_user=None):
        resource.Resource.__init__(self)
        self.avatar = avatar
        self.delegated_user = delegated_user
