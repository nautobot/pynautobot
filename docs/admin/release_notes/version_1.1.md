# v1.1.0 (YANKED)

* Added new `api_version` argument.

### Added 

(#36) Add api_version argument [@timizuoebideri1]

## v1.1.2

### Fixed

- (#57) - Revert wide spread changes introduced in (#41) to resolve `__str__` method for **nat_inside** and **nat_outside** objects. Updated primary `Record.__str__` to use **display** and fallback to previous method.

## v1.1.1

### Fixed

(#43) Incorrect attribute (**display_name**) set for VirtualChassis in `__str__` method of record. Changed to **display**.
(#44) Incorrect method signatures for new `api_version` argument causing data to be set as `api_version`.
(#46) Added assert_called_with() checks to several unit tests; various test refactoring
