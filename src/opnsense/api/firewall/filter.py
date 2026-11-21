# src/opnsense/api/firewall/filter.py

from opnsense.client import OPNsenseClient

import logging

logger = logging.getLogger(__name__)


class FilterAPI:
    """
    OPNsense Firewall Filter API

    module: firewall
    controller: filter
    """

    def __init__(self, client: OPNsenseClient):
        self.client = client
        self.base = "/api/firewall/filter"

    #
    # Basic operations
    #

    def get_rule(self, params):
        """
        GET /api/firewall/filter/get_rule/<uuid>
        """

        uuid = params["uuid"]

        url = f"{self.base}/get_rule/{uuid}"

        return self.client.get(url)

    def search_rule(self, data=None):
        """
        POST /api/firewall/filter/search_rule
        """

        url = f"{self.base}/search_rule"

        return self.client.post(
            url,
            json=data
        )

    def add_rule(self, data):
        """
        POST /api/firewall/filter/add_rule
        """

        url = f"{self.base}/add_rule"

        return self.client.post(
            url,
            json=data
        )

    def set_rule(self, data, params):
        """
        POST /api/firewall/filter/set_rule/<uuid>
        """

        uuid = params["uuid"]

        url = f"{self.base}/set_rule/{uuid}"

        return self.client.post(
            url,
            json=data
        )

    def del_rule(self, params):
        """
        POST /api/firewall/filter/del_rule/<uuid>
        """

        uuid = params["uuid"]

        url = f"{self.base}/del_rule/{uuid}"

        return self.client.post(url)

    def toggle_rule(self, params):
        """
        POST /api/firewall/filter/toggleRule/<uuid>
        """

        uuid = params["uuid"]

        url = f"{self.base}/toggleRule/{uuid}"

        return self.client.post(url)

    #
    # Apply
    #

    def apply(self):
        """
        POST /api/firewall/filter/apply
        """

        url = f"{self.base}/apply"

        return self.client.post(url)

    #
    # Utility
    #

    @staticmethod
    def prune_selected(obj):
        """
        Recursively remove items where
        selected == 0
        """

        if (
            isinstance(obj, dict)
            and "selected" in obj
        ):
            return (
                obj
                if obj["selected"] == 1
                else None
            )

        if isinstance(obj, dict):

            new_obj = {}

            for key, value in obj.items():

                pruned = (
                    FilterAPI.prune_selected(
                        value
                    )
                )

                if pruned is not None:
                    new_obj[key] = pruned

            return new_obj

        if isinstance(obj, list):

            new_list = []

            for item in obj:

                pruned = (
                    FilterAPI.prune_selected(
                        item
                    )
                )

                if pruned is not None:
                    new_list.append(pruned)

            return new_list

        return obj
