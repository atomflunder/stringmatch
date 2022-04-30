import Levenshtein  # type: ignore

from stringmatch.strings import Strings


class _Scorer:
    def score(self, string1: str, string2: str) -> float:
        raise NotImplementedError


class LevenshteinScorer(_Scorer):
    def score(self, string1: str, string2: str) -> float:
        return Levenshtein.ratio(string1, string2)


class JaroScorer(_Scorer):
    def score(self, string1: str, string2: str) -> float:
        return Levenshtein.jaro(string1, string2)


class JaroWinklerScorer(_Scorer):
    def score(self, string1: str, string2: str) -> float:
        return Levenshtein.jaro_winkler(string1, string2)


class Ratio:
    """Contains functions for calculating the ratio of similarity between two strings."""

    def __init__(self, scorer: type[_Scorer] = LevenshteinScorer) -> None:
        """Initialize the Ratio class with the correct scoring algorithm.

        Parameters
        ----------
        scorer : type[_Scorer], optional
            The scoring algorithm to use, by default LevenshteinScorer
            Available scorers: LevenshteinScorer, JaroScorer, JaroWinklerScorer.
        """
        self.scorer = scorer

    def ratio(
        self,
        string1: str,
        string2: str,
        *,
        latinise: bool = False,
        ignore_case: bool = False,
        remove_punctuation: bool = False,
        only_letters: bool = False,
        **kwargs,
    ) -> int:
        """Returns the similarity score between two strings.

        Parameters
        ----------
        string1 : str
            The first string to compare.
        string2 : str
            The second string to compare.
        latinise : bool, optional
            If special unicode characters should be removed from the strings, by default False.
        ignore_case : bool, optional
            If the strings should be compared ignoring case, by default False.
        remove_punctuation : bool, optional
            If punctuation should be removed from the strings, by default False.
        only_letters : bool, optional
            If the strings should only be compared by their latin letters, by default False.

        Returns
        -------
        int
            The score between 0 and 100.
        """
        if latinise:
            string1, string2 = Strings().latinise(string1), Strings().latinise(string2)

        if ignore_case:
            string1, string2 = Strings().ignore_case(string1), Strings().ignore_case(
                string2
            )

        if remove_punctuation:
            string1, string2 = Strings().remove_punctuation(
                string1
            ), Strings().remove_punctuation(string2)

        if only_letters:
            string1, string2 = Strings().only_letters(string1), Strings().only_letters(
                string2
            )

        # if either string is empty we wanna return 0
        return (
            round(self.scorer().score(string1, string2) * 100)
            if string1 and string2
            else 0
        )

    def ratio_list(
        self,
        string: str,
        string_list: list[str],
        *,
        latinise: bool = False,
        ignore_case: bool = False,
        remove_punctuation: bool = False,
        only_letters: bool = False,
    ) -> list[int]:
        """Returns the similarity score between a string and a list of strings.

        Parameters
        ----------
        string : str
            The string to compare.
        string_list : list[str]
            The list of strings to compare to.
        latinise : bool, optional
            If special unicode characters should be removed from the strings, by default False.
        ignore_case : bool, optional
            If the strings should be compared ignoring case, by default False.
        remove_punctuation : bool, optional
            If punctuation should be removed from the strings, by default False.
        only_letters : bool, optional
            If the strings should only be compared by their latin letters, by default False.

        Returns
        -------
        list[int]
            The scores between 0 and 100.
        """
        kwargs = {
            "latinise": latinise,
            "ignore_case": ignore_case,
            "remove_punctuation": remove_punctuation,
            "only_letters": only_letters,
        }

        return [self.ratio(string, s, **kwargs) for s in string_list]
