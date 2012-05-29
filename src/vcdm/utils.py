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
""" Set of common utilities """
import sys
import os
import errno
import datetime

from twisted.python import log, util

import vcdm
from vcdm.accounting import send_ogf_ur_accounting

conf = vcdm.config.get_config()


def copyStreamToStream(streamFrom, streamTo, input_length=sys.maxint, offset=0,
                        buffer=2 ** 2 ** 2 ** 2):
    """ Copy contents of one stream into another. """
    streamFrom.seek(offset, 0)
    nbytes = 0
    while  nbytes < input_length:
                chunk = streamFrom.read(min(input_length - nbytes, buffer))
                if not chunk:
                    break
                streamTo.write(chunk)
                nbytes += len(chunk)


def print_memory_stats(location_tag="undef"):
    """ Printout memory usage statistics. """
    try:
        import psutil
        p = psutil.Process(os.getpid())
        rm, vm = p.get_memory_info()
        print "MEM_STAT (%s) rm=%s, vm=%s" % (location_tag, rm, vm)
    except ImportError:
        print "psutil module not available"


class AccountingLogObserver(log.FileLogObserver):
    """Observer for the accounting log events. Keeps track of a number of basic operations and dumps stats every
    defined period to an accounting log and optionally UR server"""

    def __init__(self, f):
        log.FileLogObserver.__init__(self, f)
        self.aggregated_operations = 0

    def emit(self, eventDict):
        if eventDict.get('type') == 'accounting':
            acc_type = eventDict.get('acc_type')
            if acc_type != 'blob_total_size':
                self.aggregated_operations += eventDict.get('amount')
            else:
                timeStr = datetime.datetime.fromtimestamp(eventDict['time']).isoformat()
                avatar = eventDict.get('avatar')
                amount = eventDict.get('amount')
                acc_type = eventDict.get('acc_type')
                start_time = datetime.datetime.fromtimestamp(eventDict.get('start_time', 0)).isoformat()
                end_time = datetime.datetime.fromtimestamp(eventDict.get('end_time', 0)).isoformat()

                msg = "%s %s %s %s %s %s\n" % (timeStr, start_time, end_time, avatar, amount, self.aggregated_operations)
                if conf.getboolean('general', 'send_accounting_to_ur'):
                    send_ogf_ur_accounting(start_time, end_time, avatar, amount, self.aggregated_operations)
                util.untilConcludes(self.write, msg)
                util.untilConcludes(self.flush)
                self.aggregated_operations = 0


def check_path(container_path):
    # for a top-level container - all is good
    if container_path == ['/']:
        return True
    # XXX: probably not the best way to do the search, but seems to work
    # construct all possible fullpaths of containers and do a search for them
    all_paths = []
    for i, value in enumerate(container_path):
        if i == 0:  # top-level
            all_paths.append('/')
        else:
            all_paths.append(all_paths[i - 1].rstrip('/') + '/' + value)

    log.msg("Checking paths: %s" % all_paths)
    # XXX: better to embed len into the request
    return len(vcdm.env['ds'].find_path_uids(all_paths)) == len(container_path)


def mkdir_p(path):
    """Emulate mkdir -p in Python"""
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST:
            pass
        else: raise
