import curses
from curses import wrapper
import calendar

current_year = 2022
current_month = 4
current_day = 10

cal = calendar.Calendar()
cell_width = 6
weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

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

def init_colors():
    global color_white
    global color_red

    color_white = Color()
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

    draw_weekdays(window)
    draw_calendar_delimiter(window)
    draw_calendar_days(window)
    window.refresh()

    current_key = ""
    current_key = stdscr.getkey()

if __name__ == "__main__":
    wrapper(main)
