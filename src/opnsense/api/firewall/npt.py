from opnsense.client import OPNsenseClient


class NptAPI:
    """
    OPNsense Firewall NPT (Network Prefix Translation) API
    module: firewall
    controller: npt
    """

    def __init__(self, client: OPNsenseClient):
        self.client = client

    def search(self, query: dict | None = None):
        """
        Search NPT rules.
        POST /api/firewall/npt/searchRule
        """
        return self.client.post("/api/firewall/npt/searchRule", json=query or {})

    def get_rule(self, uuid: str):
        """
        Get a single NPT rule by UUID.
        GET /api/firewall/npt/getRule/<uuid>
        """
        return self.client.get(f"/api/firewall/npt/getRule/{uuid}")

    def add_rule(self, rule_data: dict):
        """
        Add an NPT rule.
        POST /api/firewall/npt/addRule
        """
        return self.client.post("/api/firewall/npt/addRule", json=rule_data)

    def set_rule(self, uuid: str, rule_data: dict):
        """
        Update an NPT rule.
        POST /api/firewall/npt/setRule/<uuid>
        """
        return self.client.post(f"/api/firewall/npt/setRule/{uuid}", json=rule_data)

    def delete_rule(self, uuid: str):
        """
        Delete an NPT rule.
        POST /api/firewall/npt/delRule/<uuid>
        """
        return self.client.post(f"/api/firewall/npt/delRule/{uuid}")

    def toggle_rule(self, uuid: str):
        """
        Enable/disable an NPT rule.
        POST /api/firewall/npt/toggleRule/<uuid>
        """
        return self.client.post(f"/api/firewall/npt/toggleRule/{uuid}")

    def apply(self):
        """
        Apply NPT changes.
        POST /api/firewall/npt/apply
        """
        return self.client.post("/api/firewall/npt/apply")

