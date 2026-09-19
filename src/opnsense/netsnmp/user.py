import sys
import os
import getopt

import json

import logging

from opnsense.client import OPNsenseClient

logger = logging.getLogger(__name__)

class NetSnmpUserAPI:
    """
    OPNsense NetSNMP User API
    module: netsnmp
    controller: user
    """

    def __init__(self, client: OPNsenseClient):
        self.client = client

    def add_user(self, data=None):
        """
        POST /api/netsnmp/user/add_user
        """
        return self.client.post("/api/netsnmp/user/add_user", json=data)
    
    def del_user(self, data=None, params=None):
        """
        POST /api/netsnmp/user/del_user
        """
        if not 'uuid' in params :
            logger.error("param 'uuid' is not defined")
            sys.exit(2)

        param = params['uuid']
        url = "/api/netsnmp/user/del_user/{0}".format(param)
        return self.client.post(url)
    
    def get(self, json=None, params=None):
        """
        GET /api/netsnmp/user/get
        """
        url = "/api/netsnmp/user/get"
        return self.client.get(url)

    def get_user(self, data=None):
        """
        GET /api/netsnmp/user/get_user
        """
        param = data['user']['uuid']
        url = "/api/netsnmp/user/get_user/{0}".format(param)
        return self.client.get(url)
    
    def search_user(self, data=None):
        """
        GET /api/netsnmp/user/search_user
        """
        url = "/api/netsnmp/user/search_user"
        return self.client.get(url)

    def set(self, data=None):
        """
        GET /api/netsnmp/user/set
        """
        url = "/api/netsnmp/user/set"
        return self.client.post(url, json=data)

    def set_user(self, data=None):
        """
        GET /api/netsnmp/user/set_user
        """
        param = data['user']['uuid']
        url = "/api/netsnmp/user/set_user/{0}".format(param)
        return self.client.post(url, json=data)

    def toggle_user(self, data=None):
        """
        GET /api/netsnmp/user/toggle_user
        """
        param = data['user']['uuid']
        url = "/api/netsnmp/user/toggle_user/{0}".format(param)
        return self.client.post(url, json=data)

