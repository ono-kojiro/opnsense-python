from opnsense.client import OPNsenseClient


class LaggSettingsAPI:
    """
    OPNsense Interfaces LAGG Settings API
    module: interfaces
    controller: lagg_settings
    """

    def __init__(self, client: OPNsenseClient):
        self.client = client
        self.base = "/api/interfaces/lagg_settings"

    def add_item(self, data: dict):
        return self.client.post(f"{self.base}/add_item", json=data)

    def del_item(self, uuid: str):
        return self.client.post(f"{self.base}/del_item/{uuid}")

    def get(self):
        return self.client.get(f"{self.base}/get")

    def get_item(self, uuid: str | None = None):
        if uuid:
            return self.client.get(f"{self.base}/get_item/{uuid}")
        return self.client.get(f"{self.base}/get_item")

    def get_lagg_protocols(self):
        return self.client.get(f"{self.base}/get_lagg_protocols")

    def reconfigure(self):
        return self.client.post(f"{self.base}/reconfigure")

    def search_item(self, query: dict | None = None):
        return self.client.post(f"{self.base}/search_item", json=query or {})

    def set(self, data: dict):
        return self.client.post(f"{self.base}/set", json=data)

    def set_item(self, uuid: str, data: dict):
        return self.client.post(f"{self.base}/set_item/{uuid}", json=data)

