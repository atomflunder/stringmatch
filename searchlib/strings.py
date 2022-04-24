from unidecode import unidecode


class Strings:
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
            c for c in string if c not in "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
        )
