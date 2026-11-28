from unittest.mock import MagicMock

from opnsense.api.netsnmp.user import UserAPI


def test_add_user():

    client = MagicMock()

    api = UserAPI(client)

    data = {
        "user": {
            "username": "testuser",
            "password": "secret",
            "enckey": "secret",
            "enabled": "1",
        }
    }

    api.add_user(data)

    client.post.assert_called_once_with(
        "/api/netsnmp/user/add_user",
        json=data,
    )


def test_del_user():

    client = MagicMock()

    api = UserAPI(client)

    params = {
        "uuid": "12345678",
    }

    api.del_user(params)

    client.post.assert_called_once_with(
        "/api/netsnmp/user/del_user/12345678"
    )


def test_get():

    client = MagicMock()

    api = UserAPI(client)

    api.get()

    client.get.assert_called_once_with(
        "/api/netsnmp/user/get"
    )


def test_get_user():

    client = MagicMock()

    api = UserAPI(client)

    params = {
        "uuid": "12345678",
    }

    api.get_user(params)

    client.get.assert_called_once_with(
        "/api/netsnmp/user/get_user/12345678"
    )


def test_search_user():

    client = MagicMock()

    api = UserAPI(client)

    api.search_user()

    client.get.assert_called_once_with(
        "/api/netsnmp/user/search_user"
    )


def test_set():

    client = MagicMock()

    api = UserAPI(client)

    data = {
        "user": {
            "enabled": "1",
        }
    }

    api.set(data)

    client.post.assert_called_once_with(
        "/api/netsnmp/user/set",
        json=data,
    )


def test_set_user():

    client = MagicMock()

    api = UserAPI(client)

    data = {
        "user": {
            "enabled": "1",
        }
    }

    params = {
        "uuid": "12345678",
    }

    api.set_user(
        data,
        params,
    )

    client.post.assert_called_once_with(
        "/api/netsnmp/user/set_user/12345678",
        json=data,
    )


def test_toggle_user():

    client = MagicMock()

    api = UserAPI(client)

    params = {
        "uuid": "12345678",
    }

    api.toggle_user(params)

    client.post.assert_called_once_with(
        "/api/netsnmp/user/toggle_user/12345678"
    )

