from opnsense.client import OPNsenseClient


class SourceNatAPI:
    """
    OPNsense Firewall Source NAT API
    module: firewall
    controller: source_nat
    """

    def __init__(self, client: OPNsenseClient):
        self.client = client

    def search(self, query: dict | None = None):
        """
        Search Source NAT rules.
        POST /api/firewall/source_nat/searchRule
        """
        return self.client.post("/api/firewall/source_nat/searchRule", json=query or {})

    def get_rule(self, uuid: str):
        """
        Get a single Source NAT rule by UUID.
        GET /api/firewall/source_nat/getRule/<uuid>
        """
        return self.client.get(f"/api/firewall/source_nat/getRule/{uuid}")

    def add_rule(self, rule_data: dict):
        """
        Add a Source NAT rule.
        POST /api/firewall/source_nat/addRule
        """
        return self.client.post("/api/firewall/source_nat/addRule", json=rule_data)

    def set_rule(self, uuid: str, rule_data: dict):
        """
        Update a Source NAT rule.
        POST /api/firewall/source_nat/setRule/<uuid>
        """
        return self.client.post(f"/api/firewall/source_nat/setRule/{uuid}", json=rule_data)

    def delete_rule(self, uuid: str):
        """
        Delete a Source NAT rule.
        POST /api/firewall/source_nat/delRule/<uuid>
        """
        return self.client.post(f"/api/firewall/source_nat/delRule/{uuid}")

    def toggle_rule(self, uuid: str):
        """
        Enable/disable a Source NAT rule.
        POST /api/firewall/source_nat/toggleRule/<uuid>
        """
        return self.client.post(f"/api/firewall/source_nat/toggleRule/{uuid}")

    def apply(self):
        """
        Apply Source NAT changes.
        POST /api/firewall/source_nat/apply
        """
        return self.client.post("/api/firewall/source_nat/apply")

