import Levenshtein


class Ratio:
    """Contains functions for calculating the ratio of similarity between two strings."""

    def __init__(self, scorer: str = "levenshtein") -> None:
        """Initialize the Ratio class with the correct scoring algorithm.

        Parameters
        ----------
        scorer : str, optional
            _description_, by default "levenshtein"
        """
        self.available_scorers = {
            "levenshtein": Levenshtein.ratio,
            "jaro": Levenshtein.jaro,
            "jaro_winkler": Levenshtein.jaro_winkler,
        }

        # if the scorer is not found, use levenshtein as the default.
        self.scorer = self.available_scorers.get(scorer, Levenshtein.ratio)

    def ratio(self, string1: str, string2: str) -> int:
        """Returns the similarity score between two strings.

        Parameters
        ----------
        string1 : str
            The first string to compare.
        string2 : str
            The second string to compare.


        Returns
        -------
        int
            The score between 0 and 100.
        """

        # if either string is empty we wanna return 0
        return round(self.scorer(string1, string2) * 100) if string1 and string2 else 0

    def ratio_list(self, string: str, string_list: list[str]) -> list[int]:
        """Returns the similarity score between a string and a list of strings.

        Parameters
        ----------
        string : str
            The string to compare.
        string_list : list[str]
            The list of strings to compare to.

        Returns
        -------
        list[int]
            The scores between 0 and 100.
        """
        return [self.ratio(string, s) for s in string_list]
