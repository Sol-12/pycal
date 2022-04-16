import json
import getopt
import sys
import os

from .events import Event

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

    def get_dates_with_events(self):
        # Analyzes data we have an returns all days that have an event
        output = []
        for event in self.events:
            output.append(event.datetime)

        return output

    def get_events_for_date(self, day, month, year):
        # Returns all events on a certain date
        output = []

        for event in self.events:
            if event.is_on_date(day, month, year):
                output.append(event)

        return output

    def get_event_on_date(self, day, month, year, event_inx) -> Event:
        # Returns an event on a specific day with a certain index
        events_on_date = self.get_events_for_date(day, month, year)

        if len(events_on_date) > event_inx:
            return events_on_date[event_inx]

        return None

    def write_to_file(self):
        # Write current list of events (self.events) to the calendar file
        filename = "calendar.json"
        base_path = sys.path[0]
        data_path = base_path + "/" + filename

        json_array = []
        for event in self.events:
            json_array.append(event.to_json())

        with open(data_path, 'w') as fileptr:
            fileptr.write(json.dumps(json_array))
            fileptr.close()

    def remove_event(self, event):
        # Removes event from list
        self.events.remove(event)

    def get_next_id(self):
        # Gets a new id for a new event
        highest_id = 0
        for event in self.events:
            if event.id > highest_id:
                highest_id = event.id

        new_id = highest_id + 1
        return new_id

    def add_event(self, event):
        # Adds a new event into the list
        if event.id == None:
            event.id = self.get_next_id()

        self.events.append(event)
        self.write_to_file()
