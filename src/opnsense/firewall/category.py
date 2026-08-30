from opnsense.client import OPNsenseClient


class CategoryAPI:
    """
    OPNsense Firewall Category API
    module: firewall
    controller: category
    """

    def __init__(self, client: OPNsenseClient):
        self.client = client

    def get(self, json=None):
        """
        Get categories.
        GET /api/firewall/category/get
        """
        return self.client.get("/api/firewall/category/get")

    def search_item(self, query: dict | None = None):
        """
        Search categories.
        POST /api/firewall/category/search_item
        """
        return self.client.post("/api/firewall/category/search_item", json=query or {})

    def add_item(self, data: dict):
        """
        Add category.
        POST /api/firewall/category/add_item
        """
        return self.client.post("/api/firewall/category/add_item", json=data)

    def set(self, data: dict):
        """
        Update category.
        POST /api/firewall/category/setCategory/<uuid>
        """
        return self.client.post(f"/api/firewall/category/set/{uuid}", json=data)

    def del_item(self, json=None):
        """
        Delete category.
        POST /api/firewall/category/del_item/<uuid>
        """
        uuid = json['category']['uuid']
        return self.client.post(f"/api/firewall/category/del_item/{uuid}")

    def apply(self):
        """
        Apply category changes.
        POST /api/firewall/category/apply
        """
        return self.client.post("/api/firewall/category/apply")

