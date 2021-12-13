from os import urandom
from cryptography.fernet import Fernet
from mysql.connector.connection_cext import CMySQLConnection
from strongbox import encryption
from strongbox.database import database


def is_valid_account_id(db, vault_id, account_id) -> bool:
    """
    Returns True if matches the given account_id with a created
    account, else returns False.
    """
    for account in database.retrieve_all_accounts(db, vault_id):
        if account[-1] == account_id:
            return True
    return False


def is_valid_vault_password(db: CMySQLConnection, vault_password: str) -> bool:
    """
    Returns True if matches the given vault_password with a created
    vault, else returns False.
    """
    hashed_password = encryption.generate_hash(vault_password)
    for vault in database.retrieve_vaults(db):
        if vault[0] == hashed_password:
            return True

    return False


def create_vault(db: CMySQLConnection, vault_password: str) -> None:
    encoded_salt = urandom(16)
    decoded_salt = encryption.decode_salt(encoded_salt)
    hashed_password = encryption.generate_hash(vault_password)
    database.create_vault(db, hashed_password, decoded_salt)


def connect_to_vault(db: CMySQLConnection, vault_password: str) -> tuple[int, Fernet]:
    """
    Given the database and a vault password, returns the vault id and a fernet
    object generating with the corresponding vault key (generated from vault
    password).
    """
    hashed_password = encryption.generate_hash(vault_password)
    salt, vault_id = database.retrieve_vault_salt_and_id(db, hashed_password)
    encoded_salt = encryption.encode_salt(salt)
    key = encryption.generate_key(vault_password, encoded_salt)
    fernet = Fernet(key)
    return vault_id, fernet


def create_accounts(
    db: CMySQLConnection, accounts: list[tuple[str, str, str, str]], vault_password: str
) -> None:
    """
    Saves a given list of accounts on the database. Accounts must be passed
    as a list tuple:
    accounts = [
        ("website1", "example1@gmail.com", "username1", "password123"),
        ("website2", "example2@gmail.com", "username2", "password456"),
        ("website3", "example3@gmail.com", "username3", "password789")
    ]
    """
    vault_id, fernet = connect_to_vault(db, vault_password)
    for account in accounts:
        name = account[0]
        mail = account[1]
        username = account[2]
        encrypted_password = encryption.encrypt_password(fernet, account[3])
        database.create_account(db, name, mail, username, encrypted_password, vault_id)


def destroy_vault(db, vault_id):
    database.delete_vault(db, vault_id)
    for account in database.retrieve_all_accounts(db, vault_id):
        database.delete_account(db, account[-1])
