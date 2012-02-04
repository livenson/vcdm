from twisted.python import log

from vcdm import container
from vcdm.server.cdmi.cdmi_content_types import CDMI_CONTAINER
from vcdm.server.cdmi.generic import parse_path, set_common_headers,\
    get_common_body, CDMI_SERVER_HEADER
from vcdm.server.cdmi.root import StorageResource

from httplib import OK

try:
    import json
except ImportError:
    import simplejson as json


class Container(StorageResource):
    isLeaf = True
    allowMethods = ('PUT', 'GET', 'DELETE')

    def render_GET(self, request):
        """GET operation corresponds to reading container's data"""
        # parse the request
        _, __, fullpath = parse_path(request.path)

        # contact the backend
        status, vals = container.read(self.avatarID, fullpath)

        # create a header
        request.setResponseCode(status)
        request.setHeader('Content-Type', CDMI_CONTAINER)
        request.setLastModified(float(vals['mtime']))
        set_common_headers(request)

        # and a body
        if status == OK:
            children = vals['children'].values()
            response_body = {
                             'completionStatus': 'Complete',
                             'metadata': vals['metadata'],
                             'children': children,
                             'childrenrange': '' if len(children) == 0 else '0-%s'
                                                    % len(children),
                             'capabilitiesURI': '/cdmi_capabilities/container'
                             }
            response_body.update(get_common_body(request, vals['uid'], fullpath))
            return json.dumps(response_body)
        else:
            return ''

    def render_PUT(self, request):
        name, container_path, fullpath = parse_path(request.path)
        log.msg("Creating container %s" % fullpath)
        req_length = int(request.getHeader('Content-Length'))
        request.content.seek(0, 0)
        # process json encoded request body
        body = json.loads(request.content.read(req_length))
        metadata = {}
        if 'metadata' in body:
            metadata = body['metadata']
        status, vals = container.create_or_update(self.avatarID, name,
                                                  container_path,
                                                  fullpath, metadata)
        children = vals['children'].values() if 'children' in vals else {}
        request.setResponseCode(status)
        request.setHeader('Content-Type', CDMI_CONTAINER)
        set_common_headers(request)

        # and a body
        response_body = {
                         'completionStatus': 'Complete',
                         'metadata': metadata,
                         'children': children,
                         'childrenrange': '' if len(children) == 0 else '0-%s' % len(children),
                         }
        response_body.update(get_common_body(request, vals['uid'], fullpath))

        return json.dumps(response_body)

    def render_DELETE(self, request):
        _, __, fullpath = parse_path(request.path)
        status = container.delete(self.avatarID, fullpath)
        request.setResponseCode(status)
        request.setHeader('Server', CDMI_SERVER_HEADER)
        return ""


class NonCDMIContainer(StorageResource):
    isLeaf = True
    allowMethods = ('PUT', 'GET', 'DELETE')

    def render_GET(self, request):
        """GET operation corresponds to reading a container's data."""
        # parse the request
        _, __, fullpath = parse_path(request.path)

        # contact the backend
        status, vals = container.read(self.avatarID, fullpath)
        # create a header
        request.setResponseCode(status)

        if status == OK:
            request.setHeader('Content-Type', 'application/json')
            children = None if not 'children' in vals else vals['children'].values()
            response_body = {
                             'metadata': vals['metadata'],
                             'children': children,
                             }
            return json.dumps(response_body)
        else:
            return ''

    def render_PUT(self, request):
        name, container_path, fullpath = parse_path(request.path)
        status, _ = container.create_or_update(self.avatarID, name,
                                               container_path, fullpath, {})
        request.setResponseCode(status)
        return ""

    def render_DELETE(self, request):
        _, __, fullpath = parse_path(request.path)
        status = container.delete(self.avatarID, fullpath)
        request.setResponseCode(status)
        request.setHeader('Server', CDMI_SERVER_HEADER)
        return ""
