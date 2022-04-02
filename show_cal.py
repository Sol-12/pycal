#!/bin/python3

import json
import getopt
import sys
from datetime import datetime

from print_calendar import print_calendar
from print_calendar import get_month_string

filename = "calendar.json"
base_path = sys.path[0]
holidays_filename = "holidays.json"
holidays_path = base_path + "/" + holidays_filename

# Loaded JSON data 
data = None
holidays = []

# Loads data from a json file
def load_data():
    global data

    data_path = base_path + "/" + filename

    file_pointer = open(data_path)
    raw_data = json.load(file_pointer)
    file_pointer.close()

    data = []
    for event in raw_data:
        raw_event_datetime = event["datetime"]
        event_datetime = datetime.fromisoformat(raw_event_datetime)

        event_type = None
        if "type" in event: 
            event_type = event["type"]

        parsed_event = {
                "id": event["id"],
                "datetime": event_datetime,
                "title": event["title"],
                "content": event["content"],
                "type": event_type
        }
        data.append(parsed_event)

def load_holidays():
    global holidays

    with open(holidays_path) as fileptr:
        holidays = json.load(fileptr)
        fileptr.close()

# Analyzes data we have an returns all days that have an event
def get_dates_with_events():
    output = []
    for event in data:
        output.append(event["datetime"])

    return output

def is_same_date(day, month, year, date):
    return date.day == day and date.month == month and date.year == year

def get_events_for_date(day, month, year):
    output = []

    for event in data:
        if is_same_date(day, month, year, event["datetime"]):
            output.append(event)

    return output

def format_time(date):
    hour = date.hour
    minute = date.minute

    if hour < 10:
        hour = "0" + str(hour)
    else:
        hour = str(hour)

    if minute < 10:
        minute = "0" + str(minute)
    else:
        minute = str(minute)

    output = hour + ":" + minute
    return output

def get_holidays_for_selected_day(selected_year, selected_month, selected_day):
    # TODO: add easter
    output = []
    for holiday in holidays:
        if holiday["day"] == selected_day and holiday["month"] == selected_month:
            output.append(holiday)

    return output

def print_selected_day_events(selected_year, selected_month, selected_day):

    selected_day_events = get_events_for_date(selected_day, selected_month, selected_year)
    selected_day_holidays = get_holidays_for_selected_day(selected_year, selected_month, selected_day)

    # If there's anything happening that day, print the header
    if len(selected_day_holidays) != 0 or len(selected_day_events) != 0:
        print()
        print("# " + get_month_string(selected_month - 1) + " " + str(selected_day))

    # Print holiday, if any
    if len(selected_day_holidays) != 0:
        print("## HOLIDAYS")
        for holiday in selected_day_holidays:
            print("- " + holiday["name"])

    # Print event, if any 
    if len(selected_day_events) != 0: # print events
        print("## EVENTS")

        for event in selected_day_events:
            print("- ", end='')
            print("(", end='')
            print(format_time(event["datetime"]), end='')
            print(")", end='')
            print(" [" ,end='')
            print(event["id"], end='')
            print("] " ,end='')
            print(event["title"])
            print(event["content"])

def load_and_get_events_dates():
    load_data()
    return get_dates_with_events()

def load_and_get_holidays():
    load_holidays()
    return holidays

def get_selected_day_events_string(selected_year, selected_month, selected_day, selected_day_events = None, selected_day_holidays = None, selected_event = None):
    output = ""

    if selected_day_events == None or selected_day_holidays == None:
        # Load data
        load_data()
        load_holidays()

        selected_day_events = get_events_for_date(selected_day, selected_month, selected_year)
        selected_day_holidays = get_holidays_for_selected_day(selected_year, selected_month, selected_day)

    # If there's anything happening that day, add the header
    if len(selected_day_holidays) != 0 or len(selected_day_events) != 0:
        output += "\n" + "# " + get_month_string(selected_month - 1) + " " + str(selected_day) + "\n"

    # Add holidays, if any
    if len(selected_day_holidays) != 0:
        output += "## HOLIDAYS\n"
        for holiday in selected_day_holidays:
            output += "- " + holiday["name"] + "\n"

    # Add events, if any 
    if len(selected_day_events) != 0:
        output += "## EVENTS\n"

        event_counter = 0
        for event in selected_day_events:
            if event["type"] == "timeless":
                # Event without time
                if selected_event == event_counter:
                    output += "- " + " ([" + str(event["id"]) + "]) " + event["title"] + "\n" + event["content"] + "\n"
                else:
                    output += "- " + " [" + str(event["id"]) + "] " + event["title"] + "\n" + event["content"] + "\n"
            else:
                # Event with time
                output += "- (" + format_time(event["datetime"]) + ")" + " [" + str(event["id"]) + "] " + event["title"] + "\n" + event["content"] + "\n"

            event_counter += 1

    return output


def main(args):
    # Default arguments
    selected_year = datetime.today().year
    selected_month = datetime.today().month
    selected_day = datetime.today().day

    # Parse arguments
    for key, val in args:
        if key == "-y":
            selected_year = int(val)
        elif key == "-m":
            selected_month = int(val)
        elif key == "-d":
            selected_day = int(val)

    # Load data
    load_data()
    load_holidays()

    # Events
    dates_with_events = get_dates_with_events()

    # Display calendar
    print_calendar(selected_year, selected_month, selected_day, dates_with_events, holidays)

    # Display events if any
    print_selected_day_events(selected_year, selected_month, selected_day)

if __name__ == '__main__':
    # Get arguments
    argv = sys.argv[1:]
    args = getopt.getopt(argv, "y:m:d:")
    main(args[0])
