import pytest


class TestCustomField:

    """Verify we can create, custom field, and custom field choices."""

    @pytest.fixture(scope="session")
    def create_custom_field(self, nb_client):
        data = {
            "name": "test_cf",
            "slug": "test_cf",
            "content_types": ["dcim.device"],
            "type": "select",
            "weight": 100,
            "filter_logic": "loose",
        }
        return nb_client.extras.custom_fields.create(**data)

    @pytest.fixture(scope="session")
    def create_custom_field_choices(self, nb_client, create_custom_field):
        data = {
            "value": "A",
            "field": create_custom_field["id"],
            "weight": 100,
        }
        return nb_client.extras.custom_field_choices.create(**data)

    def test_custom_field(self, create_custom_field):
        assert create_custom_field["name"] == "test_cf"

    def test_custom_field_choice_value(self, create_custom_field_choices):
        assert create_custom_field_choices["value"] == "A"

    def test_custom_field_choice_to_cf(self, create_custom_field_choices, create_custom_field):
        assert create_custom_field_choices["field"]["id"] == create_custom_field["id"]
