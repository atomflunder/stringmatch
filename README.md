# Searchlib

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


A very small, lightweight string matching library based on the [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance) and the [Levenshtein Python C Extension](https://github.com/maxbachmann/Levenshtein).  
Inspired by [seatgeek/thefuzz](https://github.com/seatgeek/thefuzz), which did not quite fit my needs, so I am building this library for myself, primarily.

## Installation

tbd

## Requirements

- Python 3.9 or later.

## Usage

```python
from searchlib import Match, Ratio

# Basic usage:
Match().match("searchlib", "srchlib") # returns True
Match().match("searchlib", "something else") # returns False

# Matching lists:
searches = ["searchli", "searhli", "search", "lib", "whatever", "s"]
Match().get_best_match("searchlib", searches) # returns "searchli"
Match().get_best_matches("searchlib", searches) # returns ['searchli', 'searhli', 'search']

# Ratios:
Ratio().ratio("searchlib", "searchlib") # returns 100
Ratio().ratio("searchlib", "srechlib") # returns 82

# Some special arguments:
Match().match("test", "TEST", ignore_case=True) # returns True
Match().match("test", "-- test --!<<><", only_letters=True) # returns True
Match().match("séàr#.chlib", "searchlib", latinise=True, remove_punctuation=True) # returns True

search_list = ["limit 5", "limit 4", "limit 3", "limit 2", "limit 1", "limit 0"]
Match().get_best_matches("limit 5", searchlist, limit=2) # returns ["limit 5", "limit 4"]
```

## Links

Packages used:

- [Levenshtein](https://github.com/maxbachmann/Levenshtein)
- [Unidecode](https://github.com/avian2/unidecode)

Related packages:

- [thefuzz](https://github.com/seatgeek/thefuzz)
