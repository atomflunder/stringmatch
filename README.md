# stringmatch

[![PyPI](https://img.shields.io/pypi/v/stringmatch?color=blue)](https://pypi.org/project/stringmatch/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/stringmatch)](https://pypi.org/project/stringmatch/)
[![Downloads](https://pepy.tech/badge/stringmatch)](https://pepy.tech/project/stringmatch)
[![Build](https://github.com/atomflunder/stringmatch/actions/workflows/build.yml/badge.svg)](https://github.com/atomflunder/stringmatch/actions/workflows/build.yml)
[![Documentation Status](https://readthedocs.org/projects/stringmatch/badge/?version=latest)](https://stringmatch.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/atomflunder/stringmatch/branch/master/graph/badge.svg?token=7JIAENN2BZ)](https://codecov.io/gh/atomflunder/stringmatch)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


**stringmatch** is a small, lightweight string matching library written in Python, based on the [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance).  
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
    - [Class Keyword Arguments](#class-keyword-arguments)
    - [Your Own Scorer](#your-own-scorer)
- [🌟 Contributing](#contributing)
- [🔗 Links](#links)
- [⚠️ License](#license)

## Key Features

This library **matches compares and strings to each other** based mainly on, among others, the [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance).  
What makes stringmatch special compared to other libraries with similar functions:

- 💨 Lightweight, straightforward and easy to use
- ⚡ High speed - at least ~12x faster than thefuzz and up to 70x
- 🧰 Allows for highly customisable searches, that yield better results
- 📚 Lots of utility functions to make your life easier
- 📝 Statically typed with mypy, compiled with mypyc
- 🌍 Handles special unicode characters, like emojis or characters from other languages, like ジャパニーズ

## Requirements

- Python 3.9 or later.
- The packages in [`requirements.txt`](/requirements.txt), pip will handle these for you.

## Installation

Install the latest stable version with pip:

```
pip install -U stringmatch
```

Or install the newest version via git (Might be unstable or unfinished):
```
pip install -U git+https://github.com/atomflunder/stringmatch
```

## Basic Usage

Below are some basic examples on how to use this library.  
For a more detailed explanation head over to [the Documentation](https://stringmatch.readthedocs.io/en/latest/).  
For examples on how to use this library, head over to the [`examples` directory](/examples/).  

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
ratio.ratio("stringmatch", "stringmatch")           # returns 100
ratio.ratio("stringmatch", "strngmach")             # returns 90
ratio.ratio("stringmatch", "eh")                    # returns 15

# Getting the ratio between the first string and the list of strings at once:
searches = ["stringmatch", "strngmach", "eh"]
ratio.ratio_list("stringmatch", searches)           # returns [100, 90, 15]

# Searching for partial ratios with substrings:
ratio.partial_ratio("a string", "a string longer")  # returns 80
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
strings.alphanumeric("Héllö, world!")           # returns "Hll world"
strings.ignore_case("test test!", lower=False)  # returns "TEST TEST!"
```

## Advanced Usage

### Keyword Arguments

There are some **optional arguments** available for a few functions.

### `score`

| Type  | Default | Description | Available for: |
| ---   | ---     | ---         | ---            |
| Integer | 70 | The score cutoff for matching. If the score is below the threshold it will not get returned. | All functions from the `Match()` class.

```python
# Example:

from stringmatch import Match

match = Match()

match.match("stringmatch", "strngmach", score=95)    # returns False
match.match("stringmatch", "strngmach", score=70)    # returns True
```

---

### `limit`

| Type  | Default | Description | Available for: |
| ---   | ---     | ---         | ---            |
| Integer | 5 | The limit of how many matches to return. **If you want to return every match set this to 0 or None.** | `get_best_matches()`, `get_best_matches_with_ratio()`

```python
# Example:

from stringmatch import Match

match = Match()

searches = ["limit 5", "limit 4", "limit 3", "limit 2", "limit 1", "limit 0", "something else"]

# returns ["limit 5", "limit 4"]
match.get_best_matches("limit 5", searches, limit=2)

# returns ["limit 5"]
match.get_best_matches("limit 5", searches, limit=1)

# returns ["limit 5", "limit 4", "limit 3", "limit 2", "limit 1", "limit 0"]
match.get_best_matches("limit 5", searches, limit=None) 
```

---

### Class Keyword Arguments

You can also pass in on or more of these **optional arguments when initialising the `Match()` and `Ratio()`** classes to customize your search even further.  
Of course you can use multiple of these keyword arguments at once, to customise the search to do exactly what you intend to do.  

### `scorer`

| Type  | Default | Description |
| ---   | ---     | ---         |
| BaseScorer | LevenshteinScorer | Different scoring algorithms to use. The available options are: [`LevenshteinScorer`](https://en.wikipedia.org/wiki/Levenshtein_distance), [`JaroScorer`](https://en.wikipedia.org/wiki/Jaro–Winkler_distance#Jaro_similarity), [`JaroWinklerScorer`](https://en.wikipedia.org/wiki/Jaro–Winkler_distance#Jaro–Winkler_similarity). 

Click on the links above for detailed information about these, but speaking generally the Jaro Scorer will be the fastest, focussing on the characters the strings have in common.  
The Jaro-Winkler Scorer slightly modified the Jaro Scorer to prioritise characters at the start of the string.  
The Levenshtein Scorer will, most likely, produce the best results, focussing on the number of edits needed to get from one string to the other.

```python
# Example:

from stringmatch import Match, LevenshteinScorer, JaroWinklerScorer

lev_matcher = Match(scorer=LevenshteinScorer)
lev_matcher.match_with_ratio("test", "th test") # returns (True, 73)

jw_matcher = Match(scorer=JaroWinklerScorer)
jw_matcher.match_with_ratio("test", "th test")  # returns (False, 60)
```

---

### `latinise`

| Type  | Default | Description |
| ---   | ---     | ---         |
| Boolean | False | Replaces special unicode characters with their latin alphabet equivalents. Examples: `Ǽ` -> `AE`, `ノース` -> `nosu` 

```python
# Example:

from stringmatch import Match

lat_match = Match(latinise=True)
lat_match.match("séärçh", "search") # returns True

def_match = Match(latinise=False)
def_match.match("séärçh", "search") # returns False
```

---

### `ignore_case`

| Type  | Default | Description |
| ---   | ---     | ---         |
| Boolean | True | If you want to ignore case sensitivity while searching. 

```python
# Example:

from stringmatch import Match

def_match = Match(ignore_case=True)
def_match.match("test", "TEST")   # returns True

case_match = Match(ignore_case=False)
case_match.match("test", "TEST")  # returns False
```

---

### `remove_punctuation`

| Type  | Default | Description |
| ---   | ---     | ---         |
| Boolean | False | Removes commonly used punctuation symbols from the strings, like `.,;:!?` and so on. 

```python
# Example:

from stringmatch import Match

punc_match = Match(remove_punctuation=True)
punc_match.match("test,---....", "test")  # returns True

def_match = Match(remove_punctuation=False)
def_match.match("test,---....", "test")   # returns False
```

---

### `alphanumeric`

| Type  | Default | Description |
| ---   | ---     | ---         |
| Boolean | False | Removes every character that is not a number or in the latin alphabet, a more extreme version of `remove_punctuation`. 

```python
# Example:

from stringmatch import Match

let_match = Match(alphanumeric=True)
let_match.match("»»ᅳtestᅳ►", "test")  # returns True

def_match = Match(alphanumeric=False)
def_match.match("»»ᅳtestᅳ►", "test")  # returns False
```

---

### `include_partial`

| Type  | Default | Description |
| ---   | ---     | ---         |
| Boolean | False | If set to true, also searches for partial substring matches. This may lead to more desirable results but is a bit slower. This will return a score of 65-95 depending on how far apart the sizes of the strings are to ensure only identical matches provide a score of 100. It will start matching at a length of 2, or 1 if it is the first letter of the string.

```python
# Example:

from stringmatch import Match

part_match = Match(include_partial=True)
# returns (True, 65)
part_match.match_with_ratio("A string", "A string thats like really really long", score=60)

def_match = Match(include_partial=False)
# returns (False, 35)
def_match.match_with_ratio("A string", "A string thats like really really long", score=60)
```

---

### Your Own Scorer

If you are unhappy with the scoring algorithms provided, you can of course construct your own scorer class. Make sure it inherits from `BaseScorer` and has a `score()` method that takes 2 strings and returns a float between 0 and 100.

```python
# Example:

from stringmatch import BaseScorer, Match

class MyOwnScorer(BaseScorer):
    def score(self, string1: str, string2: str) -> float:
        # Highly advanced technology
        return 100

my_matcher = Match(scorer=MyOwnScorer)
my_matcher.match_with_ratio("anything", "whatever") # returns (True, 100)
```

## Contributing

Contributions to this library are always appreciated! If you have any sort of feedback, or are interested in contributing, head on over to the [Contributing Guidelines](/.github/CONTRIBUTING.md).  
Additionally, if you like this library, leaving a star and spreading the word would be appreciated a lot!  
Thanks in advance for taking the time to do so.

## Links

Packages used:

- [Mypy](https://github.com/python/mypy) ([Mypyc](https://github.com/mypyc/mypyc))
- [RapidFuzz](https://github.com/maxbachmann/RapidFuzz)
- [Unidecode](https://github.com/avian2/unidecode)

## License

This project is licensed under the [MIT License](/LICENSE).