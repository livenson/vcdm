from twisted.web import resource

import vcdm

class InfoResource(resource.Resource):
    """
    A root resource which is protected by guard and requires authentication in order to access.
    """
    def getChild(self, type, request):        
        return self

    def render(self, request):
        res = """ 
        <html> 
        <title>VCDM Server Dashboard</title>
        <h3>VCDM Server Dashboard</h3> 
        
        <h4>General data</h4>
        """
                
        res += "<p><b>Cost per month:</b> $3.99 (TODO: frontend to accounting stats)</p>"
        res += "<p><a href=\"http://localhost:5984/_utils/\">Datastore management</a></p>"
        
        res += """<h4>Supported backends (blob)</h4>
        <ul>
        """
        for i in vcdm.blob_backends.keys():
            current = ""
            if i == vcdm.c('general', 'blob.backend'):
                current = "<b>current</b>"
            res += "<li>%s: <a href=\"#\">description</a> | <a href=\"#\">test results</a> %s</li>" %(i, current)
        res += """
        </ul>
        <h4>Supported backends (message queues)</h4>
        <ul>
        """
        for i in vcdm.mq_backends.keys():
            current = ""
            if i == vcdm.c('general', 'mq.backend'):
                current = "<b>current</b>"
            res += "<li>%s: <a href=\"#\">description</a> | <a href=\"#\">test results</a> %s</li>" %(i, current)
        res += """
        </ul>
        <h4>Supported backends (datastore)</h4>
        <ul>
        """
        for i in vcdm.datastore_backends.keys():
            current = ""
            if i == vcdm.config.get('general', 'ds.backend'):
                current = "<b>current</b>"
            res += "<li>%s: <a href=\"#\">description</a> | <a href=\"#\">test results</a> %s</li>" % (i, current)
        res +="</ul>"
        res += """
        
        </html>
        """ 
        return res
