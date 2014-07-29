from twisted.application import service, internet
from twisted.web.server import Site

from config import Config
from webService import ATStagingWebResource
from dlrProcessor import DlrProcessor

def makeService():
    parentService = service.MultiService()
    
    # Web Server 
    port         = int(Config['webServerPort'])
    dlrProcessor = DlrProcessor()
    root         = ATStagingWebResource(dlrProcessor)
    site         = Site(root)
    j            = internet.TCPServer(port, site)
    
    j.setServiceParent(parentService)
    
    return parentService
