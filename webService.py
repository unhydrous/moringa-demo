from twisted.python import log
from twisted.web.resource import Resource, NoResource

from smsGateway import SafaricomSmsGatewayRequestWebPage, KenyaSmsGatewayRequestWebPage, RouteSmsGatewayRequestWebPage, TwilioSmsGatewayRequestWebPage 

class ATStagingWebResource(Resource):
    
    def getChild(self, name, request):
        log.msg("ATUssdWebResource::getChild processing name=%s;uri=%s;clientIP=%s;" % (name, request.uri, request.getClientIP()))
        if name == 'sms-gateway':
            if 'safaricom' in request.uri:
                return SafaricomSmsGatewayRequestWebPage()
            elif 'kenya' in request.uri:
                return KenyaSmsGatewayRequestWebPage()
            elif 'route-sms' in request.uri:
                return RouteSmsGatewayRequestWebPage()
            elif 'twilio' in request.uri:
                return TwilioSmsGatewayRequestWebPage()
            else:
                return NoResource

        else:
            return NoResource()
