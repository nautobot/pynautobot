Retrieving Records
------------------

Pynautobot's :py:class:`<pynautobot.core.endpoint.Endpoint>` objects also provide mechanisms
to retrieve the :py:class:`Records <pynautobot.core.response.Record>` stored in the Nautobot database.
The :py:meth:`~pynautobot.core.endpoint.Endpoint.get` method can be used to retrieve a single :ref:`Record <Terminology>`.
The most common way to use this method is to pass keyword arguments mapping the
Record's :ref:`fields <Terminology>` with its value, such as ``slug="access-switch"``.

.. code-block:: python

    nautobot = api(url=url, token=token)
    device_roles = nautobot.dcim.device_roles

    # Show getting a record using a keyword argument
    access_role = device_roles.get(slug="access-switch")

.. note::
   Multiple keyword arguments can be supplied if needed to uniquely identify a single entry.

The :py:class:`~pynautobot.core.response.Record` object returned by the
:py:meth:`~pynautobot.core.endpoint.Endpoint.get` method is the same object that was returned
from the :py:meth:`~pynautobot.core.endpoint.Endpoint.create` method in :ref:`Creating Records`.

.. code-block:: python

    >>> access_role.name
    'Access Switch'
    >>> access_role.slug
    'access-switch'
    >>> access_role.description
    ''
    >>> # Show that the primary key has the same value from create object
    >>> access_role.id
    '6929b68d-8f87-4470-8377-e7fdc933a2bb'

The :py:meth:`~pynautobot.core.endpoint.Endpoint.all` method is useful
for retrieving all Records of the :ref:`Model <Terminology>`.

.. code-block:: python

    >>> nautobot = api(url=url, token=token)
    >>> device_roles = nautobot.dcim.device_roles

    >>> # Show retrieving all Device Role Records
    >>> all_device_roles = device_roles.all()
    >>> all_device_roles
    ['Spine', 'Leaf', 'Access Switch']

    >>> # Show that the returned objects are record instances
    >>> for role in all_device_roles:
    ...     print(f"Device Role {role.name} has an ID of: {role.id}")
    ... 
    Device Role Spine has an ID of: 6929b68d-8f87-4470-8377-e7fdc933a2bb
    Device Role Leaf has an ID of: 749396ff-692b-448e-9c98-b24f4c7fcb3d
    Device Role Access Switch has an ID of: 6928e7b4-f68e-4b69-bff5-9575c950f713

.. warning::

   Some Models might have large number of Records,
   which could potentially take longer to load and consume a large amount of memory.
