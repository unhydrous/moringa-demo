from twisted.python import log
from twisted.web.resource import Resource, NoResource

from endpoints import UssdRequestWebPage, VoiceRequestWebPage, PaymentRequestWebPage

class ATDemoWebResource(Resource):
    
    def __init__(self, callerRegistry):
        Resource.__init__(self)
        self.callerRegistry = callerRegistry
    
    def getChild(self, name, request):
        log.msg("ATDemoWebResource::getChild processing name=%s;uri=%s;clientIP=%s;" % (name, request.uri, request.getClientIP()))
        if name == 'test':
            if 'voice' in request.uri:
                return VoiceRequestWebPage(self.callerRegistry)
            elif 'ussd' in request.uri:
                return UssdRequestWebPage(self.callerRegistry)
            elif 'payment' in request.uri:
                return PaymentRequestWebPage()
            else:
                return NoResource()
        else:
            return NoResource()
