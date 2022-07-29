from typing import List, Optional, Tuple, Type

from stringmatch.ratio import Ratio
from stringmatch.scorer import BaseScorer, LevenshteinScorer


class Match:
    """Contains methods for comparing and matching strings."""

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
        """Initialise the Match class with the given parameters.

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
        Match
            The Match class.

        Examples
        --------
        >>> Match(latninise=True, scorer=JaroScorer, include_partial=True)
        """
        self.scorer: Type[BaseScorer] = scorer
        self.latinise: bool = latinise
        self.ignore_case: bool = ignore_case
        self.remove_punctuation: bool = remove_punctuation
        self.alphanumeric: bool = alphanumeric
        self.include_partial: bool = include_partial

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

        Examples
        --------
        >>> match("stringmatch", "strmatch")
        True
        >>> match("stringmatch", "something different")
        False
        """
        return self.match_with_ratio(string1, string2, score=score)[0]

    def match_with_ratio(
        self, string1: str, string2: str, *, score: int = 70
    ) -> Tuple[bool, int]:
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
        Tuple[bool, int]
            If the strings are similar and their score.

        Examples
        --------
        >>> match_with_ratio("stringmatch", "strmatch")
        (True, 84)
        >>> match_with_ratio("stringmatch", "something different")
        (False, 40)
        """
        r: int = Ratio(
            scorer=self.scorer,
            latinise=self.latinise,
            ignore_case=self.ignore_case,
            remove_punctuation=self.remove_punctuation,
            alphanumeric=self.alphanumeric,
            include_partial=self.include_partial,
        ).ratio(string1, string2)

        return (r >= score, r)

    def get_best_match(
        self, string: str, string_list: List[str], *, score: int = 70
    ) -> Optional[str]:
        """Returns the best match from a list of strings.

        Parameters
        ----------
        string : str
            The string to compare.
        string_list : List[str]
            The List of strings to compare to.
        score : int, optional
            The cutoff for the score, by default 70.

        Returns
        -------
        Optional[str]
            The best string found, or None if no good match was found.

        Examples
        --------
        >>> get_best_match("stringmatch", ["strmatch", "test", "something else"])
        'strmatch'
        """
        match: Optional[Tuple[str, int]] = self.get_best_match_with_ratio(
            string, string_list, score=score
        )

        return match[0] if match else None

    def get_best_match_with_ratio(
        self, string: str, string_list: List[str], *, score: int = 70
    ) -> Optional[Tuple[str, int]]:
        """Same as get_best_match, but returns a tuple with the best match and its score.

        Parameters
        ----------
        string : str
            The string to compare.
        string_list : List[str]
            The List of strings to compare to.
        score : int, optional
            The cutoff for the score, by default 70.

        Returns
        -------
        Optional[tuple[str, int]]
            The best string and its score found, or None if no good match was found.

        Examples
        --------
        >>> get_best_match_with_ratio("stringmatch", ["strmatch", "test", "something else"])
        ('strmatch', 84)
        """
        ratio: Ratio = Ratio(
            scorer=self.scorer,
            latinise=self.latinise,
            remove_punctuation=self.remove_punctuation,
            ignore_case=self.ignore_case,
            alphanumeric=self.alphanumeric,
            include_partial=self.include_partial,
        )

        matches: List[Tuple[str, int]] = sorted(
            # We only add the entry to the list if the ratio is above the cutoff score.
            [(s, r) for s in string_list if (r := ratio.ratio(string, s)) >= score],
            key=lambda x: (
                # We first sort the list by the score.
                x[1],
                # Then we sort the list by the character difference.
                -abs(
                    len(string) - len(x[0])
                    if all(isinstance(c, str) for c in [x[0], string])
                    else float("-inf")
                ),
                # And lastly we sort it by the length of the string.
                len(x[0]) if isinstance(x[0], str) else float("-inf"),
                # If all of these are tied, the list is sorted by order of how they appear in the original list.
            ),
            reverse=True,
        )

        return (matches[0]) if matches else None

    def get_best_matches(
        self,
        string: str,
        string_list: List[str],
        *,
        score: int = 70,
        limit: Optional[int] = 5,
    ) -> List[str]:
        """Matches a string to a list of strings, returns the strings found that are similar.
        If there are more than `limit` matches,
        only the `limit` best matches are returned, sorted by score.
        If no matches are found, returns an empty list.

        Parameters
        ----------
        string : str
            The string to compare.
        string_list : List[str]
            The List of strings to compare to.
        score : int, optional
            The cutoff for the score, by default 70.
        limit : int, optional
            The number of matches to return, by default 5.
            If you want to return every match, set this to 0 (or less than 0) or None.

        Returns
        -------
        List[str]
            All of the matches found.

        Examples
        --------
        >>> get_best_matches("stringmatch", ["strmatch", "stringmatch", "test", "something else"])
        ['stringmatch', 'strmatch']
        """
        # We return every match found if the limit is 0 or less.
        if limit is not None and limit < 1:
            limit = None

        return [
            # We only return the string without the score.
            m[0]
            for m in self.get_best_matches_with_ratio(
                string, string_list, score=score, limit=limit
            )
        ]

    def get_best_matches_with_ratio(
        self,
        string: str,
        string_list: List[str],
        *,
        score: int = 70,
        limit: Optional[int] = 5,
    ) -> List[Tuple[str, int]]:
        """Same as get_best_matches, but returns a list of tuples with the best matches and their score.

        Parameters
        ----------
        string : str
            The string to compare.
        string_list : List[str]
            The List of strings to compare to.
        score : int, optional
            The cutoff for the score, by default 70.
        limit : int, optional
            The number of matches to return, by default 5.
            If you want to return every match, set this to 0 (or less than 0) or None.

        Returns
        -------
        List[tuple[str, int]]
            All of the matches found.

        Examples
        --------
        >>> get_best_matches_with_ratio("stringmatch", ["strmatch", "stringmatch", "test", "something else"])
        [('stringmatch', 100), ('strmatch', 84)]
        """
        if limit is not None and limit < 1:
            limit = None

        ratio: Ratio = Ratio(
            scorer=self.scorer,
            latinise=self.latinise,
            remove_punctuation=self.remove_punctuation,
            ignore_case=self.ignore_case,
            alphanumeric=self.alphanumeric,
            include_partial=self.include_partial,
        )

        # This is the same sorting as in the get_best_match_with_ratio function.
        return sorted(
            [(s, r) for s in string_list if (r := ratio.ratio(string, s)) >= score],
            key=lambda x: (
                x[1],
                -abs(
                    len(string) - len(x[0])
                    if all(isinstance(c, str) for c in [x[0], string])
                    else float("-inf")
                ),
                len(x[0]) if isinstance(x[0], str) else float("-inf"),
            ),
            reverse=True,
        )[:limit]
