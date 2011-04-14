"""
Process blob-specific CDMI request.
"""

from twisted.web import resource
from vcdm import blob
from vcdm.server.cdmi.cdmi_content_types import CDMI_OBJECT

from vcdm.server.cdmi.generic import set_common_headers, parse_path,\
    get_common_body

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
        _, __, fullpath = parse_path(request.path)
        
        # perform operation on ADT
        status, content, uid, mimetype, metadata = blob.read(fullpath)
        
        # construct response
        request.setResponseCode(status)
        request.setHeader('Content-Type', CDMI_OBJECT)
        set_common_headers(request)            
        
        # construct body
        response_body = {
                         'completionStatus': 'Complete',
                         'mimetype': mimetype, 
                         'metadata': metadata,
                         'value': content,
                         'capabilitiesURI': '/cdmi_capabilities/dataobject'
                         }  
        response_body.update(get_common_body(request, uid, fullpath))
        return json.dumps(response_body)
        
    def render_PUT(self, request):
        """PUT corresponds to a create/update operation on a blob"""
        # process path and extract potential containers/fnm
        name, container_path, fullpath = parse_path(request.path)
        
        length = int(request.getHeader('Content-Length'))    
        request.content.seek(0, 0)
        # process json encoded request body
        body = json.loads(request.content.read(length))
        # default values of mimetype and metadata
        mimetype = 'text/plain' 
        metadata = {}
        if 'mimetype' in body:
            mimetype = body['mimetype'] 
        if 'metadata' in body:
            metadata = body['metadata']
                
        status, uid = blob.write(name, container_path, fullpath, mimetype, metadata, body['value'])
        
        request.setResponseCode(status)
        request.setHeader('Content-Type', CDMI_OBJECT)
        set_common_headers(request)

        response_body = {
                         'completionStatus': 'Complete',
                         'mimetype': mimetype, 
                         'metadata': metadata,
                         }
        # add common elements
        response_body.update(get_common_body(request, uid, fullpath))
          
        return json.dumps(response_body)
        

    def render_DELETE(self, request):
        """DELETE operations corresponds to the blob deletion operation"""
        _, __, fullpath = parse_path(request.path)
        status = blob.delete(fullpath)
        request.setResponseCode(status)
        set_common_headers(request)
        return ""
