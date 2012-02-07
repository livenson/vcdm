import cgi

try:
    import json
except ImportError:
    import simplejson as json

from vcdm import mq
from vcdm.server.cdmi.generic import set_common_headers, parse_path,\
    get_common_body
from vcdm.server.cdmi.cdmi_content_types import CDMI_QUEUE
from vcdm.server.cdmi.cdmiresource import StorageResource


class Queue(StorageResource):
    allowedMethods = ('PUT', 'GET', 'DELETE', 'POST')
    isLeaf = True

    def render_GET(self, request):
        # parse the request
        _, __, fullpath = parse_path(request.path)

        status, value, uid, metadata, mimetype = mq.get(fullpath)
        # construct response
        request.setResponseCode(status)
        request.setHeader('Content-Type', CDMI_QUEUE)
        set_common_headers(request)

        # construct body
        response_body = {
                         'completionStatus': 'Complete',
                         'mimetype': mimetype,
                         'metadata': metadata,
                         'value': value,
                         'queueValues': None,
                         'capabilitiesURI': '/cdmi_capabilities/queue'
                         }
        response_body.update(get_common_body(request, uid, fullpath))
        return json.dumps(response_body)

    def render_PUT(self, request):
        qnm = request.postpath[0]
        mq.create(qnm)
        return "create new queue/update queue %s" % qnm

    def render_DELETE(self, request):
        qnm = request.postpath[0]
        # TODO: twisted problem - valueless parameters are not transcoded to
        # request.args. Currently use a workaround
        if 'value' in request.uri[-6:]:
            # it's a value delete request
            mq.delete_message(qnm)
            return "deleted last message from queue %s" % qnm
        else:
            # delete the queue
            mq.delete(qnm)
            return "delete queue %s" % qnm

    def render_POST(self, request):
        qnm = request.postpath[0]
        val = cgi.escape(request.args["value"][0])
        mq.enqueue(qnm, val)
        return "enqueued into %s value %s " % (qnm, val)
