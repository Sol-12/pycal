#!/bin/python3

import curses
import calendar

from enum import Enum

from datetime import date
from datetime import datetime

from curses import wrapper
from curses.textpad import Textbox, rectangle

from print_calendar import get_calendar_string
from show_cal import load_and_get_holidays
from show_cal import load_and_get_events_dates
from show_cal import get_selected_day_events_string

from add_cal_event import add_event_to_json

class Modes(Enum):
    CALENDAR = 0
    EVENTS = 1

# Configuration
ESCAPE_KEY = "q"
PREVIOUS_KEY = "h"
NEXT_KEY = "l"
UP_KEY = "k"
DOWN_KEY = "j"

ADD_EVENT_KEY = "a"

CYCLE_MODE_KEY = "m"

# Globals
year = date.today().year
month = date.today().month
day = date.today().day

mode = Modes.CALENDAR

# Movement functions
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

# Add event
def add_event(stdscr):
    win = curses.newwin(1, 99, 1, 1)
    box = Textbox(win)
    rectangle(stdscr, 0, 0, 2, 100)
    stdscr.refresh()

    box.edit()

    event_title = box.gather()

    event_datetime = datetime(year, month, day)
    add_event_to_json(event_datetime, event_title, "")

# Render calendar and content
def get_calendar_with_content_string():
        holidays = load_and_get_holidays()
        events_dates = load_and_get_events_dates()

        calendar_view = get_calendar_string(year, month, day, events_dates, holidays)
        cal_entries = get_selected_day_events_string(year, month, day)
        return calendar_view + "\n" + cal_entries

def cycle_mode():
    global mode

    if mode == Modes.CALENDAR:
        mode = Modes.EVENTS
    else:
        mode = Modes.CALENDAR

def handle_key_calendar_mode(key):
    if key == NEXT_KEY:
        next_day()
    elif key == PREVIOUS_KEY:
        previous_day()
    elif key == UP_KEY:
        previous_week()
    elif key == DOWN_KEY:
        next_week()
    elif key == ADD_EVENT_KEY:
        add_event(stdscr)

def handle_key_event_mode(key):
    pass

def handle_key_pressed(key):

    # Handle switch mode key
    if key == CYCLE_MODE_KEY:
        cycle_mode()

    # Handle key for current mode
    if mode == Modes.CALENDAR:
        handle_key_calendar_mode(key)
    elif mode == Modes.EVENTS:
        handle_key_event_mode(key)

# Main loop
def main(stdscr):
    # Init
    stdscr.clear()
    current_key = ""

    # Loop
    while current_key != ESCAPE_KEY:
        to_display = get_calendar_with_content_string()

        # Update display
        stdscr.clear()
        stdscr.addstr(0, 0, to_display)

        # Get command
        current_key = stdscr.getkey()

        # Handle the command
        handle_key_pressed(current_key)

if __name__ == "__main__":
    wrapper(main)
