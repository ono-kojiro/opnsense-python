# src/opnsense/api/interfaces/vip_settings.py

import logging

from opnsense.client import OPNsenseClient

logger = logging.getLogger(__name__)


class VipSettingsAPI:
    """
    OPNsense Interfaces VIP Settings API

    module: interfaces
    controller: vip_settings
    """

    def __init__(self, client: OPNsenseClient):
        self.client = client
        self.base = "/api/interfaces/vip_settings"

    def add_item(self, data):
        """
        POST /api/interfaces/vip_settings/add_item
        """
        url = f"{self.base}/add_item"

        return self.client.post(
            url,
            json=data,
        )

    def del_item(self, params):
        """
        POST /api/interfaces/vip_settings/del_item/<uuid>
        """
        uuid = params["uuid"]

        url = f"{self.base}/del_item/{uuid}"

        return self.client.post(url)

    def get(self):
        """
        GET /api/interfaces/vip_settings/get
        """
        url = f"{self.base}/get"

        return self.client.get(url)

    def get_item(self, params):
        """
        GET /api/interfaces/vip_settings/get_item/<uuid>
        """
        uuid = params["uuid"]

        url = f"{self.base}/get_item/{uuid}"

        return self.client.get(url)

    def reconfigure(self):
        """
        POST /api/interfaces/vip_settings/reconfigure
        """
        url = f"{self.base}/reconfigure"

        return self.client.post(url)

    def search_item(self, data=None):
        """
        POST /api/interfaces/vip_settings/search_item
        """
        url = f"{self.base}/search_item"

        return self.client.post(
            url,
            json=data,
        )

    def set(self, data):
        """
        POST /api/interfaces/vip_settings/set
        """
        url = f"{self.base}/set"

        return self.client.post(
            url,
            json=data,
        )

    def set_item(self, data, params):
        """
        POST /api/interfaces/vip_settings/set_item/<uuid>
        """
        uuid = params["uuid"]

        url = f"{self.base}/set_item/{uuid}"

        return self.client.post(
            url,
            json=data,
        )
