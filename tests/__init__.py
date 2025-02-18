"""Test initialization file."""
import unittest
from unittest.mock import patch

import pynautobot

from .util import Response

with patch("pynautobot.api.version", "2.0"):
    api = pynautobot.api(
        "http://localhost:8000",
        token="abc123",
    )

HEADERS = {
    "accept": "application/json;",
    "authorization": "Token abc123",
}

POST_HEADERS = {
    "Content-Type": "application/json;",
    "authorization": "Token abc123",
}


class Generic:  # pylint: disable=too-few-public-methods
    """Generic test class."""
    class Tests(unittest.TestCase):
        """Generic tests."""
        ret = pynautobot.core.response.Record

        app = ""  # to be set by subclasses
        name = ""  # to be set by subclasses
        name_singular = ""  # to be optionally set by subclasses
        uuid = "5b39ba88-e5ab-4be2-89f5-5a016473b53c"

        @property
        def bulk_uri(self):
            """Return the URI for the bulk endpoint."""
            return f"http://localhost:8000/api/{self.app}/{self.name.replace('_', '-')}/"

        @property
        def detail_uri(self):
            """Return the URI for the detail endpoint."""
            return f"http://localhost:8000/api/{self.app}/{self.name.replace('_', '-')}/{self.uuid}/"

        def setUp(self):
            self.nb = getattr(api, self.app)
            self.endpoint = getattr(self.nb, self.name)
            if not self.name_singular:
                self.name_singular = self.name[:-1]

        #
        # Generic test cases for the given app/name
        #

        def test_get_all(self):
            with patch(
                "requests.sessions.Session.get",
                return_value=Response(fixture=f"{self.app}/{self.name}.json"),
            ) as mock:
                ret = self.endpoint.all()
                self.assertIsInstance(ret, list)
                self.assertIsInstance(ret[0], self.ret)
                mock.assert_called_with(self.bulk_uri, params={}, json=None, headers=HEADERS)

        def test_filter(self):
            with patch(
                "requests.sessions.Session.get",
                return_value=Response(fixture=f"{self.app}/{self.name}.json"),
            ) as mock:
                ret = self.endpoint.filter(name="test")
                self.assertIsInstance(ret, list)
                self.assertIsInstance(ret[0], self.ret)
                mock.assert_called_with(self.bulk_uri, params={"name": "test"}, json=None, headers=HEADERS)

        def test_get(self):
            with patch(
                "requests.sessions.Session.get",
                return_value=Response(fixture=f"{self.app}/{self.name_singular}.json"),
            ) as mock:
                ret = self.endpoint.get(self.uuid)
                self.assertIsInstance(ret, self.ret)
                self.assertEqual(ret.id, self.uuid)
                self.assertIsInstance(str(ret), str)
                self.assertIsInstance(dict(ret), dict)
                mock.assert_called_with(self.detail_uri, params={}, json=None, headers=HEADERS)

        def test_delete(self):
            with patch(
                "requests.sessions.Session.get",
                return_value=Response(fixture=f"{self.app}/{self.name_singular}.json"),
            ) as mock, patch("requests.sessions.Session.delete") as delete:
                ret = self.endpoint.get(self.uuid)
                # get() was already tested more thoroughly above, not repeated here
                self.assertTrue(ret.delete())
                mock.assert_called_with(self.detail_uri, params={}, json=None, headers=HEADERS)
                delete.assert_called_with(self.detail_uri, params={}, json=None, headers=HEADERS)

        def test_endpoint_update(self):
            """Tests that calling Endpoint.update(id=x, data={...}) will result in an HTTP PATCH"""
            with patch(
                "requests.sessions.Session.patch",
                return_value=Response(fixture=f"{self.app}/{self.name_singular}.json"),
            ) as mock:
                update_data = {"field1": "value1"}
                ret = self.endpoint.update(id=self.uuid, data=update_data)
                self.assertTrue(ret)
                mock.assert_called_with(self.detail_uri, params={}, json=update_data, headers=HEADERS)

        def test_diff(self):
            with patch(
                "requests.sessions.Session.get",
                return_value=Response(fixture=f"{self.app}/{self.name_singular}.json"),
            ):
                ret = self.endpoint.get(self.uuid)
                self.assertTrue(ret)
                self.assertEqual(ret._diff(), set())  # pylint: disable=protected-access

        def test_serialize(self):
            with patch(
                "requests.sessions.Session.get",
                return_value=Response(fixture=f"{self.app}/{self.name_singular}.json"),
            ):
                ret = self.endpoint.get(self.uuid)
                self.assertTrue(ret)
                self.assertTrue(ret.serialize())
