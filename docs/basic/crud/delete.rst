Deleting Records
----------------

Lastly, deleting a Record from the Nautobot database is done by calling
the :py:meth:`~pynautobot.core.response.Record.delete` method on a Record object.
This method will return a boolean to indicate whether or not the Record was successfully deleted.

.. code-block:: python

    >>> nautobot = api(url=url, token=token)
    >>> roles = nautobot.extras.roles
    >>>
    >>> # Get the record object for the access-switch role
    >>> access_role = roles.get(name="Access Switch")
    >>>
    >>> # Show deleting the Record
    >>> access_role.delete()
    True
    >>>
    >>> # Show that the "access-switch" Role was deleted
    >>> pprint(roles.get(name="Access Switch"))
    None
