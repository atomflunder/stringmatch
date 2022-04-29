import pytest

from stringmatch.ratio import (
    JaroScorer,
    JaroWinklerScorer,
    LevenshteinScorer,
    Ratio,
    _Scorer,
)


def test_ratio():
    assert Ratio().ratio("test", "test") == 100
    assert Ratio().ratio("bla", "nope") == 0
    assert Ratio().ratio("searchlib", "srechlib") == 82

    assert Ratio(scorer=JaroWinklerScorer).ratio("searchlib", "srechlib") == 93
    assert Ratio(scorer=LevenshteinScorer).ratio("test", "th test") == 73
    assert Ratio(scorer=JaroWinklerScorer).ratio("test", "th test") == 60
    assert Ratio(scorer=JaroScorer).ratio("test", "th test") == 60

    with pytest.raises(TypeError):
        assert Ratio(scorer="nope").ratio("searchlib", "srechlib") == 82  # type: ignore

    with pytest.raises(NotImplementedError):
        assert Ratio(scorer=_Scorer).ratio("searchlib", "srechlib") == 82

    assert Ratio().ratio("", "f") == 0
    assert Ratio(LevenshteinScorer).ratio_list("test", ["th test", "hwatever"]) == [
        73,
        33,
    ]
    assert Ratio(JaroWinklerScorer).ratio_list("test", ["th test", "hwatever"]) == [
        60,
        58,
    ]


def test_ratio_list():
    assert Ratio().ratio_list("test", ["test", "nope"]) == [100, 25]
    assert Ratio().ratio_list(
        "srechlib", ["searchlib", "slib", "searching library", "spam"]
    ) == [82, 67, 56, 17]
