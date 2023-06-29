import pytest

from pynautobot.core.response import Record


class TestApiDepth:
    """Test API Depth."""

    @pytest.fixture
    def nb_client_depth(self, nb_client):
        """Implements teardown to restore api_depth."""
        yield nb_client
        nb_client.api_depth = 1

    def test_api_depth_none(self, nb_client_depth):
        """Verify default depth returns urls."""
        nb_client_depth.api_depth = None
        rq = nb_client_depth.ipam.prefixes.get(prefix="192.0.0.0/8")
        assert isinstance(rq.namespace, str) and "http" in rq.namespace

    def test_api_depth_one(self, nb_client_depth):
        """Verify depth one returns Record object."""
        nb_client_depth.api_depth = 1
        rq = nb_client_depth.ipam.prefixes.get(prefix="192.0.0.0/8")
        assert isinstance(rq.namespace, Record) and rq.namespace.name == "Global"

    def test_api_depth_override(self, nb_client_depth):
        """Verify depth can be overriden in individual request."""
        nb_client_depth.api_depth = None
        rq = nb_client_depth.ipam.prefixes.get(prefix="192.0.0.0/8", depth=1)
        assert isinstance(rq.namespace, Record) and rq.namespace.name == "Global"

    def test_api_depth_not_changed(self, nb_client):
        """Verify api_depth is still set to one."""
        assert nb_client.api_depth == 1
