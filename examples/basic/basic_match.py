# This shows off the basic matching functionality.

from stringmatch import Match


def main():
    # Initialising the Match class, with default settings.
    base_match = Match()

    answer = "Mount Everest"

    print("What is the tallest mountain in the world?")

    guess = input()

    # Returns True if the input matches, False if not.
    # This will not only match if you input "Mount Everest", but also stuff like "Mt. Everest", "Everest", etc.
    if base_match.match(answer, guess):
        print("Correct!")
    else:
        print("No thats not it!")


if __name__ == "__main__":
    main()
