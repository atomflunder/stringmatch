from typing import Optional

from stringmatch.args import RatioKwargs
from stringmatch.ratio import Ratio
from stringmatch.scorer import LevenshteinScorer, _Scorer


class Match:
    """Contains methods for comparing and matching strings."""

    def __init__(
        self,
        *,
        scorer: type[_Scorer] = LevenshteinScorer,
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
        scorer : type[_Scorer], optional
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

    def match(self, string1: str, string2: str, *, score: int = 70) -> bool:
        """Matches two strings, returns True if they are similar enough.

        Parameters
        ----------
        string1 : str
            The first string to compare.
        string2 : str
            The second string to compare.
        score : int, optional
            The cutoff for the score, by default 70.

        Returns
        -------
        bool
            If the strings are similar enough.
        """
        kwargs: RatioKwargs = {
            "scorer": self.scorer,
            "latinise": self.latinise,
            "ignore_case": self.ignore_case,
            "remove_punctuation": self.remove_punctuation,
            "alphanumeric": self.alphanumeric,
            "include_partial": self.include_partial,
        }

        return Ratio(**kwargs).ratio(string1, string2) >= score

    def match_with_ratio(
        self, string1: str, string2: str, *, score: int = 70
    ) -> tuple[bool, int]:
        """Same as match, but returns the boolean in a tuple, together with the score.

        Parameters
        ----------
        string1 : str
            The first string to compare.
        string2 : str
            The second string to compare.
        score : int, optional
            The cutoff for the score, by default 70.

        Returns
        -------
        tuple[bool, int]
            If the strings are similar and their score.
        """
        kwargs: RatioKwargs = {
            "scorer": self.scorer,
            "score": score,
            "latinise": self.latinise,
            "ignore_case": self.ignore_case,
            "remove_punctuation": self.remove_punctuation,
            "alphanumeric": self.alphanumeric,
            "include_partial": self.include_partial,
        }

        return (
            self.match(string1, string2, score=score),
            Ratio(**kwargs).ratio(string1, string2),
        )

    def get_best_match(
        self, string: str, string_list: list[str], *, score: int = 70
    ) -> Optional[str]:
        """Returns the best match from a list of strings.

        Parameters
        ----------
        string : str
            The string to compare.
        string_list : list[str]
            The list of strings to compare to.
        score : int, optional
            The cutoff for the score, by default 70.

        Returns
        -------
        Optional[str]
            The best string found, or None if no good match was found.
        """
        kwargs: RatioKwargs = {
            "scorer": self.scorer,
            "score": score,
            "latinise": self.latinise,
            "remove_punctuation": self.remove_punctuation,
            "ignore_case": self.ignore_case,
            "alphanumeric": self.alphanumeric,
            "include_partial": self.include_partial,
        }

        return max(
            (s for s in string_list if self.match(string, s, score=score)),
            key=lambda s: (
                # okay so, we first sort this by the ratio, obviously.
                Ratio(**kwargs).ratio(string, s),
                # if the ratio is tied we sort this by the difference in length of the strings.
                # so if you have two strings that are tied in score, the one with the more similar length will win.
                -abs(
                    len(string) - len(s)
                    if all(isinstance(c, str) for c in [s, string])
                    # if a non-string gets input we sort it all the way back.
                    else float("-inf")
                ),
                # then if the length difference happens to be tied as well, we sort by the length of the string.
                # so a longer string will win over the shorter string.
                # the logic here is that if you wanted to get the shorter string, you would input something shorter.
                # so it is more likely that you want the longer of the two strings.
                # this is most likely to trigger for partial matches anyways, so this works fairly well imo.
                len(s) if isinstance(s, str) else float("-inf"),
                # If the length of the string is also tied, it is sorted by the placement of the string in the original list.
                # We could also sort alphabetically or something, but this is better I think.
            ),
            default=None,
        )

    def get_best_match_with_ratio(
        self, string: str, string_list: list[str], *, score: int = 70
    ) -> Optional[tuple[str, int]]:
        """Same as get_best_match, but returns a tuple with the best match and its score.

        Parameters
        ----------
        string : str
            The string to compare.
        string_list : list[str]
            The list of strings to compare to.
        score : int, optional
            The cutoff for the score, by default 70.

        Returns
        -------
        Optional[tuple[str, int]]
            The best string and its score found, or None if no good match was found.
        """

        kwargs: RatioKwargs = {
            "scorer": self.scorer,
            "score": score,
            "latinise": self.latinise,
            "remove_punctuation": self.remove_punctuation,
            "ignore_case": self.ignore_case,
            "alphanumeric": self.alphanumeric,
            "include_partial": self.include_partial,
        }

        match = self.get_best_match(string, string_list, score=score)

        return (match, Ratio(**kwargs).ratio(string, match)) if match else None

    def get_best_matches(
        self,
        string: str,
        string_list: list[str],
        *,
        score: int = 70,
        limit: Optional[int] = 5,
    ) -> list[str]:
        """Matches a string to a list of strings, returns the strings found that are similar.
        If there are more than `limit` matches,
        only the `limit` best matches are returned, sorted by score.
        If no matches are found, returns an empty list.

        Parameters
        ----------
        string : str
            The string to compare.
        string_list : list[str]
            The list of strings to compare to.
        score : int, optional
            The cutoff for the score, by default 70.
        limit : int, optional
            The number of matches to return, by default 5.
            If you want to return every match, set this to 0 (or less than 0) or None.

        Returns
        -------
        list[str]
            All of the matches found.
        """
        # we return every match found if the limit is 0 or less
        if limit is not None and limit < 1:
            limit = None

        kwargs: RatioKwargs = {
            "scorer": self.scorer,
            "score": score,
            "limit": limit,
            "latinise": self.latinise,
            "remove_punctuation": self.remove_punctuation,
            "ignore_case": self.ignore_case,
            "alphanumeric": self.alphanumeric,
            "include_partial": self.include_partial,
        }

        return sorted(
            [s for s in string_list if self.match(string, s, score=score)],
            key=lambda s: (
                Ratio(**kwargs).ratio(string, s),
                -abs(
                    len(string) - len(s)
                    if all(isinstance(c, str) for c in [s, string])
                    else float("-inf")
                ),
                len(s) if isinstance(s, str) else float("-inf"),
            ),
            # by default this would sort the list from lowest to highest.
            reverse=True,
        )[:limit]

    def get_best_matches_with_ratio(
        self,
        string: str,
        string_list: list[str],
        *,
        score: int = 70,
        limit: Optional[int] = 5,
    ) -> list[tuple[str, int]]:
        """Same as get_best_matches, but returns a list of tuples with the best matches and their score.

        Parameters
        ----------
        string : str
            The string to compare.
        string_list : list[str]
            The list of strings to compare to.
        score : int, optional
            The cutoff for the score, by default 70.
        limit : int, optional
            The number of matches to return, by default 5.
            If you want to return every match, set this to 0 (or less than 0) or None.

        Returns
        -------
        list[tuple[str, int]]
            All of the matches found.
        """
        kwargs: RatioKwargs = {
            "scorer": self.scorer,
            "score": score,
            "limit": limit,
            "latinise": self.latinise,
            "remove_punctuation": self.remove_punctuation,
            "ignore_case": self.ignore_case,
            "alphanumeric": self.alphanumeric,
            "include_partial": self.include_partial,
        }

        matches = self.get_best_matches(string, string_list, score=score, limit=limit)

        return [(match, Ratio(**kwargs).ratio(string, match)) for match in matches][
            :limit
        ]
