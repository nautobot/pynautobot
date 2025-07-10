# Changelog

## v1.5.5

- (#330) Updated urlib3 and requests dependencies because of reported CVEs.

## v1.5.4

- (#219) Replaced `pkg_resources` with `importlib.metadata` to enable Python 3.12 support.

## v1.5.3

- (#206) Added python-pynautobot version to default headers.

## v1.5.2

- (#174) Fixes for authentication change in Nautobot.

## v1.5.1

### Bug Fixes

- (#140) Fixes SSL
- (#141) Fixes methods and endpoints naming overlap

## v1.5.0

### New Features

- (#125) Adds Update Method based on ID to keep within the pynautobot experience to update a device (@jamesharr)

```python
    import os
    from pynautobot import api
    url = os.environ["NAUTOBOT_URL"]
    token = os.environ["NAUTOBOT_TOKEN"]
    nautobot = api(url=url, token=token)
    # Update status and name fields
    result = nautobot.dcim.devices.update(
      id="491d799a-eeee-bbbb-aaaa-7c5cbb5b71b6",
      data={
        "comments": "removed from service",
        "status": "decommissioned",
      },
    )
```

## v.1.4.0

### New Features

- (#56) Adds ability to execute a job via pynautobot

> Run an instance of the job

```python
# Gets the job from the list of all jobs
>>> gc_backup_job = nautobot.extras.jobs.all()[14]
>>> job_result = gc_backup_job.run()
>>> job_result.result.id
 '1838f8bd-440f-434e-9f29-82b46549a31d' # <-- Job Result ID.
```

> Running the job with inputs

```python
job = nautobot.extras.jobs.all()[7]
job.run(data={"hostname_regex": ".*"})
```

### Package Updates

- Updates `gitpython` to 3.1.30
-

## v1.3.0

### New Features

- (#85) Added `retries` option to API

### Bug Fixes

- (#94) Fixes API version key for updating records

## v1.2.2

### Bug Fixes

- (#84) Fixes URLs for plugins with nested endpoints (i.e. /api/plugins/app_name/endpoint/nested_endpoint)

## v1.2.1

- (#76) Feature: Removing the restriction on `id` for filter
  > It is now allowed to filter per id. (switch = devices.get(id="..."))
- (#81) Development: Added two invoke tasks:
  - `debug` to get the logs for Nautobot to the screen
  - `stop` to execute `docker-compose down` for started containers

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
