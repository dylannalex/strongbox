from os import system, urandom
from typing import Union
from prettytable import PrettyTable
from cryptography.fernet import Fernet
from strongbox import encryption
from strongbox.database import database
from strongbox.menu import settings
from strongbox.menu import style
from strongbox.validation import verifier
from strongbox.validation import checker


def create_vault(password) -> bool:
    while True:
        system("cls")
        print(style.TITLE)
        create_vault = (
            input(
                f"No vault with password '{password}' found. Create new vault? (y/n): "
            )
            .strip()
            .lower()
        )
        if create_vault == "y":
            return True

        if create_vault == "n":
            return False


def get_vault_password() -> None:
    system("cls")
    print(style.TITLE)
    return input(" Enter vault password: ").strip()


def get_option(options: str, valid_options: list[int]) -> int:
    while True:
        system("cls")
        print(style.TITLE)
        print(options, end="\n\n")
        option = input(" Insert option: ")
        if verifier.valid_option(option, valid_options):
            return int(option)


def get_account() -> str:
    system("cls")
    print(style.TITLE)
    name = input(" Website/App name:\t").strip().lower()
    username = input(" Username:\t\t").strip().lower()
    mail = input(" Mail:\t\t\t").strip().lower()
    password1 = input(" Password:\t\t").strip()
    password2 = input(" Re-enter password:\t").strip()
    checker.check_account(name, mail, username, password1, password2)
    return name, mail, username, password1


def show_accounts(fernet, accounts) -> None:
    accounts_table = PrettyTable()
    accounts_table.field_names = [
        "Website/App name",
        "Username",
        "Mail",
        "Password",
        "Id",
    ]
    for account in accounts:
        name = account[0]
        mail = account[1]
        username = account[2]
        encrypted_password = bytes(account[3], "utf-8")
        decrypted_password = fernet.decrypt(encrypted_password).decode("utf-8")
        account_id = account[5]
        accounts_table.add_row([name, username, mail, decrypted_password, account_id])
    display_message(str(accounts_table))


def show_vaults(db, vaults) -> None:
    vaults_table = PrettyTable()
    vaults_table.field_names = ["Id", "Total accounts", "Hashed password"]
    for vault in vaults:
        hashed_password = vault[0]
        id = vault[2]
        total_accounts = database.get_total_accounts(db, id)
        vaults_table.add_row([id, total_accounts, hashed_password])
    display_message(str(vaults_table))


def wait() -> None:
    input("Press Enter to continue...")


def display_message(msg: str) -> None:
    system("cls")
    print(style.TITLE)
    for line in msg.split("\n"):
        print(f" {line}")
    print("\n")
    wait()


def delete_vault(db) -> None:
    password = get_vault_password()
    encrypted_password = encryption.generate_hash(password)
    vaults = database.retrieve_vaults(db)
    for vault in vaults:
        if vault[0] == encrypted_password:
            vault_id = vault[2]
            break
    else:
        raise ValueError("Invalid vault password")

    system("cls")
    vault_accounts = database.retrieve_all_accounts(db, vault_id)
    confirmation = (
        input(
            f" Are you sure you want to delete vault with {len(vault_accounts)} accounts? (y/n): "
        )
        .strip()
        .lower()
    )
    if confirmation == "y":
        database.delete_vault(db, vault_id)
        for account in vault_accounts:
            database.delete_account(db, account[-1])


def find_vault_values(db, hashed_password):
    for vault in database.retrieve_vaults(db):
        if vault[0] == hashed_password:
            return vault[1], vault[2]
    else:
        return (None, None)


def get_vault(db) -> Union[tuple[str, str, int], None]:
    password = get_vault_password()
    hashed_password = encryption.generate_hash(password)
    # Check if vault exist:
    vault_salt, vault_id = find_vault_values(db, hashed_password)
    if vault_id:
        encoded_salt = encryption.encode_salt(vault_salt)
        return encryption.generate_key(password, encoded_salt), vault_id

    # Password did not match any vault:
    if create_vault(password):
        encoded_salt = urandom(16)
        decoded_salt = encryption.decode_salt(encoded_salt)
        database.save_vault(db, hashed_password, decoded_salt)
        vault_id = find_vault_values(db, hashed_password)[1]
        return encryption.generate_key(password, encoded_salt), vault_id
    else:
        raise Exception("Action canceled")


def delete_account(db) -> None:
    while True:
        system("cls")
        account_id = input(" Enter account id: ")
        if verifier.valid_int(account_id):
            break

    confirmation = (
        input(f" Are you sure you want to delete account with id={account_id}? (y/n): ")
        .strip()
        .lower()
    )
    if confirmation:
        database.delete_account(db, account_id)


def vault_menu(db, fernet, vault_id) -> None:
    while True:
        try:
            option = get_option(style.VAULT_OPTIONS, settings.VALID_VAULT_OPTIONS)
            if option == 1:
                name, mail, username, password = get_account()
                encrypted_password = encryption.encrypt_password(fernet, password)
                database.save_account(
                    db, name, mail, username, encrypted_password, vault_id
                )
            if option == 2:
                name = input(" Enter website/app name: ").strip().lower()
                accounts = database.retrieve_accounts(db, name, vault_id)
                show_accounts(fernet, accounts)
            if option == 3:
                accounts = database.retrieve_all_accounts(db, vault_id)
                show_accounts(fernet, accounts)
            if option == 4:
                delete_account(db)
            if option == 5:
                return

        except Exception as error:
            display_message(str(error))


def main_menu():
    db = database.connect_to_database()
    option = get_option(style.MAIN_OPTIONS, settings.VALID_MAIN_OPTIONS)
    if option == 1:
        system("cls")
        key, vault_id = get_vault(db)
        fernet = Fernet(key)
        vault_menu(db, fernet, vault_id)
    if option == 2:
        show_vaults(db, database.retrieve_vaults(db))
    if option == 3:
        delete_vault(db)
