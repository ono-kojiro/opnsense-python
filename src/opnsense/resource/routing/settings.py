# src/opnsense/resource/routing/settings.py

import logging

from opnsense.api.routing.settings import SettingsAPI

logger = logging.getLogger(__name__)


class Settings(SettingsAPI):

    def _find_uuid(self, name):

        res = self.search_gateway()

        for row in res["rows"]:

            if row["name"] == name:
                return row["uuid"]

        raise ValueError(
            f"gateway '{name}' not found"
        )

    def _resolve_uuid(self, params):

        if "uuid" in params:
            return params

        if "name" not in params:
            raise ValueError(
                "no uuid parameter and name parameter"
            )

        params = dict(params)

        params["uuid"] = self._find_uuid(
            params["name"]
        )

        return params

    #
    # aliases
    #

    def delete(self, params):

        return self.del_gateway(params)

    #
    # extended methods
    #

    def get_gateway(self, params):
        """
        Supports:

            uuid=<uuid>

        or

            name=<name>
        """

        params = self._resolve_uuid(params)

        return super().get_gateway(params)

    def set_gateway(self, data, params):
        """
        Supports:

            uuid=<uuid>

        or

            name=<name>

        Convert CLI style payload:

            {
                "gateway": {
                    "disabled": "0"
                }
            }

        into GUI compatible payload:

            {
                "gateway_item": {
                    ...
                }
            }
        """

        params = self._resolve_uuid(params)

        current = super().get_gateway(params)

        item = current["gateway_item"]

        updates = data.get(
            "gateway",
            {}
        )

        item.update(updates)

        #
        # convert selection objects
        # into form values expected
        # by set_gateway()
        #

        interface = item.get("interface")

        if isinstance(interface, dict):

            for key, value in interface.items():

                if value.get("selected") == 1:
                    item["interface"] = key
                    break

        ipprotocol = item.get("ipprotocol")

        if isinstance(ipprotocol, dict):

            for key, value in ipprotocol.items():

                if value.get("selected") == 1:
                    item["ipprotocol"] = key
                    break

        return super().set_gateway(
            {
                "gateway_item": item
            },
            params,
        )

    def del_gateway(self, params):
        """
        Supports:

            uuid=<uuid>

        or

            name=<name>
        """

        params = self._resolve_uuid(params)

        return super().del_gateway(params)

    def toggle_gateway(self, params):
        """
        Supports:

            uuid=<uuid>

        or

            name=<name>
        """

        params = self._resolve_uuid(params)

        return super().toggle_gateway(params)
