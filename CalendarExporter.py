from RedmineClient import RedmineClient
from datetime import datetime, timedelta
import re
from icalendar import Calendar, Event
import tempfile, os

class CalendarExporter:
    def export(self):
        cal = Calendar()
        issues = self.prepareIssues()
        for issue in issues:
            event = Event()
            event.add('summary', str(issue["author"]) + " - " + issue["subject"])
            event.add('dtstart', issue["startDate"])
            event.add('dtend', issue["endDate"])
            cal.add_component(event)
        
        directory = tempfile.mkdtemp()
        path = os.path.join(directory, 'export.ics')
        f = open(path, 'wb')
        f.write(cal.to_ical())
        f.close()

        print(path)

    def prepareIssues(self):
        redmineClient = RedmineClient()
        vacations = redmineClient.issues("urlaub")
        issues = list()
        for vacation in vacations:
            print(vacation.subject)
            
            match = re.findall(r'\d{2}.\d{2}.\d{2,4}', vacation.subject)

            if match:
                startDate = self.try_parsing_date(match[0])
                if len(match) > 1:
                    endDate = self.try_parsing_date(match[1]) + timedelta(days=1)
                else:
                    endDate = startDate

                issues.append({
                    "startDate": startDate, 
                    "endDate": endDate,
                    "author": vacation.author, 
                    "subject": vacation.subject
                })

        return issues

    def try_parsing_date(self, text):
        for fmt in ('%d.%m.%Y', '%d.%m.%y'):
            try:
                return datetime.strptime(text, fmt).date()
            except ValueError:
                pass
        raise ValueError('no valid date format found')
