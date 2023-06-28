import unittest
from unittest.mock import Mock, call

from pynautobot.core.query import Request


class RequestTestCase(unittest.TestCase):
    def test_get_count(self):
        test_obj = Request(
            http_session=Mock(),
            base="http://localhost:8001/api/dcim/devices",
            filters={"q": "abcd"},
        )
        test_obj.http_session.get.return_value.json.return_value = {
            "count": 42,
            "next": "http://localhost:8001/api/dcim/devices?limit=1&offset=1&q=abcd",
            "previous": False,
            "results": [],
        }
        call(
            "http://localhost:8001/api/dcim/devices/",
            params={"q": "abcd", "limit": 1},
            headers={"accept": "application/json;"},
        )
        test_obj.http_session.get.ok = True
        test = test_obj.get_count()
        self.assertEqual(test, 42)
        test_obj.http_session.get.assert_called_with(
            "http://localhost:8001/api/dcim/devices/",
            params={"q": "abcd", "limit": 1},
            headers={"accept": "application/json;"},
            json=None,
        )

    def test_get_count_no_filters(self):
        test_obj = Request(
            http_session=Mock(),
            base="http://localhost:8001/api/dcim/devices",
        )
        test_obj.http_session.get.return_value.json.return_value = {
            "count": 42,
            "next": "http://localhost:8001/api/dcim/devices?limit=1&offset=1",
            "previous": False,
            "results": [],
        }
        test_obj.http_session.get.ok = True
        test = test_obj.get_count()
        self.assertEqual(test, 42)
        test_obj.http_session.get.assert_called_with(
            "http://localhost:8001/api/dcim/devices/",
            params={"limit": 1},
            headers={"accept": "application/json;"},
            json=None,
        )

    def test_get_api_depth_none(self):
        test_obj = Request(http_session=Mock(), base="http://localhost:8001/api", api_depth=None)
        self.assertEqual(test_obj.api_depth, None)
        test_obj.get()
        test_obj.http_session.get.assert_called_with(
            "http://localhost:8001/api/",
            params={},
            headers={"accept": "application/json;"},
            json=None,
        )

    def test_get_api_depth_value(self):
        test_obj = Request(http_session=Mock(), base="http://localhost:8001/api", api_depth=1)
        self.assertEqual(test_obj.api_depth, 1)
        test_obj.get()
        test_obj.http_session.get.assert_called_with(
            "http://localhost:8001/api/",
            headers={"accept": "application/json;"},
            params={},
            json=None,
        )

    def test_get_api_depth_value_override(self):
        test_obj = Request(http_session=Mock(), base="http://localhost:8001/api", api_depth=1)
        self.assertEqual(test_obj.api_depth, 1)
        test_obj.get(add_params={"depth": 0})
        test_obj.http_session.get.assert_called_with(
            "http://localhost:8001/api/",
            headers={"accept": "application/json;"},
            params={"depth": 0},
            json=None,
        )

    def test_get_api_depth_value_override_filters(self):
        test_obj = Request(http_session=Mock(), base="http://localhost:8001/api", api_depth=1)
        test_obj.filters = {"depth": 2}
        self.assertEqual(test_obj.filters, {"depth": 2})
        test_obj.get()
        test_obj.http_session.get.assert_called_with(
            "http://localhost:8001/api/",
            headers={"accept": "application/json;"},
            params={"depth": 2},
            json=None,
        )
