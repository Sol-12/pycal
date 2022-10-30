import curses

class Color:
    last_color_id = 0

    def __init__(self, standard_color=curses.COLOR_WHITE, standard_highlight_color=-1, highlight_foreground_color=None, highlight_background_color=curses.COLOR_YELLOW, alt_highlight_foreground_color=None, alt_highlight_background_color=curses.COLOR_WHITE):
        self.standard_color = standard_color
        self.highlight_background_color = highlight_background_color

        if highlight_foreground_color == None:
            highlight_foreground_color = standard_color

        if alt_highlight_foreground_color == None:
            alt_highlight_foreground_color = standard_color

        self.highlight_foreground_color = highlight_foreground_color

        Color.last_color_id += 1
        self.standard_color_id = Color.last_color_id
        Color.last_color_id += 1
        self.highlight_color_id = Color.last_color_id
        Color.last_color_id += 1
        self.alt_highlight_color_id = Color.last_color_id
        
        curses.init_pair(self.standard_color_id, standard_color, standard_highlight_color)
        curses.init_pair(self.highlight_color_id, highlight_foreground_color, highlight_background_color)
        curses.init_pair(self.alt_highlight_color_id, alt_highlight_foreground_color, alt_highlight_background_color)

class PyCalColors:
    # Define colors
    color_white: Color
    color_red: Color
    color_blue: Color

    @staticmethod
    def init_colors():
        PyCalColors.color_white = Color(highlight_foreground_color=curses.COLOR_BLACK, alt_highlight_foreground_color=curses.COLOR_BLACK)
        PyCalColors.color_red = Color(standard_color = curses.COLOR_RED)
        PyCalColors.color_blue = Color(standard_color=curses.COLOR_BLUE)
