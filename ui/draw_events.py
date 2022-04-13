import curses
from .draw_calendar import get_month_string

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
            if event.type == "timeless":
                # Event without time
                if state.selected_event == event_counter:
                    window.addstr("- " + " ([" + str(event.id) + "]) " + event.title + "\n" + event.content + "\n")
                else:
                    window.addstr("- " + " [" + str(event.id) + "] " + event.title + "\n" + event.content + "\n")
            else:
                # Event with time
                if state.selected_event == event_counter:
                    window.addstr("- (" + format_time(event.datetime) + ")" + " ([" + str(event.id) + "]) " + event.title + "\n" + event.content + "\n")
                else:
                    window.addstr("- (" + format_time(event.datetime) + ")" + " [" + str(event.id) + "] " + event.title + "\n" + event.content + "\n")

            event_counter += 1

    window.refresh()

def init_events_window():
    win_height = 60
    win_width = 60
    win_start_x = 0
    win_start_y = 15

    # Init window
    window = curses.newwin(win_height, win_width, win_start_y, win_start_x)

    return window
