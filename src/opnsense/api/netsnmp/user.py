import sys
import os
import getopt

import json

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
        self.base   = "/api/netsnmp/user"

    def __add_user(self, mod, ctl, cmd):
        print('  options:')
        print('    username=...')
        print('    password=...')
        print('    enckey=...')
        print('    enabled=0 or enabled=1')
        print('')
        print('  NOTE:')
        print('    After adding user, run following command to save configuration')
        print('    $ opncli netsnmp service reconfigure')

    def add_user(self, data=None, params=None):
        """
        POST /api/netsnmp/user/add_user
        """
        ret = 0
        if not 'username' in data['user'] :
            print('ERROR: no username data')
            ret += 1
        if not 'password' in data['user'] :
            print('ERROR: no password data')
            ret += 1
        if not 'enckey' in data['user'] :
            print('ERROR: no enckey data')
            ret += 1
        if not 'enabled' in data['user'] :
            print('ERROR: no enabled data')
            ret += 1

        if ret :
            sys.exit(1)

        return self.client.post(f"{self.base}/add_user", json=data)
    
    def del_user(self, data=None, params=None):
        """
        POST /api/netsnmp/user/del_user
        """
        if not 'uuid' in params :
            logger.error("param 'uuid' is not defined")
            sys.exit(2)

        uuid = params['uuid']
        url = f"{self.base}/del_user/{uuid}"
        return self.client.post(url)
    
    def get(self):
        """
        GET /api/netsnmp/user/get
        """
        url = f"{self.base}/get"
        return self.client.get(url)

    def get_user(self, data=None):
        """
        GET /api/netsnmp/user/get_user
        """
        uuid = data['user']['uuid']
        url = f"{self.base}/get_user/{uuid}"
        return self.client.get(url)
    
    def search_user(self):
        """
        GET /api/netsnmp/user/search_user
        """
        url = f"{self.base}/search_user"
        return self.client.get(url)

    def set(self, data=None, params=None):
        """
        GET /api/netsnmp/user/set
        """
        url = f"{self.base}/set"
        return self.client.post(url, json=data)

    def set_user(self, data=None, params=None):
        """
        GET /api/netsnmp/user/set_user
        """
        uuid = params['uuid']
        url = f"{self.base}/set_user/{uuid}"
        return self.client.post(url, json=data)

    def toggle_user(self, params):
        """
        GET /api/netsnmp/user/toggle_user
        """
        uuid = params['uuid']
        url = f"{self.base}/toggle_user/{uuid}"
        return self.client.post(url)

