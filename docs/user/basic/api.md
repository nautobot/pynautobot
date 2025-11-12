# Creating a Pynautobot Instance

To start using pynautobot, instantiate an
`~pynautobot.core.api.Api`{.interpreted-text role="py:class"} object,
passing in the proper URL and a valid Token. The code sample below
assumes that the token has been stored as an environment variable, and
uses the builtin `os`{.interpreted-text role="py:mod"} module to
retrieve it.

!!! Note
    To display dictionaries or other objects in examples, the `pprint` package is used. To install it run `pip install pprint`.


``` python
>>> import os
>>>
>>> from pprint import pprint
>>>
>>> from pynautobot import api
>>>
>>> url = "https://next.demo.nautobot.com"
>>>
>>> # Retrieve token from system environment variable
>>> # token = os.environ["NAUTOBOT_TOKEN"]
>>> token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
>>> nautobot = api(url=url, token=token)
>>> nautobot
<pynautobot.core.api.Api object at ...>
```

!!! Tip

    Creating a [token](https://docs.nautobot.com/projects/core/en/stable/user-guide/platform-functionality/users/token/#tokens) in Nautobot.

# Nautobot Info and Apps

The nautobot object returned above is the main entrypoint to interact
with the Nautobot REST API. This object provides access to general
information about the Nautobot system, and the core
`Apps <Terminology>`{.interpreted-text role="ref"} and
`Plugins <Terminology>`{.interpreted-text role="ref"}.

The core Apps are:

-   circuits
-   cloud
-   data_validation
-   dcim
-   extras
-   ipam
-   load_balancers
-   tenancy
-   users
-   virtualization
-   vpn
-   wireless

``` python
>>> nautobot = api(url=url, token=token)
>>>
>>> # View version of Nautobot
>>> nautobot.version
'2.0'
>>>
>>> # View various details about Nautobot
>>> pprint(nautobot.status())
{'celery-workers-running': 0,
 'django-version': '3.2.21',
 'installed-apps': {'constance': '2.9.1',
                    'constance.backends.database': None,
                    'corsheaders': None,
                    'db_file_storage': None,
                    'debug_toolbar': '4.1.0',
                    'django.contrib.admin': None,
                    'django.contrib.auth': None,
                    'django.contrib.contenttypes': None,
                    'django.contrib.humanize': None,
                    'django.contrib.messages': None,
                    'django.contrib.sessions': None,
                    'django.contrib.staticfiles': None,
                    'django_ajax_tables': None,
                    'django_celery_beat': '2.5.0..',
                    'django_celery_results': '2.4.0..',
                    'django_extensions': '3.2.3',
                    'django_filters': '23.1',
                    'django_jinja': '3.2.21.final.0',
                    'django_prometheus': '2.3.1',
                    'django_tables2': '2.6.0',
                    'drf_spectacular': '0.26.3',
                    'drf_spectacular_sidecar': '2023.9.1',
                    'example_plugin': '1.0.0',
                    'graphene_django': '2.16.0',
                    'health_check': None,
                    'health_check.storage': None,
                    'nautobot.circuits': None,
                    'nautobot.core': None,
                    'nautobot.dcim': None,
                    'nautobot.extras': None,
                    'nautobot.extras.tests.example_plugin_dependency': None,
                    'nautobot.ipam': None,
                    'nautobot.tenancy': None,
                    'nautobot.users': None,
                    'nautobot.virtualization': None,
                    'rest_framework': '3.14.0',
                    'social_django': '5.2.0',
                    'taggit': '4.0.0',
                    'timezone_field': '5.1'},
 'nautobot-version': '2.0.0',
 'plugins': {'example_plugin': '1.0.0'},
 'python-version': '3.8.18'}
>>> 
>>> # Show that the dcim app is available
>>> nautobot.dcim
<pynautobot.core.app.App object at ...>
```

The main purpose of `~pynautobot.core.app.App`{.interpreted-text
role="py:class"} objects is to provide access to
`Models <Terminology>`{.interpreted-text role="ref"} and their data.

# Models

Pynautobot `~pynautobot.core.app.App`{.interpreted-text role="py:class"}
objects will treat all unknown attributes as
`Endpoints <pynautobot.core.endpoint.Endpoint>`{.interpreted-text
role="py:class"}. The
`~pynautobot.core.endpoint.Endpoint`{.interpreted-text role="py:class"}
class is used to represent Models in Nautobot. For example, the Nautobot
DCIM App contains Models, such as: *Devices*, *Platforms*, and *Roles*.
The pynautobot `dcim` `~pynautobot.core.app.App`{.interpreted-text
role="py:class"} does not provide attributes to represent these Models,
however, `~pynautobot.core.endpoint.Endpoint`{.interpreted-text
role="py:class"} objects are created upon attribute access.

The code sample below shows that Models do not exist in the
`nautobot.dcim` attribute dictionary, but the `devices` Model is still
accessible from it.

``` python
>>> nautobot = api(url=url, token=token)
>>>
>>> # Show that the devices attribute does not exist on the dcim object
>>> pprint(nautobot.dcim.__dict__)
{'_choices': None,
 'api': <pynautobot.core.api.Api object at ...>,
 'model': <module 'pynautobot.models.dcim' from '/opt/ntc/nautobot/pynautobot/pynautobot/models/dcim.py'>,
 'name': 'dcim'}
>>> 
>>> # Show that the devices attribute is accessible and
>>> # is an Endpoint object corresponding to the Devices Model
>>> devices = nautobot.dcim.devices
>>> devices
<pynautobot.core.endpoint.Endpoint object at ...>
>>> devices.url
'https://next.demo.nautobot.com/api/dcim/devices'
```

!!! Note
    Since Models are evaluated lazily, using the builtin `dir` and `help` functions on the Apps will not provide any information regarding the available Models.

Some Models in Nautobot have names that contain more than a single word.
In order to access these Models, the names should be joined with an
underscore. The above example of *Roles* would use `roles`. Pynautobot
will automatically convert the underscore into a hyphen for access to
the Nautobot API endpoint.

``` python
>>> nautobot = api(url=url, token=token)
>>>
>>> # Show using an underscore to access Models with multi-word names.
>>> roles = nautobot.extras.roles
>>>
>>> # Show that the URL converts the underscore to a hyphen
>>> roles.url
'https://next.demo.nautobot.com/api/extras.roles'
```

!!! Note
    Attributes are not checked against the Nautobot API, so misspelled or non-existent Models will not raise an Exception until a CRUD operation is attempted on the returned object.

    For example, calling `nautobot.dcim.device` (missing the trailing **s**) will return an `~pynautobot.core.endpoint.Endpoint`{.interpreted-text role="py:class"} object. However, the URL assigned to the Endpoint will not be a valid Nautobot API endpoint, and performing any CRUD operations against that URL will result in an Exception being raised.
