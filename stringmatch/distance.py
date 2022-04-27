import Levenshtein


class Distance:
    """Contains functions for calculating the levenshtein distance between strings."""

    def distance(self, string1: str, string2: str) -> int:
        """Returns the levenshtein distance between two strings.

        Parameters
        ----------
        string1 : str
            The first string to compare.
        string2 : str
            The second string to compare.

        Returns
        -------
        int
            The levenshtein distance between the two strings.
        """
        return Levenshtein.distance(string1, string2)

    def distance_list(self, string: str, string_list: list[str]) -> list[int]:
        """Returns the levenshtein distance for a string and a list of strings.

        Parameters
        ----------
        string : str
            The string to compare.
        string_list : list[str]
            The list of strings to compare to.

        Returns
        -------
        list[int]
            The levenshtein distances between the two strings.
        """
        return [self.distance(string, s) for s in string_list]