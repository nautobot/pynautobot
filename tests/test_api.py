import unittest
from unittest.mock import patch

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
    @patch("requests.sessions.Session.post",)
    def test_get(self, *_):
        api = pynautobot.api(host, **def_kwargs)
        self.assertTrue(api)

    @patch("requests.sessions.Session.post",)
    def test_sanitize_url(self, *_):
        api = pynautobot.api("http://localhost:8000/", **def_kwargs)
        self.assertTrue(api)
        self.assertEqual(api.base_url, "http://localhost:8000/api")


class ApiVersionTestCase(unittest.TestCase):
    class ResponseHeadersWithVersion:
        headers = {"API-Version": "1.999"}
        ok = True

    @patch(
        "requests.sessions.Session.get", return_value=ResponseHeadersWithVersion(),
    )
    def test_api_version(self, *_):
        api = pynautobot.api(host,)
        self.assertEqual(api.version, "1.999")

    class ResponseHeadersWithoutVersion:
        headers = {}
        ok = True

    @patch(
        "requests.sessions.Session.get", return_value=ResponseHeadersWithoutVersion(),
    )
    def test_api_version_not_found(self, *_):
        api = pynautobot.api(host,)
        self.assertEqual(api.version, "")


class ApiStatusTestCase(unittest.TestCase):
    class ResponseWithStatus:
        ok = True

        def json(self):
            return {
                "nautobot-version": "1.3.2",
            }

    @patch(
        "requests.sessions.Session.get", return_value=ResponseWithStatus(),
    )
    def test_api_status(self, *_):
        api = pynautobot.api(host,)
        self.assertEqual(api.status()["nautobot-version"], "1.3.2")
