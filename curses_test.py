import curses
from curses import wrapper
from print_calendar import get_calendar_string

ESCAPE_KEY = "q"

def test_func():
    year = 2022
    month = 3
    day = 28

    cal = get_calendar_string(year, month, day)
    print(cal)

def main(stdscr):
    year = 2022
    month = 3
    day = 28

    current_key = ""
    while current_key != ESCAPE_KEY:
        stdscr.clear()
        stdscr.addstr(get_calendar_string(year, month, day))
        stdscr.addstr(current_key)
        current_key = stdscr.getkey()

if __name__ == "__main__":
    wrapper(main)
