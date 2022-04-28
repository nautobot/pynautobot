from . import Generic


class TenantsTestCase(Generic.Tests):
    app = "tenancy"
    name = "tenants"


class TenantGroupsTestCase(Generic.Tests):
    app = "tenancy"
    name = "tenant_groups"
