# This here shows you the usage of the keyword arguments available
# when initialising the Match() or Ratio() classes with one exception, include_partial.
# You can find examples of include_partial in the ./examples/custom/partial_match.py file.
# The ones shown here all modify the strings prior to matching.

from stringmatch import Match


def latinise():
    # The latinise keyword argument modifies a string into its latin alphabet equivalent.
    # Also called transliteration.
    # We use the unidecode library to do this.

    # Initialising the Match class, with latinise set to true.
    lat_match = Match(latinise=True)
    # And for comparison, we initialise the Match class without latinise set.
    no_lat_match = Match()

    greek_string = "αγώνας"
    latin_string = "agonas"

    print("\nLatinise:")
    print(f"Latinised: {lat_match.match_with_ratio(greek_string, latin_string)}")
    print(f"Default: {no_lat_match.match_with_ratio(greek_string, latin_string)}")

    # If you dont want to run the code yourself, here are the results:
    #
    # Latinised: (True, 100)
    # Default: (False, 0)


def case_sensitivity():
    # The ignore_case keyword argument modifies a string into lowercase.
    # It is enabled by default, so if you need your search to be case sensitive,
    # you need to switch it to False.

    # Initialising the Match class, with default values.
    default_match = Match()
    # And for comparison, we initialise the Match class with ignore_case set to False.
    case_match = Match(ignore_case=False)

    upper_string = "STRINGMATCH"
    lower_string = "stringmatch"

    print("\nCase Sensitivity:")
    print(f"Default: {default_match.match_with_ratio(upper_string, lower_string)}")
    print(f"Case sensitive: {case_match.match_with_ratio(upper_string, lower_string)}")

    # If you dont want to run the code yourself, here are the results:
    #
    # Default: (True, 100)
    # Case sensitive: (False, 0)


def special_chars():
    # The next two keyword arguments are remove_punctuation and alphanumeric.
    # remove_punctuation removes all commonly used punctuation from a string.
    # alphanumeric removes all non-alphanumeric characters from a string.
    # Use whichever one fits your needs better.
    # They are both disabled by default.

    # Initialising the Match class, with remove_punctuationset to True.
    punct_match = Match(remove_punctuation=True)
    # Initialising with alphanumeric set to True.
    alpha_match = Match(alphanumeric=True)
    # And for comparison, we initialise the Match class with default values.
    def_match = Match()

    a_string = "🙽🙽!!!Stringmatch!!!🙽🙽"
    b_string = "stringmatch"

    print("\nSpecial Characters:")
    print(f"Default: {def_match.match_with_ratio(a_string, b_string)}")
    print(f"No-punctuation: {punct_match.match_with_ratio(a_string, b_string)}")
    print(f"Only-alphanumeric: {alpha_match.match_with_ratio(a_string, b_string)}")

    # If you dont want to run the code yourself, here are the results:
    #
    # Default: (False, 69)
    # No-punctuation: (True, 85)
    # Only-alphanumeric: (True, 100)


def combining():
    # This here just shows that you can, of course,
    # mix-and-match the above keyword arguments, depending on what you need.

    # Initialising the Match class with some keyword arguments.
    my_match = Match(remove_punctuation=True, latinise=True, ignore_case=False)
    # And the default one, just for comparisions sake.
    def_match = Match()

    greek_string = "αγώνας!!!"
    latin_string = "Agonas"

    print("\nCombining:")
    print(f"Combined: {my_match.match_with_ratio(greek_string, latin_string)}")
    print(f"Default: {def_match.match_with_ratio(greek_string, latin_string)}")

    # If you dont want to run the code yourself, here are the results:
    #
    # Combined: (True, 83)
    # Default: (False, 0)


if __name__ == "__main__":
    latinise()
    case_sensitivity()
    special_chars()
    combining()
