"""IPAM tests."""

from unittest.mock import patch

import pynautobot

from . import HEADERS, POST_HEADERS, Generic, api
from .util import Response


# pylint: disable=protected-access
class PrefixTestCase(Generic.Tests):
    """Prefix test case."""

    app = "ipam"
    name = "prefixes"
    name_singular = "prefix"

    @patch(
        "requests.sessions.Session.get",
        side_effect=[Response(fixture="ipam/namespace.json"), Response(fixture="ipam/prefix.json")],
    )
    def test_namespace_in_prefix(self, mock):
        namespace = self.endpoint.get(self.uuid)
        prefix = api.ipam.prefixes.get(self.uuid)
        mock.assert_called_with(
            f"http://localhost:8000/api/ipam/prefixes/{self.uuid}/",
            params={},
            json=None,
            headers=HEADERS,
        )
        self.assertEqual(namespace.id, prefix.namespace.id)
        self.assertEqual(namespace.name, prefix.namespace.name)

    @patch("requests.sessions.Session.get", return_value=Response(fixture="ipam/prefix.json"))
    def test_modify(self, *_):
        ret = self.endpoint.get(self.uuid)
        ret.prefix = "10.1.2.0/24"
        ret_serialized = ret.serialize()
        self.assertTrue(ret_serialized)
        self.assertEqual(ret._diff(), {"prefix"})
        self.assertEqual(ret_serialized["prefix"], "10.1.2.0/24")
        self.assertTrue(ret.tags)
        self.assertIsInstance(ret.tags[0], pynautobot.core.response.Record)

    @patch("requests.sessions.Session.put", return_value=Response(fixture="ipam/prefix.json"))
    @patch("requests.sessions.Session.get", return_value=Response(fixture="ipam/prefix.json"))
    def test_idempotence(self, *_):
        ret = self.endpoint.get(self.uuid)
        test = ret.save()
        self.assertFalse(test)

    @patch(
        "requests.sessions.Session.get",
        side_effect=[Response(fixture="ipam/prefix.json"), Response(fixture="ipam/available-ips.json")],
    )
    def test_get_available_ips(self, mock):
        pfx = self.endpoint.get(self.uuid)
        ret = pfx.available_ips.list()
        mock.assert_called_with(f"{self.detail_uri}available-ips/", params={}, json=None, headers=HEADERS)
        self.assertTrue(ret)
        self.assertEqual(len(ret), 3)
        for record in ret:
            self.assertEqual(record.address, str(record))

    @patch("requests.sessions.Session.post", return_value=Response(fixture="ipam/available-ips-post.json"))
    @patch("requests.sessions.Session.get", return_value=Response(fixture="ipam/prefix.json"))
    def test_create_available_ips(self, _, post):
        create_parms = {"status": 2}
        pfx = self.endpoint.get(self.uuid)
        ret = pfx.available_ips.create(create_parms)
        post.assert_called_with(f"{self.detail_uri}available-ips/", params={}, headers=POST_HEADERS, json=create_parms)
        self.assertTrue(ret)
        self.assertIsInstance(ret, pynautobot.core.response.Record)

    @patch(
        "requests.sessions.Session.get",
        side_effect=[Response(fixture="ipam/prefix.json"), Response(fixture="ipam/available-prefixes.json")],
    )
    def test_get_available_prefixes(self, mock):
        pfx = self.endpoint.get(self.uuid)
        ret = pfx.available_prefixes.list()
        mock.assert_called_with(f"{self.detail_uri}available-prefixes/", params={}, json=None, headers=HEADERS)
        self.assertTrue(ret)
        self.assertEqual(len(ret), 1)
        for record in ret:
            self.assertEqual(record.prefix, str(record))

    @patch("requests.sessions.Session.post", return_value=Response(fixture="ipam/available-prefixes-post.json"))
    @patch("requests.sessions.Session.get", return_value=Response(fixture="ipam/prefix.json"))
    def test_create_available_prefixes(self, _, post):
        create_parms = {"prefix_length": 30}
        pfx = self.endpoint.get(self.uuid)
        ret = pfx.available_prefixes.create(create_parms)
        post.assert_called_with(
            f"{self.detail_uri}available-prefixes/", params={}, headers=POST_HEADERS, json=create_parms
        )
        self.assertTrue(ret)
        self.assertTrue(isinstance(ret[0], pynautobot.models.ipam.Prefixes))


class IPAddressTestCase(Generic.Tests):
    """IP Address test case."""

    app = "ipam"
    name = "ip_addresses"
    name_singular = "ip_address"

    @patch("requests.sessions.Session.get", return_value=Response(fixture="ipam/ip_address.json"))
    def test_modify(self, *_):
        ret = self.endpoint.get(self.uuid)
        ret.description = "testing"
        ret_serialized = ret.serialize()
        self.assertTrue(ret_serialized)
        self.assertEqual(ret._diff(), {"description"})
        self.assertEqual(ret_serialized["address"], "10.0.255.1/32")
        self.assertEqual(ret_serialized["description"], "testing")


class RoleTestCase(Generic.Tests):
    """Role test case."""

    app = "ipam"
    name = "roles"


class RIRTestCase(Generic.Tests):
    """RIR test case."""

    app = "ipam"
    name = "rirs"


class AggregatesTestCase(Generic.Tests):
    """Aggregates test case."""

    app = "ipam"
    name = "aggregates"

    @patch(
        "requests.sessions.Session.get",
        side_effect=[Response(fixture="ipam/aggregate.json")],
    )
    def test_get_aggregate_stringify(self, mock):
        ret = self.endpoint.get(self.uuid)
        mock.assert_called_with(f"{self.detail_uri}", params={}, json=None, headers=HEADERS)
        self.assertTrue(ret)
        self.assertEqual(ret.prefix, str(ret))


class VlanTestCase(Generic.Tests):
    """Vlan test case."""

    app = "ipam"
    name = "vlans"

    @patch(
        "requests.sessions.Session.get",
        side_effect=[Response(fixture="ipam/vlan.json"), Response(fixture="dcim/interface.json")],
    )
    def test_vlan_in_interface(self, mock):
        vlan = self.endpoint.get(self.uuid)
        interface = api.dcim.interfaces.get(self.uuid)
        mock.assert_called_with(
            f"http://localhost:8000/api/dcim/interfaces/{self.uuid}/",
            params={},
            json=None,
            headers=HEADERS,
        )
        self.assertEqual(vlan.vid, interface.tagged_vlans[0].vid)
        self.assertEqual(vlan.id, interface.tagged_vlans[0].id)
        self.assertTrue(vlan in interface.tagged_vlans)


class VlanGroupsTestCase(Generic.Tests):
    """Vlan Groups test case."""

    app = "ipam"
    name = "vlan_groups"


class VRFTestCase(Generic.Tests):
    """VRF test case."""

    app = "ipam"
    name = "vrfs"

    @patch(
        "requests.sessions.Session.get",
        side_effect=[Response(fixture="ipam/namespace.json"), Response(fixture="ipam/vrf.json")],
    )
    def test_namespace_in_vrf(self, mock):
        namespace = self.endpoint.get(self.uuid)
        vrf = api.ipam.vrfs.get(self.uuid)
        mock.assert_called_with(
            f"http://localhost:8000/api/ipam/vrfs/{self.uuid}/",
            params={},
            json=None,
            headers=HEADERS,
        )
        self.assertEqual(namespace.id, vrf.namespace.id)
        self.assertEqual(namespace.name, vrf.namespace.name)


class NameSpaceTestCase(Generic.Tests):
    """Namespace test case."""

    app = "ipam"
    name = "namespaces"
    name_singular = "namespace"


# class ServicesTestCase(Generic.Tests):
#     app = "ipam"
#     name = "services"
