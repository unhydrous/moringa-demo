import random
from datetime import datetime
from twisted.python import log
from twisted.internet import reactor, defer
from twisted.internet.error import AlreadyCancelled

from AfricasTalkingGateway import AfricasTalkingGateway, AfricasTalkingGatewayException

class CallerRegistry:

    def __init__(self):
        self.callers    = []
	self.answers    = {
            'How many software developers does Africas Talking have?' : '6',
            'How many employees does Africas Talking have?' : '17',
            'How many servers has Africas Talking deployed in their cloud?' : '41',
            'How many MIT graduates work at Africas Talking?': '3',
            'How old is Africas Talking in years?' : '5',
            'On what floor is our new office?' : '7',
            }
        self.asked      = {}
        self.makeCallId = reactor.callLater(5, self._makeCall)
        
    def addCaller(self, phoneNumber):
	if phoneNumber in self.asked:
            log.msg('We have already asked the user %s' % phoneNumber)
            return False
        else:
            self.callers.append(phoneNumber)
            question = random.choice(self.answers.keys())
            log.msg('Will ask %s the question %s' % (phoneNumber, question))
            self.asked[phoneNumber] = question
            return True
            
    def checkAnswer(self, phoneNumber, answer):
        log.msg("_checkAnswer phoneNumber=%s;answer=%s" % (phoneNumber, answer))
        question = self.asked[phoneNumber]
        expected = self.answers[question]
        if answer == expected:
            return True
        else:
            del self.asked[phoneNumber]
            return False
    
    def getQuestion(self, phoneNumber):
        if phoneNumber in self.asked:
            return self.asked[phoneNumber]

    def _makeCall(self):
	if self.callers:
            phoneNumbers = self.callers[:10]
            self.callers = self.callers[10:]
            self._makeCallImpl(','.join(phoneNumbers))
	self.makeCallId = reactor.callLater(30, self._makeCall)

    @defer.inlineCallbacks
    def _makeCallImpl(self, phoneNumbers):
        username = "APIUsername";
        apikey   = "APIKey";
        callFrom = "+254711082903";
        
        # Create a new instance of our awesome gateway class
        gateway  = AfricasTalkingGateway(username, apikey)
        try:
            yield gateway.call(callFrom, phoneNumbers)
            log.msg("Calls have been initiated. Time for song and dance!\n")
            
        except AfricasTalkingGatewayException, e:
            log.msg('Encountered an error while making the call: %s' % str(e))
