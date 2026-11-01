import sys

import logging
logger = logging.getLogger(__name__)

from opnsense.client import OPNsenseClient

class AssignmentAPI:
    """
    OPNsense Interfaces Assignment API
    module: interfaces
    controller: assginment
    """

    def __init__(self, client: OPNsenseClient):
        self.client = client
        self.base = "/api/interfaces/assignment"

    def add_item(self, data, params):
        return self.client.post(f"{self.base}/add_item", json=data)

    def del_item(self, data, params):
        ifnames = params.get('ifnames', None)
        if not ifnames :
            logger.error('no ifnames parameter')
            sys.exit(1)

        return self.client.post(f"{self.base}/del_item/{ifnames}")

    def get(self, data, params):
        return self.client.get(f"{self.base}/get")

    def get_item(self, data, params) :
        ifname = params.get('ifname', None)
        if not ifname :
            logger.error('no ifname parameter')
            sys.exit(1)

        return self.client.get(f"{self.base}/get_item/{ifname}")
    
    def pending(self, data, params):
        return self.client.get(f"{self.base}/pending")

    def reconfigure(self, data, params):
        return self.client.post(f"{self.base}/reconfigure")

    def search_item(self, data, params) :
        return self.client.post(f"{self.base}/search_item")

    def set(self, data, params) :
        return self.client.post(f"{self.base}/set", json=data)

    def set_item(self, data, params):
        ifname = params.get('ifname', None)
        if not ifname :
            logger.error('no ifname parameter')
            sys.exit(1)
        return self.client.post(f"{self.base}/set_item/{ifname}")

