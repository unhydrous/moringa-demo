import json, cgi, uuid

from twisted.python import log
from twisted.web.resource import Resource, NoResource
from twisted.internet import defer
from twisted.web.server import NOT_DONE_YET

class HeartbeatRequestWebPage(Resource):
    isLeaf = True
            
    def render_POST(self, request):
        self._processRequest(request)
        return NOT_DONE_YET        

    def _processRequest(self, request):
        paramStr = request.args
        log.msg('HeartbeatRequest::_processRequest: Received %s' % str(paramStr))
        request.setResponseCode(200)
        request.write(json.dumps({"Message": "Success"}))
        if not request.finished:
            request.finish()


class PublishErrorRequestWebPage(Resource):
    isLeaf = True
            
    def render_POST(self, request):
        self._processRequest(request)
        return NOT_DONE_YET        

    def _processRequest(self, request):
        paramStr = request.args
        log.msg('PublishErrorRequest::_processRequest: Received %s' % str(paramStr))
        request.setResponseCode(200)
        request.write(json.dumps({"Message": "Success"}))
        if not request.finished:
            request.finish()

