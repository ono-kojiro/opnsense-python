import sys

import logging
logger = logging.getLogger(__name__)

from opnsense.client import OPNsenseClient


class VipSettingsAPI:
    """
    OPNsense Interfaces VIP Settings API
    module: interfaces
    controller: vip_settings
    """

    def __init__(self, client: OPNsenseClient):
        self.client = client
        self.base = "/api/interfaces/vip_settings"

    def add_item(self, data: dict, params: dict):
        return self.client.post(f"{self.base}/add_item", json=data)
    
    def add(self, data: dict, params: dict):
        return self.add_item(data, params)

    def del_item(self, data: dict, params: dict):
        res = self.get(data, params)
        items = res['vip']['vip']
        descr2uuid = {}
        for uuid in items :
            item = items[uuid]
            descr = item.get('descr')
            descr2uuid[descr] = uuid

        uuid = params.get('uuid', None)
        descr = params.get('descr', None)
        if not uuid and not descr:
            logging.error('no uuid/descr parameter')
            sys.exit(1)

        if descr :
            uuid = descr2uuid[descr]

        return self.client.post(f"{self.base}/del_item/{uuid}")
    
    def delete(self, data: dict, params: dict):
        return self.del_item(data, params)

    def get(self, data: dict, params: dict):
        return self.client.get(f"{self.base}/get")

    def get_item(self, data: dict, params: dict):
        uuid = params.get('uuid', None)
        if not uuid :
            logging.error('no uuid parameter')
            sys.exit(1)
        return self.client.get(f"{self.base}/get_item/{uuid}")

    def reconfigure(self, data: dict, params: dict):
        return self.client.post(f"{self.base}/reconfigure")

    def search_item(self, data: dict, params: dict):
        return self.client.post(f"{self.base}/search_item", json=data)

    def set(self, data: dict, params: dict):
        return self.client.post(f"{self.base}/set", json=data)

    def set_item(self, data: dict, params: dict):
        uuid = params.get('uuid', None)
        if not uuid :
            logging.error('no uuid parameter')
            sys.exit(1)
        return self.client.post(f"{self.base}/set_item/{uuid}")

