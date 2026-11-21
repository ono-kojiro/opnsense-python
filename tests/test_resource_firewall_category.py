from unittest.mock import patch

from opnsense.resource.firewall.category import Category


@patch(
    "opnsense.api.firewall.category.CategoryAPI.del_item"
)
def test_del_item_by_name(mock_del_item):

    category = Category(None)

    category.search_item = lambda: {
        "rows": [
            {
                "name": "blue",
                "uuid": "12345678"
            }
        ]
    }

    category.del_item({
        "name": "blue"
    })

    mock_del_item.assert_called_once_with({
        "name": "blue",
        "uuid": "12345678"
    })


