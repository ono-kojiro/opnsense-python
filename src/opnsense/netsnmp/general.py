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

    def get(self, json=None):
        """
        Get snmp general information.
        GET /api/netsnmp/general/get
        """
        return self.client.get("/api/netsnmp/general/get")
    
    def set(self, json=None):
        """
        Set snmp general information.
        POST /api/netsnmp/general/set
        """
        return self.client.set("/api/netsnmp/general/set", json=json)

