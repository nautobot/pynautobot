import pytest


@pytest.mark.parametrize(
    "app_name",
    [
        "dcim",
        "ipam",
        "circuits",
        "virtualization",
        "tenancy",
        "extras",
    ],
)
def test_app_get_api_endpoints(nb_client, app_name):
    """Validate the _get_api_endpoints method of various apps."""
    app = getattr(nb_client, app_name)
    api_endpoints = app._get_api_endpoints()
    assert api_endpoints

    assert [f"/api/{app_name}/" in endpoint_url for endpoint_url in api_endpoints.values()]


@pytest.mark.parametrize(
    "app_name",
    [
        "dcim",
        "ipam",
        "circuits",
        "virtualization",
        "tenancy",
        "extras",
    ],
)
def test_app_dir(nb_client, app_name):
    """Validate the __dir__ method of various apps."""
    app = getattr(nb_client, app_name)
    api_endpoints = app._get_api_endpoints()
    app_endpoints = [e.replace("-", "_") for e in api_endpoints.keys()]
    app_dir = dir(app)
    assert app_dir

    for endpoint_name in app_endpoints:
        print(endpoint_name)
        assert endpoint_name in app_dir
        if endpoint_name in ["connected_device"]:
            # Certain endpoints require additional parameters to be passed
            continue
        assert isinstance(getattr(app, endpoint_name).count(), int)
