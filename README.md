# stringmatch

[![PyPI](https://img.shields.io/pypi/v/stringmatch?color=blue)](https://pypi.org/project/stringmatch/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/stringmatch)](https://pypi.org/project/stringmatch/) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


**stringmatch** is yet another small, lightweight string matching library written in Python, based on the [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance) and the [Levenshtein Python C Extension](https://github.com/maxbachmann/Levenshtein).  
Inspired by libraries like [seatgeek/thefuzz](https://github.com/seatgeek/thefuzz), which did not quite fit my needs. And so I am building this library for myself, primarily.

## Table of Contents
- [🎯 Key Features](#key-features)
- [📋 Requirements](#requirements)
- [⚙️ Installation](#installation)
- [🔨 Basic Usage](#basic-usage)
  - [Matching](#matching)
  - [Ratios](#ratios)
  - [Matching & Ratios](#matching--ratios)
  - [Distances](#distances)
  - [Strings](#strings)
- [🛠️ Advanced Usage](#advanced-usage)
    - [Keyword Arguments](#keyword-arguments)
    - [Scoring Algorithms](#scoring-algorithms)
- [🌟 Contributing](#contributing)
- [🔗 Links](#links)

## Key Features
At its core this library **compares and matches between strings** based mainly on, among others, the [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance).  
What sets stringmatch apart from the other libraries that do the same are:

  - Up to **10x faster**
  - Offering more options for customising searches
  - More utility functions for modifying and comparing strings
  - Better matching & handling of special characters
  - Better UX (hopefully)

## Requirements

- Python 3.9 or later.

## Installation

Install the latest stable version with pip:

```
pip install stringmatch
```

Or install the newest version via git (Might be unstable or unfinished):
```
pip install -U git+https://github.com/atomflunder/stringmatch
```

## Basic Usage

### Matching

The match functions allow you to compare 2 strings and check if they are "similar enough" to each other, or get the best match(es) from a list of strings:

```python
from stringmatch import Match

match = Match()

# Checks if the strings are similar.
match.match("searchlib", "srchlib")           # returns True
match.match("searchlib", "something else")    # returns False

# Returns the best match(es) found in the list.
searches = ["searchli", "searhli", "search", "lib", "whatever", "s"]
match.get_best_match("searchlib", searches)   # returns "searchli"
match.get_best_matches("searchlib", searches) # returns ['searchli', 'searhli', 'search']
```

### Ratios

You can get the "ratio of similarity" between strings like this:

```python
from stringmatch import Ratio

ratio = Ratio()

# Getting the ratio between the two strings.
ratio.ratio("searchlib", "searchlib")   # returns 100
ratio.ratio("searchlib", "srechlib")    # returns 82

# Getting the ratio between the first string and the list of strings at once.
searches = ["searchlib", "srechlib"]
ratio.ratio_list("searchlib", searches) # returns [100, 82]
```

### Matching & Ratios

You can also get both the match and the ratio together in a tuple using these functions:

```python
from stringmatch import Match

match = Match()
searches = ["test", "nope", "tset"]

match.match_with_ratio("searchlib", "srechlib")       # returns (True, 82)
match.get_best_match_with_ratio("test", searches)     # returns ("test", 100)
match.get_best_matches_with_ratio("test", searches)   # returns [("test", 100), ("tset", 75)]
```

### Distances

Instead of the ratio, you can also get the Levenshtein distance between strings directly:

```python
from stringmatch import Distance

distance = Distance()

distance.distance("kitten", "sitting")      # returns 3

searches = ["sitting", "kitten"]
distance.distance_list("kitten", searches)  # returns [3, 0]
```

### Strings

This is primarily meant for internal usage, but you can also use this library to modify strings:

```python
from stringmatch import Strings

strings = Strings()

strings.latinise("Héllö, world!")               # returns "Hello, world!"
strings.remove_punctuation("wh'at;, ever")      # returns "what ever"
strings.only_letters("Héllö, world!")           # returns "Hll world"
strings.ignore_case("test test!", lower=False)  # returns "TEST TEST!"
```

## Advanced Usage

### Keyword Arguments
You can pass in these optional arguments for the `Match()` and `Ratio()` functions to customise your search further:

### `score`

| Name  | Description   | Type  | Default | Required? |
| ---   | ---           | ---   | ---     | ---       |
| score | The score cutoff for matching. Only available for `Match()` functions. | Integer | 70 | No

```python
# Example:

match("searchlib", "srechlib", score=85)    # returns False
match("searchlib", "srechlib", score=70)    # returns True
```

---

### `limit`

| Name  | Description   | Type  | Default | Required? |
| ---   | ---           | ---   | ---     | ---       |
| limit | The limit of how many matches to return. Only available for `Matches().get_best_matches()`. If you want to return every match set this to 0. | Integer | 5 | No

```python
# Example:

searches = ["limit 5", "limit 4", "limit 3", "limit 2", "limit 1", "limit 0"]
get_best_matches("limit 5", searches, limit=2)  # returns ["limit 5", "limit 4"]
get_best_matches("limit 5", searches, limit=1)  # returns ["limit 5"]
```

---

### `latinise`

| Name  | Description   | Type  | Default | Required? |
| ---   | ---           | ---   | ---     | ---       |
| latinise | Replaces special unicode characters with their latin alphabet equivalents. | Boolean | False | No

```python
# Example:

match("séärçh", "search", latinise=True)    # returns True
match("séärçh", "search", latinise=False)   # returns False
```

---

### `ignore_case`

| Name  | Description   | Type  | Default | Required? |
| ---   | ---           | ---   | ---     | ---       |
| ignore_case | If you want to ignore case sensitivity while searching. | Boolean | False | No

```python
# Example:

match("test", "TEST", ignore_case=True)     # returns True
match("test", "TEST", ignore_case=False)    # returns False
```

---

### `remove_punctuation`

| Name  | Description   | Type  | Default | Required? |
| ---   | ---           | ---   | ---     | ---       |
| remove_punctuation | Removes commonly used punctuation symbols from the strings, like `.,;:!?` and so on. | Boolean | False | No

```python
# Example:

match("test,---....", "test", remove_punctuation=True)  # returns True
match("test,---....", "test", remove_punctuation=False) # returns False
```

---

### `only_letters`

| Name  | Description   | Type  | Default | Required? |
| ---   | ---           | ---   | ---     | ---       |
| only_letters | Removes every character that is not in the latin alphabet, a more extreme version of `remove_punctuation`. | Boolean | False | No

```python
# Example:

match("»»ᅳtestᅳ►", "test", only_letters=True)   # returns True
match("»»ᅳtestᅳ►", "test", only_letters=False)  # returns False
```

---

### Scoring Algorithms

You can pass in different scoring algorithms when initialising the `Match()` and `Ratio()` classes.  
The available options are: [`LevenshteinScorer`](https://en.wikipedia.org/wiki/Levenshtein_distance), [`JaroScorer`](https://en.wikipedia.org/wiki/Jaro–Winkler_distance#Jaro_similarity), [`JaroWinklerScorer`](https://en.wikipedia.org/wiki/Jaro–Winkler_distance#Jaro–Winkler_similarity).   
Different algorithms will produce different results, obviously. By default set to `LevenshteinScorer`.

```python
from stringmatch import Match, LevenshteinScorer, JaroWinklerScorer

levenshtein_matcher = Match(scorer=LevenshteinScorer)
jaro_winkler_matcher = Match(scorer=JaroWinklerScorer)

levenshtein_matcher.match("test", "th test")  # returns True (score = 73)
jaro_winkler_matcher.match("test", "th test") # returns False (score = 60)
```

## Contributing

Contributions to this library are always appreciated! If you have any sort of feedback, or are interested in contributing, head on over to the [Contributing Guidelines](/.github/CONTRIBUTING.md).  
Additionally, if you like this library, leaving a star and spreading the word would be appreciated a lot!  
Thanks in advance for taking the time to do so.

## Links

Packages used:

- [Levenshtein](https://github.com/maxbachmann/Levenshtein)
- [Unidecode](https://github.com/avian2/unidecode)

Related packages:

- [thefuzz](https://github.com/seatgeek/thefuzz)
