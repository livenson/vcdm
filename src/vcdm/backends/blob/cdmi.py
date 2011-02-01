# TODO
backend_type = 'cdmi'

from twisted.internet.defer import Deferred
from twisted.internet.protocol import Protocol
from pprint import pformat

import vcdm

from vcdm.client import cdmi_request 

def read(fnm, rng=None):
    username = vcdm.config.get('cdmi', 'credentials.username') 
    password = vcdm.config.get('cdmi', 'credentials.password')
    hostname = vcdm.config.get('cdmi', 'cdmi.blob_url')
    return cdmi_request.request(cbRequest, 'GET', '%s/%s' % (hostname, fnm), username, password)

def write(fnm, content):
    username = vcdm.config.get('cdmi', 'credentials.username') 
    password = vcdm.config.get('cdmi', 'credentials.password')
    hostname = vcdm.config.get('cdmi', 'cdmi.blob_url')
    return cdmi_request.request('PUT', '%s/%s' % (hostname, fnm), username, password, content)

def delete(fnm):
    username = vcdm.config.get('cdmi', 'credentials.username') 
    password = vcdm.config.get('cdmi', 'credentials.password')
    hostname = vcdm.config.get('cdmi', 'cdmi.blob_url')
    return cdmi_request.request('DELETE', '%s/%s' % (hostname, fnm), username, password)

def cbRequest(response):
    print 'Response version:', response.version
    print 'Response code:', response.code
    print 'Response phrase:', response.phrase
    print 'Response headers:'
    print pformat(list(response.headers.getAllRawHeaders()))
    finished = Deferred()
    response.deliverBody(BeginningPrinter(finished))
    return finished

class BeginningPrinter(Protocol):
    def __init__(self, finished):
        self.finished = finished
        self.remaining = 1024 * 10

    def dataReceived(self, bytes):        
        if self.remaining:
            display = bytes[:self.remaining]
            print 'Some data received:'
            print display
            self.remaining -= len(display)

    def connectionLost(self, reason):
        print 'Finished receiving body:', reason.getErrorMessage()
        self.finished.callback(None)
