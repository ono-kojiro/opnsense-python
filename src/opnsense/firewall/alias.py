from opnsense.client import OPNsenseClient


class AliasAPI:
    """
    OPNsense Firewall Alias API
    module: firewall
    controller: alias
    """

    def __init__(self, client: OPNsenseClient):
        self.client = client

    def get(self):
        """
        Get all aliases.
        GET /api/firewall/alias/get
        """
        return self.client.get("/api/firewall/alias/get")

    def search(self, query: dict | None = None):
        """
        Search aliases.
        POST /api/firewall/alias/searchAlias
        """
        return self.client.post("/api/firewall/alias/searchAlias", json=query or {})

    def add(self, alias_data: dict):
        """
        Add alias.
        POST /api/firewall/alias/addAlias
        """
        return self.client.post("/api/firewall/alias/addAlias", json=alias_data)

    def set(self, uuid: str, alias_data: dict):
        """
        Update alias.
        POST /api/firewall/alias/setAlias/<uuid>
        """
        return self.client.post(f"/api/firewall/alias/setAlias/{uuid}", json=alias_data)

    def delete(self, uuid: str):
        """
        Delete alias.
        POST /api/firewall/alias/delAlias/<uuid>
        """
        return self.client.post(f"/api/firewall/alias/delAlias/{uuid}")

    def apply(self):
        """
        Apply alias changes.
        POST /api/firewall/alias/apply
        """
        return self.client.post("/api/firewall/alias/apply")

