backend_type = 'azure'

from lib import winazurestorage

conn = None

def getConnection():
    if conn is None:
        conn = winazurestorage.QueueStorage()

def create(qnm):
    conn.create_queue(qnm)

def delete(qnm):
    conn.delete_queue(qnm)

def enqueue(qnm, value):
    conn.put_message(qnm, value)   

def get(qnm):
    return conn.get_message(qnm)

def delete_message(qnm):
    # TODO: do it smarter
    conn.delete_message(conn.get_message(qnm), qnm)