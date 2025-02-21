"""API module for pynautobot."""

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

from packaging import version
import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from pynautobot.core.query import Request
from pynautobot.core.app import App, PluginsApp
from pynautobot.core.graphql import GraphQLQuery


# pylint: disable=too-many-instance-attributes, too-many-instance-attributes, too-many-arguments, too-many-positional-arguments
class Api:
    """The `Api` object is the primary entry point for interacting with a Nautobot
    instance using pynautobot.

    Args:
        url (str): The base URL of the Nautobot instance you want to connect to.
        token (str): Your Nautobot authentication token.
        threading (bool, optional): Enable threading for `.all()` and `.filter()`
            requests. Defaults to `False`.
        max_workers (int, optional): The maximum number of worker threads to use
            for `.all()` and `.filter()` requests. Defaults to the number of CPU cores.
        api_version (str, optional): Override the default Nautobot REST API version
            used for all requests.
        retries (int, optional): The number of retries for HTTP status codes
            429, 500, 502, 503, and 504. Defaults to 0 (no retries).
        verify (bool, optional): Whether to verify SSL certificates. Defaults to `True`.

    Attributes:
        dcim: An instance of the `App` class providing access to DCIM endpoints.
        cloud: An instance of the `App` class providing access to Cloud endpoints.
        ipam: An instance of the `App` class providing access to IPAM endpoints.
        circuits: An instance of the `App` class providing access to Circuits endpoints.
        tenancy: An instance of the `App` class providing access to Tenancy endpoints.
        extras: An instance of the `App` class providing access to Extras endpoints.
        virtualization: An instance of the `App` class providing access to Virtualization endpoints.
        users: An instance of the `App` class providing access to User endpoints.
        wireless: An instance of the `App` class providing access to Wireless endpoints.
        http_session (requests.Session): The underlying HTTP session object used for
            making requests to Nautobot. You can override the default session with your
            own to control HTTP behavior such as SSL verification, custom headers,
            retries, and timeouts. See the documentation on custom sessions
            for more information.

    Raises:
        AttributeError: If an invalid application name is provided.

    Examples:
        >>> import pynautobot
        >>> nb = pynautobot.api(
        ...     'http://localhost:8000',
        ...     token='d6f4e314a5b5fefd164995169f28ae32d987704f'
        ... )
        >>> nb.dcim.devices.all()
    """

    def __init__(
        self,
        url,
        token=None,
        threading=False,
        max_workers=4,
        api_version=None,
        retries=0,
        verify=True,
    ):
        from pynautobot import __version__  # pylint: disable=import-outside-toplevel

        base_url = f"{url.rstrip('/')}/api"
        self.token = token
        self.headers = {"Authorization": f"Token {self.token}"}
        self.base_url = base_url
        self.http_session = requests.Session()
        self.http_session.verify = verify
        self.http_session.headers.update({"User-Agent": f"python-pynautobot/{__version__}"})
        if retries:
            _adapter = HTTPAdapter(
                max_retries=Retry(
                    total=retries,
                    backoff_factor=1,
                    allowed_methods=None,
                    status_forcelist=[429, 500, 502, 503, 504],
                )
            )
            self.http_session.mount("http://", _adapter)
            self.http_session.mount("https://", _adapter)
        self.threading = threading
        self.max_workers = max_workers
        self.api_version = api_version

        self.dcim = App(self, "dcim")
        self.ipam = App(self, "ipam")
        self.cloud = App(self, "cloud")
        self.circuits = App(self, "circuits")
        self.tenancy = App(self, "tenancy")
        self.extras = App(self, "extras")
        self.virtualization = App(self, "virtualization")
        self.users = App(self, "users")
        self.wireless = App(self, "wireless")
        self.plugins = PluginsApp(self)
        self.graphql = GraphQLQuery(self)
        self._validate_version()

    def _validate_version(self):
        """Validate API version if eq or ge than 2.0 raise an error."""
        api_version = self.version
        if api_version.replace(".", "").isnumeric() and version.parse(api_version) < version.parse("2.0"):
            raise ValueError("Nautobot version 1 detected, please downgrade pynautobot to version 1.x")

    @property
    def version(self):
        """Retrieves the version of the Nautobot REST API that the connected instance is using.

        This method can be helpful for checking API compatibility and determining
        if specific features or syntaxes are available.

        Returns:
            (str): The Nautobot API version string.

        Raises:
            requests.exceptions.RequestException: If there is an error fetching the
                version information from Nautobot.

        Examples:
            >>> import pynautobot
            >>> nb = pynautobot.api(
            ...     'http://localhost:8000',
            ...     token='d6f4e314a5b5fefd164995169f28ae32d987704f'
            ... )
            >>> nb.version
            '1.0'
        """

        return Request(
            base=self.base_url,
            http_session=self.http_session,
            api_version=self.api_version,
            token=self.token,
        ).get_version()

    def openapi(self):
        """Retrieves the OpenAPI specification (OAS) document for the connected Nautobot instance.

        The OpenAPI specification provides a machine-readable description of the Nautobot REST API,
        including available endpoints, parameters, request and response formats, and more.

        This can be useful for tools like code generation or API clients in other languages.

        Returns:
            (dict): The OpenAPI specification document as a Python dictionary.

        Raises:
            requests.exceptions.RequestException: If there is an error fetching the
                OpenAPI spec from Nautobot.

        Examples:
            >>> import pynautobot
            >>> nb = pynautobot.api(
            ...     'http://localhost:8000',
            ...     token='d6f4e314a5b5fefd164995169f28ae32d987704f'
            ... )
            >>> nb.openapi()
            {...}
        """

        return Request(
            base=self.base_url,
            http_session=self.http_session,
            api_version=self.api_version,
            token=self.token,
        ).get_openapi()

    def status(self):
        """Retrieves status information about the connected Nautobot instance.

        This method provides various details about the Nautobot instance, including:

        * Django version
        * Installed apps and their versions
        * Nautobot version
        * Active plugins (if any)
        * Python version
        * Number of running RQ workers (if applicable)

        **Availability:** Requires Nautobot version 2.10.0 or newer.

        Returns:
            (dict): A dictionary containing the status information as returned by Nautobot.

        Raises:
            pynautobot.exceptions.RequestError: If the request to Nautobot fails.

        Examples:
            >>> import pprint
            >>> nb = pynautobot.api(
            ...     'http://localhost:8000',
            ...     token='d6f4e314a5b5fefd164995169f28ae32d987704f'
            ... )
            >>> pprint.pprint(nb.status())
            {'django-version': '3.1.3',
            'installed-apps': {...},
            'nautobot-version': '1.0.0',
            'plugins': {},
            'python-version': '3.7.3',
            'rq-workers-running': 1}
        """
        return Request(
            base=self.base_url,
            token=self.token,
            http_session=self.http_session,
            api_version=self.api_version,
        ).get_status()
