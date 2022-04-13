#!/bin/python3

import json
import sys
import curses
from curses import wrapper

from config.configuration import Configuration
from events.event_manager import EventManager
from handle_command import State
from handle_command import handle_key_pressed
from ui.draw_calendar import draw_calendar
from ui.draw_calendar import init_calendar_window
from ui.draw_events import draw_events, init_events_window
from ui.colors import PyCalColors

current_state = State()

# Get config
config = Configuration()

def get_holidays():
    base_path = sys.path[0]
    holidays_filename = "holidays.json"
    holidays_path = base_path + "/" + holidays_filename
    with open(holidays_path) as fileptr:
        holidays = json.load(fileptr)
        fileptr.close()
        return holidays

def get_todays_holidays(holidays):
    output = []
    for holiday in holidays:
        if holiday["month"] == current_state.month and holiday["day"] == current_state.day:
            output.append(holiday)

    return output

# Main loop
def main(stdscr):
    global current_state

    # Init
    curses.use_default_colors()
    PyCalColors.init_colors()
    stdscr.clear()

    # Init window
    calendar_window = init_calendar_window()
    events_window = init_events_window()
    stdscr.refresh()

    current_key = ""

    # Loop
    while current_key != config.ESCAPE_KEY:
        # Get events
        event_manager = EventManager()
        events = event_manager.get_events_for_date(current_state.day, current_state.month, current_state.year)
        events_dates = event_manager.get_dates_with_events()
        holidays = get_holidays()
        todays_holidays = get_todays_holidays(holidays)

        # Update display
        draw_calendar(calendar_window, current_state.year, current_state.month, current_state.day, events_dates, holidays)
        draw_events(events_window, current_state, events, todays_holidays)

        # Get command
        current_key = stdscr.getkey()

        # Handle the command
        current_state = handle_key_pressed(current_key, stdscr)

    calendar_window.clear()
    events_window.clear()
    stdscr.clear()

if __name__ == "__main__":
    wrapper(main)
