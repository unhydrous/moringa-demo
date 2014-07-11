from twisted.application import service
from twisted.python.log import ILogObserver
from twisted.python.logfile import LogFile

import staging, config
from log import ATFileLogObserver

s           = staging.makeService()
application = service.Application('ATStaging')

logDir      = config.Config['logDir']
logfile     = LogFile("application.log", logDir, rotateLength=None)
application.setComponent(ILogObserver, ATFileLogObserver(logfile).emit)

s.setServiceParent(service.IServiceCollection(application))
