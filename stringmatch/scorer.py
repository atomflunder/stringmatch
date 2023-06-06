from mypy_extensions import mypyc_attr
from rapidfuzz import distance


@mypyc_attr(allow_interpreted_subclasses=True)
class BaseScorer:
    """The base scorer class, for inheriting the other scorers and constructing your own."""

    def score(self, string1: str, string2: str) -> float:
        raise NotImplementedError


class LevenshteinScorer(BaseScorer):
    """The Levenshtein scorer class, uses the Levenshtein Distance to calculate the similarity."""

    def score(self, string1: str, string2: str) -> float:
        return (
            distance.Levenshtein.normalized_similarity(
                string1, string2, weights=(1, 1, 2)
            )
            * 100
        )


class JaroScorer(BaseScorer):
    """The Jaro scorer class, uses the Jaro Similarity to calculate the similarity."""

    def score(self, string1: str, string2: str) -> float:
        return distance.Jaro.normalized_similarity(string1, string2) * 100


class JaroWinklerScorer(BaseScorer):
    """The Jaro-Winkler scorer class, uses the Jaro-Winkler Similarity to calculate the similarity."""

    def score(self, string1: str, string2: str) -> float:
        return distance.JaroWinkler.normalized_similarity(string1, string2) * 100
