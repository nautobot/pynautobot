# v1.1.1

## Fixed

(#43) Incorrect attribute (**display_name**) set for VirtualChassis in `__str__` method of record. Changed to **display**.
(#44) Incorrect method signatures for new `api_version` argument causing data to be set as `api_version`.
(#46) Added assert_called_with() checks to several unit tests; various test refactoring
