from pynautobot.core.response import Record


def test_ip_address_nat_inside_outside_correct_objects(nb_client):
    """Validate nat_inside and nat_outside both return IpAddress Record objects."""
    parent = nb_client.ipam.prefixes.get(prefix="192.0.0.0/8")
    ip_inside = nb_client.ipam.ip_addresses.create(address="192.0.2.1/32", status={"name": "Active"}, parent=parent.id)
    nb_client.ipam.ip_addresses.create(
        address="192.0.2.2/32", status={"name": "Active"}, parent=parent.id, nat_inside=ip_inside.id
    )

    ip_inside_refresh = nb_client.ipam.ip_addresses.get(address="192.0.2.1/32")
    ip_outside_refresh = nb_client.ipam.ip_addresses.get(address="192.0.2.2/32")

    assert str(ip_outside_refresh.nat_inside.address) == "192.0.2.1/32"
    assert str(ip_inside_refresh.nat_outside_list[0].address) == "192.0.2.2/32"


def test_prefixes_successfully_stringify_tags(nb_client):
    """Validate prefix will properly stringify the tags attribute and they are Record objects."""
    tag = nb_client.extras.tags.create(name="production", content_types=["ipam.prefix"])
    nb_client.ipam.prefixes.create(
        prefix="192.0.2.0/24", namespace={"name": "Global"}, status={"name": "Active"}, tags=[tag.id]
    )
    prefix = nb_client.ipam.prefixes.get(prefix="192.0.2.0/24", namespace="Global")
    assert str(prefix) == "192.0.2.0/24"
    assert prefix.tags
    assert isinstance(prefix.tags[0], Record)
