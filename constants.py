from enum import Enum

TITLE = "Sea Battle"
VERSION = "0.8.0"
AUTHOR = "Aunmag"
DESCRIPTION = (
    f"{TITLE} (battleship) - my first text-based game, which I'd started to develop at "
    "February 2016. While I was been learning GUI, I decided to make this test project "
    "to code practicing. And some time later I was back to have all done completely and "
    "tweak some defects."
    "\n\n"
    "Notice that you may not arrange your ships manually. In the begging you can only "
    "shuffle their position randomly."
)

CELL_SHIP_UNIT = 'D'
CELL_SHIP_DAMAGED = 'x'
CELL_SHIP_DESTROYED = '#'
CELL_SPACE_EMPTY = '.'  # 183, 1632, 1776
CELL_SPACE_HIT = '*'  # 42295, 10625, 8226

OFFSETS = (-1, 0, 1)

ITERATION_LIMIT = 256  # Used to avoid infinite loops


class Color(object):

    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    GRAY = "\033[2m"
    READ = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    DEFAULT = "\033[0m"

    @classmethod
    def deactivate(cls):
        cls.BOLD = ''
        cls.UNDERLINE = ''
        cls.GRAY = ''
        cls.READ = ''
        cls.GREEN = ''
        cls.YELLOW = ''
        cls.BLUE = ''
        cls.DEFAULT = ''


class AxisDirection(Enum):
    UNKNOWN = 0
    X = 1
    Y = 2


class HitStatus(Enum):
    UNKNOWN = 0
    MISS = 1
    MISS_REPEATED = 2
    DAMAGED = 3
    DESTROYED = 4


class Console(Enum):
    WRONG_INPUT = 0
