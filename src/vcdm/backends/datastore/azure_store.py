from libazure.azure_storage import TableStorage
from vcdm.interfaces.datastore import IDatastore

from vcdm import c

class AzureStore(IDatastore):
    ts = None
    table_name = 'meta'
    
    def init(self, initialize = False):
        self.ts = TableStorage(c('azure', 'credentials.table_url'),
                                 c('azure', 'credentials.account'), 
                                 c('azure', 'credentials.password'))
        if initialize:
            self.ts.create_table(self.table_name)
        