import sys
import re

import logging
logger = logging.getLogger(__name__)

from opnsense.client import OPNsenseClient
from opnsense.firewall.category import CategoryAPI

class FilterAPI:
    """
    OPNsense Firewall Filter API
    module: firewall
    controller: filter
    commands: get, add_rule, del_rule, toggleRule, search_rule, setRule, etc.
    """

    def __init__(self, client: OPNsenseClient):
        self.client = client
        self.base = "/api/firewall/filter"

    #
    # ───────────────────────────────────────────────
    # 基本コマンド（公式ドキュメント準拠）
    # https://docs.opnsense.org/development/api/core/firewall.html
    # ───────────────────────────────────────────────
    #

    def get(self, data=None, params=None):
        """
        Get all firewall filter rules.
        GET /api/firewall/filter/get
        """
        return self.client.get(f"{self.base}/get")

    def search_rule(self, data=None, params=None):
        """
        Search firewall rules.
        POST /api/firewall/filter/searc_rule
        """
        return self.client.post(
            f"{self.base}/search_rule",
            json=data
        )

    def add_rule(self, data=None, params=None):
        """
        Add a new firewall rule.
        POST /api/firewall/filter/add_rule
        """
        logging.debug(data)
        if not 'description' in data['rule'] :
            logger.error('no description for rule')
            sys.exit(1)

        category_api = CategoryAPI(self.client)
        res = category_api.get()
        cat_uuids = res['category']['categories']['category']
        cat2uuid = {}
        for uuid in cat_uuids:
            name = cat_uuids[uuid]['name']
            cat2uuid[name] = uuid

        ret = 0
        values = ''
        if 'categories' in data['rule'] :
            tokens = re.split(r',', data['rule']['categories'])
            for token in tokens:
                uuid = cat2uuid.get(token, None)
                if uuid is None :
                    logger.error('no such category, "{0}"'.format(token))
                    ret = ret + 1
                else :
                    values = values + ',' + uuid
        if ret :
            sys.exit(1)

        values = re.sub(r'^,', '', values)
        data['rule']['categories'] = values

        return self.client.post(f"{self.base}/add_rule", json=data)

    def set_rule(self, data=None, params=None):
        """
        Update an existing firewall rule.
        POST /api/firewall/filter/setRule/<uuid>
        """
        uuid = params['uuid']
        return self.client.post(
                  f"{self.base}/setRule/{uuid}",
                  json=data
               )

    def del_rule(self, data=None, params=None):
        """
        Delete a firewall rule by UUID.
        POST /api/firewall/filter/del_rule/<uuid>
        """
        uuid = params['uuid']
        return self.client.post(f"{self.base}/del_rule/{uuid}")

    def toggle_rule(self, data=None, params=None):
        """
        Enable/disable a firewall rule.
        POST /api/firewall/filter/toggleRule/<uuid>
        """
        uuid = params['uuid']
        return self.client.post(f"{self.base}/toggleRule/{uuid}")

    #
    # ───────────────────────────────────────────────
    # apply コマンド（Firewall/NAT/Rules 共通）
    # ───────────────────────────────────────────────
    #

    def apply(self, data=None, params=None):
        """
        Apply firewall changes.
        POST /api/firewall/filter/apply
        """
        return self.client.post(f"{self.base}/apply")

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

