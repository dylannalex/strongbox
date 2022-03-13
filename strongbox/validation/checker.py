from mysql.connector.connection import MySQLConnection
from strongbox.database.manager import is_valid_vault_password
from strongbox.validation import exceptions


SPACE = " "


def _check_passwords(password1: str, password2: str) -> None:
    if password1 != password2:
        raise exceptions.DifferentPasswordsException


def _check_spaces(mail: str, username: str, password: str) -> None:
    if SPACE in mail:
        raise exceptions.SpacesException("mail")

    if SPACE in username:
        raise exceptions.SpacesException("username")

    if SPACE in password:
        raise exceptions.SpacesException("password")


def _check_empty(name: str, mail: str, password: str) -> None:
    if len(name) == 0:
        raise exceptions.EmptyStringException("name")

    if len(mail) == 0:
        raise exceptions.EmptyStringException("mail")

    if len(password) == 0:
        raise exceptions.EmptyStringException("password")


def check_account(
    name: str, mail: str, username: str, password1: str, password2: str
) -> None:
    _check_empty(name, mail, password1)
    _check_spaces(mail, username, password1)
    _check_passwords(password1, password2)


def check_vaults_passwords(db: MySQLConnection, *args: str) -> None:
    for vault_password in args:
        if not is_valid_vault_password(db, vault_password):
            raise exceptions.InvalidVaultPasswordException(vault_password)
