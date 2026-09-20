import sys
import os
import getopt

import json

import logging

from opnsense.client import OPNsenseClient

logger = logging.getLogger(__name__)

class NetSnmpServiceAPI:
    """
    OPNsense NetSNMP Service API
    module: netsnmp
    controller: general
    """

    def __init__(self, client: OPNsenseClient):
        self.client = client
        self.base   = "/api/netsnmp/service"

    def reconfigure(self, data=None, params=None):
        """
        POST /api/netsnmp/service/reconfigure
        """
        return self.client.post("{0}/reconfigure".format(self.base))
    
    def restart(self, data=None, params=None):
        """
        POST /api/netsnmp/service/restart
        """
        return self.client.post("{0}/restart".format(self.base))

    def start(self, data=None, params=None):
        """
        POST /api/netsnmp/service/start
        """
        return self.client.post("{0}/start".format(self.base))
    
    def status(self, data=None, params=None):
        """
        GET /api/netsnmp/service/status
        """
        return self.client.get("{0}/status".format(self.base))
    
    def stop(self, data=None, params=None):
        """
        POST /api/netsnmp/service/stop
        """
        return self.client.post("{0}/stop".format(self.base))

