from vcdm.interfaces.mq import IMessageQueue

## TODO: reformat lib into a reasonable one
from lib import winazurestorage

class AzureQueue(IMessageQueue):
    conn = None
    backend_type = 'azure'
    
    def __init__(self):
        self.conn = winazurestorage.QueueStorage() # pass parameters
    
    def create(self, qnm):
        self.conn.create_queue(qnm)
    
    def delete(self, qnm):
        self.conn.delete_queue(qnm)
    
    def enqueue(self, qnm, value):
        self.conn.put_message(qnm, value)   
    
    def get(self, qnm):
        return self.conn.get_message(qnm)
    
    def delete_message(self, qnm):
        # TODO: do it smarter
        self.conn.delete_message(self.conn.get_message(qnm), qnm)