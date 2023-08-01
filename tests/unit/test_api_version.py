import unittest
from unittest.mock import patch, Mock

from pynautobot.core.endpoint import Endpoint


@patch("pynautobot.core.endpoint.response_loader")
class APIVersionTestCase(unittest.TestCase):
    def setUp(self):
        self.api = Mock(base_url="http://localhost:8000/api", api_version="1.3", name="API-Mock")
        self.api.token = 1234
        app = Mock(name="test")
        app.name = "test"
        self.test_obj = Endpoint(self.api, app, "test")

    def test_api_versioning_at_api_level(self, ResponseLoader):
        # Test get request includes version=1.3 in its headers
        self.test_obj.get(1)
        self.api.http_session.get.assert_called_with(
            "http://localhost:8000/api/test/test/1/",
            headers={"accept": "application/json; version=1.3", "authorization": "Token 1234"},
            params={},
            json=None,
        )

        # Test all request includes version=1.3 in its headers
        self.test_obj.all()
        self.api.http_session.get.assert_called_with(
            "http://localhost:8000/api/test/test/",
            headers={"accept": "application/json; version=1.3", "authorization": "Token 1234"},
            params={"limit": 0},
            json=None,
        )

        # Test filter request includes version=1.3 in its headers
        self.test_obj.filter(test="test")
        self.api.http_session.get.assert_called_with(
            "http://localhost:8000/api/test/test/",
            headers={"accept": "application/json; version=1.3", "authorization": "Token 1234"},
            params={"test": "test", "limit": 0},
            json=None,
        )

        # Test choices request includes version=1.3 in its headers
        self.api.http_session.options.return_value.json.return_value = {"actions": {"POST": []}}
        self.test_obj.choices()
        self.api.http_session.options.assert_called_with(
            "http://localhost:8000/api/test/test/",
            headers={"accept": "application/json; version=1.3", "authorization": "Token 1234"},
            params={},
            json=None,
        )

    def test_api_versioning_at_per_request_level(self, ResponseLoader):
        # Test get request overrides Api level versioning
        self.test_obj.get(1, api_version=1.2)
        self.api.http_session.get.assert_called_with(
            "http://localhost:8000/api/test/test/1/",
            headers={"accept": "application/json; version=1.2", "authorization": "Token 1234"},
            params={},
            json=None,
        )

        # Test all request overrides Api level versioning
        self.test_obj.all(api_version=1.2)
        self.api.http_session.get.assert_called_with(
            "http://localhost:8000/api/test/test/",
            headers={"accept": "application/json; version=1.2", "authorization": "Token 1234"},
            params={"limit": 0},
            json=None,
        )

        # Test filter request overrides Api level versioning
        self.test_obj.filter(test="test", api_version=1.2)
        self.api.http_session.get.assert_called_with(
            "http://localhost:8000/api/test/test/",
            headers={"accept": "application/json; version=1.2", "authorization": "Token 1234"},
            params={"test": "test", "limit": 0},
            json=None,
        )

        # Test choices request overrides Api level versioning
        self.api.http_session.options.return_value.json.return_value = {"actions": {"POST": []}}
        self.test_obj.choices(api_version=1.2)
        self.api.http_session.options.assert_called_with(
            "http://localhost:8000/api/test/test/",
            headers={"accept": "application/json; version=1.2", "authorization": "Token 1234"},
            params={},
            json=None,
        )
