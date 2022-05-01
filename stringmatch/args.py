from typing import Optional, TypedDict


class KeywordArguments(TypedDict, total=False):
    """Keyword arguments for type hinting purposes, mostly."""

    score: int
    limit: Optional[int]
    latinise: bool
    ignore_case: bool
    remove_punctuation: bool
    only_letters: bool
    include_partial: bool
