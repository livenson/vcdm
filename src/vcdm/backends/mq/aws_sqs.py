from vcdm.interfaces.mq import IMessageQueue
from vcdm.config import get_config

try:
    import boto
    from boto.sqs.message import Message
except ImportError:
    print "AWS mq plugin missing."


class AWSSQSMessageQueue(IMessageQueue):
    
    backend_name = 'sqs'
    conn = None    
    
    def __init__(self):
        self.conn = boto.connect_sqs(get_config().get('aws', 'credentials.username'),
                                     get_config().get('aws', 'credentials.password'))

    def create(self, qnm):
        self.conn.create_queue(qnm)    

    def delete(self, qnm):
        self.conn.delete_queue(qnm)

    def enqueue(self, qnm, value):
        q = self.conn.create_queue(qnm)
        m = Message()
        m.set_body(value)
        q.write(m)

    def get(self, qnm):
        q = self.conn.create_queue(qnm)
        rs = q.get_messages()
        value = ""
        if len(rs) > 0:
            m = rs[0]
            print dir(m)
            value = m.get_body()
        return value

    def delete_message(self, qnm):
        q = self.conn.create_queue(qnm)
        rs = q.get_messages()
        if len(rs) > 0:
            q.delete_message(rs[0])
