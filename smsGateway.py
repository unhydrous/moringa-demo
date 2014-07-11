import json, cgi, uuid

from twisted.python import log
from twisted.web.resource import Resource, NoResource
from twisted.internet import defer
from twisted.web.server import NOT_DONE_YET

class SafaricomSmsGatewayRequestWebPage(Resource):    
    isLeaf = True
    def render_POST(self, request):
        self._processRequest(request)
        return NOT_DONE_YET        

    def _processRequest(self, request):
        request.setResponseCode(201)
        request.write(json.dumps({"Message": "Success"}))
        if not request.finished:
            request.finish()

class KenyaSmsGatewayRequestWebPage(Resource):
    isLeaf = True
    def render_POST(self, request):
        self._processRequest(request)
        return NOT_DONE_YET        
    
    def _processRequest(self, request):
        try:
            transactionId = cgi.escape(request.args['transactionId'][0])
            destination   = cgi.escape(request.args['destination'][0])             
        except KeyError, e:
            raise Exception("Missing parameter: %s" % e)
        else:
            toArr   = destination.split(',')
            results = {}
            for to in toArr:
                results[to] = "1701"
            response = {"TransactionData": results}
            
            request.setResponseCode(201)
            request.write(json.dumps(response))
            if not request.finished:
                request.finish()

class RouteSmsGatewayRequestWebPage(Resource):
    isLeaf = True
    
    def render_POST(self, request):
        self._processRequest(request)
        return NOT_DONE_YET        
    
    def _processRequest(self, request):
        try:
            destination   = cgi.escape(request.args['destination'][0])             
        except KeyError, e:
            raise Exception("Missing parameter: %s" % e)
        else:
            toArr   = destination.split(',')
            results = []
            for to in toArr:
                if to.startswith('+'):
                    to = to[1:]

                results.append("1701|%s|%s" % (to, uuid.uuid4()))

            response = ",".join(results)

            request.setResponseCode(200)
            request.write(response)
            if not request.finished:
                request.finish()        

class TwilioSmsGatewayRequestWebPage(Resource):
    isLeaf = True
    def render_POST(self, request):
        self._processRequest(request)
        return NOT_DONE_YET        
    
    def _processRequest(self, request):
        request.setResponseCode(200)
        request.write("Some(Twiml)")
        if not request.finished:
            request.finish()
