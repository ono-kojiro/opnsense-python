# opnsense-python

A developer-friendly Python wrapper for the OPNsense API.  
Designed for automation, testing, and integration scenarios, this package exposes structured API modules (client, firewall, interfaces, VIP settings).

## example

### category

```
$ opncli firewall category add_item name=blue color="0000ff"
$ opncli firewall category get
```

```
$ opncli firewall category search_item
$ opncli firewall category del_item uuid=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

