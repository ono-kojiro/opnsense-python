# src/opnsense/api/firewall/alias.py

from opnsense.client import OPNsenseClient

import logging

logger = logging.getLogger(__name__)


class AliasAPI:
    """
    OPNsense Firewall Alias API

    module: firewall
    controller: alias
    """

    def __init__(self, client: OPNsenseClient):
        self.client = client
        self.base = "/api/firewall/alias"

    def get(self):
        """
        Get all aliases.

        GET /api/firewall/alias/get
        """
        url = f"{self.base}/get"
        return self.client.get(url)

    def get_alias_u_u_i_d(self, params):
        """
        GET /api/firewall/alias/get_alias_u_u_i_d/<name>
        """
        name = params["name"]

        url = f"{self.base}/get_alias_u_u_i_d/{name}"

        return self.client.get(url)

    def get_geo_i_p(self):
        """
        GET /api/firewall/alias/get_geo_i_p
        """
        url = f"{self.base}/get_geo_i_p"

        return self.client.get(url)

    def get_item(self, params):
        """
        GET /api/firewall/alias/get_item/<uuid>
        """
        uuid = params["uuid"]

        url = f"{self.base}/get_item/{uuid}"

        return self.client.get(url)

    def get_table_size(self):
        """
        GET /api/firewall/alias/get_table_size
        """
        url = f"{self.base}/get_table_size"

        return self.client.get(url)

    def search_item(self, data=None):
        """
        POST /api/firewall/alias/search_item
        """
        url = f"{self.base}/search_item"

        return self.client.post(url, json=data)

    def add_item(self, data):
        """
        POST /api/firewall/alias/add_item
        """
        url = f"{self.base}/add_item"

        return self.client.post(url, json=data)

    def set_item(self, data, params):
        """
        POST /api/firewall/alias/set_item/<uuid>
        """
        uuid = params["uuid"]

        url = f"{self.base}/set_item/{uuid}"

        return self.client.post(url, json=data)

    def del_item(self, params):
        """
        POST /api/firewall/alias/del_item/<uuid>
        """
        uuid = params["uuid"]

        url = f"{self.base}/del_item/{uuid}"

        return self.client.post(url)

    def toggle_item(self, params):
        """
        POST /api/firewall/alias/set_item/<uuid>&enabled=<enabled>
        """
        uuid = params["uuid"]
        enabled = params["enabled"]

        url = (
            f"{self.base}/set_item/"
            f"{uuid}&enabled={enabled}"
        )

        return self.client.post(url)

    def set(self, data):
        """
        POST /api/firewall/alias/set
        """
        url = f"{self.base}/set"

        return self.client.post(url, json=data)

    def save(self, data=None):
        """
        POST /api/firewall/alias/export
        """
        url = f"{self.base}/export"

        return self.client.post(url, json=data)

    def load(self, data=None):
        """
        POST /api/firewall/alias/import
        """
        url = f"{self.base}/import"

        return self.client.post(url, json=data)

    def reconfigure(self):
        """
        POST /api/firewall/alias/reconfigure
        """
        url = f"{self.base}/reconfigure"

        return self.client.post(url)

    def list_categories(self):
        """
        GET /api/firewall/alias/list_categories
        """
        url = f"{self.base}/list_categories"

        return self.client.get(url)

    def list_countries(self):
        """
        GET /api/firewall/alias/list_countries
        """
        url = f"{self.base}/list_countries"

        return self.client.get(url)

    def list_network_aliases(self):
        """
        GET /api/firewall/alias/list_network_aliases
        """
        url = f"{self.base}/list_network_aliases"

        return self.client.get(url)

    def list_user_groups(self):
        """
        GET /api/firewall/alias/list_user_groups
        """
        url = f"{self.base}/list_user_groups"

        return self.client.get(url)
    