from opnsense.client import OPNsenseClient


class CoreSystemAPI:
    """
    OPNsense Core System API
    module: core
    controller: system
    commands: dismiss_status, halt, reboot status 
    """

    def __init__(self, client: OPNsenseClient):
        self.client = client

    def status(self, data=None, params=None):
        """
        Get system status
        GET /api/core/system/status
        """
        return self.client.get("/api/core/system/status")

