# tests/integration/firewall/test_integration_filter.py

import json

from helpers import run_shell


def test_filter_lifecycle():

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
    # filter create
    #

    cmd = (
        'opncli firewall filter '
        'add_rule '
        'description=hoge '
        'categories=admin'
    )

    lines = run_shell(cmd)

    data = json.loads(lines)

    assert data["result"] == "saved"

    #
    # filter exists
    #

    cmd = 'opncli firewall filter search_rule'

    lines = run_shell(cmd)

    data = json.loads(lines)

    enabled = None

    for row in data["rows"]:

        if row["description"] == "hoge":
            enabled = row["enabled"]

    assert enabled is not None

    #
    # disable rule
    #

    cmd = (
        'opncli firewall filter '
        'set_rule '
        '--descr="hoge" '
        'enabled=0'
    )

    lines = run_shell(cmd)

    data = json.loads(lines)

    assert data["result"] == "saved"

    #
    # apply
    #

    cmd = 'opncli firewall filter apply'

    lines = run_shell(cmd)

    data = json.loads(lines)

    assert data["status"] == "OK\n\n"

    #
    # verify disabled
    #

    cmd = 'opncli firewall filter search_rule'

    lines = run_shell(cmd)

    data = json.loads(lines)

    enabled = None

    for row in data["rows"]:

        if row["description"] == "hoge":
            enabled = row["enabled"]

    assert enabled == "0"

    #
    # enable rule
    #

    cmd = (
        'opncli firewall filter '
        'set_rule '
        '--descr="hoge" '
        'enabled=1'
    )

    lines = run_shell(cmd)

    data = json.loads(lines)

    assert data["result"] == "saved"

    #
    # apply
    #

    cmd = 'opncli firewall filter apply'

    lines = run_shell(cmd)

    data = json.loads(lines)

    assert data["status"] == "OK\n\n"

    #
    # verify enabled
    #

    cmd = 'opncli firewall filter search_rule'

    lines = run_shell(cmd)

    data = json.loads(lines)

    enabled = None

    rule_uuid = None

    for row in data["rows"]:

        if row["description"] == "hoge":
            enabled = row["enabled"]
            rule_uuid = row["uuid"]

    assert enabled == "1"
    assert rule_uuid is not None

    #
    # delete rule
    #

    cmd = (
        'opncli firewall filter '
        f'del_rule --uuid={rule_uuid}'
    )

    lines = run_shell(cmd)

    data = json.loads(lines)

    assert data["result"] == "deleted"

    #
    # verify deleted
    #

    cmd = 'opncli firewall filter search_rule'

    lines = run_shell(cmd)

    data = json.loads(lines)

    found = False

    for row in data["rows"]:

        if row["description"] == "hoge":
            found = True

    assert found is False

    #
    # category delete
    #

    cmd = 'opncli firewall category get'

    lines = run_shell(cmd)

    data = json.loads(lines)

    category_uuid = None

    items = data["category"]["categories"]["category"]

    for uuid in items:

        if items[uuid]["name"] == "admin":
            category_uuid = uuid

    assert category_uuid is not None

    cmd = (
        'opncli firewall category '
        f'del_item --uuid={category_uuid}'
    )

    lines = run_shell(cmd)

    data = json.loads(lines)

    assert data["result"] == "deleted"

