import unittest
from unittest.mock import ANY, Mock, patch, call
from http.client import HTTPMessage

from pynautobot.core.query import RequestErrorFromException
import pynautobot

host = "http://localhost:8000"

def_kwargs = {
    "token": "abc123",
}

# Keys are app names, values are arbitrarily selected endpoints
# We use dcim and ipam since they have unique app classes
# and circuits because it does not. We don't add other apps/endpoints
# beyond 'circuits' as they all use the same code as each other
endpoints = {
    "dcim": "devices",
    "ipam": "prefixes",
    "circuits": "circuits",
}


class ApiTestCase(unittest.TestCase):
    @patch(
        "requests.sessions.Session.post",
    )
    def test_get(self, *_):
        api = pynautobot.api(host, **def_kwargs)
        self.assertTrue(api)

    @patch(
        "requests.sessions.Session.post",
    )
    def test_sanitize_url(self, *_):
        api = pynautobot.api("http://localhost:8000/", **def_kwargs)
        self.assertTrue(api)
        self.assertEqual(api.base_url, "http://localhost:8000/api")


class ApiVersionTestCase(unittest.TestCase):
    class ResponseHeadersWithVersion:
        headers = {"API-Version": "1.999"}
        ok = True

    @patch(
        "requests.sessions.Session.get",
        return_value=ResponseHeadersWithVersion(),
    )
    def test_api_version(self, *_):
        api = pynautobot.api(
            host,
        )
        self.assertEqual(api.version, "1.999")

    class ResponseHeadersWithoutVersion:
        headers = {}
        ok = True

    @patch(
        "requests.sessions.Session.get",
        return_value=ResponseHeadersWithoutVersion(),
    )
    def test_api_version_not_found(self, *_):
        api = pynautobot.api(
            host,
        )
        self.assertEqual(api.version, "")


class ApiStatusTestCase(unittest.TestCase):
    class ResponseWithStatus:
        ok = True

        def json(self):
            return {
                "nautobot-version": "1.3.2",
            }

    @patch(
        "requests.sessions.Session.get",
        return_value=ResponseWithStatus(),
    )
    def test_api_status(self, *_):
        api = pynautobot.api(
            host,
        )
        self.assertEqual(api.status()["nautobot-version"], "1.3.2")


class ApiRetryTestCase(unittest.TestCase):
    class ResponseWithStatus:
        ok = False
        status_code = 429

    @patch("urllib3.connectionpool.HTTPConnectionPool._get_conn")
    def test_api_retry(self, getconn_mock):
        getconn_mock.return_value.getresponse.side_effect = [
            Mock(status=500, msg=HTTPMessage()),
            Mock(status=429, msg=HTTPMessage()),
            Mock(status=200, msg=HTTPMessage()),
        ]

        api = pynautobot.api(
            "http://any.url/",
            retries=1,
        )

        api.version

        assert getconn_mock.return_value.request.mock_calls == [
            call("GET", "/api/", body=None, headers=ANY),
            call("GET", "/api/", body=None, headers=ANY),
            call("GET", "/api/", body=None, headers=ANY),
        ]

    @patch("urllib3.connectionpool.HTTPConnectionPool._get_conn")
    def test_api_retry_fails(self, getconn_mock):
        getconn_mock.return_value.getresponse.side_effect = [
            Mock(status=500, msg=HTTPMessage()),
            Mock(status=429, msg=HTTPMessage()),
            Mock(status=200, msg=HTTPMessage()),
        ]

        api = pynautobot.api(
            "http://any.url/",
            retries=1,
        )

        with self.assertRaises(RequestErrorFromException):
            api.version
