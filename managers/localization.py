import enum
from languages import english as language


class Languages(enum.Enum):
    ENGLISH = 1
    RUSSIAN = 2


default_language = Languages.ENGLISH
current_language = default_language


def load_language(language_to_load):
    global language, current_language
    current_language = language_to_load

    if language_to_load is Languages.RUSSIAN:
        from languages import russian as language
    else:
        from languages import english as language
        current_language = default_language


def get_message(message_key):
    return f"[{message_key}]"
