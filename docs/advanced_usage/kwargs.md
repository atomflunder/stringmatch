# Keyword Arguments

This is a short explanation of the optional keyword arguments you can use when initialising the Ratio and Match classes.  
Except for `include_partial`, which has its own page [here](partial_matches.md).

## `latinise`

By default set to `False`. Replaces non-latin unicode characters from differing alphabets with a latin transliteration using the [Unidecode](https://github.com/avian2/unidecode) library.

Example:

```python
from stringmatch import Match

lat_match = Match(latinise=True)
lat_match.match("στρινγματχ", "stringmatch")    # returns True

def_match = Match(latinise=False)
def_match.match("στρινγματχ", "stringmatch")    # returns False
```

## `ignore_case`

By default set to `True`. Ignores case sensitivity while comparing strings.

```python
from stringmatch import Match

def_match = Match(ignore_case=True)
def_match.match("test", "TEST")   # returns True

case_match = Match(ignore_case=False)
case_match.match("test", "TEST")  # returns False
```

## `remove_punctuation`

By default set to `False`. Removes commonly used punctuation symbols from the strings, which are:  

    !\"#'()*+,-./:;<=>?[]^_`{|}~’„“»«

Example:

```python
from stringmatch import Match

punc_match = Match(remove_punctuation=True)
punc_match.match("test,---....", "test")  # returns True

def_match = Match(remove_punctuation=False)
def_match.match("test,---....", "test")   # returns False
```

## `alphanumeric`

By default set to `False`. Removes every character that is not a number, a space or in the latin alphabet, which are:

    1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 

Example:

```python
from stringmatch import Match

let_match = Match(alphanumeric=True)
let_match.match("»»ᅳtestᅳ►", "test")  # returns True

def_match = Match(alphanumeric=False)
def_match.match("»»ᅳtestᅳ►", "test")  # returns False
```

## `include_partial`

Again, include partial has its own in-depth explanation [here](partial_matches.md).
