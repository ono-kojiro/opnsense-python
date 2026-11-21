# src/opnsense/resource/firewall/alias.py

import logging
import textwrap

from opnsense.api.firewall.alias import AliasAPI
from opnsense.resource.firewall.category import Category

logger = logging.getLogger(__name__)


class Alias(AliasAPI):

    def _find_uuid(self, name):
        res = self.get_alias_u_u_i_d(
            params={
                "name": name,
            }
        )

        uuid = res.get("uuid")

        if not uuid:
            raise ValueError(
                f'alias "{name}" not found'
            )

        return uuid

    def _convert_categories(self, data):
        alias = data.get("alias", {})

        categories = alias.get("categories")

        if not categories:
            return data

        category_api = Category(self.client)

        res = category_api.get()

        cat_uuids = res["category"]["categories"]["category"]

        cat2uuid = {}

        for uuid in cat_uuids:
            name = cat_uuids[uuid]["name"]
            cat2uuid[name] = uuid

        values = []

        for token in categories.split(","):
            token = token.strip()

            uuid = cat2uuid.get(token)

            if uuid is None:
                raise ValueError(
                    f'category "{token}" not found'
                )

            values.append(uuid)

        alias["categories"] = ",".join(values)

        return data

    #
    # alias
    #

    def add(self, data):
        return self.add_item(data)

    def delete(self, params):
        return self.del_item(params)

    #
    # extended add_item()
    #

    def add_item(self, data):
        data = self._convert_categories(data)

        return super().add_item(data)

    #
    # extended set_item()
    #

    def set_item(self, data, params):

        if "uuid" not in params:

            if "name" not in params:
                raise ValueError(
                    "no uuid parameter and name parameter"
                )

            params = dict(params)

            params["uuid"] = self._find_uuid(
                params["name"]
            )

        data = self._convert_categories(data)

        return super().set_item(data, params)

    #
    # extended del_item()
    #

    def del_item(self, params):

        if "uuid" not in params:

            if "name" not in params:
                raise ValueError(
                    "no uuid parameter and name parameter"
                )

            params = dict(params)

            params["uuid"] = self._find_uuid(
                params["name"]
            )

        return super().del_item(params)

    #
    # extended toggle_item()
    #

    def toggle_item(self, params):

        if "uuid" not in params:

            if "name" not in params:
                raise ValueError(
                    "no uuid parameter and name parameter"
                )

            params = dict(params)

            params["uuid"] = self._find_uuid(
                params["name"]
            )

        return super().toggle_item(params)

    #
    # help messages
    #

    def __add_item(self, mod, ctl, cmd):
        msg = '''
            ex.
              $ opncli firewall alias add \
                  name=myalias type=host content=192.168.1.1
        '''
        print(textwrap.dedent(msg).strip())

    def __search_item(self, mod, ctl, cmd):
        msg = '''
            ex.
              $ opncli firewall alias search_item

              $ opncli firewall alias search_item \
                  | jq '.rows[] | select(.name == "myalias")'

              $ opncli firewall alias search_item \
                  | jq '.rows[] | select(.name == "myalias") | { name, type, content }'
        '''
        print(textwrap.dedent(msg).strip())

    def __del_item(self, mod, ctl, cmd):
        msg = '''
            ex.
              $ opncli firewall alias del_item name=myalias

              $ opncli firewall alias del_item uuid=xxxxx
        '''
        print(textwrap.dedent(msg).strip())

