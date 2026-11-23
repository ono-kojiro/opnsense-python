# tests/api/routing/test_settings.py

from unittest.mock import MagicMock

from opnsense.api.routing.settings import SettingsAPI


def test_add_gateway():

    client = MagicMock()

    api = SettingsAPI(client)

    data = {
        "gateway": {
            "name": "WAN_GW",
        }
    }

    api.add_gateway(data)

    client.post.assert_called_once_with(
        "/api/routing/settings/add_gateway",
        json=data,
    )


def test_del_gateway():

    client = MagicMock()

    api = SettingsAPI(client)

    params = {
        "uuid": "12345678",
    }

    api.del_gateway(params)

    client.post.assert_called_once_with(
        "/api/routing/settings/del_gateway/12345678"
    )


def test_get():

    client = MagicMock()

    api = SettingsAPI(client)

    api.get()

    client.get.assert_called_once_with(
        "/api/routing/settings/get"
    )


def test_get_gateway():

    client = MagicMock()

    api = SettingsAPI(client)

    params = {
        "uuid": "12345678",
    }

    api.get_gateway(params)

    client.get.assert_called_once_with(
        "/api/routing/settings/get_gateway/12345678"
    )


def test_reconfigure():

    client = MagicMock()

    api = SettingsAPI(client)

    api.reconfigure()

    client.post.assert_called_once_with(
        "/api/routing/settings/reconfigure"
    )


def test_search_gateway():

    client = MagicMock()

    api = SettingsAPI(client)

    data = {}

    api.search_gateway(data)

    client.post.assert_called_once_with(
        "/api/routing/settings/search_gateway",
        json=data,
    )


def test_set_gateway():

    client = MagicMock()

    api = SettingsAPI(client)

    data = {
        "gateway": {
            "disabled": "1",
        }
    }

    params = {
        "uuid": "12345678",
    }

    api.set_gateway(
        data,
        params,
    )

    client.post.assert_called_once_with(
        "/api/routing/settings/set_gateway/12345678",
        json=data,
    )


def test_toggle_gateway():

    client = MagicMock()

    api = SettingsAPI(client)

    params = {
        "uuid": "12345678",
    }

    api.toggle_gateway(params)

    client.post.assert_called_once_with(
        "/api/routing/settings/toggle_gateway/12345678"
    )

