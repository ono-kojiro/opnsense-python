#!/usr/bin/env python3

import sys
import os

import uuid

import getopt
import yaml
import json

from opnsense.interfaces import InterfacesAPI
from dotenv import load_dotenv

from opnsense.client import OPNsenseClient
from opnsense.firewall import FirewallAPI
from opnsense.interfaces import InterfacesAPI
from opnsense.interfaces.vip_settings import VipSettingsAPI
from opnsense.firewall.category import CategoryAPI

from opnsense.utils.vip import vip_add, vip_clean, vip_list
from opnsense.utils.rule import rule_add, rule_clean, rule_list
from opnsense.utils.category import category_add, category_clean, category_list

load_dotenv(dotenv_path=".env")

from pprint import pprint

def usage():
    prog = os.path.basename(sys.argv[0])
    print('usage: {0} COMMAND [OPTIONS]'.format(prog))

def read_yaml(filepath):
    fp = open(filepath, mode="r", encoding="utf-8")
    data = yaml.safe_load(fp)
    fp.close()
    return data

def main() :
    ret = 0

    try:
        options, args = getopt.getopt(
            sys.argv[1:],
            "hv",
            [
              "help",
              "version",
            ]
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    output = None

    for option, arg in options:
        if option in ("-v", "-h", "--help"):
            usage()
            sys.exit(0)
        elif option in ("-o", "--output"):
            output = arg
        else:
            assert False, "unknown option"

    if ret != 0:
        sys.exit(1)

    load_dotenv()

    key = os.getenv("OPNSENSE_KEY")
    secret = os.getenv("OPNSENSE_SECRET")
    base_url = os.getenv("OPNSENSE_BASE_URL", "https://localhost:8443")

    client = OPNsenseClient(
        base_url=base_url,
        key=key,
        secret=secret,
        verify_ssl=True,
    )

    funcs = {
        'vip-add': vip_add,
        'vip-list': vip_list,
        'vip-clean': vip_clean,
        'rule-add': rule_add,
        'rule-list': rule_list,
        'rule-clean': rule_clean,
        'category-list': category_list,
    }

    if len(args) == 0:
        usage()
        sys.exit(1)

    cmd = args[0]
    if cmd in funcs:
        funcs[cmd](client, args[1:])
    else :
        print('ERROR: unknown command, {0}'.format(cmd))
        sys.exit(1)

if __name__ == "__main__":
    main()
