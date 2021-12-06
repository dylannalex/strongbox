from urllib.parse import urlparse
import mysql.connector
from mysql.connector.connection_cext import CMySQLConnection
from strongbox.database.settings import DATABASE_URL
from strongbox.database.settings import ACCOUNT_TABLE


def connect_to_database() -> CMySQLConnection:
    dbc = urlparse(DATABASE_URL)
    db = mysql.connector.connect(
        host=dbc.hostname,
        user=dbc.username,
        database=dbc.path.lstrip("/"),
        passwd=dbc.password,
    )
    return db


def save_account(
    db: CMySQLConnection,
    name: str,
    username: str,
    mail: str,
    encrypted_password: str,
    vault_id: int,
):
    if not username:
        username = "Null"

    cursor = db.cursor()
    cursor.execute(
        f"INSERT INTO {ACCOUNT_TABLE} VALUES ('{name}', '{username}', '{mail}', '{encrypted_password}', '{vault_id}');"
    )
    db.commit()


def retrieve_all_accounts(db: CMySQLConnection):
    """
    Returns all the accounts from every website/app name.
    """
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM {ACCOUNT_TABLE};")
    return tuple([account for account in cursor])


def retrieve_accounts(db: CMySQLConnection, name: str):
    """
    Returns all the accounts from the given website/app name.
    """
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM {ACCOUNT_TABLE} WHERE name='{name}';")
    return tuple([account for account in cursor])
