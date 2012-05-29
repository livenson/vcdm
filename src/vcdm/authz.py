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

from vcdm import c


def authorize(avatar, resource, action, acls=None):
    """
    Top-level authorize function dispatching calls to the configured authZ
    mechanism.
    """
    try:
        result = mechanisms[c('general', 'server.authz')](avatar, resource,
                                                          action, acls)
        log.err("Authorized request: %s" % result)
        return result
    except KeyError:
        log.err("Requested authZ mechanism %s was not found.")
        return False  # default failover


### Implementations ###
def dummy(avatar, resource, action, acls):
    """Dummy authorization schema, allows everything."""
    log.msg("Dummy authorization of %s to perform %s on %s. ACLs: %s" %
            (avatar, action, resource, acls))
    return True


def strict(avatar, resource, action, acls):
    """Only allows operation if a user has the corresponding bit set"""
    log.msg("Strict authorization of %s to perform %s on %s. ACLs: %s" %
            (avatar, action, resource, acls))
    if resource == '/':
        return True  # allow everything for the root folder
    if acls is None:
        return False  # disallowed by default
    for prefix in ['read', 'write', 'delete']:
        if action.startswith(prefix):
            user_acls = acls.get(avatar)
            if user_acls is None:
                return False  # disallowed by default
            return rights[prefix] in user_acls
    return False

# map of all possible mechanisms
mechanisms = {'dummy': dummy,
              'strict': strict}

rights = {'read': 'r',
          'write': 'w',
          'delete': 'd'}
