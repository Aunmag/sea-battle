import os


def press_enter():
    input("Press Enter key to continue... ")


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
