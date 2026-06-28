import yaml
import json

import sys
import getopt

from opnsense.client import OPNsenseClient
from opnsense.firewall.filter import FilterAPI
from opnsense.firewall.category import CategoryAPI

from opnsense.utils.category import category_list

from pprint import pprint

def read_yaml(filepath):
    fp = open(filepath, mode="r", encoding="utf-8")
    data = yaml.safe_load(fp)
    fp.close()
    return data

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

def rule_add(client, argv):
    ret = 0
    output = None

    api = FilterAPI(client)
    category_api = CategoryAPI(client)

    try:
        options, args = getopt.getopt(
            argv,
            "hvo:",
            [
              "help",
              "output="
            ]
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    for option, arg in options:
        if option in ("-v", "-h", "--help"):
            usage_vip_add()
            sys.exit(0)
        elif option in ("-o", "--output"):
            output = arg
        else:
            assert False, "unknown option"

    if output is not None:
        fp = open(output, mode="w", encoding="utf-8")
    else :
        fp = sys.stdout

    if ret != 0:
        sys.exit(1)

    for arg in args:
        items = read_yaml(arg)

        for item in items :
            res = api.add_rule(
                {
                    "rule": item,
                }
            )
            print(res)

    if output is not None:
        fp.close()

def rule_list(client, argv):
    ret = 0
    output = None

    api = FilterAPI(client)

    try:
        options, args = getopt.getopt(
            argv,
            "hvo:",
            [
              "help",
              "output="
            ]
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    for option, arg in options:
        if option in ("-v", "-h", "--help"):
            usage_vip_add()
            sys.exit(0)
        elif option in ("-o", "--output"):
            output = arg
        else:
            assert False, "unknown option"

    if output is not None:
        fp = open(output, mode="w", encoding="utf-8")
    else :
        fp = sys.stdout

    if ret != 0:
        sys.exit(1)

    res = api.get()

    #print(res)
    res = prune_selected(res)

    print(
        json.dumps(res)
    )

    #items = res.get('vip', {}).get('vip', {})

    #if isinstance(items, list) :
    #    print('list')
    #elif isinstance(items, dict) :
    #    print('dict')
    #else :
    #    print('ERROR: unknown type of response')
    #    sys.exit(1)
    
    #pprint(items)

    if output is not None:
        fp.close()


def rule_clean(client, argv):
    ret = 0
    output = None

    api = VipSettingsAPI(client)

    try:
        options, args = getopt.getopt(
            argv,
            "hvo:",
            [
              "help",
              "output="
            ]
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    for option, arg in options:
        if option in ("-v", "-h", "--help"):
            usage_rule_add()
            sys.exit(0)
        elif option in ("-o", "--output"):
            output = arg
        else:
            assert False, "unknown option"

    if output is not None:
        fp = open(output, mode="w", encoding="utf-8")
    else :
        fp = sys.stdout

    if ret != 0:
        sys.exit(1)

    res = api.get()
    items = res.get('vip', {}).get('vip', {})

    #pprint(items)

    if isinstance(items, list) :
        #print('list')
        pass
    elif isinstance(items, dict) :
        #print('dict')
        for uuid, item in items.items():
            print(json.dumps(item))
            res2 = api.del_item(uuid)
            print(res2)
    else :
        print('ERROR: unknown type of response')
        sys.exit(1)

    if output is not None:
        fp.close()

