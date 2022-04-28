from . import Generic


class ClusterTypesTestCase(Generic.Tests):
    app = "virtualization"
    name = "cluster_types"


class ClusterGroupsTestCase(Generic.Tests):
    app = "virtualization"
    name = "cluster_groups"


class ClustersTestCase(Generic.Tests):
    app = "virtualization"
    name = "clusters"


class VirtualMachinesTestCase(Generic.Tests):
    app = "virtualization"
    name = "virtual_machines"


class InterfacesTestCase(Generic.Tests):
    app = "virtualization"
    name = "interfaces"
