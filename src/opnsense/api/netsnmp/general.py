import sys
import os
import getopt

import json

import logging

from opnsense.client import OPNsenseClient

logger = logging.getLogger(__name__)

class NetSnmpGeneralAPI:
    """
    OPNsense NetSNMP API
    module: netsnmp
    controller: general
    """

    def __init__(self, client: OPNsenseClient):
        self.client = client

    def get(self, data=None, params=None):
        """
        Get snmp general information.
        GET /api/netsnmp/general/get
        """
        return self.client.get("/api/netsnmp/general/get")

    def __set(self, mod, ctl, cmd) :
        msg = '''
ex.
  $ opncli netsnmp general set enabled=1
  $ opncli netsnmp service reconfigure
'''
        print(msg)

    def set(self, data=None, params=None):
        """
        Set snmp general information.
        POST /api/netsnmp/general/set
        """
        return self.client.set("/api/netsnmp/general/set", json=data)

