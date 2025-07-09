"""
(c) 2017 DigitalOcean

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

This file has been modified by NetworktoCode, LLC.
"""

import logging

from pynautobot.core.endpoint import Endpoint, JobsEndpoint
from pynautobot.core.query import Request
from pynautobot.models import circuits, dcim, extras, ipam, users, virtualization

logger = logging.getLogger(__name__)


class App(object):
    """Represents apps in Nautobot.

    Calls to attributes are returned as Endpoint objects.

    :returns: :py:class:`.Endpoint` matching requested attribute.
    :raises: :py:class:`.RequestError`
        if requested endpoint doesn't exist.
    """

    models = {
        "dcim": dcim,
        "ipam": ipam,
        "circuits": circuits,
        "virtualization": virtualization,
        "extras": extras,
        "users": users,
    }

    def __init__(self, api, name):
        self.api = api
        self.name = name
        self._choices = None
        self._setmodel()

    def _setmodel(self):
        self.model = App.models[self.name] if self.name in App.models else None

    def __getstate__(self):
        return {"api": self.api, "name": self.name, "_choices": self._choices}

    def __setstate__(self, d):
        self.__dict__.update(d)
        self._setmodel()

    def __getattr__(self, name):
        if name == "jobs":
            return JobsEndpoint(self.api, self, name, model=self.model)
        return Endpoint(self.api, self, name, model=self.model)

    def choices(self):
        """Returns _choices response from App

        .. note::

            This method is deprecated and only works with Nautobot version 2.7.x
            or older. The ``choices()`` method in :py:class:`.Endpoint` is
            compatible with all Nautobot versions.

        :Returns: Raw response from Nautobot's _choices endpoint.
        """
        if self._choices:
            return self._choices

        self._choices = Request(
            base="{}/{}/_choices/".format(self.api.base_url, self.name),
            token=self.api.token,
            http_session=self.api.http_session,
        ).get()

        return self._choices

    def custom_choices(self):
        """Returns custom-fields response from app

        .. note::

            This method is deprecated and will be removed in pynautobot
            2.0 or newer. Please use `custom_fields()` instead.

        :Returns: Raw response from Nautobot's custom-fields endpoint.
        :Raises: :py:class:`.RequestError` if called for an invalid endpoint.
        :Example:

        >>> nb.extras.custom_choices()
        {'Testfield1': {'Testvalue2': 2, 'Testvalue1': 1},
         'Testfield2': {'Othervalue2': 4, 'Othervalue1': 3}}
        """
        logger.warning(
            "WARNING: The method 'custom_choices()' will be removed in "
            "the next major version (2.x) of pynautobot. Please use "
            "`get_custom_fields()` instead."
        )

        return self.get_custom_fields()

    def get_custom_fields(self):
        """Returns custom-fields response from app

        :Returns: Raw response from Nautobot's custom-fields endpoint.
        :Raises: :py:class:`.RequestError` if called for an invalid endpoint.
        :Example:

        >>> nb.extras.get_custom_fields()
        [
            {
                "id": "5b39ba88-e5ab-4be2-89f5-5a016473b53c",
                "display": "Test custom field",
                "url": "http://localhost:8000/api/extras/custom-fields/5b39ba88-e5ab-4be2-89f5-5a016473b53c/",
                "content_types": ["dcim.rack"],
                "type": {"value": "integer", "label": "Integer"},
                "label": "Test custom field",
                "name": "test_custom_field",
                "slug": "test_custom_field",
                "description": "",
                "required": False,
                "filter_logic": {"value": "loose", "label": "Loose"},
                "default": None,
                "weight": 100,
                "validation_minimum": None,
                "validation_maximum": None,
                "validation_regex": "",
                "created": "2023-04-15",
                "last_updated": "2023-04-15T17:45:11.839431Z",
                "notes_url": "http://localhost:8000/api/extras/custom-fields/5b39ba88-e5ab-4be2-89f5-5a016473b53c/notes/",
            },
        ]
        """
        return Request(
            base=f"{self.api.base_url}/{self.name}/custom-fields/",
            token=self.api.token,
            http_session=self.api.http_session,
        ).get()

    def get_custom_field_choices(self):
        """Returns custom-field-choices response from app

        :Returns: Raw response from Nautobot's custom-field-choices endpoint.
        :Raises: :py:class:`.RequestError` if called for an invalid endpoint.
        :Example:

        >>> nb.extras.get_custom_field_choices()
        [
            {
                "id": "5b39ba88-e5ab-4be2-89f5-5a016473b53c",
                "display": "First option",
                "url": "http://localhost:8000/api/extras/custom-field-choices/5b39ba88-e5ab-4be2-89f5-5a016473b53c/",
                "field": {
                    "display": "Test custom field 2",
                    "id": "5b39ba88-e5ab-4be2-89f5-5a016473b53c",
                    "url": "http://localhost:8000/api/extras/custom-fields/5b39ba88-e5ab-4be2-89f5-5a016473b53c/",
                    "name": "test_custom_field_2"
                },
                "value": "First option",
                "weight": 100,
                "created": "2023-04-15",
                "last_updated": "2023-04-15T18:11:57.163237Z"
            },
        ]
        """
        return Request(
            base=f"{self.api.base_url}/{self.name}/custom-field-choices/",
            token=self.api.token,
            http_session=self.api.http_session,
        ).get()

    def config(self):
        """Returns config response from app

        :Returns: Raw response from Nautobot's config endpoint.
        :Raises: :py:class:`.RequestError` if called for an invalid endpoint.
        :Example:

        >>> pprint.pprint(nb.users.config())
        {'tables': {'DeviceTable': {'columns': ['name',
                                                'status',
                                                'tenant',
                                                'device_role',
                                                'site',
                                                'primary_ip',
                                                'tags']}}}
        """
        config = Request(
            base="{}/{}/config/".format(
                self.api.base_url,
                self.name,
            ),
            token=self.api.token,
            http_session=self.api.http_session,
        ).get()
        return config


class PluginsApp(object):
    """
    Basically valid plugins api could be handled by same App class,
    but you need to add plugins to request url path.

    :returns: :py:class:`.App` with added plugins into path.

    """

    def __init__(self, api):
        self.api = api

    def __getattr__(self, name):
        return App(self.api, f"plugins/{name.replace('_', '-')}")

    def installed_plugins(self):
        """Returns raw response with installed plugins

        :returns: Raw response Nautobot's installed plugins.
        :Example:

        >>> nb.plugins.installed_plugins()
        [{
            'name': 'test_plugin',
            'package': 'test_plugin',
            'author': 'Dmitry',
            'description': 'Nautobot test plugin',
            'verison': '0.10'
        }]
        """
        installed_plugins = Request(
            base="{}/plugins/installed-plugins".format(
                self.api.base_url,
            ),
            token=self.api.token,
            http_session=self.api.http_session,
        ).get()
        return installed_plugins
