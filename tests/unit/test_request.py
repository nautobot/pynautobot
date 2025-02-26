"""Request tests."""

import unittest
from unittest.mock import Mock

from pynautobot.core.query import Request


class RequestTestCase(unittest.TestCase):
    """Request test cases."""

    def test_get_openapi(self):
        test = Request("http://localhost:8080/api", Mock(), token="1234")
        test.get_openapi()
        test.http_session.get.assert_called_with(
            "http://localhost:8080/api/docs/?format=openapi",
            headers={"Content-Type": "application/json;", "Authorization": "Token 1234"},
        )
