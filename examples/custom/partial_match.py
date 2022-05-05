# This here shows you how to include partial matches in your searches.
# Partial matches will lead to better results, but they also are a bit slower.

from stringmatch import Match


def main():
    # Initialize the match object with partial matching turned on.
    part_match = Match(include_partial=True)
    # And for comparison, the default match class.
    def_match = Match()

    # Partial matches are very useful if the thing you want to search for is commonly abbreviated.
    # A good example is sports teams.
    # If you want to search for the Lakers you dont want to input "Los Angeles Lakers", but just "Lakers".

    # Yeah these are not all teams, I left some out for the sake of this example.
    nba_teams = [
        "Boston Celtics",
        "Chicago Bulls",
        "Cleveland Cavaliers",
        "Dallas Mavericks",
        "Los Angeles Lakers",
        "Memphis Grizzlies",
        "Miami Heat",
        "Milwaukee Bucks",
        "Minnesota Timberwolves",
        "New Orleans Pelicans",
        "New York Knicks",
        "Oklahoma City Thunder",
        "Orlando Magic",
        "Philadelphia 76ers",
        "Phoenix Suns",
    ]

    laker_string = "Lakers"
    seventy_string = "76ers"

    print("\nPartial matches:")
    print("Lakers:", part_match.get_best_match(laker_string, nba_teams))
    print("76ers:", part_match.get_best_match(seventy_string, nba_teams))

    print("\nDefault matches:")
    print("Lakers:", def_match.get_best_match(laker_string, nba_teams))
    print("76ers:", def_match.get_best_match(seventy_string, nba_teams))

    # If you dont want to run the code yourself, here are the results:
    #
    # Partial matches:
    # Lakers: Los Angeles Lakers
    # 76ers: Philadelphia 76ers
    #
    # Default matches:
    # Lakers: None
    # 76ers: None


if __name__ == "__main__":
    main()
