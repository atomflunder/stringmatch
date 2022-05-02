from typing import Optional, TypedDict

from stringmatch.scorer import _Scorer


class RatioKwargs(TypedDict, total=False):
    """Contains the kwargs for the Ratio class, for type hinting purposes."""

    scorer: type[_Scorer]
    score: int
    limit: Optional[int]
    latinise: bool
    ignore_case: bool
    remove_punctuation: bool
    only_letters: bool
    include_partial: bool
