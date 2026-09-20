import sys

from opnsense.client import OPNsenseClient

import logging
logger = logging.getLogger(__name__)

class CategoryAPI:
    """
    OPNsense Firewall Category API
    module: firewall
    controller: category
    """

    def __init__(self, client: OPNsenseClient):
        self.client = client
        self.base   = "/api/firewall/category"

    def get(self, json=None, params=None):
        """
        Get categories.
        GET /api/firewall/category/get
        """
        return self.client.get("{0}/get".format(self.base))

    def search_item(self, json=None, params=None):
        """
        Search categories.
        POST /api/firewall/category/search_item
        """
        return self.client.post("{0}/search_item".format(self.base), json=json)

    def __add_item(self, mod, ctl, cmd) :
        msg = '''
  ex.
        $ opncli firewall category add_item name=blue color="0000ff"
'''
        print(msg)

    def add_item(self, json=None, params=None):
        """
        Add category.
        POST /api/firewall/category/add_item
        """
        logger.debug(json)
        return self.client.post("{0}/add_item".format(self.base), json=json)

    def __add(self, mod, ctl, cmd):
        return self.__add_item(mod, ctl, cmd)

    def add(self, json=None, params=None):
        return self.add_item(json, params)

    def set(self, json=None, params=None):
        """
        Update category.
        POST /api/firewall/category/setCategory/<uuid>
        """
        if not 'uuid' in params:
            logging.error('no uuid parameter')
            sys.exit(1)

        uuid = params['uuid']
        return self.client.post("{0}/set/{1}".format(self.base, uuid), json=json)

    def del_item(self, json=None, params=None):
        """
        Delete category.
        POST /api/firewall/category/del_item/<uuid>
        """
        uuid = None

        if 'name' in params :
            name = params['name']

            res = self.search_item()
            for row in res['rows'] :
                if row['name'] == name :
                    uuid = row['uuid']
        elif 'uuid' in params :
            uuid = params['uuid']
        else :
            logging.error('no uuid parameter and name parameter')
            sys.exit(1)

        return self.client.post("{0}/del_item/{1}".format(self.base, uuid))

    def apply(self, json=None, params=None):
        """
        Apply category changes.
        POST /api/firewall/category/apply
        """
        return self.client.post("{0}/apply".format(self.base))

