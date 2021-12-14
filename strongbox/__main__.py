from strongbox.menu import menu
from strongbox.menu.screen import display_message
from strongbox.database.database import connect_to_database


def main():
    db = connect_to_database()
    while True:
        try:
            menu.main_menu(db)
        except Exception as error:
            display_message(str(error))


if __name__ == "__main__":
    main()
