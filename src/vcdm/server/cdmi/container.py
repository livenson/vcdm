##
# Copyright 2002-2012 Ilja Livenson, PDC KTH
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##
from twisted.python import log

from vcdm import container
from vcdm.server.cdmi.cdmi_content_types import CDMI_CONTAINER
from vcdm.server.cdmi.generic import parse_path, set_common_headers,\
    get_common_body
from vcdm.server.cdmi.cdmiresource import StorageResource

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
        status, vals = container.read(self.avatar, fullpath)

        # create a header
        request.setResponseCode(status)
        request.setHeader('Content-Type', CDMI_CONTAINER)
        set_common_headers(request)

        # and a body
        if status == OK:
            request.setLastModified(float(vals['mtime']))
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
        req_length = request.getHeader('Content-Length')
        if req_length is None:
            request.setResponseCode(411)
            return ''

        req_length = int(req_length)
        request.content.seek(0, 0)
        # process json encoded request body
        body = request.content.read(req_length) if req_length > 0 else '{}'  # a workaround for a buggy curl behavior
        body = json.loads(body)
        metadata = {}
        if 'metadata' in body:
            metadata = body['metadata']
        status, vals = container.create_or_update(self.avatar, name,
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
        status = container.delete(self.avatar, fullpath)
        request.setResponseCode(status)
        set_common_headers(request)
        return ""


class NonCDMIContainer(StorageResource):
    isLeaf = True
    allowMethods = ('PUT', 'GET', 'DELETE')

    def render_GET(self, request):
        """GET operation corresponds to reading a container's data."""
        # parse the request
        _, __, fullpath = parse_path(request.path)

        # contact the backend
        status, vals = container.read(self.avatar, fullpath)
        # create a header
        request.setResponseCode(status)
        set_common_headers(request, False)
        if status == OK:
            request.setHeader('Content-Type', 'application/json')
            request.setLastModified(float(vals['mtime']))
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
        status, _ = container.create_or_update(self.avatar, name,
                                               container_path, fullpath, {})
        request.setResponseCode(status)
        set_common_headers(request, False)
        return ""

    def render_DELETE(self, request):
        _, __, fullpath = parse_path(request.path)
        status = container.delete(self.avatar, fullpath)
        request.setResponseCode(status)
        set_common_headers(request, False)
        return ""
