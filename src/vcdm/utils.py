""" Set of common utilities """
import sys
import os

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

