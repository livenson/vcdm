backend_type = 'amqp'

from amqplib import client_0_8 as amqp

conn = None

def get_connection():
    global conn
    if conn is None:
        conn = amqp.Connection(host="localhost:5672", userid="guest", password="guest", virtual_host="/", insist=False)
        #conn.channel().exchange_declare(exchange="vcdm-queues", type="direct", durable=True, auto_delete=False,)        
    return conn

# TODO: move to a setup script
def init():
    chan = get_connection().channel()
    # create exchange box
    chan.exchange_declare(exchange="vcdm-queues", type="direct", durable=True, auto_delete=False,)
    chan.close()
    
def create(qnm):
    chan = get_connection().channel()
    chan.queue_declare(queue=qnm, durable=True, exclusive=False, auto_delete=False)
    chan.queue_bind(queue=qnm, exchange="vcdm-queues", routing_key=qnm)
    chan.close()
    
def delete(qnm):
    chan = get_connection().channel()
    chan.queue_delete(queue=qnm)
    chan.close()

def enqueue(qnm, value):
    chan = get_connection().channel()
    msg = amqp.Message(value)
    msg.properties["delivery_mode"] = 2
    chan.basic_publish(msg, exchange="vcdm-queues", routing_key=qnm)
    chan.close()
    
def get(qnm):
    chan = get_connection().channel()
    # get the last value    
    msg = chan.basic_get(qnm)
    value = ""
    if msg is not None:
        value = msg.body
    chan.close()
    return value

def delete_message(qnm):
    chan = get_connection().channel()
    msg = chan.basic_get(qnm)
    if msg is not None:
        chan.basic_ack(msg.delivery_tag) 
    chan.close()