from enum import Enum

TITLE = "Sea Battle"
VERSION = "0.7.0"
AUTHOR = "Aunmag"
DESCRIPTION = (
    "This is my first game (text-based) since 2016.03.12. While I was been learning GUI "
    "I decided to make this test project to work with code only."
    "\n\n"
    "For now AI can't distinguish and chase damaged ships. I'll improve it later."
    "\n\n"
    "Notice that you can't arrange your ships manually. In the begging you can only "
    "shuffle their position randomly."
)
TIPS = (
    " - After game start you take turn first"
    '\n'
    " - You may press Ctrl+C to exit game at any time"
    '\n'
    " - Source code available here: github.com/aunmag/sea-battle"
)

CELL_SHIP_UNIT = 'D'
CELL_SHIP_DAMAGED = 'x'
CELL_SHIP_DESTROYED = '#'
CELL_SPACE_EMPTY = '.'
CELL_SPACE_HIT = '*'
CELL_SPACE_BUFFER = '^'

OFFSETS = (-1, 0, 1)


class AxisDirection(Enum):
    X = 0
    Y = 1


class HitStatus(Enum):
    UNKNOWN = 0
    MISS = 1
    MISS_REPEATED = 2
    DAMAGED = 3
    DESTROYED = 4


class Console(Enum):
    WRONG_INPUT = 0
