"""Exclude m2m tests."""

import pytest
from packaging import version


class TestExcludeM2M:
    """Testing exclude_m2m."""

    @pytest.fixture(autouse=True, scope="class")
    def skipif_version(self, nb_status):
        """Skip all tests in this class if the Nautobot version is less than 2.4."""
        nautobot_version = nb_status.get("nautobot-version")
        if version.parse(nautobot_version) < version.parse("2.4"):
            pytest.skip("The exclude_m2m filter is only in Nautobot 2.4+")

    def test_prefix_include_m2m_get(self, nb_client):
        prefixes = nb_client.ipam.prefixes.get(prefix="192.0.0.0/8")
        assert "locations" in prefixes.serialize()

    def test_prefix_include_m2m_all(self, nb_client):
        prefixes = nb_client.ipam.prefixes.all()
        assert "locations" in prefixes[0].serialize()

    def test_prefix_include_m2m_filter(self, nb_client):
        prefixes = nb_client.ipam.prefixes.filter(prefix="192.0.0.0/8")
        assert "locations" in prefixes[0].serialize()

    def test_prefix_exclude_m2m_get(self, nb_client_exclude_m2m):
        prefixes = nb_client_exclude_m2m.ipam.prefixes.get(prefix="192.0.0.0/8")
        assert "locations" not in prefixes.serialize()

    def test_prefix_exclude_m2m_all(self, nb_client_exclude_m2m):
        prefixes = nb_client_exclude_m2m.ipam.prefixes.all()
        assert "locations" not in prefixes[0].serialize()

    def test_prefix_exclude_m2m_filter(self, nb_client_exclude_m2m):
        prefixes = nb_client_exclude_m2m.ipam.prefixes.filter(prefix="192.0.0.0/8")
        assert "locations" not in prefixes[0].serialize()

    def test_prefix_m2m_override_false_get(self, nb_client_exclude_m2m):
        """Test that even if exclude_m2m is set, we can override it for a single get request."""
        prefixes = nb_client_exclude_m2m.ipam.prefixes.get(prefix="192.0.0.0/8", exclude_m2m=False)
        assert "locations" in prefixes.serialize()

    def test_prefix_m2m_override_false_all(self, nb_client_exclude_m2m):
        """Test that even if exclude_m2m is set, we can override it for a single all request."""
        prefixes = nb_client_exclude_m2m.ipam.prefixes.all(exclude_m2m=False)
        assert "locations" in prefixes[0].serialize()

    def test_prefix_m2m_override_false_filter(self, nb_client_exclude_m2m):
        """Test that even if exclude_m2m is set, we can override it for a single filter request."""
        prefixes = nb_client_exclude_m2m.ipam.prefixes.filter(prefix="192.0.0.0/8", exclude_m2m=False)
        assert "locations" in prefixes[0].serialize()

    def test_prefix_m2m_override_true_get(self, nb_client):
        """Test that even if exclude_m2m is set, we can override it for a single get request."""
        prefixes = nb_client.ipam.prefixes.get(prefix="192.0.0.0/8", exclude_m2m=True)
        assert "locations" not in prefixes.serialize()

    def test_prefix_m2m_override_true_all(self, nb_client):
        """Test that even if exclude_m2m is set, we can override it for a single all request."""
        prefixes = nb_client.ipam.prefixes.all(exclude_m2m=True)
        assert "locations" not in prefixes[0].serialize()

    def test_prefix_m2m_override_true_filter(self, nb_client):
        """Test that even if exclude_m2m is set, we can override it for a single filter request."""
        prefixes = nb_client.ipam.prefixes.filter(prefix="192.0.0.0/8", exclude_m2m=True)
        assert "locations" not in prefixes[0].serialize()

    def test_permission_include_m2m_create(self, nb_client):
        permissions = nb_client.users.permissions.create(
            name="Testing Exclude M2M Create 1", actions=["view"], object_types=["dcim.device"]
        )
        assert "object_types" in permissions.serialize()

    def test_permission_exclude_m2m_create(self, nb_client_exclude_m2m):
        permissions = nb_client_exclude_m2m.users.permissions.create(
            name="Testing Exclude M2M Create 2", actions=["view"], object_types=["dcim.device"]
        )
        assert "object_types" not in permissions.serialize()

    def test_permission_include_m2m_bulk_update(self, nb_client):
        permissions = list(nb_client.users.permissions.filter(name="Testing Exclude M2M Create 1"))
        permissions[0].description = "Testing Exclude M2M Bulk Update 1"
        permissions_updated = nb_client.users.permissions.update(permissions)
        assert "object_types" in permissions_updated[0].serialize()

    def test_permission_exclude_m2m_bulk_update(self, nb_client_exclude_m2m):
        permissions = list(nb_client_exclude_m2m.users.permissions.filter(name="Testing Exclude M2M Create 2"))
        permissions[0].description = "Testing Exclude M2M Bulk Update 2"
        permissions_updated = nb_client_exclude_m2m.users.permissions.update(permissions)
        assert "object_types" not in permissions_updated[0].serialize()


class TestIncludeFilters:
    """Testing include filters."""

    def test_device_exclude_config_context_get(self, nb_client):
        devices = nb_client.dcim.devices.get(name="dev-1")
        assert "config_context" not in devices.serialize()

    def test_device_exclude_config_context_all(self, nb_client):
        devices = nb_client.dcim.devices.all()
        assert "config_context" not in devices[0].serialize()

    def test_device_exclude_config_context_filter(self, nb_client):
        devices = nb_client.dcim.devices.filter(name="dev-1")
        assert "config_context" not in devices[0].serialize()

    def test_device_include_config_context_get(self, nb_client_include_config_context):
        devices = nb_client_include_config_context.dcim.devices.get(name="dev-1")
        assert "config_context" in devices.serialize()

    def test_device_include_config_context_all(self, nb_client_include_config_context):
        nb_client_include_config_context.default_filters["include"] = "config_context,computed_fields"
        devices = nb_client_include_config_context.dcim.devices.all()
        assert "config_context" in devices[0].serialize()
        assert "computed_fields" in devices[0].serialize()

    def test_device_include_config_context_filter(self, nb_client_include_config_context):
        devices = nb_client_include_config_context.dcim.devices.filter(name="dev-1")
        assert "config_context" in devices[0].serialize()

    def test_device_include_config_context_override_false_get(self, nb_client_include_config_context):
        devices = nb_client_include_config_context.dcim.devices.get(name="dev-1", include="")
        assert "config_context" not in devices.serialize()

    def test_device_include_config_context_override_false_all(self, nb_client_include_config_context):
        nb_client_include_config_context.default_filters["include"] = "config_context,computed_fields"
        devices = nb_client_include_config_context.dcim.devices.all(include="")
        assert "config_context" not in devices[0].serialize()
        assert "computed_fields" not in devices[0].serialize()

    def test_device_include_config_context_override_false_filter(self, nb_client_include_config_context):
        devices = nb_client_include_config_context.dcim.devices.filter(name="dev-1", include="")
        assert "config_context" not in devices[0].serialize()

    def test_device_include_config_context_override_true_get(self, nb_client):
        devices = nb_client.dcim.devices.get(name="dev-1", include="config_context")
        assert "config_context" in devices.serialize()

    def test_device_include_config_context_override_true_all(self, nb_client):
        devices = nb_client.dcim.devices.all(include="config_context,computed_fields")
        assert "config_context" in devices[0].serialize()
        assert "computed_fields" in devices[0].serialize()

    def test_device_include_config_context_override_true_filter(self, nb_client):
        devices = nb_client.dcim.devices.filter(name="dev-1", include="config_context")
        assert "config_context" in devices[0].serialize()
