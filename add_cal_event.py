#!/bin/python3

import json
import getopt
import sys
from datetime import datetime

filename = "calendar.json"
base_path = sys.path[0]
data_path = base_path + "/" + filename

def assemble_datetime(year, month, day, hour, minute):
    return datetime(year, month, day, hour, minute)

def get_next_id():
    data = None
    with open(data_path) as fileptr:
        data = json.load(fileptr)
        fileptr.close()

    if data == None:
        return None

    highest_id = 0
    for event in data:
        if event["id"] > highest_id:
            highest_id = event["id"]

    new_id = highest_id + 1
    return new_id

def save_event(event):
    data = None
    with open(data_path) as fileptr:
        data = json.load(fileptr)
        fileptr.close()

    data.append(event)

    with open(data_path, 'w') as fileptr:
        fileptr.write(json.dumps(data))
        fileptr.close()

def add_event_to_json(datetime, title, content):
    new_id = get_next_id()

    if new_id == None:
        print("Adding failed, couldn't calculate new id...")
        return

    datetime_iso_format = datetime.isoformat()

    event = {
        "id": new_id,
        "datetime": datetime_iso_format,
        "title": title, 
        "content": content,
        "type": "timeless"
    }

    save_event(event)

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

    event_datetime = assemble_datetime(selected_year, selected_month, selected_day, hour, minute)
    add_event_to_json(event_datetime, title, content)

if __name__ == '__main__':
    # Get arguments
    argv = sys.argv[1:]
    args = getopt.getopt(argv, "y:m:d:h:M:t:c:")
    main(args[0])
