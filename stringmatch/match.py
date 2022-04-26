from typing import Optional

from stringmatch.exceptions import EmptySearchException, InvalidLimitException
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
        Be careful when using remove_punctuation and only_letters,
        if they remove everything in the string, this will raise an EmptySearchException.

        Parameters
        ----------
        string1 : str
            The first string to compare.
        string2 : str
            The second string to compare.
        score : int, optional
            The cutoff for the score, by default 70.
        latinise : bool, optional
            If special unicode characters should be removed from the strings, by default False
        ignore_case : bool, optional
            If the strings should be compared ignoring case, by default False
        remove_punctuation : bool, optional
            If punctuation should be removed from the strings, by default False
        only_letters : bool, optional
            If the strings should only be compared by their latin letters, by default False
        scorer : str, optional
            The scorer to use, by default "levenshtein".
            Available scorers:
                "levenshtein"
                "jaro"
                "jaro_winkler"

        Returns
        -------
        bool
            If the strings are similar enough.

        Raises
        ------
        EmptySearchException
            If one of the strings to compare is empty.
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

        if not string1 or not string2:
            raise EmptySearchException("Cannot compare an empty string.")

        return Ratio().ratio(string1, string2, scorer=scorer) >= score

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
        Be careful when using remove_punctuation and only_letters,
        if they remove everything in the string, this will raise an EmptySearchException.

        Parameters
        ----------
        string : str
            The string to compare.
        string_list : list[str]
            The list of strings to compare to.
        score : int, optional
            The cutoff for the score, by default 70
        latinise : bool, optional
            If special unicode characters should be removed from the strings, by default False
        ignore_case : bool, optional
            If the strings should be compared ignoring case, by default False
        remove_punctuation : bool, optional
            If punctuation should be removed from the strings, by default False
        only_letters : bool, optional
            If the strings should only be compared by their latin letters, by default False
        scorer : str, optional
            The scorer to use, by default "levenshtein".
            Available scorers:
                "levenshtein"
                "jaro"
                "jaro_winkler"

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
            max(string_list, key=lambda s: Ratio().ratio(string, s))
            if any(s for s in string_list if self.match(string, s, **kwargs))
            else None
        )

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
        Be careful when using remove_punctuation and only_letters,
        if they remove everything in the string, this will raise an EmptySearchException.

        Parameters
        ----------
        string : str
            The string to compare.
        string_list : list[str]
            The list of strings to compare to.
        score : int, optional
            The cutoff for the score, by default 70
        limit : int, optional
            The number of matches to return, by default 5
        latinise : bool, optional
            If special unicode characters should be removed from the strings, by default False
        ignore_case : bool, optional
            If the strings should be compared ignoring case, by default False
        remove_punctuation : bool, optional
            If punctuation should be removed from the strings, by default False
        only_letters : bool, optional
            If the strings should only be compared by their latin letters, by default False
        scorer : str, optional
            The scorer to use, by default "levenshtein".
            Available scorers:
                "levenshtein"
                "jaro"
                "jaro_winkler"

        Returns
        -------
        list[str]
            All of the matches found.

        Raises
        ------
        InvalidLimitException
            If the limit used is less than 1.
        """
        if limit < 1:
            raise InvalidLimitException("Limit must be greater than 1.")

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
            key=lambda s: Ratio().ratio(string, s),
            # by default this would sort the list from lowest to highest.
            reverse=True,
        )[:limit]
