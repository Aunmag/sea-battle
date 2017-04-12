import os

from constants import *


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


def raise_wrong_axis_direction(axis_direction):
    raise ValueError(f"Got wrong axis direction {axis_direction}.")


def raise_wrong_hit_status(hit_status, x=None, y=None, details=None):
    message = f"Got wrong hit status {hit_status}."

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


def validate_iteration_number(value):
    if value == ITERATION_LIMIT:
        raise OverflowError(f"Iteration number exceeded. Limit is {ITERATION_LIMIT}.")

    return value + 1
