import curses
import calendar
from curses import wrapper
from print_calendar import get_calendar_string

# Configuration
ESCAPE_KEY = "q"
PREVIOUS_KEY = "h"
NEXT_KEY = "l"
UP_KEY = "k"
DOWN_KEY = "j"

# Globals
year = 2022
month = 2
day = 28

def day_exists():
    return True

def next_month():
    global month
    global year
    if month == 12:
        year += 1
        month = 1
    else:
        month += 1

def previous_month():
    global month
    global year
    if month == 1:
        year -= 1
        month = 12
    else:
        month -= 1

def increment_day(val):
    global year
    global month
    global day

    days_in_month = calendar.monthrange(year, month)[1]

    new_day = day + val
    if new_day > days_in_month:
        day = new_day - days_in_month
        next_month()
    elif new_day < 1:
        previous_month()
        days_in_new_month = calendar.monthrange(year, month)[1]
        day = days_in_new_month + new_day
    else: 
        day = new_day

def next_day():
    increment_day(1)

def previous_day():
    increment_day(-1)

def next_week():
    increment_day(7)

def previous_week():
    increment_day(-7)

# Main loop
def main(stdscr):

    stdscr.clear()
    current_key = ""
    while current_key != ESCAPE_KEY:
        # Update display
        stdscr.addstr(0, 0, get_calendar_string(year, month, day))
        stdscr.refresh()

        # Get command
        current_key = stdscr.getkey()

        # Handle command
        if current_key == NEXT_KEY:
            next_day()
        elif current_key == PREVIOUS_KEY:
            previous_day()
        elif current_key == UP_KEY:
            previous_week()
        elif current_key == DOWN_KEY:
            next_week()

if __name__ == "__main__":
    wrapper(main)
