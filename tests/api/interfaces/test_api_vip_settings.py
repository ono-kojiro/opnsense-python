# tests/api/interfaces/test_vip_settings.py

from unittest.mock import MagicMock

from opnsense.api.interfaces.vip_settings import VipSettingsAPI


def test_add_item():
    client = MagicMock()

    api = VipSettingsAPI(client)

    data = {
        "vip": {
            "descr": "vip_test",
            "subnet": "192.168.1.254",
        }
    }

    api.add_item(data)

    client.post.assert_called_once_with(
        "/api/interfaces/vip_settings/add_item",
        json=data,
    )


def test_del_item():
    client = MagicMock()

    api = VipSettingsAPI(client)

    params = {
        "uuid": "12345678",
    }

    api.del_item(params)

    client.post.assert_called_once_with(
        "/api/interfaces/vip_settings/del_item/12345678"
    )


def test_get():
    client = MagicMock()

    api = VipSettingsAPI(client)

    api.get()

    client.get.assert_called_once_with(
        "/api/interfaces/vip_settings/get"
    )


def test_get_item():
    client = MagicMock()

    api = VipSettingsAPI(client)

    params = {
        "uuid": "12345678",
    }

    api.get_item(params)

    client.get.assert_called_once_with(
        "/api/interfaces/vip_settings/get_item/12345678"
    )


def test_reconfigure():
    client = MagicMock()

    api = VipSettingsAPI(client)

    api.reconfigure()

    client.post.assert_called_once_with(
        "/api/interfaces/vip_settings/reconfigure"
    )


def test_search_item():
    client = MagicMock()

    api = VipSettingsAPI(client)

    data = {}

    api.search_item(data)

    client.post.assert_called_once_with(
        "/api/interfaces/vip_settings/search_item",
        json=data,
    )


def test_set():
    client = MagicMock()

    api = VipSettingsAPI(client)

    data = {
        "vip": {
            "descr": "vip_test",
        }
    }

    api.set(data)

    client.post.assert_called_once_with(
        "/api/interfaces/vip_settings/set",
        json=data,
    )


def test_set_item():
    client = MagicMock()

    api = VipSettingsAPI(client)

    data = {
        "vip": {
            "descr": "vip_test",
        }
    }

    params = {
        "uuid": "12345678",
    }

    api.set_item(data, params)

    client.post.assert_called_once_with(
        "/api/interfaces/vip_settings/set_item/12345678",
        json=data,
    )
