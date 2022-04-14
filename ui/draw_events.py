import curses
from .draw_calendar import get_month_string
from .colors import PyCalColors

def format_time(date):
    hour = date.hour
    minute = date.minute

    if hour < 10:
        hour = "0" + str(hour)
    else:
        hour = str(hour)

    if minute < 10:
        minute = "0" + str(minute)
    else:
        minute = str(minute)

    output = hour + ":" + minute
    return output

def draw_single_event(window, event, is_selected = False):
    # Draw title
    if is_selected:
        window.addstr(" ", curses.color_pair(PyCalColors.color_white.highlight_color_id))

    if event.type == "timeless":
        window.addstr(event.title, curses.A_UNDERLINE)
        window.addstr("\n")
    else:
        time_format = format_time(event.datetime)
        window.addstr(event.title, curses.A_UNDERLINE)
        window.addstr(" - " + "(" + time_format + ")\n")

    # Draw content
    if event.content != None and event.content != "":
        if is_selected:
            window.addstr(" ", curses.color_pair(PyCalColors.color_white.highlight_color_id))
        content = event.content
        if len(event.content) > 20:
            content = event.content[:20] + "..."
        content = content.replace('\n', '')
        window.addstr("-> " + content + "\n")
    
    # Draw separator
    window.addstr("------------------------------\n")

def draw_events(window, state, events, holidays):
    window.clear()
    # If there's anything happening that day, add the header
    if len(holidays) != 0 or len(events) != 0:
        window.addstr("\n" + "# " + get_month_string(state.month - 1) + " " + str(state.day) + "\n")

    # Add holidays, if any
    if len(holidays) != 0:
        window.addstr("## HOLIDAYS\n")
        for holiday in holidays:
            window.addstr("- " + holiday["name"] + "\n")

    # Add events, if any 
    if len(events) != 0:
        window.addstr("## EVENTS\n")

        event_counter = 0
        for event in events:
            is_selected = state.selected_event == event_counter
            draw_single_event(window, event, is_selected)
            event_counter += 1

    window.refresh()

def init_events_window():
    win_height = 60
    win_width = 60
    win_start_x = 0
    win_start_y = 12

    # Init window
    window = curses.newwin(win_height, win_width, win_start_y, win_start_x)

    return window
