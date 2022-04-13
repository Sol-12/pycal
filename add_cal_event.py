#!/bin/python3

# Enables adding an event from cli

import json
import getopt
import sys

from datetime import datetime

from events.event_manager import EventManager
from events.events import Event

filename = "calendar.json"
base_path = sys.path[0]
data_path = base_path + "/" + filename

def add_event_to_json(datetime, title, content):
    manager = EventManager()
    event = Event(datetime=datetime, title=title, content=content)
    manager.add_event(event)

def main(args):
    # Default arguments
    selected_year = datetime.today().year
    selected_month = datetime.today().month
    selected_day = datetime.today().day
    hour = datetime.now().hour
    minute = datetime.now().minute
    title = None
    content = ""

    # Parse arguments
    for key, val in args:
        if key == "-y":
            selected_year = int(val)
        elif key == "-m":
            selected_month = int(val)
        elif key == "-d":
            selected_day = int(val)
        elif key == "-t":
            title = val
        elif key == "-c":
            content = val
        elif key == "-h":
            hour = int(val)
        elif key == "-M":
            minute = int(val)

    if title == None:
        print("Title (-t) option is required")
        return

    event_datetime = datetime(selected_year, selected_month, selected_day, hour, minute)
    add_event_to_json(event_datetime, title, content)

if __name__ == '__main__':
    # Get arguments
    argv = sys.argv[1:]
    args = getopt.getopt(argv, "y:m:d:h:M:t:c:")
    main(args[0])
