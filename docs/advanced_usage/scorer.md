# Scorer Classes

These are the different scoring algorithms included in this library.  
To construct your own scorer, please take a look at the [Custom Scorer classes page](custom_scorer.md)

| Name | Quick Explanation | Wikipedia |
|---|---|----|
LevenshteinScorer | This is the default scorer, focussing on the number of edits needed to transform one string to the other, and will generally yield the most desirable results. | [Link](https://en.wikipedia.org/wiki/Levenshtein_distance)
JaroScorer | This scorer focusses on the characters in common between the two strings, it will generally be the fastest of the three. | [Link](https://en.wikipedia.org/wiki/Jaro–Winkler_distance#Jaro_similarity)
JaroWinklerScorer | This scorer slightly modifies the JaroScorer, prioritising the characters near the start of the string. | [Link](https://en.wikipedia.org/wiki/Jaro–Winkler_distance#Jaro–Winkler_similarity)

Examples:

```python
from stringmatch import Match, LevenshteinScorer, JaroScorer, JaroWinklerScorer

lev_match = Match(scorer=LevenshteinScorer)
lev_match.match_with_ratio("stringmatch", "strmatch")   # returns (True, 84)

jaro_match = Match(scorer=JaroScorer)
jaro_match.match_with_ratio("stringmatch", "strmatch")  # returns (True, 91)

jw_match = Match(scorer=JaroWinklerScorer)
jw_match.match_with_ratio("stringmatch", "strmatch")    # returns (True, 94)
```

