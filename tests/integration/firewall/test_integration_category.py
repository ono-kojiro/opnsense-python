# test/integration/firewall/test_integration_category.py

import json

from helpers import run_shell

TARGET_CATEGORIES = (
    "admin",
    "debug",
    "test",
)


def test_category_get_search_consistency():

    cmd = "opncli firewall category get"
    lines = run_shell(cmd)

    data = json.loads(lines)

    items = data["category"]["categories"]["category"]

    count = len(items)

    cmd = "opncli firewall category search_item"
    lines = run_shell(cmd)

    data = json.loads(lines)

    assert data["rowCount"] == count


def test_category_add():

    cmd = 'opncli firewall category add name="admin" color="FF0000"'
    lines = run_shell(cmd)

    data = json.loads(lines)

    assert data["result"] == "saved"

    cmd = 'opncli firewall category add name="debug" color="00FF00"'
    lines = run_shell(cmd)

    data = json.loads(lines)

    assert data["result"] == "saved"

    cmd = 'opncli firewall category add name="test" color="0000FF"'
    lines = run_shell(cmd)

    data = json.loads(lines)

    assert data["result"] == "saved"


def test_category_exists():

    cmd = "opncli firewall category get"
    lines = run_shell(cmd)

    data = json.loads(lines)

    items = data["category"]["categories"]["category"]

    names = []

    for uuid in items:
        names.append(items[uuid]["name"])

    for name in TARGET_CATEGORIES:
        assert name in names


def test_category_delete():

    cmd = "opncli firewall category get"
    lines = run_shell(cmd)

    data = json.loads(lines)

    items = data["category"]["categories"]["category"]

    targets = []

    for uuid in items:

        name = items[uuid]["name"]

        if name in TARGET_CATEGORIES:
            targets.append(uuid)

    for uuid in targets:

        cmd = (
            "opncli firewall category "
            f"del_item --uuid={uuid}"
        )

        lines = run_shell(cmd)

        data = json.loads(lines)

        assert data["result"] == "deleted"


def test_category_deleted():

    cmd = "opncli firewall category get"
    lines = run_shell(cmd)

    data = json.loads(lines)

    items = data["category"]["categories"]["category"]

    names = []

    for uuid in items:
        names.append(items[uuid]["name"])

    for name in TARGET_CATEGORIES:
        assert name not in names

