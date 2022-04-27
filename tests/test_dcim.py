import unittest
import six

import pynautobot
from .util import Response

if six.PY3:
    from unittest.mock import patch
else:
    from mock import patch


api = pynautobot.api("http://localhost:8000", token="abc123",)

nb = api.dcim

HEADERS = {
    "accept": "application/json;",
    "authorization": "Token abc123",
}
POST_HEADERS = {
    "Content-Type": "application/json;",
    "authorization": "Token abc123",
}


class Generic(object):
    class Tests(unittest.TestCase):
        name = ""
        ret = pynautobot.core.response.Record
        app = "dcim"
        uuid = "5b39ba88-e5ab-4be2-89f5-5a016473b53c"

        @property
        def bulk_uri(self):
            return f"http://localhost:8000/api/{self.app}/{self.name.replace('_', '-')}/"

        @property
        def detail_uri(self):
            return f"http://localhost:8000/api/{self.app}/{self.name.replace('_', '-')}/{self.uuid}/"

        def test_get_all(self):
            with patch(
                "requests.sessions.Session.get",
                return_value=Response(fixture="{}/{}.json".format(self.app, self.name)),
            ) as mock:
                ret = getattr(nb, self.name).all()
                self.assertTrue(ret)
                self.assertTrue(isinstance(ret, list))
                self.assertTrue(isinstance(ret[0], self.ret))
                mock.assert_called_with(
                    self.bulk_uri, params={}, json=None, headers=HEADERS,
                )

        def test_filter(self):
            with patch(
                "requests.sessions.Session.get",
                return_value=Response(fixture="{}/{}.json".format(self.app, self.name)),
            ) as mock:
                ret = getattr(nb, self.name).filter(name="test")
                self.assertTrue(ret)
                self.assertTrue(isinstance(ret, list))
                self.assertTrue(isinstance(ret[0], self.ret))
                mock.assert_called_with(
                    self.bulk_uri, params={"name": "test"}, json=None, headers=HEADERS,
                )

        def test_get(self):
            with patch(
                "requests.sessions.Session.get",
                return_value=Response(fixture="{}/{}.json".format(self.app, self.name[:-1])),
            ) as mock:
                ret = getattr(nb, self.name).get(self.uuid)
                self.assertTrue(ret)
                self.assertTrue(isinstance(ret, self.ret))
                self.assertTrue(isinstance(str(ret), str))
                self.assertTrue(isinstance(dict(ret), dict))
                mock.assert_called_with(
                    self.detail_uri, params={}, json=None, headers=HEADERS,
                )

        def test_delete(self):
            with patch(
                "requests.sessions.Session.get",
                return_value=Response(fixture="{}/{}.json".format(self.app, self.name[:-1])),
            ) as mock, patch("requests.sessions.Session.delete") as delete:
                ret = getattr(nb, self.name).get(self.uuid)
                self.assertEqual(self.uuid, ret.id)
                self.assertTrue(ret.delete())
                mock.assert_called_with(
                    self.detail_uri, params={}, json=None, headers=HEADERS,
                )
                delete.assert_called_with(
                    self.detail_uri, params={}, json=None, headers=HEADERS,
                )

        def test_diff(self):
            with patch(
                "requests.sessions.Session.get",
                return_value=Response(fixture="{}/{}.json".format(self.app, self.name[:-1])),
            ):
                ret = getattr(nb, self.name).get(self.uuid)
                self.assertTrue(ret)
                self.assertEqual(ret._diff(), set())

        def test_serialize(self):
            with patch(
                "requests.sessions.Session.get",
                return_value=Response(fixture="{}/{}.json".format(self.app, self.name[:-1])),
            ):
                ret = getattr(nb, self.name).get(self.uuid)
                self.assertTrue(ret)
                self.assertTrue(ret.serialize())


class DeviceTestCase(Generic.Tests):
    name = "devices"

    @patch(
        "requests.sessions.Session.get", return_value=Response(fixture="dcim/device.json"),
    )
    def test_get(self, mock):
        ret = getattr(nb, self.name).get(self.uuid)
        self.assertTrue(ret)
        self.assertTrue(isinstance(ret, self.ret))
        self.assertTrue(isinstance(ret.primary_ip, pynautobot.models.ipam.IpAddresses))
        self.assertTrue(isinstance(ret.primary_ip4, pynautobot.models.ipam.IpAddresses))
        self.assertTrue(isinstance(ret.config_context, dict))
        self.assertTrue(isinstance(ret.custom_fields, dict))
        self.assertTrue(isinstance(ret.local_context_data, dict))
        mock.assert_called_with(
            self.detail_uri, params={}, json=None, headers=HEADERS,
        )

    @patch(
        "requests.sessions.Session.get", return_value=Response(fixture="dcim/devices.json"),
    )
    def test_multi_filter(self, mock):
        ret = getattr(nb, self.name).filter(role=["test", "test1"], site="TEST#1")
        self.assertTrue(ret)
        self.assertTrue(isinstance(ret, list))
        self.assertTrue(isinstance(ret[0], self.ret))
        mock.assert_called_with(
            self.bulk_uri, params={"role": ["test", "test1"], "site": "TEST#1"}, json=None, headers=HEADERS,
        )

    @patch(
        "requests.sessions.Session.get", return_value=Response(fixture="dcim/device.json"),
    )
    def test_modify(self, *_):
        ret = nb.devices.get(self.uuid)
        ret.serial = "123123123123"
        ret_serialized = ret.serialize()
        self.assertTrue(ret_serialized)
        self.assertEqual(ret._diff(), {"serial"})
        self.assertEqual(ret_serialized["serial"], "123123123123")

    @patch(
        "requests.sessions.Session.post", return_value=Response(fixture="dcim/device.json"),
    )
    def test_create(self, mock):
        data = {
            "name": "test-device",
            "site": 1,
            "device_type": 1,
            "device_role": 1,
        }
        ret = nb.devices.create(**data)
        self.assertTrue(ret)
        mock.assert_called_with(
            self.bulk_uri, headers=POST_HEADERS, params={}, json=data,
        )

    @patch(
        "requests.sessions.Session.post", return_value=Response(fixture="dcim/device_bulk_create.json"),
    )
    def test_create_device_bulk(self, mock):
        data = [
            {"name": "test-device", "site": 1, "device_type": 1, "device_role": 1},
            {"name": "test-device1", "site": 1, "device_type": 1, "device_role": 1},
        ]
        ret = nb.devices.create(data)
        self.assertTrue(ret)
        self.assertTrue(len(ret), 2)
        mock.assert_called_with(
            self.bulk_uri, headers=POST_HEADERS, params={}, json=data,
        )

    @patch(
        "requests.sessions.Session.get",
        side_effect=[Response(fixture="dcim/device.json"), Response(fixture="dcim/rack.json")],
    )
    def test_get_recurse(self, *_):
        """Test that automatic recursion works, and that nested items
        are converted to Response() objects.
        """
        ret = getattr(nb, self.name).get(self.uuid)
        self.assertTrue(ret)
        self.assertTrue(isinstance(ret, self.ret))
        self.assertTrue(isinstance(ret.rack.role, self.ret))

    @patch(
        "requests.sessions.Session.get",
        side_effect=[Response(fixture="dcim/device.json"), Response(fixture="dcim/napalm.json")],
    )
    def test_get_napalm(self, mock):
        test = nb.devices.get(self.uuid)
        ret = test.napalm.list(method="get_facts")
        mock.assert_called_with(
            f"{self.detail_uri}napalm/", params={"method": "get_facts"}, json=None, headers=HEADERS,
        )
        self.assertTrue(ret)
        self.assertTrue(ret["get_facts"])


class SiteTestCase(Generic.Tests):
    name = "sites"

    @patch(
        "requests.sessions.Session.get", return_value=Response(fixture="dcim/site.json"),
    )
    def test_modify_custom(self, *_):
        """Test modifying a custom field.
        """
        ret = getattr(nb, self.name).get(self.uuid)
        ret.custom_fields["test_custom"] = "Testing"
        self.assertEqual(ret._diff(), {"custom_fields"})
        self.assertTrue(ret.serialize())
        self.assertEqual(ret.custom_fields["test_custom"], "Testing")

    @patch(
        "requests.sessions.Session.get", return_value=Response(fixture="dcim/site.json"),
    )
    def test_custom_selection_serializer(self, _):
        """Tests serializer with custom selection fields.
        """
        ret = getattr(nb, self.name).get(self.uuid)
        ret.custom_fields["test_custom"] = "Testing"
        test = ret.serialize()
        self.assertEqual(test["custom_fields"]["test_selection"], 2)

    @patch(
        "requests.sessions.Session.post", return_value=Response(fixture="dcim/site.json"),
    )
    def test_create(self, mock):
        data = {"name": "TEST1", "custom_fields": {"test_custom": "Testing"}}
        ret = nb.sites.create(**data)
        self.assertTrue(ret)
        mock.assert_called_with(
            self.bulk_uri, headers=POST_HEADERS, params={}, json=data,
        )


class InterfaceTestCase(Generic.Tests):
    name = "interfaces"

    @patch(
        "requests.sessions.Session.get", return_value=Response(fixture="dcim/interface.json"),
    )
    def test_modify(self, *_):
        ret = nb.interfaces.get(self.uuid)
        ret.description = "Testing"
        ret_serialized = ret.serialize()
        self.assertTrue(ret)
        self.assertEqual(ret_serialized["description"], "Testing")
        self.assertEqual(ret_serialized["form_factor"], 1400)

    @patch(
        "requests.sessions.Session.get",
        side_effect=[
            Response(fixture="dcim/{}.json".format(name + "_1")),
            Response(fixture="dcim/{}.json".format(name + "_2")),
        ],
    )
    def test_get_all(self, mock):
        ret = getattr(nb, self.name).all()
        self.assertTrue(ret)
        self.assertTrue(isinstance(ret, list))
        self.assertTrue(isinstance(ret[0], self.ret))
        self.assertEqual(len(ret), 71)
        mock.assert_called_with(
            self.bulk_uri, params={"limit": 221, "offset": 50}, json=None, headers=HEADERS,
        )

    @patch(
        "requests.sessions.Session.get",
        side_effect=[Response(fixture="dcim/interface.json"), Response(fixture="dcim/interface_trace.json")],
    )
    def test_trace(self, mock):
        ret = nb.interfaces.get(self.uuid)
        trace = ret.trace()
        self.assertTrue(len(trace) == 3)
        for hop in trace:
            self.assertTrue(len(hop) == 3)


class RackTestCase(Generic.Tests):
    name = "racks"

    @patch(
        "requests.sessions.Session.get",
        side_effect=[Response(fixture="dcim/rack.json"), Response(fixture="dcim/rack_u.json")],
    )
    def test_get_units(self, mock):
        test = nb.racks.get(self.uuid)
        ret = test.units.list()
        mock.assert_called_with(
            f"{self.detail_uri}units/", params={}, json=None, headers=HEADERS,
        )
        self.assertTrue(ret)
        self.assertTrue(isinstance(ret[0].device, pynautobot.models.dcim.Devices))

    @patch(
        "requests.sessions.Session.get",
        side_effect=[Response(fixture="dcim/rack.json"), Response(fixture="dcim/rack_u.json")],
    )
    def test_get_elevation(self, mock):
        test = nb.racks.get(self.uuid)
        ret = test.elevation.list()
        mock.assert_called_with(
            f"{self.detail_uri}elevation/", params={}, json=None, headers=HEADERS,
        )
        self.assertTrue(ret)
        self.assertTrue(isinstance(ret[0].device, pynautobot.models.dcim.Devices))


class RackRoleTestCase(Generic.Tests):
    name = "rack_roles"


class RegionTestCase(Generic.Tests):
    name = "regions"


class RackGroupsTestCase(Generic.Tests):
    name = "rack_groups"


class RackReservationsTestCase(Generic.Tests):
    name = "rack_reservations"


class ManufacturersTestCase(Generic.Tests):
    name = "manufacturers"


class DeviceTypeTestCase(Generic.Tests):
    name = "device_types"


class ConsolePortTemplateTestCase(Generic.Tests):
    name = "console_port_templates"


class ConsoleServerPortTemplateTestCase(Generic.Tests):
    name = "console_server_port_templates"


class PowerPortTemplateTestCase(Generic.Tests):
    name = "power_port_templates"


class PowerOutletTemplateTestCase(Generic.Tests):
    name = "power_outlet_templates"


class InterfaceTemplateTestCase(Generic.Tests):
    name = "interface_templates"


class DeviceBayTemplateTestCase(Generic.Tests):
    name = "device_bay_templates"


class DeviceRolesTestCase(Generic.Tests):
    name = "device_roles"


class PlatformsTestCase(Generic.Tests):
    name = "platforms"


class ConsolePortsTestCase(Generic.Tests):
    name = "console_ports"


class ConsoleServerPortsTestCase(Generic.Tests):
    name = "console_server_ports"


class PowerPortsTestCase(Generic.Tests):
    name = "power_ports"


class PowerOutletsTestCase(Generic.Tests):
    name = "power_outlets"


class DeviceBaysTestCase(Generic.Tests):
    name = "device_bays"


# class InventoryItemsTestCase(Generic.Tests):
#     name = 'inventory_items'


class InterfaceConnectionsTestCase(Generic.Tests):
    name = "interface_connections"


# class ConnectedDevicesTestCase(Generic.Tests):
#     name = 'connected_device'


class VirtualChassisTestCase(Generic.Tests):
    name = "virtual_chassis_devices"


class Choices(unittest.TestCase):
    def test_get(self):
        with patch(
            "requests.sessions.Session.get", return_value=Response(fixture="{}/{}.json".format("dcim", "choices")),
        ) as mock:
            ret = nb.choices()
            self.assertTrue(ret)
            mock.assert_called_with(
                "http://localhost:8000/api/dcim/_choices/", params={}, json=None, headers=HEADERS,
            )


class CablesTestCase(Generic.Tests):
    name = "cables"

    def test_get_circuit(self):
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
                        "cid": "TEST123321",
                    },
                    "term_side": "A",
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
        with patch("requests.sessions.Session.get", return_value=response_obj,) as mock:
            ret = getattr(nb, self.name).get(self.uuid)
            self.assertTrue(ret)
            self.assertTrue(isinstance(ret, self.ret))
            self.assertTrue(isinstance(str(ret), str))
            self.assertTrue(isinstance(dict(ret), dict))
            mock.assert_called_with(
                self.detail_uri, headers=HEADERS, params={}, json=None,
            )
