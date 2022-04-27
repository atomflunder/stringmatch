# Changelog

This is a broad overview of the changes that have been made over the lifespan of this library.

## v0.5.0 - 2022-04-27

- Removed scorer argument from functions, added it into `__init__` in both Match() and Ratio()
- Renamed *_with_score functions to *_with_ratio to be consistent with naming
    - This affects the three functions added in v0.4.0
- Removed Exceptions
    - Returning a score of 0 instead of raising EmptySearchException
    - Using "levenshtein" as default instead of raising InvalidScorerException
    - Setting no limit instead of raising InvalidLimitException, if a limit less than 1 is set
    - Updated docstrings to reflect these changes
    - Updated tests to reflect these changes

## v0.4.1 - 2022-04-27

- Added proper Python Versions to setup classifiers

## v0.4.0 - 2022-04-27

- Added match_with_score, get_best_match_with_score and get_best_matches_with_score functions
    - Added tests for those functions
- Updated documentation a bit

## v0.3.1 - 2022-04-26

- Fixed bug where matches are ordered by the default scorer and not the one chosen

## v0.3.0 - 2022-04-26

- Made library installable via pip
- Rebranded library from searchlib to stringmatch

## v0.2.0 - 2022-04-25

- Made library public and installable via git
- Added multiple scorers
- Added new kwargs to Match functions
    - Added tests for those
- Improved various functions
- Added exception type
- Some documentation improvements

## v0.1.0 - 2022-04-24

- Initial commit
- Added basic ratio, string manipulation and matching functions
- Added tests for those
- Added some custom exceptions