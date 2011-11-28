""" Set of common utilities """
import sys
import os

from twisted.python.log import FileLogObserver
from twisted.python import util


def copyStreamToStream(streamFrom, streamTo, input_length=sys.maxint, offset=0,  buffer=2**2**2**2):
    """ Copy contents of one stream into another. """
    streamFrom.seek(offset, 0)
    nbytes = 0
    while  nbytes < input_length:
                chunk = streamFrom.read(min(input_length-nbytes, buffer))
                if not chunk:
                    break
                streamTo.write(chunk)
                nbytes += len(chunk)
                
def print_memory_stats(location_tag = "undef"):
    """ Printout memory usage statistics. """
    try:
        import psutil
        p = psutil.Process(os.getpid())
        rm, vm = p.get_memory_info()
        print "MEM_STAT (%s) rm=%s, vm=%s" % (location_tag, rm, vm)
    except ImportError:
        print "psutil module not available"


class AccountingLogObserver(FileLogObserver):
    
    def __init__(self, f):
        FileLogObserver.__init__(self, f)
    
    def emit(self, eventDict):
        if eventDict.get('type') == 'accounting':
            timeStr = self.formatTime(eventDict['time'])
            avatar = eventDict.get('avatar')
            amount = eventDict.get('amount')
            acc_type = eventDict.get('acc_type')
            msg = "%s %s %s %s\n" %(timeStr, avatar, acc_type, amount)
            util.untilConcludes(self.write, msg)
            util.untilConcludes(self.flush)