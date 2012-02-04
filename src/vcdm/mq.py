import vcdm

backend = vcdm.env['mq']
ds = vcdm.env['ds']


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
