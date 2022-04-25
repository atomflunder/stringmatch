import pytest

from searchlib.exceptions import EmptySearchException, InvalidLimitException
from searchlib.match import Match


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
    with pytest.raises(EmptySearchException):
        assert Match().match("", "f")

    assert Match().match("séärçh", "search", latinise=True) is True
    assert Match().match("séärçh", "search", latinise=False) is False

    assert Match().match("test,---....", "test", remove_punctuation=True) is True
    assert Match().match("test,---....", "test", remove_punctuation=False) is False

    assert Match().match("»»ᅳtestᅳ►", "test", only_letters=True) is True
    assert Match().match("»»ᅳtestᅳ►", "test", only_letters=False) is False

    assert Match().match("test", "th test", scorer="levenshtein") is True
    assert Match().match("test", "th test", scorer="jaro_winkler") is False


def test_get_best_match():
    assert Match().get_best_match("test", ["test", "nope", "tset"]) == "test"
    assert Match().get_best_match("whatever", ["test", "nope", "tset"]) is None
    assert (
        Match().get_best_match(
            "searchlib", ["srechlib", "slib", "searching library", "spam"]
        )
        == "srechlib"
    )
    with pytest.raises(EmptySearchException):
        assert Match().get_best_match("", ["f"])

    with pytest.raises(EmptySearchException):
        assert Match().get_best_match("....-", ["f"], remove_punctuation=True)


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
    with pytest.raises(EmptySearchException):
        assert Match().get_best_matches("", ["f"])
    with pytest.raises(InvalidLimitException):
        assert Match().get_best_matches("test", ["test", "nope", "tset"], limit=-1) == [
            "test"
        ]
