from stringmatch.ratio import Ratio


def test_ratio():
    assert Ratio().ratio("test", "test") == 100
    assert Ratio().ratio("bla", "nope") == 0
    assert Ratio().ratio("searchlib", "srechlib") == 82
    assert Ratio().ratio("searchlib", "srechlib", scorer="jaro_winkler") == 93
    assert Ratio().ratio("test", "th test", scorer="levenshtein") == 73
    assert Ratio().ratio("test", "th test", scorer="jaro_winkler") == 60
    assert Ratio().ratio("searchlib", "srechlib", scorer="nope") == 82
    assert Ratio().ratio("", "f") == 0


def test_ratio_list():
    assert Ratio().ratio_list("test", ["test", "nope"]) == [100, 25]
    assert Ratio().ratio_list(
        "srechlib", ["searchlib", "slib", "searching library", "spam"]
    ) == [82, 67, 56, 17]
