import Levenshtein  # type: ignore

from stringmatch.scorer import BaseScorer, LevenshteinScorer
from stringmatch.strings import Strings


class Ratio:
    """Contains functions for calculating the ratio of similarity between two strings."""

    def __init__(
        self,
        *,
        scorer: type[BaseScorer] = LevenshteinScorer,
        latinise: bool = False,
        ignore_case: bool = True,
        remove_punctuation: bool = False,
        alphanumeric: bool = False,
        include_partial: bool = False,
        **kwargs,
    ) -> None:
        """Initialise the Match class with the correct scoring algorithm,
        to be passed along to the Ratio class.

        Parameters
        ----------
        scorer : type[BaseScorer], optional
            The scoring algorithm to use, by default LevenshteinScorer
            Available scorers: LevenshteinScorer, JaroScorer, JaroWinklerScorer.
        latinise : bool, optional
            If special unicode characters should be removed from the strings, by default False.
        ignore_case : bool, optional
            If the strings should be compared ignoring case, by default True.
        remove_punctuation : bool, optional
            If punctuation should be removed from the strings, by default False.
        alphanumeric : bool, optional
            If the strings should only be compared by their latin letters, by default False.
        include_partial : bool, optional
            If partial substring matches should be included, by default False.
        """
        self.scorer = scorer
        self.latinise = latinise
        self.ignore_case = ignore_case
        self.remove_punctuation = remove_punctuation
        self.alphanumeric = alphanumeric
        self.include_partial = include_partial

    def _prepare_strings(self, string1: str, string2: str) -> tuple[str, str]:
        """Modifies the strings to be ready for comparison, according to the settings.
        Only meant for internal usage.
        """
        if self.latinise:
            string1, string2 = Strings().latinise(string1), Strings().latinise(string2)

        if self.ignore_case:
            string1, string2 = Strings().ignore_case(string1), Strings().ignore_case(
                string2
            )

        if self.remove_punctuation:
            string1, string2 = Strings().remove_punctuation(
                string1
            ), Strings().remove_punctuation(string2)

        if self.alphanumeric:
            string1, string2 = Strings().alphanumeric(string1), Strings().alphanumeric(
                string2
            )

        return (string1, string2)

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
        # if you happen to pass in a non-string we will just return 0 instead of raising an error
        # could happen if you have an incredibly large list of strings and something sneaks in i guess
        if not all(isinstance(s, str) for s in [string1, string2]):
            return 0

        string1, string2 = self._prepare_strings(string1, string2)

        # if either string is empty after modifying we wanna return 0
        if not string1 or not string2:
            return 0

        if self.include_partial:
            return self.partial_ratio(string1, string2)

        return round(self.scorer().score(string1, string2) * 100)

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

    def partial_ratio(self, string1: str, string2: str) -> int:
        """Returns the similarity score between subsections of strings.

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
        string1, string2 = self._prepare_strings(string1, string2)

        if not string1 or not string2:
            return 0

        scores = []

        if len(string1) >= len(string2):
            longer_string, shorter_string = string1, string2
        else:
            longer_string, shorter_string = string2, string1

        def partialise_score(long_string: str, short_string: str, score: int):
            """If the two strings are really far away in length, we adjust the similarity score."""
            if len(long_string) - len(short_string) >= 20:
                # The default score threshold is 70,
                # so this would not show up by default.
                return round(score * 0.65)
            if len(long_string) - len(short_string) >= 10:
                return round(score * 0.75)
            if len(long_string) - len(short_string) >= 4:
                return round(score * 0.85)
            if len(long_string) - len(short_string) >= 1:
                # we dont really want it to return 100, except when its actually identical
                return round(score * 0.95)
            return score

        editops = Levenshtein.editops(longer_string, shorter_string)

        blocks = Levenshtein.matching_blocks(editops, longer_string, shorter_string)

        for block in blocks:
            # doesnt make too much sense to me to match substrings with a length of 1
            # except when they are at the start of a string.
            if block[2] > 1 or (block[2] == 1 and block[0] == 0):
                longer_string_start = max((block[0] - block[1]), 0)
                longer_string_end = longer_string_start + len(shorter_string)
                longer_string_substring = longer_string[
                    longer_string_start:longer_string_end
                ]

                scores.append(
                    partialise_score(
                        longer_string,
                        shorter_string,
                        round(
                            self.scorer().score(longer_string_substring, shorter_string)
                            * 100
                        ),
                    )
                )

        # also gets the "normal score" for both starting strings,
        # and returns whichever one is higher.
        scores.append(round(self.scorer().score(string1, string2) * 100))

        return max(scores, default=0)
