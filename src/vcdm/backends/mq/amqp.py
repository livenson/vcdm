from interfaces.mq import IMessageQueue

from amqplib import client_0_8 as amqp

from vcdm import c

class AMQPMQ(IMessageQueue):
    
    conn = None
    backend_type = 'amqp'
        
    def __init__(self, initialize_exchange=False):        
        self.conn = amqp.Connection(host=c('local', 'mq.endpoint'), 
                               userid=c('local', 'mq.username'), 
                               password=c('local', 'mq.password'), 
                               virtual_host="/", insist=False)
        if initialize_exchange:
            chan = self.conn.channel()
            chan.exchange_declare(exchange="vcdm-queues", type="direct", durable=True, auto_delete=False,)
            chan.close()
                    
        
    def create(self, qnm):
        chan = self.conn.channel()
        chan.queue_declare(queue=qnm, durable=True, exclusive=False, auto_delete=False)
        chan.queue_bind(queue=qnm, exchange="vcdm-queues", routing_key=qnm)
        chan.close()
        
    def delete(self, qnm):
        chan = self.conn.channel()
        chan.queue_delete(queue=qnm)
        chan.close()
    
    def enqueue(self, qnm, value):
        chan = self.conn.channel()
        msg = amqp.Message(value)
        msg.properties["delivery_mode"] = 2
        chan.basic_publish(msg, exchange="vcdm-queues", routing_key=qnm)
        chan.close()
        
    def get(self, qnm):
        chan = self.conn.channel()
        # get the last value    
        msg = chan.basic_get(qnm)
        value = ""
        if msg is not None:
            value = msg.body
        chan.close()
        return value
    
    def delete_message(self, qnm):
        chan = self.conn.channel()
        msg = chan.basic_get(qnm)
        if msg is not None:
            chan.basic_ack(msg.delivery_tag) 
        chan.close()
