![pynautobot](docs/nautobot_logo.svg "Nautobot logo")

# Pynautobot
Python API client library for [Nautobot](https://github.com/nautobot/nautobot).

> Pynautobot was initially developed as a fork of [pynetbox](https://github.com/digitalocean/pynetbox/).
  Pynetbox was originally developed by Zach Moody at DigitalOcean and the NetBox Community.


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

## Queries

Pynautobot provides several ways to retrieve objects from Nautobot.
Only the `get()` method is show here.
To continue from the example above, the `Endpoint` object returned will be used to `get`
the device named _hq-access-01_.

```python
switch = devices.get(nam="hq-access-01")
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

Pynautobot supports multithreaded calls for `.filter()` and `.all()` queries. It is **highly recommended** you have `MAX_PAGE_SIZE` in your Nautobot install set to anything *except* `0` or `None`. The default value of `1000` is usually a good value to use. To enable threading, add `threading=True` parameter when instantiating the `Api` object:

```python
nautobot = pynautobot.api(
    url="http://localhost:8000",
    token="d6f4e314a5b5fefd164995169f28ae32d987704f",
    threading=True,
)
```

### Versioning

Used for Nautobot Rest API versioning. Versioning can be controlled globally by setting `api_version` on initialization of the `API` class and/or for a specific request e.g (`list()`, `get()`, `create()` etc.) by setting an optional `api_version` parameter.

__Global versioning__
```python
import pynautobot
nautobot = pynautobot.api(
    url="http://localhost:8000",
    token="d6f4e314a5b5fefd164995169f28ae32d987704f",
    api_version="1.3"
)
```

__Request specific versioning__
```python
import pynautobot
nautobot = pynautobot.api(
  url="http://localhost:8000", token="d6f4e314a5b5fefd164995169f28ae32d987704f",
)
tags = nautobot.extras.tags
tags.create(name="Tag", slug="tag", api_version="1.2",)
tags.list(api_version="1.3",)
```

## Related projects

Please see [our wiki](https://github.com/nautobot/nautobot/wiki/Related-Projects)
for a list of relevant community projects.
