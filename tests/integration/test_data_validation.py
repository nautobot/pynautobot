"""Data validation tests."""

import pytest
from packaging import version


class TestDataValidationApp:
    """Data validation test."""

    @pytest.fixture
    def skipif_version(self, nb_status):
        """Skip the test if the Nautobot version is less than 3.0."""
        nautobot_version = nb_status.get("nautobot-version")
        if version.parse(nautobot_version) < version.parse("3.0.0a0"):
            pytest.skip("Data validation app is only in Nautobot 3.0+")

        return nautobot_version

    def test_required_rules(self, skipif_version, nb_client):
        """Verify we can CRUD a required rule."""
        assert skipif_version

        # Create
        required_rule = nb_client.data_validation.required_rules.create(
            name="Test Required Device Serial Rule",
            content_type="dcim.device",
            field="serial",
        )
        assert required_rule

        # Read
        test_required_rule = nb_client.data_validation.required_rules.get(name="Test Required Device Serial Rule")
        assert test_required_rule.name == "Test Required Device Serial Rule"

        # Update
        test_required_rule.name = "Updated Test Required Device Serial Rule"
        test_required_rule.save()
        updated_required_rule = nb_client.data_validation.required_rules.get(
            name="Updated Test Required Device Serial Rule"
        )
        assert updated_required_rule.name == "Updated Test Required Device Serial Rule"

        # Delete
        test_required_rule.delete()
        deleted_required_rule = nb_client.data_validation.required_rules.get(
            name="Updated Test Required Device Serial Rule"
        )
        assert not deleted_required_rule

    def test_min_max_rules(self, skipif_version, nb_client):
        """Verify we can CRUD a min max rule."""
        assert skipif_version

        # Create
        min_max_rule = nb_client.data_validation.min_max_rules.create(
            name="Test Min Max Rule",
            content_type="dcim.rack",
            field="u_height",
            min=42,
            max=48,
        )
        assert min_max_rule

        # Read
        test_min_max_rule = nb_client.data_validation.min_max_rules.get(name="Test Min Max Rule")
        assert test_min_max_rule.min == 42
        assert test_min_max_rule.max == 48

        # Update
        test_min_max_rule.min = 40
        test_min_max_rule.save()
        updated_min_max_rule = nb_client.data_validation.min_max_rules.get(name="Test Min Max Rule")
        assert updated_min_max_rule.min == 40

        # Delete
        test_min_max_rule.delete()
        deleted_min_max_rule = nb_client.data_validation.min_max_rules.get(name="Updated Test Min Max Rule")
        assert not deleted_min_max_rule

    def test_regex_rules(self, skipif_version, nb_client):
        """Verify we can CRUD a regex rule."""
        assert skipif_version

        # Create
        regex_rule = nb_client.data_validation.regex_rules.create(
            name="Test Regex Rule",
            content_type="dcim.device",
            field="serial",
            regular_expression="^[A-Z0-9]{10}$",
        )
        assert regex_rule

        # Read
        test_regex_rule = nb_client.data_validation.regex_rules.get(name="Test Regex Rule")
        assert test_regex_rule.regular_expression == "^[A-Z0-9]{10}$"

        # Update
        test_regex_rule.regular_expression = "^[A-Z0-9]{12}$"
        test_regex_rule.save()
        updated_regex_rule = nb_client.data_validation.regex_rules.get(name="Test Regex Rule")
        assert updated_regex_rule.regular_expression == "^[A-Z0-9]{12}$"

        # Delete
        test_regex_rule.delete()
        deleted_regex_rule = nb_client.data_validation.regex_rules.get(name="Test Regex Rule")
        assert not deleted_regex_rule

    def test_unique_rules(self, skipif_version, nb_client):
        """Verify we can CRUD a unique rule."""
        assert skipif_version

        # Create
        unique_rule = nb_client.data_validation.unique_rules.create(
            name="Test Unique Rule",
            content_type="dcim.location",
            field="asn",
        )
        assert unique_rule

        # Read
        test_unique_rule = nb_client.data_validation.unique_rules.get(name="Test Unique Rule")
        assert test_unique_rule.field == "asn"

        # Update
        test_unique_rule.field = "facility"
        test_unique_rule.save()
        updated_unique_rule = nb_client.data_validation.unique_rules.get(name="Test Unique Rule")
        assert updated_unique_rule.field == "facility"

        # Delete
        test_unique_rule.delete()
        deleted_unique_rule = nb_client.data_validation.unique_rules.get(name="Test Unique Rule")
        assert not deleted_unique_rule
