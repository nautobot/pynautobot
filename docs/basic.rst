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


Installing Pynautobot
=====================

You can install using either :ref:`pip <Pip Install>` or :ref:`poetry <Poetry Install>`

Pip Install
-----------

.. code-block:: sh

    $ pip install pynautobot
    ...


Poetry Install
--------------

.. code-block:: sh

    $ git clone https://github.com/nautobot/pynautobot.git
    ...
    $ cd pynautobot
    $ pip install poetry
    ...
    $ poetry shell
    Virtual environment already activated: /home/user/pynautobot/.venv
    $ poetry install
    ...


Creating a Pynautobot Instance
==============================

To start using pynautobot, instantiate an :py:class:`~pynautobot.core.api.Api` object,
passing in the proper URL and a valid Token.
The code sample below assumes that the token has been stored as an environment variable,
and uses the builtin :py:mod:`os` module to retrieve it.

.. code-block:: python

    import os

    from pynautobot import api

    url = "https://nautobot.networktocode.com"

    # Retrieve token from system environment variable
    token = os.environ["NAUTOBOT_TOKEN"]
    nautobot = api(url=url, token=token)

.. tip::

   Creating a `token <https://nautobot.readthedocs.io/en/latest/rest-api/authentication/>`_ in Nautobot.


Nautobot Info and Apps
======================

The nautobot object returned above is the main entrypoint to interact with the Nautobot REST API.
This object provides access to general information about the Nautobot system, and the core Apps and Plugins.
The core apps are:

* dcim
* ipam
* circuits
* tenancy
* extras
* virtualization
* users

.. code-block:: python

    >>> nautobot = api(url=url, token=token)

    >>> # View version of Nautobot
    >>> nautobot.version
    '2.10'

    >>> # View various details about Nautobot
    >>> nautobot.status()
    {
        'django-version': '3.1.3',
        'installed-apps': {...},
        'nautobot-version': '2.10.3+5de17ddd',
        'plugins': {
            'nautobot_healthcheck': '0.0.1'
        },
        'python-version': '3.7.9',
        'rq-workers-running': 2
    }

    >>> # Show that the dcim app is available
    >>> nautobot.dcim
    <pynautobot.core.app.App object at 0x7fbd42870fa0>

The main purpose of :py:class:`~pynautobot.core.app.App` objects is to provide access to the models
contained within each app and their data.


Models
======

Pynautobot app objects will treat all unknown attributes as API endpoints that correspond to Models contained within the App.
For example, the DCIM App contains several Models, such as: *Devices*, *Platforms*, and *Device Roles*.
The pynautobot :py:attr:`~pynautobot.api.Api.dcim` app does not provide attributes to represent these models,
however, the models are created upon attribute access.

The code sample below shows that models do not exist in the ``nautobot.dcim`` attribute dict,
but the ``devices`` model is still accessible from it.

.. code-block:: python

    >>> nautobot = api(url=url, token=token)

    >>> # Show that the devices attribute does not exist on the dcim object
    >>> nautobot.dcim.__dict__
    {
        'api': <pytnautobot.core.api.Api object at 0x7fb9c20dbfa0>,
        'name': 'dcim',
        '_choices': None,
        'model': <module 'pytnautobot.models.dcim'
    }

    >>> # Show that the devices attribute is accessible and
    >>> # is an Endpoint objectcorresponding to the Devices Model
    >>> devices = nautobot.dcim.devices
    >>> devices
    <pynautobot.core.endpoint.Endpoint object at 0x7fb9c1b4c0a0>
    >>> devices.url
    'https://nautobot.networktocode.com/api/dcim/devices'

.. note::

   Since models are evaluated lazily, using the builtin ``dir`` and ``help`` functions
   on the apps will not provide any information regarding the available models.

Some Models have names that contain more than a single word.
In order to access these Models, the names should be joined with an underscore ( **_** ).
The above example of *Device Roles* would use ``device_roles``.
Pynautobot will automatically convert the underscore into a hyphen for access to the API endpoint.

.. code-block:: python

    >>> nautobot = api(url=url, token=token)

    >>> # Show using an underscore to access Models with multi-word names.
    >>> device_roles = nautobot.dcim.device_roles

    >>> # Show that the URL converts the underscore to a hyphen
    >>> device_roles.url
    'https://nautobot.networktocode.com/api/dcim/device-roles'

.. note::

   Attributes are not checked against the Nautobot API,
   so misspelled or non-existent models will not raise an Exception
   until a CRUD operation is attempted on the returned object.

   For example, calling ``nautobot.dcim.device`` (missing the trailing **s**)
   will return an :py:class:`~pynautobot.core.endpoint.Endpoint` object.
   However, the URL assigned to the Endpoint will not be a valid Nautobot API endpoint,
   and performing any CRUD operations against that URL will result in an Exception being raised.


CRUD Operations
===============

The model objects support Create and Read Operations. Records or entries in the model support Update and Delete operations.
This section introduces performing all four operations with pynautobot, see :ref:`Advanced Operations` for more complete coverage.


Creating Records
----------------

New Records can be created using a model's :py:meth:`~pynautobot.core.endpoint.Endpoint.create` method.
All fields supported by the Model can be passed into the method, and every required field must be passed.

.. code-block:: python

    nautobot = api(url=url, token=token)
    device_roles = nautobot.dcim.device_roles

    # Create a dict of keyword arguments to use for device role config.
    access_role_config = {
        "name": "Access Switch",
        "slug": "access-switch",
    }

    # Create a new Record in the Device Roles Model.
    access_role = device_roles.create(**access_role_config)

Creating an entry adds a new Record into the Nautobot database,
and a representative :py:class:`~pynautobot.core.response.Record` object is returned.
This record object has attributes for each field in Nautobot.
The following code block is a continuation of the previous one.

.. code-block:: python

    >>> # Show that fields passed to the create method
    >>> # are accessible attributes with expected values
    >>> access_role.name
    'Access Switch'
    >>> access_role.slug
    'access-switch'

    >>> # Show that fields not passed to the method
    >>> # were assigned values by the Model
    >>> access_role.description
    ''
    >>> access_role.id
    '6929b68d-8f87-4470-8377-e7fdc933a2bb'


Retrieving Records
------------------

Pynautobot's model objects also provide mechanisms to retrieve the Records stored in the Nautobot database.
The :py:meth:`~pynautobot.core.endpoint.Endpoint.get` method can be used to retrieve a single record.
The most common way to use this method is to pass keyword arguments mapping the record's field with its value,
such as ``slug="access-switch"``.

.. code-block:: python

    nautobot = api(url=url, token=token)
    device_roles = nautobot.dcim.device_roles

    # Show getting a record using a keyword argument
    access_role = device_roles.get(slug="access-switch")

.. note::
   Multiple keyword arguments can be supplied if needed to uniquely identify a single entry.

The :py:class:`~pynautobot.core.response.Record` object returned by the ``get`` method is
the same as what is returned in the above ``create`` method.

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

The :py:meth:`~pynautobot.core.endpoint.Endpoint.all` method is useful for retrieving all Records of the Model.

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


Updating Records
----------------

Modifying the data in a Record is accomplished by using a record object's
:py:meth:`~pynautobot.core.response.Record.update` method.
This method accepts a dict of field/value mappings (Ex: {"description": "Provides access to end hosts"}).
A boolean is returned to indicate whether updates were made to the Record.
The below example shows retrieving a record using the ``get`` method, and then updating its fields.

.. code-block:: python

    >>> nautobot = api(url=url, token=token)
    >>> device_roles = nautobot.dcim.device_roles

    >>> # Get the record object for the access-switch device role
    >>> access_role = device_roles.get(slug="access-switch")

    >>> # Show existing values for name and description fields
    >>> access_role.name
    'Access Switch'
    >>> access_role.description
    ''

    >>> # Create a dictionary to update the device role fields
    >>> access_switch_updates = {
            "name": "access switch",
            "description": "Provides access to end hosts",
        }

    >>> # Show using the update method on the device role
    >>> access_role.update(access_switch_updates)
    True

    >>> # Show that the fields were updated on the existing device role
    >>> access_role.name
    'access switch'
    >>> access_role.description
    'Provides access to end hosts'


Deleting Records
----------------

Lastly, deleting a Record from a Model is done by calling
the :py:meth:`~pynautobot.core.response.Record.delete` method on a record object.
This method attempts to delete the Record from the database,
and will return a boolean to indicate whether or not it was successful.

.. code-block:: python

    >>> nautobot = api(url=url, token=token)
    >>> device_roles = nautobot.dcim.device_roles

    >>> # Get the record object for the access-switch device role
    >>> access_role = device_roles.get(slug="access-switch")

    >>> # Show deleting the Record
    >>> access_role.delete()

    >>> # Show that the "access-switch" Device Role was deleted
    >>> device_roles.get(slug="access-switch")
    ValueError ...
