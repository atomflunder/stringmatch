import Levenshtein  # type: ignore

from stringmatch.scorer import LevenshteinScorer, _Scorer
from stringmatch.strings import Strings


class Ratio:
    """Contains functions for calculating the ratio of similarity between two strings."""

    def __init__(
        self,
        *,
        scorer: type[_Scorer] = LevenshteinScorer,
        latinise: bool = False,
        ignore_case: bool = False,
        remove_punctuation: bool = False,
        only_letters: bool = False,
        include_partial: bool = False,
        **kwargs,
    ) -> None:
        """Initialise the Match class with the correct scoring algorithm,
        to be passed along to the Ratio class.

        Parameters
        ----------
        scorer : type[_Scorer], optional
            The scoring algorithm to use, by default LevenshteinScorer
            Available scorers: LevenshteinScorer, JaroScorer, JaroWinklerScorer.
        latinise : bool, optional
            If special unicode characters should be removed from the strings, by default False.
        ignore_case : bool, optional
            If the strings should be compared ignoring case, by default False.
        remove_punctuation : bool, optional
            If punctuation should be removed from the strings, by default False.
        only_letters : bool, optional
            If the strings should only be compared by their latin letters, by default False.
        include_partial : bool, optional
            If partial substring matches should be included, by default False.
        """
        self.scorer = scorer
        self.latinise = latinise
        self.ignore_case = ignore_case
        self.remove_punctuation = remove_punctuation
        self.only_letters = only_letters
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

        if self.only_letters:
            string1, string2 = Strings().only_letters(string1), Strings().only_letters(
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
        string1, string2 = self._prepare_strings(string1, string2)

        if not string1 or not string2:
            return 0

        # if either string is empty we wanna return 0
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
            if len(long_string) - len(short_string) >= 15:
                # The default score threshold is 70,
                # so if the strings are more than 10 characters apart,
                # this would not show up by default. Also funny number.
                return round(score * 0.69)
            if len(long_string) - len(short_string) >= 9:
                return round(score * 0.75)
            if len(long_string) - len(short_string) >= 4:
                return round(score * 0.85)
            # we dont really want it to return 100, except when its actually identical
            # 95 felt too low, 99 felt too high so i settled upon 97.
            if len(long_string) - len(short_string) >= 1:
                return round(score * 0.97)
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
