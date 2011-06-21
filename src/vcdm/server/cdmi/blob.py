"""
Process blob-specific CDMI request.
"""

from twisted.web import resource
from twisted.python import log

from vcdm import blob
from vcdm.server.cdmi.cdmi_content_types import CDMI_OBJECT

from vcdm.server.cdmi.generic import set_common_headers, parse_path,\
    get_common_body
from vcdm.server.cdmi.root import CDMI_SERVER_HEADER
from httplib import NOT_FOUND, OK, CREATED
from twisted.web.server import NOT_DONE_YET
from twisted.web.static import NoRangeStaticProducer
from StringIO import StringIO
import sys

try:
    import json
except ImportError:
    import simplejson as json

class Blob(resource.Resource):
    isLeaf = True # data items cannot be nested
    allowedMethods = ('PUT','GET','DELETE', 'HEAD') # commands we support for the data items
    
    def __init__(self, avatar = None):        
        resource.Resource.__init__(self)
        self.avatar = avatar

    def render_GET(self, request):
        """GET operation corresponds to reading of the blob object"""
        # process path and extract potential containers/fnm
        _, __, fullpath = parse_path(request.path)
        
        # perform operation on ADT
        status, content_object, uid, mimetype, metadata, _ = blob.read(self.avatar,fullpath)
        
        # construct response
        request.setResponseCode(status)
        request.setHeader('Content-Type', CDMI_OBJECT)
        set_common_headers(request)
        if status == OK:
            # for content we want to read in the full object into memory
            content = content_object.read()
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
        else:
            return ''
        
    def render_PUT(self, request):
        """PUT corresponds to a create/update operation on a blob"""
        # process path and extract potential containers/fnm
        name, container_path, fullpath = parse_path(request.path)
        
        length = int(request.getHeader('Content-Length'))
        request.content.seek(0, 0)
        # process json encoded request body
        body = json.loads(request.content.read(length))
        # default values of mimetype and metadata
        mimetype = body.get('mimetype', 'text/plain') 
        metadata = body.get('metadata', {})
        
        content = (StringIO(body['value']), sys.getsizeof(body['value']))
        status, uid = blob.write(self.avatar, name, container_path, fullpath, mimetype, metadata, content)
        request.setResponseCode(status)
        request.setHeader('Content-Type', CDMI_OBJECT)
        set_common_headers(request)
        if status == OK or status == CREATED:
            response_body = {
                             'completionStatus': 'Complete',
                             'mimetype': mimetype, 
                             'metadata': metadata,
                             }
            # add common elements
            response_body.update(get_common_body(request, uid, fullpath))              
            return json.dumps(response_body)
        else:
            # error state
            return ''
        
    def render_DELETE(self, request):
        """DELETE operations corresponds to the blob deletion operation"""
        _, __, fullpath = parse_path(request.path)
        status = blob.delete(self.avatar, fullpath)
        request.setResponseCode(status)
        set_common_headers(request)
        return ''
    
    def render_HEAD(self, request):
        """ XXX: In general HEAD should have the same semantics as GET - body. 
        But for now abuse it a bit."""
        _, __, fullpath = parse_path(request.path)
        request.setResponseCode(blob.exists(self.avatar, fullpath))
        return ''


class NonCDMIBlob(resource.Resource):
    isLeaf = True # data items cannot be nested
    allowedMethods = ('PUT','GET','DELETE', 'HEAD') # commands we support for the data items
    
    def makeProducer(self, request, content_object):       
        request.setResponseCode(OK)
        # TODO: add full support for multi-part download and upload
        # TODO: twisted.web.static.File is a nice example for streaming
        # TODO: For non-local backends twisted.web.Proxy approach should be reused.
        return NoRangeStaticProducer(request, content_object)        
    
    def __init__(self, avatar = None):        
        resource.Resource.__init__(self)
        self.avatar = avatar

    def render_GET(self, request):
        # process path and extract potential containers/fnm
        _, __, fullpath = parse_path(request.path)
        log.msg("Getting blob (non-cdmi) %s" % fullpath)        
        # perform operation on ADT
        status, content_object, _, mimetype, __, size = blob.read(self.avatar, fullpath)        
        # construct response
        request.setResponseCode(status)
        if status is not NOT_FOUND:
            # XXX: hack - somewhy the response just hangs if to simply path mimetype as a content_object type
            actual_type = 'text/plain' if mimetype == 'text/plain' else str(mimetype) # convert to str to avoid UnicodeDecodeError in twisted
            request.setHeader('Content-Type', actual_type)          
            request.setHeader('Content-Length', str(size))
            producer = self.makeProducer(request, content_object)
            producer.start()
            return NOT_DONE_YET
        return ''
        
    def render_HEAD(self, request):
        _, __, fullpath = parse_path(request.path)
        request.setResponseCode(blob.exists(self.avatar, fullpath))
        return ''
        
    def render_PUT(self, request):
        """PUT corresponds to a create/update operation on a blob"""
        # process path and extract potential containers/fnm
        name, container_path, fullpath = parse_path(request.path)
        length = int(request.getHeader('Content-Length'))    
        content = (request.content, length)
        # default values of mimetype and metadata        
        mimetype = request.getHeader('Content-Type') \
                    if request.getHeader('Content-Type') is not None \
                    else 'text/plain'
        status, _ = blob.write(self.avatar, name, container_path, fullpath, mimetype, {}, content)        
        request.setResponseCode(status)
        return ''
    
    def render_DELETE(self, request):
        """DELETE operations corresponds to the blob deletion operation"""
        _, __, fullpath = parse_path(request.path)
        status = blob.delete(self.avatar, fullpath)
        request.setResponseCode(status)
        request.setHeader('Server', CDMI_SERVER_HEADER)
        return ''