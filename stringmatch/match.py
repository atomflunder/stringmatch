from typing import Optional

from stringmatch.ratio import Ratio
from stringmatch.strings import Strings


class Match:
    """Contains methods for comparing and matching strings."""

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
        scorer: str = "levenshtein",
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
        scorer : str, optional
            The scorer to use, by default "levenshtein".
            Available scorers:
                "levenshtein",
                "jaro",
                "jaro_winkler".

        Returns
        -------
        bool
            If the strings are similar enough.
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

        return Ratio().ratio(string1, string2, scorer=scorer) >= score

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
        scorer: str = "levenshtein",
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
        scorer : str, optional
            The scorer to use, by default "levenshtein".
            Available scorers:
                "levenshtein",
                "jaro",
                "jaro_winkler".

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
            "scorer": scorer,
        }

        return (
            self.match(string1, string2, **kwargs),
            Ratio().ratio(string1, string2, scorer=scorer),
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
        scorer: str = "levenshtein",
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
        scorer : str, optional
            The scorer to use, by default "levenshtein".
            Available scorers:
                "levenshtein",
                "jaro",
                "jaro_winkler".

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
            "scorer": scorer,
        }

        return (
            max(string_list, key=lambda s: Ratio().ratio(string, s, scorer=scorer))
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
        scorer: str = "levenshtein",
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
        scorer : str, optional
            The scorer to use, by default "levenshtein".
            Available scorers:
                "levenshtein",
                "jaro",
                "jaro_winkler".

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
            "scorer": scorer,
        }

        match = self.get_best_match(string, string_list, **kwargs)

        return (match, Ratio().ratio(string, match, scorer=scorer)) if match else None

    def get_best_matches(
        self,
        string: str,
        string_list: list[str],
        *,
        score: int = 70,
        limit: int = 5,
        latinise: bool = False,
        ignore_case: bool = False,
        remove_punctuation: bool = False,
        only_letters: bool = False,
        scorer: str = "levenshtein",
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
            If you want to return every match, set this to 0.
        latinise : bool, optional
            If special unicode characters should be removed from the strings, by default False.
        ignore_case : bool, optional
            If the strings should be compared ignoring case, by default False.
        remove_punctuation : bool, optional
            If punctuation should be removed from the strings, by default False.
        only_letters : bool, optional
            If the strings should only be compared by their latin letters, by default False.
        scorer : str, optional
            The scorer to use, by default "levenshtein".
            Available scorers:
                "levenshtein",
                "jaro",
                "jaro_winkler".

        Returns
        -------
        list[str]
            All of the matches found.
        """
        # we return every match found if the limit is 0 or less
        if limit < 1:
            limit = None

        kwargs = {
            "score": score,
            "latinise": latinise,
            "remove_punctuation": remove_punctuation,
            "ignore_case": ignore_case,
            "only_letters": only_letters,
            "scorer": scorer,
        }

        return sorted(
            [s for s in string_list if self.match(string, s, **kwargs)],
            key=lambda s: Ratio().ratio(string, s, scorer=scorer),
            # by default this would sort the list from lowest to highest.
            reverse=True,
        )[:limit]

    def get_best_matches_with_ratio(
        self,
        string: str,
        string_list: list[str],
        *,
        score: int = 70,
        limit: int = 5,
        latinise: bool = False,
        ignore_case: bool = False,
        remove_punctuation: bool = False,
        only_letters: bool = False,
        scorer: str = "levenshtein",
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
            If you want to return every match, set this to 0.
        latinise : bool, optional
            If special unicode characters should be removed from the strings, by default False.
        ignore_case : bool, optional
            If the strings should be compared ignoring case, by default False.
        remove_punctuation : bool, optional
            If punctuation should be removed from the strings, by default False.
        only_letters : bool, optional
            If the strings should only be compared by their latin letters, by default False.
        scorer : str, optional
            The scorer to use, by default "levenshtein".
            Available scorers:
                "levenshtein",
                "jaro",
                "jaro_winkler".

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
            "scorer": scorer,
        }

        matches = self.get_best_matches(string, string_list, **kwargs)

        return [
            (match, Ratio().ratio(string, match, scorer=scorer)) for match in matches
        ]
