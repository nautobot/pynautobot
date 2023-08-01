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
from typing import Dict
from pynautobot.core.query import Request, RequestError
from pynautobot.core.response import Record

RESERVED_KWARGS = ("pk", "limit", "offset")


def response_loader(req, return_obj, endpoint):
    if isinstance(req, list):
        return [return_obj(i, endpoint.api, endpoint) for i in req]
    return return_obj(req, endpoint.api, endpoint)


class Endpoint(object):
    """Represent actions available on endpoints in the Nautobot API.

    Takes ``name`` and ``app`` passed from App() and builds the correct
    url to make queries to and the proper Response object to return
    results in.

    :arg obj api: Takes :py:class:`.Api` created at instantiation.
    :arg obj app: Takes :py:class:`.App`.
    :arg str name: Name of endpoint passed to App().
    :arg obj,optional model: Custom model for given app.

    .. note::

        In order to call Nautobot endpoints with dashes in their
        names you should convert the dash to an underscore.
        (E.g. querying the ip-addresses endpoint is done with
        ``nb.ipam.ip_addresses.all()``.)

    """

    def __init__(self, api, app, name, model=None):
        self.return_obj = self._lookup_ret_obj(name, model)
        self.name = name.replace("_", "-")
        self.api = api
        self.base_url = api.base_url
        self.token = api.token
        self.url = "{base_url}/{app}/{endpoint}".format(
            base_url=self.base_url,
            app=app.name,
            endpoint=self.name,
        )
        self._choices = None

    def _lookup_ret_obj(self, name, model):
        """Loads unique Response objects.

        This method loads a unique response object for an endpoint if
        it exists. Otherwise return a generic `Record` object.

        :arg str name: Endpoint name.
        :arg obj model: The application model that
            contains unique Record objects.

        :Returns: Record (obj)
        """
        if model:
            name = name.title().replace("_", "").replace("-", "")
            ret = getattr(model, name, Record)
        else:
            ret = Record
        return ret

    def all(self, api_version=None):
        """Queries the 'ListView' of a given endpoint.

        Returns all objects from an endpoint.

        :arg str,optional api_version: Override default or globally-set Nautobot REST API
            version for this single request.

        :Returns: List of :py:class:`.Record` objects.

        :Examples:

        >>> nb.dcim.devices.all()
        [test1-a3-oobsw2, test1-a3-oobsw3, test1-a3-oobsw4]
        >>>
        """

        api_version = api_version or self.api.api_version
        req = Request(
            base="{}/".format(self.url),
            token=self.token,
            http_session=self.api.http_session,
            threading=self.api.threading,
            api_version=api_version,
        )

        return response_loader(req.get(), self.return_obj, self)

    def get(self, *args, **kwargs):
        r"""Queries the DetailsView of a given endpoint.

        :arg int,optional key: id for the item to be
            retrieved.

        :arg str,optional \**kwargs: Accepts the same keyword args as
            filter(). Any search argument the endpoint accepts can
            be added as a keyword arg.

        :arg str,optional api_version: Override default or globally-set Nautobot REST API
            version for this single request.

        :returns: A single :py:class:`.Record` object or None

        :raises ValueError: if kwarg search return more than one value.

        :Examples:

        Referencing with a kwarg that only returns one value.

        >>> nb.dcim.devices.get(name='test1-a3-tor1b')
        test1-a3-tor1b
        >>>

        Referencing with an id.

        >>> nb.dcim.devices.get(1)
        test1-edge1
        >>>
        """

        try:
            key = args[0]
        except IndexError:
            key = None

        is_api_version = kwargs.pop("api_version") if kwargs.get("api_version") else None
        api_version = is_api_version or self.api.api_version

        if not key:
            filter_lookup = self.filter(**kwargs)
            if filter_lookup:
                if len(filter_lookup) > 1:
                    raise ValueError(
                        "get() returned more than one result. "
                        "Check that the kwarg(s) passed are valid for this "
                        "endpoint or use filter() or all() instead."
                    )
                else:
                    return filter_lookup[0]
            return None

        req = Request(
            key=key,
            base=self.url,
            token=self.token,
            http_session=self.api.http_session,
            api_version=api_version,
        )

        try:
            resp = req.get()
        except RequestError as e:
            if e.req.status_code == 404:
                return None
            else:
                raise e

        return response_loader(resp, self.return_obj, self)

    def filter(self, *args, api_version=None, **kwargs):
        r"""Queries the 'ListView' of a given endpoint.

        Takes named arguments that match the usable filters on a
        given endpoint. If an argument is passed then it's used as a
        freeform search argument if the endpoint supports it.

        :arg str,optional \*args: Freeform search string that's
            accepted on given endpoint.
        :arg str,optional \**kwargs: Any search argument the
            endpoint accepts can be added as a keyword arg.
        :arg str,optional api_version: Override default or globally-set
            Nautobot REST API version for this single request.

        :Returns: A list of :py:class:`.Record` objects.

        :Examples:

        To return a list of objects matching a named argument filter.

        >>> nb.dcim.devices.filter(role='leaf-switch')
        [test1-a3-tor1b, test1-a3-tor1c, test1-a3-tor1d, test1-a3-tor2a]
        >>>

        Using a freeform query along with a named argument.

        >>> nb.dcim.devices.filter('a3', role='leaf-switch')
        [test1-a3-tor1b, test1-a3-tor1c, test1-a3-tor1d, test1-a3-tor2a]
        >>>

        Chaining multiple named arguments.

        >>> nb.dcim.devices.filter(role='leaf-switch', status=True)
        [test1-leaf2]
        >>>

        Passing a list as a named argument adds multiple filters of the
        same value.

        >>> nb.dcim.devices.filter(role=['leaf-switch', 'spine-switch'])
        [test1-a3-spine1, test1-a3-spine2, test1-a3-leaf1]
        >>>
        """

        if args:
            kwargs.update({"q": args[0]})

        if not kwargs:
            raise ValueError("filter must be passed kwargs. Perhaps use all() instead.")
        if any(i in RESERVED_KWARGS for i in kwargs):
            raise ValueError("A reserved {} kwarg was passed. Please remove it " "try again.".format(RESERVED_KWARGS))

        api_version = api_version or self.api.api_version
        req = Request(
            filters=kwargs,
            base=self.url,
            token=self.token,
            http_session=self.api.http_session,
            threading=self.api.threading,
            api_version=api_version,
        )

        return response_loader(req.get(), self.return_obj, self)

    def create(self, *args, api_version=None, **kwargs):
        r"""Creates an object on an endpoint.

        Allows for the creation of new objects on an endpoint. Named
        arguments are converted to json properties, and a single object
        is created. Nautobot's bulk creation capabilities can be used by
        passing a list of dictionaries as the first argument.

        .. note:

            Any positional arguments will supercede named ones.

        :arg list \*args: A list of dictionaries containing the
            properties of the objects to be created.
        :arg str \**kwargs: key/value strings representing
            properties on a json object.
        :arg str,optional api_version: Override default or globally-set
            Nautobot REST API version for this single request.

        :returns: A list or single :py:class:`.Record` object depending
            on whether a bulk creation was requested.

        :Examples:

        Creating an object on the `devices` endpoint you can lookup a
        device_role's name with:

        >>> nautobot.dcim.devices.create(
        ...    name='test',
        ...    device_role=1,
        ... )
        >>>

        Use bulk creation by passing a list of dictionaries:

        >>> nb.dcim.devices.create([
        ...     {
        ...         "name": "test1-core3",
        ...         "device_role": 3,
        ...         "site": 1,
        ...         "device_type": 1,
        ...         "status": 1
        ...     },
        ...     {
        ...         "name": "test1-core4",
        ...         "device_role": 3,
        ...         "site": 1,
        ...         "device_type": 1,
        ...         "status": 1
        ...     }
        ... ])
        """

        api_version = api_version or self.api.api_version

        req = Request(
            base=self.url,
            token=self.token,
            http_session=self.api.http_session,
            api_version=api_version,
        ).post(args[0] if args else kwargs)

        return response_loader(req, self.return_obj, self)

    def update(self, id: str, data: Dict[str, any]):
        """
        Update a resource with a dictionary.

        Accepts the id of the object that needs to be updated as well as
        a dictionary of k/v pairs used to update an object. The object
        is directly updated on the server using a PATCH request without
        fetching object information.

        For fields requiring an object reference (such as a device location),
        the API user is responsible for providing the object ID or the object
        URL. This API will not accept the pynautobot object directly.

        :arg str id: Identifier of the object being updated
        :arg dict data: Dictionary containing the k/v to update the
            record object with.
        :returns: True if PATCH request was successful.
        :example:

        >>> nb.dcim.devices.update(id="0238a4e3-66f2-455a-831f-5f177215de0f", data={
        ...     "name": "test-switch2",
        ...     "serial": "ABC321",
        ...     "location": "9b1f53c7-89fa-4fb2-a89a-b97364fef50c",
        ... })
        True
        """
        req = Request(
            key=id,
            base=self.url,
            token=self.api.token,
            http_session=self.api.http_session,
            api_version=self.api.api_version,
        )
        if req.patch(data):
            return True
        return False

    def choices(self, api_version=None):
        """Returns all choices from the endpoint.

        The returned dict is also saved in the endpoint object (in
        ``_choices`` attribute) so that later calls will return the same data
        without recurring requests to Nautobot. When using ``.choices()`` in
        long-running applications, consider restarting them whenever Nautobot is
        upgraded, to prevent using stale choices data.

        :arg str,optional api_version: Override default or globally-set
            Nautobot REST API version for this single request.

        :Returns: Dict containing the available choices.

        :Example (from Nautobot 2.8.x):

        >>> from pprint import pprint
        >>> pprint(nb.ipam.ip_addresses.choices())
        {'role': [{'display_name': 'Loopback', 'value': 'loopback'},
                  {'display_name': 'Secondary', 'value': 'secondary'},
                  {'display_name': 'Anycast', 'value': 'anycast'},
                  {'display_name': 'VIP', 'value': 'vip'},
                  {'display_name': 'VRRP', 'value': 'vrrp'},
                  {'display_name': 'HSRP', 'value': 'hsrp'},
                  {'display_name': 'GLBP', 'value': 'glbp'},
                  {'display_name': 'CARP', 'value': 'carp'}],
         'status': [{'display_name': 'Active', 'value': 'active'},
                    {'display_name': 'Reserved', 'value': 'reserved'},
                    {'display_name': 'Deprecated', 'value': 'deprecated'},
                    {'display_name': 'DHCP', 'value': 'dhcp'}]}
        >>>
        """
        if self._choices:
            return self._choices

        api_version = api_version or self.api.api_version

        req = Request(
            base=self.url,
            token=self.api.token,
            http_session=self.api.http_session,
            api_version=api_version,
        ).options()
        try:
            post_data = req["actions"]["POST"]
        except KeyError:
            raise ValueError("Unexpected format in the OPTIONS response at {}".format(self.url))
        self._choices = {}
        for prop in post_data:
            if "choices" in post_data[prop]:
                self._choices[prop] = post_data[prop]["choices"]

        return self._choices

    def count(self, *args, api_version=None, **kwargs):
        r"""Returns the count of objects in a query.

        Takes named arguments that match the usable filters on a
        given endpoint. If an argument is passed then it's used as a
        freeform search argument if the endpoint supports it. If no
        arguments are passed the count for all objects on an endpoint
        are returned.

        :arg str,optional \*args: Freeform search string that's
            accepted on given endpoint.
        :arg str,optional \**kwargs: Any search argument the
            endpoint accepts can be added as a keyword arg.
        :arg str,optional api_version: Override default or globally-set
            Nautobot REST API version for this single request.

        :Returns: Integer with count of objects returns by query.

        :Examples:

        To return a count of objects matching a named argument filter.

        >>> nb.dcim.devices.count(site='tst1')
        5827
        >>>

        To return a count of objects on an entire endpoint.

        >>> nb.dcim.devices.count()
        87382
        >>>
        """

        if args:
            kwargs.update({"q": args[0]})

        if any(i in RESERVED_KWARGS for i in kwargs):
            raise ValueError("A reserved {} kwarg was passed. Please remove it " "try again.".format(RESERVED_KWARGS))

        api_version = api_version or self.api.api_version

        ret = Request(
            filters=kwargs, base=self.url, token=self.token, http_session=self.api.http_session, api_version=api_version
        )

        return ret.get_count()


class DetailEndpoint(object):
    """Enables read/write Operations on detail endpoints.

    Endpoints like ``available-ips`` that are detail routes off
    traditional endpoints are handled with this class.
    """

    def __init__(self, parent_obj, name, custom_return=None):
        self.parent_obj = parent_obj
        self.custom_return = custom_return
        self.url = "{}/{}/{}/".format(parent_obj.endpoint.url, parent_obj.id, name)

        self.request_kwargs = dict(
            base=self.url,
            token=parent_obj.api.token,
            http_session=parent_obj.api.http_session,
        )

    def list(self, api_version=None, **kwargs):
        r"""The view operation for a detail endpoint

        Returns the response from Nautobot for a detail endpoint.

        Args:
            :arg str,optional api_version: Override default or globally set Nautobot REST API version for this single request.
            **kwargs: key/value pairs that get converted into url parameters when passed to the endpoint.
                E.g. ``.list(method='get_facts')`` would be converted to ``.../?method=get_facts``.

        :returns: A dictionary or list of dictionaries retrieved from
            Nautobot.
        """
        api_version = api_version or self.parent_obj.api.api_version

        req = Request(api_version=api_version, **self.request_kwargs).get(add_params=kwargs)

        if self.custom_return:
            return response_loader(req, self.custom_return, self.parent_obj.endpoint)
        return req

    def create(self, data=None, api_version=None):
        """The write operation for a detail endpoint.

        Creates objects on a detail endpoint in Nautobot.

        :arg dict/list,optional data: A dictionary containing the
            key/value pair of the items you're creating on the parent
            object. Defaults to empty dict which will create a single
            item with default values.
        :args str,optional api_version: Override default or globally set
            Nautobot REST API version for this single request.

        :returns: A dictionary or list of dictionaries its created in
            Nautobot.
        """
        data = data or {}
        api_version = api_version or self.parent_obj.api.api_version

        req = Request(api_version=api_version, **self.request_kwargs).post(data)
        if self.custom_return:
            return response_loader(req, self.custom_return, self.parent_obj.endpoint)
        return req


class RODetailEndpoint(DetailEndpoint):
    def create(self, data):
        raise NotImplementedError("Writes are not supported for this endpoint.")


class JobsEndpoint(Endpoint):
    """Extend Endpoint class to support run method only for jobs."""

    def run(self, *args, api_version=None, **kwargs):
        r"""Runs a job based on the class_path provided to the job.

        Takes a kwarg of `class_path` or `job_id` to specify the job that should be run.

        :arg str,optional \*args: Freeform search string that's
            accepted on given endpoint.
        :arg str,optional \**kwargs: Any search argument the
            endpoint accepts can be added as a keyword arg.
        :arg str,optional api_version: Override default or globally-set
            Nautobot REST API version for this single request.

        :Returns: Job details: job_result object uuid found at `obj.result.id`.

        :Examples:

        To return a count of objects matching a named argument filter.

        >>> nb.extras.jobs.run(
                class_path="local/data_quality/VerifyHostnames",
                data={"hostname_regex": ".*"},
                commit=True,
            )
        >>>
        """
        api_version = api_version or self.api.api_version or self.api.version

        # Check Nautobot Version as API version can be `None`.  Job run endpoints changed in 1.3.
        if float(api_version) < 1.3:
            if not kwargs.get("class_path"):
                raise ValueError(
                    'Keyword Argument "class_path" is required to run a job in Nautobot APIv1.2 and older.'
                )
            job_run_url = f"{self.url}/{kwargs['class_path']}/run/"
        else:
            if not kwargs.get("job_id"):
                raise ValueError('Keyword Argument "job_id" is required to run a job in Nautobot APIv1.3 and newer.')
            job_run_url = f"{self.url}/{kwargs['job_id']}/run/"

        req = Request(
            base=job_run_url,
            token=self.token,
            http_session=self.api.http_session,
            api_version=api_version,
        ).post(args[0] if args else kwargs)

        return response_loader(req, self.return_obj, self)
