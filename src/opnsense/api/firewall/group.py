from opnsense.client import OPNsenseClient


class GroupAPI:
    """
    OPNsense Firewall Group API
    module: firewall
    controller: group
    """

    def __init__(self, client: OPNsenseClient):
        self.client = client

    def get(self):
        """
        Get firewall groups.
        GET /api/firewall/group/get
        """
        return self.client.get("/api/firewall/group/get")

    def search(self, query: dict | None = None):
        """
        Search firewall groups.
        POST /api/firewall/group/searchGroup
        """
        return self.client.post("/api/firewall/group/searchGroup", json=query or {})

    def add(self, data: dict):
        """
        Add firewall group.
        POST /api/firewall/group/addGroup
        """
        return self.client.post("/api/firewall/group/addGroup", json=data)

    def set(self, uuid: str, data: dict):
        """
        Update firewall group.
        POST /api/firewall/group/setGroup/<uuid>
        """
        return self.client.post(f"/api/firewall/group/setGroup/{uuid}", json=data)

    def delete(self, uuid: str):
        """
        Delete firewall group.
        POST /api/firewall/group/delGroup/<uuid>
        """
        return self.client.post(f"/api/firewall/group/delGroup/{uuid}")

    def apply(self):
        """
        Apply firewall group changes.
        POST /api/firewall/group/apply
        """
        return self.client.post("/api/firewall/group/apply")

