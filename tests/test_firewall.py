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

from helpers import run_shell, get_categories

@pytest.mark.order(100)
def test_firewall_delete_categories():
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

    for uuid in items:
        cmd = 'opncli firewall category del_item --uuid={0}'.format(uuid)
        lines = run_shell(cmd)
        data = json.loads(lines)
        result = data['result']
        assert result == 'deleted'

@pytest.mark.order(110)
def test_firewall_check_category():
    cmd = 'opncli firewall category search_item'
    lines = run_shell(cmd)

    data = json.loads(lines)
    ret = data['rowCount']
    assert ret == 0


@pytest.mark.order(120)
def test_firewall_add_categories():
    cmd = 'opncli firewall category get'
    lines = run_shell(cmd)
    data = json.loads(lines)
    items = data['category']['categories']['category']

    names = {}
    for uuid in items:
        name = items[uuid]['name']
        names[name] = 1

    cmd = 'opncli firewall category add name="admin" color="FF0000"'
    lines = run_shell(cmd)
    data = json.loads(lines)
    got = data['result']
    if not 'admin' in names:
        exp = 'saved'
    else :
        exp = 'failed'
    assert got == exp

    cmd = 'opncli firewall category add name="debug" color="00FF00"'
    lines = run_shell(cmd)
    data = json.loads(lines)
    got = data['result']
    if not 'debug' in names:
        exp = 'saved'
    else :
        exp = 'failed'
    assert got == exp

    cmd = 'opncli firewall category add name="test" color="0000FF"'
    lines = run_shell(cmd)
    data = json.loads(lines)
    got = data['result']
    if not 'test' in names:
        exp = 'saved'
    else :
        exp = 'failed'
    assert got == exp

@pytest.mark.order(130)
def test_firewall_delete_aliases():
    cmd = 'opncli firewall alias get'
    lines = run_shell(cmd)
    data = json.loads(lines)

    count = 0
    items = data['alias']['aliases']['alias']
    for uuid in items:
        name = items[uuid]['name']
        count = count +1

    assert count != 0

@pytest.mark.order(131)
def test_firewall_add_aliases():
    cat_uuids = get_categories()

    cmd = 'opncli firewall alias get'
    lines = run_shell(cmd)
    data = json.loads(lines)

    count = 0
    items = data['alias']['aliases']['alias']

    aliases = {}
    for uuid in items:
        name = items[uuid]['name']
        aliases[name] = 1

    name = 'myhost'
    content = '192.168.1.1'
    desc = 'myhost'
    category = 'admin'

    category_uuid = cat_uuids[category]

    cmd = 'opncli firewall alias add_item name="{0}" '.format(name)
    cmd = cmd + 'type=host content={0} enabled=1 '.format(content)
    cmd = cmd + 'categories.{0}.value={0} '.format(category)
    cmd = cmd + 'categories.{0}.selected=1 '.format(category_uuid)
    cmd = cmd + 'description="{0}"'.format(desc)
    lines = run_shell(cmd)
    data = json.loads(lines)
    got = data['result']
    if name in aliases :
        exp = 'failed'
    else :
        exp = 'saved'

    assert got == exp

@pytest.mark.order(190)
def test_firewall_clean_categories():
    cmd = 'opncli firewall category get'
    lines = run_shell(cmd)
    data = json.loads(lines)

    count = 0

    items = data['category']['categories']['category']
    for uuid in items:
        item  = items[uuid]

        name  = item['name']
        color = item['color']

        #if not name in ( 'admin', 'debug', 'test' ) :
        if not name in ( 'admin', 'debug' ) :
            cmd = 'opncli firewall category del_item --uuid={0}'.format(uuid)
            lines = run_shell(cmd)
            data = json.loads(lines)
            result = data['result']
            assert result == 'deleted'

