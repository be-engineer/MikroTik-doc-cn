## Summary

[?](https://help.mikrotik.com/docs/display/ROS/LTE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">Package</code><code class="ros constants">: system</code></div></div></td></tr></tbody></table>

Support for Direct-IP mode type cards only. MBIM support is available in RouterOS v7 releases and MBIM driver is loaded automatically. If modem is not recognized in RouterOS v6 - Please test it in v7 releases before asking for support in RouterOS v6.

To enable access via a PPP interface instead of a LTE Interface, change direct IP mode with `/port firmware set ignore-directip-modem=yes` command and a reboot. Note that using PPP emulation mode you may not get the same throughput speeds as using the LTE interface emulation type. 

For RouterOS v7 ignore-direct-modem parameter renamed to "mode" and moved to `/interface lte settings` menu.

## LTE Client

[?](https://help.mikrotik.com/docs/display/ROS/LTE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">Sub-menu</code><code class="ros constants">: /interface lte</code></div></div></td></tr></tbody></table>

### Properties

| 
Property

 | 

Description

 |     |
 | --- |  |
 |     |

Property

 | 

Description

 |                                                   |
 | ------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
 | **allow-roaming** (_yes                           | no_; Default: **no**)                                                                                                                                                      | Enable data roaming for connecting to other countries data-providers. Not all LTE modems support this feature. Some modems, that do not fully support this feature, will connect to the network but will not establish an IP data connection with allow-roaming set to no. |
 | **apn-profiles** (_string_; Default: **default**) | Which APN profile to use for this interface                                                                                                                                |
 | **band** (_integer list_; Default: **""**)        | LTE Frequency band used in communication `[LTE Bands and bandwidths](https://en.wikipedia.org/wiki/LTE_frequency_bands#Frequency_bands_and_channel_bandwidths)`            |
 | **nr-band** (_integer list_; Default: "")         | 5G NR Frequency band used in communication `[5G NR Bands and bandwidths](https://en.wikipedia.org/wiki/5G_NR_frequency_bands)`                                             |
 | **comment** (_string_; Default: **""**)           | Descriptive name of an item                                                                                                                                                |
 | **disabled** (_yes                                | no_; Default: **yes**)                                                                                                                                                     | Whether interface is disabled or not. By default it is disabled.                                                                                                                                                                                                           |
 | **modem-init** (_string_; Default: **""**)        | Modem init string (AT command that will be executed at modem startup)                                                                                                      |
 | **mtu** (_integer_; Default: **1500**)            | Maximum Transmission Unit. Max packet size that LTE interface will be able to send without packet fragmentation.                                                           |
 | **name** (_string_; Default: **""**)              | Descriptive name of the interface.                                                                                                                                         |
 | **network-mode** (_3g                             | gsm                                                                                                                                                                        | lte                                                                                                                                                                                                                                                                        | 5g_) | Select/force mode for LTE interface to operate with |
 | **operator** (_integer_; Default: **""**)         | used to lock device to specific operator full PLMN number is used for lock consisting from MCC+MNC. [PLMN codes](https://en.wikipedia.org/wiki/Public_land_mobile_network) |
 | **pin** (_integer_; Default: **""**)              | SIM Card's PIN code.                                                                                                                                                       |

### APN profiles

All network related settings are moved under profiles, starting from RouterOS 6.41

[?](https://help.mikrotik.com/docs/display/ROS/LTE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">Sub-menu</code><code class="ros constants">: /interface lte apn</code></div></div></td></tr></tbody></table>

  

| 
Property

 | 

Description

 |     |
 | --- |  |
 |     |

Property

 | 

Description

 |                                                                    |
 | ------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
 | **add-default-route** (_yes                                        | no_)                                                                                                                                                                                                                                                                    | Whether to add default route to forward all traffic over the LTE interface.                                               |
 | **apn** (_string_)                                                 | Service Provider's Access Point Name                                                                                                                                                                                                                                    |
 | **authentication** (_pap                                           | chap                                                                                                                                                                                                                                                                    | none_; Default: **none**)                                                                                                 | Allowed protocol to use for authentication |
 | **default-route-distance** (_integer_; Default: **2**)             | Sets distance value applied to auto created default route, if add-default-route is also selected. LTE route by default is with distance 2 to prefer wired routes over LTE                                                                                               |
 | **ip-type** (_ipv4                                                 | ipv4-ipv6                                                                                                                                                                                                                                                               | ipv6_; Default: )                                                                                                         | Requested PDN type                         |
 | **ipv6-interface** (; Default: )                                   | Interface on which to advertise IPv6 prefix                                                                                                                                                                                                                             |
 | **name** (_string_; Default: )                                     | APN profile name                                                                                                                                                                                                                                                        |
 | **number** (_integer_; Default: )                                  | APN profile number                                                                                                                                                                                                                                                      |
 | **passthrough-interface** (; Default: )                            | Interface to passthrough IP configuration (activates passthrough)                                                                                                                                                                                                       |
 | **passthrough-mac** (_MAC_; Default: **auto**)                     | If set to auto, then will learn MAC from first packet                                                                                                                                                                                                                   |
 | **passthrough-subnet-selection** (_auto / p2p_; Default: **auto**) | "auto" selects the smallest possible subnet to be used for the passthrough interface. "p2p" sets the passthrough interface subnet as /32 and picks gateway address from 10.177.0.0/16 range. The gateway address stays the same until the apn configuration is changed. |
 | **password** (_string_; Default: )                                 | Password used if any of the authentication protocols are active                                                                                                                                                                                                         |
 | **use-network-apn** (_yes                                          | no_; Default: **yes**)                                                                                                                                                                                                                                                  | Parameter is available starting from RouterOS v7 and used only for MBIM modems. If set to yes, uses network provided APN. |
 | **use-peer-dns** (_yes                                             | no_; Default: **yes**)                                                                                                                                                                                                                                                  | If set to yes, uses DNS recieved from LTE interface                                                                       |
 | **user** (_integer_)                                               | Username used if any of the authentication protocols are active                                                                                                                                                                                                         |

### Scanner

It is possible to scan LTE interfaces with `/interface lte scan` command

Available read only properties:

| 
Property

 | 

Description

 |     |
 | --- |  |
 |     |

Property

 | 

Description

 |                                       |
 | ------------------------------------- | --------------------------- |
 | **duration** (_integer_)              | Duration of scan in seconds |
 | **freeze-frame-interval** (_integer_) | time between data printout  |
 | **number** (_integer_)                | Interface number or name    |

### User Info command

It is possible to send special "info" command to LTE interface with `/interface lte info` command. In RouterOS v7 this command is moved to `/interface lte monitor` menu.

#### Properties (Up to 6.40)

| 
Property

 | 

Description

 |     |
 | --- |  |
 |     |

Property

 | 

Description

 |                                              |
 | -------------------------------------------- | ------------------------------------------------------------------------------- |
 | **user-command** (_string_; Default: **""**) | send a command to LTE card to extract useful information, e.g. with AT commands |
 | **user-command-only** (_yes                  | no_; Default: )                                                                 |
 |                                              |

### User at-chat command

It is possible to send user defined "at-chat" command to LTE interface with `/interface lte at-chat` command.

[?](https://help.mikrotik.com/docs/display/ROS/LTE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; </code><code class="ros constants">/interface lte at-chat lte1 input="AT*mrd_imei\?"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">output</code><code class="ros constants">: *MRD_IMEI:356159060388208</code></div><div class="line number3 index2 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">OK</code></div></div></td></tr></tbody></table>

You can also use "at-chat" function in scripts and assign command output to variable.

[?](https://help.mikrotik.com/docs/display/ROS/LTE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; </code><code class="ros constants">:</code><code class="ros functions">global </code><code class="ros string">"lte_command"</code> <code class="ros plain">[</code><code class="ros constants">/interface lte at-chat lte1 input="AT*mrd_imei\?" as-value ]</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; </code><code class="ros constants">:</code><code class="ros functions">put </code><code class="ros plain">$</code><code class="ros string">"lte_command"</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros value">output</code><code class="ros plain">=*MRD_IMEI:356159060388208</code></div><div class="line number4 index3 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">OK</code></div></div></td></tr></tbody></table>

## Quick setup example

Start with network settings -

This guide is for RouterOS versions starting from 6.41

Start with network settings - Add new connection parameters under LTE apn profile (provided by network provider):

[?](https://help.mikrotik.com/docs/display/ROS/LTE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface lte apn </code><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=profile1</code> <code class="ros value">apn</code><code class="ros plain">=phoneprovider.net</code> <code class="ros value">authentication</code><code class="ros plain">=chap</code> <code class="ros value">password</code><code class="ros plain">=web</code> <code class="ros value">user</code><code class="ros plain">=web</code></div></div></td></tr></tbody></table>

Select newly created profile for LTE connection:

[?](https://help.mikrotik.com/docs/display/ROS/LTE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface lte </code><code class="ros functions">set </code><code class="ros plain">[find] </code><code class="ros value">apn-profiles</code><code class="ros plain">=profile1</code></div></div></td></tr></tbody></table>

LTE interface should appear with running (R) flag:

[?](https://help.mikrotik.com/docs/display/ROS/LTE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; </code><code class="ros constants">/interface lte </code><code class="ros plain">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disabled, R - running</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">0 R </code><code class="ros value">name</code><code class="ros plain">=</code><code class="ros string">"lte1"</code> <code class="ros value">mtu</code><code class="ros plain">=1500</code> <code class="ros value">mac-address</code><code class="ros plain">=AA:AA:AA:AA:AA:AA</code></div></div></td></tr></tbody></table>

From RouterOS=>6.41 DHCP client is added automatically. If it's not added - add a DHCP Client to LTE Interface manually:

[?](https://help.mikrotik.com/docs/display/ROS/LTE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip dhcp-client </code><code class="ros functions">add </code><code class="ros value">default-route-distance</code><code class="ros plain">=1</code> <code class="ros value">disabled</code><code class="ros plain">=no</code> <code class="ros value">interface</code><code class="ros plain">=lte1</code></div></div></td></tr></tbody></table>

If required, add NAT Masquerade for LTE Interface to get internet to the local network:

[?](https://help.mikrotik.com/docs/display/ROS/LTE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip firewall nat </code><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=masquerade</code> <code class="ros value">chain</code><code class="ros plain">=srcnat</code> <code class="ros value">out-interface</code><code class="ros plain">=lte1</code></div></div></td></tr></tbody></table>

After interface is added, you can use "info" command to see what parameters client acquired (parameters returned depends on LTE hardware device):

```
[admin@MikroTik] > /interface lte info lte1 once 
status: call in progress
pin-status: no password required
functionality: full
manufacturer: Huawei Technologies Co., Ltd.
model: ME909u-521
revision: 12.631.07.01.00
current-operator: vodafone ES
current-cellid: 44436007
access-technology: Evolved 3G (LTE)
signal-strengh: -79 dBm
frame-error-rate: n/a
earfcn: n/a
imei: 860461024123456
imsi: 234012555034981
uicc: n/a
rssi: -79dBm
rsrp: -109dBm
rsrq: -13dB
sinr: -1dB
```

## Passthrough Example

Starting from RouterOS v6.41 some LTE interfaces support LTE Passthrough feature where the IP configuration is applied directly to the client device. In this case modem firmware is responsible for the IP configuration and router is used only to configure modem settings - APN, Network Technologies and IP-Type. In this configuration the router will not get IP configuration from the modem. The LTE Passthrough modem can pass both IPv4 and IPv6 addresses if that is supported by modem. Some modems support multiple APN where you can pass the traffic from each APN to a specific router interface.

Passthrough will only work for one host. Router will automatically detect MAC address of the first received packet and use it for the Passthrough. If there are multiple hosts on the network it is possible to lock the Passthrough to a specific MAC. On the host on the network where the Passthrough is providing the IP a DHCP-Client should be enabled on that interface to. Note, that it will not be possible to connect to the LTE router via public lte ip address or from the host which is used by the passthrough. It is suggested to create additional connection from the LTE router to the host for configuration purposes. For example vlan interface between the LTE router and host.

To enable the Passthrough a new entry is required or the default entry should be changed in the '/interface lte apn' menu

  

Passthrough is not supported by all chipsets.

  
Examples.

To configure the Passthrough on ether1:

[?](https://help.mikrotik.com/docs/display/ROS/LTE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; </code><code class="ros constants">/interface lte apn </code><code class="ros functions">add </code><code class="ros value">apn</code><code class="ros plain">=apn1</code> <code class="ros value">passthrough-interface</code><code class="ros plain">=ether1</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; </code><code class="ros constants">/interface lte </code><code class="ros functions">set </code><code class="ros plain">lte1 </code><code class="ros value">apn-profiles</code><code class="ros plain">=apn1</code></div></div></td></tr></tbody></table>

To configure the Passthrough on ether1 host 00:0C:42:03:06:AB:

[?](https://help.mikrotik.com/docs/display/ROS/LTE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; </code><code class="ros constants">/interface lte apn </code><code class="ros functions">add </code><code class="ros value">apn</code><code class="ros plain">=apn1</code> <code class="ros value">passthrough-interface</code><code class="ros plain">=ether1</code> <code class="ros value">passthrough-mac</code><code class="ros plain">=00:0C:42:03:06:AB</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; </code><code class="ros constants">/interface lte </code><code class="ros functions">set </code><code class="ros plain">lte1 </code><code class="ros value">apn-profiles</code><code class="ros plain">=apn1</code></div></div></td></tr></tbody></table>

To configure multiple APNs on ether1 and ether2:

[?](https://help.mikrotik.com/docs/display/ROS/LTE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; </code><code class="ros constants">/interface lte apn </code><code class="ros functions">add </code><code class="ros value">apn</code><code class="ros plain">=apn1</code> <code class="ros value">passthrough-interface</code><code class="ros plain">=ether1</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; </code><code class="ros constants">/interface lte apn </code><code class="ros functions">add </code><code class="ros value">apn</code><code class="ros plain">=apn2</code> <code class="ros value">passthrough-interface</code><code class="ros plain">=ether2</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; </code><code class="ros constants">/interface lte </code><code class="ros functions">set </code><code class="ros plain">lte1 </code><code class="ros value">apn-profiles</code><code class="ros plain">=apn1,apn2</code></div></div></td></tr></tbody></table>

To configure multiple APNs with the same APN for different interfaces:

[?](https://help.mikrotik.com/docs/display/ROS/LTE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; </code><code class="ros constants">/interface lte apn </code><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=interface1</code> <code class="ros value">apn</code><code class="ros plain">=apn1</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; </code><code class="ros constants">/interface lte apn </code><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=interface2</code> <code class="ros value">apn</code><code class="ros plain">=apn1</code> <code class="ros value">passthrough-interface</code><code class="ros plain">=ether1</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; </code><code class="ros constants">/interface lte </code><code class="ros functions">set </code><code class="ros plain">lte1 </code><code class="ros value">apn-profiles</code><code class="ros plain">=interface1</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; </code><code class="ros constants">/interface lte </code><code class="ros functions">set </code><code class="ros plain">lte2 </code><code class="ros value">apn-profiles</code><code class="ros plain">=interface2</code></div></div></td></tr></tbody></table>

## Dual SIM  

### Boards with switchable SIM slots

| RouterBoard | Modem slot | SIM slots | Switchable |
| ----------- | ---------- | --------- | ---------- |
| RouterBoard | Modem slot | SIM slots | Switchable |
| ---         | ---        | ---       | ---        |
| LtAP        |
  
 | lower | 2 | 3 | Y |
| upper | 1 | N |
| LtAP mini |   
 | up | down | Y |
| SXT R |   
 | a |  b | Y |

SIM slots switching commands

-   RouterOS v7

[?](https://help.mikrotik.com/docs/display/ROS/LTE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface lte settings </code><code class="ros functions">set </code><code class="ros value">sim-slot</code><code class="ros plain">=down</code></div></div></td></tr></tbody></table>

-   RouterOS v6 after 6.45.1

[?](https://help.mikrotik.com/docs/display/ROS/LTE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/system routerboard modem </code><code class="ros functions">set </code><code class="ros value">sim-slot</code><code class="ros plain">=down</code></div></div></td></tr></tbody></table>

-   RouterOS v6 pre 6.45.1:

[?](https://help.mikrotik.com/docs/display/ROS/LTE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/system routerboard sim </code><code class="ros functions">set </code><code class="ros value">sim-slot</code><code class="ros plain">=down</code></div></div></td></tr></tbody></table>

For more reference please see board block diagram,  Quick Guide and User manual.

### Usage Example

Follow this link - [Dual SIM Application](https://wiki.mikrotik.com/wiki/Dual_SIM_Application "Dual SIM Application"), to see examples of how to change SIM slot based on roaming status and in case the interface status is down with help of RouterOS scripts and scheduler.

## Tips and Tricks

This paragraph contains information for additional features and usage cases.

### Find device location using Cell information

On devices using R11e-LTE International version card (wAP LTE kit) some extra information is provided under info command (from 6.41rc61)

```
   current-operator: 24701
                lac: 40
     current-cellid: 2514442
```

| 
Property

 | 

Description

 |     |
 | --- |  |
 |     |

Property

 | 

Description

 |                                             |
 | ------------------------------------------- | ------------------------------------------------------------------------------------ |
 | **current-operator** (_integer_; Default: ) | Contains MCC and MNC. For example: current-operator: 24701 breaks to: MCC=247 MNC=01 |
 | **lac** (_integer_; Default: )              | location area code (LAC)                                                             |
 | **current-cellid** (_integer_; Default: )   | Station identification number                                                        |

Values can be used to find location in databases: [Cell Id Finder](https://cellidfinder.com/cells/findcell)

### Using Cell lock

It is possible to lock R11e-LTE, R11e-LTE6 and R11e-4G modems and equipped devices to exact LTE tower. LTE info command provides currently used cellular tower information:

```
         phy-cellid: 384
             earfcn: 1300 (band 3, bandwidth 20Mhz)
```

| 
Property

 | 

Description

 |     |
 | --- |  |
 |     |

Property

 | 

Description

 |                                       |
 | ------------------------------------- | ---------------------------------------------------------------- |
 | **phy-cellid** (_integer_; Default: ) | Physical Cell Identification (PCI) of currently used cell tower. |
 | **earfcn** (_integer_; Default: )     | Absolute Radio Frequency Channel Number                          |

Exact tower location as well as available bands and other information can be acquired from mobile carrier or by using online services:

[CellMapper](https://www.cellmapper.net/map)

By using those acquired variables it's possible to send AT command to modem for locking to tower in current format:

**for R11e-LTE and R11e-LTE6**

```
AT*Cell=<mode>,<NetworkMode>,<band>,<EARFCN>,<PCI>

where

<mode> :
0 – Cell/Frequency disabled
1 – Frequency lock enabled
2 – Cell lock enabled

<NetworkMode>
0 – GSM
1 – UMTS_TD
2 – UMTS_WB
3 – LTE

<band>
Not in use, leave this blank

<EARFCN>
earfcn from lte info

<PCI>
phy-cellid from lte info
```

To lock modem at previously used tower at-chat can be used:

[?](https://help.mikrotik.com/docs/display/ROS/LTE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface lte at-chat lte1 input="AT*Cell=2,3,,1300,384"</code></div></div></td></tr></tbody></table>

For R11e-LTE all set on locks are lost after reboot or modem reset. Cell data can be also gathered from "cell-monitor".

For R11e-LTE6 cell lock works only for the primary band, this can be useful if you have multiple channels on the same band and you want to lock it to a specific earfcn. Note, that cell lock is not band-specific and for ca-band it can also use other frequency bands, unless you use band lock.

Use cell lock to set the primary band to the 1300 earfcn and use the second channel for the ca-band:

[?](https://help.mikrotik.com/docs/display/ROS/LTE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface lte at-chat lte1 input="AT*Cell=2,3,,1300,138"</code></div></div></td></tr></tbody></table>

Now it uses the earfcn: 1300 for the primary channel:

```
         primary-band: B3@20Mhz earfcn: 1300 phy-cellid: 138
              ca-band: B3@5Mhz earfcn: 1417 phy-cellid: 138
```

You can also set it the other way around:

[?](https://help.mikrotik.com/docs/display/ROS/LTE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface lte at-chat lte1 input="AT*Cell=2,3,,1417,138"</code></div></div></td></tr></tbody></table>

Now it uses the earfcn: 1417 for the primary channel:

```
         primary-band: B3@5Mhz earfcn: 1417 phy-cellid: 138
              ca-band: B3@20Mhz earfcn: 1300 phy-cellid: 138
```

For R11e-LTE6 modem cell lock information will not be lost after reboot or modem reset. To remove cell lock use at-chat command:

[?](https://help.mikrotik.com/docs/display/ROS/LTE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface lte at-chat lte1 input="AT*Cell=0"</code></div></div></td></tr></tbody></table>

**for R11e-4G**

```
AT%CLCMD=<mode>,<mode2>,<EARFCN>,<PCI>,<PLMN>
AT%CLCMD=1,1,3250,244,\"24705\"

where

<mode> :
0 – Cell/Frequency disabled
1 – Cell lock enabled

<mode2> :
0 - Save lock for first scan
1 - Always use lock 
(after each reset modem will clear out previous settings no matter what is used here)

<EARFCN>
earfcn from lte info

<PCI>
phy-cellid from lte info

<PLMN>
Mobile operator code
```

All PLMN codes available [here](https://en.wikipedia.org/wiki/Mobile_country_code) this variable can be also left blank

To lock modem to the cell - modem needs to be in non operating state, easiest way for **R11e-4G** modem is to add CellLock line to "modem-init" string:

[?](https://help.mikrotik.com/docs/display/ROS/LTE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface lte </code><code class="ros functions">set </code><code class="ros plain">lte1 </code><code class="ros value">modem-init</code><code class="ros plain">=</code><code class="ros string">"AT%CLCMD=1,1,3250,244,\"24705\""</code></div></div></td></tr></tbody></table>

Multiple cells can also be added by providing list instead of one tower information in following format:

```
AT%CLCMD=<mode>,<mode2>,<EARFCN_1>,<PCI_1>,<PLMN_1>,<EARFCN_2>,<PCI_2>,<PLMN_2>
```

For example to lock to two different PCIs within same band and operator:

[?](https://help.mikrotik.com/docs/display/ROS/LTE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface lte </code><code class="ros functions">set </code><code class="ros plain">lte1 </code><code class="ros value">modem-init</code><code class="ros plain">=</code><code class="ros string">"AT%CLCMD=1,1,6300,384,\"24701\",6300,385,\"24701\""</code></div></div></td></tr></tbody></table>

**for Chateau LTE12, Chateau 5G and LHG LTE18  
**

```
AT+QNWLOCK="common/4g",<num of cells>,[[<freq>,<pci>],...]
AT+QNWLOCK=\"common/4g\",1,6300,384

where

<num of cells>
number of cells to cell lock

<freq>
earfcn from lte info

<pci>
phy-cellid from lte info

```

Single cell lock example:

[?](https://help.mikrotik.com/docs/display/ROS/LTE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface/lte/at-chat lte1 input="AT+QNWLOCK=\"common/4g\",1,3050,448"</code></div></div></td></tr></tbody></table>

  

Multiple cells can also be added to cell lock. For example to lock to two different cells:

[?](https://help.mikrotik.com/docs/display/ROS/LTE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface/lte/at-chat lte1 input="AT+QNWLOCK=\"common/4g\",2,3050,448,1574,474"</code></div></div></td></tr></tbody></table>

  

To remove the cell lock use this at-chat command:

[?](https://help.mikrotik.com/docs/display/ROS/LTE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface/lte/at-chat lte1 input="at+qnwlock=\"common/4g\",0"</code></div></div></td></tr></tbody></table>

  

1\. Cell lock information will not be saved after a reboot or modem reset. 2. AT+QNWLOCK command can lock the cell and frequency. Therefore, the module can be given priority to register to the locked cell, however, according to the 3gpp protocol, the module will be redirected or handover to a cell with better signal instructions, even if it is not within the lock of the command. This phenomenon is normal.

### Cell Monitor

Cell monitor allows to scan available nearby mobile network cells:

[?](https://help.mikrotik.com/docs/display/ROS/LTE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; </code><code class="ros constants">/interface lte cell-</code><code class="ros functions">monitor </code><code class="ros plain">lte1</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">PHY-CELLID BAND&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; PSC EARFCN&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; RSRP&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; RSRQ&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; RSSI&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; SINR</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">49 B20&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 6300&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -110dBm&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -19.5dB</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">272 B20&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 6300&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -116dBm&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -19.5dB</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">374 B20&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 6300&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -108dBm&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -16dB</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">384 B1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 150&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -105dBm&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -13.5dB</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">384 B3&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 1300&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -106dBm&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -12dB</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">384 B7&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 2850&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -107dBm&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -11.5dB</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">432 B7&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 2850&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -119dBm&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -19.5dB</code></div></div></td></tr></tbody></table>

Gathered data can be used for more precise location detection or for Cell lock.

Not all modems support this feature

## Troubleshooting

Enable LTE logging:

[?](https://help.mikrotik.com/docs/display/ROS/LTE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; </code><code class="ros constants">/system logging </code><code class="ros functions">add </code><code class="ros value">topics</code><code class="ros plain">=lte</code></div></div></td></tr></tbody></table>

Check for errors in log:

[?](https://help.mikrotik.com/docs/display/ROS/LTE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; </code><code class="ros constants">/</code><code class="ros functions">log </code><code class="ros plain">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">11</code><code class="ros constants">:08:59 lte,async lte1: sent AT+CPIN?</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">11</code><code class="ros constants">:08:59 lte,async lte1: rcvd +CME ERROR: 10</code></div></div></td></tr></tbody></table>

search for CME error description online,

in this case: CME error 10 - SIM not inserted

### Locking band on Huawei and other modems

To lock band for Huawei modems `/interface lte set lte1 band=""` option can't be used.

It is possible to use AT commands to lock to desired band manually.

To check all supported bands run at-chat command:

[?](https://help.mikrotik.com/docs/display/ROS/LTE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] </code><code class="ros constants">/interface lte at-chat lte1 input="AT^SYSCFGEX=\?"</code></div><div class="line number2 index1 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">output</code><code class="ros constants">: ^SYSCFGEX: ("00","03","02","01","99"),((2000004e80380,"GSM850/GSM900/GSM1800/GSM1900/WCDMA BCI/WCDMA BCII/WCDMA BCV/WCDMA BCVIII"),</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">(3fffffff,</code><code class="ros string">"All Bands"</code><code class="ros plain">)),(0-2),(0-4),((800d7,"LTE BC1</code><code class="ros constants">/LTE BC2/LTE</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">BC3</code><code class="ros constants">/LTE BC5/LTE BC7/LTE BC8/LTE BC20"),(7fffffffffffffff,"All Bands"))</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">OK</code></div></div></td></tr></tbody></table>

Example to lock to LTE band 7:

[?](https://help.mikrotik.com/docs/display/ROS/LTE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] </code><code class="ros constants">/interface lte </code><code class="ros functions">set </code><code class="ros plain">lte1 </code><code class="ros value">modem-init</code><code class="ros plain">=</code><code class="ros string">"AT^SYSCFGEX=\"03\",3FFFFFFF,2,4,40,,"</code></div></div></td></tr></tbody></table>

Change last part **40** to desired band specified hexadecimal value where:

```
4 LTE BC3
40 LTE BC7
80000 LTE BC20
7FFFFFFFFFFFFFFF  All bands
etc
```

All band HEX values and AT commands can be found in [Huawei AT Command Interface Specification guide](https://download-c.huawei.com/download/downloadCenter?downloadId=29741&version=72288&siteCode=)

Check if band is locked:

[?](https://help.mikrotik.com/docs/display/ROS/LTE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] </code><code class="ros constants">/interface lte at-chat lte1 input="AT^SYSCFGEX\?"</code></div><div class="line number2 index1 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">output</code><code class="ros constants">: ^SYSCFGEX: "03",3FFFFFFF,0,2,40</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">OK</code></div></div></td></tr></tbody></table>

For more information check modem manufacturers AT command reference manuals.

### mPCIe modems with RB9xx series devices

In case your modem is not being recognized after a soft reboot, then you might need to add a delay before the USB port is being initialized. This can be done using the following command:

[?](https://help.mikrotik.com/docs/display/ROS/LTE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/system routerboard settings </code><code class="ros functions">set </code><code class="ros value">init-delay</code><code class="ros plain">=5s</code></div></div></td></tr></tbody></table>

### Boards with USB-A port and mPCIe  

Some devices such as specific RB9xx's and the RBLtAP-2HnD share the same USB lines between a single mPCIe slot and a USB-A port. If auto switch is not taking place and a modem is not getting detected, you might need to switch manually to either use the USB-A or mini-PCIe:

[?](https://help.mikrotik.com/docs/display/ROS/LTE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/system routerboard usb </code><code class="ros functions">set </code><code class="ros value">type</code><code class="ros plain">=mini-PCIe</code></div></div></td></tr></tbody></table>

### Modem firmware upgrade

Before attempting LTE modem firmware upgrade - upgrade RouterOS version to latest releases [How To Upgrade RouterOS](https://wiki.mikrotik.com/wiki/Manual:Upgrading_RouterOS)

  
Starting from RouterOS version 6.44beta20 it is possible to upgrade modems firmware. The firmware upgrade is also possible for the Chateau series products starting from 7.1beta1 version.

Firmware update is available only as FOTA Firmware Over The Air - firmware upgrade can only be done through working mobile connection for:

-   )R11e-LTE
-   )R11e-LTE-US

Firmware update available as FOTA and as well as upgrade from file for:

-   )R11e-4G
-   )R11e-LTE6

Firmware update available as FOTA with access to the internet over any interface:

-   )EG12-EA (Chateau LTE12)
-   )RG502Q-EA (Chateau 5G)
-   )EG18-EA (LHG LTE18)

Firmware updates usually includes small improvements in stability or small bug fixes that can't be included into RouterOS.

Check currently used firmware version by running:

[?](https://help.mikrotik.com/docs/display/ROS/LTE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; </code><code class="ros constants">/interface lte </code><code class="ros functions">info </code><code class="ros plain">lte1 once</code></div><div class="line number2 index1 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">-----</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">revision</code><code class="ros constants">: "MikroTik_CP_2.160.000_v008"</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">-----</code></div></div></td></tr></tbody></table>

Check if new firmware is available:

[?](https://help.mikrotik.com/docs/display/ROS/LTE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; </code><code class="ros constants">/interface lte firmware-</code><code class="ros functions">upgrade </code><code class="ros plain">lte1</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">installed</code><code class="ros constants">: MikroTik_CP_2.160.000_v008</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">latest</code><code class="ros constants">: MikroTik_CP_2.160.000_v010</code></div></div></td></tr></tbody></table>

Upgrade firmware:

[?](https://help.mikrotik.com/docs/display/ROS/LTE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; interface lte firmware-</code><code class="ros functions">upgrade </code><code class="ros plain">lte1 </code><code class="ros value">upgrade</code><code class="ros plain">=yes</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">status</code><code class="ros constants">: downloading via LTE connection (&gt;2min)</code></div></div></td></tr></tbody></table>

Whole upgrade process may take up to 10 minutes, depending on mobile connection speed.

After successful upgrade issue USB power-reset, reboot device or run AT+reset command, to update modem version readout under info command:

[?](https://help.mikrotik.com/docs/display/ROS/LTE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; </code><code class="ros constants">/interface lte at-chat lte1 input="AT+reset"</code></div></div></td></tr></tbody></table>

if modem has issues connecting to cells after update, or there are any other unrelated issues - wipe old configuration with:

[?](https://help.mikrotik.com/docs/display/ROS/LTE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface lte at-chat lte1 input="AT+RSTSET"</code></div></div></td></tr></tbody></table>

### Avoiding tethering speed throttling

Some operators (TMobile, YOTA etc.) allows unlimited data only for device SIM card is used on, all other data coming from mobile hotspots or tethering is highly limited by volume or by throughput speed. [Some sources](https://www.reddit.com/r/hacking/comments/54a7dd/bypassing_tmobiles_tethering_data_capthrottling/) have found out that this limitation is done by monitoring TTL (Time To Live) values from packets to determinate if limitations need to be applied (TTL is decreased by 1 for each "hop" made). RouterOS allows changing the TTL parameter for packets going from the router to allow hiding sub networks. Keep in mind that this may conflict with fair use policy.

[?](https://help.mikrotik.com/docs/display/ROS/LTE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">IPv4 mangle rule</code><code class="ros constants">:</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros constants">/ip firewall mangle</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=change-ttl</code> <code class="ros value">chain</code><code class="ros plain">=postrouting</code> <code class="ros value">new-ttl</code><code class="ros plain">=set:65</code> <code class="ros value">out-interface</code><code class="ros plain">=lte1</code> <code class="ros value">passthrough</code><code class="ros plain">=yes</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">IPv6 mangle rule</code><code class="ros constants">:</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros constants">/ipv6 firewall mangle</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=change-hop-limit</code> <code class="ros value">chain</code><code class="ros plain">=postrouting</code> <code class="ros value">new-hop-limit</code><code class="ros plain">=set:65</code> <code class="ros value">passthrough</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

More information: [YOTA](https://m.habr.com/en/post/238351/), [TMobile](https://www.reddit.com/r/mikrotik/comments/acq4kz/anyone_familiar_with_configuring_the_ltap_us_with/)

### Unlocking SIM card after multiple wrong PIN code attempts

After locking SIM card, unlock can be done through "at-chat"

Check current PIN code status:

[?](https://help.mikrotik.com/docs/display/ROS/LTE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface lte at-chat lte1 input="at+cpin\?"</code></div></div></td></tr></tbody></table>

If card is locked - unlock it by providing:

[?](https://help.mikrotik.com/docs/display/ROS/LTE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface lte at-chat lte1 input="AT+CPIN=\"PUK_code\",\"NEW_PIN\""</code></div></div></td></tr></tbody></table>

Replace PUK\_code and NEW\_PIN with matching values.

The command for sim slot selection changes in v6.45.1 and again in v7. Some device models like SXT, have SIM slots named "a" and "b" instead of "up" and down"