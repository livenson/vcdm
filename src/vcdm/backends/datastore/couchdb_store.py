import couchdb
from uuid import uuid4
from vcdm.interfaces.datastore import IDatastore

from vcdm import c
from vcdm.errors import InternalError

class CouchDBStore(IDatastore):

    db = None
    
    def __init__(self):
        server = couchdb.Server(c('local', 'datastore.endpoint'))
        try:
            self.db = server.create('meta')
        except:
            # already created?
            self.db = server['meta']          
    
    def read(self, docid):        
        return self.db[docid]
    
    def write(self, data, docid = None):
        doc = None
        if docid is None:
            docid = uuid4().hex
        else:
            doc = self.db[docid]
        data['_id'] = docid 
        #XXX: it seems there's a bug in python couchdb. For same odd case it 
        # raises Conflict if rev is not defined for an existing document.
        # For now: load the whole document and take its revision (should be the last one)
        if doc is not None:
            data['_rev'] = doc.rev
        self.db.save(data)
        return docid
    
    def exists(self, docid):
        return (docid in self.db)
    
    def delete(self, docid):
        del self.db[docid]
    
    def find_uid_match(self, dirn):
        dirn_fun = '''
        function(doc) {
           if (doc.filename.match(/^%s/)) {
               emit(doc.id, { filename: doc.filename, acl: doc.acl });
           }
        }
        ''' % dirn.replace("/", "\\/")
         
        reslist = map(lambda r: (r.value['filename'], 
                                 { 'acl':  r.value['acl'] }, 0), 
                      list(self.db.query(dirn_fun)))
        return reslist
    
    def find_uid(self, fnm, fields = None):
        
        fields = 'null'
        if fields is not None:
            fields = '[' + ','.join(['doc.' + f for f in fields]) + ']'
                    
        fnm_fun = '''function(doc) {
            if (doc.fullpath == "%s") {
                emit(doc.id, %s);            
            }
        } 
        ''' % (fnm, fields)
        res = self.db.query(fnm_fun)
        if len(res) == 0:
            return None
        elif len(res) > 1:
            raise InternalError("Namespace collision: more than one UID corresponds to a filename.")
        else:
            # XXX: change into an elegant retrieval
            tmp_res = list(res)[0]
            return  (tmp_res.key, tmp_res.value)
        
    def get_total_stats(self):
        sizes = '''function(doc) {       
               emit(doc.size, null);
        }
        ''' 
        res = self.db.query(sizes)
        if len(res) == 0:
            return (None, None)
        else: 
            return (len(res), sum([s['key'] for s in list(res)]))
        
    def find_path_uids(self, paths):
        """Return a list of IDs of container objects that correspond to the specified path."""
        comparision_string = ['doc.fullpath == "' + p + '"' for p in paths]
        fnm_fun = '''function(doc) {
            if (doc.object == 'container' && (%s)) {
                emit(doc.id, null);            
            }
        } 
        ''' % ' || '.join(comparision_string)
        res = self.db.query(fnm_fun)
        if len(res) == 0:
            return None        
        else:
            return list(res)
