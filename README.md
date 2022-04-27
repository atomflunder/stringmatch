# Stringmatch

[![PyPI](https://img.shields.io/pypi/v/stringmatch?color=blue)](https://pypi.org/project/stringmatch/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/stringmatch)](https://pypi.org/project/stringmatch/) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


Yet another small, lightweight string matching library written in Python, based on the [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance) and the [Levenshtein Python C Extension](https://github.com/maxbachmann/Levenshtein).  
Inspired by [seatgeek/thefuzz](https://github.com/seatgeek/thefuzz), which did not quite fit my needs, so I am building this library for myself, primarily.

## Table of Contents
- [Requirements](#requirements)
- [Installation](#installation)
- [Basic Usage](#basic-usage)
  - [Additional Arguments](#additional-arguments)
- [Links](#links)

## Requirements

- Python 3.9 or later.

## Installation

Install the latest stable version with pip:

```
pip install stringmatch
```

Or install the newest version via git (Might be unstable/unfinished):
```
pip install -U git+https://github.com/atomflunder/stringmatch
```

## Basic Usage

```python
from stringmatch import Match, Ratio, Strings

# Basic usage:
match = Match()

match.match("searchlib", "srchlib")                   # returns True
match.match("searchlib", "something else")            # returns False

# Matching lists:
searches = ["searchli", "searhli", "search", "lib", "whatever", "s"]
match.get_best_match("searchlib", searches)           # returns "searchli"
match.get_best_matches("searchlib", searches)         # returns ['searchli', 'searhli', 'search']

# Ratios:
ratio = Ratio()

ratio.ratio("searchlib", "searchlib")                 # returns 100
ratio.ratio("searchlib", "srechlib")                  # returns 82
searches = ["searchlib", "srechlib"]
ratio.ratio_list("searchlib", searches)               # returns [100, 82]

# Getting matches and ratios:
match.match_with_ratio("searchlib", "srechlib")       # returns (True, 82)
searches = ["test", "nope", "tset"]
match.get_best_match_with_ratio("test", searches)     # returns ("test", 100)
match.get_best_matches_with_ratio("test", searches)   # returns [("test", 100), ("tset", 75)]

# Modify strings:
# This is meant for internal use, but you can also use it yourself, if you choose to.
strings = Strings()

strings.latinise("Héllö, world!")                     # returns "Hello, world!"
strings.remove_punctuation("wh'at;, ever")            # returns "what ever"
strings.only_letters("Héllö, world!")                 # returns "Hll world"
strings.ignore_case("test test!", lower=False)        # returns "TEST TEST!"
```

### Additional Arguments
You can pass in additional arguments for the `Match()` functions to customise your search further:

#### `score=int`

The score cutoff for matching, by default set to 70.

```python
match("searchlib", "srechlib", score=85)    # returns False
match("searchlib", "srechlib", score=70)    # returns True
```

#### `limit=int`

The limit of how many matches to return. Only available for `Matches().get_best_matches()`. If you want to return every match set this to 0. By default this is set to `5`.

```python
searches = ["limit 5", "limit 4", "limit 3", "limit 2", "limit 1", "limit 0"]
get_best_matches("limit 5", searches, limit=2)  # returns ["limit 5", "limit 4"]
get_best_matches("limit 5", searches, limit=1)  # returns ["limit 5"]
```

#### `latinise=bool`

Replaces special unicode characters with their latin alphabet equivalents. By default turned off.

```python
match("séärçh", "search", latinise=True)    # returns True
match("séärçh", "search", latinise=False)   # returns False
```

#### `ignore_case=bool`

If you want to ignore case sensitivity while searching. By default turned off.

```python
match("test", "TEST", ignore_case=True)     # returns True
match("test", "TEST", ignore_case=False)    # returns False
```

#### `remove_punctuation=bool`

Removes commonly used punctuation symbols from the strings, like `.,;:!?` and so on. By default turned off.

```python
match("test,---....", "test", remove_punctuation=True)  # returns True
match("test,---....", "test", remove_punctuation=False) # returns False
```

#### `only_letters=bool`

Removes every character that is not in the latin alphabet, a more extreme version of `remove_punctuation`. By default turned off.

```python
match("»»ᅳtestᅳ►", "test", only_letters=True)   # returns True
match("»»ᅳtestᅳ►", "test", only_letters=False)  # returns False
```

#### `scorer=str`

The scoring algorithm to use, the available options are: [`"levenshtein"`](https://en.wikipedia.org/wiki/Levenshtein_distance), [`"jaro"`](https://en.wikipedia.org/wiki/Jaro–Winkler_distance#Jaro_similarity), [`"jaro_winkler"`](https://en.wikipedia.org/wiki/Jaro–Winkler_distance#Jaro–Winkler_similarity). Different algorithms will produce different results, obviously. By default set to `"levenshtein"`.

```python
match("test", "th test", scorer="levenshtein")  # returns True (score = 73)
match("test", "th test", scorer="jaro_winkler") # returns False (score = 60)
```


## Links

Packages used:

- [Levenshtein](https://github.com/maxbachmann/Levenshtein)
- [Unidecode](https://github.com/avian2/unidecode)

Related packages:

- [thefuzz](https://github.com/seatgeek/thefuzz)
