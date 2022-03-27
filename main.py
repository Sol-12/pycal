import json
from datetime import datetime

from print_calendar import print_calendar
from print_calendar import get_month_string

# Loaded JSON data 
data = None

# Loads data from a json file
def load_data():
    global data

    file_pointer = open("calendar.json")
    raw_data = json.load(file_pointer)
    file_pointer.close()

    data = []
    for event in raw_data:
        raw_event_datetime = event["datetime"]
        event_datetime = datetime.fromisoformat(raw_event_datetime)
        parsed_event = {
                "id": event["id"],
                "datetime": event_datetime,
                "title": event["title"],
                "content": event["content"]
        }
        data.append(parsed_event)

# Creates 'example_calendar.json' file with an example of an json formatted calendar
def make_example_calendar_json():
    tmp_datetime = datetime.now()

    example_calendar = [{"id":"1","datetime":tmp_datetime.isoformat(),"content":"example content"}]

    json_string = json.dumps(example_calendar)

    with open("example_calendar.json", "w") as outfile:
        outfile.write(json_string)
        outfile.close()


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

def print_selected_day_events(selected_year, selected_month, selected_day):
    selected_day_events = get_events_for_date(selected_day, selected_month, selected_year)
    print()
    print("# " + get_month_string(selected_month - 1) + " " + str(selected_day))
    print("## EVENTS:")

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


def main():
    # Load arguments
    selected_year = 2022
    selected_month = 3
    selected_day = 27

    # Load data
    load_data()

    # Events
    dates_with_events = get_dates_with_events()

    # Display calendar
    print_calendar(selected_year, selected_month, selected_day, dates_with_events)

    # Display events if any
    print_selected_day_events(selected_year, selected_month, selected_day)

if __name__ == '__main__':
    main()

