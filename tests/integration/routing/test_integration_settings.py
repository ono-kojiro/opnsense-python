import json

from helpers import run_shell


def _find_gateway(name):

    cmd = (
        "opncli routing settings "
        "search_gateway"
    )

    lines = run_shell(cmd)

    data = json.loads(lines)

    for row in data["rows"]:

        if row["name"] == name:
            return row

    return None


def test_gateway_lifecycle():

    #
    # WAN_GW state
    #

    gw = _find_gateway("WAN_GW")

    assert gw is not None

    initial_disabled = gw["disabled"]

    #
    # toggle
    #

    cmd = (
        "opncli routing settings "
        "toggle_gateway "
        "--name=WAN_GW"
    )

    lines = run_shell(cmd)

    data = json.loads(lines)

    assert data["changed"] is True

    #
    # apply
    #

    cmd = (
        "opncli routing settings "
        "reconfigure"
    )

    lines = run_shell(cmd)

    json.loads(lines)

    #
    # verify state changed
    #

    gw = _find_gateway("WAN_GW")

    assert gw is not None

    changed_disabled = gw["disabled"]

    assert changed_disabled != initial_disabled

    #
    # toggle back
    #

    cmd = (
        "opncli routing settings "
        "toggle_gateway "
        "--name=WAN_GW"
    )

    lines = run_shell(cmd)

    data = json.loads(lines)

    assert data["changed"] is True

    #
    # apply
    #

    cmd = (
        "opncli routing settings "
        "reconfigure"
    )

    lines = run_shell(cmd)

    json.loads(lines)

    #
    # verify restored
    #

    gw = _find_gateway("WAN_GW")

    assert gw is not None

    assert gw["disabled"] == initial_disabled

