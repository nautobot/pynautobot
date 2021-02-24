Deleting Records
----------------

Lastly, deleting a Record from a Model is done by calling
the :py:meth:`~pynautobot.core.response.Record.delete` method on a record object.
This method attempts to delete the Record from the database,
and will return a boolean to indicate whether or not it was successful.

.. code-block:: python

    >>> nautobot = api(url=url, token=token)
    >>> device_roles = nautobot.dcim.device_roles

    >>> # Get the record object for the access-switch device role
    >>> access_role = device_roles.get(slug="access-switch")

    >>> # Show deleting the Record
    >>> access_role.delete()

    >>> # Show that the "access-switch" Device Role was deleted
    >>> device_roles.get(slug="access-switch")
    ValueError ...
