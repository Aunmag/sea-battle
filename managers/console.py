import os

import constants
from managers import localization


def press_enter(message=None, message_action=None):
    if message_action is None:
        message_action = localization.language.to_continue

    message_press_enter = localization.language.press_enter
    message_press_enter = f"{message_press_enter} {message_action}... "

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
        heading = localization.language.choices

    message = f"### {heading}:"

    for number, choice in enumerate(choices):
        snipped = f"\n {number + 1}. {choice}"
        message += snipped

    message += "\n\n" + localization.language.chose_action + ": "

    input_value = input(message)
    input_value = validate_input(input_value, len(choices))
    return input_value


def validate_integer(value):
    try:
        value = int(value)
    except ValueError:
        print(localization.language.have_to_enter_integers)
        return constants.Console.WRONG_INPUT
    else:
        return value


def validate_input(value, choices_quantity):
    value = validate_integer(value)

    if value is constants.Console.WRONG_INPUT:
        press_enter()
        return constants.Console.WRONG_INPUT
    elif 0 < value <= choices_quantity:
        return value
    else:
        message = localization.language.chose_between.format(choices_quantity, value)
        press_enter(message=message)
        return constants.Console.WRONG_INPUT


def validate_input_coordinate(value, board_size):
    value = validate_integer(value)

    if value is constants.Console.WRONG_INPUT:
        return constants.Console.WRONG_INPUT
    elif 0 <= value < board_size:
        return value
    else:
        print(localization.language.location_too_far)
        return constants.Console.WRONG_INPUT


def validate_iteration_number(value):
    if value == constants.ITERATION_LIMIT:
        message = f"Iteration number exceeded. Limit is {constants.ITERATION_LIMIT}."
        raise OverflowError(message)

    return value + 1
