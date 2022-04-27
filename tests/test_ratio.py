from stringmatch.ratio import Ratio


def test_ratio():
    assert Ratio().ratio("test", "test") == 100
    assert Ratio().ratio("bla", "nope") == 0
    assert Ratio().ratio("searchlib", "srechlib") == 82
    assert Ratio(scorer="jaro_winkler").ratio("searchlib", "srechlib") == 93
    assert Ratio(scorer="levenshtein").ratio("test", "th test") == 73
    assert Ratio(scorer="jaro_winkler").ratio("test", "th test") == 60
    assert Ratio(scorer="nope").ratio("searchlib", "srechlib") == 82
    assert Ratio().ratio("", "f") == 0
    assert Ratio("levenshtein").ratio_list("test", ["th test", "hwatever"]) == [73, 33]
    assert Ratio("jaro_winkler").ratio_list("test", ["th test", "hwatever"]) == [60, 58]


def test_ratio_list():
    assert Ratio().ratio_list("test", ["test", "nope"]) == [100, 25]
    assert Ratio().ratio_list(
        "srechlib", ["searchlib", "slib", "searching library", "spam"]
    ) == [82, 67, 56, 17]
