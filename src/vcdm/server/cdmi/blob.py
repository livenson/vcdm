"""
Process blob-specific CDMI request.
"""
from twisted.python import log
from twisted.web.server import NOT_DONE_YET
from twisted.web.static import NoRangeStaticProducer

from vcdm import blob
from vcdm import c
from vcdm.server.cdmi.cdmi_content_types import CDMI_OBJECT
from vcdm.server.cdmi.generic import set_common_headers, parse_path,\
    get_common_body
from vcdm.server.cdmi.cdmiresource import StorageResource

from httplib import OK, CREATED, FOUND
from StringIO import StringIO
import base64

try:
    import json
except ImportError:
    import simplejson as json


class Blob(StorageResource):
    isLeaf = True  # data items cannot be nested
    allowedMethods = ('PUT', 'GET', 'DELETE', 'HEAD')

    def render_GET(self, request, bodyless=False):
        """GET operation corresponds to reading of the blob object"""
        # process path and extract potential containers/fnm
        _, __, fullpath = parse_path(request.path)

        tre_header = request.getHeader('tre-enabled')
        tre_request = tre_header is not None and tre_header.lower() == 'true'
        log.msg("Request for TRE-enabled download received.")
        # perform operation on ADT
        status, vals = blob.read(self.avatar, fullpath, tre_request)
        # construct response
        request.setResponseCode(status)

        request.setHeader('Content-Type', CDMI_OBJECT)
        if tre_request and status == FOUND:
            request.setHeader('Location', "/".join([c('general', 'tre_server'),
                                                    str(vals['uid'])]))
            request.setLastModified(float(vals['mtime']))

        set_common_headers(request)
        if status == OK:
            # for content we want to read in the full object into memory
            request.setLastModified(float(vals['mtime']))
            if not bodyless:
                content = vals['content'].read()
                # construct body
                response_body = {
                                 'completionStatus': 'Complete',
                                 'mimetype': vals['mimetype'],
                                 'metadata': vals['metadata'],
                                 'value': content,
                                 'actual_uri': vals.get('actual_uri'),
                                 'capabilitiesURI': '/cdmi_capabilities/dataobject'
                                 }
                response_body.update(get_common_body(request, str(vals['uid']),
                                                     fullpath))
                return json.dumps(response_body)
            return ''  # empty body for bodyless requests
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
        desired_backend = metadata.get('desired_backend') or request.getHeader('desired_backend')
        valueencoding = body.get('valuetransferencoding', 'utf-8')
        value = body['value'] if valueencoding == 'utf-8' else base64.b64decode(body['value'])
        content = (StringIO(value), len(value))
        status, uid = blob.write(self.avatar, name, container_path, fullpath,
                                 mimetype, metadata, content, desired_backend)
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
        """Custom HEAD operation - Twisted's automatic body swallowing is failing on certain requests"""
        return self.render_GET(request, bodyless=True)


class NonCDMIBlob(StorageResource):
    isLeaf = True
    allowedMethods = ('PUT', 'GET', 'DELETE', 'HEAD')

    def makeProducer(self, request, content_object):
        request.setResponseCode(OK)
        # TODO: add full support for multi-part download and upload
        # TODO: twisted.web.static.File is a nice example for streaming
        # TODO: For non-local backends twisted.web.Proxy approach should be reused.
        return NoRangeStaticProducer(request, content_object)

    def render_GET(self, request, bodyless=False):
        """GET returns contents of a blob"""
        # process path and extract potential containers/fnm
        _, __, fullpath = parse_path(request.path)
        log.msg("Getting blob (non-cdmi) %s" % fullpath)
        tre_header = request.getHeader('tre-enabled')
        tre_request = tre_header is not None and tre_header.lower() == 'true'
        # perform operation on ADT
        status, vals = blob.read(self.avatar, fullpath, tre_request)
        # construct response
        request.setResponseCode(status)
        set_common_headers(request, False)
        if tre_request and status == FOUND:
            request.setHeader('Location', "/".join([c('general', 'tre_server'),
                                                    str(vals['uid'])]))

        if status is OK:
            # XXX: hack - some-why the response just hangs if to simply path
            # mimetype as a content_object type
            mimetype = vals['mimetype']
            actual_type = 'text/plain' if mimetype == 'text/plain' else str(mimetype)
            request.setHeader('Content-Type', actual_type)
            request.setLastModified(float(vals['mtime']))
            if not bodyless:
                request.setHeader('Content-Length', str(vals['size']))
                producer = self.makeProducer(request, vals['content'])
                producer.start()
                return NOT_DONE_YET
            else:
                return ''
        return ''

    def render_PUT(self, request):
        """PUT corresponds to a create/update operation on a blob"""
        # process path and extract potential containers/fnm
        name, container_path, fullpath = parse_path(request.path)
        length = request.getHeader('Content-Length')
        if length is None:
            request.setResponseCode(411)
            return ''
        content = (request.content, int(length))
        # default values of mimetype and metadata
        mimetype = request.getHeader('Content-Type') if request.getHeader('Content-Type') is not None else 'text/plain'
        desired_backend = request.getHeader('desired_backend')
        status, _ = blob.write(self.avatar, name, container_path, fullpath,
                               mimetype, {}, content, desired_backend)
        request.setResponseCode(status)
        set_common_headers(request, False)
        return ''

    def render_DELETE(self, request):
        """DELETE operations corresponds to the blob deletion operation"""
        _, __, fullpath = parse_path(request.path)
        status = blob.delete(self.avatar, fullpath)
        request.setResponseCode(status)
        set_common_headers(request, False)
        return ''

    def render_HEAD(self, request):
        """Custom HEAD operation - Twisted's automatic body swallowing is failing on certain requests"""
        return self.render_GET(request, bodyless=True)
