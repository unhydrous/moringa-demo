import json

from twisted.trial import unittest
from twisted_web_test_utils import DummySite
from twisted.internet import defer

from config import Config
from webService import ATStagingWebResource
from dlrProcessor import DlrProcessor

class TestSnoopWebService(unittest.TestCase):
    
    def setUp(self):
        self.dlrProcessor = DlrProcessor()
        self.web          = DummySite(ATStagingWebResource(self.dlrProcessor))

    @defer.inlineCallbacks
    def test_heartbeat(self):
        request = yield self.web.post("snoop/heartbeat", 
                                      {"serviceName" : "hydra-api"})
        self.assertEquals(request.responseCode, 200)
        the_page = "".join(request.written)
        self.assertEquals(the_page, json.dumps({"Message": "Success"}))

    @defer.inlineCallbacks
    def test_publishError(self):
        request = yield self.web.post("snoop/publish-error", 
                                      {"serviceName"  : "hydra-api",
                                       "errorCode"    : "failedFuture",
                                       "errorMessage" : "Could not process this future. The error is this other error"})
        self.assertEquals(request.responseCode, 200)
        the_page = "".join(request.written)
        self.assertEquals(the_page, json.dumps({"Message": "Success"}))

