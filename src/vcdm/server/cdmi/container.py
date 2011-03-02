from  twisted.web import resource

from  vcdm import container

class Container(resource.Resource):
    isLeaf = True
    allowMethods = ('PUT', 'GET', 'DELETE')

    def render_GET(self, request):
        # parse the request
        fnm = '/' + request.postpath[0]
        # contact the backend
        status, data = container.read(fnm)
        # create a header
        request.setResponseCode(status)
        # request.setHeader()
        return "%s" % data
    
    def render_PUT(self, request):
        fnm = '/' + request.postpath[0]
        request.content.seek(0, 0)
        d = request.content.read()
        status, uid = container.write(fnm, d)
        request.setResponseCode(status)
        return "saving content into %s, uid = %s" % (fnm, str(uid))

    def render_DELETE(self, request):
        fnm = '/' + request.postpath[0]
        status, smth = container.delete(fnm)
        request.setResponseCode(status)
        return "delete, Data (%s), status = %s" % (request, status)

