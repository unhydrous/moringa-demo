import urllib
import urllib2
import json

class AfricasTalkingGatewayException(Exception):
    pass

class AfricasTalkingGateway:
    
    def __init__(self, username_, apiKey_):
	self.username = username_
	self.apiKey   = apiKey_
	
        self.SmsUrlString                   = "https://api.africastalking.com/version1/messaging"
        self.SubscriptionUrlString          = "https://api.africastalking.com/version1/subscription"
	self.VoiceUrlString                 = "https://voice.africastalking.com/call"
        self.SendAirtimeUrlString           = "https://api.africastalking.com/version1/airtime/send"    
        self.MobilePaymentCheckoutUrlString = "https://api.africastalking.com/payment/mobile/checkout/v1"

    def sendMessage(self, to_, message_, from_ = None, bulkSMSMode_ = 1, enqueue_ = 0, keyword_ = None, linkId_ = None, retryDurationInHours_ = None):
	
	'''
	 The optional from_ parameter should be populated with the value of a shortcode or alphanumeric that is 
	 registered with us 
	 
         The optional bulkSMSMode_ parameter will be used by the Mobile Service Provider to determine who gets billed for a 
	 message sent using a Mobile-Terminated ShortCode. The default value is 1 (which means that 
	 you, the sender, gets charged). This parameter will be ignored for messages sent using 
	 alphanumerics or Mobile-Originated shortcodes.
	 
         The optional enqueue_ parameter is useful when sending a lot of messages at once where speed is of the essence
         
         The optional keyword_ is used to specify which subscription product to use to send messages for premium rated short codes
         
         The optional linkId_ parameter is pecified when responding to an on-demand content request on a premium rated short code
         
         '''
	
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

        headers = {'Accept' : 'application/json',
		   'apikey' : self.apiKey }
	
	try:
            data     = urllib.urlencode(values)
            request  = urllib2.Request(self.SmsUrlString, data, headers=headers)
            response = urllib2.urlopen(request)
            the_page = response.read()
            print "Response is " + the_page
            
        except urllib2.HTTPError as e:
            the_page = e.read()
            raise AfricasTalkingGatewayException(the_page)

        else:
            decoded  = json.loads(the_page)
            recipients = decoded['SMSMessageData']['Recipients']
            return recipients
    
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
        
    def call(self, from_, to_, enqueue_ = 0):
	values = {'username' : self.username,
		  'from'     : from_,
                  'to'       : to_,
                  'enqueue'  : enqueue_}
        
	headers = {'Accept' : 'application/json',
                   'apikey' : self.apiKey }
        
        try:
            data     = urllib.urlencode(values)
            request  = urllib2.Request(self.VoiceUrlString, data, headers=headers)
            response = urllib2.urlopen(request)
            return response.read()

        except urllib2.HTTPError as e:
            the_page = e.read()
            raise AfricasTalkingGatewayException(the_page)

    def sendAirtime(self, recipients_):
        values = {'username'   : self.username,
		  'recipients' : json.dumps(recipients_) }
        
	headers = {'Accept' : 'application/json',
                   'apikey' : self.apiKey }
        
        try:
            data     = urllib.urlencode(values)
            request  = urllib2.Request(self.SendAirtimeUrlString, data, headers=headers)
            response = urllib2.urlopen(request)
        
        except urllib2.HTTPError as e:
            the_page = e.read()
            raise AfricasTalkingGatewayException(the_page)
        
        else:
            decoded   = json.loads(response.read())
            responses = decoded['responses']
            if len(responses) > 0:
                return responses
            else:
                raise AfricasTalkingGatewayException(decoded['errorMessage'])

    def promptMobilePaymentCheckout(self, productName_, phoneNumber_, currencyCode_, amount_, metadata_):
        values = {'username'     : self.username,
		  'productName'  : productName_,
                  'phoneNumber'  : phoneNumber_,
                  'currencyCode' : currencyCode_,
                  'amount'       : amount_,
                  'metadata'     : metadata_}

	headers = {'Content-Type' : 'application/json',
                   'Accept'       : 'application/json',
                   'apikey'       : self.apiKey }
        
        try:
            data     = json.dumps(values)                    
            request  = urllib2.Request(self.MobilePaymentCheckoutUrlString, data, headers=headers)
            response = urllib2.urlopen(request)
        
        except urllib2.HTTPError as e:
            the_page = e.read()
            raise AfricasTalkingGatewayException(the_page)
        
        else:
            responseStr = response.read()
            print "SNG: response is " + responseStr
            decoded     = json.loads(responseStr)
            return decoded
            
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

	headers = {'Accept' : 'application/json',
                   'apikey' : self.apiKey }
        
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
    
