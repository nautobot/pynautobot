"""Endpoint tests."""

import pytest
from packaging import version


class TestEndpoint:
    """Verify different methods on an endpoint."""

    def test_get_all_devices(self, nb_client):
        devices = nb_client.dcim.devices.all()
        assert len(devices) == 8

    def test_get_all_devices_include_context(self, nb_client):
        devices = nb_client.dcim.devices.all(name="dev-1", include=["config_context"])
        assert devices[0].config_context == {"foo": "bar"}

    def test_get_filtered_devices(self, nb_client):
        devices = nb_client.dcim.devices.filter(device_type="DCS-7050TX3-48C8")
        assert len(devices) == 6

    def test_choices(self, nb_client):
        choices = nb_client.dcim.devices.choices()
        # Not testing that we get specific choices back, just in case of changes in the API
        assert isinstance(choices, dict)
        assert len(choices) > 0

    def test_child_choices(self, nb_client, nb_status):
        nautobot_version = nb_status["nautobot-version"]
        if version.parse(nautobot_version) < version.parse("2.4"):
            pytest.skip("Child choices are only in Nautobot 2.4+")

        # Some endpoints have fields that is a list of choices (Issue 322)
        choices = nb_client.dcim.controllers.choices()
        assert isinstance(choices, dict)
        assert "capabilities" in choices


class TestPagination:
    """Verify we can limit and offset results on an endpoint."""

    def test_all_content_types_with_offset(self, nb_client):
        limit = 10
        offset = 5
        offset_cts = nb_client.extras.content_types.all(limit=limit, offset=offset)
        assert len(offset_cts) == limit

    def test_all_content_types_with_limit(self, nb_client):
        content_types = nb_client.extras.content_types.all()
        limited_cts = nb_client.extras.content_types.all(limit=10)
        assert len(content_types) == len(limited_cts)

    def test_filter_content_types_with_offset(self, nb_client):
        limit = 10
        offset = 5
        offset_cts = nb_client.extras.content_types.filter(app_label="dcim", limit=limit, offset=offset)
        assert len(offset_cts) == limit

    def test_filter_content_types_with_limit(self, nb_client):
        content_types = nb_client.extras.content_types.filter(app_label="dcim")
        limited_cts = nb_client.extras.content_types.filter(app_label="dcim", limit=10)
        assert len(content_types) == len(limited_cts)
