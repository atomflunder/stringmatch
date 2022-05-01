import Levenshtein  # type: ignore


class _Scorer:
    """The base scorer class, used mainly for type hinting purposes."""

    def score(self, string1: str, string2: str) -> float:
        raise NotImplementedError


class LevenshteinScorer(_Scorer):
    """The Levenshtein scorer class."""

    def score(self, string1: str, string2: str) -> float:
        return Levenshtein.ratio(string1, string2)


class JaroScorer(_Scorer):
    """The Jaro scorer class."""

    def score(self, string1: str, string2: str) -> float:
        return Levenshtein.jaro(string1, string2)


class JaroWinklerScorer(_Scorer):
    """The Jaro-Winkler scorer class."""

    def score(self, string1: str, string2: str) -> float:
        return Levenshtein.jaro_winkler(string1, string2)
