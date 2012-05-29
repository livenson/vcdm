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
import base64

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

    # add Basic HTTP authn headers
    username = conf.get('general', 'ur_username')
    password = conf.get('general', 'ur_password')
    basicAuth = base64.encodestring("%s:%s" % (username, password))
    authHeader = "Basic " + basicAuth.strip()

    d = agent.request(
    'POST',
    conf.get('general', 'ur_server'),
    Headers(
        {
         'Authorization': [authHeader],
         'User-Agent': ['CDMI-Proxy'],
         'Content-Type': ['application/xml']}),
    body)

    def cbResponse(r):
        log.err("Accounting info sent to UR, response: %s %s" % (r.code, r.phrase))
    d.addCallback(cbResponse)

    def cbError(e):
        log.err("Error contacting UR server: %s" % e)
    d.addErrback(cbError)
