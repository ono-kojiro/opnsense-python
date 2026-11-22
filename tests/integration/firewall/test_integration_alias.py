# tests/integration/firewall/test_integration_alias.py

import json

from helpers import run_shell


def test_alias_lifecycle():

    #
    # category create
    #

    cmd = (
        'opncli firewall category '
        'add name="admin" color="FF0000"'
    )

    lines = run_shell(cmd)

    data = json.loads(lines)

    assert data["result"] == "saved"

    #
    # alias create
    #

    aliases = [
        {
            "name": "myhost",
            "type": "host",
            "content": "192.168.1.1",
            "description": "host_myhost",
        },
        {
            "name": "mynetwork",
            "type": "network",
            "content": "192.168.1.0/24",
            "description": "nw_mynetwork",
        },
        {
            "name": "myport",
            "type": "port",
            "content": "1022",
            "description": "port_myport",
        },
    ]

    for item in aliases:

        cmd = (
            f'opncli firewall alias add_item '
            f'name="{item["name"]}" '
            f'type={item["type"]} '
            f'content={item["content"]} '
            f'enabled=1 '
            f'categories=admin '
            f'description="{item["description"]}"'
        )

        lines = run_shell(cmd)

        data = json.loads(lines)

        assert data["result"] == "saved"

    #
    # alias verify
    #

    cmd = 'opncli firewall alias get'

    lines = run_shell(cmd)

    data = json.loads(lines)

    items = data['alias']['aliases']['alias']

    names = set()

    for uuid in items:
        names.add(items[uuid]['name'])

    assert "myhost" in names
    assert "mynetwork" in names
    assert "myport" in names

    #
    # alias delete
    #

    targets = []

    for uuid in items:

        name = items[uuid]['name']

        if name in (
            "myhost",
            "mynetwork",
            "myport",
        ):
            targets.append(uuid)

    for uuid in targets:

        cmd = (
            'opncli firewall alias '
            f'del_item --uuid={uuid}'
        )

        lines = run_shell(cmd)

        data = json.loads(lines)

        assert data["result"] == "deleted"

    #
    # alias verify deleted
    #

    cmd = 'opncli firewall alias get'

    lines = run_shell(cmd)

    data = json.loads(lines)

    items = data['alias']['aliases']['alias']

    names = set()

    for uuid in items:
        names.add(items[uuid]['name'])

    assert "myhost" not in names
    assert "mynetwork" not in names
    assert "myport" not in names

    #
    # category delete
    #

    cmd = 'opncli firewall category get'

    lines = run_shell(cmd)

    data = json.loads(lines)

    items = data['category']['categories']['category']

    admin_uuid = None

    for uuid in items:

        if items[uuid]['name'] == 'admin':
            admin_uuid = uuid
            break

    assert admin_uuid is not None

    cmd = (
        'opncli firewall category '
        f'del_item --uuid={admin_uuid}'
    )

    lines = run_shell(cmd)

    data = json.loads(lines)

    assert data["result"] == "deleted"

    #
    # category verify deleted
    #

    cmd = 'opncli firewall category get'

    lines = run_shell(cmd)

    data = json.loads(lines)

    items = data['category']['categories']['category']

    names = set()

    for uuid in items:
        names.add(items[uuid]['name'])

    assert "admin" not in names

