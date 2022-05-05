# This shows you how to extract the best match out of a list of strings.

from stringmatch import Match


def main():
    # Initialising the Match class, with default settings.
    base_match = Match()

    print("What is your favorite holiday?")

    guess = input()

    # Just a list of some holidays in the United States
    holiday_list = [
        "New Year's Day",
        "Martin Luther King, Jr. Day",
        "Presidents' Day",
        "Memorial Day",
        "Independence Day",
        "Labor Day",
        "Columbus Day",
        "Veterans Day",
        "Thanksgiving Day",
        "Christmas Day",
    ]

    # Returns the best match from the list of holidays,or None if no match is found.
    # This will not only match if you input "New Year's Day", but also stuff like "New Years", "New Year", etc.
    fav_holiday = base_match.get_best_match(guess, holiday_list)

    if fav_holiday:
        print(f"Your favorite holiday is {fav_holiday}? Cool!")
    else:
        print("Sorry, I don't know that one.")


if __name__ == "__main__":
    main()
