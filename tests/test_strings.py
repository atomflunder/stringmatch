from searchlib.strings import Strings


def test_latinise():
    assert Strings().latinise("Héllö, world!") == "Hello, world!"
    assert Strings().latinise("ỲṖßɆȜǼǄ") == "YPssEYAEDZ"


def test_remove_punctuation():
    assert Strings().remove_punctuation("Héllö, world!") == "Héllö world"
    assert Strings().remove_punctuation("wh'at;, ever") == "what ever"
