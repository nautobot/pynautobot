# Accessing Nautobot Apps

Nautobot allows for the expansion of the core application with the support of additional applications to be installed on top of Nautobot. To that, the SDK should support this capability. A couple of examples include accessing job results or the applications.

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