# opnsense-python

A developer-friendly Python wrapper for the OPNsense API.  
Designed for automation, testing, and integration scenarios, this package exposes structured API modules (client, firewall, interfaces, VIP settings).

## example

### firewall::alias

```
$ opncli firewall alias get
$ opncli firewall alias list_categories
$ opncli firewall alias list_countries
$ opncli firewall alias list_network_aliases
$ opncli firewall alias list_user_groups
$ opncli firewall alias list_reconfigure
$ opncli firewall alias search_item

$ opncli firewall alias add_item name=myalias \
    type=host content=192.168.1.10 enabled=1 description="hoge"

# apply
$ opncli firewall alias reconfigure

```

### firewall::category

```
$ opncli firewall category add_item name=blue color="0000ff"
$ opncli firewall category get
```

```
$ opncli firewall category search_item
$ opncli firewall category del_item uuid=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

### firewall::filter::add_rule

```
opncli firewall filter add_rule \
  enabled=1 \
  action=pass \
  interface=wan \
  direction=in \
  ipprotocol=inet \
  protocol=ICMP \
  source_net=any \
  destination_net=wanip \
  descr="allow PING from wan to this firewall" \
  quick=1 \
  statetype=keep \
  sequence=111
```

### netsnmp::user::add_user

```
$ opncli netsnmp user add_user \
    username=myuser \
    password=myauthpass \
    enckey=myencpass \
    enabled=1

# Push "Save" button.
$ opncli netsnmp service reconfigure

```

