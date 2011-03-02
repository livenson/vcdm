from twisted.web import resource, server
from vcdm import blob
from vcdm.server.cdmi.cdmi_content_types import CDMI_DATA, CDMI_OBJECT
from vcdm.server.cdmi.root import CDMI_VERSION

class Blob(resource.Resource):
    isLeaf = True # data items cannot be nested
    allowedMethods = ('PUT','GET','DELETE') # commands we support for the data items

    def render_GET(self, request):
        # TODO: get fnm from request, validate. for now just assume it's everything after the path
        fnm = '/' + request.postpath[0]        
        # TODO: get range of bytes from the request. For now just assume static
        #rng = request.
        rng = None
        status, d = blob.read(fnm, rng)
        
        # construct response
        request.setResponseCode(status)
        request.setHeader('Content-Type', CDMI_OBJECT)
        request.setHeader('X-CDMI-Specification-Version', CDMI_VERSION)
        request.setHeader('Accept', CDMI_DATA)
        return "%s" % d

    def render_PUT(self, request):
        # TODO: once we have a normal folder system, remove this hack
        fnm = '/' + request.postpath[0]
        request.content.seek(0, 0)
        d = request.content.read()
        status, uid = blob.write(fnm, d)
        request.setResponseCode(status)        
        return "saving content into %s, uid = %s" % (fnm, str(uid))
        

    def render_DELETE(self, request):
        fnm = '/' + request.postpath[0]
        status, params = blob.delete(fnm)
        request.setResponseCode(status)
        return "delete, Data (%s), status = %s" %(request, status)
