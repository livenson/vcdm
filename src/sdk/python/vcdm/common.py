import urllib2

# MIME content types
CDMI_CONTAINER = 'application/vnd.org.snia.cdmi.container+json'
CDMI_CAPABILITIES = 'application/vnd.org.snia.cdmi.capabilities+json'
CDMI_OBJECT = 'application/vnd.org.snia.cdmi.object+json'
CDMI_DATA = 'application/vnd.org.snia.cdmi.dataobject+json'

class CDMIRequestWithMethod(urllib2.Request):
    """Workaround for using custom command with urllib2.
    
    Inspired by: http://abhinandh.com/post/2383952338/making-a-http-delete-request-with-urllib2
    """
    def __init__(self, url, method, data=None, headers={},\
        origin_req_host=None, unverifiable=False):
        self._method = method
        
        # add custom always-on CDMI headers
        headers['User-agent'] = 'libcdmi-python/0.1'
        headers['X-CDMI-Specification-Version'] = '1.0'
        
        urllib2.Request.__init__(self, url, data, headers,\
                 origin_req_host, unverifiable)

    def get_method(self):
        if self._method:
            return self._method
        else:
            return urllib2.Request.get_method(self)
    