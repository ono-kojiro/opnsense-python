#!/usr/bin/env python3

import ipaddress
import yaml
import re


class FortiGateConfig:
    def __init__(self):
        self.addresses = {}
        self.addrgrps = {}
        self.services = {}
        self.service_groups = {}
        self.policies = {}


def parse_fortigate_config(filename):
    cfg = FortiGateConfig()

    section = None
    current = None

    with open(filename) as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            if line.startswith("config firewall address"):
                section = "address"
                continue

            if line.startswith("config firewall addrgrp"):
                section = "addrgrp"
                continue

            if line.startswith("config firewall service custom"):
                section = "service"
                continue

            if line.startswith("config firewall service group"):
                section = "service_group"
                continue

            if line.startswith("config firewall policy"):
                section = "policy"
                continue

            if line == "end":
                section = None
                continue

            m = re.match(r'edit\s+"?(.*?)"?$', line)
            if m:
                current = m.group(1)

                if section == "address":
                    cfg.addresses[current] = {}

                elif section == "addrgrp":
                    cfg.addrgrps[current] = {}

                elif section == "service":
                    cfg.services[current] = {}

                elif section == "service_group":
                    cfg.service_groups[current] = {}

                elif section == "policy":
                    cfg.policies[current] = {}

                continue

            if line == "next":
                current = None
                continue

            if current is None:
                continue

            m = re.match(r'set\s+(\S+)\s+(.+)', line)
            if not m:
                continue

            key = m.group(1)
            val = m.group(2).strip('"')

            if section == "address":
                cfg.addresses[current][key] = val

            elif section == "addrgrp":
                cfg.addrgrps[current][key] = val

            elif section == "service":
                cfg.services[current][key] = val

            elif section == "service_group":
                cfg.service_groups[current][key] = val

            elif section == "policy":
                cfg.policies[current][key] = val

    return cfg


def subnet_to_cidr(subnet):
    ip, mask = subnet.split()

    net = ipaddress.IPv4Network(f"{ip}/{mask}", strict=False)

    return str(net)


def generate_aliases(cfg):

    aliases = []

    #
    # address -> network / host
    #

    for name, data in cfg.addresses.items():

        if "subnet" not in data:
            continue

        cidr = subnet_to_cidr(data["subnet"])

        net = ipaddress.ip_network(cidr)

        if net.prefixlen == 32:
            alias_type = "host"
            content = str(net.network_address)
        else:
            alias_type = "network"
            content = cidr

        aliases.append(
            {
                "name": name,
                "type": alias_type,
                "content": content,
                "enabled": 1,
                "categories": "red",
                "description": data.get("comment", ""),
            }
        )

    #
    # service -> port
    #

    for name, data in cfg.services.items():

        port = data.get("tcp-portrange")

        if port is None:
            continue

        aliases.append(
            {
                "name": name,
                "type": "port",
                "content": port,
                "enabled": 1,
                "categories": "red",
                "description": data.get("comment", ""),
            }
        )

    #
    # addrgrp -> networkgroup
    #

    for name, data in cfg.addrgrps.items():

        members = (
            data.get("member", "")
            .replace('"', "")
            .split()
        )

        aliases.append(
            {
                "name": name,
                "type": "networkgroup",
                "content": ",".join(members),
                "enabled": 1,
                "categories": "red",
                "description": "",
            }
        )

    #
    # service_group -> portgroup
    #

    for name, data in cfg.service_groups.items():

        members = (
            data.get("member", "")
            .replace('"', "")
            .split()
        )

        aliases.append(
            {
                "name": name,
                "type": "portgroup",
                "content": ",".join(members),
                "enabled": 1,
                "categories": "red",
                "description": "",
            }
        )

    return {"aliases": aliases}


def service_to_protocol(service_name):

    if service_name == "PING":
        return ("ICMP", None)

    if service_name == "ALL":
        return ("TCP", "any")

    if service_name.startswith("port_"):
        try:
            port = service_name.split("_", 1)[1]
            return ("TCP", port)
        except Exception:
            pass

    return ("TCP", "any")


def generate_filters(cfg):

    filters = []

    for seq, policy in sorted(
        cfg.policies.items(),
        key=lambda x: int(x[0])
    ):

        protocol, dst_port = service_to_protocol(
            policy.get("service", "ALL")
        )

        filt = {
            "description": policy.get(
                "comments",
                policy.get("name", "")
            ),
            "categories": "red",
            "action": "pass",
            "interface": policy.get("srcintf", ""),
            "direction": "in",
            "ipprotocol": "inet",
            "protocol": protocol,
            "source_net": policy.get("srcaddr", ""),
            "destination_net": policy.get("dstaddr", ""),
            "enabled": 1,
            "quick": 1,
            "statetype": "keep",
            "sequence": int(seq),
        }

        if dst_port:
            filt["destination_port"] = dst_port

        filters.append(filt)

    return {"filters": filters}


def main():

    cfg = parse_fortigate_config("dummy.conf")

    aliases = generate_aliases(cfg)

    filters = generate_filters(cfg)

    with open("aliases.yml", "w") as f:
        yaml.safe_dump(
            aliases,
            f,
            allow_unicode=True,
            sort_keys=False,
        )

    with open("filters.yml", "w") as f:
        yaml.safe_dump(
            filters,
            f,
            allow_unicode=True,
            sort_keys=False,
        )

    print("generated aliases.yml")
    print("generated filters.yml")


if __name__ == "__main__":
    main()

