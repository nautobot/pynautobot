Updating Objects
================

The :ref:`Updating Records` section shows how to use the
:py:meth:`~pynautobot.core.response.Record.update` method to update :ref:`fields <Terminology>`.
Another way to accomplish update operations is to update the
:py:class:`~pynautobot.core.response.Record` object's attributes,
and call the :py:meth:`~pynautobot.core.response.Record.save` method.
The main difference with this approach is that changes are not synced
to Nautobot until the :py:meth:`~pynautobot.core.response.Record.save` method is called.

Modifying a Record by Attribute Updates
---------------------------------------

The below example will:

* make updates to a *Device*
* show that updates haven't synced to Nautobot before saving.
* show that updates are synced after calling the save method.

.. code-block::

    >>> device = nautobot.dcim.devices.get(name="hq-access-03")
    >>>
    >>> # Show that device is active
    >>> device.status
    <pynautobot.core.response.Record ('Active') at ...>
    >>>
    >>> # Update status and name fields
    >>> device.comments = "removed from service"
    >>> device.status = "Decommissioned"
    >>>
    >>> # Show that changes haven't been synced
    >>> tmp_device = nautobot.dcim.devices.get(name="hq-access-03")
    >>> tmp_device.status
    <pynautobot.core.response.Record ('Active') at ...>
    >>>
    >>> # Save updates and show that changes have been synced
    >>> device.save()
    >>> updated_device = nautobot.dcim.devices.get(name="hq-access-03")
    >>> updated_device.comments
    'removed from service'
    >>> updated_device.status
    <pynautobot.core.response.Record ('Decommissioned') at ...>

Errors with updates
-------------------

Since the Update operation behaves similarly to the Create operation,
performing an update can have the some of the same errors.
The two examples below are the same issues outlined
in :ref:`The Data Sent Does Not Adhere to the Database Schema`.

The first example uses the :py:meth:`~pynautobot.core.response.Record.update`
method and returns an exception immediately.
The second example modifies the objects ``position`` attribute,
and the exception is not raised until the :py:meth:`~pynautobot.core.response.Record.save` method is called.

Invalid Type
^^^^^^^^^^^^

.. code-block:: python

    >>> # Get a device record
    >>> hq_access_4 = devices.get(name="hq-access-04")
    >>>
    >>> # Attempt to update position with an invalid type
    >>> hq_access_4.update({"postition": "high"})
    False

Invalid Schema
^^^^^^^^^^^^^^

.. code-block:: python

    >>> # Get a device record
    >>> hq_access_4 = devices.get(name="hq-access-04")
    >>>
    >>> # Attempt to provide invalid rack unit for position
    >>> hq_access_4.position = 100
    >>>
    >>> # The exception is only raised when save() is called
    >>> hq_access_4.save()
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

Atomic
^^^^^^

One important feature of the Nautobot API is that **updates** are Atomic.
If any of the fields being updated causes an error, then all updates are aborted.
The following example updates the ``face`` and ``position`` fields.
An error is raised for the ``position`` field,
and fetching the object from Nautobot shows that ``face`` has also been left unchanged.

.. code-block:: python

    >>> # Get a device record
    >>> hq_access_4 = devices.get(name="hq-access-04")
    >>>
    >>> # Set the face attribute
    >>> hq_access_4.face = "front"
    >>>
    >>> # Attempt to provide invalid rack unit for position
    >>> hq_access_4.position = 100
    >>>
    >>> # An exception is raised
    >>> hq_access_4.save()
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

    >>> # Show that the object's face field has not changed
    >>> tmp_hq_access_4 = devices.get(name="hq-access-04")
    >>> tmp_hq_access_4.face is None
    True
    >>>
    >>> # Fix the position field and retrigger update
    >>> hq_access_4.position = 42
    >>> hq_access_4.save()
    True
    >>>
    >>> # Show that updates have taken affect
    >>> tmp_hq_access_4 = devices.get(name="hq-access-04")
    >>> tmp_hq_access_4.face
    <pynautobot.core.response.Record ('Front') at 0x7f65000ade90>
    >>> tmp_hq_access_4.position
    42

Updating objects without loading data
-------------------------------------

In some cases it may not be necessary to load an object to update it, for example
if the ID and updated fields are known, the call HTTP PATCH may be made without
performing an :py:meth:`~pynautobot.core.endpoint.Endpoint.get` first.

In this case, the :py:meth:`~pynautobot.core.endpoint.Endpoint.update` method may
be used to directly submit a PATCH to the Nautobot REST API. Using this reduces
the number of API calls. It can be particularly useful as a way to update data
fetched from the GraphQL API.

The examples updates a Device record, however this can apply to other API
:py:class:`~pynautobot.core.endpoint.Endpoint` types.

.. code-block:: python

    >>> import os
    >>> from pynautobot import api
    >>>
    >>> url = os.environ["NAUTOBOT_URL"]
    >>> token = os.environ["NAUTOBOT_TOKEN"]
    >>> nautobot = api(url=url, token=token)
    >>>
    >>> # Update status and name fields
    >>> result = nautobot.dcim.devices.update(
    >>>   id="491d799a-2b4d-41fc-80e1-7c5cbb5b71b6",
    >>>   data={
    >>>     "comments": "removed from service",
    >>>     "status": "Decommissioned",
    >>>   },
    >>> )
    >>>
    >>> result
    True

References:

* :ref:`Gathering Data from GraphQL Endpoint`
