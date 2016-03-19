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

            username = "APIUsername"
            apikey   = "APIKey"
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
        amount = None
        try:
            phoneNumber = cgi.escape(request.args["phoneNumber"][0])
            text        = cgi.escape(request.args["text"][0])
        except KeyError, e:
            response = "END Invalid request"
        else:
            if text == "":
                response = "CON Welcome to the test.\n1. How much airtime would you like to purchase?"
            else:
                try:
                    amount = int(text)
                    response = "END Thank you. Please pay at the next prompt"
                except ValueError:
                    response = "END Please respond with a number"
                    
            request.setResponseCode(200)
            request.write(response)
            
            if not request.finished:
                request.finish()

            if amount is not None:
                self._promptCheckout(
                    phoneNumber = phoneNumber,
                    amount      = amount
                    )

    def _promptCheckout(self, phoneNumber, amount):
        username   = "APIUsername"
        apikey     = "APIKey"

        gateway    = AfricasTalkingGateway(username, apikey)

        try:
            response = gateway.promptMobilePaymentCheckout(
                productName_  = "Demo",
                phoneNumber_  = phoneNumber,
                currencyCode_ = "KES",
                amount_       = amount,
                metadata_     = {"paymentFor" : "Airtime"}
                )
            print response

        except AfricasTalkingGatewayException, e:
            print 'Encountered an error while making the call: %s' % str(e)

class PaymentRequestWebPage(Resource):
    isLeaf = True

    def render_POST(self, request):
        self._processRequest(request)
        return NOT_DONE_YET        

    def _processRequest(self, request):
        params = json.loads(request.content.read())
        log.msg('PaymentRequest::_processRequest: Received %s' % str(params))        
        status      = params["status"]
        phoneNumber = params["phoneNumber"]
        value       = params["value"]
        
        request.setResponseCode(200)
        request.write("OK")
            
        if not request.finished:
            request.finish()
            
        username   = "APIUsername"
        apikey     = "APIKey"

        recipients = [{"phoneNumber" : phoneNumber, 
                       "amount"      : value}]
        
        gateway    = AfricasTalkingGateway(username, apikey)
        
        try:
            responses = gateway.sendAirtime(recipients)
            for response in responses:
                print "phoneNumber=%s;amount=%s;status=%s;requestId=%s" % (response['phoneNumber'],
                                                                           response['amount'],
                                                                           response['status'],
                                                                           response['requestId'])
                
        except AfricasTalkingGatewayException, e:
            print 'Encountered an error while making the call: %s' % str(e)

                
