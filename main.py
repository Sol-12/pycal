import json
from print_calendar import print_calendar
from datetime import datetime

# Loaded JSON data 
data = None

# Loads data from a json file
def load_data():
    global data

    file_pointer = open("calendar.json")
    data = json.load(file_pointer)
    file_pointer.close()

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
        raw_event_datetime = event["datetime"]
        event_datetime = datetime.fromisoformat(raw_event_datetime)

        output.append(event_datetime)

    return output

def main():
    # Load arguments
    selected_year = 2022
    selected_month = 3
    selected_day = 26

    # Load data
    load_data()

    # Events
    dates_with_events = get_dates_with_events()

    # Display calendar
    print_calendar(selected_year, selected_month, selected_day, dates_with_events)

if __name__ == '__main__':
    main()

