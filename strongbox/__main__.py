from strongbox.menu import menu


def main():
    while True:
        try:
            menu.main_menu()
        except Exception as error:
            menu.display_message(str(error))


if __name__ == "__main__":
    main()
