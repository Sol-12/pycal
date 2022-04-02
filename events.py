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

    def get_time_format(self):
        return str(self.datetime.hour) + ":" + str(self.datetime.minute)

    def to_vim_string(self):
        output = "# " + self.title + "\n\n"
        output += "---\n\n"
        output += "ID: " + str(self.id) + "\n"
        output += "Date: " + self.get_date_format() + "\n"
        if self.type != "timeless":
            output += "Time: " + self.get_time_format() + "\n"
        output += "\n---\n\n"
        output += self.content
        return output

    def open_in_vim(self):
        with open('tmp_event.md', 'w') as fileptr:
            fileptr.write(self.to_vim_string())
            fileptr.close()

        os.system("nvim tmp_event.md")

    def parse_tmp_vim_file(self):
        parsed_title = None
        parsed_id = None
        parsed_date = None
        parsed_content = ""
        parsed_time = None
        
        tmp_event_string = ""
        with open('tmp_event.md') as fileptr:
            tmp_event_string = fileptr.read()
            fileptr.close()

        if tmp_event_string == "":
            return

        split_string = tmp_event_string.split('\n')

        # 0 - title section, 1 - meta section, 2 description section
        section_inx = 0 

        meta_section_split_counter = 0
        for line in split_string:
            if section_inx == 0:
                # Title section
                if line[:2] == "# ": 
                    # Parse title
                    parsed_title = line[2:]
                    section_inx += 1
            elif section_inx == 1:
                # Meta section
                if line[:3] == "---":
                    meta_section_split_counter += 1

                    # If meta section ended
                    if meta_section_split_counter > 1:
                        section_inx += 1
                split_line = line.split(":")
                if len(split_line) > 1:
                    keyword = split_line[0]

                    # Get all what comes after the first : as the value
                    value = ""
                    for i in split_line[1:]:
                        value += i + ":"
                    value = value[:len(value)-1]

                    # Clean value
                    value = value.strip()

                    if keyword == "Time":
                        hour_minute = value.split(":")
                        print(hour_minute)

                        if len(hour_minute) > 1:
                            hour = int(hour_minute[0])
                            minute = int(hour_minute[1])
                            
                            parsed_time = datetime(self.datetime.year, self.datetime.month, self.datetime.day, hour, minute)

            else:
                # Content section
                parsed_content += line + "\n"

        # Clean parsed content
        if parsed_content[:1] == "\n":
            parsed_content = parsed_content[1:]

        if parsed_content[len(parsed_content)-2:] == "\n\n":
            parsed_content = parsed_content[:len(parsed_content)-2]

        # Apply changes
        if parsed_title != None:
            self.title = parsed_title

        if parsed_content != "":
            self.content = parsed_content

        if parsed_time != None:
            self.datetime = parsed_time
            self.type = None

    def to_json(self):
        return {
            "id": self.id,
            "datetime": self.datetime.isoformat(),
            "title": self.title, 
            "content": self.content,
            "type": self.type
        }

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

    def write_to_file(self):
        filename = "calendar.json"
        base_path = sys.path[0]
        data_path = base_path + "/" + filename

        json_array = []
        for event in self.events:
            json_array.append(event.to_json())

        with open(data_path, 'w') as fileptr:
            fileptr.write(json.dumps(json_array))
            fileptr.close()


