# tests/api/firewall/test_filter.py

from unittest.mock import MagicMock

from opnsense.api.firewall.filter import FilterAPI


def test_get_rule():
    client = MagicMock()

    api = FilterAPI(client)

    params = {
        "uuid": "12345678",
    }

    api.get_rule(params)

    client.get.assert_called_once_with(
        "/api/firewall/filter/get_rule/12345678"
    )


def test_search_rule():
    client = MagicMock()

    api = FilterAPI(client)

    data = {}

    api.search_rule(data)

    client.post.assert_called_once_with(
        "/api/firewall/filter/search_rule",
        json=data,
    )


def test_add_rule():
    client = MagicMock()

    api = FilterAPI(client)

    data = {
        "rule": {
            "description": "allow_admin",
        }
    }

    api.add_rule(data)

    client.post.assert_called_once_with(
        "/api/firewall/filter/add_rule",
        json=data,
    )


def test_set_rule():
    client = MagicMock()

    api = FilterAPI(client)

    data = {
        "rule": {
            "description": "allow_admin",
        }
    }

    params = {
        "uuid": "12345678",
    }

    api.set_rule(data, params)

    client.post.assert_called_once_with(
        "/api/firewall/filter/set_rule/12345678",
        json=data,
    )


def test_del_rule():
    client = MagicMock()

    api = FilterAPI(client)

    params = {
        "uuid": "12345678",
    }

    api.del_rule(params)

    client.post.assert_called_once_with(
        "/api/firewall/filter/del_rule/12345678"
    )


def test_toggle_rule():
    client = MagicMock()

    api = FilterAPI(client)

    params = {
        "uuid": "12345678",
    }

    api.toggle_rule(params)

    client.post.assert_called_once_with(
        "/api/firewall/filter/toggleRule/12345678"
    )


def test_apply():
    client = MagicMock()

    api = FilterAPI(client)

    api.apply()

    client.post.assert_called_once_with(
        "/api/firewall/filter/apply"
    )


def test_prune_selected_dict():
    src = {
        "items": {
            "a": {
                "selected": 1,
                "value": "foo",
            },
            "b": {
                "selected": 0,
                "value": "bar",
            },
        }
    }

    dst = FilterAPI.prune_selected(src)

    assert "a" in dst["items"]
    assert "b" not in dst["items"]


def test_prune_selected_list():
    src = [
        {
            "selected": 1,
            "name": "allow",
        },
        {
            "selected": 0,
            "name": "deny",
        },
    ]

    dst = FilterAPI.prune_selected(src)

    assert len(dst) == 1

    assert dst[0]["name"] == "allow"

