import pytest

from stringmatch.ratio import Ratio
from stringmatch.scorer import (
    BaseScorer,
    JaroScorer,
    JaroWinklerScorer,
    LevenshteinScorer,
)


def test_ratio():
    assert Ratio().ratio("test", "test") == 100
    assert Ratio().ratio("bla", "nope") == 0
    assert Ratio().ratio("stringmatch", "strngmach") == 90
    assert Ratio().ratio("stringmatch", "eh") == 15
    # for the explanation: the skintone emojis are the yellow emojis + a tone modifier
    assert Ratio().ratio("👍", "👍🏻") == 67
    assert Ratio().ratio("", "f") == 0
    assert Ratio().ratio(1, "what?") == 0  # type: ignore

    assert Ratio(latinise=True).ratio("ジャパニーズ", "ziyapani-zu") == 100

    assert Ratio(ignore_case=True).ratio("TESTbot test", "testbot") == 74
    assert Ratio(ignore_case=False).ratio("TESTbot test", "testbot") == 42

    assert Ratio(scorer=JaroWinklerScorer).ratio("searchlib", "srechlib") == 93
    assert Ratio(scorer=LevenshteinScorer).ratio("test", "th test") == 73
    assert Ratio(scorer=JaroWinklerScorer).ratio("test", "th test") == 60
    assert Ratio(scorer=JaroScorer).ratio("test", "th test") == 60

    with pytest.raises(TypeError):
        assert Ratio(scorer="nope").ratio("searchlib", "srechlib") == 82  # type: ignore

    with pytest.raises(NotImplementedError):
        assert Ratio(scorer=BaseScorer).ratio("searchlib", "srechlib") == 82


def test_ratio_list():
    assert Ratio().ratio_list("test", ["test", "nope"]) == [100, 25]
    assert Ratio().ratio_list(
        "srechlib", ["searchlib", "slib", "searching library", "spam"]
    ) == [82, 67, 56, 17]
    assert Ratio(ignore_case=False).ratio_list(
        "test", ["th TEST", "hwatever", "*"]
    ) == [18, 33, 0]

    assert Ratio(ignore_case=True, alphanumeric=True).ratio_list(
        "test", ["th TEST", "hwatever", "*"]
    ) == [73, 33, 0]

    assert Ratio(
        scorer=JaroWinklerScorer, ignore_case=True, alphanumeric=True
    ).ratio_list("test", ["th TEST", "hwatever", "*"]) == [60, 58, 0]

    assert Ratio(scorer=LevenshteinScorer).ratio_list(
        "test", ["th test", "hwatever"]
    ) == [73, 33]
    assert Ratio(scorer=JaroWinklerScorer).ratio_list(
        "test", ["th test", "hwatever"]
    ) == [60, 58]


def test_partial_ratio():
    assert Ratio().partial_ratio("test124", "93210") == 17
    assert Ratio().partial_ratio("93210", "test124") == 17
    assert Ratio().partial_ratio("testbot test", "testbot") == 85
    assert Ratio().partial_ratio("a", "this is a test") == 13
    assert Ratio().partial_ratio("e", "this is a test") == 13
    assert Ratio().partial_ratio("a ", "this is a test") == 75
    assert Ratio().partial_ratio("a test", "this is a test") == 85
    assert Ratio().partial_ratio("this", "this is a test") == 75
    assert Ratio().partial_ratio("this is a test", "this this this") == 71
    assert Ratio().partial_ratio("", "what?") == 0
    assert Ratio().partial_ratio(1, "what?") == 0  # type: ignore
    assert Ratio().partial_ratio("d", "dabuz") == 85
    assert Ratio().partial_ratio("a", "dabuz") == 33
    assert Ratio().partial_ratio("ab", "dabuz") == 95
    assert Ratio().partial_ratio("dabuz", "dabuz") == 100
    assert (
        Ratio().partial_ratio("a ", "this is a really really damn long string, wow")
        == 65
    )

    assert Ratio(ignore_case=True).partial_ratio("TESTbot test", "testbot") == 85
    assert Ratio(ignore_case=False).partial_ratio("TESTbot test", "testbot") == 42
