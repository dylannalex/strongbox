from os import system
from prettytable import PrettyTable
from strongbox import encryption
from strongbox.database import database
from strongbox.menu import settings
from strongbox.menu import style
from strongbox.validation import verifier
from strongbox.validation import checker
from strongbox.database import manager


### Functions to get user confirmation:
def confirm_task(confirmation_message: str) -> bool:
    while True:
        system("cls")
        print(style.TITLE)
        confirmation = input(f" {confirmation_message} (y/n): ").strip().lower()
        if confirmation == "y":
            return True
        if confirmation == "n":
            return False


def confirm_vault_creation(password) -> bool:
    return confirm_task(f"No vault with password '{password}' found. Create new vault?")


def confirm_vault_deletion(db, vault_id):
    vault_accounts = database.retrieve_all_accounts(db, vault_id)
    return confirm_task(
        f"Are you sure you want to delete vault with {len(vault_accounts)} accounts?"
    )


def confirm_account_deletion(account_id):
    return confirm_task(
        f"Are you sure you want to delete account with id={account_id}?"
    )


### Functions to get user input (password, option, account, account id):
def get_account_id() -> None:
    system("cls")
    print(style.TITLE)
    id = input(" Enter account id: ").strip()
    if not verifier.valid_int(id):
        raise ValueError(f"Invalid id: '{id}'")
    return int(id)


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


def get_website_name() -> str:
    system("cls")
    print(style.TITLE)
    print("\n Enter 'all' for retrieving all websites/apps accounts")
    return input(" Enter website/app name: ").strip().lower()


### Functions to display information on screen:
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


### Menus:
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

            elif option == 2:
                name = get_website_name()
                if name == "all":
                    accounts = database.retrieve_all_accounts(db, vault_id)
                else:
                    accounts = database.retrieve_accounts(db, name, vault_id)
                show_accounts(fernet, accounts)

            elif option == 3:
                account_id = get_account_id()
                if not manager.is_valid_account_id(db, vault_id, account_id):
                    raise ValueError(f"Account with id={account_id} was not found")
                if not confirm_account_deletion(account_id):
                    raise Exception(
                        f"Account with id={account_id} deletion cancelled by user"
                    )
                database.delete_account(db, account_id)

            elif option == 4:
                return

        except Exception as error:
            display_message(str(error))


def main_menu():
    db = database.connect_to_database()
    option = get_option(style.MAIN_OPTIONS, settings.VALID_MAIN_OPTIONS)
    if option == 1:
        vault_password = get_vault_password()
        if not manager.is_valid_vault_password(db, vault_password):
            if not confirm_vault_creation(vault_password):
                return
            manager.create_vault(db, vault_password)
        vault_id, fernet = manager.connect_to_vault(db, vault_password)
        vault_menu(db, fernet, vault_id)

    elif option == 2:
        show_vaults(db, database.retrieve_vaults(db))

    elif option == 3:
        vault_password = get_vault_password()
        if not manager.is_valid_vault_password(db, vault_password):
            raise ValueError(f"Invalid vault password: '{vault_password}'")

        _, vault_id = database.retrieve_vault_salt_and_id(
            db, encryption.generate_hash(vault_password)
        )

        if not confirm_vault_deletion(db, vault_id):
            raise Exception(f"Vault with id={vault_id} deletion cancelled by user")

        manager.destroy_vault(db, vault_id)
