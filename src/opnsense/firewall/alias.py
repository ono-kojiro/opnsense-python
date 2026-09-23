import sys
import textwrap

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
    
    def add_item(self, data=None, params=None):
        """
        Add alias.
        POST /api/firewall/alias/add_item
        """
        url = "{0}/add_item".format(self.base)
        return self.client.post(url, json=data)
    
    def del_item(self, data=None, params=None):
        uuid = None

        # custom parameter
        name = params.get('name', None)
        if name :
            res = self.get_alias_u_u_i_d(data, params)
            if 'uuid' in res :
                uuid = res.get('uuid', None)
        elif 'uuid' in params :
            uuid = params.get('uuid')

        if not uuid :
            logger.error("no uuid/name parameter")
            sys.exit(1)

        url = "{0}/del_item/{1}".format(self.base, uuid)
        return self.client.post(url, json=data)
   
    # save
    def save(self, data=None, params=None):
        url = "{0}/export".format(self.base)
        return self.client.post(url, json=data)

    def get(self, data=None, params=None):
        """
        Get all aliases.
        GET /api/firewall/alias/get
        """
        url = "{0}/get".format(self.base)
        return self.client.get(url)
    
    def get_alias_u_u_i_d(self, data=None, params=None):
        name = params.get('name', None)
        if not name :
            logger.error("no name parameter")
            sys.exit(1)
        url = "{0}/get_alias_u_u_i_d/{1}".format(self.base, name)
        return self.client.get(url)
    
    def get_geo_i_p(self, data=None, params=None):
        url = "{0}/get_geo_i_p".format(self.base)
        return self.client.get(url)
    
    def get_item(self, data=None, params=None):
        uuid = params.get('uuid', None)
        if not uuid :
            logger.error("no uuid parameter")
            sys.exit(1)
        
        url = "{0}/get_item/{1}".format(self.base, uuid)
        return self.client.get(url)
    
    def get_table_size(self, data=None, params=None):
        url = "{0}/get_table_size".format(self.base)
        return self.client.get(url)
    
    # import
    def load(self, data=None, params=None):
        url = "{0}/import".format(self.base)
        return self.client.post(url, json=data)

    def list_categories(self, data=None, params=None):
        """
        list categories
        GET /api/firewall/alias/list_categories
        """
        return self.client.get("/api/firewall/alias/list_categories")
    
    def list_countries(self, data=None, params=None):
        """
        list countries
        GET /api/firewall/alias/list_countries
        """
        return self.client.get("/api/firewall/alias/list_countries")
    
    def list_network_aliases(self, data=None, params=None):
        """
        list network_aliases
        GET /api/firewall/alias/list_network_aliases
        """
        return self.client.get("/api/firewall/alias/list_network_aliases")
    
    def list_user_groups(self, data=None, params=None):
        """
        list user groups
        GET /api/firewall/alias/list_user_groups
        """
        return self.client.get("/api/firewall/alias/list_user_groups")
    
    def reconfigure(self, data=None, params=None):
        """
        reconfigure
        POST /api/firewall/alias/reconfigure
        """
        return self.client.post(f"/api/firewall/alias/reconfigure")
    
    def search_item(self, data=None, params=None):
        """
        Search aliases.
        POST /api/firewall/alias/search_item
        """
        url = "{0}/search_item".format(self.base)
        return self.client.post(url, json=data)

    def set(self, data=None, params=None):
        """
        Update alias.
        POST /api/firewall/alias/setAlias/<uuid>
        """
        url = "{0}/set".format(self.base)
        return self.client.post(url, json=data)
    
    def set_item(self, data=None, params=None):
        uuid = None

        # custom parameter
        name = params.get('name', None)
        if name :
            res = self.get_alias_u_u_i_d(data, params)
            if 'uuid' in res :
                uuid = res.get('uuid', None)
        elif 'uuid' in params :
            uuid = params.get('uuid')

        if not uuid :
            logger.error("no uuid/name parameter")
            sys.exit(1)

        url = "{0}/set_item/{1}".format(self.base, uuid)
        return self.client.post(url, json=data)
    
    def toggle_item(self, data=None, params=None):
        uuid = None

        # custom parameter
        name = params.get('name', None)
        if name :
            res = self.get_alias_u_u_i_d(data, params)
            if 'uuid' in res :
                uuid = res.get('uuid', None)
        elif 'uuid' in params :
            uuid = params.get('uuid')

        enabled = params.get('enabled', None)

        if not uuid or not enabled :
            logger.error("no uuid/name/enabled parameter")
            sys.exit(1)

        url = "{0}/set_item/{1}&enabled={2}".format(
                self.base, uuid, enabled)

        return self.client.post(url, json=data)

    #
    # optional
    #
    def add(self, data=None, params=None):
        return self.add_item(data, params)
    
    def delete(self, data=None, params=None):
        return self.del_item(data, params)

    #
    # help message
    #
    def __add_item(self, mod, ctl, cmd):
        msg = '''
            ex.
              $ opncli firewall alias add \\
                  name=myalias type=host content=192.168.1.1
        '''
        msg = textwrap.dedent(msg).strip()
        print(msg)
   
    def __search_item(self, mod, ctl, cmd):
        msg = '''

            ex.
              $ opncli firewall alias search_item 

              $ opncli firewall alias search_item \\
                  | jq '.rows[] | select(.name == "myalias")'

              $ $ opncli firewall alias search_item \\
                  | jq '.rows[] | select(.name == "myalias") | { name, type, content }'
        '''
        msg = textwrap.dedent(msg).strip()
        print(msg)

    def __del_item(self, mod, ctl, cmd):
        msg = '''
            ex.
              $ opncli firewall alias del_item --name=myalias

              $ opncli firewall alias del_item --uuid=xxxxx
        '''
        msg = textwrap.dedent(msg).strip()
        print(msg)
        pass


