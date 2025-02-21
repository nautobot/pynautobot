"""Provides classes and functions for interacting with the Nautobot API endpoints."""

# (c) 2017 DigitalOcean
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

from time import sleep

from typing import List, Dict, Any
from uuid import UUID
from pynautobot.core.query import Request, RequestError
from pynautobot.core.response import Record

RESERVED_KWARGS = ("pk",)


def response_loader(req, return_obj, endpoint):
    """Loads the response from the API into an object."""
    if isinstance(req, list):
        return [return_obj(i, endpoint.api, endpoint) for i in req]
    return return_obj(req, endpoint.api, endpoint)


class Endpoint:
    """Represent actions available on endpoints in the Nautobot API.

    Takes `name` and `app` passed from `App()` and builds the correct
    URL to make queries to and the proper Response object to return
    results in.

    Args:
        api (object): Takes `Api` created at instantiation.
        app (object): Takes `App`.
        name (str): Name of endpoint passed to `App()`.
        model (object, optional): Custom model for given app.

    Note:
        In order to call Nautobot endpoints with dashes in their
        names you should convert the dash to an underscore.
        (E.g. querying the ip-addresses endpoint is done with
        `nb.ipam.ip_addresses.all()`.)
    """

    def __init__(self, api, app, name, model=None):
        self.return_obj = self._lookup_ret_obj(name, model)
        self.name = name.replace("_", "-")
        self.api = api
        self.base_url = api.base_url
        self.token = api.token
        self.url = f"{self.base_url}/{app.name}/{self.name}"
        self._choices = None

    def _lookup_ret_obj(self, name, model):
        """Loads unique Response objects.

        This method loads a unique response object for an endpoint if
        it exists. Otherwise, it returns a generic `Record` object.

        Args:
            name (str): Endpoint name.
            model (obj): The application model that contains unique Record objects.

        Returns:
            (Record): Unique response object if exists, otherwise a generic `Record` object.
        """
        if model:
            name = name.title().replace("_", "").replace("-", "")
            ret = getattr(model, name, Record)
        else:
            ret = Record
        return ret

    def all(self, *args, **kwargs):
        """Queries the 'ListView' of a given endpoint.

        Returns all objects from an endpoint.

        Optional Args:
            api_version (str, optional): Override default or globally-set Nautobot REST API
                version for this single request.
            limit (int, optional): Overrides the max page size on
                paginated returns.  This defines the number of records that will
                be returned with each query to the Netbox server.  The queries
                will be made as you iterate through the result set.
            offset (int, optional): Overrides the offset on paginated returns.
        Returns:
            (list): List of :py:class:`.Record` objects.

        Examples:
            >>> nb.dcim.devices.all()
            [test1-a3-oobsw2, test1-a3-oobsw3, test1-a3-oobsw4]
        """
        return self.filter(*args, **kwargs)

    def get(self, *args, **kwargs):
        """Queries the DetailsView of a given endpoint.

        Optional Args:
            key (int, optional): ID for the item to be retrieved.
            **kwargs (str, optional): Accepts the same keyword args as filter().
                Any search argument the endpoint accepts can be added as a keyword arg.
            api_version (str, optional): Override default or globally-set Nautobot REST API
                version for this single request.

        Returns:
            (Union[Record, None]): A single :py:class:`.Record` object or None.

        Raises:
            ValueError: If kwarg search returns more than one value.

        Examples:
            Referencing with a kwarg that only returns one value.
            >>> nb.dcim.devices.get(name='test1-a3-tor1b')
            test1-a3-tor1b

            Referencing with an id.
            >>> nb.dcim.devices.get(1)
            test1-edge1
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
            raise e

        return response_loader(resp, self.return_obj, self)

    def filter(self, *args, api_version=None, **kwargs):
        """Queries the 'ListView' of a given endpoint.

        Takes named arguments that match the usable filters on a
        given endpoint. If an argument is passed then it's used as a
        freeform search argument if the endpoint supports it.

        Args:
            *args (str, optional): Freeform search string that's
                accepted on given endpoint.
            **kwargs (str, optional): Any search argument the
                endpoint accepts can be added as a keyword arg.
            api_version (str, optional): Override default or globally-set
                Nautobot REST API version for this single request.

        Returns:
            (list): A list of :py:class:`.Record` objects.

        Examples:
            To return a list of objects matching a named argument filter.
            >>> nb.dcim.devices.filter(role='leaf-switch')
            [test1-a3-tor1b, test1-a3-tor1c, test1-a3-tor1d, test1-a3-tor2a]

            Using a freeform query along with a named argument.
            >>> nb.dcim.devices.filter('a3', role='leaf-switch')
            [test1-a3-tor1b, test1-a3-tor1c, test1-a3-tor1d, test1-a3-tor2a]

            Chaining multiple named arguments.
            >>> nb.dcim.devices.filter(role='leaf-switch', status=True)
            [test1-leaf2]

            Passing a list as a named argument adds multiple filters of the
            same value.
            >>> nb.dcim.devices.filter(role=['leaf-switch', 'spine-switch'])
            [test1-a3-spine1, test1-a3-spine2, test1-a3-leaf1]
        """

        if args:
            kwargs.update({"q": args[0]})

        if any(i in RESERVED_KWARGS for i in kwargs):
            raise ValueError(f"A reserved {RESERVED_KWARGS} kwarg was passed. Please remove it and try again.")
        limit = kwargs.pop("limit") if "limit" in kwargs else None
        offset = kwargs.pop("offset") if "offset" in kwargs else None
        if not limit and offset is not None:
            raise ValueError("offset requires a positive limit value")
        api_version = api_version or self.api.api_version
        req = Request(
            filters=kwargs,
            base=self.url,
            token=self.token,
            http_session=self.api.http_session,
            threading=self.api.threading,
            api_version=api_version,
            limit=limit,
            offset=offset,
        )

        return response_loader(req.get(), self.return_obj, self)

    def create(self, *args, api_version=None, **kwargs):
        """Creates an object on an endpoint.

        Allows for the creation of new objects on an endpoint. Named
        arguments are converted to JSON properties, and a single object
        is created. Nautobot's bulk creation capabilities can be used by
        passing a list of dictionaries as the first argument.

        Note:
            Any positional arguments will supersede named ones.

        Args:
            *args (list): A list of dictionaries containing the
                properties of the objects to be created.
            **kwargs (str): Key/value strings representing
                properties on a JSON object.
            api_version (str, optional): Override default or globally-set
                Nautobot REST API version for this single request.

        Returns:
            (Union[Record, List[Record]]): A list or single :py:class:`.Record` object depending
                on whether a bulk creation was requested.

        Examples:
            Creating an object on the `devices` endpoint you can look up a
            device_role's name with:
            >>> nautobot.dcim.devices.create(
            ...    name='test',
            ...    device_role=1,
            ... )

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

    def update(self, *args, **kwargs):
        """Update a single resource with a dictionary or bulk update a list of objects.

        Allows for bulk updating of existing objects on an endpoint.
        Objects is a list which contain either JSON/dicts or Record
        derived objects, which contain the updates to apply.
        If JSON/dicts are used, then the id of the object *must* be
        included.

        Args:
            *args (list, optional): A list of dicts or a list of Record.
            **kwargs (str, optional): See Below.

        Keyword Arguments:
            id (string): Identifier of the object being updated.
            data (dict): Key/value pairs to update the record object with.

        Returns:
            (Union[Record, List[Record]]): A list or single :py:class:`.Record` object depending
                on whether a bulk update was requested.

        Examples:
            Accepts the id of the object that needs to be updated as well as a
            dictionary of k/v pairs used to update an object.
            >>> nb.dcim.devices.update(id="0238a4e3-66f2-455a-831f-5f177215de0f", data={
            ...     "name": "test",
            ...     "serial": "1234",
            ...     "location": "9b1f53c7-89fa-4fb2-a89a-b97364fef50c",
            ... })

            Use bulk update by passing a list of dicts:
            >>> devices = nb.dcim.devices.update([
            ...    {'id': "db8770c4-61e5-4999-8372-e7fa576a4f65", 'name': 'test'},
            ...    {'id': "e9b5f2e0-4f20-41ad-9179-90a4987f743e", 'name': 'test2'},
            ... ])

            Use bulk update by passing a list of Records:
            >>> devices = list(nb.dcim.devices.filter())
            >>> devices
            [Device1, Device2, Device3]
            >>> for d in devices:
            ...     d.name = d.name+'-test'
            ...
            >>> nb.dcim.devices.update(devices)
        """
        if not args and not kwargs:
            raise ValueError("You must provide either a UUID and data dict or a list of objects to update")
        uuid = kwargs.get("id", "")
        data = kwargs.get("data", {})
        if data and not uuid:
            uuid = args[0]
        if len(args) == 2:
            uuid, data = args

        if not any([uuid, data]):
            return self.bulk_update(args[0])

        req = Request(
            key=uuid,
            base=self.url,
            token=self.api.token,
            http_session=self.api.http_session,
            api_version=self.api.api_version,
        )
        if req.patch(data):
            return True
        return False

    def bulk_update(self, objects: List[Dict[str, Any]]):
        """This method is called from the update() method if a bulk
        update is detected.

        Allows for bulk updating of existing objects on an endpoint.
        Objects is a list which contain either JSON/dicts or Record
        derived objects, which contain the updates to apply.
        If JSON/dicts are used, then the id of the object *must* be
        included.

        Args:
            objects (list): A list of dicts or a list of Record.
        """

        if not isinstance(objects, list):
            raise ValueError("objects must be a list[dict()|Record] not " + str(type(objects)))

        bulk_data = []
        for o in objects:
            try:
                if isinstance(o, dict):
                    bulk_data.append(o)
                elif isinstance(o, Record):
                    if not hasattr(o, "id"):
                        raise ValueError("'Record' object has no attribute 'id'")
                    updates = o.updates()
                    if updates:
                        updates["id"] = o.id
                        bulk_data.append(updates)
                else:
                    raise ValueError("Invalid object type: " + str(type(o)))
            except ValueError as exc:
                raise ValueError("Unexpected value in object list") from exc

        req = Request(
            base=self.url,
            token=self.api.token,
            http_session=self.api.http_session,
            api_version=self.api.api_version,
        ).patch(bulk_data)
        return response_loader(req, self.return_obj, self)

    def delete(self, objects):
        """Bulk deletes objects on an endpoint.

        Allows for batch deletion of multiple objects from
        a single endpoint.

        Args:
            objects (list): A list of either IDs or Records to delete.

        Returns:
            (bool): True if bulk DELETE operation was successful.

        Examples:
            Deleting all `devices`:
            >>> pynautobot.dcim.devices.delete(pynautobot.dcim.devices.all())

            Use bulk deletion by passing a list of IDs:
            >>> pynautobot.dcim.devices.delete([
            ...     "db8770c4-61e5-4999-8372-e7fa576a4f65",
            ...     "e9b5f2e0-4f20-41ad-9179-90a4987f743e"
            ... ])

            Use bulk deletion to delete objects e.g. when filtering
            on a `custom_field`:
            >>> pynautobot.dcim.devices.delete([
            ...     d for d in pynautobot.dcim.devices.all()
            ...     if d.custom_fields.get("field", False)
            ... ])
        """

        ids = []
        if not isinstance(objects, list):
            raise ValueError("objects must be a list[str(id)|Record] not " + str(type(objects)))
        for o in objects:
            try:
                if isinstance(o, str):
                    if UUID(o):
                        ids.append(o)
                elif isinstance(o, Record):
                    if not hasattr(o, "id"):
                        raise ValueError("'Record' object has no attribute 'id'")
                    ids.append(o.id)
                else:
                    raise ValueError("Invalid object type: " + str(type(o)))
            except ValueError as exc:
                raise ValueError("Unexpected value in object list") from exc

        req = Request(
            base=self.url,
            token=self.token,
            http_session=self.api.http_session,
            api_version=self.api.api_version,
        )

        return req.delete(data=[{"id": id} for id in ids])

    def choices(self, api_version=None):
        """Returns all choices from the endpoint.

        The returned dict is also saved in the endpoint object (in
        ``_choices`` attribute) so that later calls will return the same data
        without recurring requests to Nautobot. When using ``.choices()`` in
        long-running applications, consider restarting them whenever Nautobot is
        upgraded, to prevent using stale choices data.

        Args:
            api_version (str, optional): Override default or globally-set
                Nautobot REST API version for this single request.

        Returns:
            (dict): Dict containing the available choices.

        Example (from Nautobot 2.8.x):
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
        if req.get("schema", {}).get("properties") is not None:
            # Nautobot 2.3 and below
            post_data = req["schema"]["properties"]
            self._choices = {
                prop: [
                    {"value": x, "display": y} for x, y in zip(post_data[prop]["enum"], post_data[prop]["enumNames"])
                ]
                for prop in post_data
                if "enum" in post_data[prop]
            }
        elif req.get("actions", {}).get("POST") is not None:
            # Nautobot 2.4+
            post_data = req["actions"]["POST"]
            self._choices = {prop: post_data[prop]["choices"] for prop in post_data if "choices" in post_data[prop]}
        else:
            raise ValueError(f"Unexpected format in the OPTIONS response at {self.url}")
        return self._choices

    def count(self, *args, api_version=None, **kwargs):
        """Returns the count of objects in a query.

        Takes named arguments that match the usable filters on a
        given endpoint. If an argument is passed then it's used as a
        freeform search argument if the endpoint supports it. If no
        arguments are passed the count for all objects on an endpoint
        are returned.

        Args:
            *args (str, optional): Freeform search string that's
                accepted on given endpoint.
            **kwargs (str, optional): Any search argument the
                endpoint accepts can be added as a keyword arg.
            api_version (str, optional): Override default or globally-set
                Nautobot REST API version for this single request.

        Returns:
            (int): Integer with count of objects returned by query.

        Examples:
            To return a count of objects matching a named argument filter.
            >>> nb.dcim.devices.count(site='tst1')
            5827

            To return a count of objects on an entire endpoint.
            >>> nb.dcim.devices.count()
            87382
        """

        if args:
            kwargs.update({"q": args[0]})

        if any(i in RESERVED_KWARGS for i in kwargs):
            raise ValueError(f"A reserved {RESERVED_KWARGS} kwarg was passed. Please remove it and try again.")

        api_version = api_version or self.api.api_version

        ret = Request(
            filters=kwargs, base=self.url, token=self.token, http_session=self.api.http_session, api_version=api_version
        )

        return ret.get_count()


class DetailEndpoint:
    """Enables read/write Operations on detail endpoints.

    Endpoints like ``available-ips`` that are detail routes off
    traditional endpoints are handled with this class.
    """

    def __init__(self, parent_obj, name, custom_return=None):
        self.parent_obj = parent_obj
        self.custom_return = custom_return
        self.url = f"{parent_obj.endpoint.url}/{parent_obj.id}/{name}/"

        self.request_kwargs = {
            "base": self.url,
            "token": parent_obj.api.token,
            "http_session": parent_obj.api.http_session,
        }

    def list(self, api_version=None, **kwargs):
        """The view operation for a detail endpoint.

        Returns the response from Nautobot for a detail endpoint.

        Args:
            api_version (str, optional): Override default or globally set Nautobot REST API version for this single request.
            **kwargs (dict): Key/value pairs that get converted into URL parameters when passed to the endpoint.
                E.g. ``.list(method='get_facts')`` would be converted to ``.../?method=get_facts``.

        Returns:
            (Union[Dict, List[Dict]]): A dictionary or list of dictionaries retrieved from Nautobot.
        """

        api_version = api_version or self.parent_obj.api.api_version

        req = Request(api_version=api_version, **self.request_kwargs).get(add_params=kwargs)

        if self.custom_return:
            return response_loader(req, self.custom_return, self.parent_obj.endpoint)
        return req

    def create(self, data=None, api_version=None):
        """The write operation for a detail endpoint.

        Creates objects on a detail endpoint in Nautobot.

        Args:
            data (dict or list, optional): A dictionary containing the
                key/value pairs of the items you're creating on the parent
                object. Defaults to an empty dict, which will create a single
                item with default values.
            api_version (str, optional): Override default or globally set
                Nautobot REST API version for this single request.

        Returns:
            (Union[Dict, List[Dict]]): A dictionary or list of dictionaries representing
                the items created in Nautobot.
        """
        data = data or {}
        api_version = api_version or self.parent_obj.api.api_version

        req = Request(api_version=api_version, **self.request_kwargs).post(data)
        if self.custom_return:
            return response_loader(req, self.custom_return, self.parent_obj.endpoint)
        return req


class RODetailEndpoint(DetailEndpoint):
    """Enables read-only Operations on detail endpoints."""

    def create(self, data=None, api_version=None):
        raise NotImplementedError("Writes are not supported for this endpoint.")


class JobsEndpoint(Endpoint):
    """Extend Endpoint class to support run method only for jobs."""

    def run(self, *args, api_version=None, **kwargs):
        """Runs a job based on the class_path provided to the job.

        Takes a kwarg of `class_path` or `job_id` to specify the job that should be run.

        Args:
            *args (str, optional): Freeform search string that's
                accepted on given endpoint.
            **kwargs (str, optional): Any search argument the
                endpoint accepts can be added as a keyword arg.
            api_version (str, optional): Override default or globally-set
                Nautobot REST API version for this single request.

        Returns:
            obj (str): Job details: job_result object uuid found at `obj.result.id`.

        Examples:
            To run a job for verifying hostnames:
            >>> nb.extras.jobs.run(
                    class_path="local/data_quality/VerifyHostnames",
                    data={"hostname_regex": ".*"},
                    commit=True,
                )
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

    def run_and_wait(self, *args, api_version=None, interval=5, max_rechecks=50, **kwargs):
        """Runs a job and waits for the response.
        Args:
            *args (str, optional): Freeform search string that's
                accepted on given endpoint.
            **kwargs (str, optional): Any search argument the
                endpoint accepts can be added as a keyword arg.
            api_version (str, optional): Override default or globally-set
                Nautobot REST API version for this single request.
            interval (int, optional): Time in seconds to wait between
                checking job results.
            max_rechecks (int, optional): Number of times to check job result
                before exiting the method.
        Returns:
            obj (str): Job details: job_result object uuid found at `obj.result.id`.
        Examples:
            To run a job for verifying hostnames:
            >>> response = nb.extras.jobs.run_and_wait(
                    class_path="local/data_quality/VerifyHostnames",
                    data={"hostname_regex": ".*"},
                    commit=True,
                    interval=5,
                    max_rechecks=10,
                )
            >>> print(f"Job completed, Job Result ID: {response.job_result.id}")
            Job completed, Job Result ID: 123
        """
        if max_rechecks <= 0:
            raise ValueError("Attribute `max_rechecks` must be a postive integer to prevent recursive loops.")

        job_obj = self.run(*args, api_version=api_version, **kwargs)
        job_result = job_obj.job_result

        # Job statuses which indicate a job not yet started or in progress.
        # If the job status is not in this list, it will consider the job complete and return the job result object.
        active_job_statuses = (
            "RECEIVED",
            "PENDING",
            "STARTED",
            "RETRY",
        )

        interval_counter = 0

        while interval_counter <= max_rechecks:
            # Sleep for interval and increment counter
            sleep(interval)
            interval_counter += 1

            job_result.full_details()
            if job_result.status not in active_job_statuses:
                return job_obj

        raise ValueError("Did not receieve completed job result for job.")


class GraphqlEndpoint(Endpoint):
    """Extend Endpoint class to support run method for graphql queries."""

    def run(self, query_id, *args, **kwargs):
        """Runs a saved graphql query based on the query_id provided.

        Takes a kwarg of `query_id` to specify the query that should be run.

        Args:
            *args (str, optional): Used as payload for POST method
                to the API if provided.
            **kwargs (str, optional): Any additional argument the
                endpoint accepts can be added as a keyword arg.
            query_id (str, required): The UUID of the query object
                that is being ran.

        Returns:
            (Response): An API response from the execution of the saved graphql query.

        Examples:
            To run a query no variables:
            >>> query = nb.extras.graphql_queries.get("Example")
            >>> query.run()

            To run a query with `variables` as kwarg:
            >>> query = nb.extras.graphql_queries.get("Example")
            >>> query.run(
                    variables={"foo": "bar"})
                )

            To run a query with JSON payload as an arg:
            >>> query = nb.extras.graphql_queries.get("Example")
            >>> query.run(
                    {"variables":{"foo":"bar"}}
                )
        """
        query_run_url = f"{self.url}/{query_id}/run/"
        return Request(
            base=query_run_url,
            token=self.token,
            http_session=self.api.http_session,
        ).post(args[0] if args else kwargs)
