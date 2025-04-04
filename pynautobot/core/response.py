"""Provides classes and functions to handle responses from the Nautobot API."""

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

import copy
from collections import OrderedDict
from urllib.parse import urlparse

import pynautobot.core.app
import pynautobot.core.endpoint
from pynautobot.core.query import Request
from pynautobot.core.util import Hashabledict


# List of fields that are lists but should be treated as sets.
LIST_AS_SET = ("tags", "tagged_vlans", "nat_outside")


def get_return(lookup, return_fields=None):
    """Returns simple representations for items passed to lookup.

    Args:
        lookup (dict|Record): The object or collection to retrieve representations for.
        return_fields (list, optional): A list of fields to reference when
            calling values on lookup.

    Note:
        Used to return a "simple" representation of objects and collections
        sent to it via lookup. Otherwise, we look to see if
        lookup is a "choices" field (dict with only 'id' and 'value')
        or a nested_return. Finally, we check if it's a Record, if
        so simply return a string. Order is important due to nested_return
        being self-referential.
    """

    for i in return_fields or ["id", "value", "nested_return"]:
        if isinstance(lookup, dict) and lookup.get(i):
            return lookup[i]
        if hasattr(lookup, i):
            # check if this is a "choices" field record
            # from a Nautobot 2.7 server.
            if sorted(dict(lookup)) == sorted(["id", "value", "label"]):
                return getattr(lookup, "value")
            return getattr(lookup, i)

    if isinstance(lookup, Record):
        return str(lookup)
    return lookup


# pylint: disable=too-few-public-methods
class JsonField:
    """Explicit field type for values that are not to be converted to a Record object."""

    _json_field = True


class Record:
    """Create Python objects from Nautobot API responses.

    Creates an object from a Nautobot response passed as `values`.
    Nested dicts that represent other endpoints are also turned
    into Record objects. All fields are then assigned to the
    object's attributes. If a missing attribute is requested
    (e.g., requesting a field that's only present on a full response on
    a Record made from a nested response), the pynautobot will make a
    request for the full object and return the requested value.

    Examples:
        Default representation of the object usually contains object's
        class, object's name, and its location in memory

        >>> x = nb.dcim.devices.get(1)
        >>> x
        <pynautobot.models.dcim.Devices ('test1-switch1') at 0x1953d821250>
        >>>

        Querying a string field.

        >>> x = nb.dcim.devices.get(1)
        >>> x.serial
        'ABC123'
        >>>

        Querying a field on a nested object.

        >>> x = nb.dcim.devices.get(1)
        >>> x.device_type.model
        'QFX5100-24Q'
        >>>

        Casting the object as a dictionary.

        >>> from pprint import pprint
        >>> pprint(dict(x))
        {'asset_tag': None,
         'cluster': None,
         'comments': '',
         'config_context': {},
         'created': '2018-04-01',
         'custom_fields': {},
         'device_role': {...},
         'device_type': {...},
         'display_name': 'test1-switch1',
         'face': {'label': 'Rear', 'value': 1},
         'id': 1,
         'name': 'test1-switch1',
         'parent_device': None,
         'platform': {...},
         'position': 1,
         'primary_ip': {...},
         'primary_ip4': {...},
         'primary_ip6': None,
         'rack': {...},
         'serial': 'ABC123',
         'site': {...},
         'status': {...},
         'tags': [],
         'tenant': None,
         'vc_position': None,
         'vc_priority': None,
         'virtual_chassis': None}

        Iterating over a Record object.

        >>> for i in x:
        ...     print(i)
        ...
        ('id', 1)
        ('name', 'test1-switch1')
        ('display_name', 'test1-switch1')
        >>>
    """

    url = None

    def __init__(self, values, api, endpoint):
        self.has_details = False
        self._full_cache = []
        self._init_cache = []
        self.api = api
        self.default_ret = Record
        self.endpoint = self._endpoint_from_url(values["url"]) if "url" in values else endpoint

        if values:
            self._parse_values(values)

    def __getattr__(self, k):
        """Default behavior for missing attributes.

        We'll call `full_details()` if we're asked for an attribute
        we don't have.

        Args:
            k (str): The name of the attribute.

        Returns:
            (Any): The value of the requested attribute.

        Raises:
            AttributeError: If the attribute is not found.

        Note:
            In order to prevent non-explicit behavior, `k='keys'` is
            excluded because casting to dict() calls this attribute.
        """
        if self.url:
            if self.has_details is False and k != "keys":
                if self.full_details():
                    ret = getattr(self, k, None)
                    if ret or hasattr(self, k):
                        return ret

        raise AttributeError(f'object has no attribute "{k}"')

    def __iter__(self):
        for i in dict(self._init_cache):
            cur_attr = getattr(self, i)
            if isinstance(cur_attr, Record):
                yield i, dict(cur_attr)
            elif isinstance(cur_attr, list) and all(isinstance(i, Record) for i in cur_attr):
                yield i, [dict(x) for x in cur_attr]
            else:
                yield i, cur_attr

    def __getitem__(self, k):
        return dict(self)[k]

    def __str__(self):
        return str(getattr(self, "display", None) or getattr(self, "name", None) or getattr(self, "label", None) or "")

    def __repr__(self):
        return f"<{self.__class__.__module__}.{self.__class__.__name__} ('{self}') at {hex(id(self))}>"

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__.update(d)

    def __key__(self):
        if hasattr(self, "id"):
            return (self.endpoint.name, self.id)
        return self.endpoint.name

    def __hash__(self):
        return hash(self.__key__())

    def __eq__(self, other):
        if isinstance(other, Record):
            return self.__key__() == other.__key__()
        return NotImplemented

    def _add_cache(self, item):
        key, value = item
        if key == "local_context_data":
            self._init_cache.append((key, copy.deepcopy(value)))
        else:
            self._init_cache.append((key, get_return(value)))

    def _parse_values(self, values):
        """Parses the values provided during initialization.

        Args:
            values (dict): A dictionary containing the values to be set as object attributes.

        Returns:
            None

        Note:
            This method sets object attributes using the values within the provided dictionary.
        """

        def list_parser(list_item):
            if isinstance(list_item, dict) and list_item.get("id"):
                return self.default_ret(list_item, self.api, self.endpoint)
            return list_item

        for k, v in values.items():
            if isinstance(v, dict):
                lookup = getattr(self.__class__, k, None)
                if k in ["custom_fields", "local_context_data"] or hasattr(lookup, "_json_field"):
                    self._add_cache((k, v.copy()))
                    setattr(self, k, v)
                    continue
                if lookup:
                    v = lookup(v, self.api, self.endpoint)
                else:
                    v = self.default_ret(v, self.api, self.endpoint)
                self._add_cache((k, v))

            elif isinstance(v, list):
                v = [list_parser(i) for i in v]
                to_cache = list(v)
                self._add_cache((k, to_cache))

            else:
                self._add_cache((k, v))
            setattr(self, k, v)

    def _endpoint_from_url(self, url):
        url_path = urlparse(url).path
        base_url_path_parts = urlparse(self.api.base_url).path.split("/")
        if len(base_url_path_parts) > 2:
            # There are some extra directories in the path, remove them from url
            extra_path = "/".join(base_url_path_parts[:-1])
            url_path = url_path[len(extra_path) :]
        split_url_path = url_path.split("/")
        if split_url_path[2] == "plugins":
            # Keep plugins in app path
            app = "/".join(split_url_path[2:4])
            name = "/".join(split_url_path[4:-2])
        else:
            app, name = split_url_path[2:4]
        return getattr(pynautobot.core.app.App(self.api, app), name)

    def full_details(self):
        """Queries the hyperlinked endpoint if 'url' is defined.

        This method will populate the attributes from the detail
        endpoint when it's called. Sets the class-level `has_details`
        attribute when it's called to prevent being called more
        than once.

        Returns: (bool)
        """
        if self.url:
            req = Request(
                base=self.url,
                token=self.api.token,
                http_session=self.api.http_session,
                api_version=self.api.api_version,
            )
            self._parse_values(req.get())
            self.has_details = True
            return True
        return False

    # pylint: disable=possibly-used-before-assignment
    def serialize(self, nested=False, init=False):
        """Serializes the object.

        Pulls all the attributes in an object and creates a dictionary
        that can be turned into the JSON format expected by Nautobot.

        Args:
            nested (bool): Whether to include nested objects in the serialization. Default is False.
            init (bool): Whether to include initialization attributes in the serialization. Default is False.

        Returns:
            (dict): A dictionary representation of the serialized object.

        Note:
            Using this method to get a dictionary representation of the record
            is discouraged. It's probably better to cast to dict() instead.
            See the Record docstring for an example.
        """
        if nested:
            return get_return(self)

        if init:
            init_vals = dict(self._init_cache)

        ret = {}
        for i in dict(self):
            current_val = getattr(self, i) if not init else init_vals.get(i)
            if i in ["custom_fields", "constraints"]:  # just pass constraints as it is (a JSON string)
                ret[i] = current_val

            else:
                if isinstance(current_val, Record):
                    current_val = getattr(current_val, "serialize")(nested=True)

                if isinstance(current_val, list):
                    current_val = [v.id if isinstance(v, Record) else v for v in current_val]
                    if i in LIST_AS_SET and (
                        all(isinstance(v, str) for v in current_val) or all(isinstance(v, int) for v in current_val)
                    ):
                        current_val = list(OrderedDict.fromkeys(current_val))
                ret[i] = current_val
        return ret

    def _diff(self):
        def fmt_dict(k, v):
            if isinstance(v, dict):
                return k, Hashabledict(v)
            if isinstance(v, list):
                return k, ",".join(map(str, v))
            return k, v

        current = Hashabledict({fmt_dict(k, v) for k, v in self.serialize().items()})
        init = Hashabledict({fmt_dict(k, v) for k, v in self.serialize(init=True).items()})
        return {i[0] for i in set(current.items()) ^ set(init.items())}

    def updates(self):
        """Compiles changes for an existing object into a dictionary.

        Takes a diff between the object's current state and its state at initialization
        and returns them as a dictionary. Returns an empty dictionary if no changes
        have been made.

        Returns:
            (dict): A dictionary containing the changes made to the object.

        Examples:
            >>> x = nb.dcim.devices.get(name='test1234')
            >>> x.serial
            ''
            >>> x.serial = '1234'
            >>> x.updates()
            {'serial': '1234'}
        """
        if self.id:
            diff = self._diff()
            if diff:
                serialized = self.serialize()
                return {i: serialized[i] for i in diff}
        return {}

    def save(self):
        """Saves changes to an existing object.

        Takes a diff between the object's current state and its state at initialization
        and sends them as a dictionary to Request.patch().

        Returns:
            (bool): True if the PATCH request was successful.

        Examples:
            >>> x = nb.dcim.devices.get(name='test1-a3-tor1b')
            >>> x.serial
            ''
            >>> x.serial = '1234'
            >>> x.save()
            True
        """
        if self.id:
            diff = self._diff()
            if diff:
                serialized = self.serialize()
                req = Request(
                    key=self.id,
                    base=self.endpoint.url,
                    token=self.api.token,
                    http_session=self.api.http_session,
                    api_version=self.api.api_version,
                )
                if req.patch({i: serialized[i] for i in diff}):
                    return True

        return False

    def update(self, data):
        """Update an object with a dictionary.

        Accepts a dictionary and uses it to update the record and call save().
        For nested and choice fields you'd pass an int the same as if you were
        modifying the attribute and calling save().

        Args:
            data (dict): Dictionary containing the key-value pairs to update
                the record object with.

        Returns:
            (bool): True if the PATCH request was successful.

        Examples:
            >>> x = nb.dcim.devices.get(1)
            >>> x.update({
            ...   "name": "test-switch2",
            ...   "serial": "ABC321",
            ... })
            True
        """

        for k, v in data.items():
            setattr(self, k, v)
        return self.save()

    def delete(self):
        """Deletes an existing object.

        Returns:
            (bool): True if the DELETE operation was successful.

        Examples:
            >>> x = nb.dcim.devices.get(name='test1-a3-tor1b')
            >>> x.delete()
            True
        """
        req = Request(
            key=self.id,
            base=self.endpoint.url,
            token=self.api.token,
            http_session=self.api.http_session,
            api_version=self.api.api_version,
        )
        return bool(req.delete())

    @property
    def notes(self):
        """Represents the ``notes`` detail endpoint.

        Returns a list of DetailEndpoint objects that are
        related to the passed in object

        :returns: :py:class:`.DetailEndpoint`

        :Examples:

        Notes associated to a device object:

        >>> device = nb.dcim.devices.get(name="test")
        >>> device.notes.list()
        [<pynautobot.core.response.Record ('test - 2024-07-16T11:59:00.169296+00:00')...]

        Notes associated to a controller object:

        >>> controller = nb.dcim.controllers.get(name="test")
        >>> controller.notes.list()
        [<pynautobot.core.response.Record ('test - 2024-07-16T11:59:00.169296+00:00')...]

        Create new note on device object:

        >>> device = nb.dcim.devices.get(name="test")
        >>> device.notes.create({"note": "foo bar"})
        [<pynautobot.core.response.Record ('test - 2024-07-16T18:45:07.653263+00:00')...]

        """
        return pynautobot.core.endpoint.DetailEndpoint(self, "notes", custom_return=Record)
