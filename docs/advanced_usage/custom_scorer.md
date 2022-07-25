# Custom Scorer Classes

If you are not satisfied with the included scoring algorithms, you can use the [BaseScorer](../usage/scorer.md) class to construct your own Scorer.  
Simply create a class inheriting the [BaseScorer](../usage/scorer.md) class with a function named `score()` which takes 2 strings as arguments and returns a float between 0 and 100.

Example:

```python
from stringmatch import BaseScorer, Match

class MyOwnScorer(BaseScorer):
    def score(self, string1: str, string2: str) -> float:
        # Highly advanced technology
        return 100

# Using the custom scorer:
my_matcher = Match(scorer=MyOwnScorer)
my_matcher.match_with_ratio("anything", "whatever") # returns (True, 100)
```

A more useful example would be to use a different, established similarity algorithm that is not included here.  
For example you could use the [Damerau-Levenshtein distance](https://en.wikipedia.org/wiki/Damerau–Levenshtein_distance) using the [fastDamerauLevenshtein module](https://github.com/robertgr991/fastDamerauLevenshtein) like this:

```python
from stringmatch import Match, BaseScorer
from fastDamerauLevenshtein import damerauLevenshtein

class DamerauScorer(BaseScorer):
    def score(self, string1: str, string2: str) -> float:
        return damerauLevenshtein(string1, string2, similarity=True) * 100

dl_match = Match(scorer=DamerauScorer)
dl_match.match_with_ratio("stringmatch", "strmatch")     # returns (True, 73)

# For comparison, here is the Levenshtein score:
normal_match = Match()  
normal_match.match_with_ratio("stringmatch", "strmatch") # returns (True, 84)
```

Keep in mind that different scoring algorithms obviously produce differing results. Read the documentation of the modules for more information.  
They will also more than likely have worse performance than the included scorers, mainly because inherited classes cannot be compiled ahead of time with [mypyc](https://github.com/mypyc/mypyc).
