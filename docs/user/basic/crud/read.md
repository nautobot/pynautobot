# Retrieving Records

Pynautobot\'s `<pynautobot.core.endpoint.Endpoint>`{.interpreted-text
role="py:class"} objects also provide mechanisms to retrieve the
`Records <pynautobot.core.response.Record>`{.interpreted-text
role="py:class"} stored in the Nautobot database. The
`~pynautobot.core.endpoint.Endpoint.get`{.interpreted-text
role="py:meth"} method can be used to retrieve a single
`Record <Terminology>`{.interpreted-text role="ref"}. The most common
way to use this method is to pass keyword arguments mapping the
Record\'s `fields <Terminology>`{.interpreted-text role="ref"} with its
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

The `~pynautobot.core.response.Record`{.interpreted-text
role="py:class"} object returned by the
`~pynautobot.core.endpoint.Endpoint.get`{.interpreted-text
role="py:meth"} method is the same object that was returned from the
`~pynautobot.core.endpoint.Endpoint.create`{.interpreted-text
role="py:meth"} method in `Creating Records`{.interpreted-text
role="ref"}.

``` python
>>> access_role.name
'Access Switch'
>>> access_role.description
''
>>> # Show that the primary key has the same value from create object
>>> access_role.id
'6929b68d-8f87-4470-8377-e7fdc933a2bb'
```

The `~pynautobot.core.endpoint.Endpoint.all`{.interpreted-text
role="py:meth"} method is useful for retrieving all Records of the
`Model <Terminology>`{.interpreted-text role="ref"}.

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
