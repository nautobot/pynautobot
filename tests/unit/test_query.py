"""Request tests."""

import unittest
from unittest.mock import Mock, call

from pynautobot.core.query import Request


class RequestTestCase(unittest.TestCase):
    """Request test cases."""

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
