Retrieving Objects From Nautobot
================================

The :py:class:`~pynautobot.core.endpoint.Endpoint` class provides three methods
for retrieving :py:class:`~pynautobot.core.response.Record` objects from Nautobot.

* The :py:meth:`~pynautobot.core.endpoint.Endpoint.get` method is used to get a single Record.
* The :py:meth:`~pynautobot.core.endpoint.Endpoint.filter` method will return a list of Records.
* The :py:meth:`~pynautobot.core.endpoint.Endpoint.all` method will return all Records for the Model.


Using the Get Method
--------------------

The :ref:`Retrieving Records` sections shows how to use the
:py:meth:`~pynautobot.core.endpoint.Endpoint.get` method by passing in keyword arguments.
Another way to retrieve a :ref:`Record <Terminology>` is by passing in the value of the PK,
which is the ID for most objects.

.. code-block:: python

    >>> dev = nautobot.dcim.devices.get('2302f2a1-2ed4-4ac9-a43a-285c95190071')
    >>> dev.name
    'hq-access-01'
    >>> dev.status
    Active
    >>> dev.device_type
    c9300-48
    >>> dev.device_role
    Access

.. note::
   If an entry with the specified value for the PK does not exist,
   then ``None`` in the above example.

When using the :py:meth:`~pynautobot.core.endpoint.Endpoint.get` method
with keyword arguments, the keyword arguments must match only a single Record.
If multiple Records are matched, then a ``ValueError`` is raised.

.. code-block:: python

    >>> dev = nautobot.dcim.devices.get(device_type="c9300-48")
    Traceback (most recent call last):
    ...
    ValueError: get() returned more than one result.
    Check that the kwarg(s) passed are valid for this endpoint
    or use filter() or all() instead.


Using the Filter Method
-----------------------

The error message from the previous example suggests to use the
:py:meth:`~pynautobot.core.endpoint.Endpoint.filter` method.
Using this method will return a list of :py:class:`~pynautobot.core.response.Record`
instances; one for each matching **record**.
This method also supports:

* filtering a single :ref:`field <Terminology>` with multiple values
* filtering based on custom fields
* filtering with lookup expressions


Basic Usage
^^^^^^^^^^^

The simplest usage of the :py:meth:`~pynautobot.core.endpoint.Endpoint.filter`
method is to pass keyword arguments with single values.
The previous example raised an exception using the
:py:meth:`~pynautobot.core.endpoint.Endpoint.get` method,
but will return all matches using :py:meth:`~pynautobot.core.endpoint.Endpoint.filter`.

.. code-block:: python

    >>> # Get all c9300-48 devices
    >>> devices = nautobot.dcim.devices.filter(device_type="c9300-48")

    >>> # Show a list of Records are returned
    >>> devices
    [hq-access-01, hq-access-02, hq-access-03, hq-access-04, hq-access-05, switch0, switch1]

    >>> # Show accessing data from the first c9300-48 device
    >>> dev1 = devices[0]
    >>> dev1.name
    'hq-access-01'
    >>> dev1.status
    Active


Filtering with OR logic
^^^^^^^^^^^^^^^^^^^^^^^

The :py:meth:`~pynautobot.core.endpoint.Endpoint.filter` method allows
using an **OR** condition by passing in a list of values to match against the field.
The example below gets all devices located in either *Site* ``hq`` or ``dc``.

.. code-block:: python

    >>> # There are 100 devices total
    >>> nautobot.dcim.devices.count()
    100

    >>> # There are 20 dc devices
    >>> dev_dc_site = nautobot.dcim.devices.filter(site="dc")
    >>> len(dev_dc_site)
    20

    >>> # There are 5 hq devices
    >>> dev_hq_site = nautobot.dcim.devices.filter(site="hq")
    >>> len(dev_hq_site)
    5

    # The filter method will grab all devices in both sites
    >>> dev_hq_dc_sites = nautobot.dcim.devices.filter(site=["hq", "dc"])
    >>> len(dev_all_sites)
    25


Filtering based on a Custom Field
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Nautobot provides `Custom Fields <https://nautobot.readthedocs.io/en/latest/additional-features/custom-fields/>`_
as a way of extending a :ref:`Model's <Terminology>` fields.
These fields can be referenced in the API by appending `cf_` to the field's name.
The below example has a custom field named **owner**, which is used to filter the devices
by passing the ``cf_owner`` keyword argument.

.. code-block:: python

    >>> devices = nautobot.dcim.devices.filter(cf_owner="John Smith")
    >>> devices
    [switch0, switch1]

    >>> # Show device has an owner of "John Smith"
    >>> devices[0].custom_fields["owner"]
    'John Smith'


Filtering with Lookup Expressions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Nautobot API uses `Lookup Expressions <https://nautobot.readthedocs.io/en/latest/rest-api/filtering/#lookup-expressions>`_
to filter using something other than the exact matches that have been used so far.
There are several expressions that can be used; they generally cover things like:

* greater than
* less than
* not equal
* starts with
* contains
* case insensitivity

The example below shows how use negation with *__n*.
From the previous examples, there are 100 devices total, and 25 are located in either the `dc` or `hq` site.
Using ``site__n`` to get the negation of these sites returns 75 devices.

.. code-block::

    >>> devices = nautobot.dcim.devices.filter(site__n=["hq", "dc"])
    >>> len(devices)
    75

    >>> # Show the device is not in either hq or dc site
    >>> devices[0].site
    branch1


Using the All Method
--------------------

The :py:meth:`~pynautobot.core.endpoint.Endpoint.all` is used to get all records of a specific endpoint.
This will return a list of all :py:class:`~pynautobot.core.response.Record` objects for the specific **Endpoint**.

.. code-block:: python

    >>> devices = nautobot.dcim.devices.all()
    >>> len(devices)
    100
    >>> dev1 = devices[0]
    >>> dev1.name
    'hq-access-01'
    >>> dev1.status
    Active

.. tip::
  Both ``filter`` and ``all`` can use threading by passing
  in ``use_threading=True`` when instantiating the ``api`` object.

The following two pages cover interacting with the returned :py:class:`~pynautobot.core.response.Record` objects.
The next page covers additional Update operations, which is followed by a discussion of other features and methods.
