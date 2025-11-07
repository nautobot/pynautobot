"""VPN tests."""

import pytest
from packaging import version


class TestVpnApp:
    """VPN test."""

    @pytest.fixture
    def skipif_version(self, nb_status):
        """Skip the test if the Nautobot version is less than 3.0."""
        nautobot_version = nb_status.get("nautobot-version")
        if version.parse(nautobot_version) < version.parse("3.0.0a0"):
            pytest.skip("VPN app is only in Nautobot 3.0+")

        return nautobot_version

    def test_vpn_phase_1_policy(self, skipif_version, nb_client):
        """Verify we can CRUD a VPN phase 1 policy."""
        assert skipif_version

        # Create
        vpn_phase_1_policy = nb_client.vpn.vpn_phase_1_policies.create(name="Test Phase 1 Policy")
        assert vpn_phase_1_policy

        # Read
        test_vpn_phase_1_policy = nb_client.vpn.vpn_phase_1_policies.get(name="Test Phase 1 Policy")
        assert test_vpn_phase_1_policy.name == "Test Phase 1 Policy"

        # Update
        test_vpn_phase_1_policy.description = "Updated Test Description"
        test_vpn_phase_1_policy.save()
        updated_vpn_phase_1_policy = nb_client.vpn.vpn_phase_1_policies.get(name="Test Phase 1 Policy")
        assert updated_vpn_phase_1_policy.description == "Updated Test Description"

        # Delete
        updated_vpn_phase_1_policy.delete()
        deleted_vpn_phase_1_policy = nb_client.vpn.vpn_phase_1_policies.get(name="Test Phase 1 Policy")
        assert not deleted_vpn_phase_1_policy

    def test_vpn_phase_2_policy(self, skipif_version, nb_client):
        """Verify we can CRUD a VPN phase 2 policy."""
        assert skipif_version

        # Create
        vpn_phase_2_policy = nb_client.vpn.vpn_phase_2_policies.create(name="Test Phase 2 Policy")
        assert vpn_phase_2_policy

        # Read
        test_vpn_phase_2_policy = nb_client.vpn.vpn_phase_2_policies.get(name="Test Phase 2 Policy")
        assert test_vpn_phase_2_policy.name == "Test Phase 2 Policy"

        # Update
        test_vpn_phase_2_policy.description = "Updated Test Description"
        test_vpn_phase_2_policy.save()
        updated_vpn_phase_2_policy = nb_client.vpn.vpn_phase_2_policies.get(name="Test Phase 2 Policy")
        assert updated_vpn_phase_2_policy.description == "Updated Test Description"

        # Delete
        updated_vpn_phase_2_policy.delete()
        deleted_vpn_phase_2_policy = nb_client.vpn.vpn_phase_2_policies.get(name="Test Phase 2 Policy")
        assert not deleted_vpn_phase_2_policy

    def test_vpn_profile(self, skipif_version, nb_client):
        """Verify we can CRUD a VPN profile."""
        assert skipif_version

        # Create
        phase_1_policy = nb_client.vpn.vpn_phase_1_policies.create(name="Test Phase 1 Policy")
        phase_2_policy = nb_client.vpn.vpn_phase_2_policies.create(name="Test Phase 2 Policy")
        vpn_profile = nb_client.vpn.vpn_profiles.create(
            name="Test Profile",
            vpn_phase1_policies=["Test Phase 1 Policy"],
            vpn_phase2_policies=["Test Phase 2 Policy"],
        )
        assert vpn_profile

        # Read
        test_vpn_profile = nb_client.vpn.vpn_profiles.get(name="Test Profile")
        assert test_vpn_profile.name == "Test Profile"

        # Update
        test_vpn_profile.name = "Updated Test Profile"
        test_vpn_profile.save()
        updated_vpn_profile = nb_client.vpn.vpn_profiles.get(name="Updated Test Profile")
        assert updated_vpn_profile.name == "Updated Test Profile"

        # Delete
        updated_vpn_profile.delete()
        deleted_vpn_profile = nb_client.vpn.vpn_profiles.get(name="Updated Test Profile")
        assert not deleted_vpn_profile

        # Cleanup
        phase_1_policy.delete()
        phase_2_policy.delete()
