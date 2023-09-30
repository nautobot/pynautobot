Updating Records
----------------

Modifying the data in a :ref:`Record <Terminology>` is accomplished by using a Record's
:py:meth:`~pynautobot.core.response.Record.update` method.
This method accepts a dictionary of field/value mappings (Ex: {"description": "Provides access to end hosts"}).
A boolean is returned to indicate whether updates were made to the Record.
The below example shows retrieving a record using the :py:meth:`~pynautobot.core.endpoint.Endpoint.get` method,
and then updating :ref:`fields <Terminology>` in the returned :py:class:`Record <pynautobot.core.response.Record>` object.

.. code-block:: python

    >>> nautobot = api(url=url, token=token)
    >>> roles = nautobot.extras.roles
    >>>
    >>> # Get the record object for the access-switch role
    >>> access_role = roles.get(name="Access Switch")
    >>>
    >>> # Show existing values for name and description fields
    >>> access_role.name
    'Access Switch'
    >>> access_role.description
    ''
    >>>
    >>> # Create a dictionary to update the role fields
    >>> access_switch_updates = {
    ...     "name": "access switch",
    ...     "description": "Provides access to end hosts",
    ... }
    >>>
    >>> # Show using the update method on the role
    >>> access_role.update(access_switch_updates)
    True
    >>>
    >>> # Show that the fields were updated on the existing role
    >>> access_role.name
    'access switch'
    >>> access_role.description
    'Provides access to end hosts'
