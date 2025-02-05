import os

import yaml

import subprocess as subp
import pynautobot
import pytest
import requests


DOCKER_PROJECT_PREFIX = "pytest_pynautobot"
DEVICETYPE_LIBRARY_OBJECTS = [
    "A10/TH6430.yaml",
    "APC/AP8868.yaml",
    "Arista/DCS-7010T-48.yaml",
    "Arista/DCS-7050TX3-48C8.yaml",
    "Arista/DCS-7280CR3-32P4.yaml",
    "Arista/DCS-7280SR-48C6.yaml",
    "Dell/Networking_S4048-ON.yaml",
    "Dell/PowerEdge_R640.yaml",
    "Generic/48-port_copper_patch_panel.yaml",
    "Generic/LC-48-port_fiber_patch_panel.yaml",
    "Opengear/IM7248-2-DAC-US.yaml",
]
DEVICE_ROLE_NAMES = [
    "Border Leaf Switch",
    "Console Server",
    "Leaf Switch",
    "PDU",
    "Patch Panel",
    "Server",
    "Spine Switch",
]
PARENT_PREFIXES = [
    "192.0.0.0/8",
]

# When running tests locally `export NAUTOBOT_URL="http://localhost:8000"` (or wherever Nautobot runs) to override the default
_NAUTOBOT_URL = os.getenv("NAUTOBOT_URL", "http://nautobot:8000")


@pytest.fixture(scope="session")
def git_toplevel():
    """Get the top level of the current git repo.

    Returns:
        str: The path of the top level directory of the current git repo.

    """
    return subp.check_output(["git", "rev-parse", "--show-toplevel"]).decode("utf-8").splitlines()[0]


@pytest.fixture(scope="session")
def devicetype_library_repo_dirpath(git_toplevel):
    """Get the path to the devicetype-library repo we will use.

    Returns:
        str: The path of the directory of the devicetype-library repo we will use.
    """
    repo_fpath = os.path.join(git_toplevel, ".devicetype-library")
    if os.path.isdir(repo_fpath):
        subp.check_call(["git", "fetch"], cwd=repo_fpath, stdout=subp.PIPE, stderr=subp.PIPE)
    else:
        subp.check_call(
            ["git", "clone", "https://github.com/netbox-community/devicetype-library", repo_fpath],
            cwd=git_toplevel,
            stdout=subp.PIPE,
            stderr=subp.PIPE,
        )

    # Checkout to a commit hash that is compatibility with pynautobot
    subp.check_call(
        ["git", "checkout", "9ead65a5b9b400ea601c245eb6505b496dedc1fa"],
        cwd=repo_fpath,
        stdout=subp.PIPE,
        stderr=subp.PIPE,
    )

    return repo_fpath


def nautobot_is_responsive(url):
    """Chack if the HTTP service is up and responsive."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
    except ConnectionError:
        return False


def populate_nautobot_object_types(nb_api, devicetype_library_repo_dirpath):
    """Load some object types in to a fresh instance of nautobot.

    These objects will be used in tests.
    """
    # collect and load the configs for each of the requested object models
    device_type_models = []
    for object_model_relfpath in DEVICETYPE_LIBRARY_OBJECTS:
        device_type_models.append(
            yaml.safe_load(
                open(
                    os.path.join(
                        devicetype_library_repo_dirpath,
                        "device-types",
                        object_model_relfpath,
                    ),
                    "r",
                ).read()
            )
        )

    # create the manufacturers
    manufacturer_names = {model["manufacturer"] for model in device_type_models}
    for manufacturer_name in manufacturer_names:
        nb_api.dcim.manufacturers.create(name=manufacturer_name)

    # create the device types and their components
    for device_type_model in device_type_models:
        device_type_model["manufacturer"] = {"name": device_type_model["manufacturer"]}
        device_type = nb_api.dcim.device_types.create(**device_type_model)

        for interface_template in device_type_model.get("interfaces", []):
            nb_api.dcim.interface_templates.create(device_type=device_type.id, **interface_template)

        for front_port_template in device_type_model.get("front_ports", []):
            nb_api.dcim.front_port_templates.create(device_type=device_type.id, **front_port_template)

        for rear_port_template in device_type_model.get("rear_ports", []):
            nb_api.dcim.rear_port_templates.create(device_type=device_type.id, **rear_port_template)

        for console_port_template in device_type_model.get("console-ports", []):
            nb_api.dcim.console_port_templates.create(device_type=device_type.id, **console_port_template)

        for console_server_port_template in device_type_model.get("console-server-ports", []):
            nb_api.dcim.console_server_port_templates.create(device_type=device_type.id, **console_server_port_template)

        for power_port_template in device_type_model.get("power-ports", []):
            nb_api.dcim.power_port_templates.create(device_type=device_type.id, **power_port_template)

        for power_outlet_template in device_type_model.get("power-outlets", []):
            if "power_port" in power_outlet_template:
                power_outlet_template["power_port"] = {"name": power_outlet_template["power_port"]}
            nb_api.dcim.power_outlet_templates.create(device_type=device_type.id, **power_outlet_template)

        for device_bay_template in device_type_model.get("device-bays", []):
            nb_api.dcim.device_bay_templates.create(device_type=device_type.id, **device_bay_template)

    # add device roles
    for device_role_name in DEVICE_ROLE_NAMES:
        nb_api.extras.roles.create(name=device_role_name, content_types=["dcim.device"])

    # add parent prefix
    for parent_prefix in PARENT_PREFIXES:
        nb_api.ipam.prefixes.create(prefix=parent_prefix, namespace={"name": "Global"}, status={"name": "Active"})


@pytest.fixture(scope="session")
def nb_client(devicetype_library_repo_dirpath):
    """Setup the nb_client and import necessary data."""

    nb_api = pynautobot.api(_NAUTOBOT_URL, token="0123456789abcdef0123456789abcdef01234567")
    populate_nautobot_object_types(nb_api=nb_api, devicetype_library_repo_dirpath=devicetype_library_repo_dirpath)

    return nb_api


@pytest.fixture(scope="session")
def nb_status(nb_client):
    """Cache the status of the Nautobot instance as fixture so we don't have to call it repeatedly."""
    status = nb_client.status()
    assert status
    # Assert that the nautobot-version key is present since we use it to conditionally skip some tests
    assert status.get("nautobot-version")
    return status
