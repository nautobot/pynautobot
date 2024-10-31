from packaging import version

import pytest


class TestCloudResourceType:
    @pytest.fixture
    def skipif_version(self, nb_client):
        """Retrieve the current Nautobot version and skip the test if less than 2.3."""
        status = nb_client.status()
        nautobot_version = status.get("nautobot-version")
        if version.parse(nautobot_version) < version.parse("2.3"):
            pytest.skip("Cloud resources are only in Nautobot 2.3+")

        return nautobot_version

    def test_cloud_resource_types(self, skipif_version, nb_client):
        """Verify we can CRUD a cloud resource type."""
        assert skipif_version

        # Create
        cloud_resource_type = nb_client.cloud.cloud_resource_types.create(
            name="Test", provider="Dell", content_types=["cloud.cloudservice"]
        )
        assert cloud_resource_type

        # Read
        test_cloud_resource_type = nb_client.cloud.cloud_resource_types.get(name="Test")
        assert test_cloud_resource_type.name == "Test"

        # Update
        test_cloud_resource_type.name = "Updated Test"
        test_cloud_resource_type.save()
        updated_cloud_resource_type = nb_client.cloud.cloud_resource_types.get(name="Updated Test")
        assert updated_cloud_resource_type.name == "Updated Test"

        # Delete
        updated_cloud_resource_type.delete()
        deleted_cloud_resource_type = nb_client.cloud.cloud_resource_types.get(name="Updated Test")
        assert not deleted_cloud_resource_type
