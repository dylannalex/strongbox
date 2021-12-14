class DifferentPasswordsException(Exception):
    def __init__(self):
        super().__init__("Passwords entered are not equal")


class SpacesException(Exception):
    def __init__(self, item):
        super().__init__(f"{item} cannot have empty spaces")


class EmptyStringException(Exception):
    def __init__(self, item):
        super().__init__(f"{item} cannot be empty")


class InvalidVaultPasswordException(Exception):
    def __init__(self, password):
        super().__init__(f"{password}  is not a valid vault password")
