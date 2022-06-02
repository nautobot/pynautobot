import inspect
import json
import pytest
import requests_mock
import unittest
from unittest.mock import patch, Mock

from pynautobot.core.endpoint import Endpoint
from pynautobot.core.query import RequestError
from pynautobot.core.response import Record
from pynautobot.models.dcim import Devices
from pynautobot.models.ipam import Prefixes


class EndPointTestCase(unittest.TestCase):
    def test_filter(self):
        with patch("pynautobot.core.query.Request.get", return_value=Mock()) as mock:
            api = Mock(base_url="http://localhost:8000/api")
            app = Mock(name="test")
            mock.return_value = [{"id": 123}, {"id": 321}]
            test_obj = Endpoint(api, app, "test")
            test = test_obj.filter(test="test")
            self.assertEqual(len(test), 2)

    def test_filter_empty_kwargs(self):

        api = Mock(base_url="http://localhost:8000/api")
        app = Mock(name="test")
        test_obj = Endpoint(api, app, "test")
        with self.assertRaises(ValueError) as _:
            test_obj.filter()

    def test_filter_reserved_kwargs(self):

        api = Mock(base_url="http://localhost:8000/api")
        app = Mock(name="test")
        test_obj = Endpoint(api, app, "test")
        with self.assertRaises(ValueError) as _:
            test_obj.filter(id=1)

    def test_choices(self):
        with patch("pynautobot.core.query.Request.options", return_value=Mock()) as mock:
            api = Mock(base_url="http://localhost:8000/api")
            app = Mock(name="test")
            mock.return_value = {
                "actions": {
                    "POST": {
                        "letter": {
                            "choices": [
                                {"display_name": "A", "value": 1},
                                {"display_name": "B", "value": 2},
                                {"display_name": "C", "value": 3},
                            ]
                        }
                    }
                }
            }
            test_obj = Endpoint(api, app, "test")
            choices = test_obj.choices()
            self.assertEqual(choices["letter"][1]["display_name"], "B")
            self.assertEqual(choices["letter"][1]["value"], 2)


DISPLAY_FIELD_RECORD_TESTS = [
    ("circuits", "circuits", "circuits/circuits.json", "cid", Record),
    ("circuits", "circuit_terminations", "circuits/circuit_terminations.json", "circuit.cid", Record),
    ("dcim", "devices", "dcim/devices.json", "display", Devices),
    ("ipam", "prefixes", "ipam/prefixes.json", "display", Prefixes),
]


@pytest.mark.parametrize("app,endpoint,fixture,field,record", DISPLAY_FIELD_RECORD_TESTS)
def test_record_string_method_returns_valid_value(pynautobot_api, app, endpoint, fixture, field, record):
    app = getattr(pynautobot_api, app)
    ep = getattr(app, endpoint)

    # Load in the fixture data to be mocked
    with open(f"tests/fixtures/{fixture}") as data:
        response = json.loads(data.read())

    # Gather all endpoint records with mocked data
    with requests_mock.Mocker() as mock_resp:
        mock_resp.register_uri("GET", f"{ep.url}/", json=response)
        all_records = ep.all()

    # Iterate over records and assert string methods return correctly
    for rec in all_records:
        # Validate the specified field is available on the object
        # It will attempt to make a requests call, but we catch the exception and fail
        try:
            parent, *children = field.split(".")
            field_value = getattr(rec, parent)

            # We need to iterate to the end of children to get the field_value for the string assertion
            if field_value and children:
                while children:
                    child_field = children.pop(0)
                    field_value = getattr(field_value, child_field)
        except RequestError:
            assert False, f"{field} is missing for {rec.id}. Check mock data or __str__ method on {record}."

        # Assert the stringified version of the record matches the result from the correct attribute
        assert field_value == str(rec)

        # Validate correct sub records existing that are defined on custom pynautobot models
        sub_records = {attr for attr in inspect.getmembers(record, inspect.isclass) if not attr[0] == "__class__"}
        if sub_records:
            assert all(
                [
                    sub_rec
                    for sub_rec in sub_records
                    if not isinstance(getattr(rec, sub_rec[0]), list)
                    and isinstance(getattr(rec, sub_rec[0]), sub_rec[1])
                ]
            )
