from opnsense.client import OPNsenseClient

# controller modules
from .alias import AliasAPI
from .category import CategoryAPI
from .d_nat import DNatAPI
from .filter import FilterAPI
from .group import GroupAPI
from .npt import NptAPI
from .source_nat import SourceNatAPI

class FirewallAPI:
    """
    OPNsense Firewall API (module: firewall)
    Controller をまとめる集約クラス。
    """

    def __init__(self, client: OPNsenseClient):
        self.client = client

        # controller instances
        self.alias = AliasAPI(client)
        self.category = CategoryAPI(client)
        self.d_nat = DNatAPI(client)
        self.filter = FilterAPI(client)
        self.group = GroupAPI(client)
        self.npt = NptAPI(client)
        self.source_nat = SourceNatAPI(client)
        
