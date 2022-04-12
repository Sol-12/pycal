import curses
import calendar

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
color_white: Color
color_red: Color
color_blue: Color

cal = calendar.Calendar()
cell_width = 6
weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

current_year = 2022
current_month = 1
current_day = 1


def init_colors():
    global color_white
    global color_red
    global color_blue

    color_white = Color(highlight_foreground_color=curses.COLOR_BLACK)
    color_red = Color(standard_color = curses.COLOR_RED)
    color_blue = Color(standard_color=curses.COLOR_BLUE)

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
    if date.month != current_month:
        selected_color_object = color_blue
    elif is_holiday(date):
        selected_color_object = color_red

    # Check if highlighted
    if date.day == current_day and date.month == current_month:
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

def draw_calendar(window, year, month, day):
    global current_year
    global current_month
    global current_day

    current_year = year
    current_month = month
    current_day = day

    init_colors()
    window.clear()

    draw_month_header(window)
    window.addstr("\n")
    draw_weekdays(window)
    draw_calendar_delimiter(window)
    draw_calendar_days(window)
    window.refresh()
