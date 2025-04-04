"""Defines various classes representing different components in DCIM."""

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

from urllib.parse import urlparse

from pynautobot.core.query import Request
from pynautobot.core.response import Record, JsonField
from pynautobot.core.endpoint import RODetailEndpoint
from pynautobot.models.circuits import Circuits


class TraceableRecord(Record):
    """Traceable record in the DCIM (Data Center Infrastructure Management) module."""

    def _get_app_endpoint(self, hop_item_data):
        if "url" not in hop_item_data:
            return ""
        path_elements = urlparse(hop_item_data["url"][len(self.api.base_url) :]).path.split("/")[1:3]
        return "/".join(path_elements)

    def trace(self):
        """Trace the path of the record."""
        req = Request(
            key=str(self.id) + "/trace",
            base=self.endpoint.url,
            token=self.api.token,
            http_session=self.api.http_session,
        )
        uri_to_obj_class_map = {
            "dcim/cables": Cables,
            "dcim/front-ports": FrontPorts,
            "dcim/interfaces": Interfaces,
            "dcim/rear-ports": RearPorts,
        }
        ret = []
        for termination_a_data, cable_data, termination_b_data in req.get():
            this_hop_ret = []
            for hop_item_data in (termination_a_data, cable_data, termination_b_data):
                # if not fully terminated then some items will be None
                if not hop_item_data:
                    this_hop_ret.append(hop_item_data)
                    continue

                app_endpoint = self._get_app_endpoint(hop_item_data)

                return_obj_class = uri_to_obj_class_map.get(
                    app_endpoint,
                    Record,
                )

                this_hop_ret.append(return_obj_class(hop_item_data, self.endpoint.api, self.endpoint))

            ret.append(this_hop_ret)

        return ret


class DeviceTypes(Record):
    """DeviceTypes Object"""

    def __str__(self):
        return self.model


class Devices(Record):
    """Devices Object

    Represents a device response from nautobot.

    Attributes:
        primary_ip, ip4, ip6 (list): Tells __init__ in Record() to
            take the `primary_ip` field's value from the API
            response and return an initialized list of IpAddress
            objects
        device_type (obj): Tells __init__ in Record() to take the
            `device_type` field's value from the API response and
            return an initialized DeviceType object
    """

    has_details = True
    device_type = DeviceTypes
    local_context_data = JsonField
    config_context = JsonField

    @property
    def napalm(self):
        """Represents the ``napalm`` detail endpoint.

        Returns a DetailEndpoint object that is the interface for
        viewing response from the napalm endpoint.

        :returns: :py:class:`.DetailEndpoint`

        :Examples:

        >>> device = nb.ipam.devices.get(123)
        >>> device.napalm.list(method='get_facts')
        {"get_facts": {"interface_list": ["ge-0/0/0"]}}

        """
        return RODetailEndpoint(self, "napalm")


class InterfaceConnections(Record):
    """InterfaceConnections Object"""

    def __str__(self):
        return self.interface_a.name


class InterfaceConnection(Record):
    """InterfaceConnection Object"""

    def __str__(self):
        return self.interface.name


class ConnectedEndpoint(Record):
    """ConnectedEndpoint Object"""

    device = Devices


class Interfaces(TraceableRecord):
    """Interfaces Object"""

    interface_connection = InterfaceConnection
    connected_endpoint = ConnectedEndpoint


class PowerOutlets(TraceableRecord):
    """PowerOutlets Object"""

    device = Devices


class PowerPorts(TraceableRecord):
    """PowerPorts Object"""

    device = Devices


class ConsolePorts(TraceableRecord):
    """ConsolePorts Object"""

    device = Devices


class ConsoleServerPorts(TraceableRecord):
    """ConsoleServerPorts Object"""

    device = Devices


class RackReservations(Record):
    """RackReservations Object"""

    def __str__(self):
        return self.description


class VirtualChassis(Record):
    """VirtualChassis Object"""

    def __str__(self):
        if self.master is not None:
            return self.master.display
        return self.display


class RUs(Record):
    """RUs Object"""

    device = Devices


class FrontPorts(Record):
    """FrontPorts Object"""

    device = Devices


class RearPorts(Record):
    """RearPorts Object"""

    device = Devices


class Racks(Record):
    """Racks Object"""

    @property
    def units(self):
        """Represents the ``units`` detail endpoint.

        Returns a DetailEndpoint object that is the interface for
        viewing response from the units endpoint.

        :returns: :py:class:`.DetailEndpoint`

        :Examples:

        >>> rack = nb.dcim.racks.get(123)
        >>> rack.units.list()
        {"get_facts": {"interface_list": ["ge-0/0/0"]}}

        """
        return RODetailEndpoint(self, "units", custom_return=RUs)

    @property
    def elevation(self):
        """Represents the ``elevation`` detail endpoint.

        Returns a DetailEndpoint object that is the interface for
        viewing response from the elevation endpoint updated in
        Nautobot version 2.8.

        :returns: :py:class:`.DetailEndpoint`

        :Examples:

        >>> rack = nb.dcim.racks.get(123)
        >>> rack.elevation.list()
        {"get_facts": {"interface_list": ["ge-0/0/0"]}}

        """
        return RODetailEndpoint(self, "elevation", custom_return=RUs)


class Termination(Record):
    """Termination Object"""

    def __str__(self):
        return self.display

    device = Devices
    circuit = Circuits


class Cables(Record):
    """Cables Object"""

    def __str__(self):
        if all(isinstance(i, Termination) for i in (self.termination_a, self.termination_b)):
            return f"{self.termination_a} <> {self.termination_b}"
        return f"Cable #{self.id}"

    termination_a = Termination
    termination_b = Termination


class Platforms(Record):
    """
    Platform object
    """

    napalm_args = JsonField
