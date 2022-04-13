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

# Main loop
def main(stdscr):
    global current_state

    # Init
    curses.use_default_colors()
    stdscr.clear()

    # Init window
    window = init_calendar_window()
    stdscr.refresh()

    current_key = ""

    # Loop
    while current_key != config.ESCAPE_KEY:
        # Get events
        event_manager = EventManager()
        events = event_manager.get_events_for_date(current_state.day, current_state.month, current_state.year)
        events_dates = event_manager.get_dates_with_events()
        holidays = get_holidays()

        # Update display
        draw_calendar(window, current_state.year, current_state.month, current_state.day, events_dates, holidays)

        # Get command
        current_key = stdscr.getkey()

        # Handle the command
        current_state = handle_key_pressed(current_key, stdscr)

if __name__ == "__main__":
    wrapper(main)
