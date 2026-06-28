from opnsense.client import OPNsenseClient


class FilterAPI:
    """
    OPNsense Firewall Filter API
    module: firewall
    controller: filter
    commands: get, addRule, delRule, toggleRule, searchRule, setRule, etc.
    """

    def __init__(self, client: OPNsenseClient):
        self.client = client

    #
    # ───────────────────────────────────────────────
    # 基本コマンド（公式ドキュメント準拠）
    # https://docs.opnsense.org/development/api/core/firewall.html
    # ───────────────────────────────────────────────
    #

    def get(self):
        """
        Get all firewall filter rules.
        GET /api/firewall/filter/get
        """
        return self.client.get("/api/firewall/filter/get")

    def search(self, query: dict | None = None):
        """
        Search firewall rules.
        POST /api/firewall/filter/searchRule
        """
        return self.client.post("/api/firewall/filter/searchRule", json=query or {})

    def add_rule(self, rule_data: dict):
        """
        Add a new firewall rule.
        POST /api/firewall/filter/addRule
        """
        return self.client.post("/api/firewall/filter/addRule", json=rule_data)

    def set_rule(self, uuid: str, rule_data: dict):
        """
        Update an existing firewall rule.
        POST /api/firewall/filter/setRule/<uuid>
        """
        return self.client.post(f"/api/firewall/filter/setRule/{uuid}", json=rule_data)

    def delete_rule(self, uuid: str):
        """
        Delete a firewall rule by UUID.
        POST /api/firewall/filter/delRule/<uuid>
        """
        return self.client.post(f"/api/firewall/filter/delRule/{uuid}")

    def toggle_rule(self, uuid: str):
        """
        Enable/disable a firewall rule.
        POST /api/firewall/filter/toggleRule/<uuid>
        """
        return self.client.post(f"/api/firewall/filter/toggleRule/{uuid}")

    #
    # ───────────────────────────────────────────────
    # apply コマンド（Firewall/NAT/Rules 共通）
    # ───────────────────────────────────────────────
    #

    def apply(self):
        """
        Apply firewall changes.
        POST /api/firewall/filter/apply
        """
        return self.client.post("/api/firewall/filter/apply")

    #
    # ───────────────────────────────────────────────
    # Utility: selected=0 の項目を再帰的に削除するフィルタ
    # ───────────────────────────────────────────────
    #

    @staticmethod
    def prune_selected(obj):
        """
        Recursively remove items where selected == 0.
        Useful for cleaning OPNsense API responses.
        """

        # selected を持つ辞書なら判定して返す
        if isinstance(obj, dict) and "selected" in obj:
            return obj if obj["selected"] == 1 else None

        # 辞書なら再帰的に処理
        if isinstance(obj, dict):
            new_obj = {}
            for key, value in obj.items():
                pruned = FilterAPI.prune_selected(value)
                if pruned is not None:
                    new_obj[key] = pruned
            return new_obj

        # リストなら再帰的に処理
        if isinstance(obj, list):
            new_list = []
            for item in obj:
                pruned = FilterAPI.prune_selected(item)
                if pruned is not None:
                    new_list.append(pruned)
            return new_list

        # その他の型はそのまま返す
        return obj

