# This here shows you how to use different scoring algorithms,
# and even how to implement your own.

from stringmatch import BaseScorer, JaroWinklerScorer, LevenshteinScorer, Match


def main():
    # This initialises the Match class with the Levenshtein scorer.
    # This is the default scorer, so you could also just leave this empty.
    # This is for demonstration purposes.
    lev_scorer = Match(scorer=LevenshteinScorer)

    # This initialises the Match class with another available scorer, JaroWinkler.
    jw_scorer = Match(scorer=JaroWinklerScorer)

    # This initialises the Match class with a custom scorer.
    # You first have to create a class that inherits from BaseScorer, with a score method.
    # The score method takes two strings and returns a float between 0 and 100.
    class MyOwnScorer(BaseScorer):
        def score(self, a: str, b: str) -> float:
            # You should probably actually do some calculations here.
            return 50

    my_scorer = Match(scorer=MyOwnScorer)

    # Different scoring algorithms will of course produce differing results.
    # You can read up on the details of what each scoring algorithm does on wikipedia:
    # https://en.wikipedia.org/wiki/Levenshtein_distance
    # https://en.wikipedia.org/wiki/Jaro–Winkler_distance

    query = "A testing string!"
    target = "String test!"

    print(f"Levenshtein score: {lev_scorer.match_with_ratio(query, target)}")
    print(f"JaroWinkler score: {jw_scorer.match_with_ratio(query, target)}")
    print(f"MyOwnScorer score: {my_scorer.match_with_ratio(query, target)}")

    # If you do not want to run this yourself, here are the results:
    #
    # Levenshtein score: (False, 62)
    # JaroWinkler score: (True, 76)
    # MyOwnScorer score: (False, 50)


if __name__ == "__main__":
    main()
