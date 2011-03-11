from lib import winazurestorage
from uuid import uuid4

ts = None
table_name = 'meta'


def init():
    if ts is None:
        ts = winazurestorage.TableStorage()
    ts.create_table(table_name)        

def read(docid):
    pass

def write(data, docid=None):    
    if not docid:
        docid = uuid4().hex
    #TODO: ts.add_entry(docid, table_name, docid)
    return docid

def exists(docid):
    pass

def delete(docid):
    pass
    
def find_uid(fnm):
    pass
