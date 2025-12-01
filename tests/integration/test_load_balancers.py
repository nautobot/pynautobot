"""Load balancers tests."""

import pytest
from packaging import version


class TestLoadBalancersApp:
    """Load balancers test."""

    @pytest.fixture
    def skipif_version(self, nb_status):
        """Skip the test if the Nautobot version is less than 3.0."""
        nautobot_version = nb_status.get("nautobot-version")
        if version.parse(nautobot_version) < version.parse("3.0.0a0"):
            pytest.skip("Load balancers app is only in Nautobot 3.0+")

        return nautobot_version

    def test_virtual_server(self, skipif_version, nb_client):
        """Verify we can CRUD a virtual server."""
        assert skipif_version

        # Create
        prefix = nb_client.ipam.prefixes.create(prefix="10.0.0.0/24", status="Active", namespace="Global")
        ip_address = nb_client.ipam.ip_addresses.create(address="10.0.0.1/32", status="Active", namespace="Global")
        virtual_server = nb_client.load_balancers.virtual_servers.create(
            name="Test Virtual Server", vip=ip_address.id, protocol="tcp"
        )
        assert virtual_server

        # Read
        test_virtual_server = nb_client.load_balancers.virtual_servers.get(name="Test Virtual Server")
        assert test_virtual_server.name == "Test Virtual Server"

        # Update
        test_virtual_server.name = "Updated Test Virtual Server"
        test_virtual_server.save()
        updated_virtual_server = nb_client.load_balancers.virtual_servers.get(name="Updated Test Virtual Server")
        assert updated_virtual_server.name == "Updated Test Virtual Server"

        # Delete
        updated_virtual_server.delete()
        deleted_virtual_server = nb_client.load_balancers.virtual_servers.get(name="Updated Test Virtual Server")
        assert not deleted_virtual_server

        # Cleanup
        ip_address.delete()
        prefix.delete()

    def test_load_balancer_pools(self, skipif_version, nb_client):
        """Verify we can CRUD a load balancer pool."""
        assert skipif_version

        # Create
        load_balancer_pool = nb_client.load_balancers.load_balancer_pools.create(
            name="Test Load Balancer Pool", load_balancing_algorithm="round_robin"
        )
        assert load_balancer_pool

        # Read
        test_load_balancer_pool = nb_client.load_balancers.load_balancer_pools.get(name="Test Load Balancer Pool")
        assert test_load_balancer_pool.name == "Test Load Balancer Pool"
        assert test_load_balancer_pool.load_balancing_algorithm == "round_robin"

        # Update
        test_load_balancer_pool.load_balancing_algorithm = "least_connections"
        test_load_balancer_pool.save()
        updated_load_balancer_pool = nb_client.load_balancers.load_balancer_pools.get(name="Test Load Balancer Pool")
        assert updated_load_balancer_pool.load_balancing_algorithm == "least_connections"

        # Delete
        updated_load_balancer_pool.delete()
        deleted_load_balancer_pool = nb_client.load_balancers.load_balancer_pools.get(
            name="Updated Test Load Balancer Pool"
        )
        assert not deleted_load_balancer_pool

    def test_load_balancer_pool_members(self, skipif_version, nb_client):
        """Verify we can CRUD a load balancer pool member."""
        assert skipif_version

        # Create
        load_balancer_pool = nb_client.load_balancers.load_balancer_pools.create(
            name="Test Load Balancer Pool", load_balancing_algorithm="round_robin"
        )
        prefix = nb_client.ipam.prefixes.create(prefix="10.1.0.0/24", status="Active", namespace="Global")
        ip_address = nb_client.ipam.ip_addresses.create(address="10.1.0.1/32", status="Active", namespace="Global")
        load_balancer_pool_member = nb_client.load_balancers.load_balancer_pool_members.create(
            load_balancer_pool=load_balancer_pool.id,
            ip_address=ip_address.id,
            port=80,
            status="Active",
        )
        assert load_balancer_pool_member

        # Read
        test_load_balancer_pool_member = nb_client.load_balancers.load_balancer_pool_members.get(
            ip_address=ip_address.id
        )
        assert test_load_balancer_pool_member.ip_address.address == "10.1.0.1/32"
        assert test_load_balancer_pool_member.port == 80

        # Update
        test_load_balancer_pool_member.port = 8080
        test_load_balancer_pool_member.save()
        updated_load_balancer_pool_member = nb_client.load_balancers.load_balancer_pool_members.get(
            ip_address=ip_address.id
        )
        assert updated_load_balancer_pool_member.port == 8080

        # Delete
        updated_load_balancer_pool_member.delete()
        deleted_load_balancer_pool_member = nb_client.load_balancers.load_balancer_pool_members.get(
            ip_address=ip_address.id
        )
        assert not deleted_load_balancer_pool_member

        # Cleanup
        load_balancer_pool.delete()
        ip_address.delete()
        prefix.delete()
