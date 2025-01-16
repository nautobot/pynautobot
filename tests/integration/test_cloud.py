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
            name="Test", provider="Dell", content_types=["cloud.cloudservice"], config_schema={"Foo": "Bar"}
        )
        assert cloud_resource_type

        # Confirm json field is retrievable
        assert cloud_resource_type.config_schema == {"Foo": "Bar"}

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

    def test_cloud_accounts(self, skipif_version, nb_client):
        """Verify we can CRUD a cloud account."""
        assert skipif_version

        # Create
        cloud_account = nb_client.cloud.cloud_accounts.create(name="TestAcct", provider="Dell", account_number="424242")
        assert cloud_account

        # Read
        test_cloud_account = nb_client.cloud.cloud_accounts.get(name="TestAcct")
        assert test_cloud_account.name == "TestAcct"

        # Update
        test_cloud_account.name = "Updated TestAcct"
        test_cloud_account.save()
        updated_cloud_account = nb_client.cloud.cloud_accounts.get(name="Updated TestAcct")
        assert updated_cloud_account.name == "Updated TestAcct"

        # Delete
        updated_cloud_account.delete()
        deleted_cloud_account = nb_client.cloud.cloud_accounts.get(name="Updated TestAcct")
        assert not deleted_cloud_account

    def test_cloud_services(self, skipif_version, nb_client):
        """Verify we can CRUD a cloud service."""
        assert skipif_version

        # Create
        cloud_resource_type = nb_client.cloud.cloud_resource_types.create(
            name="Test", provider="Dell", content_types=["cloud.cloudservice"]
        )
        cloud_account = nb_client.cloud.cloud_accounts.create(name="TestAcct", provider="Dell", account_number="424242")
        cloud_service = nb_client.cloud.cloud_services.create(
            name="TestService", cloud_resource_type="Test", cloud_account="TestAcct", extra_config={"Foo": "Bar"}
        )
        assert cloud_service

        # Confirm json field is retrievable
        assert cloud_service.extra_config == {"Foo": "Bar"}

        # Read
        test_cloud_service = nb_client.cloud.cloud_services.get(name="TestService")
        assert test_cloud_service.name == "TestService"

        # Update
        test_cloud_service.name = "Updated TestService"
        test_cloud_service.save()
        updated_cloud_service = nb_client.cloud.cloud_services.get(name="Updated TestService")
        assert updated_cloud_service.name == "Updated TestService"

        # Delete
        updated_cloud_service.delete()
        deleted_cloud_service = nb_client.cloud.cloud_services.get(name="Updated TestService")
        assert not deleted_cloud_service

        # Cleanup
        cloud_resource_type.delete()
        cloud_account.delete()

    def test_cloud_networks(self, skipif_version, nb_client):
        """Verify we can CRUD a cloud service."""
        assert skipif_version

        # Create
        cloud_resource_type = nb_client.cloud.cloud_resource_types.create(
            name="Test", provider="Dell", content_types=["cloud.cloudnetwork"]
        )
        cloud_account = nb_client.cloud.cloud_accounts.create(name="TestAcct", provider="Dell", account_number="424242")
        cloud_network = nb_client.cloud.cloud_networks.create(
            name="TestNetwork", cloud_resource_type="Test", cloud_account="TestAcct", extra_config={"Foo": "Bar"}
        )
        assert cloud_network

        # Confirm json field is retrievable
        assert cloud_network.extra_config == {"Foo": "Bar"}

        # Read
        test_cloud_network = nb_client.cloud.cloud_networks.get(name="TestNetwork")
        assert test_cloud_network.name == "TestNetwork"

        # Update
        test_cloud_network.name = "Updated TestNetwork"
        test_cloud_network.save()
        updated_cloud_network = nb_client.cloud.cloud_networks.get(name="Updated TestNetwork")
        assert updated_cloud_network.name == "Updated TestNetwork"

        # Delete
        updated_cloud_network.delete()
        deleted_cloud_network = nb_client.cloud.cloud_networks.get(name="Updated TestNetwork")
        assert not deleted_cloud_network

        # Cleanup
        cloud_resource_type.delete()
        cloud_account.delete()
