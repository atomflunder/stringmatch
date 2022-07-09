# Basic Usage

Once you installed the library, you can start to use it like this:

Setup:
```python
from stringmatch import Match

# Initialises the Match class, for later use.
match = Match()
```

Very basic check if the strings are similar:
```python
match.match("stringmatch", "strngmach")         # returns True
match.match("stringmatch", "something else")    # returns False
```

Getting the best match from a list:
```python
searches = ["stringmat", "strinma", "strings", "mtch", "whatever", "s"]

match.get_best_match("stringmatch", searches)   # returns "stringmat"
match.get_best_matches("stringmatch", searches) # returns ["stringmat", "strinma"]
```

Getting matches together with the percentage of similarity, called ratio.
```python
match.match_with_ratio("stringmatch", "strngmach")    # returns (True, 90)

searches = ["test", "nope", "tset"]
match.get_best_match_with_ratio("test", searches)     # returns ("test", 100)
match.get_best_matches_with_ratio("test", searches)   # returns [("test", 100), ("tset", 75)]
```

These are just the very basics, please see the Usage section on the sidebar for a detailed explanation of the whole library, or the Examples section for some real world use cases.

The [`README.md`](https://github.com/atomflunder/stringmatch/blob/master/README.md) file on GitHub also covers much of the same topics in a condensed format.
