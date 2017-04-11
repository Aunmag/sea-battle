import settings


def get_message(message_key):
    if settings.language is 'en':
        from languages.language_english import messages
    else:
        from languages.language_russian import messages

    return messages[message_key]
