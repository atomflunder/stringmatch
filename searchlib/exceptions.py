class EmptySearchException(Exception):
    """Exception that will get raised when you try to compare an empty string to something."""

    pass


class InvalidLimitException(Exception):
    """Exception that will get raised when you try to set a limit that is less than 1."""

    pass
