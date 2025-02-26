"""Virtualization tests."""

from . import Generic


class ClusterTypesTestCase(Generic.Tests):
    """ClusterTypes test."""

    app = "virtualization"
    name = "cluster_types"


class ClusterGroupsTestCase(Generic.Tests):
    """ClusterGroups test."""

    app = "virtualization"
    name = "cluster_groups"


class ClustersTestCase(Generic.Tests):
    """Clusters test."""

    app = "virtualization"
    name = "clusters"


class VirtualMachinesTestCase(Generic.Tests):
    """VirtualMachines test."""

    app = "virtualization"
    name = "virtual_machines"


class InterfacesTestCase(Generic.Tests):
    """Interfaces test."""

    app = "virtualization"
    name = "interfaces"
