from opnsense.client import OPNsenseClient

def test_interfaces_settings_get(interfaces_settings_api):
    api = interfaces_settings_api
    res = api.get()

    assert res['settings']['dhcp6_debug'] == "0"

