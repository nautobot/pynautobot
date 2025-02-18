"""Wireless tests."""
from packaging import version

import pytest


class TestWirelessApp:
    """Wireless test."""
    @pytest.fixture
    def skipif_version(self, nb_status):
        """Skip the test if the Nautobot version is less than 2.4."""
        nautobot_version = nb_status.get("nautobot-version")
        if version.parse(nautobot_version) < version.parse("2.4"):
            pytest.skip("Wireless app is only in Nautobot 2.4+")

        return nautobot_version

    def test_wireless_networks(self, skipif_version, nb_client):
        """Verify we can CRUD a wireless network."""
        assert skipif_version

        # Create
        wireless_network = nb_client.wireless.wireless_networks.create(
            name="Test Wireless Network", ssid="Test SSID", mode="Mesh", authentication="WPA2 Personal"
        )
        assert wireless_network

        # Read
        test_wireless_network = nb_client.wireless.wireless_networks.get(name="Test Wireless Network")
        assert test_wireless_network.name == "Test Wireless Network"

        # Update
        test_wireless_network.name = "Updated Test Wireless Network"
        test_wireless_network.save()
        updated_wireless_network = nb_client.wireless.wireless_networks.get(name="Updated Test Wireless Network")
        assert updated_wireless_network.name == "Updated Test Wireless Network"

        # Delete
        updated_wireless_network.delete()
        deleted_wireless_network = nb_client.wireless.wireless_networks.get(name="Updated Test Wireless Network")
        assert not deleted_wireless_network

    def test_wireless_radio_profiles(self, skipif_version, nb_client):
        """Verify we can CRUD a wireless radio profile."""
        assert skipif_version

        # Create
        wireless_radio_profile = nb_client.wireless.radio_profiles.create(
            name="802.11ax",
            regulatory_domain="US",
            allowed_channel_list=["1"],
            channel_width=[20],
        )
        assert wireless_radio_profile

        # Read
        test_wireless_radio_profile = nb_client.wireless.radio_profiles.get(name="802.11ax")
        assert test_wireless_radio_profile.name == "802.11ax"

        # Update
        test_wireless_radio_profile.frequency = "5GHz"
        test_wireless_radio_profile.save()
        updated_wireless_radio_profile = nb_client.wireless.radio_profiles.get(name="802.11ax")
        assert updated_wireless_radio_profile.frequency == "5GHz"

        # Delete
        updated_wireless_radio_profile.delete()
        deleted_wireless_radio_profile = nb_client.wireless.radio_profiles.get(name="802.11ax")
        assert not deleted_wireless_radio_profile

    def test_wireless_supported_data_rates(self, skipif_version, nb_client):
        """Verify we can CRUD a wireless supported data rate."""
        assert skipif_version

        # Create
        wireless_supported_data_rate = nb_client.wireless.supported_data_rates.create(standard="802.11ax", rate=40000)
        assert wireless_supported_data_rate

        # Read
        test_wireless_supported_data_rate = nb_client.wireless.supported_data_rates.get(standard="802.11ax")
        assert test_wireless_supported_data_rate.standard == "802.11ax"

        # Update
        test_wireless_supported_data_rate.rate = 80000
        test_wireless_supported_data_rate.save()
        updated_wireless_supported_data_rate = nb_client.wireless.supported_data_rates.get(standard="802.11ax")
        assert updated_wireless_supported_data_rate.rate == 80000

        # Delete
        updated_wireless_supported_data_rate.delete()
        deleted_wireless_supported_data_rate = nb_client.wireless.supported_data_rates.get(standard="802.11ax")
        assert not deleted_wireless_supported_data_rate
