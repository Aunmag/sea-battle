import os

from constants import *


class Color(object):

    BOLD = ''
    UNDERLINE = ''
    REVERSED = ''
    GRAY_1 = ''
    GRAY_2 = ''
    READ = ''
    GREEN = ''
    YELLOW = ''
    BLUE = ''
    IN_GRAY = ''
    IN_READ = ''
    IN_GREEN = ''
    IN_YELLOW = ''
    IN_BLUE = ''
    DEFAULT = ''

    @classmethod
    def activate(cls):
        code_start = "\033["
        code_end = "m"
        cls.BOLD = f"{code_start}1{code_end}"
        cls.UNDERLINE = f"{code_start}4{code_end}"
        cls.REVERSED = f"{code_start}7{code_end}"
        cls.GRAY_1 = f"{code_start}90{code_end}"
        cls.GRAY_2 = f"{code_start}2{code_end}"
        cls.READ = f"{code_start}91{code_end}"
        cls.GREEN = f"{code_start}92{code_end}"
        cls.YELLOW = f"{code_start}93{code_end}"
        cls.BLUE = f"{code_start}94{code_end}"
        cls.IN_GRAY = f"{code_start}40{code_end}"
        cls.IN_READ = f"{code_start}41{code_end}"
        cls.IN_GREEN = f"{code_start}42{code_end}"
        cls.IN_YELLOW = f"{code_start}43{code_end}"
        cls.IN_BLUE = f"{code_start}44{code_end}"
        cls.DEFAULT = f"{code_start}0{code_end}"

    @classmethod
    def deactivate(cls):
        cls.BOLD = ''
        cls.UNDERLINE = ''
        cls.REVERSED = ''
        cls.GRAY_1 = ''
        cls.GRAY_2 = ''
        cls.READ = ''
        cls.GREEN = ''
        cls.YELLOW = ''
        cls.BLUE = ''
        cls.IN_GRAY = ''
        cls.IN_READ = ''
        cls.IN_GREEN = ''
        cls.IN_YELLOW = ''
        cls.IN_BLUE = ''
        cls.DEFAULT = ''


def press_enter(message=None, action="continue"):
    message_press_enter = f"Press Enter to {action}... "

    if message is not None:
        message_press_enter = f"{message} {message_press_enter}"

    input(message_press_enter)


def clear():
    if os.name == 'nt':
        console_command = 'cls'
    else:
        console_command = 'clear'

    os.system(console_command)


def raise_wrong_hit_status(hit_status, x=None, y=None, details=None):
    message = "Got wrong hit status ({})."
    message = message.format(hit_status)

    if x is not None and y is not None:
        coordinates = "\nCoordinates: x{} y{}.".format(x, y)
        message += coordinates

    if details is not None:
        details = "\nDetails: {}".format(details)
        message += details

    raise ValueError(message)


def request_input(heading, choices):
    if not heading:
        heading = "Choices"

    message = f"### {heading}:"

    for number, choice in enumerate(choices):
        snipped = f"\n {number + 1}. {choice}"
        message += snipped

    message += "\n\nChose an action and press Enter: "

    input_value = input(message)
    input_value = validate_input(input_value, len(choices))
    return input_value


def validate_integer(value):
    try:
        value = int(value)
    except ValueError:
        print("Error. You have to enter integers. Change your choice.")
        return Console.WRONG_INPUT
    else:
        return value


def validate_input(value, choices_quantity):
    value = validate_integer(value)

    if value is Console.WRONG_INPUT:
        press_enter()
        return Console.WRONG_INPUT
    elif 0 < value <= choices_quantity:
        return value
    else:
        message = (
            f"You can chose between 1 an {choices_quantity} inclusively both."
            f"\nGot {value} instead. Please try again."
        )
        print(message)
        press_enter()
        return Console.WRONG_INPUT


def validate_input_coordinate(value, board_size):
    value = validate_integer(value)

    if value is Console.WRONG_INPUT:
        return Console.WRONG_INPUT
    elif 0 <= value < board_size:
        return value
    else:
        print("Error! This location is too far to hit! Change your choose.")
        return Console.WRONG_INPUT


def print_cell(cell):
    color = Color.DEFAULT

    if cell is CELL_SPACE_EMPTY or cell is CELL_SPACE_HIT or cell is CELL_SHIP_DESTROYED:
        color = Color.GRAY_1
    elif cell is CELL_SHIP_UNIT:
        color = Color.BOLD
    elif cell is CELL_SHIP_DAMAGED:
        color = Color.READ

    print(end=color)
    print(cell, end=' ')
    print(end=Color.DEFAULT)


def print_mark(mark):
    print(end=Color.GRAY_1)
    print(mark, end=' ')
    print(end=Color.DEFAULT)

