from typing import Optional, TypedDict

from stringmatch.scorer import BaseScorer


class RatioKwargs(TypedDict, total=False):
    """Contains the kwargs for the Ratio class, for type hinting purposes."""

    scorer: type[BaseScorer]
    score: int
    limit: Optional[int]
    latinise: bool
    ignore_case: bool
    remove_punctuation: bool
    alphanumeric: bool
    include_partial: bool
