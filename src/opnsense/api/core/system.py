from opnsense.client import OPNsenseClient


class SystemAPI:
    """
    OPNsense Core System API
    module: core
    controller: system
    commands: dismiss_status, halt, reboot status 
    """

    def __init__(self, client: OPNsenseClient):
        self.client = client
        self.base = "/api/core/system"

    def status(self):
        """
        Get system status
        GET /api/core/system/status
        """
        return self.client.get("/api/core/system/status")

