# Examples

This page provides for examples of how to use pynautobot from the community. What are some of the common use cases? Well here are just a few, including the support of additional applications to be installed on top of Nautobot.

=== "Accessing Job Results"

    ```python
    In [1]: import pynautobot

    In [2]: nautobot = pynautobot.api("https://demo.nautobot.com", token=nautobot_api_token)

    In [3]: jobs_results = getattr(nautobot.extras, "job-results")

    In [4]: jobs_results
    Out[4]: <pynautobot.core.endpoint.Endpoint at 0x1047929a0>

    In [5]: jobs_results.all()
    Out[5]:
    [plugins/nautobot_golden_config.jobs/AllGoldenConfig,
    plugins/nautobot_golden_config.jobs/AllGoldenConfig,
    DeviceConnectionsReport,
    VerifyPrimaryIP,
    VerifyPlatform,
    VerifyHostnames,
    VerifyHasRack,
    VerifyCircuitTermination,
    device lifecycle,
    device lifecycle,
    templates,
    templates,
    data,
    data,
    configs,
    configs,
    backups,
    backups,
    colo,
    colo,
    pops,
    pops,
    pops,
    pops,
    pops,
    pops,
    pops,
    pops,
    pops,
    pops,
    pops,
    pops,
    pops,
    pops,
    pops,
    pops,
    pops,
    pops,
    pops,
    pops,
    pops,
    pops,
    pops,
    pops,
    pops,
    pops,
    pops,
    pops,
    pops,
    pops,
    pops,
    pops,
    pops,
    pops,
    pops,
    devicetypes,
    devicetypes,
    circuits,
    manufacturers,
    regions,
    users]
    ```

=== "Access Application Endpoints"

    This demonstrates accessing the Device Lifecycle Management endpoints.

    ```
    import pynautobot

    nautobot = pynautobot.api(
        url="http://localhost:8000",
        token="d6f4e314a5b5fefd164995169f28ae32d987704f",
    )

    test = getattr(nautobot.plugins, "nautobot-device-lifecycle-mgmt")

    cves = test.cve.all()
    ```

=== "Assign IP address to interface"

    This is how to assign an IP address to an interface. We need to provide the id of the objects as parameters.

    ```python
    import pynautobot

    nautobot = pynautobot.api(
        url="http://localhost:8000/",
        token="d6f4e314a5b5fefd164995169f28ae32d987704f",
    )

    # Get the IP address object
    ip_address = nb.ipam.ip_addresses.get(address="192.0.2.1")

    # Get the interface object
    nb_interface = nb.dcim.interfaces.get(name="GigabitEthernet0/0", device=nb.dcim.devices.get(name="sample-rtr-01").id)

    # Assign IP to Interface
    ip_to_interface = nb.ipam.ip_address_to_interface.create(
        ip_address = ip_address.id,
        interface = nb_interface.id
    )
    ```
