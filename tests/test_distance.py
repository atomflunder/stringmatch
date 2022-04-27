from stringmatch.distance import Distance


def test_distance():
    assert Distance().distance("kitten", "sitting") == 3
    assert (
        Distance().distance(
            "eh", "a really, really, really different and long string to compare it to"
        )
        == 66
    )


def test_distance_list():
    assert Distance().distance_list("kitten", ["sitting", "kitten"]) == [3, 0]
    assert Distance().distance_list(
        "stringmatch", ["strmtc", "string", "match", "matchstring", ""]
    ) == [5, 5, 6, 10, None]
    assert Distance().distance("kitten", "") is None
