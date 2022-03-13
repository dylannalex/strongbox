from strongbox.menu import menu
from strongbox.database.database import connect_to_database


def main() -> None:
    db = connect_to_database()
    menu.main_menu(db)


if __name__ == "__main__":
    main()
