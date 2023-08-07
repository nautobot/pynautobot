import pytest
from packaging import version

from pynautobot.core.api import Api
from pynautobot.core.graphql import GraphQLQuery

DEFAULT_NETBOX_VERSIONS = "2.8, 2.9, 2.10"


def pytest_addoption(parser):
    """Hook on the pytest option parser setup.

    Add some extra options to the parser.
    """
    parser.addoption(
        "--netbox-versions",
        action="store",
        default=DEFAULT_NETBOX_VERSIONS,
        help=(
            "The versions of netbox to run integration tests against, as a"
            " comma-separated list. Default: %s" % DEFAULT_NETBOX_VERSIONS
        ),
    )

    parser.addoption(
        "--no-cleanup",
        dest="cleanup",
        action="store_false",
        help=(
            "Skip any cleanup steps after the pytest session finishes. Any containers"
            " created will be left running and the docker-compose files used to"
            " create them will be left on disk."
        ),
    )


def pytest_configure(config):
    """Hook that runs after test collection is completed.

    Here we can modify items in the collected tests or parser args.
    """
    # verify the netbox versions parse correctly and split them
    config.option.netbox_versions = [
        version.Version(version_string) for version_string in config.option.netbox_versions.split(",")
    ]


@pytest.fixture
def pynautobot_api(monkeypatch):
    """Factory to create pynautobot api instance."""
    monkeypatch.setattr("pynautobot.api.version", "1.999")
    return Api(url="https://mocknautobot.example.com", token="1234567890abcdefg")


@pytest.fixture
def graphql_test_class(pynautobot_api):
    """Factory to create test class to be used as base."""
    test_class = GraphQLQuery(pynautobot_api)
    return test_class
