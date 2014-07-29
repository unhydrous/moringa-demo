import urllib

from twisted.internet import defer
from twisted.web import client
from twisted.python import log

from config import Config

class DlrEntry:
    def __init__(self, gateway, token):
	self.gateway = gateway
	self.token   = token

class DlrProcessor:

    def __init__(self):
        log.msg("DlrProcessor is starting...")
	self.queue   = defer.DeferredQueue()
	self.workers = [self.worker() for _ in range(10)]
	
	self.safaricomDlrUrl = Config['safaricomDlrUrl']
	self.kenyaDlrUrl     = Config['kenyaDlrUrl']	
	self.routeSmsDlrUrl  = Config['routeSmsDlrUrl']

    def addSafaricomEntry(self, phoneNumber, transactionId):
	log.msg("Adding safaricom entry with phoneNumber %s and transactionId %s" % (phoneNumber, transactionId))
        self.queue.put(DlrEntry('safaricom', '%s:%s' % (phoneNumber, transactionId)))

    def addKenyaEntry(self, phoneNumber, transactionId):
	self.queue.put(DlrEntry('kenya', '%s:%s' % (phoneNumber, transactionId)))

    def addRouteSmsEntry(self, messageId):
	self.queue.put(DlrEntry('routeSms', messageId))
	
    @defer.inlineCallbacks
    def worker(self):
        log.msg("SNG: Queue::worker has been called")
	while 1:
            log.msg("SNG: Queue is running. The length is %s" % self.queue.size)
	    entry = yield self.queue.get()
            try:
                yield self._sendReport(entry)
            except Exception, e:
                log.msg("SNG: There was an error and it is %s" % str(e))
            else:
                log.msg("Great success")

    @defer.inlineCallbacks
    def _sendReport(self, entry):
	log.msg("SNG: We are sending the entry with gateway %s and token %s" % (entry.gateway, entry.token))
        if entry.gateway == 'safaricom':
	    phoneNumber, messageId = entry.token.split(':')
	    data = {'messageId'   : messageId,
		    'phoneNumber' : phoneNumber,
		    'status'      : 1}
	    log.msg("OK, this is safaricom. Lets send it")
            response = yield self._sendToApi(self.safaricomDlrUrl, data)
	    log.msg("Send to safaricom has received response " + response)

	elif entry.gateway == 'kenya':
	    phoneNumber, messageId = entry.token.split(':')

	    data = {'messageId'   : messageId,
		    'phoneNumber' : phoneNumber,
		    'status'      : 1}
            log.msg("OK, this is kenya. Lets send it")
	    response = yield self._sendToApi(self.kenyaDlrUrl, data)
	    log.msg("Send so kenya has received response " + response)

	elif entry.gateway == 'routeSms':
	    data = {'messageId' : entry.token,
		    'status'    : 'DELIVRD'}
            log.msg("OK, this is routeSms. Lets send it")
	    response = yield self._sendToApi(self.routeSmsDlrUrl, data)
	    log.msg("Send to routeSms has received response " + response)

        else:
            log.msg("This is an unknown gateway: " + entry.gateway)

    @defer.inlineCallbacks
    def _sendToApi(self, url, data):
        log.msg("Send to api called with url=%s" % url)
        data = urllib.urlencode(data)
        try:
            response = yield client.getPage(url, method="POST", postdata=data, headers={'Content-Type':'application/x-www-form-urlencoded'})
        except Exception, e:
            # TODO: testcase for this
            log.msg("URL call has failed with error %s" % str(e))
            response = 'URL Call Failed with error %s' % str(e)
            defer.returnValue(response)
        else:
            log.msg("URL call has succeeded with  %s" % response.strip())
            defer.returnValue(response.strip())
