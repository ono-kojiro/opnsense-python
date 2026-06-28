from opnsense.client import OPNsenseClient


class CategoryAPI:
    """
    OPNsense Firewall Category API
    module: firewall
    controller: category
    """

    def __init__(self, client: OPNsenseClient):
        self.client = client

    def get(self):
        """
        Get categories.
        GET /api/firewall/category/get
        """
        return self.client.get("/api/firewall/category/get")

    def search(self, query: dict | None = None):
        """
        Search categories.
        POST /api/firewall/category/searchCategory
        """
        return self.client.post("/api/firewall/category/searchCategory", json=query or {})

    def add(self, data: dict):
        """
        Add category.
        POST /api/firewall/category/addCategory
        """
        return self.client.post("/api/firewall/category/addCategory", json=data)

    def set(self, uuid: str, data: dict):
        """
        Update category.
        POST /api/firewall/category/setCategory/<uuid>
        """
        return self.client.post(f"/api/firewall/category/setCategory/{uuid}", json=data)

    def delete(self, uuid: str):
        """
        Delete category.
        POST /api/firewall/category/delCategory/<uuid>
        """
        return self.client.post(f"/api/firewall/category/delCategory/{uuid}")

    def apply(self):
        """
        Apply category changes.
        POST /api/firewall/category/apply
        """
        return self.client.post("/api/firewall/category/apply")

