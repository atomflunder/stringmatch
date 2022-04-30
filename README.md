# stringmatch

[![PyPI](https://img.shields.io/pypi/v/stringmatch?color=blue)](https://pypi.org/project/stringmatch/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/stringmatch)](https://pypi.org/project/stringmatch/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/stringmatch)](https://pypi.org/project/stringmatch/)
[![codecov](https://codecov.io/gh/atomflunder/stringmatch/branch/master/graph/badge.svg?token=7JIAENN2BZ)](https://codecov.io/gh/atomflunder/stringmatch)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


**stringmatch** is a small, lightweight string matching library written in Python, based on the [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance) and the [Levenshtein Python C Extension](https://github.com/maxbachmann/Levenshtein).  
Inspired by libraries like [seatgeek/thefuzz](https://github.com/seatgeek/thefuzz), which did not quite fit my needs. And so I am building this library for myself, primarily.

**Disclaimer: This library is still in an alpha development phase!** Changes may be frequent and breaking changes can occur! It is recommended to update frequently to minimise bugs and maximise features.

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
- [⚠️ License](#license)

## Key Features

This library **matches compares and strings to each other** based mainly on, among others, the [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance).  
What makes stringmatch special compared to other libraries with similar functions:

- 💨 Lightweight, straightforward and easy to use
- ⚡ Extremely fast, up to 10x faster than comparable libraries
- 🧰 Allows for highly customisable searches
- 📚 Lots of utility functions to make your life easier
- 🌍 Handles special unicode characters, like emojis or characters from other languages, like ジャパニーズ

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

# Checks if the strings are similar:
match.match("stringmatch", "strngmach")         # returns True
match.match("stringmatch", "something else")    # returns False

# Returns the best match(es) found in the list:
searches = ["stringmat", "strinma", "strings", "mtch", "whatever", "s"]
match.get_best_match("stringmatch", searches)   # returns "stringmat"
match.get_best_matches("stringmatch", searches) # returns ["stringmat", "strinma"]
```

### Ratios

The "ratio of similarity" describes how similar the strings are to each other. It ranges from 100 being an exact match to 0 being something completely different.  
You can get the ratio between strings like this:

```python
from stringmatch import Ratio

ratio = Ratio()

# Getting the ratio between the two strings:
ratio.ratio("stringmatch", "stringmatch")   # returns 100
ratio.ratio("stringmatch", "strngmach")     # returns 90
ratio.ratio("stringmatch", "eh")            # returns 15

# Getting the ratio between the first string and the list of strings at once:
searches = ["stringmatch", "strngmach", "eh"]
ratio.ratio_list("stringmatch", searches)   # returns [100, 90, 15]
```

### Matching & Ratios

You can also get both the match and the ratio together in a tuple using these functions:

```python
from stringmatch import Match

match = Match()

match.match_with_ratio("stringmatch", "strngmach")    # returns (True, 90)

searches = ["test", "nope", "tset"]
match.get_best_match_with_ratio("test", searches)     # returns ("test", 100)
match.get_best_matches_with_ratio("test", searches)   # returns [("test", 100), ("tset", 75)]
```

### Distances

Instead of the ratio, you can also get the Levenshtein distance between strings directly. The bigger the distance, the more different the strings:

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

You can pass in these **optional arguments** for the `Match()` and `Ratio()` functions to customize your search further:

### `score`

| Type  | Default | Description |
| ---   | ---     | ---         |
| Integer | 70 | The score cutoff for matching. Only available for `Match()` functions. 

```python
# Example:

match("stringmatch", "strngmach", score=95)    # returns False
match("stringmatch", "strngmach", score=70)    # returns True
```

---

### `limit`

| Type  | Default | Description |
| ---   | ---     | ---         |
| Integer | 5 | The limit of how many matches to return. **If you want to return every match set this to 0 or None.** Only available for the `get_best_matches()` function.

```python
# Example:

searches = ["limit 5", "limit 4", "limit 3", "limit 2", "limit 1", "limit 0", "something else"]

# returns ["limit 5", "limit 4"]
get_best_matches("limit 5", searches, limit=2)

# returns ["limit 5"]
get_best_matches("limit 5", searches, limit=1)

# returns ["limit 5", "limit 4", "limit 3", "limit 2", "limit 1", "limit 0"]
get_best_matches("limit 5", searches, limit=None) 
```

---

### `latinise`

| Type  | Default | Description |
| ---   | ---     | ---         |
| Boolean | False | Replaces special unicode characters with their latin alphabet equivalents. Examples: `Ǽ` -> `AE`, `ノース` -> `nosu` 

```python
# Example:

match("séärçh", "search", latinise=True)    # returns True
match("séärçh", "search", latinise=False)   # returns False
```

---

### `ignore_case`

| Type  | Default | Description |
| ---   | ---     | ---         |
| Boolean | False | If you want to ignore case sensitivity while searching. 

```python
# Example:

match("test", "TEST", ignore_case=True)     # returns True
match("test", "TEST", ignore_case=False)    # returns False
```

---

### `remove_punctuation`

| Type  | Default | Description |
| ---   | ---     | ---         |
| Boolean | False | Removes commonly used punctuation symbols from the strings, like `.,;:!?` and so on. 

```python
# Example:

match("test,---....", "test", remove_punctuation=True)  # returns True
match("test,---....", "test", remove_punctuation=False) # returns False
```

---

### `only_letters`

| Type  | Default | Description |
| ---   | ---     | ---         |
| Boolean | False | Removes every character that is not in the latin alphabet, a more extreme version of `remove_punctuation`. 

```python
# Example:

match("»»ᅳtestᅳ►", "test", only_letters=True)   # returns True
match("»»ᅳtestᅳ►", "test", only_letters=False)  # returns False
```

---

### Scoring Algorithms

You can pass in different scoring algorithms when initializing the `Match()` and `Ratio()` classes.  
The available options are: [`LevenshteinScorer`](https://en.wikipedia.org/wiki/Levenshtein_distance), [`JaroScorer`](https://en.wikipedia.org/wiki/Jaro–Winkler_distance#Jaro_similarity), [`JaroWinklerScorer`](https://en.wikipedia.org/wiki/Jaro–Winkler_distance#Jaro–Winkler_similarity).   
Different algorithms will produce different results, obviously. By default set to `LevenshteinScorer`.

```python
from stringmatch import Match, LevenshteinScorer, JaroWinklerScorer

lev_matcher = Match(scorer=LevenshteinScorer)
jw_matcher = Match(scorer=JaroWinklerScorer)

lev_matcher.match_with_ratio("test", "th test") # returns (True, 73)
jw_matcher.match_with_ratio("test", "th test")  # returns (False, 60)
```

## Contributing

Contributions to this library are always appreciated! If you have any sort of feedback, or are interested in contributing, head on over to the [Contributing Guidelines](/.github/CONTRIBUTING.md).  
Additionally, if you like this library, leaving a star and spreading the word would be appreciated a lot!  
Thanks in advance for taking the time to do so.

## Links

Packages used:

- [Levenshtein](https://github.com/maxbachmann/Levenshtein)
- [Unidecode](https://github.com/avian2/unidecode)
- [mypyc](https://github.com/mypyc/mypyc)

Related packages:

- [thefuzz](https://github.com/seatgeek/thefuzz)

## License

This project is licensed under the [MIT License](/LICENSE).