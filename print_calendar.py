import json
import calendar
from datetime import date
import getopt
import sys

cal = calendar.Calendar()
cell_width = 12

base_path = sys.path[0]
holidays_filename = "holidays.json"
holidays_path = base_path + "/" + holidays_filename
holidays = []

weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
current_year = 2022
current_month = 12
selected_day = 8
days_with_events = []

class bcolors:
    OK = '\033[92m' #GREEN
    WARNING = '\033[93m' #YELLOW
    FAIL = '\033[91m' #RED
    RESET = '\033[0m' #RESET COLOR

def day_to_string(day):
    if day < 10:
        return "0" + str(day)
    else:
        return str(day)

# returns a string with day and marks for that day, if necessary
def date_day_to_string(date):
    output = day_to_string(date.day)
    if date.day == selected_day and date.month == current_month:
        current_month_delimiter = "|"
        output = current_month_delimiter + output + current_month_delimiter
    elif date_has_content(date):
        output = " " + output
        output += "*"
    return output

def date_has_content(date):
    for i in days_with_events:
        if i.year == date.year and i.month == date.month and i.day == date.day:
            return True
    return False

def get_month_string(month):
    return months[month]

def get_month_header():
    output = ""

    calendar_width = (cell_width + 1) * 7 + 1

    core_string = "| " + str(current_year) + " - " + get_month_string(current_month - 1) + " |"
    top_string_width = len(core_string)
    top_string = ""
    for i in range(top_string_width):
        top_string += "-"
    padded_top_string = top_string.center(calendar_width)

    output += padded_top_string + "\n"

    padded_core_string = core_string.center(calendar_width)
    output += padded_core_string + "\n"
    output += padded_top_string + "\n"
    return output

def get_weekday_header():
    output = ""
    for i in range(7):
        day_string = weekdays[i].center(cell_width)
        output += "|"
        output += day_string

    output += "|"
    return output

def get_calendar_delimiter():
    output = ""
    for i in range(7):
        output += "|"
        for i in range(cell_width):
            output += "-"

    output += "|"
    return output

def is_holiday(date):
    for holiday in holidays:
        if holiday["day"] == date.day and holiday["month"] == date.month:
            return True
    return False

# is the day free of work
def is_free_day(date):
    return date.weekday() == 5 or date.weekday() == 6 or is_holiday(date)

# returns the center section of the date, without the |
def get_date_with_colors(date):
    output = ""

    padded_day_string = date_day_to_string(date).center(cell_width)

    if date.day == selected_day and date.month == current_month:
        output += padded_day_string
    elif date.month != current_month: # day is only in previous / next month
        output += padded_day_string
    elif is_free_day(date): # day is only weekend / holiday
        output += padded_day_string
    else: # it's a normal day
        output += padded_day_string

    return output

def get_days_section():
    output = ""
    weekday = 0
    for i in cal.itermonthdates(current_year, current_month):
        if weekday == 0:
            output += "|"
        day = get_date_with_colors(i)
        output += day
        output += "|"
        if weekday >= 6:
            weekday = 0
            output += "\n"
        else:
            weekday += 1
    return output

def get_calendar_string(year, month, day=None, event_datetimes=[], holidays_parameter=[]):
    global current_year
    global current_month
    global selected_day
    global days_with_events
    global holidays

    # Set global variables
    current_year = year
    current_month = month
    selected_day = day
    days_with_events = event_datetimes
    holidays = holidays_parameter

    output = ""
    output += get_month_header()
    output += get_weekday_header() + "\n"
    output += get_calendar_delimiter() + "\n"
    output += get_days_section()

    return output

def print_calendar(year, month, day=None, event_datetimes=None, holidays_parameter=[]):
    calendar_string = get_calendar_string(year, month, day, event_datetimes, holidays_parameter)
    print(calendar_string)

def main():
    # Get arguments
    argv = sys.argv[1:]
    args = getopt.getopt(argv, "y:m:d:")

    # Set default values
    year = date.today().year
    month = date.today().month
    day = date.today().day

    # Parse arguments
    for key, val in args[0]:
        if key == "-y":
            year = int(val)
        elif key == "-m":
            month = int(val)
        elif key == "-d":
            day = int(val)

    # Display calendar
    print_calendar(year, month, day)

if __name__ == '__main__':
    main()
