from pynautobot.core.response import Record


class TestApiDepth:
    """Test API Depth."""

    def test_api_depth_none(self, nb_client):
        """Verify default depth returns urls."""
        nb_client.api_depth = None
        rq = nb_client.ipam.prefixes.get(prefix="192.0.0.0/8")
        assert isinstance(rq.namespace, str) and "http" in rq.namespace

    def test_api_depth_one(self, nb_client):
        """Verify depth one returns Record object."""
        nb_client.api_depth = 1
        rq = nb_client.ipam.prefixes.get(prefix="192.0.0.0/8")
        assert isinstance(rq.namespace, Record) and rq.namespace.name == "Global"

    def test_api_depth_override(self, nb_client):
        """Verify depth can be overriden in individual request."""
        nb_client.api_depth = None
        rq = nb_client.ipam.prefixes.get(prefix="192.0.0.0/8", depth=1)
        assert isinstance(rq.namespace, Record) and rq.namespace.name == "Global"
