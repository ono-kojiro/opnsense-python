#!/usr/bin/env python3

import os
from dotenv import load_dotenv

from opnsense.client import OPNsenseClient
from opnsense.interfaces.vip_settings import VirtualIPAPI

load_dotenv()

def main():
    base_url = os.getenv("OPNSENSE_BASE_URL")
    key = os.getenv("OPNSENSE_KEY")
    secret = os.getenv("OPNSENSE_SECRET")

    if not base_url or not key or not secret:
        raise RuntimeError("OPNSENSE_BASE_URL / OPNSENSE_KEY / OPNSENSE_SECRET are not defined")

    # create client
    client = OPNsenseClient(
        base_url=base_url,
        key=key,
        secret=secret,
        verify_ssl=True,  # self-signed
        #verify_ssl=False,  # self-signed
    )

    vip_api = VirtualIPAPI(client)

    # VIP list
    vips = vip_api.list_virtual_ips()

    print("=== Virtual IP List ===")
    print(vips)


if __name__ == "__main__":
    main()

