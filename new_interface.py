import curses
import calendar

from curses import wrapper
from datetime import date

from enum import Enum

from config.configuration import Configuration
from ui.draw_calendar import draw_calendar

from handle_command import State
from handle_command import handle_key_pressed

current_state = State()

# Get config
config = Configuration()

# Main loop
def main(stdscr):
    global current_state

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
        draw_calendar(window, current_state.year, current_state.month, current_state.day)

        # Get command
        current_key = stdscr.getkey()

        # Handle the command
        current_state = handle_key_pressed(current_key, stdscr)

if __name__ == "__main__":
    wrapper(main)
