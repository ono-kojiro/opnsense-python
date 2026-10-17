import os
import sys

import pytest
import subprocess
import shlex

import re
import json

from opnsense.client import OPNsenseClient
from opnsense.firewall import FirewallAPI

from pprint import pprint

from helpers import run_shell, get_categories
        
target_categories = ( 'admin', 'debug', 'test' )

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
    cmd = 'opncli firewall category get'
    lines = run_shell(cmd)

    count = 0

    data = json.loads(lines)
    items = data['category']['categories']['category']
    for uuid in items :
        name = items[uuid]['name']
        count += 1

    cmd = 'opncli firewall category search_item'
    lines = run_shell(cmd)

    data = json.loads(lines)
    ret = data['rowCount']
    assert ret == count


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
    exp = 'saved'
    #if not 'admin' in names:
    #    exp = 'saved'
    #else :
    #    exp = 'failed'
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

    items = [
        {
            "name": "myhost",
            "type": "host",
            "description": "host_myhost",
            "content": "192.168.1.1",
        },
        {
            "name": "mynetwork",
            "type": "network",
            "description": "nw_mynetwork",
            "content": "192.168.1.0/24",
        },

        {
            "name": "myport",
            "type": "port",
            "description": "port_myport",
            "content": "1022",
        },
    ]

    category = 'admin'
    for item in items :
        name    = item['name']
        typ     = item['type']
        content = item['content']
        description = item['description']

        category_uuid = cat_uuids[category]

        cmd = 'opncli firewall alias add_item name="{0}" '.format(name)
        cmd = cmd + 'type={0} content={1} enabled=1 '.format(typ, content)
        cmd = cmd + 'categories={0} '.format(category)
        cmd = cmd + 'description="{0}"'.format(description)
        lines = run_shell(cmd)
        data = json.loads(lines)
        got = data['result']
        if name in aliases :
            exp = 'failed'
        else :
            exp = 'saved'

        assert got == exp

@pytest.mark.order(140)
def test_firewall_add_rules():
    cat_uuids = get_categories()

    cmd = 'opncli firewall filter add_rule description=hoge categories=admin'
    lines = run_shell(cmd)
    data = json.loads(lines)
    assert data['result'] == 'saved'

@pytest.mark.order(197)
def test_firewall_clean_rules():
    uuids = []
    cmd = 'opncli firewall filter search_rule | jq -r ".rows[] | select(.\\"%categories\\" == \\"admin\\") | .uuid"'

    lines = run_shell(cmd)
    #pprint(lines, stream=sys.stderr)
    for line in re.split(r'\n', lines) :
        if line == '' :
            continue
        uuids.append(line)

    for uuid in uuids:
        cmd = 'opncli firewall filter del_rule --uuid={0}'.format(uuid)
        #pprint(cmd, stream=sys.stderr)
        lines = run_shell(cmd)
        data = json.loads(lines)
        assert data['result'] == 'deleted'


@pytest.mark.order(198)
def test_firewall_clean_aliases():
    cmd = 'opncli firewall alias get'
    lines = run_shell(cmd)
    data = json.loads(lines)
    items = data['alias']['aliases']['alias']

    targets = []

    for uuid in items :
        name = items[uuid]['name']
        categories = items[uuid]['categories']
        for cat_uuid in categories :
            value    = categories[cat_uuid]['value']
            selected = categories[cat_uuid]['selected']

            if value in target_categories and selected == 1:
                targets.append(uuid)

    for uuid in targets:
        cmd = 'opncli firewall alias del_item --uuid={0}'.format(uuid)
        lines = run_shell(cmd)
        data = json.loads(lines)
        assert data['result'] == 'deleted'

@pytest.mark.order(199)
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
        #if not name in ( 'admin', 'debug' ) :
        cmd = 'opncli firewall category del_item --uuid={0}'.format(uuid)
        lines = run_shell(cmd)
        #pprint(lines, stream=sys.stderr)
        data = json.loads(lines)
        result = data['result']
        assert result == 'deleted'

