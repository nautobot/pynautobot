import pytest
import pynautobot


class TestAPIVersioning:
    """Verify Invalid api_version error response from Nautobot is handled gracefully."""

    def test_invalid_api_version(self, nb_client):
        with pytest.raises(pynautobot.core.query.RequestError) as _:
            nb_client.extras.tags.all(api_version="0.0")
