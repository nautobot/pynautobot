"""DCIM tests."""

import pytest


def test_create_manufacturer(nb_client):
    cisco_manu = {"name": "Cisco", "slug": "cisco"}
    cisco = nb_client.dcim.manufacturers.create(cisco_manu)
    juniper_manu = {"name": "Juniper", "slug": "juniper"}
    juniper = nb_client.dcim.manufacturers.create(**juniper_manu)
    demo = nb_client.dcim.manufacturers.create(name="Demo", slug="demo")
    assert cisco
    assert juniper
    assert demo


class TestSimpleServerRackingAndConnecting:
    """Verify we can create, rack, and connect a server."""

    @pytest.fixture
    def location(self, nb_client):
        """Verify we can create a location."""
        location_types = ["dcim.device", "dcim.rack", "dcim.rackgroup"]
        site_type = nb_client.dcim.location_types.create(name="Site", content_types=location_types, nestable=True)
        location_name = "MSP"
        location = nb_client.dcim.locations.create(
            name=location_name,
            status={"name": "Active"},
            location_type=site_type.id,
        )
        assert location

        return location

    @pytest.fixture
    def rack_group(self, location):
        """Verify we can create a rack device."""
        rack_group = location.api.dcim.rack_groups.create(name="rack_group_1", location=location.id)
        assert rack_group

        return rack_group

    @pytest.fixture
    def rack(self, location, rack_group):
        """Verify we can create a rack device."""
        rack = location.api.dcim.racks.create(
            name="rack1", location=location.id, rack_group=rack_group.id, status={"name": "Active"}
        )
        assert rack

        return rack

    @pytest.fixture
    def data_leafs(self, rack, location):
        """Verify we can create data leaf switch devices."""
        devices = []
        for i in [1, 2]:
            device = rack.api.dcim.devices.create(
                name=f"access_switch{i}.networktocode.com",
                device_type={"model": "DCS-7050TX3-48C8"},
                role={"name": "Leaf Switch"},
                location=location.id,
                rack=rack.id,
                face="rear",
                position=rack.u_height - i,
                status={"name": "Active"},
            )
            assert device
            devices.append(device)

        return devices

    @pytest.fixture
    def mgmt_leaf(self, rack, location):
        """Verify we can create data leaf switch devices."""
        device = rack.api.dcim.devices.create(
            name="mgmt_switch1.networktocode.com",
            device_type={"model": "DCS-7010T-48"},
            role={"name": "Leaf Switch"},
            location=location.id,
            rack=rack.id,
            face="rear",
            position=rack.u_height - 3,
            status={"name": "Active"},
        )
        assert device

        return device

    @pytest.fixture
    def server(self, location):
        """Verify we can create a server device."""
        device = location.api.dcim.devices.create(
            name="server.networktocode.com",
            device_type={"model": "PowerEdge R640"},
            role={"name": "Server"},
            location=location.id,
            status={"name": "Active"},
        )
        assert device

        return device

    # pylint: disable=too-many-arguments, too-many-locals, too-many-positional-arguments
    def test_racking_server(self, nb_client, server, data_leafs, mgmt_leaf, rack):
        """Verify we can rack the server."""
        assert server.update({"rack": rack.id, "face": "front", "position": rack.u_height - 4})

        # connect the mgmt iface
        server_mgmt_iface = server.api.dcim.interfaces.get(device_id=server.id, mgmt_only=True, has_cable=False)
        assert server_mgmt_iface

        mleaf_iface = mgmt_leaf.api.dcim.interfaces.filter(mgmt_only=False, has_cable=False)[0]
        cable = server.api.dcim.cables.create(
            termination_a_type="dcim.interface",
            termination_a_id=server_mgmt_iface.id,
            termination_b_type="dcim.interface",
            termination_b_id=mleaf_iface.id,
            status={"name": "Connected"},
        )

        # connect the data ifaces in a bond
        server_data_ifaces = server.api.dcim.interfaces.filter(device_id=server.id, mgmt_only=False)[:2]
        assert len(server_data_ifaces) == 2

        bond_iface = server.api.dcim.interfaces.create(
            device=server.id, name="bond0", type="lag", status={"name": "Active"}
        )
        assert bond_iface

        for server_data_iface, data_leaf in zip(server_data_ifaces, data_leafs):
            dleaf_iface = data_leaf.api.dcim.interfaces.filter(
                device_id=data_leaf.id, mgmt_only=False, has_cable=False
            )[0]
            cable = server.api.dcim.cables.create(
                termination_a_type="dcim.interface",
                termination_a_id=server_data_iface.id,
                termination_b_type="dcim.interface",
                termination_b_id=dleaf_iface.id,
                status={"name": "Connected"},
            )
            assert cable

            assert server_data_iface.update({"lag": bond_iface.id})

        # now reload the server and verify it's set correctly
        server = nb_client.dcim.devices.get(name="server.networktocode.com")

        # check the cable traces
        for iface in server.api.dcim.interfaces.filter(device_id=server.id, has_cable=True):
            trace = iface.trace()
            assert len(trace) == 1
            local_iface, cable, remote_iface = trace[0]

            assert local_iface.device.id == server.id
            assert remote_iface.device.id in [dleaf_iface.id] + [data_leaf.id for data_leaf in data_leafs]

        # check that it's racked properly
        assert server.rack.id == rack.id

    def test_string_represention(self, nb_client):
        """Validate two device objects return the proper string when casting to string."""
        location = nb_client.dcim.locations.get(name="MSP")
        device_no_name = nb_client.dcim.devices.create(
            device_type={"model": "DCS-7050TX3-48C8"},
            role={"name": "Leaf Switch"},
            location=location.id,
            status={"name": "Active"},
        )
        device_w_name = nb_client.dcim.devices.create(
            name="im a real boy",
            device_type={"model": "DCS-7050TX3-48C8"},
            role={"name": "Leaf Switch"},
            location=location.id,
            status={"name": "Active"},
        )
        assert str(device_no_name) == f"Arista DCS-7050TX3-48C8 ({device_no_name['id']})"
        assert str(device_w_name) == "im a real boy"

    def test_fetching_vc_success(self, nb_client):
        """Validate nb_client.dcim.virtual_chassis.all() fetches successfully and has the correct data."""
        location = nb_client.dcim.locations.get(name="MSP")
        dev1 = nb_client.dcim.devices.create(
            name="dev-1",
            device_type={"model": "DCS-7050TX3-48C8"},
            role={"name": "Leaf Switch"},
            location=location.id,
            status={"name": "Active"},
            local_config_context_data={"foo": "bar"},
        )
        vc = nb_client.dcim.virtual_chassis.create(name="VC1", master=dev1.id)
        nb_client.dcim.devices.create(
            name="dev-2",
            device_type={"model": "DCS-7050TX3-48C8"},
            role={"name": "Leaf Switch"},
            location=location.id,
            status={"name": "Active"},
            virtual_chassis=vc.id,
            vc_position=2,
            local_config_context_data={"foo": "bar"},
        )
        all_vcs = nb_client.dcim.virtual_chassis.all()
        assert len(all_vcs) == 1

        vc1 = nb_client.dcim.virtual_chassis.get(name="VC1")
        assert vc1.member_count == 2
        assert vc1.master.name == dev1.name
        assert vc1.master.id == dev1.id
