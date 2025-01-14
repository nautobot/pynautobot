# v1.2.0

### Updated

- (#71) Drops support for Python3.6 and updates package dependencies.

### Fixed

- (#75) Fixes child prefixes for the **available-prefixes/ips** endpoint.
- (#72) Updates to account for JSON Custom Field type introduced by Nautobot Custom Fields.

## v1.2.2

### Fixed

- (#84) Fixes URLs for plugins with nested endpoints (i.e. /api/plugins/app_name/endpoint/nested_endpoint)

## v1.2.1

### Added

- (#76) Feature: Removing the restriction on `id` for filter
  > It is now allowed to filter per id. (switch = devices.get(id="..."))

- (#81) Development: Added two invoke tasks:
  - `debug` to get the logs for Nautobot to the screen
  - `stop` to execute `docker-compose down` for started containers


