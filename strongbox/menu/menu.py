from typing import Any, Callable, Union
from cryptography.fernet import Fernet
from mysql.connector.connection_cext import CMySQLConnection
from strongbox.menu import screen
from strongbox import encryption
from strongbox.database import database
from strongbox.menu import settings
from strongbox.menu import style
from strongbox.database import manager
from strongbox.validation.checker import check_vaults_passwords
from mysql.connector.errors import OperationalError


def menu(exit_option: Union[int, None] = None) -> Callable:
    """
    This decorator let you run a function that needs to stablish
    a connection with the database. Every time the database
    connection is lost, wrapped_f renew the session. Any other
    exception that occur are shown to the user.
    """

    def wrap(f: Callable) -> Callable:
        def wrapped_f(*args: Any, **kwargs: Any) -> None:
            db = database.connect_to_database()
            while True:
                try:
                    opt = f(db, *args, **kwargs)
                    if exit_option and exit_option == opt:
                        return

                except OperationalError:
                    screen.display_message("MySQL connection lost. Reconnecting...")
                    db = database.connect_to_database()

                except Exception as error:
                    screen.display_message(str(error))

        return wrapped_f

    return wrap


@menu(4)
def vault_menu(db: CMySQLConnection, fernet: Fernet, vault_id: int) -> None:
    option = screen.get_option(style.VAULT_OPTIONS, settings.VALID_VAULT_OPTIONS)
    if option == 1:
        account = screen.get_account()
        if not account:
            return
        name, mail, username, password = account
        encrypted_password = encryption.encrypt_password(fernet, password)
        database.create_account(db, name, mail, username, encrypted_password, vault_id)

    elif option == 2:
        name = screen.get_website_name()
        if name == "all":
            accounts = database.retrieve_all_accounts(db, vault_id)
        else:
            accounts = database.retrieve_accounts(db, name, vault_id)
        screen.show_accounts(fernet, accounts)

    elif option == 3:
        account_id = screen.get_account_id()
        if not manager.is_valid_account_id(db, vault_id, account_id):
            raise ValueError(f"Account with id={account_id} was not found")
        if not screen.confirm_account_deletion(account_id):
            raise Exception(f"Account with id={account_id} deletion cancelled by user")
        database.delete_account(db, account_id)

    elif option == 4:
        return 4


@menu()
def main_menu(db: CMySQLConnection) -> None:
    option = screen.get_option(style.MAIN_OPTIONS, settings.VALID_MAIN_OPTIONS)
    if option == 1:
        vault_password = screen.get_vault_password()
        if not manager.is_valid_vault_password(db, vault_password):
            if not screen.confirm_vault_creation(vault_password):
                return
            manager.create_vault(db, vault_password)
        vault_id, fernet = manager.connect_to_vault(db, vault_password)
        vault_menu(fernet, vault_id)

    elif option == 2:
        old_vault_password = screen.get_user_input("Enter vault password")
        check_vaults_passwords(db, old_vault_password)
        new_vault_password = screen.get_user_input("Enter new password")
        if not screen.confirm_task(
            "Are you sure you want to change your vault password?"
        ):
            return
        manager.change_vault_password(db, old_vault_password, new_vault_password)

    elif option == 3:
        (
            strong_vault_password,
            weak_vault_password,
            destroy_weak_vault,
        ) = screen.get_vaults_to_merge()
        check_vaults_passwords(db, strong_vault_password, weak_vault_password)

        if not screen.confirm_task("Are you sure you want to merge vaults?"):
            return

        manager.merge_vaults(
            db, strong_vault_password, weak_vault_password, destroy_weak_vault
        )

    elif option == 4:
        vault_password = screen.get_vault_password()
        if not manager.is_valid_vault_password(db, vault_password):
            raise ValueError(f"Invalid vault password: '{vault_password}'")

        _, vault_id = database.retrieve_vault_salt_and_id(
            db, encryption.generate_hash(vault_password)
        )

        if not screen.confirm_vault_deletion(db, vault_id):
            raise Exception(f"Vault with id={vault_id} deletion cancelled by user")

        manager.destroy_vault(db, vault_id)

    elif option == 5:
        screen.show_vaults(db, database.retrieve_vaults(db))
