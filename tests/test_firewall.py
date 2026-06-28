from opnsense.client import OPNsenseClient
from opnsense.firewall import FirewallAPI

from pprint import pprint

def test_firewall_filter(firewall_api):
    data = firewall_api.filter.get()
    assert "filter" in data

def test_firewall_alias(firewall_api):
    data = firewall_api.alias.get()
    assert "alias" in data

def test_firewall_alias(firewall_api):
    data = firewall_api.alias.get()
    assert "alias" in data

def test_firewall_group(firewall_api):
    data = firewall_api.group.get()
    assert "group" in data

def test_firewall_category(firewall_api):
    data = firewall_api.category.get()
    assert "category" in data

def test_firewall_dnat(firewall_api):
    data = firewall_api.d_nat.get_rule(None)
    assert 0 == len(data)

def test_firewall_npt(firewall_api):
    data = firewall_api.npt.get_rule(None)
    assert 0 == len(data)

def test_firewall_source_nat(firewall_api):
    data = firewall_api.source_nat.get_rule(None)
    assert 0 == len(data)

