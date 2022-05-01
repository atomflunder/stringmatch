import Levenshtein  # type: ignore

from stringmatch.args import KeywordArguments
from stringmatch.scorer import LevenshteinScorer, _Scorer
from stringmatch.strings import Strings


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
        include_partial: bool = False,
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
        if include_partial:
            return (
                self.partial_ratio(string1, string2, **kwargs)
                if string1 and string2
                else 0
            )

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
        kwargs: KeywordArguments = {
            "latinise": latinise,
            "ignore_case": ignore_case,
            "remove_punctuation": remove_punctuation,
            "only_letters": only_letters,
        }

        return [self.ratio(string, s, **kwargs) for s in string_list]

    def partial_ratio(
        self,
        string1: str,
        string2: str,
        *,
        latinise: bool = False,
        ignore_case: bool = False,
        remove_punctuation: bool = False,
        only_letters: bool = False,
        **_kwargs,
    ) -> int:
        """Returns the similarity score between subsections of strings.

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
        kwargs: KeywordArguments = {
            "latinise": latinise,
            "ignore_case": ignore_case,
            "remove_punctuation": remove_punctuation,
            "only_letters": only_letters,
        }

        scores = []

        if len(string1) >= len(string2):
            longer_string, shorter_string = string1, string2
        else:
            longer_string, shorter_string = string2, string1

        def partialise_score(long_string: str, short_string: str, score: int):
            """If the two strings are really far away in length, we adjust the similarity score."""
            if len(long_string) - len(short_string) >= 10:
                # The default score threshold is 70,
                # so if the strings are more than 10 characters apart,
                # this will not show up by default.
                return round(score * 0.6)
            elif len(long_string) - len(short_string) >= 5:
                return round(score * 0.8)
            return score

        editops = Levenshtein.editops(longer_string, shorter_string)

        blocks = Levenshtein.matching_blocks(editops, longer_string, shorter_string)

        for block in blocks:
            longer_string_start = max(block[1] - block[0], 0)
            longer_string_end = longer_string_start + len(shorter_string)
            longer_string_substring = longer_string[
                longer_string_start:longer_string_end
            ]

            scores.append(
                partialise_score(
                    longer_string,
                    shorter_string,
                    self.ratio(longer_string_substring, shorter_string, **kwargs),
                )
            )

        max_partial = max(scores, default=0)

        # we will return the higher of the two scores, just in case
        return max(max_partial, self.ratio(string1, string2, **kwargs))
