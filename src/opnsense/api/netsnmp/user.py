# src/opnsense/api/netsnmp/user.py

import logging

from opnsense.client import OPNsenseClient


logger = logging.getLogger(__name__)


class UserAPI:
    """
    OPNsense NetSNMP User API

    module: netsnmp
    controller: user
    """

    def __init__(self, client: OPNsenseClient):
        self.client = client
        self.base = "/api/netsnmp/user"

    def add_user(self, data):
        """
        POST /api/netsnmp/user/add_user
        """

        return self.client.post(
            f"{self.base}/add_user",
            json=data,
        )

    def del_user(self, params):
        """
        POST /api/netsnmp/user/del_user/<uuid>
        """

        uuid = params["uuid"]

        return self.client.post(
            f"{self.base}/del_user/{uuid}"
        )

    def get(self):
        """
        GET /api/netsnmp/user/get
        """

        return self.client.get(
            f"{self.base}/get"
        )

    def get_user(self, params):
        """
        GET /api/netsnmp/user/get_user/<uuid>
        """

        uuid = params["uuid"]

        return self.client.get(
            f"{self.base}/get_user/{uuid}"
        )

    def search_user(self):
        """
        GET /api/netsnmp/user/search_user
        """

        return self.client.get(
            f"{self.base}/search_user"
        )

    def set(self, data):
        """
        POST /api/netsnmp/user/set
        """

        return self.client.post(
            f"{self.base}/set",
            json=data,
        )

    def set_user(self, data, params):
        """
        POST /api/netsnmp/user/set_user/<uuid>
        """

        uuid = params["uuid"]

        return self.client.post(
            f"{self.base}/set_user/{uuid}",
            json=data,
        )

    def toggle_user(self, params):
        """
        POST /api/netsnmp/user/toggle_user/<uuid>
        """

        uuid = params["uuid"]

        return self.client.post(
            f"{self.base}/toggle_user/{uuid}"
        )
