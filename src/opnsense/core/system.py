from opnsense.client import OPNsenseClient


class CoreAPI:
    """
    OPNsense Core System API
    module: core
    controller: system
    commands: dismiss_status, halt, reboot status 
    """

    def __init__(self, client: OPNsenseClient):
        self.client = client

    #
    # ───────────────────────────────────────────────
    # 基本コマンド（公式ドキュメント準拠）
    # https://docs.opnsense.org/development/api/core/firewall.html
    # ───────────────────────────────────────────────
    #

    def status(self, data=None):
        """
        Get system status
        GET /api/core/system/status
        """
        return self.client.get("/api/core/system/status")

