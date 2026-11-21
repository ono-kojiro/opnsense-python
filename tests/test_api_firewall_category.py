# tests/test_api_firewall_category.py

from unittest.mock import MagicMock

from opnsense.api.firewall.category import CategoryAPI


def test_add_item():
    client = MagicMock()

    api = CategoryAPI(client)

    data = {
        "category": {
            "name": "blue",
            "color": "0000ff",
        }
    }

    api.add_item(data)

    client.post.assert_called_once_with(
        "/api/firewall/category/add_item",
        json=data,
    )


def test_set():
    client = MagicMock()

    api = CategoryAPI(client)

    data = {
        "category": {
            "name": "blue",
            "color": "ff0000",
        }
    }

    params = {
        "uuid": "12345678"
    }

    api.set(data, params)

    client.post.assert_called_once_with(
        "/api/firewall/category/set/12345678",
        json=data,
    )


def test_del_item():
    client = MagicMock()

    api = CategoryAPI(client)

    params = {
        "uuid": "12345678"
    }

    api.del_item(params)

    client.post.assert_called_once_with(
        "/api/firewall/category/del_item/12345678"
    )


def test_apply():
    client = MagicMock()

    api = CategoryAPI(client)

    api.apply()

    client.post.assert_called_once_with(
        "/api/firewall/category/apply"
    )

