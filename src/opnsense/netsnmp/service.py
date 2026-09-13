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

    def reconfigure(self, json=None):
        """
        POST /api/netsnmp/service/reconfigure
        """
        return self.client.post("/api/netsnmp/service/reconfigure")
    
    def restart(self, json=None):
        """
        POST /api/netsnmp/service/restart
        """
        return self.client.post("/api/netsnmp/service/restart")

    def start(self, json=None):
        """
        POST /api/netsnmp/service/start
        """
        return self.client.post("/api/netsnmp/service/start")
    
    def status(self, json=None):
        """
        GET /api/netsnmp/service/status
        """
        return self.client.get("/api/netsnmp/service/status")
    
    def stop(self, json=None):
        """
        POST /api/netsnmp/service/stop
        """
        return self.client.post("/api/netsnmp/service/stop")

