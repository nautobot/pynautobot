# Interacting With A Record

We already know that we can access attributes on the record, but what
else can we do?

## NAPALM

You\'re able to run the normal NAPALM integrations as long as all the
prerequisites are taken care of.

Here we can run the `get_facts` getter.

```python
>>> device1.napalm.list(method='get_facts')
{"get_facts": {"interface_list": ["ge-0/0/0"]}}
```

## Accessing Field Data

### Serialize

Instead of accessing the device and only receiving the name, you can use
the
`serialize()<pynautobot.core.response.Record.serialize>`{.interpreted-text
role="py:meth"} to view a near dictionary like structure.

```python
>>> import json
>>> print(json.dumps(device1.serialize(), indent=4))
{
    "id": "86924375-4b50-4f95-a1c7-99896ab03307",
    "object_type": "dcim.device",
    "display": "hq-access-01",
    "url": "http://nautobot:8080/api/dcim/devices/86924375-4b50-4f95-a1c7-99896ab03307/",
    "natural_slug": "hq-access-01__hq_8692",
    "face": null,
    "local_config_context_data": null,
    "local_config_context_data_owner_object_id": null,
    "name": "hq-access-01",
    "serial": "",
    "asset_tag": null,
    "position": null,
    "device_redundancy_group_priority": null,
    "vc_position": null,
    "vc_priority": null,
    "comments": "",
    "local_config_context_schema": null,
    "local_config_context_data_owner_content_type": null,
    "device_type": "a99de3bf-9a81-4645-9828-b00866de94a5",
    "status": "44a25fa2-ee88-47ed-b004-4dd36e54706f",
    "role": "ca552e01-bb63-4742-be5c-d27e62ae3e50",
    "tenant": null,
    "platform": null,
    "location": "fb720cca-ee59-4b76-9322-dfbbdaa5d052",
    "rack": null,
    "primary_ip4": null,
    "primary_ip6": null,
    "cluster": null,
    "virtual_chassis": null,
    "device_redundancy_group": null,
    "secrets_group": null,
    "created": "2023-09-30T07:56:23.664150Z",
    "last_updated": "2023-09-30T07:56:23.664168Z",
    "tags": [],
    "notes_url": "http://nautobot:8080/api/dcim/devices/86924375-4b50-4f95-a1c7-99896ab03307/notes/",
    "custom_fields": {},
    "parent_bay": null
}
```

You may have noticed that any field that is a foreign key relationship
only provides the ID. We need to cast to a dictionary to see the actual
sub keys.

```python
>>> print(json.dumps(dict(device1), indent=4))
{
    "id": "86924375-4b50-4f95-a1c7-99896ab03307",
    "object_type": "dcim.device",
    "display": "hq-access-01",
    "url": "http://nautobot:8080/api/dcim/devices/86924375-4b50-4f95-a1c7-99896ab03307/",
    "natural_slug": "hq-access-01__hq_8692",
    "face": null,
    "local_config_context_data": null,
    "local_config_context_data_owner_object_id": null,
    "name": "hq-access-01",
    "serial": "",
    "asset_tag": null,
    "position": null,
    "device_redundancy_group_priority": null,
    "vc_position": null,
    "vc_priority": null,
    "comments": "",
    "local_config_context_schema": null,
    "local_config_context_data_owner_content_type": null,
    "device_type": {
        "id": "a99de3bf-9a81-4645-9828-b00866de94a5",
        "object_type": "dcim.devicetype",
        "url": "http://nautobot:8080/api/dcim/device-types/a99de3bf-9a81-4645-9828-b00866de94a5/"
    },
    "status": {
        "id": "44a25fa2-ee88-47ed-b004-4dd36e54706f",
        "object_type": "extras.status",
        "url": "http://nautobot:8080/api/extras/statuses/44a25fa2-ee88-47ed-b004-4dd36e54706f/",
        "display": "Active",
        "natural_slug": "active_44a2",
        "content_types": [
            "circuits.circuit",
            "dcim.device",
            "dcim.powerfeed",
            "dcim.rack",
            "ipam.ipaddress",
            "ipam.prefix",
            "ipam.vlan",
            "virtualization.virtualmachine",
            "virtualization.vminterface",
            "dcim.interface",
            "dcim.location",
            "dcim.deviceredundancygroup",
            "dcim.interfaceredundancygroup"
        ],
        "name": "Active",
        "color": "4caf50",
        "description": "Unit is active",
        "created": "2023-09-30T00:00:00Z",
        "last_updated": "2023-09-30T06:06:44.559130Z",
        "notes_url": "http://nautobot:8080/api/extras/statuses/44a25fa2-ee88-47ed-b004-4dd36e54706f/notes/",
        "custom_fields": {}
    },
    "role": {
        "id": "ca552e01-bb63-4742-be5c-d27e62ae3e50",
        "object_type": "extras.role",
        "url": "http://nautobot:8080/api/extras/roles/ca552e01-bb63-4742-be5c-d27e62ae3e50/"
    },
    "tenant": null,
    "platform": null,
    "location": {
        "id": "fb720cca-ee59-4b76-9322-dfbbdaa5d052",
        "object_type": "dcim.location",
        "url": "http://nautobot:8080/api/dcim/locations/fb720cca-ee59-4b76-9322-dfbbdaa5d052/"
    },
    "rack": null,
    "primary_ip4": null,
    "primary_ip6": null,
    "cluster": null,
    "virtual_chassis": null,
    "device_redundancy_group": null,
    "secrets_group": null,
    "created": "2023-09-30T07:56:23.664150Z",
    "last_updated": "2023-09-30T07:56:23.664168Z",
    "tags": [],
    "notes_url": "http://nautobot:8080/api/dcim/devices/86924375-4b50-4f95-a1c7-99896ab03307/notes/",
    "custom_fields": {},
    "parent_bay": null
}
```

## Record Hashes and Equality Comparison

### Record Hash

The hash of a record is made from a combination of the name of the
endpoint and its ID. If the ID does not exist, then it will be a hash of
**only** the endpoint name. If an ID does exist then the hash will be of
the tuple representing [(endpoint.name, id)]{.title-ref}.

### Equality Comparison

If there are two objects that represent the same device, but an update
is made to a field other than the name or the ID, then a equals
comparison will return True, even though there is a different data
point.

```python
>>> # Assign hq-access-01 to device1, then to device2
>>> device1 = nautobot.dcim.devices.get(name="hq-access-01")
>>> device2 = nautobot.dcim.devices.get(name="hq-access-01")
>>> device1 == device2
True
>>> device2.platform
Cisco IOS
# Change the platform
>>> device2.platform = "Cisco NXOS"
>>> device2.platform
'Cisco NXOS'
# Compare the devices, since the ID nor the 
>>> device1 == device2
True
```

A comparison can be made on individual attributes of an object:

```python
>>> device1.platform == device2.platform
False
```
