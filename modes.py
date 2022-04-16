from enum import Enum

class Modes(Enum):
    CALENDAR = 0
    EVENTS = 1

    def get_mode_string(self):
        if self == Modes.CALENDAR:
            return "CALENDAR"
        else:
            return "EVENTS"
