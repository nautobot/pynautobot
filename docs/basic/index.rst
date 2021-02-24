****************
Quickstart Guide
****************

The pynautobot package is a Python SDK for retrieving and managing data in Nautobot.
The following demonstrates how to connect to and interact with the Nautobot REST API.

.. rubric:: Terminology

Nautobot consists of Apps (IPAM, DCIM, etc.),
and each App contains Models (IP Addresses, Devices, etc.) for storing data in a database.
The pynautobot SDK contains objects that represent these Apps and Models, so for clarity in this documentation,
these terms will be capitalized when referring to the "real" objects in Nautobot,
and lowercased when referring to the representative object in pynautobot.

.. note::
   Links to the pynautobot classes will still be capitalized.

In pynautobot, Models are represented by a more generic object called :py:class:`~pynautobot.core.endpoint.Endpoint`.
Some examples will show this object when examining models, and consequently some discussion around the example also
uses the term *endpoint*. However, in order to maintain the link to the "real" implementation in Nautobot,
the term *model* is used more frequently.

.. toctree::
   :maxdepth: 3

   install
   api
   crud/index
