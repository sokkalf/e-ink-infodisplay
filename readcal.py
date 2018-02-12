# coding=utf-8

from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
from dateutil import tz
import vobject
import caldav

class Readcal:
    def __init__(self, url, username, password):
        client = caldav.DAVClient(url, username=username, password=password)
        principal = client.principal()
        self.cal = principal.calendars()[0]

    def get_next_events(self):
        next_week = datetime.today()+ relativedelta(weeks=1)
        results = self.cal.date_search(datetime.today(), next_week)
        events = []
        for r in results:
            event = vobject.readOne(r.data)
            timestamp = parse(str(event.vevent.dtstart.valueRepr())).astimezone(tz.tzlocal())
            events = events + [(timestamp,event.vevent.summary.valueRepr().decode('utf8'))]

        events = sorted(events, key=lambda tup: tup[0])
        return events

