# Pynautobot
Python API client library for [Nautobot](https://github.com/nautobot-community/nautobot).
Pynautobot is a fork of pynetbox, developed to add functionality specific to Nautobot.


## Installation

To install run `pip install pynautobot`.

Alternatively, you can clone the repo and run `python setup.py install`.


## Quick Start

The full pynautobot API is documented on [Read the Docs](http://pynautobot.readthedocs.io/en/latest/), but the following should be enough to get started using it.

To begin, import pynautobot and instantiate the API.

```
import pynautobot
nb = pynautobot.api(
    'http://localhost:8000',
    token='d6f4e314a5b5fefd164995169f28ae32d987704f'
)
```

The first argument the .api() method takes is the Nautobot URL. There are a handful of named arguments you can provide, but in most cases none are required to simply pull data. In order to write, the `token` argument should to be provided.


## Queries

The pynautobot API is setup so that Nautobot's apps are attributes of the `.api()` object, and in turn those apps have attribute representing each endpoint. Each endpoint has a handful of verbs available to carry out actions on the endpoint. For example, in order to query all the objects in the devices endpoint you would do the following:

```
nb.dcim.devices.all()
[test1-leaf1, test1-leaf2]
```

### Threading

pynautobot supports multithreaded calls (in Python 3 only) for `.filter()` and `.all()` queries. It is **highly recommended** you have `MAX_PAGE_SIZE` in your Nautobot install set to anything *except* `0` or `None`. The default value of `1000` is usually a good value to use. To enable threading, add `threading=True` parameter to the `.api`:

```python
nb = pynautobot.api(
    'http://localhost:8000',
    threading=True,
)
```
