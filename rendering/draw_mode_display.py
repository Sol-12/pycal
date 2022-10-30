import curses
from .colors import PyCalColors

from modes import Modes

# Handle drawing mode display / text feedback section

title_string = "PyCal"

def draw_mode_display(window, output_string = None):
    window.clear()

    if output_string == None:
        current_string = title_string
    else: 
        current_string = output_string

    window.addstr(current_string, curses.color_pair(PyCalColors.color_red.standard_color_id))
    window.refresh()

def init_mode_display_window():
    win_height = 2
    win_width = 60
    win_start_x = 0
    win_start_y = 0

    # Init window
    window = curses.newwin(win_height, win_width, win_start_y, win_start_x)

    return window
