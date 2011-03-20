"""
Process blob-specific CDMI request.
"""

from twisted.web import resource
from vcdm import blob
from vcdm.server.cdmi.cdmi_content_types import CDMI_OBJECT

from root import CDMI_VERSION

try:
    import json
except ImportError:
    import simplejson as json

class Blob(resource.Resource):
    isLeaf = True # data items cannot be nested
    allowedMethods = ('PUT','GET','DELETE') # commands we support for the data items

    def render_GET(self, request):
        """GET operation corresponds to reading of the blob object"""
        # process path and extract potential containers/fnm
        fullpath = request.path
        tmp = fullpath.split('/')
        container_path = tmp[:-1]                    
        status, content, uid, metadata, mimetype = blob.read(fullpath)
        
        # construct response
        request.setResponseCode(status)
        request.setHeader('Content-Type', CDMI_OBJECT)
        request.setHeader('X-CDMI-Specification-Version', CDMI_VERSION)
        
        response_body = {'objectURI': request.uri,
                         'objectID': uid,                         
                         'domainURI': request.host[1] + ":" + str(request.host[2]),
                         'parentURI': request.uri + container_path[-1],
                         'capabilitiesURI': None, 
                         'completionStatus': 'Complete',
                         'mimetype': mimetype, 
                         'metadata': metadata,
                         'value': content
                         }  
        return json.dumps(response_body)
        
    def render_PUT(self, request):
        """PUT corresponds to a create/update operation on a blob"""
        # process path and extract potential containers/fnm
        fullpath = request.path
        tmp = fullpath.split('/')
        container_path = tmp[:-1]
        filename = tmp[-1]
        length = int(request.getHeader('Content-Length'))        
        request.content.seek(0, 0)
        # process json encoded request body
        body = json.loads(request.content.read(length))
        mimetype = body['mimetype'] if body['mimetype'] is not None else 'text/plain'
        metadata = body['metadata']
                
        status, uid = blob.write(container_path, filename, mimetype, metadata, body['value'])
        request.setResponseCode(status)
        request.setHeader('Content-Type', CDMI_OBJECT)
        request.setHeader('X-CDMI-Specification-Version', CDMI_VERSION)
        response_body = {'objectID': uid,
                         'objectURI': request.uri,
                         'domainURI': request.host[1] + ":" + str(request.host[2]),
                         'parentURI': request.uri + container_path[-1],
                         'capabilitiesURI': None, 
                         'completionStatus': 'Complete',
                         'mimetype': mimetype, 
                         'metadata': metadata,
                         }  
        return json.dumps(response_body)
        

    def render_DELETE(self, request):
        """DELETE operations corresponds to the blob deletion operation"""
        fullpath = request.path
        status = blob.delete(fullpath)
        request.setResponseCode(status)                   
        return ""
