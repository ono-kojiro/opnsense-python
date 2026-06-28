from opnsense.client import OPNsenseClient

# controller modules
from .bridge_settings import BridgeSettingsAPI
from .gif_settings import GifSettingsAPI
from .gre_settings import GreSettingsAPI
from .lagg_settings import LaggSettingsAPI
from .loopback_settings import LoopbackSettingsAPI
from .neighbor_settings import NeighborSettingsAPI
from .overview import OverviewAPI
from .settings import SettingsAPI
from .vip_settings import VipSettingsAPI
from .vlan_settings import VlanSettingsAPI
from .vxlan_settings import VxlanSettingsAPI


class InterfacesAPI:
    """
    OPNsense Interfaces API (module: interfaces)
    Controller をまとめる集約クラス。
    """

    def __init__(self, client: OPNsenseClient):
        self.client = client

        # controller instances
        self.bridge_settings = BridgeSettingsAPI(client)
        self.gif_settings = GifSettingsAPI(client)
        self.gre_settings = GreSettingsAPI(client)
        self.lagg_settings = LaggSettingsAPI(client)
        self.loopback_settings = LoopbackSettingsAPI(client)
        self.neighbor_settings = NeighborSettingsAPI(client)
        self.overview = OverviewAPI(client)
        self.settings = SettingsAPI(client)
        self.vip_settings = VipSettingsAPI(client)
        self.vlan_settings = VlanSettingsAPI(client)
        self.vxlan_settings = VxlanSettingsAPI(client)

