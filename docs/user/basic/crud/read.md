# Retrieving Records

Pynautobot's [`Endpoint`][pynautobot.core.endpoint.Endpoint] objects also provide mechanisms to retrieve the
[Records][pynautobot.core.response.Record] stored in the Nautobot database. The
[`get()`][pynautobot.core.endpoint.Endpoint.get] method can be used to retrieve a single
[Record](../index.md#terminology). The most common
way to use this method is to pass keyword arguments mapping the
Record's [fields](../index.md#terminology) with its
value, such as `name="Access Switch"`.

``` python
>>> nautobot = api(url=url, token=token)
>>> roles = nautobot.extras.roles
>>>
>>> # Show getting a record using a keyword argument
>>> access_role = roles.get(name="Access Switch")
```

!!! Note
    Multiple keyword arguments can be supplied if needed to uniquely identify a single entry.

The [`Record`][pynautobot.core.response.Record] object returned by the
[`get()`][pynautobot.core.endpoint.Endpoint.get] method is the same object that was returned from the
[`create()`][pynautobot.core.endpoint.Endpoint.create] method in [Creating Records](../../advanced/create.md).

``` python
>>> access_role.name
'Access Switch'
>>> access_role.description
''
>>> # Show that the primary key has the same value from create object
>>> access_role.id
'6929b68d-8f87-4470-8377-e7fdc933a2bb'
```

The [`all()`][pynautobot.core.endpoint.Endpoint.all] method is useful for retrieving all Records of the
[Model](../index.md#terminology).

``` python
>>> nautobot = api(url=url, token=token)
>>> roles = nautobot.extras.roles
>>>
>>> # Show retrieving all Role Records
>>> all_roles = roles.all()
>>> first_3_roles = all_roles[:3]
>>> first_3_roles
[<pynautobot.core.response.Record ('loopback') at 0x7f65000837d0>, <pynautobot.core.response.Record ('mgmt') at 0x7f6500084090>, <pynautobot.core.response.Record ('point-to-point') at 0x7f650007de10>]
>>>
>>> # Show that the returned objects are record instances
>>> for role in first_3_roles:
...     print(f"Role {role.name} has an ID of: {role.id}")
... 
Role loopback has an ID of: 866eaed3-2d12-49f8-9702-7dc1c2f3b053
Role mgmt has an ID of: a1b9bb07-da6d-458a-8fd5-bf1f993da85a
Role point-to-point has an ID of: f3d0ac02-23d0-4b2d-9f2b-afd4875f5f0f
```

!!! Warning
    Some Models might have large number of Records, which could potentially take longer to load and consume a large amount of memory.
