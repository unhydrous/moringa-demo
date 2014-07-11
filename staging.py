from twisted.application import service, internet
from twisted.web.server import Site

from config import Config
from webService import ATStagingWebResource

def makeService():
    parentService = service.MultiService()
    
    # Web Server 
    port = int(Config['webServerPort'])
    root = ATStagingWebResource()
    site = Site(root)
    j    = internet.TCPServer(port, site)
    
    j.setServiceParent(parentService)
    
    return parentService
