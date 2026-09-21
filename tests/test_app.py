"""App tests."""

import unittest
from unittest.mock import patch

import pynautobot

from .util import Response

HOST = "http://localhost:8000"

def_kwargs = {
    "token": "abc123",
}


class AppCustomFieldsTestCase(unittest.TestCase):
    """App custom fields test."""

    @patch(
        "requests.sessions.Session.get",
        return_value=Response(fixture="extras/custom_fields.json"),
    )
    @patch("pynautobot.api.version", "2.0")
    def test_custom_fields(self, session_get_mock):
        api = pynautobot.api(HOST, **def_kwargs)
        cfs = api.extras.get_custom_fields()

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

    @patch(
        "requests.sessions.Session.get",
        return_value=Response(fixture="extras/custom_fields.json"),
    )
    @patch("pynautobot.api.version", "2.0")
    def test_custom_fields_passes_filters(self, session_get_mock):
        api = pynautobot.api(HOST, **def_kwargs)
        api.extras.get_custom_fields(filters={"content_types": "dcim.device"})

        params = session_get_mock.call_args[1].get("params", {})
        self.assertEqual(params.get("content_types"), "dcim.device")


class AppCustomFieldChoicesTestCase(unittest.TestCase):
    """App custom field choices test."""

    @patch(
        "requests.sessions.Session.get",
        return_value=Response(fixture="extras/custom_field_choices.json"),
    )
    @patch("pynautobot.api.version", "2.0")
    def test_custom_field_choices(self, session_get_mock):
        api = pynautobot.api(HOST, **def_kwargs)
        choices = api.extras.get_custom_field_choices()

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

    @patch(
        "requests.sessions.Session.get",
        return_value=Response(fixture="extras/custom_field_choices.json"),
    )
    @patch("pynautobot.api.version", "2.0")
    def test_custom_field_choices_passes_filters(self, session_get_mock):
        api = pynautobot.api(HOST, **def_kwargs)
        api.extras.get_custom_field_choices(filters={"field": "test_custom_field_2"})

        params = session_get_mock.call_args[1].get("params", {})
        self.assertEqual(params.get("field"), "test_custom_field_2")


class AppConfigTestCase(unittest.TestCase):
    """App config test."""

    @patch(
        "pynautobot.core.query.Request.get",
        return_value={"tables": {"DeviceTable": {"columns": ["name", "status", "tenant", "tags"]}}},
    )
    @patch("pynautobot.api.version", "2.0")
    def test_config(self, *_):
        api = pynautobot.api(HOST, **def_kwargs)
        config = api.users.config()
        self.assertEqual(sorted(config.keys()), ["tables"])
        self.assertEqual(
            sorted(config["tables"]["DeviceTable"]["columns"]),
            ["name", "status", "tags", "tenant"],
        )


class AppExcludeM2MTestCase(unittest.TestCase):
    """App exclude m2m test."""

    @patch("pynautobot.api.version", "2.4")
    def test_exclude_m2m_true(self, *_):
        api = pynautobot.api(HOST, **def_kwargs, exclude_m2m=True)
        self.assertEqual(api.default_filters["exclude_m2m"], True)

    @patch("pynautobot.api.version", "2.4")
    def test_exclude_m2m_false(self, *_):
        api = pynautobot.api(HOST, **def_kwargs, exclude_m2m=False)
        self.assertEqual(api.default_filters["exclude_m2m"], False)

    @patch("pynautobot.api.version", "2.4")
    def test_exclude_m2m_none(self, *_):
        api = pynautobot.api(HOST, **def_kwargs)
        self.assertNotIn("exclude_m2m", api.default_filters.keys())


class AppIncludeFiltersTestCase(unittest.TestCase):
    """App include filters test."""

    @patch("pynautobot.api.version", "2.0")
    def test_include_none(self, *_):
        api = pynautobot.api(HOST, **def_kwargs)
        self.assertNotIn("include", api.default_filters.keys())

    @patch("pynautobot.api.version", "2.0")
    def test_include_config_context(self, *_):
        api = pynautobot.api(HOST, **def_kwargs, include_default="config_context")
        self.assertEqual(api.default_filters["include"], "config_context")

    @patch("pynautobot.api.version", "2.0")
    def test_include_multiple(self, *_):
        api = pynautobot.api(HOST, **def_kwargs, include_default="config_context,computed_fields")
        self.assertEqual(api.default_filters["include"], "config_context,computed_fields")


class RenderJinjaTemplateTestCase(unittest.TestCase):
    """Render Jinja template test for the core and ui apps."""

    template_code = "Hello {{ name }}"
    context = {"name": "world"}

    @patch(
        "requests.sessions.Session.post",
        return_value=Response(fixture="core/render_jinja_template.json"),
    )
    @patch("pynautobot.api.version", "2.0")
    def test_core_render_jinja_template(self, session_post_mock):
        api = pynautobot.api(HOST, **def_kwargs)
        result = api.core.render_jinja_template(template_code=self.template_code, context=self.context)

        session_post_mock.assert_called_once()
        expect_url = f"{api.base_url}/core/render-jinja-template/"
        url_passed_in_args = expect_url in session_post_mock.call_args[0]
        url_passed_in_kwargs = expect_url == session_post_mock.call_args[1].get("url")
        self.assertTrue(url_passed_in_args or url_passed_in_kwargs)

        body = session_post_mock.call_args[1].get("json")
        self.assertEqual(body, {"template_code": self.template_code, "context": self.context})

        self.assertIsInstance(result, dict)
        self.assertEqual(result["rendered_template"], "Hello world")

    @patch(
        "requests.sessions.Session.post",
        return_value=Response(fixture="core/render_jinja_template.json"),
    )
    @patch("pynautobot.api.version", "2.0")
    def test_ui_render_jinja_template(self, session_post_mock):
        api = pynautobot.api(HOST, **def_kwargs)
        result = api.ui.core.render_jinja_template(template_code=self.template_code, context=self.context)

        session_post_mock.assert_called_once()
        expect_url = f"{api.base_url}/ui/core/render-jinja-template/"
        url_passed_in_args = expect_url in session_post_mock.call_args[0]
        url_passed_in_kwargs = expect_url == session_post_mock.call_args[1].get("url")
        self.assertTrue(url_passed_in_args or url_passed_in_kwargs)

        body = session_post_mock.call_args[1].get("json")
        self.assertEqual(body, {"template_code": self.template_code, "context": self.context})

        self.assertIsInstance(result, dict)
        self.assertEqual(result["rendered_template"], "Hello world")

    @patch(
        "requests.sessions.Session.post",
        return_value=Response(fixture="core/render_jinja_template.json"),
    )
    @patch("pynautobot.api.version", "2.0")
    def test_render_jinja_template_defaults_empty_context(self, session_post_mock):
        api = pynautobot.api(HOST, **def_kwargs)
        api.core.render_jinja_template(template_code=self.template_code)

        body = session_post_mock.call_args[1].get("json")
        self.assertEqual(body, {"template_code": self.template_code, "context": {}})


class PluginAppCustomChoicesTestCase(unittest.TestCase):
    """Plugin app custom choices test."""

    @patch(
        "pynautobot.core.query.Request.get",
        return_value={"Testfield1": {"TF1_1": 1, "TF1_2": 2}, "Testfield2": {"TF2_1": 3, "TF2_2": 4}},
    )
    @patch("pynautobot.api.version", "2.0")
    def test_custom_fields(self, *_):
        api = pynautobot.api(HOST, **def_kwargs)
        custom_fields = api.plugins.test_plugin.get_custom_fields()
        self.assertEqual(len(custom_fields), 2)
        self.assertEqual(sorted(custom_fields.keys()), ["Testfield1", "Testfield2"])

    @patch(
        "pynautobot.core.query.Request.get",
        return_value=[{"name": "test_plugin", "package": "netbox_test_plugin"}],
    )
    @patch("pynautobot.api.version", "2.0")
    def test_installed_plugins(self, *_):
        api = pynautobot.api(HOST, **def_kwargs)
        plugins = api.plugins.installed_plugins()
        self.assertEqual(len(plugins), 1)
        self.assertEqual(plugins[0]["name"], "test_plugin")
