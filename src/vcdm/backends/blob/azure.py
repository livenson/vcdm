backend_type = 'azure'

from lib import winazurestorage
import urllib2

conn = None

def getConnection():
    global conn
    if conn is None:
        conn = winazurestorage.BlobStorage()
        conn.create_container('vcdm')
    return conn

def read(fnm, rng=None):
    return getConnection().get_blob(u'vcdm', unicode(fnm))

def write(fnm, content):
    getConnection().put_blob(u'vcdm', unicode(fnm), content, 'text/plain')

def delete(fnm):
    try:
        getConnection().delete_blob(u'vcdm', unicode(fnm))
    except urllib2.HTTPError:
        # TODO: winazure lib seems to be passing also positive responses via exceptions. Need to clarify
        import sys
        print "====================="
        print sys.exc_info()
        print "====================="