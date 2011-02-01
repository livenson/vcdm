backend_type = 'sqs'

import boto
from boto.sqs.message import Message

import vcdm

c = boto.connect_sqs(vcdm.config.get('aws', 'credentials.username'), vcdm.config.get('aws', 'credentials.password'))

def create(qnm):
    c.create_queue(qnm)    

def delete(qnm):
    c.delete_queue(qnm)

def enqueue(qnm, value):
    q = c.create_queue(qnm)
    m = Message()
    m.set_body(value)
    q.write(m)

def get(qnm):
    q = c.create_queue(qnm)
    rs = q.get_messages()
    value = ""
    if len(rs) > 0:
        m = rs[0]
        print dir(m)
        value = m.get_body()
    return value

def delete_message(qnm):
    q = c.create_queue(qnm)
    rs = q.get_messages()
    if len(rs) > 0:
        q.delete_message(rs[0])