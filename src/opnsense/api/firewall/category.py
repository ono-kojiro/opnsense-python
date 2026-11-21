from opnsense.client import OPNsenseClient

class CategoryAPI:
    """
    OPNsense Firewall Category API
    module: firewall
    controller: category
    """

    def __init__(self, client: OPNsenseClient):
        self.client = client
        self.base   = "/api/firewall/category"

    def get(self):
        """
        Get categories.
        GET /api/firewall/category/get
        """
        url = f"{self.base}/get"
        return self.client.get(url)

    def search_item(self, data=None):
        """
        Search categories.
        POST /api/firewall/category/search_item
        """
        url = f"{self.base}/search_item"
        return self.client.post(url, json=data)

    def add_item(self, data):
        """
        Add category.
        POST /api/firewall/category/add_item
        """
        url = f"{self.base}/add_item"
        return self.client.post(url, json=data)

    def set(self, data, params):
        """
        Update category.
        POST /api/firewall/category/setCategory/<uuid>
        """
        uuid = params['uuid']
        url = f"{self.base}/set/{uuid}"
        return self.client.post(url, json=data)

    def del_item(self, params):
        """
        Delete category.
        POST /api/firewall/category/del_item/<uuid>
        """
        uuid = params['uuid']
        url = f"{self.base}/del_item/{uuid}"
        return self.client.post(url)

    def apply(self):
        """
        Apply category changes.
        POST /api/firewall/category/apply
        """
        url = f"{self.base}/apply"
        return self.client.post(url)

