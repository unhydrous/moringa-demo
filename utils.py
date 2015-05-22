from twisted.internet import defer
from twisted.web import client
from twisted.python import log

@defer.inlineCallbacks
def fetchPostUrlContent(url, data, headers):
    log.msg("The data when fetching the post url is %s" % str(data))
    the_page = yield client.getPage(url, method="POST", postdata=data, headers=headers)
    defer.returnValue(the_page.strip())
