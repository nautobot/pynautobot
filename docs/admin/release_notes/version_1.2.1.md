# v1.2.1

## Added

- (#76) Feature: Removing the restriction on `id` for filter
  > It is now allowed to filter per id. (switch = devices.get(id="..."))

- (#81) Development: Added two invoke tasks:
  - `debug` to get the logs for Nautobot to the screen
  - `stop` to execute `docker-compose down` for started containers
