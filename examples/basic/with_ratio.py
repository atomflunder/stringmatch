# This here shows you how to use the match_with_ratio function.
# For the get_best_matches_with_ratio function,
# it is more or less the same thing, but with a list of tuples.

from stringmatch import Match


def main():
    # Initialising the Match class, with default settings.
    base_match = Match()

    answer = "Copenhagen"

    print("What is the capital of Denmark?")

    guess = input()

    # Returns a tuple with the result.
    # First value is a boolean, True if the input matches, False if not.
    # Second value is the match ratio, from 0 (no match) to 100 (exact match).
    result, ratio = base_match.match_with_ratio(answer, guess)

    if result:
        # This will only trigger if you input "Copenhagen".
        if ratio == 100:
            print("Exactly!")
        # This will trigger if you input something that is close to "Copenhagen".
        else:
            print("Yeah, close enough!")
    # This will trigger if you input something that is not close to "Copenhagen".
    else:
        print("No, thats not it!")


if __name__ == "__main__":
    main()
