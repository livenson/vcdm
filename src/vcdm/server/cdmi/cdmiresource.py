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
from twisted.web import resource
from httplib import BAD_REQUEST


class StorageResource(resource.Resource):
    """Common parent for all resources representing storage objects"""

    def __init__(self, avatar='Anonymous', delegated_user=None):
        resource.Resource.__init__(self)
        self.avatar = avatar
        self.delegated_user = delegated_user

    def render(self, request):
        actual_render = getattr(self, 'render_%s' % request.method)
        try:
            return actual_render(request)
        except ValueError as e:
            typical_message = 'No JSON object could be decoded'
            if e.message == typical_message:
                request.setResponseCode(BAD_REQUEST, message='CDMI Request body is malformed')
                return ''
            else:
                raise e
