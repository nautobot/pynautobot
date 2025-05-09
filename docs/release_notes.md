# pynautobot Release Notes

This document describes all new features and changes in the release. The format is based on [Keep a
Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic
Versioning](https://semver.org/spec/v2.0.0.html).

<!-- towncrier release notes start -->
## [v2.6.3](https://github.com/nautobot/pynautobot/releases/tag/v2.6.3)

### Fixed

- [#302](https://github.com/nautobot/pynautobot/issues/302) - Fixed poetry failing to install pynautobot in the development docker image.
- [#307](https://github.com/nautobot/pynautobot/issues/307) - Fixed documentation for the update() method on Endpoint and added type enforcement.
- [#309](https://github.com/nautobot/pynautobot/issues/309) - Fixed JobsEndpoint.run_and_wait() to properly compare the job status as a string to determine if the job is complete.

### Documentation

- Updated the copyright documentation footer.

### Housekeeping

- [#301](https://github.com/nautobot/pynautobot/issues/301) - Replaced black, bandit, flake8 and pydocstyle with ruff.
- [#303](https://github.com/nautobot/pynautobot/issues/303) - Added Python 3.13 to the CI test matrix.
- Consolidated all release notes into a single page for easier searchability and a more streamlined release process.

## [v2.6.2](https://github.com/nautobot/pynautobot/releases/tag/v2.6.2)

### Fixed

- [#295](https://github.com/nautobot/pynautobot/issues/295) - Fixed `parameters` not being parsed correctly for secrets.

### Housekeeping

- [#276](https://github.com/nautobot/pynautobot/issues/276) - Fixed and enabled pylint.
- [#292](https://github.com/nautobot/pynautobot/issues/292) - Fixed mkdocs auto build for CI.
- [#294](https://github.com/nautobot/pynautobot/issues/294) - Use direct import from stdlib instead of requests re-export.

## [v2.6.1](https://github.com/nautobot/pynautobot/releases/tag/v2.6.1)

### Fixed

- [#287](https://github.com/nautobot/pynautobot/issues/287) - Fixed napalm_args not being parsed correctly for platforms.

### Documentation

- [#285](https://github.com/nautobot/pynautobot/issues/285) - Added compatibility matrix for support with Nautobot.

### Housekeeping

- [#283](https://github.com/nautobot/pynautobot/issues/283) - Fixed the release workflow.

## [v2.6.0](https://github.com/nautobot/pynautobot/releases/tag/v2.6.0)

### Added

- [#32](https://github.com/nautobot/pynautobot/issues/32) - Added a `run_and_wait` method to run a Job and wait for it to complete.
- [#263](https://github.com/nautobot/pynautobot/issues/263) - Added support for the Wireless app and endpoints.

### Housekeeping

- [#273](https://github.com/nautobot/pynautobot/issues/273) - Added the towncrier library to dev dependencies to help generate release notes.
- [#275](https://github.com/nautobot/pynautobot/issues/275) - Added support for the `invoke.yml` configuration file.
- [#275](https://github.com/nautobot/pynautobot/issues/275) - Updated `invoke tests` to clean up after itself to be able to run idempotently.
- [#275](https://github.com/nautobot/pynautobot/issues/275) - Changed the CI matrix to only test the latest stable version of Nautobot for normal PRs.
- [#275](https://github.com/nautobot/pynautobot/issues/275) - Disabled CI from running on branch push.
- [#275](https://github.com/nautobot/pynautobot/issues/275) - Added a CI workflow to be able to run tests on a branch manually.
- [#275](https://github.com/nautobot/pynautobot/issues/275) - Changed the tests to clone the nautobot devicetype-library instead of netbox.
- [#275](https://github.com/nautobot/pynautobot/issues/275) - Changed the clone directory of the devicetype-library to use a temporary directory when running in docker.
- [#278](https://github.com/nautobot/pynautobot/issues/278) - Removed the check for changelog fragments during the Manual Tests workflow.

## [v2.5.0](https://github.com/nautobot/pynautobot/releases/tag/v2.5.0)

### Changed

- [#265](https://github.com/nautobot/pynautobot/issues/265) - Dropped support for Python 3.8

### Fixed

- [#266](https://github.com/nautobot/pynautobot/issues/266) - Fixed `Endpoint.choices()` to work for Nautobot 2.4

## [v2.4.2](https://github.com/nautobot/pynautobot/releases/tag/v2.4.2)

### Fixed

- [#257](https://github.com/nautobot/pynautobot/issues/257) - Fixed issue with pagination looping under certain conditions
- [#259](https://github.com/nautobot/pynautobot/issues/259) - Fixed the `filter` field that was missing from dynamic group objects

## [v2.4.1](https://github.com/nautobot/pynautobot/releases/tag/v2.4.1)

### Fixed

- [#253](https://github.com/nautobot/pynautobot/issues/253) - Fixed missing json data returned on cloud endpoints

## [v2.4.0](https://github.com/nautobot/pynautobot/releases/tag/v2.4.0)

### Added

- [#248](https://github.com/nautobot/pynautobot/issues/248) - Added support for new cloud models found in Nautobot 2.3+

## [v2.3.0](https://github.com/nautobot/pynautobot/releases/tag/v2.3.0)

### Added

- [#213](https://github.com/nautobot/pynautobot/issues/213) - Added the ability to retrieve App endpoints via `dir`
- [#214](https://github.com/nautobot/pynautobot/issues/214) - Added support for seeing and modifying notes on all models
- [#217](https://github.com/nautobot/pynautobot/issues/217) - Added the ability to provide custom limit and offset parameters
- [#233](https://github.com/nautobot/pynautobot/issues/233) - Added the ability to run saved GraphQL queries

### Documentation Updates

- [#218](https://github.com/nautobot/pynautobot/issues/218) - Fixed documentation examples for working with prefixes

### Changed

- [#224](https://github.com/nautobot/pynautobot/issues/224) - Changed the `Termination.__str__ ` method to return the display field
- [#240](https://github.com/nautobot/pynautobot/issues/240) - Changed the `.all()` method to accept the same kwargs as `.filter()`, essentially making them redundant of each other
- [#243](https://github.com/nautobot/pynautobot/issues/243) - Updated urllib3 dependency to v2

### Housekeeping    

- [#220](https://github.com/nautobot/pynautobot/issues/220) - Added Python 3.12 to test matrix


## [v2.2.1](https://github.com/nautobot/pynautobot/releases/tag/v2.2.1)

### Changed

- [#195](https://github.com/nautobot/pynautobot/issues/195) - Fixes `Record.__str__` method to use `display` instead of `display_name`
- [#191](https://github.com/nautobot/pynautobot/issues/191) - Replaced pkg_resources with importlib.metadata.

### Housekeeping

- [#190](https://github.com/nautobot/pynautobot/issues/190) - Updated mkdocs.yml to bring it in line with latest template.
- [#193](https://github.com/nautobot/pynautobot/issues/193) - Updated docs CSS files.

## [v2.2.0](https://github.com/nautobot/pynautobot/releases/tag/v2.2.0)

### Added

- [#182](https://github.com/nautobot/pynautobot/issues/182) - Added Dynamic Group Members Detail Endpoint

### Documentation Updates

- [#184](https://github.com/nautobot/pynautobot/issues/184) - Migrated to mkdocs for docs, converted string header to comments

## [v2.1.1](https://github.com/nautobot/pynautobot/releases/tag/v2.1.1)

### Fixed

- [#173](https://github.com/nautobot/pynautobot/issues/173) - Fixes for authentication change in Nautobot.

## [v2.1.0](https://github.com/nautobot/pynautobot/releases/tag/v2.1.0)

### Added

- [#163](https://github.com/nautobot/pynautobot/issues/163) - Adds `Endpoint.delete` method for bulk deleting of records
- [#165](https://github.com/nautobot/pynautobot/issues/165) - Adds `Endpoint.update` method for bulk updating of records

### Fixed

- [#162](https://github.com/nautobot/pynautobot/issues/162) - Corrects signature of `RODetailEndpoint.create` to provide a proper error that it is not implemented when using `api_version`

## [v2.0.2](https://github.com/nautobot/pynautobot/releases/tag/v2.0.2)

### Fixed

- [#148](https://github.com/nautobot/pynautobot/issues/148) - Fixes missing `packages` dependency

## [v2.0.1](https://github.com/nautobot/pynautobot/releases/tag/v2.0.1)

### Fixed

- [#140](https://github.com/nautobot/pynautobot/issues/140) - Fixed SSL
- [#141](https://github.com/nautobot/pynautobot/issues/141) - Fixed methods and endpoints naming overlap

## [v2.0.0](https://github.com/nautobot/pynautobot/releases/tag/v2.0.0)

### Added

- New release for Nautobot 2.0

- [#130](https://github.com/nautobot/pynautobot/issues/130) - Add version constraint on `__init__` to divide 1.X and 2.X.
- [#134](https://github.com/nautobot/pynautobot/issues/134) - Updates in .choices due to changed `OPTIONS` schema
- [#135](https://github.com/nautobot/pynautobot/issues/135) - Docs Update

## [v1.5.2](https://github.com/nautobot/pynautobot/releases/tag/v1.5.2)

### Fixed

- [#174](https://github.com/nautobot/pynautobot/issues/174) - Fixes for authentication change in Nautobot.

## [v1.5.0](https://github.com/nautobot/pynautobot/releases/tag/v1.5.0)

### Added

- [#125](https://github.com/nautobot/pynautobot/issues/125) - Adds Update Method based on ID to keep within the pynautobot experience to update a device [@jamesharr](https://github.com/jamesharr)

## [v1.4.0](https://github.com/nautobot/pynautobot/releases/tag/v1.4.0)

### Added

- [#56](https://github.com/nautobot/pynautobot/issues/56) - Adds ability to execute a job via pynautobot

### Housekeeping

- Updates `gitpython` to `3.1.30`

## [v1.3.0](https://github.com/nautobot/pynautobot/releases/tag/v1.3.0)

### Added

- [#85](https://github.com/nautobot/pynautobot/issues/85) - Added `retries` option to API

## [v1.2.2](https://github.com/nautobot/pynautobot/releases/tag/v1.2.2)

### Fixed

- [#84](https://github.com/nautobot/pynautobot/issues/84) - Fixes URLs for plugins with nested endpoints (i.e. /api/plugins/app_name/endpoint/nested_endpoint)

## [v1.2.1](https://github.com/nautobot/pynautobot/releases/tag/v1.2.1)

### Added

- [#76](https://github.com/nautobot/pynautobot/issues/76) - Feature: Removing the restriction on `id` for filter
  > It is now allowed to filter per id. (switch = devices.get(id="..."))

- [#81](https://github.com/nautobot/pynautobot/issues/81) - Development: Added two invoke tasks:
  - `debug` to get the logs for Nautobot to the screen
  - `stop` to execute `docker-compose down` for started containers

## [v1.2.0](https://github.com/nautobot/pynautobot/releases/tag/v1.2.0)

### Updated

- [#71](https://github.com/nautobot/pynautobot/issues/71) - Drops support for Python3.6 and updates package dependencies.

### Fixed

- [#75](https://github.com/nautobot/pynautobot/issues/75) - Fixes child prefixes for the **available-prefixes/ips** endpoint.
- [#72](https://github.com/nautobot/pynautobot/issues/72) - Updates to account for JSON Custom Field type introduced by Nautobot Custom Fields.

## [v1.1.2](https://github.com/nautobot/pynautobot/releases/tag/v1.1.2)

### Fixed

- [#57](https://github.com/nautobot/pynautobot/issues/57) - Revert wide spread changes introduced in (#41) to resolve `__str__` method for **nat_inside** and **nat_outside** objects. Updated primary `Record.__str__` to use **display** and fallback to previous method.

## [v1.1.1](https://github.com/nautobot/pynautobot/releases/tag/v1.1.1)

### Fixed

- [#43](https://github.com/nautobot/pynautobot/issues/43) - Incorrect attribute (**display_name**) set for VirtualChassis in `__str__` method of record. Changed to **display**.

## [v1.1.0](https://github.com/nautobot/pynautobot/releases/tag/v1.1.0)

### Added

- [#36](https://github.com/nautobot/pynautobot/issues/36) - Add api_version argument [@timizuoebideri1](https://github.com/timizuoebideri1)

## [v1.0.4](https://github.com/nautobot/pynautobot/releases/tag/v1.0.4)

### Fixed

- [#28](https://github.com/nautobot/pynautobot/issues/28) - Fix Contraints String Serialization [@david-kn](https://github.com/david-kn)

## [v1.0.3](https://github.com/nautobot/pynautobot/releases/tag/v1.0.3)

### Added

- [#19](https://github.com/nautobot/pynautobot/issues/19) - Add extras model JobResults [@jmcgill298](https://github.com/jmcgill298)

### Fixed

- [#14](https://github.com/nautobot/pynautobot/issues/14) - Fixes writing to plugin endpoint [@Thetacz](https://github.com/Thetacz)

## [v1.0.2](https://github.com/nautobot/pynautobot/releases/tag/v1.0.2)

### Fixed

- [#7](https://github.com/nautobot/pynautobot/issues/7) - Add string interpretation to extras.custom_field_choices endpoint

## v1.0.0

### Release Overview

This is the first official release of the `pynautobot` library.
This project is forked from the `pynetbox` library.
