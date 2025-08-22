"""Response tests."""

import pytest
from packaging import version


class TestRecord:
    """Test the Record class."""

    def test_serialize_single_choice(self, nb_client):
        devices = nb_client.dcim.devices.all()
        device = devices[0]
        assert isinstance(dict(device)["face"], dict)
        face_value = dict(device)["face"]["value"]
        assert isinstance(device.serialize()["face"], str)
        assert device.serialize()["face"] == face_value

    def test_serialize_choice_list(self, nb_client, nb_status):
        nautobot_version = nb_status["nautobot-version"]
        if version.parse(nautobot_version) < version.parse("2.4"):
            pytest.skip("Wireless models are only in Nautobot 2.4+")

        radio_profile = nb_client.wireless.radio_profiles.create(
            name="Test Radio Profile",
            regulatory_domain="US",
            channel_width=[20, 40],
        )

        assert isinstance(dict(radio_profile)["channel_width"][0], dict)
        channel_width_value = dict(radio_profile)["channel_width"][0]["value"]
        assert isinstance(radio_profile.serialize()["channel_width"][0], int)
        assert radio_profile.serialize()["channel_width"][0] == channel_width_value
