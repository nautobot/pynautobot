from pynautobot.models.ipam import IpAddresses


def test_ip_address_nat_inside_outside_correct_objects(nb_client):
    """Validate nat_inside and nat_outside both return IpAddress Record objects."""
    ip_inside = nb_client.ipam.ip_addresses.create(address="192.0.2.1/32", status="active")
    ip_outside = nb_client.ipam.ip_addresses.create(address="192.0.2.2/32", status="active", nat_inside=ip_inside.id)

    ip_inside_refresh = nb_client.ipam.ip_addresses.get(address="192.0.2.1/32")

    assert isinstance(ip_outside.nat_inside, IpAddresses)
    assert isinstance(ip_inside_refresh.nat_outside, IpAddresses)
    assert str(ip_outside.nat_inside) == "192.0.2.1/32"
    assert str(ip_inside_refresh.nat_outside) == "192.0.2.2/32"
