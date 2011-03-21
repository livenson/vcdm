from lib import winazurestorage
from uuid import uuid4
from vcdm.interfaces.datastore import IDatastore



class AzureStore(IDatastore):
    ts = None
    table_name = 'meta'
    
    def init(self):
        if self.ts is None:
            ts = winazurestorage.TableStorage()
        ts.create_table(self.table_name)        
    
    def write(self, data, docid=None):    
        if not docid:
            docid = uuid4().hex
        #TODO: ts.add_entry(docid, table_name, docid)
        return docid
        
