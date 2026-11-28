from unittest.mock import MagicMock, patch

from opnsense.resource.routing.settings import (
    Settings
)


def test_find_uuid():

    settings = Settings(None)

    settings.search_gateway = MagicMock(
        return_value={
            "rows": [
                {
                    "name": "WAN_GW",
                    "uuid": "11111111",
                },
                {
                    "name": "LAN_GW",
                    "uuid": "22222222",
                },
            ]
        }
    )

    uuid = settings._find_uuid("LAN_GW")

    assert uuid == "22222222"


@patch(
    "opnsense.api.routing.settings.SettingsAPI.get_gateway"
)
def test_get_gateway_by_name(mock_get_gateway):

    settings = Settings(None)

    settings.search_gateway = MagicMock(
        return_value={
            "rows": [
                {
                    "name": "WAN_GW",
                    "uuid": "11111111",
                }
            ]
        }
    )

    settings.get_gateway(
        {
            "name": "WAN_GW"
        }
    )

    mock_get_gateway.assert_called_once_with(
        {
            "name": "WAN_GW",
            "uuid": "11111111",
        }
    )


@patch(
    "opnsense.api.routing.settings.SettingsAPI.set_gateway"
)
@patch(
    "opnsense.api.routing.settings.SettingsAPI.get_gateway"
)
def test_set_gateway_by_name(
    mock_get_gateway,
    mock_set_gateway,
):

    mock_get_gateway.return_value = {
        "gateway_item": {
            "name": "WAN_GW",
            "disabled": "0",
        }
    }

    settings = Settings(None)

    settings.search_gateway = MagicMock(
        return_value={
            "rows": [
                {
                    "name": "WAN_GW",
                    "uuid": "11111111",
                }
            ]
        }
    )

    data = {
        "gateway": {
            "disabled": "1"
        }
    }

    settings.set_gateway(
        data,
        {
            "name": "WAN_GW"
        }
    )

    mock_get_gateway.assert_called_once_with(
        {
            "name": "WAN_GW",
            "uuid": "11111111",
        }
    )

    mock_set_gateway.assert_called_once_with(
        {
            "gateway_item": {
                "name": "WAN_GW",
                "disabled": "1",
            }
        },
        {
            "name": "WAN_GW",
            "uuid": "11111111",
        }
    )

@patch(
    "opnsense.api.routing.settings.SettingsAPI.del_gateway"
)
def test_del_gateway_by_name(mock_del_gateway):

    settings = Settings(None)

    settings.search_gateway = MagicMock(
        return_value={
            "rows": [
                {
                    "name": "WAN_GW",
                    "uuid": "11111111",
                }
            ]
        }
    )

    settings.del_gateway(
        {
            "name": "WAN_GW"
        }
    )

    mock_del_gateway.assert_called_once_with(
        {
            "name": "WAN_GW",
            "uuid": "11111111",
        }
    )


@patch(
    "opnsense.api.routing.settings.SettingsAPI.toggle_gateway"
)
def test_toggle_gateway_by_name(mock_toggle_gateway):

    settings = Settings(None)

    settings.search_gateway = MagicMock(
        return_value={
            "rows": [
                {
                    "name": "WAN_GW",
                    "uuid": "11111111",
                }
            ]
        }
    )

    settings.toggle_gateway(
        {
            "name": "WAN_GW"
        }
    )

    mock_toggle_gateway.assert_called_once_with(
        {
            "name": "WAN_GW",
            "uuid": "11111111",
        }
    )


@patch(
    "opnsense.api.routing.settings.SettingsAPI.del_gateway"
)
def test_delete_alias(mock_del_gateway):

    settings = Settings(None)

    settings.delete(
        {
            "uuid": "11111111"
        }
    )

    mock_del_gateway.assert_called_once_with(
        {
            "uuid": "11111111"
        }
    )

