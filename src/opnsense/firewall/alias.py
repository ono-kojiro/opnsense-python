from opnsense.client import OPNsenseClient


class AliasAPI:
    """
    OPNsense Firewall Alias API
    module: firewall
    controller: alias
    """

    def __init__(self, client: OPNsenseClient):
        self.client = client

    def get(self, json=None):
        """
        Get all aliases.
        GET /api/firewall/alias/get
        """
        return self.client.get("/api/firewall/alias/get")

    def search_item(self, query: dict | None = None):
        """
        Search aliases.
        POST /api/firewall/alias/search_item
        """
        return self.client.post("/api/firewall/alias/search_item", json=query or {})

    def list_categories(self, json=None):
        """
        list categories
        GET /api/firewall/alias/list_categories
        """
        return self.client.get("/api/firewall/alias/list_categories")
    
    def list_countries(self, json=None):
        """
        list countries
        GET /api/firewall/alias/list_countries
        """
        return self.client.get("/api/firewall/alias/list_countries")
    
    def list_network_aliases(self, json=None):
        """
        list network_aliases
        GET /api/firewall/alias/list_network_aliases
        """
        return self.client.get("/api/firewall/alias/list_network_aliases")
    
    def list_user_groups(self, json=None):
        """
        list user groups
        GET /api/firewall/alias/list_user_groups
        """
        return self.client.get("/api/firewall/alias/list_user_groups")
    
    def reconfigure(self, json=None):
        """
        reconfigure
        POST /api/firewall/alias/reconfigure
        """
        return self.client.post(f"/api/firewall/alias/reconfigure")

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

