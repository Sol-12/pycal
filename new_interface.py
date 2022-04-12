import curses

from curses import wrapper

from config.configuration import Configuration
from ui.draw_calendar import draw_calendar
from ui.draw_calendar import init_calendar_window

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

    # Init window
    window = init_calendar_window()
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
