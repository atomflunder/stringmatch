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

## Arguments

Explanation of some keyword-only arguments for some more advanced usage.

`score`: The score cutoff for matches, by default set to 70.  
`latinise`: Removes special characters and sets them to the latin alphabet equivalent. Example: `éö -> eo`  
`remove_punctuation`: Removes punctuation from the strings. Example: `h,i! -> hi`  
`limit`: Only available for `get_best_matches()`. The limit of how many matches to return. Returns the best X matches in order, by default set to 5.  

## Links

Packages used:

- [Levenshtein](https://github.com/maxbachmann/Levenshtein)
- [Unidecode](https://github.com/avian2/unidecode)

Related packages:

- [thefuzz](https://github.com/seatgeek/thefuzz)
