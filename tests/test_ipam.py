from unittest.mock import patch

import pynautobot

from . import Generic, api, HEADERS, POST_HEADERS
from .util import Response


class PrefixTestCase(Generic.Tests):
    app = "ipam"
    name = "prefixes"
    name_singular = "prefix"

    @patch("requests.sessions.Session.get", return_value=Response(fixture="ipam/prefix.json"))
    def test_modify(self, *_):
        ret = self.endpoint.get(self.uuid)
        ret.prefix = "10.1.2.0/24"
        ret_serialized = ret.serialize()
        self.assertTrue(ret_serialized)
        self.assertEqual(ret._diff(), {"prefix"})
        self.assertEqual(ret_serialized["prefix"], "10.1.2.0/24")

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

    @patch("requests.sessions.Session.post", return_value=Response(fixture="ipam/available-ips-post.json"))
    @patch("requests.sessions.Session.get", return_value=Response(fixture="ipam/prefix.json"))
    def test_create_available_ips(self, _, post):
        create_parms = dict(status=2,)
        pfx = self.endpoint.get(self.uuid)
        ret = pfx.available_ips.create(create_parms)
        post.assert_called_with(f"{self.detail_uri}available-ips/", params={}, headers=POST_HEADERS, json=create_parms)
        self.assertTrue(ret)
        self.assertTrue(isinstance(ret, pynautobot.models.ipam.IpAddresses))

    @patch(
        "requests.sessions.Session.get",
        side_effect=[Response(fixture="ipam/prefix.json"), Response(fixture="ipam/available-prefixes.json")],
    )
    def test_get_available_prefixes(self, mock):
        pfx = self.endpoint.get(self.uuid)
        ret = pfx.available_prefixes.list()
        mock.assert_called_with(f"{self.detail_uri}available-prefixes/", params={}, json=None, headers=HEADERS)
        self.assertTrue(ret)

    @patch("requests.sessions.Session.post", return_value=Response(fixture="ipam/available-prefixes-post.json"))
    @patch("requests.sessions.Session.get", return_value=Response(fixture="ipam/prefix.json"))
    def test_create_available_prefixes(self, _, post):
        create_parms = dict(prefix_length=30,)
        pfx = self.endpoint.get(self.uuid)
        ret = pfx.available_prefixes.create(create_parms)
        post.assert_called_with(
            f"{self.detail_uri}available-prefixes/", params={}, headers=POST_HEADERS, json=create_parms
        )
        self.assertTrue(ret)
        self.assertTrue(isinstance(ret[0], pynautobot.models.ipam.Prefixes))


class IPAddressTestCase(Generic.Tests):
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
    app = "ipam"
    name = "roles"


class RIRTestCase(Generic.Tests):
    app = "ipam"
    name = "rirs"


class AggregatesTestCase(Generic.Tests):
    app = "ipam"
    name = "aggregates"


class VlanTestCase(Generic.Tests):
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
            f"http://localhost:8000/api/dcim/interfaces/{self.uuid}/", params={}, json=None, headers=HEADERS,
        )
        self.assertEqual(vlan.vid, interface.tagged_vlans[0].vid)
        self.assertEqual(vlan.id, interface.tagged_vlans[0].id)
        self.assertTrue(vlan in interface.tagged_vlans)


class VlanGroupsTestCase(Generic.Tests):
    app = "ipam"
    name = "vlan_groups"


class VRFTestCase(Generic.Tests):
    app = "ipam"
    name = "vrfs"


# class ServicesTestCase(Generic.Tests):
#     app = "ipam"
#     name = "services"
