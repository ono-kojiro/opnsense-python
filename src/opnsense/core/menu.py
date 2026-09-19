from opnsense.client import OPNsenseClient


class CoreMenuAPI:
    """
    OPNsense Core Menu API
    module: core
    controller: menu
    commands:
    """

    def __init__(self, client: OPNsenseClient):
        self.client = client
    
    def __search(self, mod, ctl, cmd):
        print('  no options')

    def search(self, data=None, params=None):
        """
        Get core menu search
        GET /api/core/menu/search
        """
        return self.client.get("/api/core/menu/search")
    
    def __tree(self, mod, ctl, cmd):
        print('  no options')

    def tree(self, data=None, params=None):
        """
        Get core menu tree
        GET /api/core/menu/tree
        """
        return self.client.get("/api/core/menu/tree")


