# (c) 2017 DigitalOcean
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# This file has been modified by NetworktoCode, LLC.

"""
This module defines the `App` and `PluginsApp` classes for interacting with
Nautobot applications and plugins.
"""

import logging

from pynautobot.core.endpoint import Endpoint, JobsEndpoint, GraphqlEndpoint
from pynautobot.core.query import Request
from pynautobot.models import circuits, cloud, dcim, extras, ipam, users, virtualization

logger = logging.getLogger(__name__)


class App:
    """Represents apps in Nautobot.

    Calls to attributes are returned as Endpoint objects.

    Returns:
        (Endpoint): Matching requested attribute.

    Raises:
        RequestError: If requested endpoint doesn't exist.
    """

    models = {
        "dcim": dcim,
        "cloud": cloud,
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
        if name == "graphql_queries":
            return GraphqlEndpoint(self.api, self, name, model=self.model)
        return Endpoint(self.api, self, name, model=self.model)

    def __dir__(self):
        endpoints = self._get_api_endpoints()
        # We replace all hyphens with underscores so they can be used as attributes
        endpoint_attrs = [e.replace("-", "_") for e in endpoints.keys()]
        return super().__dir__() + endpoint_attrs

    def choices(self):
        """Returns _choices response from App.

        Returns:
            (List[Response]): Raw response from Nautobot's _choices endpoint.
        """
        if self._choices:
            return self._choices

        self._choices = Request(
            base=f"{self.api.base_url}/{self.name}/_choices/",
            token=self.api.token,
            http_session=self.api.http_session,
        ).get()

        return self._choices

    def get_custom_fields(self):
        """Returns custom-fields response from app.

        Returns:
            (List[Response]): Raw response from Nautobot's custom-fields endpoint.

        Raises:
            RequestError: If called for an invalid endpoint.

        Examples:
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
        """Returns custom-field-choices response from app.

        Returns:
            (List[Response]): Raw response from Nautobot's custom-field-choices endpoint.

        Raises:
            RequestError: If called for an invalid endpoint.

        Examples:
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
        """Returns config response from app.

        Returns:
            (dict): Raw response from Nautobot's config endpoint.

        Raises:
            RequestError: If called for an invalid endpoint.

        Example:
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
            base=f"{self.api.base_url}/{self.name}/config/",
            token=self.api.token,
            http_session=self.api.http_session,
        ).get()
        return config

    def _get_api_endpoints(self):
        """Returns the API endpoints available for the app."""
        return Request(
            base=f"{self.api.base_url}/{self.name}/",
            token=self.api.token,
            http_session=self.api.http_session,
        ).get()


class PluginsApp:
    """Add plugins to the URL path.

    Basically, valid plugins API could be handled by the same App class,
    but you need to add "plugins" to the request URL path.

    Returns:
        (App): With "plugins" added to the path.
    """

    def __init__(self, api):
        self.api = api

    def __getattr__(self, name):
        return App(self.api, f"plugins/{name.replace('_', '-')}")

    def __dir__(self):
        endpoints = self._get_api_endpoints()
        # We replace all hyphens with underscores so they can be used as attributes
        endpoint_attrs = [e.replace("-", "_") for e in endpoints.keys()]
        return super().__dir__() + endpoint_attrs

    def installed_plugins(self):
        """Returns raw response with installed plugins.

        Returns:
            (List[Response]): Raw response from Nautobot's installed plugins.

        Examples:
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
            base=f"{self.api.base_url}/plugins/installed-plugins",
            token=self.api.token,
            http_session=self.api.http_session,
        ).get()
        return installed_plugins

    def _get_api_endpoints(self):
        """Returns any plugin API endpoints available."""
        return Request(
            base=f"{self.api.base_url}/plugins/",
            token=self.api.token,
            http_session=self.api.http_session,
        ).get()
