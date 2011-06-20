from twisted.web import resource

import vcdm

class InfoResource(resource.Resource):
    def getChild(self, type, request):        
        return self

    def render(self, request):
        size = vcdm.env['ds'].get_total_blob_size()
        # add predictive storage cost per month
        # requires presence of cloud-calculator module
        # TODO: load correct provider pricelist
        s3_storage_cost = 0
        try:
            from sitio.analyser import aws
            _, s3_storage_cost = aws.get_storage_costs([999999*size / 1024 / 1024 / 1024])          
        except ImportError:            
            print "Cloud-calculator module not available"
            pass
        
        res = """ 
        <html> 
        <title>CDMI-Proxy Dashboard</title>         
            
            <div style="height: 90px;"></div>
            
            <div style="text-align: center; font-size:20pt;">
                Cost per month
            </div>
            <div style="text-align: center; font-size:50pt; color:green">
                $%s
            </div>                
            <div style="height: 90px;"></div>
            <p>
            <hr />
            <a href=\"http://localhost:5984/_utils/\">Datastore management</a></p>
            <hr />
            <div style="text-align: center; font-size:20pt;">
                VENUS-C DEMO CONTAINER
            </div>
            
            <div style="text-align: center; font-size:15pt;">
        """ % s3_storage_cost
        _, top_folder = vcdm.env['ds'].find_by_path("/venus-c-demo", 
                                            object_type = 'container', fields=['children'])        
        if top_folder is not None:
            for name in top_folder['children'].values():
                res += "<br /><a href=\"http://localhost:2364/venus-c-demo/%s\">%s</a>"%(str(name),str(name))
        
        res += """
            </div>
        </html>
        """ 
        return res
