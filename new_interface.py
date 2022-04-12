import curses
from curses import wrapper

import calendar

from enum import Enum

from config.configuration import Configuration

current_year = 2022
current_month = 4
current_day = 10

cal = calendar.Calendar()
cell_width = 6
weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

class Modes(Enum):
    CALENDAR = 0
    EVENTS = 1

class Color:
    last_color_id = 0

    def __init__(self, standard_color=curses.COLOR_WHITE, highlight_foreground_color=None, highlight_background_color=curses.COLOR_WHITE):
        self.standard_color = standard_color
        self.highlight_background_color = highlight_background_color

        if highlight_foreground_color == None:
            highlight_foreground_color = standard_color

        self.highlight_foreground_color = highlight_foreground_color

        Color.last_color_id += 1
        self.standard_color_id = Color.last_color_id
        Color.last_color_id += 1
        self.highlight_color_id = Color.last_color_id
        
        curses.init_pair(self.standard_color_id, standard_color, -1)
        curses.init_pair(self.highlight_color_id, highlight_foreground_color, highlight_background_color)

# Define colors
color_white = None
color_red = None

# Get config
config = Configuration()
mode = Modes.CALENDAR

def init_colors():
    global color_white
    global color_red

    color_white = Color(highlight_foreground_color=curses.COLOR_BLACK)
    color_red = Color(standard_color = curses.COLOR_RED)

def draw_weekdays(window):
    window.addstr("|", curses.color_pair(color_white.standard_color_id))

    for weekday in weekdays:
        window.addstr(weekday.center(cell_width), curses.color_pair(color_red.standard_color_id))
        window.addstr("|", curses.color_pair(color_white.standard_color_id))
    window.addstr("\n")

def get_calendar_delimiter():
    output = ""
    for i in range(7):
        output += "|"
        for i in range(cell_width):
            output += "-"

    output += "|\n"
    return output

def draw_calendar_delimiter(window):
    window.addstr(get_calendar_delimiter(), curses.color_pair(color_white.standard_color_id))

def get_date_string(date):
    output = ""
    if date.day < 10:
        output = "0" + str(date.day)
    else:
        output = str(date.day)
    return output.center(cell_width)

def is_holiday(date):
    return date.weekday() == 6 or date.weekday() == 5

def get_color_for_date(date):
    selected_color_object = color_white
    output_color_id = 0

    # Check if special day
    if is_holiday(date):
        selected_color_object = color_red

    # Check if highlighted
    if date.day == current_day:
        return selected_color_object.highlight_color_id

    return selected_color_object.standard_color_id

def draw_calendar_days(window):
    weekday = 0
    for i in cal.itermonthdates(current_year, current_month):
        if weekday == 0:
            window.addstr("|", curses.color_pair(color_white.standard_color_id))

        day_string = get_date_string(i)
        window.addstr(day_string, curses.color_pair(get_color_for_date(i)))
        window.addstr("|", curses.color_pair(color_white.standard_color_id))

        if weekday >= 6:
            weekday = 0
            window.addstr("\n")
        else:
            weekday += 1

def draw_calendar(window):
    window.clear()
    draw_weekdays(window)
    draw_calendar_delimiter(window)
    draw_calendar_days(window)
    window.refresh()

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
    win_height = 10
    win_width = 60
    win_start_x = 0
    win_start_y = 0

    # Init window
    window = curses.newwin(win_height, win_width, win_start_y, win_start_x)
    stdscr.refresh()

    # Init colors
    init_colors()


    current_key = ""

    # Loop
    while current_key != config.ESCAPE_KEY:
        # Update display
        draw_calendar(window)

        # Get command
        current_key = stdscr.getkey()

        # Handle the command
        handle_key_pressed(current_key, stdscr)

if __name__ == "__main__":
    wrapper(main)
