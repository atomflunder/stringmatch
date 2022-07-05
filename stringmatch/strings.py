from unidecode import unidecode  # type: ignore


class Strings:
    """Modifies the strings to the desired format."""

    def latinise(self, string: str) -> str:
        """Removes special unicode characters from the string.

        Parameters
        ----------
        string : str
            The string to remove special unicode characters from.

        Returns
        -------
        str
            The string with special unicode characters removed.
        """
        return unidecode(string)

    def remove_punctuation(self, string: str) -> str:
        """Removes punctuation from a string.

        Parameters
        ----------
        string : str
            The string to remove punctuation from.

        Returns
        -------
        str
            The string with punctuation removed.
        """
        return "".join(
            c for c in string if c not in "!\"#'()*+,-./:;<=>?[]^_`{|}~’„“»«"
        )

    def alphanumeric(self, string: str) -> str:
        """Removes all non-latin letters from the string.
        Does also keep numbers.
        A more extreme version of remove_punctuation().

        Parameters
        ----------
        string : str
            The string to remove non-latin letters from.

        Returns
        -------
        str
            The string with non-latin letters removed.
        """
        return "".join(
            c
            for c in string
            if c in "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ "
        )

    def ignore_case(self, string: str, lower: bool = True) -> str:
        """Removes case from a string.

        Parameters
        ----------
        string : str
            The string to remove case from.
        lower : bool, optional
            If to convert the string to all lower case, by default True.
            If set to False, converts it to all upper case.

        Returns
        -------
        str
            The string with case removed.
        """
        return string.lower() if lower else string.upper()
