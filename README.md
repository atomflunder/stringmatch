# Searchlib

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


Yet another small, lightweight string matching library written in Python, based on the [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance) and the [Levenshtein Python C Extension](https://github.com/maxbachmann/Levenshtein).  
Inspired by [seatgeek/thefuzz](https://github.com/seatgeek/thefuzz), which did not quite fit my needs, so I am building this library for myself, primarily.

## Table of Contents
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Links](#links)

## Requirements

- git
- Python 3.9 or later.

## Installation

```
pip install -U git+https://github.com/atomflunder/searchlib
```

## Usage

```python
from searchlib import Match, Ratio, Strings

# Basic usage:
Match().match("searchlib", "srchlib")               # returns True
Match().match("searchlib", "something else")        # returns False

# Matching lists:
searches = ["searchli", "searhli", "search", "lib", "whatever", "s"]
Match().get_best_match("searchlib", searches)       # returns "searchli"
Match().get_best_matches("searchlib", searches)     # returns ['searchli', 'searhli', 'search']

# Ratios:
Ratio().ratio("searchlib", "searchlib")             # returns 100
Ratio().ratio("searchlib", "srechlib")              # returns 82
ratios = ["searchlib", "srechlib"]
Ratio().ratio_list("searchlib", ratios)             # returns [100, 82]

# Modify strings:
Strings().latinise("Héllö, world!")                 # returns "Hello, world!"
Strings().remove_punctuation("wh'at;, ever")        # returns "what ever"
Strings().only_letters("Héllö, world!")             # returns "Hll world"
Strings().ignore_case("test test!", lower=False)    # returns "TEST TEST!"
```

You can pass in additional arguments for the `Match()` functions to customise your search further:

#### `score=int`

The score cutoff for matching, by default set to 70.

```python
Match().match("searchlib", "srechlib", score=85)    # returns False
Match().match("searchlib", "srechlib", score=70)    # returns True
```

#### `limit=int`

The limit of how many matches to return. Only available for Matches().get_best_matches(). By default this is set to `5`.

```python
searches = ["limit 5", "limit 4", "limit 3", "limit 2", "limit 1", "limit 0"]
Match().get_best_matches("limit 5", searches, limit=2)  # returns ["limit 5", "limit 4"]
Match().get_best_matches("limit 5", searches, limit=1)  # returns ["limit 5"]
```

#### `latinise=bool`

Replaces special unicode characters with their latin alphabet equivalents. By default turned off.

```python
Match().match("séärçh", "search", latinise=True)    # returns True
Match().match("séärçh", "search", latinise=False)   # returns False
```

#### `ignore_case=bool`

If you want to ignore case sensitivity while searching. By default turned off.

```python
Match().match("test", "TEST", ignore_case=True)     # returns True
Match().match("test", "TEST", ignore_case=False)    # returns False
```

#### `remove_punctuation=bool`

Removes commonly used punctuation symbols from the strings, like `.,;:!?` and so on. Be careful when using this, because if you pass in a string that is only made up of punctuation symbols, you will get an `EmptySearchException`. By default turned off.

```python
Match().match("test,---....", "test", remove_punctuation=True)  # returns True
Match().match("test,---....", "test", remove_punctuation=False) # returns False
```

#### `only_letters=bool`

Removes every character that is not in the latin alphabet, a more extreme version of `remove_punctuation`. The same rules apply here, be careful when you use it or you might get an `EmptySearchException`. By default turned off.

```python
Match().match("»»ᅳtestᅳ►", "test", only_letters=True)   # returns True
Match().match("»»ᅳtestᅳ►", "test", only_letters=False)  # returns False
```

#### `scorer=str`

The scoring algorithm to use, the available options are: [`"levenshtein"`](https://en.wikipedia.org/wiki/Levenshtein_distance), [`"jaro"`](https://en.wikipedia.org/wiki/Jaro–Winkler_distance#Jaro_similarity), [`"jaro_winkler"`](https://en.wikipedia.org/wiki/Jaro–Winkler_distance#Jaro–Winkler_similarity). Different algorithms will produce different results, obviously. By default set to `"levenshtein"`.

```python
Match().match("test", "th test", scorer="levenshtein")  # returns True (score = 73)
Match().match("test", "th test", scorer="jaro_winkler") # returns False (score = 60)
```


## Links

Packages used:

- [Levenshtein](https://github.com/maxbachmann/Levenshtein)
- [Unidecode](https://github.com/avian2/unidecode)

Related packages:

- [thefuzz](https://github.com/seatgeek/thefuzz)
