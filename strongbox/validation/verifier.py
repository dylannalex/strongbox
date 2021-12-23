def valid_int(string: str) -> bool:
    try:
        int(string)
        return True
    except ValueError:
        return False


def valid_option(option: str, valid_options: list[int]) -> bool:
    if not valid_int(option):
        return False

    if not int(option) in valid_options:
        return False

    return True
