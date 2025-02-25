"""Extras tests. """

from unittest.mock import patch

from . import Generic, HEADERS
from .util import Response


class DynamicGroupTestCase(Generic.Tests):
    """DynamicGroup test."""

    app = "extras"
    name = "dynamic_groups"
    name_singular = "dynamic_group"

    @patch(
        "requests.sessions.Session.get",
        side_effect=[Response(fixture="extras/dynamic_group.json"), Response(fixture="extras/members.json")],
    )
    def test_get_members(self, mock):
        dg = self.endpoint.get(self.uuid)
        ret = dg.members.list()
        mock.assert_called_with(f"{self.detail_uri}members/", params={}, json=None, headers=HEADERS)
        self.assertTrue(ret)
        self.assertEqual(len(ret), 1)
        for record in ret:
            self.assertEqual(record.name, str(record))
