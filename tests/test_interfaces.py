from opnsense.client import OPNsenseClient
from opnsense.interfaces import InterfacesAPI

from pprint import pprint


def test_interfaces_overview(interfaces_api):
    data = interfaces_api.overview.interfaces_info()
    assert isinstance(data, dict)


def test_interfaces_settings(interfaces_api):
    data = interfaces_api.settings.get()
    assert isinstance(data, dict)


def test_interfaces_bridge_settings(interfaces_api):
    data = interfaces_api.bridge_settings.get()
    assert isinstance(data, dict)


def test_interfaces_gif_settings(interfaces_api):
    data = interfaces_api.gif_settings.get()
    assert isinstance(data, dict)


def test_interfaces_gre_settings(interfaces_api):
    data = interfaces_api.gre_settings.get()
    assert isinstance(data, dict)


def test_interfaces_lagg_settings(interfaces_api):
    data = interfaces_api.lagg_settings.get()
    assert isinstance(data, dict)


def test_interfaces_loopback_settings(interfaces_api):
    data = interfaces_api.loopback_settings.get()
    assert isinstance(data, dict)


def test_interfaces_neighbor_settings(interfaces_api):
    data = interfaces_api.neighbor_settings.get()
    assert isinstance(data, dict)


def test_interfaces_vip_settings(interfaces_api):
    data = interfaces_api.vip_settings.get()
    assert isinstance(data, dict)


def test_interfaces_vlan_settings(interfaces_api):
    data = interfaces_api.vlan_settings.get()
    assert isinstance(data, dict)


def test_interfaces_vxlan_settings(interfaces_api):
    data = interfaces_api.vxlan_settings.get()
    assert isinstance(data, dict)

