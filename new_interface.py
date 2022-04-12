import curses
import calendar

from curses import wrapper
from datetime import date

from enum import Enum

from config.configuration import Configuration
from ui.draw_calendar import draw_calendar

current_year = date.today().year
current_month = date.today().month
current_day = date.today().day

class Modes(Enum):
    CALENDAR = 0
    EVENTS = 1

# Get config
config = Configuration()
mode = Modes.CALENDAR


# Movement functions
def next_month():
    global current_month
    global current_year
    if current_month == 12:
        current_year += 1
        current_month = 1
    else:
        current_month += 1

def previous_month():
    global current_month
    global current_year

    if current_month == 1:
        current_year -= 1
        current_month = 12
    else:
        current_month -= 1

def next_event():
    global selected_event

    selected_event += 1

def previous_event():
    global selected_event
    
    if selected_event > 0:
        selected_event -= 1

def open_event():
    manager = EventManager()
    event = manager.get_event_on_date(day, month, year, event_inx=selected_event)
    event.open_in_vim()
    event.parse_tmp_vim_file()
    manager.write_to_file()

def increment_day(val):
    global current_year
    global current_month
    global current_day

    days_in_month = calendar.monthrange(current_year, current_month)[1]

    new_day = current_day + val
    if new_day > days_in_month:
        current_day = new_day - days_in_month
        next_month()
    elif new_day < 1:
        previous_month()
        days_in_new_month = calendar.monthrange(current_year, current_month)[1]
        current_day = days_in_new_month + new_day
    else: 
        current_day = new_day

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

    manager = EventManager()
    event = Event(event_datetime=event_datetime, title=event_title, content="")
    manager.add_event(event)

# Handle commands
def cycle_mode():
    global mode
    global selected_event

    if mode == Modes.CALENDAR:
        mode = Modes.EVENTS
        selected_event = 0
    else:
        selected_event = None
        mode = Modes.CALENDAR

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
    if key == UP_KEY:
        previous_event()
    elif key == DOWN_KEY:
        next_event()
    elif key == NEXT_KEY:
        open_event()

def handle_key_pressed(key, stdscr):

    # Handle switch mode key
    if key == config.CYCLE_MODE_KEY:
        cycle_mode()
        return

    # Handle key for current mode
    if mode == Modes.CALENDAR:
        handle_key_calendar_mode(key, stdscr)
    elif mode == Modes.EVENTS:
        handle_key_event_mode(key)

# Main loop
def main(stdscr):
    # Init
    curses.use_default_colors()
    stdscr.clear()
    win_height = 14
    win_width = 60
    win_start_x = 0
    win_start_y = 0

    # Init window
    window = curses.newwin(win_height, win_width, win_start_y, win_start_x)
    stdscr.refresh()

    current_key = ""

    # Loop
    while current_key != config.ESCAPE_KEY:
        # Update display
        draw_calendar(window, current_year, current_month, current_day)

        # Get command
        current_key = stdscr.getkey()

        # Handle the command
        handle_key_pressed(current_key, stdscr)

if __name__ == "__main__":
    wrapper(main)
