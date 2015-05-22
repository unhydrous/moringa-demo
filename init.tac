from twisted.application import service
from twisted.python.log import ILogObserver
from twisted.python.logfile import LogFile

import demo, config
from log import ATFileLogObserver

s           = demo.makeService()
application = service.Application('ATDemo')

logDir      = config.Config['logDir']
logfile     = LogFile("application.log", logDir, rotateLength=None)
application.setComponent(ILogObserver, ATFileLogObserver(logfile).emit)

s.setServiceParent(service.IServiceCollection(application))
