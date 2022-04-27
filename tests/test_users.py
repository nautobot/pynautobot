from unittest.mock import patch

from . import Generic
from .util import Response


class UsersTestCase(Generic.Tests):
    app = "users"
    name = "users"

    @patch("requests.sessions.Session.get", return_value=Response(fixture="users/user.json"))
    def test_repr(self, _):
        test = self.endpoint.get(self.uuid)
        self.assertEqual(str(test), "user1")


class GroupsTestCase(Generic.Tests):
    app = "users"
    name = "groups"


class PermissionsTestCase(Generic.Tests):
    app = "users"
    name = "permissions"
