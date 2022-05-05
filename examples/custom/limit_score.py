# This here shows you the usage of the keyword arguments available in functions, limit and score.

from stringmatch import Match


def score():
    # score is the minimum ratio that the match needs to have to return True.
    # So if you specify a score of 50, every match that has a ratio less than 50 will be ignored.
    # The default value for score is 70.
    # This is available for every Match function.

    # Initialising the Match class, with default settings.
    base_match = Match()

    test_string = "stringmatch"
    comp_string = "stngmach"

    # The ratio of this match is 84.

    match_50 = base_match.match(test_string, comp_string, score=50)
    match_70 = base_match.match(test_string, comp_string)
    match_100 = base_match.match(test_string, comp_string, score=100)

    print(f"Match 50: {match_50}")
    print(f"Match 70: {match_70}")
    print(f"Match 100: {match_100}")

    # If you dont want to run the code yourself, here are the results:
    #
    # Match 50: True
    # Match 70: True
    # Match 100: False


def limit():
    # The second keyword only argument is called limit.
    # This is the maximum number of matches that will be returned.
    # The default value for limit is 5.
    # If you specify a limit of 0 or None, every match will be returned.
    # This is only available for functions that return multiple matches.

    # Initialising the Match class, with default settings.
    base_match = Match()

    test_string = "stringmatch"
    string_list = [
        "stngmach",
        "smatch",
        "stringmatch",
        "matchmatch",
        "string",
        "uh",
        "well whatever",
        "stmatch",
        "st. match",
        "singmatch",
        "stingmatch",
    ]

    limit_2 = base_match.get_best_matches(test_string, string_list, limit=2)
    limit_5 = base_match.get_best_matches(test_string, string_list)
    # Setting the limit to None also works.
    limit_0 = base_match.get_best_matches(test_string, string_list, limit=0)

    print(f"Limit 2: {limit_2}")
    print(f"Limit 5: {limit_5}")
    print(f"Limit 0: {limit_0}")

    # If you dont want to run the code yourself, here are the results:
    #
    # Limit 2: ['stringmatch', 'stingmatch']
    # Limit 5: ['stringmatch', 'stingmatch', 'singmatch', 'stngmach', 'stmatch']
    # Limit 0: ['stringmatch', 'stingmatch', 'singmatch', 'stngmach', 'stmatch', 'smatch', 'string', 'st. match']


if __name__ == "__main__":
    score()
    limit()
