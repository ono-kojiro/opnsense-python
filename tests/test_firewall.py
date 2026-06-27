from opnsense.client import OPNsenseClient
from opnsense.firewall import FirewallAPI


def test_list_rules(firewall):
    data = firewall.list_rules()
    assert "filter" in data

