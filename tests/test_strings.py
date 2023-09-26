from stringmatch.strings import Strings


def test_latinise():
    assert Strings().latinise("Héllö, world!") == "Hello, world!"
    assert Strings().latinise("ỲṖßɆȜǼǄ") == "YPssEYAEDZ"
    assert Strings().latinise("ジャパニーズ") == "ziyapani-zu"
    assert Strings().latinise("「 ") == "[ "


def test_remove_punctuation():
    assert Strings().remove_punctuation("Héllö, world!") == "Héllö world"
    assert Strings().remove_punctuation("wh'at;, ever") == "what ever"


def test_alphanumeric():
    assert Strings().alphanumeric("Héllö, world!") == "Hll world"
    assert Strings().alphanumeric("ỲṖßɆȜǼǄ") == ""


def test_ignore_case():
    assert Strings().ignore_case("Héllö, world!") == "héllö, world!"
    assert Strings().ignore_case("test test!", lower=False) == "TEST TEST!"
