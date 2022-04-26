import Levenshtein

from stringmatch.exceptions import InvalidScorerException


class Ratio:
    """Contains functions for calculating the ratio of similarity between two strings."""

    def __init__(self):
        self.scorers = {
            "levenshtein": Levenshtein.ratio,
            "jaro": Levenshtein.jaro,
            "jaro_winkler": Levenshtein.jaro_winkler,
        }

    def ratio(self, string1: str, string2: str, scorer: str = "levenshtein") -> int:
        """Returns the similarity score between two strings.

        Parameters
        ----------
        string1 : str
            The first string to compare.
        string2 : str
            The second string to compare.
        scorer : str, optional
            The scorer to use, by default "levenshtein".
            Available scorers:
                "levenshtein"
                "jaro"
                "jaro_winkler"


        Returns
        -------
        int
            The score between 0 and 100.
        """

        if scorer not in self.scorers:
            raise InvalidScorerException("Scorer not in available scorers.")

        return round(self.scorers[scorer](string1, string2) * 100)

    def ratio_list(
        self, string: str, string_list: list[str], scorer: str = "levenshtein"
    ) -> list[int]:
        """Returns the similarity score between a string and a list of strings.

        Parameters
        ----------
        string : str
            The string to compare.
        string_list : list[str]
            The list of strings to compare to.
        scorer : str, optional
            The scorer to use, by default "levenshtein".
            Available scorers:
                "levenshtein"
                "jaro"
                "jaro_winkler"

        Returns
        -------
        list[int]
            The scores between 0 and 100.
        """
        if scorer not in self.scorers:
            raise InvalidScorerException("Scorer not in available scorers.")

        return [self.ratio(string, s, scorer=scorer) for s in string_list]
