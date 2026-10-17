import os
import sys

import pytest
from pprint import pprint
import subprocess
import shlex

import re
import json

from opnsense.client import OPNsenseClient
from opnsense.firewall import FirewallAPI

from pprint import pprint

from helpers import run_shell

def test_firewall_source_nat(firewall_api):
    assert 0 == 0

def test_firewall_categories():
    cmd = 'opncli firewall category get'
    lines = run_shell(cmd)
    data = json.loads(lines)

    count = 0

    items = data['category']['categories']['category']
    for cat_id in items:
        item  = items[cat_id]

        name  = item['name']
        color = item['color']

        count = count + 1

    uuids = items.keys()
    for uuid in uuids:
        cmd = 'opncli firewall category del_item --uuid={0}'.format(uuid)
        lines = run_shell(cmd)
        data = json.loads(lines)
        result = data['result']
        assert result == 'deleted'


    cmd = 'opncli firewall category search_item'
    lines = run_shell(cmd)

    data = json.loads(lines)
    ret = data['rowCount']
    assert ret == 0

    cmd = 'opncli firewall category add name="red" color="FF0000"'
    lines = run_shell(cmd)
    data = json.loads(lines)
    ret = data['result']
    assert ret == 'saved'
    
    cmd = 'opncli firewall category add name="green" color="00FF00"'
    lines = run_shell(cmd)
    data = json.loads(lines)
    ret = data['result']
    assert ret == 'saved'

    cmd = 'opncli firewall category add name="blue" color="0000FF"'
    lines = run_shell(cmd)
    data = json.loads(lines)
    ret = data['result']
    assert ret == 'saved'


