import curses
import calendar
from .colors import PyCalColors

cal = calendar.Calendar()
cell_width = 6
weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

current_year = 2022
current_month = 1
current_day = 1

events_dates = []
holidays = []

def get_month_string(month):
    return months[month]

def draw_month_header(window):
    calendar_width = (cell_width + 1) * 7 + 1

    core_string = "| " + str(current_year) + " - " + get_month_string(current_month - 1) + " |"
    top_string_width = len(core_string)
    top_string = ""
    for i in range(top_string_width):
        top_string += "-"
    padded_top_string = top_string.center(calendar_width)

    padded_top_string += "\n"
    window.addstr(padded_top_string)

    padded_core_string = core_string.center(calendar_width) + "\n"
    window.addstr(padded_core_string)
    window.addstr(padded_top_string)

def draw_weekdays(window):
    window.addstr("|", curses.color_pair(PyCalColors.color_white.standard_color_id))

    for weekday in weekdays:
        window.addstr(weekday.center(cell_width), curses.color_pair(PyCalColors.color_red.standard_color_id))
        window.addstr("|", curses.color_pair(PyCalColors.color_white.standard_color_id))
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
    window.addstr(get_calendar_delimiter(), curses.color_pair(PyCalColors.color_white.standard_color_id))

def get_date_string(date):
    output = ""
    if date.day < 10:
        output = "0" + str(date.day)
    else:
        output = str(date.day)
    return output

def is_weekend(date):
    return date.weekday() == 6 or date.weekday() == 5

def is_holiday(date):
    for holiday in holidays:
        if holiday["day"] == date.day and holiday["month"] == date.month:
            return True
    return False

def date_has_content(date):
    for i in events_dates:
        if i.year == date.year and i.month == date.month and i.day == date.day:
            return True
    return False

def get_color_for_date(date):
    selected_color_object = PyCalColors.color_white
    selected_color_id = selected_color_object.standard_color_id
    small_highlight = False

    # Check if special day
    if date.month != current_month:
        selected_color_object = PyCalColors.color_blue
    elif is_weekend(date) or is_holiday(date):
        selected_color_object = PyCalColors.color_red

    # Check if highlighted
    if date.day == current_day and date.month == current_month:
        selected_color_id = selected_color_object.highlight_color_id
    elif date_has_content(date):
        selected_color_id = selected_color_object.alt_highlight_color_id
        small_highlight = True
    else:
        selected_color_id = selected_color_object.standard_color_id

    return (selected_color_id, small_highlight)

def draw_calendar_days(window):
    weekday = 0
    for i in cal.itermonthdates(current_year, current_month):
        if weekday == 0:
            window.addstr("|", curses.color_pair(PyCalColors.color_white.standard_color_id))

        day_core_string = get_date_string(i)
        day_color_tuple = get_color_for_date(i)

        if day_color_tuple[1]:
            # If small highlight

            # Calculate whitespace
            whitespace_string = ""
            whitespace_width = int((cell_width - 2) / 2)
            for i in range(whitespace_width):
                whitespace_string += " "

            window.addstr(whitespace_string, PyCalColors.color_white.standard_color_id)
            window.addstr(day_core_string, curses.color_pair(day_color_tuple[0]))
            window.addstr(whitespace_string, PyCalColors.color_white.standard_color_id)
        else:
            # If not small highlight
            window.addstr(day_core_string.center(cell_width), curses.color_pair(day_color_tuple[0]))

        window.addstr("|", curses.color_pair(PyCalColors.color_white.standard_color_id))

        if weekday >= 6:
            weekday = 0
            window.addstr("\n")
        else:
            weekday += 1

def draw_calendar(window, year, month, day, dates_with_events=[], holidays_parameter=[]):
    global current_year
    global current_month
    global current_day
    global events_dates
    global holidays

    current_year = year
    current_month = month
    current_day = day

    events_dates = dates_with_events
    holidays = holidays_parameter

    window.clear()

    draw_month_header(window)
    window.addstr("\n")
    draw_weekdays(window)
    draw_calendar_delimiter(window)
    draw_calendar_days(window)
    window.refresh()

# Returns new window object that should house the calendar section
def init_calendar_window():
    win_height = 13
    win_width = 60
    win_start_x = 0
    win_start_y = 2

    # Init window
    window = curses.newwin(win_height, win_width, win_start_y, win_start_x)

    return window
