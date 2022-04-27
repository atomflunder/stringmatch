from stringmatch.match import Match


def test_match():
    assert Match().match("test", "test") is True
    assert Match().match("test", "nope") is False
    assert Match().match("searchlib", "srechlib") is True
    assert (
        Match().match(
            "séàr#.chlib", "searchlib", latinise=True, remove_punctuation=True
        )
        is True
    )
    assert Match().match("test", "TEST", ignore_case=False) is False
    assert Match().match("test", "TEST", ignore_case=True) is True
    assert Match().match("test", "-- test --!<<><", only_letters=True) is True
    assert Match().match("", "f") is False

    assert Match().match("séärçh", "search", latinise=True) is True
    assert Match().match("séärçh", "search", latinise=False) is False

    assert Match().match("test,---....", "test", remove_punctuation=True) is True
    assert Match().match("test,---....", "test", remove_punctuation=False) is False

    assert Match().match("»»ᅳtestᅳ►", "test", only_letters=True) is True
    assert Match().match("»»ᅳtestᅳ►", "test", only_letters=False) is False

    assert Match().match("test", "th test", scorer="levenshtein") is True
    assert Match().match("test", "th test", scorer="jaro_winkler") is False


def test_match_with_ratio():
    assert Match().match_with_ratio("test", "test") == (True, 100)
    assert Match().match_with_ratio("test", "nope") == (False, 25)
    assert Match().match_with_ratio("searchlib", "srechlib") == (True, 82)
    assert Match().match_with_ratio("test", "th test", scorer="jaro_winkler") == (
        False,
        60,
    )


def test_get_best_match():
    assert Match().get_best_match("test", ["test", "nope", "tset"]) == "test"
    assert Match().get_best_match("whatever", ["test", "nope", "tset"]) is None
    assert (
        Match().get_best_match(
            "searchlib", ["srechlib", "slib", "searching library", "spam"]
        )
        == "srechlib"
    )
    assert Match().get_best_match("", ["f"]) is None

    assert Match().get_best_match("....-", ["f"], remove_punctuation=True) is None


def test_get_best_match_with_ratio():
    assert Match().get_best_match_with_ratio("test", ["test", "nope", "tset"]) == (
        "test",
        100,
    )
    assert (
        Match().get_best_match_with_ratio("whatever", ["test", "nope", "tset"]) is None
    )


def test_get_best_matches():
    assert Match().get_best_matches("test", ["test", "nope", "tset"]) == [
        "test",
        "tset",
    ]
    assert Match().get_best_matches(
        "limit 5",
        ["limit 5", "limit 4", "limit 3", "limit 2", "limit 1", "limit 0"],
        limit=2,
    ) == ["limit 5", "limit 4"]

    assert Match().get_best_matches("", ["f"]) == []

    assert Match().get_best_matches("test", ["test", "nope", "tset"], limit=0) == [
        "test",
        "tset",
    ]


def test_get_best_matches_with_ratio():
    assert Match().get_best_matches_with_ratio("test", ["test", "nope", "tset"]) == [
        ("test", 100),
        ("tset", 75),
    ]
    assert Match().get_best_matches_with_ratio(
        "limit 5",
        ["limit 5", "limit 4", "limit 3", "limit 2", "limit 1", "limit 0"],
        limit=2,
    ) == [("limit 5", 100), ("limit 4", 86)]
