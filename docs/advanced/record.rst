Interacting With A Record
=========================

We already know that we can access attributes on the record, but what else can we do?


NAPALM
------

You're able to run the normal NAPALM integrations as long as all the prerequisites are taken care of.

Here we can run the ``get_facts`` getter.

.. code-block:: python

   dev1.napalm.list(method='get_facts')
   {"get_facts": {"interface_list": ["ge-0/0/0"]}}


Accessing Field Data
--------------------



Serialize
^^^^^^^^^

Instead of accessing the device and only receiving the name, you can use the :py:meth:`serialize()<pynautobot.core.response.Record.serialize>` to view a near dictionary like structure.

.. code-block:: python

   import json
   >>> print(json.dumps(dev1.serialize(), indent=4))
   {
       "id": "ea354978-471a-45a2-a438-92cfc046df0b",
       "url": "http://localhost:8000/api/dcim/devices/102/",
       "name": "hq-access-01",
       "display_name": "hq-access-01",
       "device_type": 2,
       "device_role": 2,
       "tenant": null,
       "platform": null,
       "serial": "",
       "asset_tag": null,
       "site": 2,
       "rack": null,
       "position": null,
       "face": null,
       "parent_device": null,
       "status": "active",
       "primary_ip": null,
       "primary_ip4": null,
       "primary_ip6": null,
       "cluster": null,
       "virtual_chassis": null,
       "vc_position": null,
       "vc_priority": null,
       "comments": "",
       "local_context_data": null,
       "tags": [],
       "custom_fields": {},
       "config_context": {},
       "created": "2021-02-17",
       "last_updated": "2021-02-17T17:46:44.788078Z"
   }

You may have noticed that any field that is a foreign key relationship only provides the ID.
We need to cast to a dictionary to see the actual sub keys.

.. code-block:: python

   >>> print(json.dumps(dict(dev1), indent=4))
   {
       "id": "2d7c20dc-78a8-44af-961b-56d418c14bea",
       "url": "http://localhost:8000/api/dcim/devices/102/",
       "name": "hq-access-01",
       "display_name": "hq-access-01",
       "device_type": {
           "id": "100fa8e8-381b-4f25-b2cd-10c99cdef523",
           "url": "http://localhost:8000/api/dcim/device-types/2/",
           "manufacturer": {
               "id": "e14f5b2b-bf5f-449f-b089-495b73657cf5",
               "url": "http://localhost:8000/api/dcim/manufacturers/1/",
               "name": "Cisco",
               "slug": "cisco"
           },
           "model": "c9300-48",
           "slug": "c9300-48",
           "display_name": "Cisco c9300-48"
       },
       "device_role": {
           "id": "022d3ff6-b08d-4380-9daa-8e16c6fed5ec",
           "url": "http://localhost:8000/api/dcim/device-roles/2/",
           "name": "Access",
           "slug": "access"
       },
       "tenant": null,
       "platform": null,
       "serial": "",
       "asset_tag": null,
       "site": {
           "id": "09df769c-af34-45f8-950a-94c268d48464",
           "url": "http://localhost:8000/api/dcim/sites/2/",
           "name": "HQ",
           "slug": "hq"
       },
       "rack": null,
       "position": null,
       "face": null,
       "parent_device": null,
       "status": {
           "value": "active",
           "label": "Active"
       },
       "primary_ip": null,
       "primary_ip4": null,
       "primary_ip6": null,
       "cluster": null,
       "virtual_chassis": null,
       "vc_position": null,
       "vc_priority": null,
       "comments": "",
       "local_context_data": null,
       "tags": [],
       "custom_fields": {},
       "config_context": {},
       "created": "2021-02-17",
       "last_updated": "2021-02-17T17:46:44.788078Z"
   }


Record Hashes and Equality Comparison
-------------------------------------


Record Hash
^^^^^^^^^^^

The hash of a record is made from a combination of the name of the endpoint and its ID. If the ID does not exist, then it will be a hash of **only** the
endpoint name. If an ID does exist then the hash will be of the tuple representing `(endpoint.name, id)`.


Equality Comparison
^^^^^^^^^^^^^^^^^^^

If there are two objects that represent the same device, but an update is made to a field other than the name or the ID,
then a equals comparison will return True, even though there is a different data point.

.. code-block:: python

    # Assign den-rtr01 to dev1, then to dev2
    >>> dev1 = nautobot.dcim.devices.get(name="den-rtr01")
    >>> dev2 = nautobot.dcim.devices.get(name="den-rtr01")
    >>> dev1 == dev2
    True
    >>> dev2.platform
    Cisco IOS
    # Change the platform
    >>> dev2.platform = "Cisco NXOS"
    >>> dev2.platform
    'Cisco NXOS'
    # Compare the devices, since the ID nor the 
    >>> dev1 == dev2
    True

A comparison can be made on individual attributes of an object:

.. code-block:: python

    >>> dev1.platform == dev2.platform
    False
