# Searchlib

A very small, lightweight string matching library based on the [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance) and the [Levenshtein Python C Extension](https://github.com/maxbachmann/Levenshtein).  
Inspired by [seatgeek/thefuzz](https://github.com/seatgeek/thefuzz), which did not quite fit my needs, so I am building this library for myself, primarily.

## Usage

```python
from searchlib import Match

# Basic usage:
Match().match("searchlib", "srchlib") # returns True
Match().match("searchlib", "something else") # returns False

# Matching lists:
searches = ["searchli", "searhli", "search", "lib", "whatever", "s"]
Match().get_best_match("searchlib", searches) # returns "searchli"
Match().get_best_matches("searchlib", searches) # returns ['searchli', 'searhli', 'search']

# Ratios:
Match().ratio("searchlib", "searchlib") # returns 100
Match().ratio("searchlib", "srechlib") # returns 82
```

