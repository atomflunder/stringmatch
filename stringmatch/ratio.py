from typing import List, Tuple, Type

from rapidfuzz.distance import Levenshtein, MatchingBlock

from stringmatch.scorer import BaseScorer, LevenshteinScorer
from stringmatch.strings import Strings


class Ratio:
    """Contains functions for calculating the ratio of similarity between two strings."""

    def __init__(
        self,
        *,
        scorer: Type[BaseScorer] = LevenshteinScorer,
        latinise: bool = False,
        ignore_case: bool = True,
        remove_punctuation: bool = False,
        alphanumeric: bool = False,
        include_partial: bool = False,
    ) -> None:
        """Initialise the Ratio class with the correct parameters.

        Parameters
        ----------
        scorer : Type[BaseScorer], optional
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

        Returns
        -------
        Ratio
            The Ratio class.

        Examples
        --------
        >>> Ratio(latninise=True, scorer=JaroScorer, include_partial=True)
        """
        self.scorer: Type[BaseScorer] = scorer
        self.latinise: bool = latinise
        self.ignore_case: bool = ignore_case
        self.remove_punctuation: bool = remove_punctuation
        self.alphanumeric: bool = alphanumeric
        self.include_partial: bool = include_partial

    def _prepare_strings(self, string1: str, string2: str) -> Tuple[str, str]:
        """Modifies the strings to be ready for comparison, according to the settings.
        Only meant for internal usage, but feel free to use it for something else.

        Parameters
        ----------
        string1 : str
            The first string to modify.
        string2 : str
            The second string to modify.

        Returns
        -------
        Tuple[str, str]
            The two modified strings.

        Examples
        --------
        >>> _prepare_strings("stringmatch", "StrMatch")
        ('stringmatch', 'strmatch')
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

        Examples
        --------
        >>> ratio("stringmatch", "strmatch")
        84
        >>> ratio("stringmatch", "something completely different")
        34
        """
        if self.include_partial:
            return self.partial_ratio(string1, string2)

        # If you happen to pass in a non-string we will just return 0 instead of raising an error.
        # Could happen if you have an incredibly large list of strings and something sneaks in i guess.
        if not all(isinstance(s, str) for s in [string1, string2]):
            return 0

        string1, string2 = self._prepare_strings(string1, string2)

        # If either string is empty after modifying we also wanna return 0.
        if not string1 or not string2:
            return 0

        return round(self.scorer().score(string1, string2))

    def ratio_list(self, string: str, string_list: List[str]) -> List[int]:
        """Returns the similarity score between a string and a list of strings.

        Parameters
        ----------
        string : str
            The string to compare.
        string_list : List[str]
            The list of strings to compare to.

        Returns
        -------
        List[int]
            The scores between 0 and 100.

        Examples
        --------
        >>> ratio_list("stringmatch", ["strmatch", "something completely different"])
        [84, 34]
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

        Examples
        --------
        >>> partial_ratio("test", "This is a test!")
        75
        >>> partial_ratio("word", "The word is in a really, really long string that is pretty different.")
        65
        """
        if not all(isinstance(s, str) for s in [string1, string2]):
            return 0

        string1, string2 = self._prepare_strings(string1, string2)

        if not string1 or not string2:
            return 0

        if len(string1) >= len(string2):
            longer_string, shorter_string = string1, string2
        else:
            longer_string, shorter_string = string2, string1

        blocks: List[MatchingBlock] = [
            block
            for block in Levenshtein.editops(
                longer_string, shorter_string
            ).as_matching_blocks()
            # Doesn't make too much sense to me to match substrings with a length of 1,
            # except when they are at the start of a string, so we filter those out.
            if (block.size > 1 or (block.size == 1 and block.a == 0))
        ]

        # Gets the correct multiplier for the partial ratio.
        # The longer the strings are apart in length, the smaller the multiplier.
        diff: int = len(longer_string) - len(shorter_string)

        multiplier: float = 1.00

        if diff >= 20:
            # Since the default cutoff score is 70, this would not show up on default settings.
            multiplier = 0.65
        elif diff >= 10:
            multiplier = 0.75
        elif diff >= 4:
            multiplier = 0.85
        elif diff >= 1:
            # We want to reserve a score of 100 for perfect matches.
            multiplier = 0.95

        scores: List[int] = []

        for block in blocks:
            start: int = max((block.a - block.b), 0)
            substring: str = longer_string[start : start + len(shorter_string)]

            scores.append(
                round(
                    self.scorer().score(
                        substring,
                        shorter_string,
                    )
                    * multiplier
                ),
            )

        # Also gets the "normal score" for both starting strings,
        # and returns whichever one is higher.
        scores.append(round(self.scorer().score(string1, string2)))

        return max(scores, default=0)
