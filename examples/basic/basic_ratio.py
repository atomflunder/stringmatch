# This here shows you the basic ratio function.
# Sometimes you only need the ratio, and not the actual match.
from stringmatch import Ratio


def main():
    # Initialising the Ratio class, with default settings.
    base_ratio = Ratio()

    answer = "Reykjavik"

    print("Spell the name of the capital of Iceland:")

    spell = input()

    # Returns the ratio of the match, from 0 (no match) to 100 (exact match).
    overlap = base_ratio.ratio(answer, spell)

    print(f"You are about {overlap}% correct.")


if __name__ == "__main__":
    main()
