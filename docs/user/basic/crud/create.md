# Creating a Record

New `Records <Terminology>`{.interpreted-text role="ref"} can be created
using an Endpoint\'s
`~pynautobot.core.endpoint.Endpoint.create`{.interpreted-text
role="py:meth"} method. All fields supported by the Model in Nautobot
can be passed into the method, and every required field must be passed.

``` python
>>> nautobot = api(url=url, token=token)
>>> roles = nautobot.extras.roles
>>>
>>> # Create a dict of keyword arguments to use for role config.
>>> access_role_config = {
...     "name": "Access Switch",
...     "content_types": ["dcim.device"],
... }
>>>
>>> # Create a new Record in the Roles Model.
>>> access_role = roles.create(**access_role_config)
```

The `~pynautobot.core.endpoint.Endpoint.create`{.interpreted-text
role="py:meth"} method adds a new Record into the Nautobot database, and
a representative `~pynautobot.core.response.Record`{.interpreted-text
role="py:class"} object is returned. This record object has attributes
for each `field <Terminology>`{.interpreted-text role="ref"} in the
database table. The following code block is a continuation of the
previous one.

``` python
>>> # Show that fields passed to the create method
>>> # are accessible attributes with expected values
>>> access_role.name
'Access Switch'
>>>
>>> # Show that fields not passed to the method
>>> # were assigned values by the Model
>>> access_role.description
''
>>> access_role.id
'6929b68d-8f87-4470-8377-e7fdc933a2bb'
```
