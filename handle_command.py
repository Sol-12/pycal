import calendar
import curses
from curses.textpad import Textbox, rectangle

from datetime import date
from datetime import datetime

from enum import Enum

from config.configuration import Configuration

from events.events import Event
from events.event_manager import EventManager

class Modes(Enum):
    CALENDAR = 0
    EVENTS = 1

class State:
    def __init__(self):
        self.year = date.today().year
        self.month = date.today().month
        self.day = date.today().day

        self.mode = Modes.CALENDAR
        self.selected_event = 0

current_state = State()
config = Configuration()

def next_month():
    global current_state
    if current_state.month == 12:
        current_state.year += 1
        current_state.month = 1
    else:
        current_state.month += 1

def previous_month():
    global current_state

    if current_state.month == 1:
        current_state.year -= 1
        current_state.month = 12
    else:
        current_state.month -= 1

def next_event():
    global current_state

    current_state.selected_event += 1

def previous_event():
    global current_state
    
    if current_state.selected_event > 0:
        current_state.selected_event -= 1

def open_event():
    manager = EventManager()
    event = manager.get_event_on_date(current_state.day, current_state.month, current_state.year, event_inx=current_state.selected_event)
    event.open_in_vim()
    event.parse_tmp_vim_file()
    manager.write_to_file()

def increment_day(val):
    global current_state

    days_in_month = calendar.monthrange(current_state.year, current_state.month)[1]

    new_day = current_state.day + val
    if new_day > days_in_month:
        current_state.day = new_day - days_in_month
        next_month()
    elif new_day < 1:
        previous_month()
        days_in_new_month = calendar.monthrange(current_state.year, current_state.month)[1]
        current_state.day = days_in_new_month + new_day
    else: 
        current_state.day = new_day

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

    event_datetime = datetime(current_state.year, current_state.month, current_state.day)

    manager = EventManager()
    event = Event(event_datetime=event_datetime, title=event_title, content="")
    manager.add_event(event)

# Handle commands
def cycle_mode():
    global current_state

    if current_state.mode == Modes.CALENDAR:
        current_state.mode = Modes.EVENTS
        current_state.selected_event = 0
    else:
        current_state.selected_event = 0
        current_state.mode = Modes.CALENDAR

def handle_key_calendar_mode(key, stdscr):
    if key == config.NEXT_KEY:
        next_day()
    elif key == config.PREVIOUS_KEY:
        previous_day()
    elif key == config.UP_KEY:
        previous_week()
    elif key == config.DOWN_KEY:
        next_week()
    elif key == config.ADD_EVENT_KEY:
        add_event(stdscr)

def handle_key_event_mode(key):
    if key == config.UP_KEY:
        previous_event()
    elif key == config.DOWN_KEY:
        next_event()
    elif key == config.NEXT_KEY:
        open_event()

def handle_key_pressed(key, stdscr):

    # Handle switch mode key
    if key == config.CYCLE_MODE_KEY:
        cycle_mode()
        return

    # Handle key for current mode
    if current_state.mode == Modes.CALENDAR:
        handle_key_calendar_mode(key, stdscr)
    elif current_state.mode == Modes.EVENTS:
        handle_key_event_mode(key)

    return current_state
