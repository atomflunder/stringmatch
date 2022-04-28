from typing import Optional

from stringmatch.ratio import LevenshteinScorer, Ratio, _Scorer


class Match:
    """Contains methods for comparing and matching strings."""

    def __init__(self, scorer: type[_Scorer] = LevenshteinScorer) -> None:
        """Initialise the Match class with the correct scoring algorithm,
        to be passed along to the Ratio class.

        Parameters
        ----------
        scorer : type[_Scorer], optional
            The scoring algorithm to use, by default LevenshteinScorer
            Available scorers: LevenshteinScorer, JaroScorer, JaroWinklerScorer.
        """
        self.scorer = scorer

    def match(
        self,
        string1: str,
        string2: str,
        *,
        score: int = 70,
        latinise: bool = False,
        ignore_case: bool = False,
        remove_punctuation: bool = False,
        only_letters: bool = False,
    ) -> bool:
        """Matches two strings, returns True if they are similar enough.

        Parameters
        ----------
        string1 : str
            The first string to compare.
        string2 : str
            The second string to compare.
        score : int, optional
            The cutoff for the score, by default 70.
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
        bool
            If the strings are similar enough.
        """
        kwargs = {
            "latinise": latinise,
            "ignore_case": ignore_case,
            "remove_punctuation": remove_punctuation,
            "only_letters": only_letters,
        }

        return Ratio(scorer=self.scorer).ratio(string1, string2, **kwargs) >= score

    def match_with_ratio(
        self,
        string1: str,
        string2: str,
        *,
        score: int = 70,
        latinise: bool = False,
        ignore_case: bool = False,
        remove_punctuation: bool = False,
        only_letters: bool = False,
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
        tuple[bool, int]
            If the strings are similar and their score.
        """
        kwargs = {
            "score": score,
            "latinise": latinise,
            "ignore_case": ignore_case,
            "remove_punctuation": remove_punctuation,
            "only_letters": only_letters,
        }

        return (
            self.match(string1, string2, **kwargs),
            Ratio(scorer=self.scorer).ratio(string1, string2, **kwargs),
        )

    def get_best_match(
        self,
        string: str,
        string_list: list[str],
        *,
        score: int = 70,
        latinise: bool = False,
        ignore_case: bool = False,
        remove_punctuation: bool = False,
        only_letters: bool = False,
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
        Optional[str]
            The best string found, or None if no good match was found.
        """
        kwargs = {
            "score": score,
            "latinise": latinise,
            "remove_punctuation": remove_punctuation,
            "ignore_case": ignore_case,
            "only_letters": only_letters,
        }

        return (
            max(
                string_list,
                key=lambda s: Ratio(scorer=self.scorer).ratio(string, s, **kwargs),
            )
            if any(s for s in string_list if self.match(string, s, **kwargs))
            else None
        )

    def get_best_match_with_ratio(
        self,
        string: str,
        string_list: list[str],
        *,
        score: int = 70,
        latinise: bool = False,
        ignore_case: bool = False,
        remove_punctuation: bool = False,
        only_letters: bool = False,
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
        Optional[tuple[str, int]]
            The best string and its score found, or None if no good match was found.
        """

        kwargs = {
            "score": score,
            "latinise": latinise,
            "remove_punctuation": remove_punctuation,
            "ignore_case": ignore_case,
            "only_letters": only_letters,
        }

        match = self.get_best_match(string, string_list, **kwargs)

        return (
            (match, Ratio(scorer=self.scorer).ratio(string, match, **kwargs))
            if match
            else None
        )

    def get_best_matches(
        self,
        string: str,
        string_list: list[str],
        *,
        score: int = 70,
        limit: Optional[int] = 5,
        latinise: bool = False,
        ignore_case: bool = False,
        remove_punctuation: bool = False,
        only_letters: bool = False,
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
        list[str]
            All of the matches found.
        """
        # we return every match found if the limit is 0 or less
        if limit is not None and limit < 1:
            limit = None

        kwargs = {
            "score": score,
            "latinise": latinise,
            "remove_punctuation": remove_punctuation,
            "ignore_case": ignore_case,
            "only_letters": only_letters,
        }

        return sorted(
            [s for s in string_list if self.match(string, s, **kwargs)],
            key=lambda s: Ratio(scorer=self.scorer).ratio(string, s, **kwargs),
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
        latinise: bool = False,
        ignore_case: bool = False,
        remove_punctuation: bool = False,
        only_letters: bool = False,
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
        list[tuple[str, int]]
            All of the matches found.
        """
        kwargs = {
            "score": score,
            "limit": limit,
            "latinise": latinise,
            "remove_punctuation": remove_punctuation,
            "ignore_case": ignore_case,
            "only_letters": only_letters,
        }

        matches = self.get_best_matches(string, string_list, **kwargs)

        return [
            (match, Ratio(scorer=self.scorer).ratio(string, match, **kwargs))
            for match in matches
        ]
