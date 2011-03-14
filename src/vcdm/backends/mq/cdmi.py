from vcdm.interfaces.mq import IMessageQueue

class CDMIQueue(IMessageQueue):
    backend_type = 'cdmi'
    ## TODO