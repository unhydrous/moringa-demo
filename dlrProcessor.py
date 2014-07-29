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
        self.queue   = defer.DeferredQueue()
	self.workers = [self.worker() for _ in range(10)]
	
	self.safaricomDlrUrl = Config['safaricomDlrUrl']
	self.kenyaDlrUrl     = Config['kenyaDlrUrl']	
	self.routeSmsDlrUrl  = Config['routeSmsDlrUrl']

    def addSafaricomEntry(self, phoneNumber, transactionId):
	self.queue.put(DlrEntry('safaricom', '%s:%s' % (phoneNumber, transactionId)))

    def addKenyaEntry(self, phoneNumber, transactionId):
	self.queue.put(DlrEntry('kenya', '%s:%s' % (phoneNumber, transactionId)))

    def addRouteSmsEntry(self, messageId):
	self.queue.put(DlrEntry('routeSms', messageId))
	
    @defer.inlineCallbacks
    def worker(self):
        while 1:
            entry = yield self.queue.get()
            try:
                yield self._sendReport(entry)
            except Exception, e:
                log.msg("ERROR_ALERT while sending report: %s" % str(e))

    @defer.inlineCallbacks
    def _sendReport(self, entry):
	if entry.gateway == 'safaricom':
	    phoneNumber, messageId = entry.token.split(':')
	    data = {'messageId'   : messageId,
		    'phoneNumber' : phoneNumber,
		    'status'      : 1}
	    response = yield self._sendToApi(self.safaricomDlrUrl, data)
	    log.msg("Send to safaricom has received response " + response)

	elif entry.gateway == 'kenya':
	    phoneNumber, messageId = entry.token.split(':')

	    data = {'messageId'   : messageId,
		    'phoneNumber' : phoneNumber,
		    'status'      : 1}
            response = yield self._sendToApi(self.kenyaDlrUrl, data)
	    log.msg("Send so kenya has received response " + response)

	elif entry.gateway == 'routeSms':
	    data = {'messageId' : entry.token,
		    'status'    : 'DELIVRD'}
            response = yield self._sendToApi(self.routeSmsDlrUrl, data)
	    log.msg("Send to routeSms has received response " + response)

        else:
            log.msg("ERROR_ALERT Unknown gateway: " + entry.gateway)

    @defer.inlineCallbacks
    def _sendToApi(self, url, data):
        data = urllib.urlencode(data)
        try:
            response = yield client.getPage(url, method="POST", postdata=data, headers={'Content-Type':'application/x-www-form-urlencoded'})
        except Exception, e:
            # TODO: testcase for this
            log.msg("ERROR_ALERT URL call has failed with error %s" % str(e))
            response = 'URL Call Failed with error %s' % str(e)
            defer.returnValue(response)
        else:
            defer.returnValue(response.strip())
