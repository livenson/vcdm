""" Set of common utilities """
import sys
import os
import errno

from twisted.python import log
from twisted.python import util


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

    def __init__(self, f):
        log.FileLogObserver.__init__(self, f)

    def emit(self, eventDict):
        if eventDict.get('type') == 'accounting':
            timeStr = self.formatTime(eventDict['time'])
            avatar = eventDict.get('avatar')
            amount = eventDict.get('amount')
            acc_type = eventDict.get('acc_type')
            msg = "%s %s %s %s\n" % (timeStr, avatar, acc_type, amount)
            util.untilConcludes(self.write, msg)
            util.untilConcludes(self.flush)


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
    import vcdm
    return len(vcdm.env['ds'].find_path_uids(all_paths)) == len(container_path)


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST:
            pass
        else: raise
