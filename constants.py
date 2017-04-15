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

OFFSETS = (-1, 0, 1)
ITERATION_LIMIT = 256  # Used to avoid infinite loops


class Color(object):
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    GRAY = "\033[2m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    DEFAULT = "\033[0m"


class Cell(Enum):
    SHIP_UNIT = 0
    SHIP_DAMAGED = 1
    SHIP_DESTROYED = 2
    SPACE_EMPTY = 3
    SPACE_HIT = 4


class Symbol(object):
    SHIP = chr(65517)  # 65517 or 'D'
    EMPTY = chr(1632)  # 1632, 1776, 183 or '.'
    HIT = chr(65794)  # 65794 or 'X' or '*'


STYLE = {
    Cell.SHIP_UNIT: (
        Symbol.SHIP,
        Color.BLUE,
    ),
    Cell.SHIP_DAMAGED: (
        Symbol.SHIP,
        Color.RED,
    ),
    Cell.SHIP_DESTROYED: (
        Symbol.SHIP,
        Color.GRAY,
    ),
    Cell.SPACE_EMPTY: (
        Symbol.EMPTY,
        Color.GRAY,
    ),
    Cell.SPACE_HIT: (
        Symbol.HIT,
        Color.GRAY,
    ),
}


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
