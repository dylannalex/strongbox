from strongbox.menu import menu
from strongbox.menu.screen import display_message


def main():
    while True:
        try:
            menu.main_menu()
        except Exception as error:
            display_message(str(error))


if __name__ == "__main__":
    main()
