import Levenshtein  # type: ignore
from mypy_extensions import mypyc_attr


@mypyc_attr(allow_interpreted_subclasses=True)
class BaseScorer:
    """The base scorer class, for inheriting the other scorers."""

    def score(self, string1: str, string2: str) -> float:
        raise NotImplementedError


class LevenshteinScorer(BaseScorer):
    """The Levenshtein scorer class."""

    def score(self, string1: str, string2: str) -> float:
        return Levenshtein.ratio(string1, string2)


class JaroScorer(BaseScorer):
    """The Jaro scorer class."""

    def score(self, string1: str, string2: str) -> float:
        return Levenshtein.jaro(string1, string2)


class JaroWinklerScorer(BaseScorer):
    """The Jaro-Winkler scorer class."""

    def score(self, string1: str, string2: str) -> float:
        return Levenshtein.jaro_winkler(string1, string2)
