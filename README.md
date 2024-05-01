<p align="center">
  <img src="https://raw.githubusercontent.com/nautobot/pynautobot/develop/docs/nautobot_logo.png" class="logo" height="200px">
  <br>
  <a href="https://github.com/nautobot/pynautobot/actions"><img src="https://github.com/nautobot/pynautobot/actions/workflows/ci.yml/badge.svg?branch=main"></a>
  <a href="https://pynautobot.readthedocs.io/en/latest"><img src="https://readthedocs.org/projects/pynautobot/badge/"></a>
  <a href="https://pypi.org/project/pynautobot/"><img src="https://img.shields.io/pypi/v/pynautobot"></a>
  <a href="https://pypi.org/project/pynautobot/"><img src="https://img.shields.io/pypi/dm/pynautobot"></a>
  <br>
</p>

# pynautobot

Python API client library for [Nautobot](https://github.com/nautobot/nautobot).

> pynautobot was initially developed as a fork of [pynetbox](https://github.com/digitalocean/pynetbox/).
> pynetbox was originally developed by Zach Moody at DigitalOcean and the NetBox Community.

The complete documentation for pynautobot can be found at [Read the Docs](https://pynautobot.readthedocs.io/en/stable/).

Questions? Comments? Join us in the **#nautobot** Slack channel on [Network to Code](https://networktocode.slack.com)!

## Installation

You can install via [pip](#using-pip) or [poetry](#using-poetry)

### Using pip

```shell
$ pip install pynautobot
...
```

### Using poetry

```shell
$ git clone https://github.com/nautobot/pynautobot.git
...
$ pip install poetry
...
$ poetry shell
Virtual environment already activated: /home/user/pynautobot/.venv
$ poetry install
...
```

## Quick Start

A short introduction is provided here; the full documention for pynautobot is at [Read the Docs](http://pynautobot.readthedocs.io/).

To begin, import pynautobot and instantiate an `Api` object, passing the `url` and `token`.

```python
import pynautobot
nautobot = pynautobot.api(
    url="http://localhost:8000",
    token="d6f4e314a5b5fefd164995169f28ae32d987704f",
)
```

The Api object provides access to the Apps in Nautobot.
The Apps provide access to the Models and the field data stored in Nautobot.
Pynautobot uses the `Endpoint` class to represent Models.
For example, here is how to access **Devices** stored in Nautobot:

```python
devices = nautobot.dcim.devices
devices
<pynautobot.core.endpoint.Endpoint object at 0x7fe801e62fa0>
```

## Jobs

Pynautobot provides a specialized `Endpoint` class to represent the Jobs model. This class is called `JobsEndpoint`.
This extends the `Endpoint` class by adding the `run` method so pynautobot can be used to call/execute a job run.

1. Run from an instance of a job.

```python
>>> gc_backup_job = nautobot.extras.jobs.all()[14]
>>> job_result = gc_backup_job.run()
>>> job_result.result.id
'1838f8bd-440f-434e-9f29-82b46549a31d' # <-- Job Result ID.
```

2. Run with Job Inputs

```python
job = nautobot.extras.jobs.all()[7]
job.run(data={"hostname_regex": ".*"})
```

3. Run by providing the job id

```python
>>> gc_backup_job = nautobot.extras.jobs.run(class_path=nautobot.extras.jobs.all()[14].id)
>>> gc_backup_job.result.id
'548832dc-e586-4c65-a7c1-a4e799398a3b' # <-- Job Result ID.
```

## Queries

Pynautobot provides several ways to retrieve objects from Nautobot.
Only the `get()` method is shown here.
To continue from the example above, the `Endpoint` object returned will be used to `get`
the device named _hq-access-01_.

```python
switch = devices.get(name="hq-access-01")
```

The object returned from the `get()` method is an implementation of the `Record` class.
This object provides access to the field data from Nautobot.

```python
switch.id
'6929b68d-8f87-4470-8377-e7fdc933a2bb'
switch.name
'hq-access-01'
switch.site
hq
```

### Threading

Pynautobot supports multithreaded calls for `.filter()` and `.all()` queries. It is **highly recommended** you have `MAX_PAGE_SIZE` in your Nautobot install set to anything _except_ `0` or `None`. The default value of `1000` is usually a good value to use. To enable threading, add `threading=True` parameter when instantiating the `Api` object:

```python
nautobot = pynautobot.api(
    url="http://localhost:8000",
    token="d6f4e314a5b5fefd164995169f28ae32d987704f",
    threading=True,
)
```

### Versioning

Used for Nautobot Rest API versioning. Versioning can be controlled globally by setting `api_version` on initialization of the `API` class and/or for a specific request e.g (`all()`, `filter()`, `get()`, `create()` etc.) by setting an optional `api_version` parameter.

**Global versioning**

```python
import pynautobot
nautobot = pynautobot.api(
    url="http://localhost:8000",
    token="d6f4e314a5b5fefd164995169f28ae32d987704f",
    api_version="2.1"
)
```

**Request specific versioning**

```python
import pynautobot
nautobot = pynautobot.api(
  url="http://localhost:8000", token="d6f4e314a5b5fefd164995169f28ae32d987704f",
)
tags = nautobot.extras.tags
tags.create(name="Tag", api_version="2.0", content_types=["dcim.device"])
tags.get(api_version="2.1",)
```

### Retry logic

By default, the client will not retry any operation. This behavior can be adjusted via the `retries` optional parameters. This will only affect HTTP codes: 429, 500, 502, 503, and 504.

**Retries**

```python
import pynautobot
nautobot = pynautobot.api(
    url="http://localhost:8000",
    token="d6f4e314a5b5fefd164995169f28ae32d987704f",
    retries=3
)
```

## Related projects

Please see [our wiki](https://github.com/nautobot/nautobot/wiki/Related-Projects)
for a list of relevant community projects.
