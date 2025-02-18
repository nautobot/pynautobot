"""Tenancy tests."""
from . import Generic


class TenantsTestCase(Generic.Tests):
    """Tenants test."""
    app = "tenancy"
    name = "tenants"


class TenantGroupsTestCase(Generic.Tests):
    """TenantGroups test."""
    app = "tenancy"
    name = "tenant_groups"
