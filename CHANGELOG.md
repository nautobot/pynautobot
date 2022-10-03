# Changelog

## v1.2.1

- (#76) Feature: Removing the restriction on `id` for filter

    It is now allowed to filter per id. (switch = devices.get(id="..."))

## v1.2.0

### Significant Updates

- (#71) Drops support for Python3.6 and updates package dependencies.

### Bug Fixes

- (#75) Fixes child prefixes for the **available-prefixes/ips** endpoint.
- (#72) Updates to account for JSON Custom Field type introduced by Nautobot Custom Fields.

## v1.1.2

### Bug Fixes

- (#57) - Revert wide spread changes introduced in (#41) to resolve `__str__` method for **nat_inside** and **nat_outside** objects. Updated primary `Record.__str__` to use **display** and fallback to previous method.

## v1.1.1

### Bug Fixes

(#43) Incorrect attribute (**display_name**) set for VirtualChassis in `__str__` method of record. Changed to **display**.
(#44) Incorrect method signatures for new `api_version` argument causing data to be set as `api_version`.
(#46) Added assert_called_with() checks to several unit tests; various test refactoring

## v1.1.0 (YANKED)

(#36) Add api_version argument [@timizuoebideri1]

## v1.0.4

(#28) Fix Contraints String Serialization [@david-kn]

## v1.0.3

(#19) Add extras model JobResults [@jmcgill298]
(#14) Fixes writing to plugin endpoint [@Thetacz]

## v1.0.2

### Bug Fixes

#8 Add string interpretation to extras.custom_field_choices endpoint (Fixes #7)

## v1.0.1

Initial Release
