import json

from twisted.trial import unittest
from twisted_web_test_utils import DummySite
from twisted.internet import defer

from config import Config
from webService import ATStagingWebResource
from dlrProcessor import DlrProcessor

class TestSmsGatewayWebService(unittest.TestCase):
    
    def setUp(self):
        self.dlrProcessor = DlrProcessor()
        self.web          = DummySite(ATStagingWebResource(self.dlrProcessor))

    @defer.inlineCallbacks
    def test_safaricomSmsGateway(self):
        request = yield self.web.post("sms-gateway/safaricom", 
                                      {"transactionId" : "TxnId1",
                                       "to"            : "+254718008164,+254729891801"})
        self.assertEquals(request.responseCode, 201)
        the_page = "".join(request.written)
        self.assertEquals(the_page, json.dumps({"Message": "Success"}))

    @defer.inlineCallbacks
    def test_kenyaSmsGateway(self):
        request = yield self.web.post("sms-gateway/kenya",
                                      {"transactionId": "TxnId1",
                                       "destination": "+254738008164,+254739891801"})
        self.assertEquals(request.responseCode, 201)
        the_page = "".join(request.written)
        transactionData = {"TransactionData" : {"+254738008164" : "1701",
                                                "+254739891801" : "1701"}}
        self.assertEquals(the_page, json.dumps(transactionData))

    @defer.inlineCallbacks
    def test_routeSmsGateway(self):
        request = yield self.web.post("sms-gateway/route-sms",
                                      {"destination": "+255718008164,+255729891801"})
        self.assertEquals(request.responseCode, 200)
        the_page = "".join(request.written)
        self.assertEquals("1701|255718008164" in the_page, True)
        self.assertEquals("1701|255729891801" in the_page, True)


    @defer.inlineCallbacks
    def test_twilioSmsGateway(self):
        request = yield self.web.post("sms-gateway/twilio")
        self.assertEquals(request.responseCode, 200)
        the_page = "".join(request.written)
        self.assertEquals(the_page, "Some(Twiml)")

    @defer.inlineCallbacks
    def test_voiceRequest(self):
        request = yield self.web.post("test/voice")
        self.assertEquals(request.responseCode, 200)
        the_page = "".join(request.written)
        self.assertEquals(the_page, """<?xml version="1.0" encoding="UTF-8"?><Response><Dial phoneNumbers="+254718008164"/></Response>""")

