# v1.5.0

## Added

- (#125) Adds Update Method based on ID to keep within the pynautobot experience to update a device (@jamesharr)

```python
    import os
    from pynautobot import api
    url = os.environ["NAUTOBOT_URL"]
    token = os.environ["NAUTOBOT_TOKEN"]
    nautobot = api(url=url, token=token)
    # Update status and name fields
    result = nautobot.dcim.devices.update(
      id="491d799a-eeee-bbbb-aaaa-7c5cbb5b71b6",
      data={
        "comments": "removed from service",
        "status": "decommissioned",
      },
    )
```