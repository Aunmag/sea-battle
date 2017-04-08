from enum import Enum

TITLE = 'Sea Battle'
VERSION = '0.7.0'
AUTHOR = 'Aunmag'

CELL_SHIP_UNIT = 'D'
CELL_SHIP_DAMAGED = 'x'
CELL_SHIP_DESTROYED = '#'
CELL_SPACE_EMPTY = '.'
CELL_SPACE_HIT = '*'
CELL_SPACE_BUFFER = '^'

X_AXIS_DIRECTED = 0
Y_AXIS_DIRECTED = 1

OFFSETS = (-1, 0, 1)

HIT_STATUS_UNKNOWN = -2
HIT_STATUS_MISS_REPEATED = -1
HIT_STATUS_MISS = 0
HIT_STATUS_DAMAGED = 1
HIT_STATUS_DESTROYED = 2


class CONSOLE(Enum):
    WRONG_INPUT = 0
