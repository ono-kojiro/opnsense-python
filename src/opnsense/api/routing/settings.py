import sys
import re

import logging
logger = logging.getLogger(__name__)

from opnsense.client import OPNsenseClient

class SettingsAPI:
    """
    OPNsense Routing Settings API
    module: routing
    controller: settings
    commands: add_gateway, del_gateway, get, get_gateway, reconfigure
      search_gateway, set, set_gateway, toggle_gateway
    """

    def __init__(self, client: OPNsenseClient):
        self.client = client
        self.base = "/api/routing/settings"

    def add_gateway(self, data=None, params=None):
        cmd = 'add_gateway'
        return self.client.post(f"{self.base}/{cmd}", json=data)

    def del_gateway(self, data=None, params=None):
        cmd = 'del_gateway'
        uuid = params['uuid']
        return self.client.post(f"{self.base}/{cmd}/{uuid}", json=data)

    def get(self, data=None, params=None):
        return self.client.get(f"{self.base}/get")

    def get_gateway(self, data=None, params=None):
        cmd = 'get_gateway'
        uuid = params['uuid']
        return self.client.get(f"{self.base}/{cmd}/{uuid}")
    
    def reconfigure(self, data=None, params=None):
        cmd = 'reconfigure'
        return self.client.post(f"{self.base}/{cmd}")

    def search_gateway(self, data=None, params=None):
        return self.client.post(
            f"{self.base}/search_gateway",
            json=data
        )

    def set_gateway(self, data=None, params=None):
        cmd = 'set_gateway'
        uuid = params['uuid']
        return self.client.post(f"{self.base}/{cmd}/{uuid}", json=data)

    def delete(self, data=None, params=None):
        return self.del_gateway(data, params)

    def toggle_gateway(self, data=None, params=None):
        cmd='toggle_gateway'
        uuid = params['uuid']
        return self.client.post(f"{self.base}/{cmd}/{uuid}", json=data)

