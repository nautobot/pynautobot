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
    '1.0'

    >>> # View various details about Nautobot
    >>> nautobot.status()
    {
        'django-version': '3.1.3',
        'installed-apps': {...},
        'nautobot-version': '1.0.3+5de17ddd',
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
