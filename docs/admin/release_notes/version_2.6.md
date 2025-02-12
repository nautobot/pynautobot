# v2.6 Release Notes

This document describes all new features and changes in the release. The format is based on [Keep a
Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic
Versioning](https://semver.org/spec/v2.0.0.html).

## [v2.6.0 (2025-02-12)](https://github.com/nautobot/pynautobot/releases/tag/v2.6.0)

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
