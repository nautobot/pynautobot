# v2.3.0

## Added

(#213) Added the ability to retrieve App endpoints via `dir`
(#214) Added support for seeing and modifying notes on all models
(#217) Added the ability to provide custom limit and offset parameters
(#233) Added the ability to run saved GraphQL queries

## Documentation Updates

(#218) Fixed documentation examples for working with prefixes

### Changed

(#224) Changed the `Termination.__str__ ` method to return the display field
(#240) Changed the `.all()` method to accept the same kwargs as `.filter()`, essentially making them redundant of each other
(#243) Updated urllib3 dependency to v2

### Housekeeping

(#220) Added Python 3.12 to test matrix
