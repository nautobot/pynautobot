"""Core and UI app integration tests."""

import pytest
from packaging import version


class TestRenderJinjaTemplate:
    """Verify rendering a Jinja template via the core and ui apps."""

    min_version = "2.4"
    template_code = "Hello {{ name }}"
    context = {"name": "world"}

    @pytest.fixture
    def skipif_version(self, nb_status):
        """Skip the test if the Nautobot version is less than the minimum version."""
        nautobot_version = nb_status.get("nautobot-version")
        if version.parse(nautobot_version) < version.parse(self.min_version):
            pytest.skip(f"render-jinja-template is only in Nautobot {self.min_version}+")

        return nautobot_version

    def test_core_render_jinja_template(self, skipif_version, nb_client):
        """Render a simple template via the core app."""
        assert skipif_version
        result = nb_client.core.render_jinja_template(template_code=self.template_code, context=self.context)
        assert result["rendered_template"] == "Hello world"

    def test_ui_render_jinja_template(self, skipif_version, nb_client):
        """Render a simple template via the ui app (ui/core/render-jinja-template/)."""
        assert skipif_version
        result = nb_client.ui.core.render_jinja_template(template_code=self.template_code, context=self.context)
        assert result["rendered_template"] == "Hello world"
