from opnsense.client import OPNsenseClient


class SettingsAPI:
    """
    OPNsense Interfaces Settings API
    module: interfaces
    controller: settings
    """

    def __init__(self, client: OPNsenseClient):
        self.client = client
        self.base = "/api/interfaces/settings"

    def get(self):
        """
        Get interface global settings
        GET /api/interfaces/settings/get
        """
        return self.client.get(f"{self.base}/get")

    def reconfigure(self):
        """
        Apply interface settings
        POST /api/interfaces/settings/reconfigure
        """
        return self.client.post(f"{self.base}/reconfigure")

    def set(self, data: dict):
        """
        Update interface settings
        POST /api/interfaces/settings/set
        """
        return self.client.post(f"{self.base}/set", json=data)

