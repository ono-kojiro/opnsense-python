# src/opnsense/resource/firewall/category.py

from opnsense.api.firewall.category import CategoryAPI

import logging
logger = logging.getLogger(__name__)

class Category(CategoryAPI):
    def _find_uuid(self, name):
        res = self.search_item()

        for row in res['rows']:
            if row['name'] == name:
                return row['uuid']

        raise ValueError(
            f"category '{name}' not found"
        )        

    def __add_item(self, mod, ctl, cmd):
        msg = '''
  ex.
        $ opncli firewall category add_item name=blue color="0000ff"
'''
        print(msg)

    def __add(self, mod, ctl, cmd):
        return self.__add_item(mod, ctl, cmd)

    def add(self, data):
        """
        Alias of add_item()
        """
        return self.add_item(data)

    def set(self, data, params):
        """
        Extended set().
        Supports:

            uuid=<uuid>

        or

            name=<name>
        """

        if 'uuid' not in params:

            if 'name' not in params:
                raise ValueError("no uuid parameter and name parameter")

            params = dict(params)
            params['uuid'] = self._find_uuid(
                params['name']
            )

        return super().set(data, params)

    def del_item(self, params):
        """
        Extended delete.

        Supports:

            uuid=<uuid>

        or

            name=<name>
        """

        if 'uuid' not in params:
            if 'name' not in params:
                raise ValueError("no uuid parameter and name parameter")

            params = dict(params)
            params['uuid'] = self._find_uuid(
                params['name']
            )

        return super().del_item(params)

    def delete(self, params):
        """
        Alias of del_item()
        """
        return self.del_item(params)

