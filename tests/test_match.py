import pytest

from searchlib.exceptions import EmptySearchException, InvalidLimitException
from searchlib.match import Match


def test_ratio():
    assert Match().ratio("test", "test") == 100
    assert Match().ratio("bla", "nope") == 0
    assert Match().ratio("searchlib", "srechlib") == 82


def test_ratio_list():
    assert Match().ratio_list("test", ["test", "nope"]) == [100, 25]
    assert Match().ratio_list(
        "srechlib", ["searchlib", "slib", "searching library", "spam"]
    ) == [82, 67, 56, 17]


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
    with pytest.raises(EmptySearchException):
        assert Match().match("", "f")


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
