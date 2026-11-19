from opnsense.client import OPNsenseClient


class OverviewAPI:
    """
    OPNsense Interfaces Overview API
    module: interfaces
    controller: overview
    """

    def __init__(self, client: OPNsenseClient):
        self.client = client
        self.base = "/api/interfaces/overview"

    def export(self):
        """
        Export interface configuration
        GET /api/interfaces/overview/export
        """
        return self.client.get(f"{self.base}/export")

    def get_interface(self, ifname: str | None = None):
        """
        Get interface details
        GET /api/interfaces/overview/get_interface/$if
        """
        if ifname:
            return self.client.get(f"{self.base}/get_interface/{ifname}")
        return self.client.get(f"{self.base}/get_interface")

    def interfaces_info(self, details: bool = False):
        """
        Get interface list and status
        GET /api/interfaces/overview/interfaces_info/$details
        """
        flag = "1" if details else "0"
        return self.client.get(f"{self.base}/interfaces_info/{flag}")

    def reload_interface(self, identifier: str | None = None):
        """
        Reload interface
        POST /api/interfaces/overview/reload_interface/$identifier
        """
        if identifier:
            return self.client.post(f"{self.base}/reload_interface/{identifier}")
        return self.client.post(f"{self.base}/reload_interface")

