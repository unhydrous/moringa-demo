import json, cgi, uuid, urllib

from twisted.python import log
from twisted.web.resource import Resource, NoResource
from twisted.internet import defer
from twisted.web.server import NOT_DONE_YET

from AfricasTalkingGateway import AfricasTalkingGateway, AfricasTalkingGatewayException

class VoiceRequestWebPage(Resource):
    isLeaf = True

    def __init__(self, callerRegistry):
        self.callerRegistry = callerRegistry

    def render_POST(self, request):
        self._processRequest(request)
        return NOT_DONE_YET

    @defer.inlineCallbacks
    def _processRequest(self, request):
        paramStr = request.args
        log.msg('VoiceRequest::_processRequest: Received %s' % str(paramStr))
        try:
            isActive     = cgi.escape(request.args['isActive'][0])
            callerNumber = cgi.escape(request.args['callerNumber'][0])            
        except KeyError, e:
            log.msg("Missing parameter %s" % str(e))
        else:
            digits = None
            try:
                digits = cgi.escape(request.args['dtmfDigits'][0])
            except KeyError, e:
                pass

            username = "gikandi"
            apikey   = "fef86cc7a64ef2c1e0533eb0ff11da8c1f5d0b33f6c492fb547972ab9ee2d2a3"
            if isActive:
                gateway  = AfricasTalkingGateway(username, apikey)
                try:
                    if digits:
                        response = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><Response><Say>You entered %s. We will let you know shortly if you are a lucky winner</Say></Response>" % digits
                        log.msg("Sending the response: %s" % response)
                        request.setResponseCode(200)
                        request.write(response)
                        if not request.finished:
                            request.finish()

                        if self.callerRegistry.checkAnswer(callerNumber, digits):      
                            yield gateway.sendMessage(to_      = callerNumber,
                                                      message_ = "You are absolutely right! We are sending you a nice reward very soon :)")
                            yield gateway.sendAirtime([
                                    {'phoneNumber': callerNumber,
                                     'amount'     : 'KES 33'},
                                    ])
                        else:
                            yield gateway.sendMessage(to_      = callerNumber,
                                                      message_ = "Ummm....that is not the right answer but thank you for playing")                
                        return
                    else:
                        question = self.callerRegistry.getQuestion(callerNumber)
                        if question:
                            response = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><Response><GetDigits finishOnKey=\"#\"><Say playBeep=\"true\">Hello player. Welcome to Africa's Talking voice services. Enter the answer to the following question, followed by the hash sign. %s</Say></GetDigits></Response>" % question
                        else:
                            response = """<?xml version="1.0" encoding="UTF-8"?><Response><Reject/></Response>"""

                except AfricasTalkingGatewayException, ex:
                    log.msg('Error while talking to the gateway: ' + str(ex))
                    response = """<?xml version="1.0" encoding="UTF-8"?><Response><Reject/></Response>"""
            else:
                response = "OK"
            
            log.msg("Sending the response: %s" % response)
            request.setResponseCode(200)
            request.write(response)                        
            if not request.finished:
                request.finish()

class UssdRequestWebPage(Resource):
    isLeaf = True

    def __init__(self, callerRegistry):
        self.callerRegistry = callerRegistry
        
    def render_POST(self, request):
        self._processRequest(request)
        return NOT_DONE_YET        

    def _processRequest(self, request):
        paramStr = request.args
        log.msg('UssdRequest::_processRequest: Received %s' % str(paramStr))        
        try:
            phoneNumber = cgi.escape(request.args["phoneNumber"][0])    
        except KeyError, e:
            response = "END Invalid request"
        else:
            if self.callerRegistry.addCaller(phoneNumber):
                response = "END Welcome to Africa's Talking USSD Services. We will call you shortly with our question of the day."
            else:
                response = "END Looks like you have already completed today's challenge. Thank you for playing!"
            request.setResponseCode(200)
            request.write(response)
            
            if not request.finished:
                request.finish()
