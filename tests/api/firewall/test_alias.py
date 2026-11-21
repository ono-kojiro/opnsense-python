# tests/api/firewall/test_alias.py

from unittest.mock import MagicMock

from opnsense.api.firewall.alias import AliasAPI


def test_get():
    client = MagicMock()

    api = AliasAPI(client)

    api.get()

    client.get.assert_called_once_with(
        "/api/firewall/alias/get"
    )


def test_search_item():
    client = MagicMock()

    api = AliasAPI(client)

    data = {}

    api.search_item(data)

    client.post.assert_called_once_with(
        "/api/firewall/alias/search_item",
        json=data,
    )


def test_add_item():
    client = MagicMock()

    api = AliasAPI(client)

    data = {
        "alias": {
            "name": "myhost",
            "type": "host",
            "content": "192.168.1.1",
        }
    }

    api.add_item(data)

    client.post.assert_called_once_with(
        "/api/firewall/alias/add_item",
        json=data,
    )


def test_set_item():
    client = MagicMock()

    api = AliasAPI(client)

    data = {
        "alias": {
            "description": "host_myhost",
        }
    }

    params = {
        "uuid": "12345678",
    }

    api.set_item(data, params)

    client.post.assert_called_once_with(
        "/api/firewall/alias/set_item/12345678",
        json=data,
    )


def test_del_item():
    client = MagicMock()

    api = AliasAPI(client)

    params = {
        "uuid": "12345678",
    }

    api.del_item(params)

    client.post.assert_called_once_with(
        "/api/firewall/alias/del_item/12345678"
    )


def test_toggle_item():
    client = MagicMock()

    api = AliasAPI(client)

    params = {
        "uuid": "12345678",
        "enabled": "1",
    }

    api.toggle_item(params)

    client.post.assert_called_once_with(
        "/api/firewall/alias/set_item/12345678&enabled=1"
    )


def test_set():
    client = MagicMock()

    api = AliasAPI(client)

    data = {
        "alias": {
            "name": "myhost",
        }
    }

    api.set(data)

    client.post.assert_called_once_with(
        "/api/firewall/alias/set",
        json=data,
    )


def test_save():
    client = MagicMock()

    api = AliasAPI(client)

    data = {
        "aliases": []
    }

    api.save(data)

    client.post.assert_called_once_with(
        "/api/firewall/alias/export",
        json=data,
    )


def test_load():
    client = MagicMock()

    api = AliasAPI(client)

    data = {
        "aliases": []
    }

    api.load(data)

    client.post.assert_called_once_with(
        "/api/firewall/alias/import",
        json=data,
    )


def test_reconfigure():
    client = MagicMock()

    api = AliasAPI(client)

    api.reconfigure()

    client.post.assert_called_once_with(
        "/api/firewall/alias/reconfigure"
    )


def test_get_alias_uuid():
    client = MagicMock()

    api = AliasAPI(client)

    params = {
        "name": "myhost",
    }

    api.get_alias_u_u_i_d(params)

    client.get.assert_called_once_with(
        "/api/firewall/alias/get_alias_u_u_i_d/myhost"
    )


def test_get_item():
    client = MagicMock()

    api = AliasAPI(client)

    params = {
        "uuid": "12345678",
    }

    api.get_item(params)

    client.get.assert_called_once_with(
        "/api/firewall/alias/get_item/12345678"
    )


def test_get_geo_ip():
    client = MagicMock()

    api = AliasAPI(client)

    api.get_geo_i_p()

    client.get.assert_called_once_with(
        "/api/firewall/alias/get_geo_i_p"
    )


def test_get_table_size():
    client = MagicMock()

    api = AliasAPI(client)

    api.get_table_size()

    client.get.assert_called_once_with(
        "/api/firewall/alias/get_table_size"
    )


def test_list_categories():
    client = MagicMock()

    api = AliasAPI(client)

    api.list_categories()

    client.get.assert_called_once_with(
        "/api/firewall/alias/list_categories"
    )


def test_list_countries():
    client = MagicMock()

    api = AliasAPI(client)

    api.list_countries()

    client.get.assert_called_once_with(
        "/api/firewall/alias/list_countries"
    )


def test_list_network_aliases():
    client = MagicMock()

    api = AliasAPI(client)

    api.list_network_aliases()

    client.get.assert_called_once_with(
        "/api/firewall/alias/list_network_aliases"
    )


def test_list_user_groups():
    client = MagicMock()

    api = AliasAPI(client)

    api.list_user_groups()

    client.get.assert_called_once_with(
        "/api/firewall/alias/list_user_groups"
    )

