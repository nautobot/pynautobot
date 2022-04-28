Creating Records
================

The :ref:`Creating a Record` section provides an example of creating a single
:py:class:`~pynautobot.core.response.Record` for a :ref:`Model <Terminology>` without any foreign key relationships.
Additionally, some :ref:`fields <Terminology>` are an enum type, which limits the acceptable values to a set of `choices`.

This section demonstrates workflows for:

1. Creating :ref:`Records <Terminology>` with enum fields and foreign key relationships.
2. Creating multiple Records with a single method call.

Finally, some common errors are shown, and the Exceptions that are then raised by these errors.


Obtaining Choices
-----------------

For fields that are enum type, Endpoint objects have a :py:meth:`~pynautobot.core.endpoint.Endpoint.choices`
method to provide a mapping of enum fields to their list of acceptable choices.
The examples used in the document revolve around creating a new Device Record.
Creating a *Device* requires specifying the ``status`` field, which is an example of an enum.
Below demonstrates how to view the list of available choices for Device Status.

.. code-block:: python

    import os
    from pynautobot import api

    url = os.environ["NAUTOBOT_URL"]
    token = os.environ["NAUTOBOT_TOKEN"]
    nautobot = api(url=url, token=token)

    # Get the choices for enum fields for the devices endpoint
    nautobot.dcim.devices.choices()
    {
        'face': [
            {
                'value': 'front',
                'display_name': 'Front'
            },
            {
                'value', 'rear',
                'display_name': 'Rear'
            }
        ],
        'status': [
          {
              'value': 'active',
              'display_name': 'Active'
          },
          {
              'value': 'maintenance',
              'display_name': 'Maintenance'
          },
          {
              'value': 'staged',
              'display_name': 'Staged'
          }
        ]
    }

    # Accessing entries from choices for the status field
    device_status_choices = nautobot.dcim.devices.choices()['status']
    device_status_choices[0]
    {'value': 'active', 'display_name': 'Active'}

.. tip::
  The list of available status choices is configurable, so the output will vary between implementations.

.. warning::
  In order to avoid repeated calls to Nautobot, ``choices`` are cached on the Endpoint object. It is advisable to
  either create new Endpoint objects or delete the ``_choices`` attribute on Endpoints periodically.


Creating Objects with Foreign Key Relationships
-----------------------------------------------

Creating a Device in Nautobot requires the following :ref:`fields <Terminology>` to specify a foreign key relationship:

  * Device Type
  * Device Role
  * Site

This can be accomplished by providing the Primary Key (**PK**),
which is an UUID string or a dictionary with key/value pairs that make the object unique.

The first example provides a workflow for obtaining the IDs of the foreign key relationships
by using the :py:meth:`~pynautobot.core.endpoint.Endpoint.get` method from the
Endpoint object, and then referencing the ``id`` of those objects to create a new *Device*.

.. code-block:: python

    nautobot = api(url=url, token=token)
    
    # Get objects for device_type, device_role, and site to get their ID
    device_type = nautobot.dcim.device_types.get(slug="c9300-48")
    device_role = nautobot.dcim.device_roles.get(slug="access")
    site = nautobot.dcim.sites.get(slug="hq")

    # Create new device using foreign key IDs
    devices = nautobot.dcim.devices
    hq_access_1 = devices.create(
        name="hq-access-01",
        device_type=device_type.id,
        device_role=device_role.id,
        site=site.id,
        status="active",
    )
    type(hq_access_1)
    "<class 'pynautobot.models.dcim.Devices'>"
    hq_access_1.created
    '2021-01-01'

The above works, but it requires three :py:meth:`~pynautobot.core.endpoint.Endpoint.get` calls.
The next example demonstrates a simpler interface for creating a device
by passing dictionary objects instead of using the Primary Key.
The dictionaries passed for these fields use key/value pairs
to lookup the Record with matching field/value pairs in the related Model.

The *Device Type*, *Device Role*, and *Site* Models all have a ``slug``
field that can be used to lookup a specific Record.

.. code-block:: python

    nautobot = api(url=url, token=token)
    device_name = "hq-access-02"

    # Create new device using fields to uniquely identify foreign key relationships
    devices = nautobot.dcim.devices
    hq_access_2 = devices.create(
        name=device_name,
        device_type={"slug": "c9300-48"},
        device_role={"slug": "access"},
        site={"slug": "hq"},
        status="active",
    )

    # Show that device was created in Nautobot
    hq_access_2.created
    '2021-01-01'


Creating Multiple Objects
-------------------------

It is also possible to create multiple :py:class:`Records <pynautobot.core.response.Record>`
of the same Model in a single :py:meth:`~pynautobot.core.endpoint.Endpoint.create` call.
This is done by passing a list of dictionaries instead of keyword arguments.

.. code-block:: python

    nautobot = api(url=url, token=token)

    # Create multiple new devices with a single method call
    devices = nautobot.dcim.devices
    hq_access_multiple = devices.create([
        {
            "name": "hq-access-03",
            "device_type": {"slug": "c9300-48"},
            "device_role": {"slug": "access"},
            "site": {"slug": "hq"},
            "status": "active",
        },
        {
            "name": "hq-access-04",
            "device_type": {"slug": "c9300-48"},
            "device_role": {"slug": "access"},
            "site": {"slug": "hq"},
            "status": "active",
        },
    ])

    # show that both devices were created in Nautobot
    hq_access_multiple
    [hq-access-03, hq-access-04]

    # We can access these Record objects as well
    hq_access_03 = hq_access_multiple[0]
    hq_access_03.created
    '2021-01-01'

    # Use get calls to get the newly created devices
    hq_access_03 = nautobot.dcim.devices.get(name="hq-access-03")
    hq_access_03.created
    '2021-01-01'
    hq_access_04 = nautobot.dcim.devices.get(name="hq-access-04")
    hq_access_04.created
    '2021-01-01'


Common Errors
-------------

When creating new :py:class:`Records <pynautobot.core.response.Record>` with pynautobot,
there are three common types of errors:

* :ref:`Missing a Required Field`
* :ref:`Unable to Resolve a Reference to a Foreign Key Relationship`
* :ref:`The Data Sent Does Not Adhere to the Database Schema`

.. note::
   The messages in the Exceptions provide context to identify the exact issue that causes the failure.


Missing a Required Field
^^^^^^^^^^^^^^^^^^^^^^^^

A :py:exc:`~pynautobot.core.query.RequestError` is raised when a required field is not passed to the
:py:meth:`~pynautobot.core.endpoint.Endpoint.create` method.
Creating a new *Device* requires passing the ``name``, ``device_type``, ``device_role``, ``site``, and ``status`` fields.
The below example demonstrates passing only ``name`` and ``status`` when creating a *Device*;
as expected, an Exception is raised indicating that ``device_type``, ``device_role``, and ``site`` are also required fields.

.. code-block:: python

    >>> hq_access_5 = devices.create(
    ...     name="hq-access-05",
    ...     status="active",
    ... )
    Traceback (most recent call last):
    ...
    pynautobot.core.query.RequestError:
    The request failed with code 400 Bad Request:
    {
      'device_type': ['This field is required.'],
      'device_role': ['This field is required.'],
      'site': ['This field is required.']
    }


Unable to Resolve a Reference to a Foreign Key Relationship
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Another reason that a :py:exc:`~pynautobot.core.query.RequestError`
could be raised is for passing in foreign key fields that cannot be resolved.
There are two reasons that can cause a foreign key to not be found:

1. The Record referenced by the foreign key does not exist in the related Model.
2. The related Model has multiple Records matching the constraints specified in the field/value dictionary.

The first two examples below make a reference to a non-existent ``device_type``:
one uses the Primary Key, and the other uses a dictionary to lookup the Record in the related *Device Type* Model.

.. code-block:: python

    >>> # Attempt to create device with non-existent device type ID
    >>> hq_access_5 = devices.create(
    ...     name="hq-access-05",
    ...     device_type='2302f2a1-2ed4-4ac9-a43a-285c95190071',
    ...     device_role={"slug": "access"},
    ...     site={"slug": "hq"},
    ...     status="active",
    ... )
    Traceback (most recent call last):
    ...
    pynautobot.core.query.RequestError:
    The request failed with code 400 Bad Request:
    {
      'device_type': [
        'Related object not found using the provided numeric ID: 2302f2a1-2ed4-4ac9-a43a-285c95190071'
      ]
    }

.. code-block:: python

    >>> # Foreign Key by fields do not exist
    >>> hq_access_5 = devices.create(
    ...     name="hq-access-05",
    ...     device_type={"slug": "non-existent-type"},
    ...     device_role={"slug": "access"},
    ...     site={"slug": "hq"},
    ...     status="active",
    ... )
    Traceback (most recent call last):
    ...
    pynautobot.core.query.RequestError:
    The request failed with code 400 Bad Request:
    {
      'device_type': [
        "Related object not found using the provided attributes: " \
        "{'slug': 'non-existent-type'}"
      ]
    }

The final example uses a dictionary for ``device_type`` that matches multiple *Device Types* in the database.

.. code-block:: python

    >>> # Non-unique data passed in for Foreign Key field
    >>> hq_access_5 = devices.create(
    ...     name="hq-access-05",
    ...     device_type={"model": "c9300-48"},
    ...     device_role={"slug": "access"},
    ...     site={"slug": "hq"},
    ...     status="active",
    ... )
    Traceback (most recent call last):
    ...
    pynautobot.core.query.RequestError:
    The request failed with code 400 Bad Request:
    {
      'device_type': [
        "Multiple objects match the provided attributes: " \
        "{'model': 'c9300-48'}"
      ]
    }


The Data Sent Does Not Adhere to the Database Schema
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The last type of common error is sending data that does not adhere to the schema for a field.
The examples below show:

1. Passing an invalid type.
2. Passing a valid type that does not adhere to the defined constraints.

In the examples below, the ``position`` field of a *Device* is used to demonstrate these errors.
The ``position`` field is a reference to the rack units it is mounted into in the related *Rack* Record.
The ``rack`` referenced in the examples is a 42U rack, which means it supports rack units 1-42.
This field uses an integer type, and has the following constraints:

* The rack units assigned must exist in the *Rack* Record.
* The rack units assigned must not be occupied by an existing device.

The first example passes a string instead of an integer.

.. code-block:: python

    >>> # Attempt to provide invalid type for position
    >>> hq_access_5 = devices.create(
    ...     name="hq-access-05",
    ...     device_type={"model": "c9300-48"},
    ...     device_role={"slug": "access"},
    ...     site={"slug": "hq"},
    ...     status="active",
    ...     rack={"name": "hq-001"},
    ...     face=1,
    ...     position="high",
    ... )
    Traceback (most recent call last):
    ...
    pynautobot.core.query.RequestError:
    The request failed with code 400 Bad Request:
    {
      'position': ['A valid integer is required.']
    }

The last example specifies a rack unit higher than what is supported by *Rack* Record.

.. code-block:: python

    >>> # Attempt to provide invalid rack unit for position
    >>> hq_access_5 = devices.create(
    ...     name="hq-access-05",
    ...     device_type={"model": "c9300-48"},
    ...     device_role={"slug": "access"},
    ...     site={"slug": "hq"},
    ...     status="active",
    ...     rack={"name": "hq-001"},
    ...     face=1,
    ...     position="high",
    ... )
    Traceback (most recent call last):
    ...
    pynautobot.core.query.RequestError:
    The request failed with code 400 Bad Request:
    {
      'position': [
        'U100 is already occupied or does not have sufficient space' \
        'to accommodate this device type: c9300-48 (1U)'
      ]
    }
