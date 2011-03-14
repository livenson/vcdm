"""
Process blob-specific CDMI request.
Parse and decode 
"""

from twisted.web import resource
from vcdm import blob
from vcdm.server.cdmi.cdmi_content_types import CDMI_DATA, CDMI_OBJECT

from root import CDMI_VERSION

try:
    import json
except ImportError:
    import simplejson as json

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
        
        # TODO: encode body into json
        return "%s" % d

    def render_PUT(self, request):
        # TODO: once we have a normal folder system, remove this hack        
        fullpath = request.path
        tmp = fullpath.split('/')
        container_path = tmp[:-1]
        filename = tmp[-1]        
        length = int(request.getHeader('Content-Length'))        
        request.content.seek(0, 0)
        body = json.loads(request.content.read(length))
        
        #container_path, fullpath,
        status, uid = blob.write(filename, body['value'])
        request.setResponseCode(status)        
        request.setResponseCode(status)
        request.setHeader('Content-Type', CDMI_OBJECT)
        request.setHeader('X-CDMI-Specification-Version', CDMI_VERSION)
        response_body = {'objectID': uid,
                         'objectURI': request.uri,
                         'domainURI': request.host[1] + ":" + str(request.host[2]),
                         'parentURI': request.uri + container_path[-1],
                         'capabilitiesURI': None, 
                         'completionStatus': 'Complete',
                         'mimetype': body['mimetype'], 
                         'metadata': None,
                         }  
        return json.dumps(response_body)
        

    def render_DELETE(self, request):
        fnm = '/' + request.postpath[0]
        status, params = blob.delete(fnm)
        request.setResponseCode(status)
        return "delete, Data (%s), status = %s" %(request, status)
