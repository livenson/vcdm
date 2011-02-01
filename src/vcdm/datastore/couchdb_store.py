import couchdb
from uuid import uuid4

def init():
    server = couchdb.Server('http://localhost:5984/')
    try:
        db = server.create('meta')
        return db
    except:
        db = server['meta']
        # already created? or failed to create for any other reason?
        return db

def getDB():
    server = couchdb.Server('http://localhost:5984/')
    return server['meta']

def read(docid):
    db = getDB()
    return db[docid]

def write(data, docid=None):
    db = getDB()
    if docid is None:
        docid = uuid4().hex
    db[docid] = data
    return docid

def exists(docid):
    db = getDB()
    return (docid in db)

def delete(docid):
    db = getDB()
    del db[docid]

def find_uid_match(dirn):
    db = getDB()
    print 'find_uid_match("', dirn, '")'
    dirn_fun = '''
    function(doc) {
       if (doc.filename.match(/^%s/)) {
           emit(doc.id, { filename: doc.filename, acl: doc.acl });
       }
    }
    ''' % dirn.replace("/", "\\/")
     
    reslist = map(lambda r: (r.value['filename'], 
                             { 'acl':  r.value['acl'] }, 0), 
                  list(db.query(dirn_fun)))
    return reslist

def find_uid(fnm):
    db = getDB()
    fnm_fun = '''function(doc) {
        if (doc.filename == "%s") {
            emit(doc.id, null);            
        }
    } 
    ''' %fnm
    res = db.query(fnm_fun)
    if len(res) == 0:
        return None
    else:
        return list(res)[0].id
    
def get_total_stats():
    db = getDB()
    sizes = '''function(doc) {       
           emit(doc.size, null);
    }
    ''' 
    res = db.query(sizes)
    if len(res) == 0:
        return (None, None)
    else: 
        return (len(res), sum([s['key'] for s in list(res)]))
