# Partial Matches

Setting `include_partial` to true will enable stringmatch to search for matches in partial substrings in the supplied strings.  
This means that we compare the shorter string of the two to substrings of the longer string with the same length.

This will yield better results, especially for searching and comparing names or titles but it is quite a bit slower, particularly when comparing very short strings to very long strings.

If a partial match is found, we **return a score between 65 and 95**, depending on the difference in length of the strings. A score of 100 is reserved for perfect matches.  
We start matching at a length of 2 characters, or 1 if it is the first character of the string.

Basic example:

```python
from stringmatch import Match

part_match = Match(include_partial=True)
# returns (True, 65)
part_match.match_with_ratio("A string", "A string thats like really really long", score=60)

def_match = Match(include_partial=False)
# returns (False, 35)
def_match.match_with_ratio("A string", "A string thats like really really long", score=60)
```

Example for searching names:

```python
from stringmatch import Match

teams = [
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

part_match = Match(include_partial=True)
part_match.get_best_match("Lakers", teams)  # returns 'Los Angeles Lakers'
part_match.get_best_match("76ers", teams)   # returns 'Philadelphia 76ers'


def_match = Match(include_partial=False)
def_match.get_best_match("Lakers", teams)  # returns None
def_match.get_best_match("76ers", teams)   # returns None
```
