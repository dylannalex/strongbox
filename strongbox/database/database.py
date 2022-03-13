from urllib.parse import urlparse
import mysql.connector
from mysql.connector.connection import MySQLConnection
from strongbox.database.settings import DATABASE_URL, VAULT_TABLE
from strongbox.database.settings import ACCOUNT_TABLE


def connect_to_database() -> MySQLConnection:
    dbc = urlparse(DATABASE_URL)
    db = mysql.connector.connect(
        host=dbc.hostname,
        user=dbc.username,
        database=dbc.path.lstrip("/"),
        passwd=dbc.password,
    )
    return db


def create_account(
    db: MySQLConnection,
    name: str,
    username: str,
    mail: str,
    encrypted_password: str,
    vault_id: int,
) -> None:
    if not username:
        username = "Null"
    cursor = db.cursor()
    cursor.execute(
        f"INSERT INTO {ACCOUNT_TABLE} VALUES ('{name}', '{username}', '{mail}', '{encrypted_password}', '{vault_id}', 0);"
    )
    db.commit()


def retrieve_all_accounts(
    db: MySQLConnection, vault_id: int
) -> list[tuple[str, str, str, str, int, int]]:
    """
    Returns all the accounts from every website/app name.
    """
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM {ACCOUNT_TABLE} WHERE vault_id='{vault_id}';")
    return tuple([account for account in cursor])


def retrieve_accounts(
    db: MySQLConnection, name: str, vault_id: int
) -> list[tuple[str, str, str, str, int, int]]:
    """
    Returns all the accounts from the given website/app name.
    """
    cursor = db.cursor()
    cursor.execute(
        f"SELECT * FROM {ACCOUNT_TABLE} WHERE name='{name}' AND vault_id='{vault_id}';"
    )
    return tuple([account for account in cursor])


def delete_account(db: MySQLConnection, account_id: int) -> None:
    cursor = db.cursor()
    cursor.execute(f"DELETE FROM {ACCOUNT_TABLE} WHERE account_id='{account_id}';")
    db.commit()


def get_total_accounts(db: MySQLConnection, vault_id: int) -> int:
    return len(retrieve_all_accounts(db, vault_id))


def create_vault(db: MySQLConnection, encrypted_password: str, salt: str) -> None:
    cursor = db.cursor()
    cursor.execute(
        f"INSERT INTO {VAULT_TABLE} VALUES ('{encrypted_password}', '{salt}', 0);"
    )
    db.commit()


def retrieve_vaults(db: MySQLConnection) -> list[tuple[str, str, int]]:
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM {VAULT_TABLE};")
    return tuple([account for account in cursor])


def retrieve_vault_salt_and_id(
    db: MySQLConnection, hashed_password: str
) -> tuple[str, int]:
    """
    Returns the salt and id of a vault given it's password.

    get_vault_salt_and_id(db, "vault1_password")
    >>> ("vault1_salt", vault1_id)
    """
    for vault in retrieve_vaults(db):
        if vault[0] == hashed_password:
            return vault[1], vault[2]
    else:
        return (None, None)


def delete_vault(db: MySQLConnection, vault_id: int) -> None:
    cursor = db.cursor()
    cursor.execute(f"DELETE FROM {VAULT_TABLE} WHERE id='{vault_id}';")
    db.commit()
