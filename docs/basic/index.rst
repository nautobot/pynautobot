****************
Quickstart Guide
****************

The pynautobot package is a Python SDK for retrieving and managing data in Nautobot.
The following demonstrates how to connect to and interact with the Nautobot REST API.

Terminology
===========

**Apps:** The root level interfaces in Nautobot (IPAM, DCIM, etc.).
Apps are represented by the :py:class:`~pynautobot.core.app.App` class.

**Models:** The second level interfaces in Nautobot (IP Addresses Devices, etc.).
Models correspond to tables in the Nautobot database, are represented by the :py:class:`~pynautobot.core.endpoint.Endpoint` class.

**Endpoint:** The class that represents `Models`.

**Records:** The rows associated with a Model's database table. Records hold the data stored in Nautobot.
Records are represented by the :py:class:`~pynautobot.core.response.Record` class.

**Entries:** See `Records`.

**Fields:** The column names associated with a Model's database table.
:py:class:`~pynautobot.core.endpoint.Endpoint` objects use these as keyword arguments for some methods.
:py:class:`~pynautobot.core.response.Record` objects use these as attribute names.

**Plugins:** Additional `Apps` added added to the Nautobot deployment that are external to provided Nautobot package.


Guide
=====

.. toctree::
   :maxdepth: 2

   install
   api
   crud/index
