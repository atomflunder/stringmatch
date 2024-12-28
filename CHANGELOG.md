# Changelog

This is a broad overview of the changes that have been made over the lifespan of this library.

## v0.14.6 - 2024-12-28

- Update wheels & workflows

## v0.14.5 - 2024-11-15

- Added support for Python 3.13

## v0.14.4 - 2024-09-24

- Dropped support for Python 3.8

## v0.14.3 - 2023-10-02

- Add Python 3.12 support

## v0.14.2 - 2023-06-06

- Upgrade to rapidfuzz Version 3.x

## v0.14.1 - 2022-10-12

- Add Python 3.11 support

## v0.14.0 - 2022-07-29

- Added support for Python 3.8
    - Support for 3.7 and below is unlikely since we make some use of the walrus operator
    - 3.6 and below are EoL anyways and 3.7 is due to follow in 2023

## v0.13.0 - 2022-07-25

- Removed Levenshtein as a dependency and replaced it with RapidFuzz
    - Under the hood Levenshtein was basically only calling RapidFuzz functions anyways, so we save ourselves the overhead
    - As a result stringmatch is now a tiny bit faster
- Custom Scorers now need to return a float between 0 and 100, instead of 0 and 1

## v0.12.5 - 2022-07-09

- Removed Ratio Keyword Arguments Class
    - Constructing the Ratio Class just manually now
    - This should be a tiny bit faster, but not noticeable by any means
- Adding docs
- Added examples in docstrings

## v0.12.4 - 2022-07-06

- Removed the specific rapidfuzz version from the list of installed packages
    - The error encountered earlier seemed to have gone away

## v0.12.3 - 2022-07-05

- Added mypy to the required packages, fixed installation

## v0.12.2 - 2022-07-05

- Bumped Version to make installation process easier

## v0.12.1 - 2022-07-05

- Fixed Custom Scorers being broken accidentally

## v0.12.0 - 2022-07-04

- Using mypyc to compile (again)
    - Various smaller changes to accomodate mypyc
    - Roughly doubles speed of library
- Holding rapidfuzz to 2.0.15 for now, 2.1.0 and above will break the library.
    - This is because editops are not implemented (yet), hopefully this will change soon.

## v0.11.1 - 2022-06-29

- Improved performance further (more than 2x improvement)
- partial_ratio now returns 0 instead of an error when a non-string is present

## v0.11.0 - 2022-06-28

- Renamed _Scorer class to BaseScorer
- Improved performance slightly

## v0.10.13 - 2022-05-05

- Added py.typed file
- Added some examples in a new examples directory
    - This includes a benchmark with thefuzz

## v0.10.12 - 2022-05-04

- Set ignore_case kwarg by default to True
- Renamed only_letters kwarg to alphanumeric to better reflect what it actually does

## v0.10.11 - 2022-05-03

- Adjusted sorting algorithm for functions that return multiple results
    - Should yield a bit better results when ratios are tied

## v0.10.10 - 2022-05-03

- Adjusted partial matching a tiny bit more
- Adjusted tests accordingly

## v0.10.9 - 2022-05-03

- Preventing raising errors when passing in non-strings
    - Just returning 0 in these cases
- Added scorer subclass example to Readme

## v0.10.8 - 2022-05-03

- Adjusted partial matching a tiny bit more
- Added tests to verify

## v0.10.7 - 2022-05-03

- Added type hints for kwargs
- Added some more tests

## v0.10.6 - 2022-05-02

- Cleaned up some internal code

## v0.10.5 - 2022-05-02

- Fixed indentation of score append in partial ratio function

## v0.10.4 - 2022-05-02

- Fixed kwargs not being passed correctly by get_best_match function.
- Adjusted partial matching a tiny bit more

## v0.10.3 - 2022-05-02

- Adjusted partial matching a tiny bit more

## v0.10.2 - 2022-05-02

- Improved partial matching a lot
    - Should now yield way better results
    - Updated tests and docs to reflect the changes made

## v0.10.1 - 2022-05-02

- Fixed score argument not being properly recognised

## v0.10.0 - 2022-05-02

- You now need to pass in special keyword only arguments when initialising the class, not the functions
    - This eliminates a lot of re-used code, and is more simple to use
    - Deleted args module as a result
    - Updated tests and docs to reflect those changes

## v0.9.0 - 2022-05-01

- Added partial ratio function
- Added include_partial keyword to most matching functions
    - These will both search for partial substrings within the strings for better results
    - Updated docs to reflect those changes
    - Added test cases to make sure everything works as intended
- Added numbers to only_letters keyword
    - Might re-name that in the future
- Added args module for cleanup

## v0.8.1 - 2022-05-01

- Moved scorer into its own module
    - Clarified Readme section about scorers

## v0.8.0 - 2022-05-01

- Reverting v0.7.0 changes with mypyc
    - This was causing too many issues, sorry

## v0.7.1 - 2022-05-01

- Fixed installation for pip
- Added link to Readme
- Added verbose flag

## v0.7.0 - 2022-05-01

- Using mypyc now
    - Should bring a significant speed boost
    - Added mypy to requirements
    - Added build-system section to pyproject.toml

## v0.6.6 - 2022-04-30

- Added typehints for kwargs in preparation for using mypyc (maybe)

## v0.6.5 - 2022-04-30

- Fixed kwargs not being passed from the ratio_list function
    - Added tests to make sure it works now
- Added coverage workflow and badges

## v0.6.4 - 2022-04-29

- Updated and clarified readme in some sections, added new examples
    - Added tests to make sure these examples are correct
- Letting tests fail now when under 100% code coverage
- Fixed encoding in setup.py file

## v0.6.3 - 2022-04-28

- Updated templates
- Fixed building of library including old unused files

## v0.6.2 - 2022-04-28

- Fixed keyword arguments not being recognised still

## v0.6.1 - 2022-04-28

- Fixed ranking of matches with keyword arguments

## v0.6.0 - 2022-04-28

- Added distance functions
    - These are: distance and distance_list
- Added new Class _Scorer with LevenshteinScorer, JaroScorer and JaroWinklerScorer subclasses
    - You need to pass these in now instead of a string when initialising Match() and Ratio() with different scorers

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