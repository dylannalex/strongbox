def valid_int(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


def valid_option(option: str, valid_options: list[int]):
    if not valid_int(option):
        return False

    if not int(option) in valid_options:
        return False

    return True
