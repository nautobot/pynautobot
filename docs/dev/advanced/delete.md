# Deleting Multiple Objects

The `Deleting Records`{.interpreted-text role="ref"} section shows how
to use the `~pynautobot.core.response.Record.delete`{.interpreted-text
role="py:meth"} method to delete a single record. Another way to
accomplish this for multiple records at once is to use the
`~pynautobot.core.endpoint.Endpoint.delete`{.interpreted-text
role="py:meth"} method.

```python
>>> import os
>>> from pynautobot import api
>>>
>>> url = os.environ["NAUTOBOT_URL"]
>>> token = os.environ["NAUTOBOT_TOKEN
>>> nautobot = api(url=url, token=token)
>>>
>>> # Delete multiple devices by passing a list of UUIDs
>>> device_uuids = [
>>>     "a3e2f3e4-5b6c-4d5e-8f9a-1b2c3d4e5f6a",
>>>     "b3e2f3e4-5b6c-4d5e-8f9a-1b2c3d4e5f6b",
>>>     "c3e2f3e4-5b6c-4d5e-8f9a-1b2c3d4e5f6c",
>>> ]
>>> nautobot.dcim.devices.delete(device_uuids)
>>>
>>> # Delete all devices with a name starting with "Test"
>>> test_devices = nautobot.dcim.devices.filter(name__sw="Test")
>>> nautobot.dcim.devices.delete(test_devices)
```
