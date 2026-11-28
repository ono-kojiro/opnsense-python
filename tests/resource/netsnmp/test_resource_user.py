from unittest.mock import MagicMock, patch

from opnsense.resource.netsnmp.user import User


def test_find_uuid():

    user = User(None)

    user.search_user = MagicMock(
        return_value={
            "rows": [
                {
                    "username": "admin",
                    "uuid": "11111111",
                },
                {
                    "username": "testuser",
                    "uuid": "22222222",
                },
            ]
        }
    )

    uuid = user._find_uuid(
        "testuser"
    )

    assert uuid == "22222222"


@patch(
    "opnsense.api.netsnmp.user.UserAPI.get_user"
)
def test_get_user_by_username(
    mock_get_user
):

    user = User(None)

    user.search_user = MagicMock(
        return_value={
            "rows": [
                {
                    "username": "testuser",
                    "uuid": "22222222",
                },
            ]
        }
    )

    user.get_user(
        {
            "username": "testuser"
        }
    )

    mock_get_user.assert_called_once_with(
        {
            "username": "testuser",
            "uuid": "22222222",
        }
    )


@patch(
    "opnsense.api.netsnmp.user.UserAPI.del_user"
)
def test_del_user_by_username(
    mock_del_user
):

    user = User(None)

    user.search_user = MagicMock(
        return_value={
            "rows": [
                {
                    "username": "testuser",
                    "uuid": "22222222",
                },
            ]
        }
    )

    user.del_user(
        {
            "username": "testuser"
        }
    )

    mock_del_user.assert_called_once_with(
        {
            "username": "testuser",
            "uuid": "22222222",
        }
    )


@patch(
    "opnsense.api.netsnmp.user.UserAPI.set_user"
)
def test_set_user_by_username(
    mock_set_user
):

    user = User(None)

    user.search_user = MagicMock(
        return_value={
            "rows": [
                {
                    "username": "testuser",
                    "uuid": "22222222",
                },
            ]
        }
    )

    data = {
        "user": {
            "enabled": "1"
        }
    }

    user.set_user(
        data,
        {
            "username": "testuser"
        }
    )

    mock_set_user.assert_called_once_with(
        data,
        {
            "username": "testuser",
            "uuid": "22222222",
        }
    )


@patch(
    "opnsense.api.netsnmp.user.UserAPI.toggle_user"
)
def test_toggle_user_by_username(
    mock_toggle_user
):

    user = User(None)

    user.search_user = MagicMock(
        return_value={
            "rows": [
                {
                    "username": "testuser",
                    "uuid": "22222222",
                },
            ]
        }
    )

    user.toggle_user(
        {
            "username": "testuser"
        }
    )

    mock_toggle_user.assert_called_once_with(
        {
            "username": "testuser",
            "uuid": "22222222",
        }
    )


@patch(
    "opnsense.api.netsnmp.user.UserAPI.add_user"
)
def test_add_user(
    mock_add_user
):

    user = User(None)

    data = {
        "user": {
            "username": "testuser",
            "password": "secret",
            "enckey": "secret",
            "enabled": "1",
        }
    }

    user.add_user(data)

    mock_add_user.assert_called_once_with(
        data
    )

