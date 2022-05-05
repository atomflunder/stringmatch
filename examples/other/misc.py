# This here shows you some miscellaneous stuff the other examples did not cover.

from stringmatch import Distance, Strings


def distance():
    # You can get the Levenshtein distance between two strings directly,
    # if you do not wish to use the ratios.
    # The distance is the number of characters you have to change to get from one string to the other.
    # So, the higher the distance, the more different the strings.

    dist = Distance()

    string_a = "stringmatch"

    string_b = "strnmetch"
    string_c = "something very different"

    print(f"Levenshtein distance a to b: {dist.distance(string_a, string_b)}")
    print(f"Levenshtein distance a to c: {dist.distance(string_a, string_c)}")

    # If you do not want to run this yourself, here are the results:
    #
    # Levenshtein distance a to b: 3
    # Levenshtein distance a to c: 19


def modify_strings():
    # You can also use the internal functions to modify the strings.
    # Look into the ./examples/custom/keyword_class.py file to see more information
    # on what they do exactly, but here are some examples:

    string_mod = Strings()

    string_a = "□ Striñgmätch!!! □"

    print(f"String: {string_a}")
    print(f"Latinised string: {string_mod.latinise(string_a)}")
    print(f"String without punctuation: {string_mod.remove_punctuation(string_a)}")
    print(f"String without non-latin letters: {string_mod.alphanumeric(string_a)}")
    print(f"String in all upper case: {string_mod.ignore_case(string_a, lower=False)}")

    # If you do not want to run this yourself, here are the results:
    #
    # String: □ Striñgmätch!!! □
    # Latinised string: # Stringmatch!!! #
    # String without punctuation: □ Striñgmätch □
    # String without non-latin letters:  Strigmtch
    # String in all upper case: □ STRIÑGMÄTCH!!! □


if __name__ == "__main__":
    distance()
    modify_strings()
