import yaml
import json

import sys
import getopt

from opnsense.client import OPNsenseClient
from opnsense.firewall.category import CategoryAPI 

from pprint import pprint

def read_yaml(filepath):
    fp = open(filepath, mode="r", encoding="utf-8")
    data = yaml.safe_load(fp)
    fp.close()
    return data

def category_add(client, argv):
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
        data = read_yaml(arg)
        #pprint(data)

        items = data['vip']
        for item in items :
            print(item)

            res = api.add_item(
                {
                    'vip' : item,
                }
            )
            print(res)

    if output is not None:
        fp.close()

def category_list(client, argv):
    ret = 0
    output = None

    api = CategoryAPI(client)

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
    pprint(res)
    items = res.get('category', {}).get('categories', {})


    if isinstance(items, list) :
        print('list')
    elif isinstance(items, dict) :
        print('dict')
    else :
        print('ERROR: unknown type of response')
        sys.exit(1)
    
    pprint(items)

    if output is not None:
        fp.close()

    return items

def category_clean(client, argv):
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

