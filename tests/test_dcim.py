"""DCIM tests."""

import unittest
from unittest.mock import patch

import pynautobot

from . import api, Generic, HEADERS, POST_HEADERS
from .util import Response


class DeviceTestCase(Generic.Tests):
    """Device test."""

    app = "dcim"
    name = "devices"

    @patch("requests.sessions.Session.get", return_value=Response(fixture="dcim/device.json"))
    def test_get(self, mock):  # pylint: disable=arguments-differ
        ret = self.endpoint.get(self.uuid)
        self.assertIsInstance(ret, self.ret)
        self.assertIsInstance(ret.primary_ip, pynautobot.core.response.Record)
        self.assertIsInstance(ret.primary_ip4, pynautobot.core.response.Record)
        self.assertIsInstance(ret.config_context, dict)
        self.assertIsInstance(ret.custom_fields, dict)
        self.assertIsInstance(ret.local_context_data, dict)
        mock.assert_called_with(self.detail_uri, params={}, json=None, headers=HEADERS)

    @patch("requests.sessions.Session.get", return_value=Response(fixture="dcim/device.json"))
    def test_get_by_id(self, mock):
        params = {"id": self.uuid}
        ret = self.endpoint.filter(**params)
        self.assertIsInstance(ret, self.ret)
        self.assertIsInstance(ret.primary_ip, pynautobot.core.response.Record)
        self.assertIsInstance(ret.primary_ip4, pynautobot.core.response.Record)
        self.assertIsInstance(ret.config_context, dict)
        self.assertIsInstance(ret.custom_fields, dict)
        self.assertIsInstance(ret.local_context_data, dict)
        mock.assert_called_with(self.bulk_uri, params=params, json=None, headers=HEADERS)

    @patch("requests.sessions.Session.get", return_value=Response(fixture="dcim/devices.json"))
    def test_multi_filter(self, mock):
        params = {"role": ["test", "test1"], "site": "TEST#1"}
        ret = self.endpoint.filter(**params)
        self.assertIsInstance(ret, list)
        self.assertIsInstance(ret[0], self.ret)
        mock.assert_called_with(self.bulk_uri, params=params, json=None, headers=HEADERS)

    @patch("requests.sessions.Session.get", return_value=Response(fixture="dcim/device.json"))
    def test_modify(self, *_):
        ret = self.endpoint.get(self.uuid)
        ret.serial = "123123123123"
        ret_serialized = ret.serialize()
        self.assertTrue(ret_serialized)
        self.assertEqual(ret._diff(), {"serial"})  # pylint: disable=protected-access
        self.assertEqual(ret_serialized["serial"], "123123123123")

    @patch("requests.sessions.Session.post", return_value=Response(fixture="dcim/device.json"))
    def test_create(self, mock):
        data = {
            "name": "test-device",
            "site": 1,
            "device_type": 1,
            "device_role": 1,
        }
        ret = self.endpoint.create(**data)
        self.assertTrue(ret)
        mock.assert_called_with(
            self.bulk_uri,
            headers=POST_HEADERS,
            params={},
            json=data,
        )

    @patch("requests.sessions.Session.post", return_value=Response(fixture="dcim/device_bulk_create.json"))
    def test_create_device_bulk(self, mock):
        data = [
            {"name": "test-device", "site": 1, "device_type": 1, "device_role": 1},
            {"name": "test-device1", "site": 1, "device_type": 1, "device_role": 1},
        ]
        ret = self.endpoint.create(data)
        self.assertTrue(ret)
        self.assertEqual(len(ret), 2)
        mock.assert_called_with(
            self.bulk_uri,
            headers=POST_HEADERS,
            params={},
            json=data,
        )

    @patch(
        "requests.sessions.Session.get",
        side_effect=[Response(fixture="dcim/device.json"), Response(fixture="dcim/rack.json")],
    )
    def test_get_recurse(self, *_):
        """Test that automatic recursion works, and that nested items
        are converted to Response() objects.
        """
        ret = self.endpoint.get(self.uuid)
        self.assertTrue(ret)
        self.assertIsInstance(ret, self.ret)
        self.assertIsInstance(ret.rack.role, self.ret)

    @patch(
        "requests.sessions.Session.get",
        side_effect=[Response(fixture="dcim/device.json"), Response(fixture="dcim/napalm.json")],
    )
    def test_get_napalm(self, mock):
        test = self.endpoint.get(self.uuid)
        ret = test.napalm.list(method="get_facts")
        mock.assert_called_with(f"{self.detail_uri}napalm/", params={"method": "get_facts"}, json=None, headers=HEADERS)
        self.assertTrue(ret)
        self.assertTrue(ret["get_facts"])


class SiteTestCase(Generic.Tests):
    """Site test."""

    app = "dcim"
    name = "sites"

    @patch("requests.sessions.Session.get", return_value=Response(fixture="dcim/site.json"))
    def test_modify_custom(self, *_):
        """Test modifying a custom field."""
        ret = self.endpoint.get(self.uuid)
        ret.custom_fields["test_custom"] = "Testing"
        self.assertEqual(ret._diff(), {"custom_fields"})  # pylint: disable=protected-access
        self.assertTrue(ret.serialize())
        self.assertEqual(ret.custom_fields["test_custom"], "Testing")

    @patch("requests.sessions.Session.get", return_value=Response(fixture="dcim/site.json"))
    def test_custom_field_json(self, _):
        """Tests serializer with custom selection fields."""
        ret = self.endpoint.get(self.uuid)
        ret.custom_fields["test_custom"] = "Testing"
        test = ret.serialize()
        self.assertEqual(test["custom_fields"]["test_json"]["second_key"], "second")

    @patch("requests.sessions.Session.post", return_value=Response(fixture="dcim/site.json"))
    def test_create(self, mock):
        data = {"name": "TEST1", "custom_fields": {"test_custom": "Testing"}}
        ret = self.endpoint.create(**data)
        self.assertTrue(ret)
        mock.assert_called_with(self.bulk_uri, headers=POST_HEADERS, params={}, json=data)


class InterfaceTestCase(Generic.Tests):
    """Interface test."""

    app = "dcim"
    name = "interfaces"

    @patch("requests.sessions.Session.get", return_value=Response(fixture="dcim/interface.json"))
    def test_modify(self, *_):
        ret = self.endpoint.get(self.uuid)
        ret.description = "Testing"
        ret_serialized = ret.serialize()
        self.assertTrue(ret)
        self.assertEqual(ret_serialized["description"], "Testing")
        self.assertEqual(ret_serialized["form_factor"], 1400)

    @patch(
        "requests.sessions.Session.get",
        side_effect=[
            Response(fixture=f"dcim/{name}_1.json"),
            Response(fixture=f"dcim/{name}_2.json"),
        ],
    )
    def test_get_all(self, mock):  # pylint: disable=arguments-differ
        ret = self.endpoint.all(limit=50)
        next_url = "http://localhost:8000/api/dcim/interfaces/?limit=50&offset=50"
        self.assertTrue(ret)
        self.assertIsInstance(ret, list)
        self.assertIsInstance(ret[0], self.ret)
        self.assertEqual(len(ret), 71)
        mock.assert_called_with(next_url, params={}, json=None, headers=HEADERS)

    @patch(
        "requests.sessions.Session.get",
        side_effect=[
            Response(fixture=f"dcim/{name}_1.json"),
            Response(fixture=f"dcim/{name}_2.json"),
        ],
    )
    def test_get_chunk(self, mock):
        ret = self.endpoint.all(limit=50, offset=0)
        self.assertTrue(ret)
        self.assertIsInstance(ret, list)
        self.assertIsInstance(ret[0], self.ret)
        self.assertEqual(len(ret), 50)
        mock.assert_called_with(self.bulk_uri, params={"limit": 50, "offset": 0}, json=None, headers=HEADERS)

    @patch(
        "requests.sessions.Session.get",
        side_effect=[Response(fixture="dcim/interface.json"), Response(fixture="dcim/interface_trace.json")],
    )
    def test_trace(self, mock): # pylint: disable=unused-argument
        ret = self.endpoint.get(self.uuid)
        trace = ret.trace()
        self.assertEqual(len(trace), 3)
        for hop in trace:
            self.assertEqual(len(hop), 3)


class RackTestCase(Generic.Tests):
    """Rack test."""

    app = "dcim"
    name = "racks"

    @patch(
        "requests.sessions.Session.get",
        side_effect=[Response(fixture="dcim/rack.json"), Response(fixture="dcim/rack_u.json")],
    )
    def test_get_units(self, mock):
        test = self.endpoint.get(self.uuid)
        ret = test.units.list()
        mock.assert_called_with(f"{self.detail_uri}units/", params={}, json=None, headers=HEADERS)
        self.assertTrue(ret)
        self.assertIsInstance(ret[0].device, pynautobot.models.dcim.Devices)

    @patch(
        "requests.sessions.Session.get",
        side_effect=[Response(fixture="dcim/rack.json"), Response(fixture="dcim/rack_u.json")],
    )
    def test_get_elevation(self, mock):
        test = self.endpoint.get(self.uuid)
        ret = test.elevation.list()
        mock.assert_called_with(f"{self.detail_uri}elevation/", params={}, json=None, headers=HEADERS)
        self.assertTrue(ret)
        self.assertIsInstance(ret[0].device, pynautobot.models.dcim.Devices)


class RackRoleTestCase(Generic.Tests):
    """RackRole test."""

    app = "dcim"
    name = "rack_roles"


class RegionTestCase(Generic.Tests):
    """Region test."""

    app = "dcim"
    name = "regions"


class RackGroupsTestCase(Generic.Tests):
    """RackGroups test."""

    app = "dcim"
    name = "rack_groups"


class RackReservationsTestCase(Generic.Tests):
    "RackReservations test."
    app = "dcim"
    name = "rack_reservations"


class ManufacturersTestCase(Generic.Tests):
    """Manufacturers test."""

    app = "dcim"
    name = "manufacturers"


class DeviceTypeTestCase(Generic.Tests):
    """DeviceType test."""

    app = "dcim"
    name = "device_types"


class ConsolePortTemplateTestCase(Generic.Tests):
    """ConsolePortTemplate test."""

    app = "dcim"
    name = "console_port_templates"


class ConsoleServerPortTemplateTestCase(Generic.Tests):
    """ConsoleServerPortTemplate test."""

    app = "dcim"
    name = "console_server_port_templates"


class PowerPortTemplateTestCase(Generic.Tests):
    """PowerPortTemplate test."""

    app = "dcim"
    name = "power_port_templates"


class PowerOutletTemplateTestCase(Generic.Tests):
    """PowerOutletTemplate test."""

    app = "dcim"
    name = "power_outlet_templates"


class InterfaceTemplateTestCase(Generic.Tests):
    """InterfaceTemplate test."""

    app = "dcim"
    name = "interface_templates"


class DeviceBayTemplateTestCase(Generic.Tests):
    """DeviceBayTemplate test."""

    app = "dcim"
    name = "device_bay_templates"


class DeviceRolesTestCase(Generic.Tests):
    """DeviceRoles test."""

    app = "dcim"
    name = "device_roles"


class PlatformsTestCase(Generic.Tests):
    """Platforms test."""

    app = "dcim"
    name = "platforms"


class ConsolePortsTestCase(Generic.Tests):
    """ConsolePorts test."""

    app = "dcim"
    name = "console_ports"


class ConsoleServerPortsTestCase(Generic.Tests):
    """ConsoleServerPorts test."""

    app = "dcim"
    name = "console_server_ports"


class PowerPortsTestCase(Generic.Tests):
    """PowerPorts test."""

    app = "dcim"
    name = "power_ports"


class PowerOutletsTestCase(Generic.Tests):
    """PowerOutlets test."""

    app = "dcim"
    name = "power_outlets"


class DeviceBaysTestCase(Generic.Tests):
    """DeviceBays test."""

    app = "dcim"
    name = "device_bays"


# class InventoryItemsTestCase(Generic.Tests):
# """InventoryItems test."""
#     app = "dcim"
#     name = "inventory_items"


class InterfaceConnectionsTestCase(Generic.Tests):
    """InterfaceConnections test."""

    app = "dcim"
    name = "interface_connections"


# class ConnectedDevicesTestCase(Generic.Tests):
# """ConnectedDevices test."""
#     app = "dcim"
#     name = "connected_device"


class VirtualChassisTestCase(Generic.Tests):
    """VirtualChassis test."""

    app = "dcim"
    name = "virtual_chassis_devices"


class Choices(unittest.TestCase):
    """Choices test."""

    def test_get(self):
        with patch(
            "requests.sessions.Session.get",
            return_value=Response(fixture="dcim/choices.json"),
        ) as mock:
            ret = api.dcim.choices()
            self.assertTrue(ret)
            mock.assert_called_with(
                "http://localhost:8000/api/dcim/_choices/",
                params={},
                json=None,
                headers=HEADERS,
            )


class CablesTestCase(Generic.Tests):
    """Cables test."""

    app = "dcim"
    name = "cables"

    def test_get_cable_between_device_and_circuit(self):
        response_obj = Response(
            content={
                "id": self.uuid,
                "termination_a_type": "circuits.circuittermination",
                "termination_a_id": 1,
                "termination_a": {
                    "id": 1,
                    "url": "http://localhost:8000/api/circuits/circuit-terminations/1/",
                    "circuit": {
                        "id": 346,
                        "url": "http://localhost:8000/api/circuits/circuits/1/",
                    },
                    "term_side": "A",
                    "display": "TEST123321",
                },
                "termination_b_type": "dcim.interface",
                "termination_b_id": 2,
                "termination_b": {
                    "id": 2,
                    "url": "http://localhost:8000/api/dcim/interfaces/2/",
                    "device": {
                        "id": 2,
                        "url": "http://localhost:8000/api/dcim/devices/2/",
                        "name": "tst1-test2",
                        "display_name": "tst1-test2",
                    },
                    "name": "xe-0/0/0",
                    "display": "xe-0/0/0",
                    "cable": 1,
                },
                "type": None,
                "status": {"value": True, "label": "Connected"},
                "label": "",
                "color": "",
                "length": None,
                "length_unit": None,
            }
        )
        with patch(
            "requests.sessions.Session.get",
            return_value=response_obj,
        ) as mock:
            ret = self.endpoint.get(self.uuid)
            self.assertTrue(ret)
            self.assertIsInstance(ret, self.ret)
            self.assertIsInstance(str(ret), str)
            self.assertIsInstance(dict(ret), dict)
            mock.assert_called_with(self.detail_uri, headers=HEADERS, params={}, json=None)
