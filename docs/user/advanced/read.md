# Retrieving Objects From Nautobot

The `~pynautobot.core.endpoint.Endpoint`{.interpreted-text
role="py:class"} class provides three methods for retrieving
`~pynautobot.core.response.Record`{.interpreted-text role="py:class"}
objects from Nautobot.

-   The `~pynautobot.core.endpoint.Endpoint.get`{.interpreted-text
    role="py:meth"} method is used to get a single Record.
-   The `~pynautobot.core.endpoint.Endpoint.filter`{.interpreted-text
    role="py:meth"} method will return a list of Records.
-   The `~pynautobot.core.endpoint.Endpoint.all`{.interpreted-text
    role="py:meth"} method will return all Records for the Model.

## Using the Get Method

The `Retrieving Records`{.interpreted-text role="ref"} sections shows
how to use the
`~pynautobot.core.endpoint.Endpoint.get`{.interpreted-text
role="py:meth"} method by passing in keyword arguments. Another way to
retrieve a `Record <Terminology>`{.interpreted-text role="ref"} is by
passing in the value of the PK, which is the ID for most objects.

```python
>>> device = nautobot.dcim.devices.get('2302f2a1-2ed4-4ac9-a43a-285c95190071')
>>> device.name
'hq-access-01'
>>> device.status
Active
>>> device.device_type
c9300-48
>>> device.role
<pynautobot.core.response.Record ('Active') at ...>
```

!!! Note

    If an entry with the specified value for the PK does not exist, then `None` in the above example.


When using the
`~pynautobot.core.endpoint.Endpoint.get`{.interpreted-text
role="py:meth"} method with keyword arguments, the keyword arguments
must match only a single Record. If multiple Records are matched, then a
`ValueError` is raised.

```python
>>> device = nautobot.dcim.devices.get(device_type="c9300-48")
Traceback (most recent call last):
...
ValueError: get() returned more than one result.
Check that the kwarg(s) passed are valid for this endpoint
or use filter() or all() instead.
```

## Using the Filter Method

The error message from the previous example suggests to use the
`~pynautobot.core.endpoint.Endpoint.filter`{.interpreted-text
role="py:meth"} method. Using this method will return a list of
`~pynautobot.core.response.Record`{.interpreted-text role="py:class"}
instances; one for each matching **record**. This method also supports:

-   filtering a single `field <Terminology>`{.interpreted-text
    role="ref"} with multiple values
-   filtering based on custom fields
-   filtering with lookup expressions

### Basic Usage

The simplest usage of the
`~pynautobot.core.endpoint.Endpoint.filter`{.interpreted-text
role="py:meth"} method is to pass keyword arguments with single values.
The previous example raised an exception using the
`~pynautobot.core.endpoint.Endpoint.get`{.interpreted-text
role="py:meth"} method, but will return all matches using
`~pynautobot.core.endpoint.Endpoint.filter`{.interpreted-text
role="py:meth"}.

```python
>>> # Get all c9300-48 devices
>>> devices = nautobot.dcim.devices.filter(device_type="c9300-48")
>>>
>>> # Show a list of Records are returned
>>> pprint(devices)
[<pynautobot.models.dcim.Devices ('hq-access-01') at ...>,
 <pynautobot.models.dcim.Devices ('hq-access-02') at ...>,
 <pynautobot.models.dcim.Devices ('hq-access-03') at ...>,
 <pynautobot.models.dcim.Devices ('hq-access-04') at ...>]
>>> 
>>> # Show accessing data from the first c9300-48 device
>>> device1 = devices[0]
>>> device1.name
'hq-access-01'
>>> device1.status
<pynautobot.core.response.Record ('Active') at ...>
```

### Filtering with OR logic

The `~pynautobot.core.endpoint.Endpoint.filter`{.interpreted-text
role="py:meth"} method allows using an **OR** condition by passing in a
list of values to match against the field. The example below gets all
devices located in either *Location* `HQ` or `DC`.

```python
>>> # There are 100 devices total
>>> nautobot.dcim.devices.count()
100
>>>
>>> # There are 20 DC devices
>>> dev_dc_location = nautobot.dcim.devices.filter(location="DC")
>>> len(dev_dc_location)
20
>>>
>>> # There are 5 HQ devices
>>> dev_hq_location = nautobot.dcim.devices.filter(location="HQ")
>>> len(dev_hq_location)
5
>>>
# The filter method will grab all devices in both locations
>>> dev_hq_dc_locations = nautobot.dcim.devices.filter(location=["HQ", "DC"])
>>> len(dev_hq_dc_locations)
25
```

### Filtering based on a Custom Field

Nautobot provides [Custom
Fields](https://nautobot.readthedocs.io/en/latest/additional-features/custom-fields/)
as a way of extending a `Model's <Terminology>`{.interpreted-text
role="ref"} fields. These fields can be referenced in the API by
appending [cf\_]{.title-ref} to the field\'s name. The below example has
a custom field named **owner**, which is used to filter the devices by
passing the `cf_owner` keyword argument.

```python
>>> devices = nautobot.dcim.devices.filter(cf_owner="John Smith")
>>> devices
[<pynautobot.models.dcim.Devices ('switch0') at ...>,
 <pynautobot.models.dcim.Devices ('switch1') at ...>]
>>>
>>> # Show device has an owner of "John Smith"
>>> devices[0].custom_fields["owner"]
'John Smith'
```

### Filtering with Lookup Expressions

The Nautobot API uses [Lookup
Expressions](https://nautobot.readthedocs.io/en/latest/rest-api/filtering/#lookup-expressions)
to filter using something other than the exact matches that have been
used so far. There are several expressions that can be used; they
generally cover things like:

-   greater than
-   less than
-   not equal
-   starts with
-   contains
-   case insensitivity

The example below shows how use negation with *\_\_n*. From the previous
examples, there are 100 devices total, and 25 are located in either the
[DC]{.title-ref} or [HQ]{.title-ref} location. Using `location__n` to
get the negation of these locations returns 75 devices.

```python
>>> devices = nautobot.dcim.devices.filter(location__n=["HQ", "DC"])
>>> len(devices)
75
>>>
>>> # Show the device is not in either HQ or DC location
>>> devices[0].location
<pynautobot.core.response.Record ('branch1') at 0x7f650006df50>
```

## Using the All Method

The `~pynautobot.core.endpoint.Endpoint.all`{.interpreted-text
role="py:meth"} is used to get all records of a specific endpoint. This
will return a list of all
`~pynautobot.core.response.Record`{.interpreted-text role="py:class"}
objects for the specific **Endpoint**.

```python
>>> devices = nautobot.dcim.devices.all()
>>> len(devices)
100
>>> device1 = devices[0]
>>> device1.name
'hq-access-01'
>>> device1.status
Active
```

The following two pages cover interacting with the returned
`~pynautobot.core.response.Record`{.interpreted-text role="py:class"}
objects. The next page covers additional Update operations, which is
followed by a discussion of other features and methods.

## Using Pagination

The Nautobot API supports pagination.  Pynautobot supports this by extending the `filter` and `all` methods the following arguments:

-   limit
-   offset

The `offset` argument can only be used when specifying a `limit`.  However, `limit` can be used without specifying an `offset`.  You could use this to prevent timeouts that result from larger datasets. (By default, pynautobot will request the maximum limit supported by the server)  You can combine this with [threading](../../index.md#threading) to overcome most performance problems.  

This example shows how you could chunk the same large dataset using limit.
```python
>>> devices = nautobot.dcim.devices.all()
>>> len(devices)
100
>>> devices = nautobot.dcim.devices.all(limit=10) # Same result, but chunks to 10 requests
>>> len(devices)
100
```

This example shows how you could offset the results in the same scenario.
```python
>>> devices = nautobot.dcim.devices.all()
>>> len(devices)
100
>>> devices = nautobot.dcim.devices.all(limit=10, offset=10) # Skip the first 10 devices
>>> len(devices)
90
```

This example shows how you could filter and chunk at the same time.
```python
>>> devices = nautobot.dcim.devices.filter(location="DC")
>>> len(devices)
20
>>> devices = nautobot.dcim.devices.filter(location="DC", limit=5) # 4 requests
>>> len(devices)
20
```