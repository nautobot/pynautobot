Deleting Records
----------------

Lastly, deleting a Record from the Nautobot database is done by calling
the :py:meth:`~pynautobot.core.response.Record.delete` method on a Record object.
This method will return a boolean to indicate whether or not the Record was successfully deleted.

.. code-block:: python

    >>> nautobot = api(url=url, token=token)
    >>> device_roles = nautobot.dcim.device_roles

    >>> # Get the record object for the access-switch device role
    >>> access_role = device_roles.get(slug="access-switch")

    >>> # Show deleting the Record
    >>> access_role.delete()
    True

    >>> # Show that the "access-switch" Device Role was deleted
    >>> device_roles.get(slug="access-switch")
    ValueError ...
