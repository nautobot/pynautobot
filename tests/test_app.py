import unittest
from unittest.mock import patch

import pynautobot

from .util import Response

host = "http://localhost:8000"

def_kwargs = {
    "token": "abc123",
}


class AppCustomFieldsTestCase(unittest.TestCase):
    @patch(
        "requests.sessions.Session.get",
        return_value=Response(fixture="extras/custom_fields.json"),
    )
    @patch("pynautobot.api.version", "2.0")
    def test_custom_fields(self, session_get_mock):
        api = pynautobot.api(host, **def_kwargs)
        cfs = api.extras.custom_fields()

        session_get_mock.assert_called_once()
        expect_url = f"{api.base_url}/extras/custom-fields/"
        self.assertGreaterEqual(len(session_get_mock.call_args), 2)
        url_passed_in_args = expect_url in session_get_mock.call_args[0]
        url_passed_in_kwargs = expect_url == session_get_mock.call_args[1].get("url")
        self.assertTrue(url_passed_in_args or url_passed_in_kwargs)

        self.assertIsInstance(cfs, list)
        self.assertEqual(len(cfs), 2)
        for field in cfs:
            self.assertIsInstance(field.get("name"), str)
            self.assertIsInstance(field.get("content_types"), list)
            self.assertIsInstance(field.get("slug"), str)
            self.assertIn("type", field)


class AppCustomFieldChoicesTestCase(unittest.TestCase):
    @patch(
        "requests.sessions.Session.get",
        return_value=Response(fixture="extras/custom_field_choices.json"),
    )
    @patch("pynautobot.api.version", "2.0")
    def test_custom_field_choices(self, session_get_mock):
        api = pynautobot.api(host, **def_kwargs)
        choices = api.extras.custom_field_choices()

        session_get_mock.assert_called_once()
        expect_url = f"{api.base_url}/extras/custom-field-choices/"
        self.assertGreaterEqual(len(session_get_mock.call_args), 2)
        url_passed_in_args = expect_url in session_get_mock.call_args[0]
        url_passed_in_kwargs = expect_url == session_get_mock.call_args[1].get("url")
        self.assertTrue(url_passed_in_args or url_passed_in_kwargs)

        self.assertIsInstance(choices, list)
        self.assertEqual(len(choices), 3)
        for choice in choices:
            self.assertIsInstance(choice.get("field"), dict)
            self.assertIsInstance(choice.get("value"), str)
            self.assertIn(choice.get("value"), ("First option", "Second option", "Third option"))


class AppConfigTestCase(unittest.TestCase):
    @patch(
        "pynautobot.core.query.Request.get",
        return_value={"tables": {"DeviceTable": {"columns": ["name", "status", "tenant", "tags"]}}},
    )
    @patch("pynautobot.api.version", "2.0")
    def test_config(self, *_):
        api = pynautobot.api(host, **def_kwargs)
        config = api.users.config()
        self.assertEqual(sorted(config.keys()), ["tables"])
        self.assertEqual(
            sorted(config["tables"]["DeviceTable"]["columns"]),
            ["name", "status", "tags", "tenant"],
        )


class PluginAppCustomChoicesTestCase(unittest.TestCase):
    @patch(
        "pynautobot.core.query.Request.get",
        return_value={"Testfield1": {"TF1_1": 1, "TF1_2": 2}, "Testfield2": {"TF2_1": 3, "TF2_2": 4}},
    )
    @patch("pynautobot.api.version", "2.0")
    def test_custom_choices(self, *_):
        api = pynautobot.api(host, **def_kwargs)
        choices = api.plugins.test_plugin.custom_fields()
        self.assertEqual(len(choices), 2)
        self.assertEqual(sorted(choices.keys()), ["Testfield1", "Testfield2"])

    @patch(
        "pynautobot.core.query.Request.get",
        return_value=[{"name": "test_plugin", "package": "netbox_test_plugin"}],
    )
    @patch("pynautobot.api.version", "2.0")
    def test_installed_plugins(self, *_):
        api = pynautobot.api(host, **def_kwargs)
        plugins = api.plugins.installed_plugins()
        self.assertEqual(len(plugins), 1)
        self.assertEqual(plugins[0]["name"], "test_plugin")
