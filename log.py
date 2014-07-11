from pytz import timezone
from datetime import datetime

from twisted.python.log import FileLogObserver

class ATFileLogObserver(FileLogObserver):
    
    tz = timezone('Africa/Nairobi')
    
    def formatTime(self, when):
        when     = datetime.fromtimestamp(when, self.tz)
        tzOffset = when.utcoffset()  
        
        tzHour = abs(int(tzOffset.seconds / 60 / 60))
        tzMin  = abs(int(tzOffset.seconds / 60 % 60))
        if tzOffset.seconds < 0:
            tzSign = '-'
        else:
            tzSign = '+'
        return '%d-%02d-%02d %02d:%02d:%02d%s%02d%02d' % (
            when.year, when.month, when.day,
            when.hour, when.minute, when.second,
            tzSign, tzHour, tzMin)

