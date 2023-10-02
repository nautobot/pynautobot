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

.. code-block:: python

    >>> import os
    >>> from pprint import pprint
    >>> from pynautobot import api
    >>>
    >>> url = os.environ["NAUTOBOT_URL"]
    >>> token = os.environ["NAUTOBOT_TOKEN"]
    >>> nautobot = api(url=url, token=token)
    >>>
    >>> # Get the choices for enum fields for the cables endpoint
    >>> pprint(nautobot.dcim.cables.choices())
    {'length_unit': [{'display': 'Kilometers', 'value': 'km'},
                     {'display': 'Meters', 'value': 'm'},
                     {'display': 'Centimeters', 'value': 'cm'},
                     {'display': 'Miles', 'value': 'mi'},
                     {'display': 'Feet', 'value': 'ft'},
                     {'display': 'Inches', 'value': 'in'}],
     'termination_a_type': [{'display': 'dcim | interface',
                             'value': 'dcim.interface'},
                            {'display': 'dcim | power feed',
                             'value': 'dcim.powerfeed'},
                            {'display': 'circuits | circuit termination',
                             'value': 'circuits.circuittermination'},
                            {'display': 'dcim | console port',
                             'value': 'dcim.consoleport'},
                            {'display': 'dcim | console server port',
                             'value': 'dcim.consoleserverport'},
                            {'display': 'dcim | front port',
                             'value': 'dcim.frontport'},
                            {'display': 'dcim | power outlet',
                             'value': 'dcim.poweroutlet'},
                            {'display': 'dcim | power port',
                             'value': 'dcim.powerport'},
                            {'display': 'dcim | rear port',
                             'value': 'dcim.rearport'}],
     'termination_b_type': [{'display': 'dcim | interface',
                             'value': 'dcim.interface'},
                            {'display': 'dcim | power feed',
                             'value': 'dcim.powerfeed'},
                            {'display': 'circuits | circuit termination',
                             'value': 'circuits.circuittermination'},
                            {'display': 'dcim | console port',
                             'value': 'dcim.consoleport'},
                            {'display': 'dcim | console server port',
                             'value': 'dcim.consoleserverport'},
                            {'display': 'dcim | front port',
                             'value': 'dcim.frontport'},
                            {'display': 'dcim | power outlet',
                             'value': 'dcim.poweroutlet'},
                            {'display': 'dcim | power port',
                             'value': 'dcim.powerport'},
                            {'display': 'dcim | rear port',
                             'value': 'dcim.rearport'}],
     'type': [{'display': 'CAT3', 'value': 'cat3'},
              {'display': 'CAT5', 'value': 'cat5'},
              {'display': 'CAT5e', 'value': 'cat5e'},
              {'display': 'CAT6', 'value': 'cat6'},
              {'display': 'CAT6a', 'value': 'cat6a'},
              {'display': 'CAT7', 'value': 'cat7'},
              {'display': 'CAT7a', 'value': 'cat7a'},
              {'display': 'CAT8', 'value': 'cat8'},
              {'display': 'Direct Attach Copper (Active)', 'value': 'dac-active'},
              {'display': 'Direct Attach Copper (Passive)', 'value': 'dac-passive'},
              {'display': 'MRJ21 Trunk', 'value': 'mrj21-trunk'},
              {'display': 'Coaxial', 'value': 'coaxial'},
              {'display': 'Multimode Fiber', 'value': 'mmf'},
              {'display': 'Multimode Fiber (OM1)', 'value': 'mmf-om1'},
              {'display': 'Multimode Fiber (OM2)', 'value': 'mmf-om2'},
              {'display': 'Multimode Fiber (OM3)', 'value': 'mmf-om3'},
              {'display': 'Multimode Fiber (OM4)', 'value': 'mmf-om4'},
              {'display': 'Singlemode Fiber', 'value': 'smf'},
              {'display': 'Singlemode Fiber (OS1)', 'value': 'smf-os1'},
              {'display': 'Singlemode Fiber (OS2)', 'value': 'smf-os2'},
              {'display': 'Active Optical Cabling (AOC)', 'value': 'aoc'},
              {'display': 'Power', 'value': 'power'},
              {'display': 'Other', 'value': 'other'}]}
    >>>
    >>> # Accessing entries from choices for the type field
    >>> cable_types_choices = nautobot.dcim.cables.choices()['type']
    >>> cable_types_choices[3]
    {'value': 'cat6', 'display': 'CAT6'}

.. warning::
  In order to avoid repeated calls to Nautobot, ``choices`` are cached on the Endpoint object. It is advisable to
  either create new Endpoint objects or delete the ``_choices`` attribute on Endpoints periodically.


Creating Objects with Foreign Key Relationships
-----------------------------------------------

Creating a Device in Nautobot requires the following :ref:`fields <Terminology>` to specify a foreign key relationship:

  * Role
  * Device Type
  * Location

This can be accomplished by providing the Primary Key (**PK**),
which is an UUID string or a dictionary with key/value pairs that make the object unique.

The first example provides a workflow for obtaining the IDs of the foreign key relationships
by using the :py:meth:`~pynautobot.core.endpoint.Endpoint.get` method from the
Endpoint object, and then referencing the ``id`` of those objects to create a new *Device*.

.. code-block:: python

    >>> nautobot = api(url=url, token=token)
    >>>
    >>> # Get objects for device_type, role, and location to get their ID
    >>> device_type = nautobot.dcim.device_types.get(model="c9300-48")
    >>> role = nautobot.extras.roles.get(name="access")
    >>> location = nautobot.dcim.locations.get(name="HQ")
    >>>
    >>> # Create new device using foreign key IDs
    >>> devices = nautobot.dcim.devices
    >>> hq_access_1 = devices.create(
    ...     name="hq-access-01",
    ...     device_type=device_type.id,
    ...     role=role.id,
    ...     location=location.id,
    ...     status={"name": "Active"},
    ... )
    >>> type(hq_access_1)
    "<class 'pynautobot.models.dcim.Devices'>"
    >>> hq_access_1.created
    '2023-09-30T07:56:23.664150Z'

The above works, but it requires three :py:meth:`~pynautobot.core.endpoint.Endpoint.get` calls.
The next example demonstrates a simpler interface for creating a device
by passing dictionary objects instead of using the Primary Key.
The dictionaries passed for these fields use key/value pairs
to lookup the Record with matching field/value pairs in the related Model.

The *Device Type* Model has ``model`` field, and  *Role* and *Location* Models all have a ``name``
field that can be used to lookup a specific Record. ``name`` is not unique for *Location*.

.. code-block:: python

    >>> nautobot = api(url=url, token=token)
    >>>
    >>> device_name = "hq-access-02"
    >>>
    >>> # Create new device using fields to uniquely identify foreign key relationships
    >>> devices = nautobot.dcim.devices
    >>> hq_access_2 = devices.create(
    ...     name=device_name,
    ...     device_type={"model": "c9300-48"},
    ...     role={"name": "access"},
    ...     location="HQ",
    ...     status="Active",
    ... )
    >>>
    >>> # Show that device was created in Nautobot
    >>> hq_access_2.created
    '2023-09-30T08:02:03.872486Z'


Creating Multiple Objects
-------------------------

It is also possible to create multiple :py:class:`Records <pynautobot.core.response.Record>`
of the same Model in a single :py:meth:`~pynautobot.core.endpoint.Endpoint.create` call.
This is done by passing a list of dictionaries instead of keyword arguments.

.. code-block:: python

    >>> nautobot = api(url=url, token=token)
    >>>
    >>> # Create multiple new devices with a single method call
    >>> devices = nautobot.dcim.devices
    >>> hq_access_multiple = devices.create([
    ...     {
    ...         "name": "hq-access-03",
    ...         "device_type": {"model": "c9300-48"},
    ...         "role": {"name": "access"},
    ...         "location": {"name": "HQ"},
    ...         "status": "Active",
    ...     },
    ...     {
    ...         "name": "hq-access-04",
    ...         "device_type": {"model": "c9300-48"},
    ...         "role": {"name": "access"},
    ...         "location": {"name": "HQ"},
    ...         "status": "Active",
    ...     },
    ... ])
    >>>
    >>> # show that both devices were created in Nautobot
    >>> hq_access_multiple
    [<pynautobot.models.dcim.Devices ('hq-access-03') ...>, <pynautobot.models.dcim.Devices ('hq-access-04') at ...>]
    >>>
    >>> # We can access these Record objects as well
    >>> hq_access_03 = hq_access_multiple[0]
    >>> hq_access_03.created
    '2023-09-30T08:14:24.756447Z'
    >>> # Use get calls to get the newly created devices
    >>> hq_access_03 = nautobot.dcim.devices.get(name="hq-access-03")
    >>> hq_access_03.created
    '2023-09-30T08:14:24.756447Z'
    >>> hq_access_04 = nautobot.dcim.devices.get(name="hq-access-04")
    >>> hq_access_04.created
    '2023-09-30T08:14:24.790198Z'


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
Creating a new *Device* requires passing the ``name``, ``device_type``, ``role``, ``location``, and ``status`` fields.
The below example demonstrates passing only ``name`` and ``status`` when creating a *Device*;
as expected, an Exception is raised indicating that ``device_type``, ``role``, and ``location`` are also required fields.

.. code-block:: python

    >>> hq_access_5 = devices.create(
    ...     name="hq-access-05",
    ...     status="Active",
    ... )
    Traceback (most recent call last):
    ...
    pynautobot.core.query.RequestError:
    The request failed with code 400 Bad Request:
    {
        'device_type': ['This field is required.'],
        'role': ['This field is required.'],
        'location': ['This field is required.']
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
    ...     role={"name": "access"},
    ...     location={"name": "HQ"},
    ...     status="Active",
    ... )
    Traceback (most recent call last):
    ...
    pynautobot.core.query.RequestError:
    The request failed with code 400 Bad Request:
    {
        'device_type': [
            "Related object not found using the provided attributes: {'pk': UUID('2302f2a1-2ed4-4ac9-a43a-285c95190071')}"
        ]
    }

.. code-block:: python

    >>> # Foreign Key by fields do not exist
    >>> hq_access_5 = devices.create(
    ...     name="hq-access-05",
    ...     device_type={"model": "non-existent-type"},
    ...     role={"name": "access"},
    ...     location={"name": "HQ"},
    ...     status="Active",
    ... )
    Traceback (most recent call last):
    ...
    pynautobot.core.query.RequestError:
    The request failed with code 400 Bad Request:
    {
        'device_type': [
            "Related object not found using the provided attributes: " \
            "{'model': 'non-existent-type'}"
        ]
    }

The final example uses a dictionary for ``device_type`` that matches multiple *Device Types* in the database.

.. code-block:: python

    >>> # Non-unique data passed in for Foreign Key field
    >>> hq_access_5 = devices.create(
    ...     name="hq-access-05",
    ...     device_type={"manufacturer": { "name": "Cisco" } },
    ...     role={"name": "access"},
    ...     location={"name": "HQ"},
    ...     status="Active",
    ... )
    Traceback (most recent call last):
    ...
    pynautobot.core.query.RequestError:
    The request failed with code 400 Bad Request:
    {
        'device_type': [
            "Multiple objects match the provided attributes: " \
            " {'manufacturer__name': 'Cisco'}"
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
    ...     role={"name": "access"},
    ...     location={"name": "HQ"},
    ...     status="Active",
    ...     rack={"name": "hq-001"},
    ...     face="front",
    ...     position=1,
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
    ...     role={"name": "access"},
    ...     location={"name": "HQ"},
    ...     status={"name": "Active"},
    ...     rack={"name": "hq-001"},
    ...     face="front",
    ...     position=1,
    ... )
    Traceback (most recent call last):
    ...
    pynautobot.core.query.RequestError:
    The request failed with code 400 Bad Request:
    {
        'non_field_errors': [
            'The position and face is already occupied on this rack. The fields rack, position, face must make a unique set.'
        ]
    }
