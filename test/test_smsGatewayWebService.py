import json

from twisted.trial import unittest
from twisted_web_test_utils import DummySite
from twisted.internet import defer

from config import Config
from webService import ATStagingWebResource

class TestSmsGatewayWebService(unittest.TestCase):
    
    def setUp(self):
        self.web             = DummySite(ATStagingWebResource())

    @defer.inlineCallbacks
    def test_safaricomSmsGateway(self):
        request = yield self.web.post("sms-gateway/safaricom", {})
        self.assertEquals(request.responseCode, 201)
        the_page = "".join(request.written)
        self.assertEquals(the_page, json.dumps({"Message": "Success"}))

    @defer.inlineCallbacks
    def test_kenyaSmsGateway(self):
        request = yield self.web.post("sms-gateway/kenya",
                                      {"transactionId": "TxnId1",
                                       "destination": "+254718008164,+254729891801"})
        self.assertEquals(request.responseCode, 201)
        the_page = "".join(request.written)
        transactionData = {"TransactionData" : {"+254718008164" : "1701",
                                                "+254729891801" : "1701"}}
        self.assertEquals(the_page, json.dumps(transactionData))

    @defer.inlineCallbacks
    def test_routeSmsGateway(self):
        request = yield self.web.post("sms-gateway/route-sms",
                                      {"destination": "+254718008164,+254729891801"})
        self.assertEquals(request.responseCode, 200)
        the_page = "".join(request.written)
        self.assertEquals("1701|254718008164" in the_page, True)
        self.assertEquals("1701|254729891801" in the_page, True)


    @defer.inlineCallbacks
    def test_twilioSmsGateway(self):
        request = yield self.web.post("sms-gateway/twilio")
        self.assertEquals(request.responseCode, 200)
        the_page = "".join(request.written)
        self.assertEquals(the_page, "Some(Twiml)")
        
