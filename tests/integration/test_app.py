"""App tests."""

import pytest
from packaging import version


class BaseAppTest:
    """Base test class for testing Nautobot apps."""

    app_name = None
    min_version = "2.0"

    @pytest.fixture
    def skipif_version(self, nb_status):
        """Retrieve the current Nautobot version and skip the test if less than the minimum version."""
        nautobot_version = nb_status.get("nautobot-version")
        if version.parse(nautobot_version) < version.parse(self.min_version):
            pytest.skip(f"{self.app_name} is only in Nautobot {self.min_version}+")

        return nautobot_version

    # pylint: disable=protected-access
    def test_app_get_api_endpoints(self, skipif_version, nb_client):
        """Validate the _get_api_endpoints method."""
        assert skipif_version
        app = getattr(nb_client, self.app_name)
        api_endpoints = app._get_api_endpoints()
        assert api_endpoints

        assert [f"/api/{self.app_name}/" in endpoint_url for endpoint_url in api_endpoints.values()]

    # pylint: disable=protected-access
    def test_app_dir(self, skipif_version, nb_client):
        """Validate the __dir__ method."""
        assert skipif_version
        app = getattr(nb_client, self.app_name)
        api_endpoints = app._get_api_endpoints()
        app_endpoints = [e.replace("-", "_") for e in api_endpoints.keys()]
        app_dir = dir(app)
        assert app_dir

        # Certain endpoints require additional parameters to be passed
        skip_endpoints = [
            ("dcim", "connected_device"),
            ("users", "config"),
        ]

        for endpoint_name in app_endpoints:
            assert endpoint_name in app_dir
            if (self.app_name, endpoint_name) in skip_endpoints:
                continue
            assert isinstance(getattr(app, endpoint_name).count(), int)


class TestCircuitsApp(BaseAppTest):
    """Test the circuits app."""

    app_name = "circuits"


class TestCloudApp(BaseAppTest):
    """Test the cloud app."""

    app_name = "cloud"
    min_version = "2.3"


class TestDataValidationApp(BaseAppTest):
    """Test the data validation app."""

    app_name = "data_validation"
    min_version = "3.0.0a1"


class TestDcimApp(BaseAppTest):
    """Test the dcim app."""

    app_name = "dcim"


class TestExtrasApp(BaseAppTest):
    """Test the extras app."""

    app_name = "extras"


class TestIpamApp(BaseAppTest):
    """Test the ipam app."""

    app_name = "ipam"


class TestLoadBalancersApp(BaseAppTest):
    """Test the load balancers app."""

    app_name = "load_balancers"
    min_version = "3.0.0a1"


class TestTenancyApp(BaseAppTest):
    """Test the tenancy app."""

    app_name = "tenancy"


class TestUsersApp(BaseAppTest):
    """Test the users app."""

    app_name = "users"


class TestVirtualizationApp(BaseAppTest):
    """Test the virtualization app."""

    app_name = "virtualization"


class TestVpnApp(BaseAppTest):
    """Test the vpn app."""

    app_name = "vpn"
    min_version = "3.0.0a1"


class TestWirelessApp(BaseAppTest):
    """Test the wireless app."""

    app_name = "wireless"
    min_version = "2.4"
