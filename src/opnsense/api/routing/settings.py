# src/opnsense/api/routing/settings.py

import logging

from opnsense.client import OPNsenseClient


logger = logging.getLogger(__name__)


class SettingsAPI:
    """
    OPNsense Routing Settings API

    module: routing
    controller: settings

    commands:
        add_gateway
        del_gateway
        get
        get_gateway
        reconfigure
        search_gateway
        set
        set_gateway
        toggle_gateway
    """

    def __init__(self, client: OPNsenseClient):
        self.client = client
        self.base = "/api/routing/settings"

    def add_gateway(self, data):
        """
        POST /api/routing/settings/add_gateway
        """

        return self.client.post(
            f"{self.base}/add_gateway",
            json=data,
        )

    def del_gateway(self, params):
        """
        POST /api/routing/settings/del_gateway/<uuid>
        """

        uuid = params["uuid"]

        return self.client.post(
            f"{self.base}/del_gateway/{uuid}"
        )

    def get(self):
        """
        GET /api/routing/settings/get
        """

        return self.client.get(
            f"{self.base}/get"
        )

    def get_gateway(self, params):
        """
        GET /api/routing/settings/get_gateway/<uuid>
        """

        uuid = params["uuid"]

        return self.client.get(
            f"{self.base}/get_gateway/{uuid}"
        )

    def reconfigure(self):
        """
        POST /api/routing/settings/reconfigure
        """

        return self.client.post(
            f"{self.base}/reconfigure"
        )

    def search_gateway(self, data=None):
        """
        POST /api/routing/settings/search_gateway
        """

        return self.client.post(
            f"{self.base}/search_gateway",
            json=data,
        )

    def set_gateway(self, data, params):
        """
        POST /api/routing/settings/set_gateway/<uuid>
        """

        uuid = params["uuid"]

        return self.client.post(
            f"{self.base}/set_gateway/{uuid}",
            json=data,
        )

    def toggle_gateway(self, params):
        """
        POST /api/routing/settings/toggle_gateway/<uuid>
        """

        uuid = params["uuid"]

        return self.client.post(
            f"{self.base}/toggle_gateway/{uuid}"
        )
