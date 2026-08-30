import sys
import os
import getopt

import json

import logging

from opnsense.client import OPNsenseClient

logger = logging.getLogger(__name__)

class NetSnmpServiceAPI:
    """
    OPNsense NetSNMP Service API
    module: netsnmp
    controller: general
    """

    def __init__(self, client: OPNsenseClient):
        self.client = client

    def reconfigure(self, json=None):
        """
        Execute snmp service reconfigure
        POST /api/netsnmp/service/reconfigure
        """
        return self.client.reconfigure("/api/netsnmp/service/reconfigure")

def netsnmp_reconfigure(client, argv):
    ret = 0
    output = None

    api = NetSnmpServiceAPI(client)

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

    res = api.reconfigure()

    if isinstance(res, list) :
        logger.debug('response is list')
    elif isinstance(res, dict) :
        logger.debug('response is dict')
    else :
        logger.error('unknown type of response')
        sys.exit(1)
    
    logger.info(res)
    fp.write(
        json.dumps(
            res,
            indent=4,
            ensure_ascii=False,
        )
    )
    fp.write('\n')

    if output is not None:
        fp.close()

    return

