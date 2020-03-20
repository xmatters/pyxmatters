import datetime

class TimeCalc(object):

    def getTimeNow(self):
        return datetime.datetime.now()

    def formatDateTimeNow(self, time):
        return time.strftime("%m-%d-%Y %H:%M:%S")

    def getDiff(self, end, start):
        duration = (end-start)

        duration_in_s = duration.total_seconds()

        days    = divmod(duration_in_s, 86400)       # Get days (without [0]!)
        hours   = divmod(days[1], 3600)               # Use remainder of days to calc hours
        minutes = divmod(hours[1], 60)                # Use remainder of hours to calc minutes
        seconds = divmod(minutes[1], 1)               # Use remainder of minutes to calc seconds
        return "%d days, %d hours, %d minutes and %d seconds" % (days[0], hours[0], minutes[0], seconds[0])
