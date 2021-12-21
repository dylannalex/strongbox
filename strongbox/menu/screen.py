from os import system
from prettytable import PrettyTable
from strongbox.database import database
from strongbox.menu import style
from strongbox.validation import verifier
from strongbox.validation import checker


### Display information on screen:
def display_on_screen(show_error_message=True, force_input=True):
    def wrap(f):
        def wrapped_f(*args, **kwargs):
            while True:
                system("cls")
                print(style.TITLE)
                try:
                    return f(*args, **kwargs)
                except Exception as error:
                    if show_error_message:
                        display_message(str(error))
                    if not force_input:
                        return

        return wrapped_f

    return wrap


def wait() -> None:
    input("Press Enter to continue...")


@display_on_screen()
def display_message(msg: str) -> None:
    for line in msg.split("\n"):
        print(f" {line}")
    print("\n")
    wait()


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


### Get user confirmation:
@display_on_screen(False)
def confirm_task(confirmation_message: str) -> bool:
    confirmation = input(f" {confirmation_message} (y/n): ").strip().lower()
    if confirmation == "y":
        return True
    elif confirmation == "n":
        return False
    else:
        raise ValueError()


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


### Get user input (password, option, account, account id):
@display_on_screen()
def get_user_input(msg: str):
    return input(f" {msg}: ").strip()


@display_on_screen()
def get_account_id() -> None:
    id = input(" Enter account id: ").strip()
    if not verifier.valid_int(id):
        raise ValueError(f"Invalid id: '{id}'")
    return int(id)


@display_on_screen()
def get_vault_password() -> None:
    return input(" Enter vault password: ").strip()


@display_on_screen(False)
def get_option(options: str, valid_options: list[int]) -> int:
    print(options, end="\n\n")
    option = input(" Insert option: ")
    if verifier.valid_option(option, valid_options):
        return int(option)
    else:
        raise ValueError()


@display_on_screen(True, False)
def get_account() -> str:
    name = input(" Website/App name:\t").strip().lower()
    username = input(" Username:\t\t").strip().lower()
    mail = input(" Mail:\t\t\t").strip().lower()
    password1 = input(" Password:\t\t").strip()
    password2 = input(" Re-enter password:\t").strip()
    checker.check_account(name, mail, username, password1, password2)
    return name, mail, username, password1


@display_on_screen()
def get_website_name() -> str:
    print("\n Enter 'all' for retrieving all websites/apps accounts\n")
    return input(" Enter website/app name: ").strip().lower()


@display_on_screen()
def get_vaults_to_merge() -> str:
    print(" The 'weak' vault will be merged into the 'strong' vault\n")
    weak_vault_password = input(" Enter weak vault password: ").strip()
    strong_vault_password = input(" Enter strong vault password: ").strip()
    destroy_weak_vault = confirm_task(f"Destroy weak vault?")
    return strong_vault_password, weak_vault_password, destroy_weak_vault