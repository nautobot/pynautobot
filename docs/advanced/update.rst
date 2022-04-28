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

    >>> # Show that device is active
    >>> device.status
    Active

    >>> # Update status and name fields
    >>> device.comments = "removed from service"
    >>> device.status = "decommissioned"

    >>> # Show that changes haven't been synced
    >>> tmp_device = nautobot.dcim.devices.get(name="hq-access-03")
    >>> tmp_device.status
    Active

    >>> # Save updates and show that changes have been synced
    >>> device.save()
    >>> updated_device = nautobot.dcim.devices.get(name="hq-access-03")
    >>> updated_device.comments
    'removed from service'
    >>> updated_device.status
    Decommissioned


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
    >>> hq_access_5 = devices.get(name="hq-access-05")

    >>> # Attempt to update position with an invalid type
    >>> hq_access_5.update({"postition": "high"})
    Traceback (most recent call last):
    ...
    pynautobot.core.query.RequestError:
    The request failed with code 400 Bad Request:
    {
      'position': ['A valid integer is required.']
    }


Invalid Schema
^^^^^^^^^^^^^^

.. code-block:: python

    >>> # Get a device record
    >>> hq_access_5 = devices.get(name="hq-access-05")

    >>> # Attempt to provide invalid rack unit for position
    >>> hq_access_5.position = 100

    >>> # The exception is only raised when save() is called
    >>> hq_access_5.save()
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
    >>> hq_access_5 = devices.get(name="hq-access-05")

    >>> # Set the face attribute
    >>> hq_access_5.face = "front"

    >>> # Attempt to provide invalid rack unit for position
    >>> hq_access_5.position = 100

    >>> # An exception is raised
    >>> hq_access_5.save()
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
    >>> tmp_hq_access_5 = devices.get(name="hq-access-05")
    >>> tmp_hq_access_5.face is None
    True

    >>> # Fix the position field and retrigger update
    >>> hq_access_5.position = 42
    >>> hq_access_5.save()
    True

    >>> # Show that updates have taken affect
    >>> tmp_hq_access_5 = devices.get(name="hq-access-05")
    >>> tmp_hq_access_5.face
    Front
    >>> tmp_hq_access_5.position
    42
