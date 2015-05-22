from twisted.application import service, internet
from twisted.web.server import Site

from config import Config
from webService import ATDemoWebResource

from callers import CallerRegistry

def makeService():
    parentService = service.MultiService()
    
    # Web Server 
    port           = int(Config['webServerPort'])
    callerRegistry = CallerRegistry()
    root           = ATDemoWebResource(callerRegistry)
    site           = Site(root)
    j              = internet.TCPServer(port, site)
    
    j.setServiceParent(parentService)
    
    return parentService
