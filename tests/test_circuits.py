from unittest.mock import patch

from . import Generic
from .util import Response


class CircuitsTestCase(Generic.Tests):
    app = "circuits"
    name = "circuits"
    uuid = "5b1d5b48-67b7-4eb4-bc72-7623aa1da9b8"

    @patch("requests.sessions.Session.get", return_value=Response(fixture="circuits/circuit.json"))
    def test_repr(self, _):
        test = self.endpoint.get(self.uuid)
        self.assertEqual(str(test), "ntt-104265404093023273")


class ProviderTestCase(Generic.Tests):
    app = "circuits"
    name = "providers"


class CircuitTypeTestCase(Generic.Tests):
    app = "circuits"
    name = "circuit_types"


class CircuitTerminationsTestCase(Generic.Tests):
    app = "circuits"
    name = "circuit_terminations"

    @patch("requests.sessions.Session.get", return_value=Response(fixture="circuits/circuit_termination.json"))
    def test_repr(self, _):
        test = self.endpoint.get(self.uuid)
        self.assertEqual(str(test), "123456")
