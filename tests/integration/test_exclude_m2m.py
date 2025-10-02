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
