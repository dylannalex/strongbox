from strongbox.validation import exceptions


SPACE = " "


def _check_passwords(password1, password2):
    if password1 != password2:
        raise exceptions.DifferentPasswordsException


def _check_spaces(mail, username, password):
    if SPACE in mail:
        raise exceptions.SpacesException("mail")

    if SPACE in username:
        raise exceptions.SpacesException("username")

    if SPACE in password:
        raise exceptions.SpacesException("password")


def _check_empty(name, mail, password):
    if len(name) == 0:
        raise exceptions.EmptyStringException("name")

    if len(mail) == 0:
        raise exceptions.EmptyStringException("mail")

    if len(password) == 0:
        raise exceptions.EmptyStringException("password")


def check_account(name, mail, username, password1, password2):
    _check_empty(name, mail, password1)
    _check_spaces(mail, username, password1)
    _check_passwords(password1, password2)
