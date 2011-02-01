from twisted.web import resource

import cgi

from vcdm import mq

class Queue(resource.Resource):
    allowedMethods = ('PUT','GET','DELETE', 'POST') # commands we support for the data items
    isLeaf = True # queues cannot be nested
    
    def render_GET(self, request):
        qnm = request.postpath[0]
        val = mq.get(qnm)
        return "queue %s - last value: %s" %(qnm, val)
        
    def render_PUT(self, request):
        qnm = request.postpath[0]
        mq.create(qnm)
        return "create new queue/update queue %s" %qnm
    
    def render_DELETE(self, request):
        qnm = request.postpath[0]
        # TODO: twisted problem - valueless parameters are not transcoded to request.args. Currently use a workaround 
        if 'value' in request.uri[-6:]:
            # it's a value delete request
            mq.delete_message(qnm)
            return "deleted last message from queue %s" %qnm
        else:
            # delete the queue
            mq.delete(qnm)
            return "delete queue %s" %qnm
    
    def render_POST(self, request):
        qnm = request.postpath[0]
        val = cgi.escape(request.args["value"][0])
        mq.enqueue(qnm, val)
        return "enqueued into %s value %s " % (qnm, val)