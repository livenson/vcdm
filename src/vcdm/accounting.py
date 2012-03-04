from zope.interface import implements

from twisted.python import log
from twisted.internet.defer import succeed
from twisted.web.iweb import IBodyProducer
from twisted.internet import reactor
from twisted.web.client import Agent
from twisted.web.http_headers import Headers

import vcdm

conf = vcdm.config.get_config()


class StringProducer(object):
    implements(IBodyProducer)

    def __init__(self, body):
        self.body = body
        self.length = len(body)

    def startProducing(self, consumer):
        consumer.write(self.body)
        return succeed(None)

    def pauseProducing(self):
        pass

    def stopProducing(self):
        pass


def send_ogf_ur_accounting(start_time, end_time, avatar, total_storage, nr_of_operations):
    agent = Agent(reactor)
    body = StringProducer("""
<usageRecord>
    <resourceType>storage</resourceType>
    <consumerId>%(avatar)s</consumerId>
    <creatorId>%(ur_creator)s</creatorId>
    <resourceOwner>%(resource_owner)s</resourceOwner>

    <startTime>%(start_time)s</startTime>
    <endTime>%(end_time)s</endTime>

    <storageContext>/</storageContext>

    <storageTransactions>%(nr_of_operations)s</storageTransactions>
    <storageVolume>%(total_storage)s</storageVolume>
</usageRecord>""" % {
            'avatar': avatar,
            'ur_creator': conf.get('general', 'ur_creator'),
            'resource_owner': conf.get('general', 'ur_resource_owner'),
            'start_time': start_time,
            'end_time': end_time,
            'nr_of_operations': nr_of_operations,
            'total_storage': total_storage
    })
    d = agent.request(
    'POST',
    conf.get('general', 'ur_server'),
    Headers(
        {
         'User-Agent': ['CDMI-Proxy'],
         'Content-Type': ['text/plain']}),
    body)

    def cbResponse(r):
        log.err("Successfully updated UR with accounting info")
    d.addCallback(cbResponse)

    def cbError(e):
        log.err("Error contacting UR server: %s" % e)
    d.addErrback(cbError)
