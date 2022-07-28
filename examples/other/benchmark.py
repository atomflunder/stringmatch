# This is just a basic benchmark to compare the speed of stringmatch and thefuzz.
# I chose thefuzz since it is the most popular library for fuzzy string matching,
# and it also inspired me to make stringmatch.
#
# Disclaimer: This is not a 100% accurate measurement of how good a library is,
# both have their own strengths and weaknesses.

import timeit

from thefuzz import process

from stringmatch import Match

query = "string"

string_list = [
    "A string",
    "Some other Strings",
    "Whatever",
    "Like a really, really, really damn long string",
    "This: String",
    "Hello!",
    "This is a string",
    "",
    "Empty string",
    "Cool",
    "???",
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "These should be enough right?",
]

# Mimicking thefuzz's settings.
match = Match(include_partial=True)


def stringmatch_benchmark():
    return match.get_best_matches_with_ratio(query, string_list, score=40, limit=7)


def thefuzz_benchmark():
    return process.extractBests(query, string_list, score_cutoff=40, limit=7)


def main():
    print(f"Stringmatch result: {stringmatch_benchmark()}")
    print(f"Thefuzz result: {thefuzz_benchmark()}")

    s_time = timeit.timeit(
        "stringmatch_benchmark()",
        setup="from __main__ import stringmatch_benchmark",
        number=100000,
    )
    f_time = timeit.timeit(
        "thefuzz_benchmark()",
        setup="from __main__ import thefuzz_benchmark",
        number=100000,
    )

    print(f"stringmatch time: {round(s_time, 3)}s")
    print(f"thefuzz time: {round(f_time, 3)}s")

    # If you dont wanna run the benchmark yourself, here are the results on my PC:
    # Stringmatch result: [
    #   ('A string', 95),
    #   ('This: String', 85),
    #   ('Empty string', 85),
    #   ('This is a string', 75),
    #   ('Some other Strings', 75),
    #   ('Like a really, really, really damn long string', 65)
    # ]

    # Thefuzz result: [
    #   ('A string', 95),
    #   ('Some other Strings', 90),
    #   ('Like a really, really, really damn long string', 90),
    #   ('This: String', 90),
    #   ('This is a string', 90),
    #   ('Empty string', 90),
    #   ('These should be enough right?', 45)
    # ]

    # stringmatch time: 2.881s
    # thefuzz time: 37.602s
    # thefuzz time (without Levenshtein): 118.11s

    # To demonstrate the result on lower-end hardware,
    # here are the times on my Raspberry Pi 3B+:

    # stringmatch time: 33.226s
    # thefuzz time: 413.555s
    # thefuzz time (without Levenshtein): 1166.083s


if __name__ == "__main__":
    main()
