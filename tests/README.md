# OPNsense configuration

## Install OPNsense

### login to INSTALLER

```
login: installer
Password: opnsense
```

## Initial Setup

### add WAN interface

```
  interface type: Direct attachment
  source        : (your host interface)
  mode          : bridge(default)
  model         : virtio (Linux, perf)
  MAC address   : (generate automatically)
```

### assign interfaces

```
Enter an option: 1     (Assign interfaces)

Do you want to configure LAGGs now? [y/N]: n
Do you want to configure VLANs now? [y/N]: n

Enter the WAN interface name or 'a' for auto-detection: vtnet1
Enter the LAN interface name or 'a' for auto-detection
NOTE: this enables full Firewalling/NAT mode.
(or nothing if finished): vtnet0

Enter the Optional interface 1 name or 'a' for auto-detection
(or nothing if finished): (press enter)

The interfaces will be assigned as follows:

WAN  -> vtnet1
LAN  -> vtnet0

Do you want to proceed? [y/N]: y
...
...

```
### change LAN address

```
Enter an option: 2     (Set interface IP address)
```

```
Available interfaces:

1 - LAN (vtnet0 - static, idassoc6)
2 - WAN (vtnet1 - dhcp, dhcp6)

Enter the number of the interface to configure: 1
```

```
Configure IPv4 address LAN interface via DHCP? [y/N] n

Enter the new LAN IPv4 address. Press <ENTER> for none:
> 192.168.122.xxx

Subnet masks are entered as bit counts (like CIDR notation).
e.g. 255.255.255.0 = 24
     255.255.0.0   = 16
     255.0.0.0     = 8

Enter the new LAN IPv4 subnet bit count (1 to 32):
> 24

For a WAN, enter the new LAN IPv4 upstream gateway address.
For a LAN, press <ENTER> for none:
> (press ENTER)

Configure IPv6 address LAN interface via WAN tracking? [Y/n] n
Configure IPv6 address LAN interface via DHCP6? [y/N] n

Enter the new LAN IPv6 address. Press <ENTER> for none:
> (press ENTER)

Do you want to enable the DHCP server on LAN? [y/N] n

Do you want to change the web GUI protocol form HTTPS to HTTP? [y/N] n
Do you want to generate a new self-signed web GUI certificate? [y/N] n
Restore web GUI access defaults? [y/N] n

...

You can now access the web GUI by opening
the following URL in your web browser:

    https://192.168.122.xxx
```

### start shell

enter the opnsense-shell and start shell

```
Enter an option: 8    ( Shell)
```

### change admin shell

```
# vi /conf/config.xml

<opnsense>
  ...
  <system>
    ...
    <user uid="xxx..... ">
      <shell>/bin/sh</shell>   <!-- MODIFY-->
    </user>
    ...

```

### enable ssh


configure /conf/config.xml

```
# vi /conf/config.xml
...

<opnsense>
  ...
  <system>
     ...
    <ssh>
      <group>admins</group>
      <enabled>enabled</enabled>              <!-- ADD -->
      <port>22</port>                         <!-- ADD -->
      <permitrootlogin>1</permitrootlogin>    <!-- ADD -->
      <passwordauth>1</passwordauth>          <!-- ADD -->
    </ssh>
```

### reload

```
root@OPNsense:~ # exit
Enter an option: 11    ( Reload all services)

or

root@OPNsense:~ # /usr/local/sbin/opnsense-shell reload
```

### ssh connection

```
$ ssh 192.168.122.xxx -l root

root@OPNsense:~ #
```

### add public key

```
$ cat ~/.ssh/id_ed25519.pub | head -n 1 | base64 --wrap 0
```

copy base64 to "authorizedkeys"

```
# vi /conf/config.xml

<opnsense>
  ...
  <system>
    ...
    <user uid="xxx..... ">
      ...
      <authorizedkeys>(BASE64 of pubkey)</authorizedkeys>
      ...
    </user>

# /usr/local/sbin/opnsense-shell reload

```

After this process, you can log-in via SSH without password.

## Halt

```
root@OPNsense:~ # exec /usr/local/opnsense/scripts/shell/halt.php
```

## Advanced Setup

### create api key and hashed secret

run following command on host (or OPNsense).

```
API KEY

$ openssl rand -base64 48 | tee apikey.txt
```

```
SECRET

$ openssl rand -hex 32 | tee secret.txt
```

```
HASH

$ cat secret.txt | openssl passwd -6 -stdin | tee hash.txt
```

### add api key

```
root@OPNsense:~ # vi /conf/config.xml

<opnsense>
  ...
  <system>
    ...
    <user uid="xxx..... ">
      ...
      <apikeys>(key)|(hash)</apikeys> <!-- ADD -->
      ...
    </user>

root@OPNsense:~ # /usr/local/sbin/opnsense-shell reload
```

### test API key

```
$ vi ./.netrc
machine 192.168.122.xx
  login    (apikey here!)
  password (secret here!)

$ curl -s -k --netrc-file .netrc https://192.168.122.xx/api/core/system/status | jq .
{
  "metadata": {
    "system": {
      "status": 2,
      "message": "No pending messages",
      "title": "System"
    },
    "translations": {
      "dialogTitle": "System Status",
      "dialogCloseButton": "Close"
    },
    "subsystems": []
  }
}
```

## disable http preferer check

```
# vi /conf/config.xml

<opnsense>
  ...
  <system>
    ...
    <webgui>
      <nohttpreferercheck>1</nohttpreferercheck>  <!-- ADD --> 
    </webgui>
    ...

# exit

Enter an option: 11 (Reload all services)
```

