from unittest.mock import MagicMock, patch

from opnsense.resource.interfaces.vip_settings import (
    VipSettings
)


def test_find_uuid():

    vip = VipSettings(None)

    vip.get = MagicMock(
        return_value={
            "vip": {
                "vip": {
                    "11111111": {
                        "descr": "vip_wan"
                    },
                    "22222222": {
                        "descr": "vip_lan"
                    }
                }
            }
        }
    )

    uuid = vip._find_uuid("vip_lan")

    assert uuid == "22222222"


@patch(
    "opnsense.api.interfaces.vip_settings.VipSettingsAPI.del_item"
)
def test_del_item_by_descr(mock_del_item):

    vip = VipSettings(None)

    vip.get = MagicMock(
        return_value={
            "vip": {
                "vip": {
                    "11111111": {
                        "descr": "vip_wan"
                    }
                }
            }
        }
    )

    vip.del_item({
        "descr": "vip_wan"
    })

    mock_del_item.assert_called_once_with(
        {
            "descr": "vip_wan",
            "uuid": "11111111",
        }
    )


@patch(
    "opnsense.api.interfaces.vip_settings.VipSettingsAPI.get_item"
)
def test_get_item_by_descr(mock_get_item):

    vip = VipSettings(None)

    vip.get = MagicMock(
        return_value={
            "vip": {
                "vip": {
                    "11111111": {
                        "descr": "vip_wan"
                    }
                }
            }
        }
    )

    vip.get_item({
        "descr": "vip_wan"
    })

    mock_get_item.assert_called_once_with(
        {
            "descr": "vip_wan",
            "uuid": "11111111",
        }
    )


@patch(
    "opnsense.api.interfaces.vip_settings.VipSettingsAPI.set_item"
)
def test_set_item_by_descr(mock_set_item):

    vip = VipSettings(None)

    vip.get = MagicMock(
        return_value={
            "vip": {
                "vip": {
                    "11111111": {
                        "descr": "vip_wan"
                    }
                }
            }
        }
    )

    data = {
        "vip": {
            "subnet": "192.168.1.254"
        }
    }

    vip.set_item(
        data,
        {
            "descr": "vip_wan"
        }
    )

    mock_set_item.assert_called_once_with(
        data,
        {
            "descr": "vip_wan",
            "uuid": "11111111",
        }
    )


@patch(
    "opnsense.api.interfaces.vip_settings.VipSettingsAPI.add_item"
)
def test_add_alias(mock_add_item):

    vip = VipSettings(None)

    data = {
        "vip": {
            "descr": "vip_wan"
        }
    }

    vip.add(data)

    mock_add_item.assert_called_once_with(data)


@patch(
    "opnsense.api.interfaces.vip_settings.VipSettingsAPI.del_item"
)
def test_delete_alias(mock_del_item):

    vip = VipSettings(None)

    vip.delete({
        "uuid": "11111111"
    })

    mock_del_item.assert_called_once_with(
        {
            "uuid": "11111111"
        }
    )

