import calendar
from datetime import date
import getopt
import sys

cal = calendar.Calendar()
cell_width = 12

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

def print_month_header():
    calendar_width = (cell_width + 1) * 7 + 1

    core_string = "| " + str(current_year) + " - " + get_month_string(current_month - 1) + " |"
    top_string_width = len(core_string)
    top_string = ""
    for i in range(top_string_width):
        top_string += "-"
    padded_top_string = top_string.center(calendar_width)
    print(padded_top_string)

    padded_core_string = core_string.center(calendar_width)
    print(padded_core_string)
    print(padded_top_string)
    print()

def print_weekday_header():
    for i in range(7):
        day_string = weekdays[i].center(cell_width)
        print("|", end='')
        print(bcolors.FAIL + day_string + bcolors.RESET, end='')

    print("|\n", end='')

def print_calendar_delimiter():
    for i in range(7):
        print("|", end='')
        for i in range(cell_width):
            print("-", end='')

    print("|")

# is the day free of work
def is_free_day(date):
    if date.weekday() == 5 or date.weekday() == 6:
        return True
    return False

# prints the center section of the date, without the |
def print_date_with_colors(date):
    padded_day_string = date_day_to_string(date).center(cell_width)

    if date.day == selected_day:
        print(bcolors.OK + padded_day_string + bcolors.RESET, end='')
    elif is_free_day(date): # day is only weekend / holiday
        print(bcolors.FAIL + padded_day_string + bcolors.RESET, end='')
    elif date.month != current_month: # day is only in previous / next month
        print(bcolors.WARNING + padded_day_string + bcolors.RESET, end='')
    else: # it's a normal day
        print(padded_day_string, end='')

def print_days_section():
    weekday = 0
    for i in cal.itermonthdates(current_year, current_month):
        if weekday == 0:
            print("|", end='')
        print_date_with_colors(i)
        print("|", end='')
        if weekday >= 6:
            weekday = 0
            print()
        else:
            weekday += 1

def print_calendar(year, month, day=None, event_datetimes=None):
    global current_year
    global current_month
    global selected_day
    global days_with_events

    current_year = year
    current_month = month
    selected_day = day
    days_with_events = event_datetimes

    print_month_header()
    print_weekday_header()
    print_calendar_delimiter()
    print_days_section()

if __name__ == '__main__':
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

    print_calendar(year, month, day)
