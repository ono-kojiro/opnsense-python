from opnsense.client import OPNsenseClient


class AuthGroupAPI:
    """
    OPNsense Auth Group API
    module: auth
    controller: group
    commands: add, del, get, search, set
    """

    def __init__(self, client: OPNsenseClient):
        self.client = client

    def search(self, data=None, params=None):
        """
        GET,POST /api/auth/group/search
        """
        return self.client.get("/api/auth/group/search")

