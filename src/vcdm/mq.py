import vcdm 

backend=vcdm.mq_backends[vcdm.config.get('general', 'mq.backend')]
ds=vcdm.datastore_backends[vcdm.config.get('general', 'ds.backend')]

def create(qnm):
    backend.create(qnm)

def delete(qnm):
    backend.delete(qnm)

def enqueue(qnm, value):
    backend.enqueue(qnm, value)

def get(qnm):
    return backend.get(qnm)

def delete_message(qnm):
    backend.delete_message(qnm)