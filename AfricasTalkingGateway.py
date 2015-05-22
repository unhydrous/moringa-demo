import urllib
import urllib2
import json

from twisted.internet import defer
from twisted.python import log

import utils

class AfricasTalkingGatewayException(Exception):
    pass

class AfricasTalkingGateway:
    
    def __init__(self, username_, apiKey_):
	self.username = username_
	self.apiKey   = apiKey_
	
        self.SmsUrlString          = "https://api.africastalking.com/version1/messaging"
        self.SubscriptionUrlString = "https://api.africastalking.com/version1/subscription"
	self.VoiceUrlString        = "https://voice.africastalking.com/call"
        self.SendAirtimeUrlString  = "https://api.africastalking.com/version1/airtime/send"    

    @defer.inlineCallbacks
    def sendMessage(self, to_, message_, from_ = None, bulkSMSMode_ = 1, enqueue_ = 0, keyword_ = None, linkId_ = None, retryDurationInHours_ = None):
	
        if len(to_) == 0 or len(message_) == 0:
            raise AfricasTalkingGatewayException("Please provide both to_ and message_ parameters")

	values = {'username' : self.username,
		  'to'       : to_,
		  'message'  : message_ }

	if not from_ is None :
	    values["from"]        = from_
	    values["bulkSMSMode"] = bulkSMSMode_

        if enqueue_ > 0:
            values["enqueue"] = enqueue_
        
        if not keyword_ is None:
            values["keyword"] = keyword_
        
        if not linkId_ is None:
            values["linkId"] = linkId_
            
        if not retryDurationInHours_ is None:
            values["retryDurationInHours"] =  retryDurationInHours_

        headers = {
            'Content-Type' : 'application/x-www-form-urlencoded',
            'Accept'       : 'application/json',
            'apikey'       : self.apiKey
            }
	
	try:
            data     = urllib.urlencode(values)
            the_page = yield utils.fetchPostUrlContent(self.SmsUrlString,
                                                       data,
                                                       headers)
            print "Response is " + the_page
            
        except urllib2.HTTPError as e:
            the_page = e.read()
            raise AfricasTalkingGatewayException(the_page)

        else:
            decoded  = json.loads(the_page)
            recipients = decoded['SMSMessageData']['Recipients']
            defer.returnValue(recipients)
    
    def fetchMessages(self, lastReceivedId_):
	
	url     = "%s?username=%s&lastReceivedId=%s" % (self.SmsUrlString, self.username, lastReceivedId_)
	headers = {'Accept' : 'application/json',
		   'apikey' : self.apiKey }
	
        try:
            request  = urllib2.Request(url, headers=headers)
            response = urllib2.urlopen(request)
            the_page = response.read()
        
        except urllib2.HTTPError as e:
            
            the_page = e.read()
            raise AfricasTalkingGatewayException(the_page)
        
        else:
            
            decoded  = json.loads(the_page)
            messages = decoded['SMSMessageData']['Messages']
        
            return messages
        
    @defer.inlineCallbacks
    def call(self, from_, to_):
        log.msg("call from=%s;to=%s;" % (from_, to_))
	values = {'username' : self.username,
		  'from'     : from_,
                  'to'       : to_ }
        
	headers = {
            'Content-Type' : 'application/x-www-form-urlencoded',
            'Accept'       : 'application/json',
            'apikey'       : self.apiKey }
        
        try:
            data     = urllib.urlencode(values)
            log.msg("The data at this point is %s" % str(data))
            response = yield utils.fetchPostUrlContent(self.VoiceUrlString,
                                                       data,
                                                       headers)        
        except urllib2.HTTPError as e:
            the_page = e.read()
            raise AfricasTalkingGatewayException(the_page)
        except Exception, ex:
            log.msg("Caught exception: %s" % str(ex))
            raise AfricasTalkingGatewayException(str(ex))

    @defer.inlineCallbacks
    def sendAirtime(self, recipients_):
        values = {'username'   : self.username,
		  'recipients' : json.dumps(recipients_) }
        
	headers = {
            'Content-Type' : 'application/x-www-form-urlencoded',
            'Accept'       : 'application/json',
            'apikey'       : self.apiKey
            }
        
        try:
            data     = urllib.urlencode(values)
            response = yield utils.fetchPostUrlContent(self.SendAirtimeUrlString,
                                                       data,
                                                       headers)
        except urllib2.HTTPError as e:
            the_page = e.read()
            raise AfricasTalkingGatewayException(the_page)
        
        else:
            decoded   = json.loads(response)
            responses = decoded['responses']
            if len(responses) > 0:
                defer.returnValue(responses)
            else:
                raise AfricasTalkingGatewayException(decoded['errorMessage'])
            
    def uploadMediaFile(self, url_):
	values = {'username' : self.username,
		  'url'      : url_}
        
	headers = {'Accept' : 'application/json',
                   'apikey' : self.apiKey }
        
        try:
            url      = "https://voice.africastalking.com/mediaUpload"
            data     = urllib.urlencode(values)
            request  = urllib2.Request(url, data, headers=headers)
            response = urllib2.urlopen(request)
        
        except urllib2.HTTPError as e:
            
            the_page = e.read()
            raise AfricasTalkingGatewayException(the_page)

    def getNumQueuedCalls(self, phoneNumber_, queueName_=None):
	values = {'username'    : self.username,
		  'phoneNumber' : phoneNumber_}
        
        if queueName_ is not None:
            values['queueName'] = queueName_

	headers = {
            'Accept'      : 'application/json',
            'apikey' : self.apiKey
            }
        
        try:
            url      = "https://voice.africastalking.com/queueStatus"
            data     = urllib.urlencode(values)
            request  = urllib2.Request(url, data, headers=headers)
            response = urllib2.urlopen(request)
            decoded  = json.loads(response.read())
            return decoded['NumQueued']

        except urllib2.HTTPError as e:
            
            the_page = e.read()
            raise AfricasTalkingGatewayException(the_page)
    
