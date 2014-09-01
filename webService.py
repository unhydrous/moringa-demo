from twisted.python import log
from twisted.web.resource import Resource, NoResource

from smsGateway import SafaricomSmsGatewayRequestWebPage, KenyaSmsGatewayRequestWebPage, RouteSmsGatewayRequestWebPage, TwilioSmsGatewayRequestWebPage 

from snoop import HeartbeatRequestWebPage, PublishErrorRequestWebPage

class ATStagingWebResource(Resource):
    
    def __init__(self, dlrProcessor):
        Resource.__init__(self)
        self.dlrProcessor = dlrProcessor
    
    def getChild(self, name, request):
        log.msg("ATStagingWebResource::getChild processing name=%s;uri=%s;clientIP=%s;" % (name, request.uri, request.getClientIP()))
        if name == 'sms-gateway':
            if 'safaricom' in request.uri:
                return SafaricomSmsGatewayRequestWebPage(self.dlrProcessor)
            elif 'kenya' in request.uri:
                return KenyaSmsGatewayRequestWebPage(self.dlrProcessor)
            elif 'route-sms' in request.uri:
                return RouteSmsGatewayRequestWebPage(self.dlrProcessor)
            elif 'twilio' in request.uri:
                return TwilioSmsGatewayRequestWebPage()
            else:
                return NoResource
        
        elif name == 'snoop':
            if 'heartbeat' in request.uri:
                return HeartbeatRequestWebPage()
            elif 'publish-error' in request.uri:
                return PublishErrorRequestWebPage()
            else:
                return NoResource()
        else:
            return NoResource()
