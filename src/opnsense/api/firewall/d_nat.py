from opnsense.client import OPNsenseClient


class DNatAPI:
    """
    OPNsense Firewall Destination NAT API
    module: firewall
    controller: d_nat
    """

    def __init__(self, client: OPNsenseClient):
        self.client = client

    def search(self, query: dict | None = None):
        """
        Search DNAT rules.
        POST /api/firewall/d_nat/searchRule
        """
        return self.client.post("/api/firewall/d_nat/searchRule", json=query or {})

    def get_rule(self, uuid: str):
        """
        Get a single DNAT rule by UUID.
        GET /api/firewall/d_nat/getRule/<uuid>
        """
        return self.client.get(f"/api/firewall/d_nat/getRule/{uuid}")

    def add_rule(self, rule_data: dict):
        """
        Add a DNAT rule.
        POST /api/firewall/d_nat/addRule
        """
        return self.client.post("/api/firewall/d_nat/addRule", json=rule_data)

    def set_rule(self, uuid: str, rule_data: dict):
        """
        Update a DNAT rule.
        POST /api/firewall/d_nat/setRule/<uuid>
        """
        return self.client.post(f"/api/firewall/d_nat/setRule/{uuid}", json=rule_data)

    def delete_rule(self, uuid: str):
        """
        Delete a DNAT rule.
        POST /api/firewall/d_nat/delRule/<uuid>
        """
        return self.client.post(f"/api/firewall/d_nat/delRule/{uuid}")

    def toggle_rule(self, uuid: str):
        """
        Enable/disable a DNAT rule.
        POST /api/firewall/d_nat/toggleRule/<uuid>
        """
        return self.client.post(f"/api/firewall/d_nat/toggleRule/{uuid}")

    def apply(self):
        """
        Apply DNAT changes.
        POST /api/firewall/d_nat/apply
        """
        return self.client.post("/api/firewall/d_nat/apply")

