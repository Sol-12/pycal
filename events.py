import json
import getopt
import sys
import os

from datetime import datetime

# Event model
class Event:
    def __init__(self, jsonObj):
        self.id = jsonObj["id"]
        self.title = jsonObj["title"]

        raw_event_datetime = jsonObj["datetime"]
        event_datetime = datetime.fromisoformat(raw_event_datetime)
        self.datetime = event_datetime

        self.content = jsonObj["content"]

        event_type = None
        if "type" in jsonObj: 
            event_type = jsonObj["type"]
        self.type = event_type

    def is_on_date(self, day, month, year):
        return self.datetime.day == day and self.datetime.month == month and self.datetime.year == year

    def get_date_format(self):
        return str(self.datetime.day) + "/" + str(self.datetime.month) + "/" + str(self.datetime.year)

    def to_vim_string(self):
        output = "# " + self.title + "\n\n"
        output += "---\n\n"
        output += "ID: " + str(self.id) + "\n"
        output += "Date: " + self.get_date_format() + "\n\n"
        output += "---\n\n"
        output += self.content
        return output

    def open_in_vim(self):
        with open('tmp_event.md', 'w') as fileptr:
            fileptr.write(self.to_vim_string())
            fileptr.close()

        os.system("nvim tmp_event.md")


# Read and write events
class EventManager:
    def __init__(self):
        self.events = self.load_events()

    def load_events(self):
        filename = "calendar.json"
        base_path = sys.path[0]

        data_path = base_path + "/" + filename

        file_pointer = open(data_path)
        raw_data = json.load(file_pointer)
        file_pointer.close()

        data = []
        for event in raw_data:
            parsed_event = Event(event)
            data.append(parsed_event)

        return data

    def get_events_for_date(self, day, month, year):
        output = []

        for event in self.events:
            if event.is_on_date(day, month, year):
                output.append(event)

        return output

    def get_event_on_date(self, day, month, year, event_inx):
        events_on_date = self.get_events_for_date(day, month, year)

        if len(events_on_date) > event_inx:
            return events_on_date[event_inx]

        return None

