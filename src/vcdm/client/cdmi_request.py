from twisted.internet import reactor
from twisted.web.client import Agent
from twisted.web.http_headers import Headers 

from twisted.python import log

def cbShutdown(ignored):
    pass

def request(callback, method, uri, username, password, data = None):
    agent = Agent(reactor)
    d = agent.request(
                      method,
                      uri,
                      Headers({'User-Agent': ['Twisted Web Client Example']}),
                      None)    
    d.addCallback(callback)
    d.addBoth(cbShutdown)
    d.addErrback(log.err)

