from twisted.web import resource, http

import blob, queue

cdmi_objects = {'mq': queue.Queue,
                'blob': blob.Blob}

class RootCDMIResource(resource.Resource):
    """
    A root resource which is protected by guard and requires authentication in order to access.
    """
    def getChild(self, type, request):       
        # TODO: choose processor based on the mime type 
        if type in cdmi_objects:
            return cdmi_objects[type]()
        else:
            return self

    def render(self, request):
        return "Unsupported"
