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

"""Defines classes and functions for making HTTP requests to the Nautobot API."""

try:
    import concurrent.futures as cf
except ImportError:
    pass
import json
import requests


def calc_pages(limit, count):
    """Calculate number of pages required for full results set."""
    return int(count / limit) + (limit % count > 0)


class RequestError(Exception):
    """Basic Request Exception

    More detailed exception that returns the original requests object
    for inspection. Along with some attributes with specific details
    from the requests object. If return is JSON we decode and add it
    to the message.

    Examples:
        >>> try:
        ...     nb.dcim.devices.create(name="destined-for-failure")
        ... except pynautobot.RequestError as e:
        ...     print(e.error)
    """

    def __init__(self, message):
        req = message

        if req.status_code == 404:
            message = f"The requested url: {req.url} could not be found."
        else:
            try:
                message = f"The request failed with code {req.status_code} {req.reason}: {req.json()}"
            except ValueError:
                message = (
                    f"The request failed with code {req.status_code} {req.reason} but more specific "
                    "details were not returned in json. Check the Nautobot Logs "
                    "or investigate this exception's error attribute."
                )

        super().__init__(message)
        self.req = req
        self.request_body = req.request.body
        self.base = req.url
        self.error = req.text


class RequestErrorFromException(Exception):
    """RequestErrorFromException is raised from exception."""


class AllocationError(Exception):
    """Allocation Exception

    Used with available-ips/available-prefixes when there is no
    room for allocation and Nautobot returns 204 No Content.
    """

    def __init__(self, message):
        req = message

        message = "The requested allocation could not be fulfilled."

        super().__init__(message)
        self.req = req
        self.request_body = req.request.body
        self.base = req.url
        self.error = message


class ContentError(Exception):
    """Content Exception

    If the API URL does not point to a valid Nautobot API, the server may
    return a valid response code, but the content is not json. This
    exception is raised in those cases.
    """

    def __init__(self, message):
        req = message

        message = "The server returned invalid (non-json) data. Maybe not a Nautobot server?"

        super().__init__(message)
        self.req = req
        self.request_body = req.request.body
        self.base = req.url
        self.error = message


# pylint: disable=too-many-instance-attributes
class Request:
    """Creates requests to the Nautobot API.

    Responsible for building the URL and making the HTTP(S) requests to
    Nautobot's API.

    Args:
        base (str): Base URL passed in api() instantiation.
        filters (dict, optional): Contains key/value pairs that
            correlate to the filters a given endpoint accepts.
            In (e.g. /api/dcim/devices/?name='test'), 'name': 'test'
            would be in the filters dict.
        max_workers (int, optional): Set the maximum workers for threading in ``.all()``
            and ``.filter()`` requests.
    """

    # pylint: disable=too-many-positional-arguments, too-many-arguments
    def __init__(
        self,
        base,
        http_session,
        filters=None,
        limit=None,
        offset=None,
        key=None,
        token=None,
        threading=False,
        max_workers=4,
        api_version=None,
    ):
        """Instantiates a new Request object

        Args:
            base (string): Base URL passed in api() instantiation.
            filters (dict, optional): contains key/value pairs that
                correlate to the filters a given endpoint accepts.
                In (e.g. /api/dcim/devices/?name='test') 'name': 'test'
                would be in the filters dict.
            key (int, optional): database id of the item being queried.
            api_version (str, optional): Set to override the default Nautobot REST API Version.
        """
        self.base = self.normalize_url(base)
        self.filters = filters
        self.key = key
        self.token = token
        self.http_session = http_session
        self.url = f"{self.base}{key}/" if key else self.base
        self.threading = threading
        self.max_workers = max_workers
        self.api_version = api_version
        self.limit = limit
        self.offset = offset

    def get_openapi(self):
        """Gets the OpenAPI Spec"""
        headers = {
            "Content-Type": "application/json;",
            "Authorization": f"Token {self.token}",
        }

        if self.api_version:
            headers["accept"] = f"application/json; version={self.api_version}"

        try:
            req = self.http_session.get(
                f"{self.normalize_url(self.base)}docs/?format=openapi",
                headers=headers,
            )
        except requests.exceptions.RetryError as error:
            raise RequestErrorFromException from error

        if req.ok:
            return req.json()
        raise RequestError(req)

    def get_version(self):
        """Gets the API version of Nautobot.

        Issues a GET request to the base URL to read the API version from the
        response headers.

        Raises:
            RequestError: If req.ok returns false.

        Returns:
            (str): Version number as a string. Empty string if version is not present in the headers.
        """
        headers = {
            "Content-Type": "application/json;",
            "Authorization": f"Token {self.token}",
        }
        if self.api_version:
            headers["accept"] = f"application/json; version={self.api_version}"

        try:
            req = self.http_session.get(
                self.normalize_url(self.base),
                headers=headers,
            )
        except requests.exceptions.RetryError as error:
            raise RequestErrorFromException from error

        if req.ok:
            return req.headers.get("API-Version", "")
        raise RequestError(req)

    def get_status(self):
        """Gets the status from /api/status/ endpoint in Nautobot.

        Returns:
            (dict): Dictionary as returned by Nautobot.

        Raises:
            RequestError: If request is not successful.
        """

        headers = {
            "Content-Type": "application/json;",
            "Authorization": f"Token {self.token}",
        }
        if self.token:
            headers["authorization"] = f"Token {self.token}"

        if self.api_version:
            headers["accept"] = f"application/json; version={self.api_version}"

        try:
            req = self.http_session.get(
                f"{self.normalize_url(self.base)}status/",
                headers=headers,
            )
        except requests.exceptions.RetryError as error:
            raise RequestErrorFromException from error

        if req.ok:
            return req.json()
        raise RequestError(req)

    def normalize_url(self, url):
        """Builds a url for POST actions."""
        if url[-1] != "/":
            return f"{url}/"

        return url

    # pylint: disable=too-many-branches
    def _make_call(self, verb="get", url_override=None, add_params=None, data=None):
        if verb in ("post", "put") or (verb in ("delete") and data):
            headers = {"Content-Type": "application/json;"}
        else:
            headers = {"accept": "application/json;"}

        if self.token:
            headers["authorization"] = f"Token {self.token}"

        if self.api_version:
            headers["accept"] = f"application/json; version={self.api_version}"

        params = {}
        if not url_override:
            if self.filters:
                params.update(self.filters)
            if add_params:
                params.update(add_params)

        try:
            req = getattr(self.http_session, verb)(url_override or self.url, headers=headers, params=params, json=data)
        except requests.exceptions.RetryError as error:
            raise RequestErrorFromException from error

        if req.status_code == 204 and verb == "post":
            raise AllocationError(req)
        if verb == "delete":
            if req.ok:
                return True
            raise RequestError(req)
        if req.ok:
            try:
                return req.json()
            except json.JSONDecodeError as exc:
                raise ContentError(req) from exc
        else:
            raise RequestError(req)

    def concurrent_get(self, ret, page_size, page_offsets):
        """Concurrently get paginated results."""
        futures_to_results = []
        with cf.ThreadPoolExecutor(max_workers=self.max_workers) as pool:
            for offset in page_offsets:
                new_params = {"offset": offset, "limit": page_size}
                futures_to_results.append(pool.submit(self._make_call, add_params=new_params))

            for future in cf.as_completed(futures_to_results):
                result = future.result()
                ret.extend(result["results"])

    def get(self, add_params=None):
        """Makes a GET request.

        Makes a GET request to Nautobot's API, and automatically recurses
        any paginated results.

        Raises:
            RequestError: If req.ok returns false.
            ContentError: If response is not JSON.

        Returns:
            (List[Response]): List of `Response` objects returned from the
                endpoint.
        """
        if not add_params and self.limit is not None:
            add_params = {"limit": self.limit}
            if self.limit and self.offset is not None:
                add_params["offset"] = self.offset

        def req_all(add_params):
            req = self._make_call(add_params=add_params)
            if isinstance(req, dict) and req.get("results") is not None:
                ret = req["results"]
                first_run = True
                while req["next"] and self.offset is None:
                    if not add_params and first_run:
                        req = self._make_call(add_params={"limit": req["count"], "offset": len(req["results"])})
                    else:
                        req = self._make_call(url_override=req["next"])
                    first_run = False
                    ret.extend(req["results"])
                return ret
            return req

        def req_all_threaded(add_params):
            if add_params is None:
                # Limit must be 0 to discover the max page size
                add_params = {"limit": 0}
            req = self._make_call(add_params=add_params)
            if isinstance(req, dict) and req.get("results") is not None:
                ret = req["results"]
                if req.get("next") and self.offset is None:
                    page_size = len(req["results"])
                    pages = calc_pages(page_size, req["count"])
                    page_offsets = [increment * page_size for increment in range(1, pages)]
                    if pages == 1:
                        req = self._make_call(url_override=req.get("next"))
                        ret.extend(req["results"])
                    else:
                        self.concurrent_get(ret, page_size, page_offsets)

                return ret
            return req

        if self.threading:
            return req_all_threaded(add_params)

        return req_all(add_params)

    def put(self, data: dict) -> dict:
        """Makes a PUT request to the Nautobot API.

        Args:
            data: (dict) The data to be sent in the PUT request body. It will be
                serialized to JSON before sending.

        Raises:
            RequestError: If the request fails (i.e., req.ok returns False).
            ContentError: If the response cannot be deserialized from JSON.

        Returns:
            (dict): The deserialized JSON response from the Nautobot API.
        """
        return self._make_call(verb="put", data=data)

    def post(self, data: dict) -> dict:
        """Makes a POST request to the Nautobot API.

        Args:
            data: (dict) The data to be sent in the POST request body. It will be
                serialized to JSON before sending.

        Raises:
            RequestError: If the request fails (i.e., req.ok returns False).
            AllocationError: If the status code is 204 (No Content), indicating
                no available resources for allocation (e.g., available IPs or prefixes).
            ContentError: If the response cannot be deserialized from JSON.

        Returns:
            (dict): The deserialized JSON response from the Nautobot API.
        """
        return self._make_call(verb="post", data=data)

    def delete(self, data=None):
        """Makes DELETE request.

        Makes a DELETE request to Nautobot's API.

        Args:
            data (list): Contains a dict that will be turned into a json object
                and sent to the API.

        Returns:
            (bool): True if successful.

        Raises:
            RequestError: If req.ok doesn't return True.
        """
        return self._make_call(verb="delete", data=data)

    def patch(self, data: dict) -> dict:
        """Makes a PATCH request to the Nautobot API.

        Args:
            data: (dict) The data to be sent in the PATCH request body. It will be
                serialized to JSON before sending.

        Raises:
            RequestError: If the request fails (i.e., req.ok returns False).
            ContentError: If the response cannot be deserialized from JSON.

        Returns:
            dict: The deserialized JSON response from the Nautobot API.
        """
        return self._make_call(verb="patch", data=data)

    def options(self) -> dict:
        """Retrieves allowed HTTP methods for a Nautobot API endpoint.

        Makes an OPTIONS request to determine the allowed HTTP methods
        supported by a specific Nautobot API endpoint.

        Raises:
            RequestError: If the request fails (i.e., req.ok returns False).
            ContentError: If the response cannot be deserialized from JSON.

        Returns:
            (dict): The deserialized JSON response from the Nautobot API,
                containing information about allowed methods.
        """

        return self._make_call(verb="options")

    def get_count(self, *args, **kwargs) -> int:  # pylint: disable=unused-argument
        """Retrieves the number of objects matching a query in the Nautobot API.

        Makes a GET request to the specified endpoint with a limited response
        (limit=1) and extracts the "count" field from the response to determine
        the total number of objects that would be returned by a full query
        with the same parameters.

        Args:
            *args (list): Additional positional arguments to be passed to the
                Nautobot API endpoint.
            **kwargs (dict): Additional keyword arguments to be passed to the
                Nautobot API endpoint.

        Raises:
            RequestError: If the request fails (i.e., req.ok returns False).
            ContentError: If the response cannot be deserialized from JSON.

        Returns:
            (int): The total number of objects that would match the provided query.
        """

        return self._make_call(add_params={"limit": 1})["count"]
