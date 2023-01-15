# Summary

___

The CCR3xx, CRS5xx series switches and CCR2116, CCR2216 routers have highly integrated switches with high-performance CPU and feature-rich packet processors. These devices can be designed into various Ethernet applications including unmanaged switch, Layer 2 managed switch, carrier switch, inter-VLAN router, and wired unified packet processor.

This article applies to CRS3xx, CRS5xx series switches, CCR2116, CCR2216 routers, and not to [CRS1xx/CRS2xx series switches](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=103841835).

## Features

| 
Features

 | 

Description

 |     |
 | --- |  |
 |     |

Features

 | 

Description

 |                |
 | -------------- |  |
 | **Forwarding** |

-   Configurable ports for switching or routing
-   Full non-blocking wire-speed switching
-   Large Unicast FDB for Layer 2 unicast forwarding
-   Forwarding Databases works based on IVL
-   Jumbo frame support
-   IGMP Snooping support
-   DHCP Snooping with Option 82 

 |
| **Routing** | 

-   Layer 3 Hardware Offloading:
    -   IPv4 Unicast Routing
    -   Supported on Ethernet, Bridge, Bonding, and VLAN interfaces
    -   ECMP
    -   Blackholes
    -   Offloaded Fasttrack connections (applies only to certain switch models)
    -   Offloaded NAT for Fasttrack connections (applies only to certain switch models)
    -   Multiple MTU profiles

 |
| **Spanning Tree Protocol** | 

-   STP
-   RSTP
-   MSTP

 |
| **Mirroring** | 

-   Various types of mirroring:
    -   Port based mirroring
    -   VLAN based mirroring
    -   MAC based mirroring

 |
| **VLAN** | 

-   Fully compatible with IEEE802.1Q and IEEE802.1ad VLAN
-   4k active VLANs
-   Flexible VLAN assignment:
    -   Port based VLAN
    -   Protocol based VLAN
    -   MAC based VLAN
-   VLAN filtering
-   From any to any VLAN translation

 |
| **Bonding** | 

-   Supports 802.3ad (LACP) and balance-xor modes
-   Up to 8 member ports per bonding interface
-   Hardware automatic failover and load balancing
-   MLAG

 |
| **Traffic Shaping** | 

-   Ingress traffic limiting

-   Port based
-   MAC based
-   IP based
-   VLAN based
-   Protocol based
-   DSCP based

-   Port based egress traffic limiting

 |
| **Port isolation** | 

-   Applicable for Private VLAN implementation

 |
| **Access Control List** | 

-   Ingress ACL tables
-   Classification based on ports, L2, L3, L4 protocol header fields
-   ACL actions include filtering, forwarding and modifying of the protocol header fields

 |

## Models

This table clarifies the main differences between Cloud Router Switch models and CCR routers.

<table class="wrapped confluenceTable" style="text-align: center;" resolved=""><colgroup><col><col><col><col><col><col><col><col><col><col><col><col></colgroup><tbody><tr><td class="highlight-grey confluenceTd" title="Background colour : undefined" data-highlight-colour="grey"><strong title=""><u>Model</u></strong></td><td class="highlight-grey confluenceTd" title="Background colour : undefined" data-highlight-colour="grey"><strong title="">Switch Chip</strong></td><td class="highlight-grey confluenceTd" title="Background colour : undefined" data-highlight-colour="grey"><strong title="">CPU</strong></td><td class="highlight-grey confluenceTd" title="Background colour : undefined" data-highlight-colour="grey"><strong title="">Cores</strong></td><td class="highlight-grey confluenceTd" title="Background colour : undefined" data-highlight-colour="grey"><strong title="">10G SFP+</strong></td><td class="highlight-grey confluenceTd" title="Background color : " data-highlight-colour="grey"><strong title="">10G Ethernet</strong></td><td class="highlight-grey confluenceTd" title="Background color : " data-highlight-colour="grey"><strong title="">25G SFP28</strong></td><td class="highlight-grey confluenceTd" title="Background color : " data-highlight-colour="grey"><strong title="">40G QSFP+</strong></td><td class="highlight-grey confluenceTd" title="Background color : " data-highlight-colour="grey"><strong title="">100G QSFP28</strong></td><td class="highlight-grey confluenceTd" title="Background colour : undefined" data-highlight-colour="grey"><strong title="">ACL rules</strong></td><td class="highlight-grey confluenceTd" title="Background colour : undefined" data-highlight-colour="grey"><strong title="">Unicast FDB entries</strong></td><td class="highlight-grey confluenceTd" title="Background colour : undefined" data-highlight-colour="grey"><strong title="">Jumbo Frame (Bytes)</strong></td></tr><tr><td class="confluenceTd">netPower 15FR (CRS318-1Fi-15Fr-2S)</td><td class="confluenceTd"><strong>Marvell-98DX224S</strong></td><td class="confluenceTd"><strong>800MHz</strong></td><td class="confluenceTd"><strong>1</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>128</strong></td><td class="confluenceTd"><strong>16,000</strong></td><td class="confluenceTd"><strong>10218</strong></td></tr><tr><td class="confluenceTd">netPower 16P (CRS318-16P-2S+)</td><td class="confluenceTd"><strong>Marvell-98DX226S</strong></td><td class="confluenceTd"><strong>800MHz</strong></td><td class="confluenceTd"><strong>1</strong></td><td class="confluenceTd"><strong>2</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>128</strong></td><td class="confluenceTd"><strong>16,000</strong></td><td class="confluenceTd"><strong>10218</strong></td></tr><tr><td class="confluenceTd">CRS310-1G-5S-4S+ (netFiber 9/IN)</td><td class="confluenceTd"><strong>Marvell-98DX226S</strong></td><td class="confluenceTd"><strong>800MHz</strong></td><td class="confluenceTd"><strong>1</strong></td><td class="confluenceTd"><strong>4</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>128</strong></td><td class="confluenceTd"><strong>16,000</strong></td><td class="confluenceTd"><strong>10218</strong></td></tr><tr><td class="confluenceTd">CRS326-24G-2S+ (RM/IN)</td><td class="confluenceTd"><strong>Marvell-98DX3236</strong></td><td class="confluenceTd"><strong>800MHz</strong></td><td class="confluenceTd"><strong>1</strong></td><td class="confluenceTd"><strong>2</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>128</strong></td><td class="confluenceTd"><strong>16,000</strong></td><td class="confluenceTd"><strong>10218</strong></td></tr><tr><td class="confluenceTd">CRS328-24P-4S+</td><td class="confluenceTd"><strong>Marvell-98DX3236</strong></td><td class="confluenceTd"><strong>800MHz</strong></td><td class="confluenceTd"><strong>1</strong></td><td class="confluenceTd"><strong>4</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>128</strong></td><td class="confluenceTd"><strong>16,000</strong></td><td class="confluenceTd"><strong>10218</strong></td></tr><tr><td class="confluenceTd">CRS328-4C-20S-4S+</td><td class="confluenceTd"><strong>Marvell-98DX3236</strong></td><td class="confluenceTd"><strong>800MHz</strong></td><td class="confluenceTd"><strong>1</strong></td><td class="confluenceTd"><strong>4</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>128</strong></td><td class="confluenceTd"><strong>16,000</strong></td><td class="confluenceTd"><strong>10218</strong></td></tr><tr><td class="confluenceTd">CRS305-1G-4S+</td><td class="confluenceTd"><strong>Marvell-98DX3236</strong></td><td class="confluenceTd"><strong>800MHz</strong></td><td class="confluenceTd"><strong>1</strong></td><td class="confluenceTd"><strong>4</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>128</strong></td><td class="confluenceTd"><strong>16,000</strong></td><td class="confluenceTd"><strong>10218</strong></td></tr><tr><td class="confluenceTd">CRS309-1G-8S+</td><td class="confluenceTd"><strong>Marvell-98DX8208</strong></td><td class="confluenceTd"><strong>800MHz</strong></td><td class="confluenceTd"><strong>2</strong></td><td class="confluenceTd"><strong>8</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>1024</strong></td><td class="confluenceTd"><strong>32,000</strong></td><td class="confluenceTd"><strong>10218</strong></td></tr><tr><td class="confluenceTd">CRS317-1G-16S+</td><td class="confluenceTd"><strong>Marvell-98DX8216</strong></td><td class="confluenceTd"><strong>800MHz</strong></td><td class="confluenceTd"><strong>2</strong></td><td class="confluenceTd"><strong>16</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>1024</strong></td><td class="confluenceTd"><strong>128,000</strong></td><td class="confluenceTd"><strong>10218</strong></td></tr><tr><td class="confluenceTd">CRS312-4C+8XG</td><td class="confluenceTd"><strong>Marvell-98DX8212</strong></td><td class="confluenceTd"><strong>650MHz</strong></td><td class="confluenceTd"><strong>1</strong></td><td class="confluenceTd"><strong>4 (combo ports)</strong></td><td class="confluenceTd"><strong>8 + 4 (combo ports)</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>512</strong></td><td class="confluenceTd"><strong>32,000</strong></td><td class="confluenceTd"><strong>10218</strong></td></tr><tr><td class="confluenceTd">CRS326-24S+2Q+</td><td class="confluenceTd"><strong>Marvell-98DX8332</strong></td><td class="confluenceTd"><strong>650MHz</strong></td><td class="confluenceTd"><strong>1</strong></td><td class="confluenceTd"><strong>24</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>2</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>256</strong></td><td class="confluenceTd"><strong>32,000</strong></td><td class="confluenceTd"><strong>10218</strong></td></tr><tr><td class="confluenceTd">CRS354-48G-4S+2Q+</td><td class="confluenceTd"><strong>Marvell-98DX3257</strong></td><td class="confluenceTd"><strong>650MHz</strong></td><td class="confluenceTd"><strong>1</strong></td><td class="confluenceTd"><strong>4</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>2</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>170</strong></td><td class="confluenceTd"><strong>32,000</strong></td><td class="confluenceTd"><strong>10218</strong></td></tr><tr><td class="confluenceTd">CRS354-48P-4S+2Q+</td><td class="confluenceTd"><strong>Marvell-98DX3257</strong></td><td class="confluenceTd"><strong>650MHz</strong></td><td class="confluenceTd"><strong>1</strong></td><td class="confluenceTd"><strong>4</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>2</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>170</strong></td><td class="confluenceTd"><strong>32,000</strong></td><td class="confluenceTd"><strong>10218</strong></td></tr><tr><td class="confluenceTd">CRS504-4XQ-IN</td><td class="confluenceTd"><strong>Marvell-98DX4310</strong></td><td class="confluenceTd"><strong>650MHz</strong></td><td class="confluenceTd"><strong>1</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>4</strong></td><td class="confluenceTd"><strong>1024</strong></td><td class="confluenceTd"><strong>128,000</strong></td><td class="confluenceTd"><strong>10218</strong></td></tr><tr><td class="confluenceTd">CRS518-16XS-2XQ</td><td class="confluenceTd"><strong>Marvell-98DX8525</strong></td><td class="confluenceTd"><strong>650MHz</strong></td><td class="confluenceTd"><strong>1</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>16</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>2</strong></td><td class="confluenceTd"><strong>1024</strong></td><td class="confluenceTd"><strong>128,000</strong></td><td class="confluenceTd"><strong>10218</strong></td></tr><tr><td class="confluenceTd">CCR2116-12G-4S+</td><td class="confluenceTd"><strong>Marvell-98DX3255</strong></td><td class="confluenceTd"><strong>2000MHz</strong></td><td class="confluenceTd"><strong>16</strong></td><td class="confluenceTd"><strong>4</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>512</strong></td><td class="confluenceTd"><strong>32,000</strong></td><td class="confluenceTd"><strong>9570</strong></td></tr><tr><td class="confluenceTd">CCR2216-1G-12XS-2XQ</td><td class="confluenceTd"><strong>Marvell-98DX8525</strong></td><td class="confluenceTd"><strong>2000MHz</strong></td><td class="confluenceTd"><strong>16</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>12</strong></td><td class="confluenceTd"><strong>-</strong></td><td class="confluenceTd"><strong>2</strong></td><td class="confluenceTd"><strong>1024</strong></td><td class="confluenceTd"><strong>128,000</strong></td><td class="confluenceTd"><strong>9570</strong></td></tr></tbody></table>

For L3 hardware offloading feature support and hardware limits, please refer to [Feature Support](https://help.mikrotik.com/docs/display/ROS/L3+Hardware+Offloading#L3HardwareOffloading-L3HWFeatureSupport) and [Device Support](https://help.mikrotik.com/docs/display/ROS/L3+Hardware+Offloading#L3HardwareOffloading-L3HWDeviceSupport) user manuals.

## Abbreviations

-   FDB - Forwarding Database
-   MDB - Multicast Database
-   SVL - Shared VLAN Learning
-   IVL - Independent VLAN Learning
-   PVID - Port VLAN ID
-   ACL - Access Control List
-   CVID - Customer VLAN ID
-   SVID - Service VLAN ID

# Port switching

___

In order to set up a port switching, check the [Bridge Hardware Offloading](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-BridgeHardwareOffloading) page.

Currently, it is possible to create only one bridge with hardware offloading. Use the `hw=yes/no` parameter to select which bridge will use hardware offloading.

  

Bridge STP/RSTP/MSTP, IGMP Snooping and VLAN filtering settings don't affect hardware offloading, since RouterOS v6.42 Bonding interfaces are also hardware offloaded.

# VLAN

___

Since RouterOS version 6.41, a bridge provides VLAN aware Layer2 forwarding and VLAN tag modifications within the bridge. This set of features makes bridge operation more like a traditional Ethernet switch and allows to overcome Spanning Tree compatibility issues compared to the configuration when tunnel-like VLAN interfaces are bridged. Bridge VLAN Filtering configuration is highly recommended to comply with STP (802.1D), RSTP (802.1w) standards and it is mandatory to enable MSTP (802.1s) support in RouterOS.

## VLAN Filtering

VLAN filtering is described on the [Bridge VLAN Filtering](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-BridgeVLANFiltering) section.

VLAN setup examples

Below are describes some of the most common ways how to utilize VLAN forwarding.

### Port-Based VLAN

The configuration is described on the [Bridge VLAN FIltering](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-BridgeVLANFiltering) section.

### MAC Based VLAN

-   The Switch Rule table is used for MAC Based VLAN functionality, see [this table](https://help.mikrotik.com/docs/display/ROS/CRS3xx%2C+CRS5xx%2C+CCR2116%2C+CCR2216+switch+chip+features#CRS3xx,CRS5xx,CCR2116,CCR2216switchchipfeatures-Models) on how many rules each device supports.
-   MAC-based VLANs will only work properly between switch ports and not between switch ports and CPU. When a packet is being forwarded to the CPU, the `pvid` property for the bridge port will be always used instead of `new-vlan-id` from ACL rules.
-   MAC-based VLANs will not work for DHCP packets when DHCP snooping is enabled.

Enable switching on ports by creating a bridge with enabled hw-offloading:

[?](https://help.mikrotik.com/docs/display/ROS/CRS3xx%2C+CRS5xx%2C+CCR2116%2C+CCR2216+switch+chip+features#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=bridge1</code> <code class="ros value">vlan-filtering</code><code class="ros plain">=yes</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge port</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether2</code> <code class="ros value">hw</code><code class="ros plain">=yes</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether7</code> <code class="ros value">hw</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

Add VLANs in the Bridge VLAN table and specify ports:

[?](https://help.mikrotik.com/docs/display/ROS/CRS3xx%2C+CRS5xx%2C+CCR2116%2C+CCR2216+switch+chip+features#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge vlan</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">tagged</code><code class="ros plain">=ether2</code> <code class="ros value">untagged</code><code class="ros plain">=ether7</code> <code class="ros value">vlan-ids</code><code class="ros plain">=200,300,400</code></div></div></td></tr></tbody></table>

Add Switch rules which assign VLAN id based on MAC address:

[?](https://help.mikrotik.com/docs/display/ROS/CRS3xx%2C+CRS5xx%2C+CCR2116%2C+CCR2216+switch+chip+features#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface ethernet switch rule</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">switch</code><code class="ros plain">=switch1</code> <code class="ros value">ports</code><code class="ros plain">=ether7</code> <code class="ros value">src-mac-address</code><code class="ros plain">=A4:12:6D:77:94:43/FF:FF:FF:FF:FF:FF</code> <code class="ros value">new-vlan-id</code><code class="ros plain">=200</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">switch</code><code class="ros plain">=switch1</code> <code class="ros value">ports</code><code class="ros plain">=ether7</code> <code class="ros value">src-mac-address</code><code class="ros plain">=84:37:62:DF:04:20/FF:FF:FF:FF:FF:FF</code> <code class="ros value">new-vlan-id</code><code class="ros plain">=300</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">switch</code><code class="ros plain">=switch1</code> <code class="ros value">ports</code><code class="ros plain">=ether7</code> <code class="ros value">src-mac-address</code><code class="ros plain">=E7:16:34:A1:CD:18/FF:FF:FF:FF:FF:FF</code> <code class="ros value">new-vlan-id</code><code class="ros plain">=400</code></div></div></td></tr></tbody></table>

### Protocol Based VLAN

-   The Switch Rule table is used for Protocol Based VLAN functionality, see [this table](https://help.mikrotik.com/docs/display/ROS/CRS3xx%2C+CRS5xx%2C+CCR2116%2C+CCR2216+switch+chip+features#CRS3xx,CRS5xx,CCR2116,CCR2216switchchipfeatures-Models) on how many rules each device supports.
-   Protocol-based VLANs will only work properly between switch ports and not between switch ports and CPU. When a packet is being forwarded to the CPU, the `pvid` property for the bridge port will be always used instead of `new-vlan-id` from ACL rules.
-   Protocol-based VLANs will not work for DHCP packets when DHCP snooping is enabled.

Enable switching on ports by creating a bridge with enabled hw-offloading:

[?](https://help.mikrotik.com/docs/display/ROS/CRS3xx%2C+CRS5xx%2C+CCR2116%2C+CCR2216+switch+chip+features#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=bridge1</code> <code class="ros value">vlan-filtering</code><code class="ros plain">=yes</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge port</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether2</code> <code class="ros value">hw</code><code class="ros plain">=yes</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether6</code> <code class="ros value">hw</code><code class="ros plain">=yes</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether7</code> <code class="ros value">hw</code><code class="ros plain">=yes</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether8</code> <code class="ros value">hw</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

Add VLANs in the Bridge VLAN table and specify ports:

[?](https://help.mikrotik.com/docs/display/ROS/CRS3xx%2C+CRS5xx%2C+CCR2116%2C+CCR2216+switch+chip+features#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge vlan</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">tagged</code><code class="ros plain">=ether2</code> <code class="ros value">untagged</code><code class="ros plain">=ether6</code> <code class="ros value">vlan-ids</code><code class="ros plain">=200</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">tagged</code><code class="ros plain">=ether2</code> <code class="ros value">untagged</code><code class="ros plain">=ether7</code> <code class="ros value">vlan-ids</code><code class="ros plain">=300</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">tagged</code><code class="ros plain">=ether2</code> <code class="ros value">untagged</code><code class="ros plain">=ether8</code> <code class="ros value">vlan-ids</code><code class="ros plain">=400</code></div></div></td></tr></tbody></table>

Add Switch rules which assign VLAN id based on MAC protocol:

[?](https://help.mikrotik.com/docs/display/ROS/CRS3xx%2C+CRS5xx%2C+CCR2116%2C+CCR2216+switch+chip+features#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface ethernet switch rule</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">mac-protocol</code><code class="ros plain">=ip</code> <code class="ros value">new-vlan-id</code><code class="ros plain">=200</code> <code class="ros value">ports</code><code class="ros plain">=ether6</code> <code class="ros value">switch</code><code class="ros plain">=switch1</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">mac-protocol</code><code class="ros plain">=ipx</code> <code class="ros value">new-vlan-id</code><code class="ros plain">=300</code> <code class="ros value">ports</code><code class="ros plain">=ether7</code> <code class="ros value">switch</code><code class="ros plain">=switch1</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">mac-protocol</code><code class="ros plain">=0x80F3</code> <code class="ros value">new-vlan-id</code><code class="ros plain">=400</code> <code class="ros value">ports</code><code class="ros plain">=ether8</code> <code class="ros value">switch</code><code class="ros plain">=switch1</code></div></div></td></tr></tbody></table>

### VLAN Tunneling (Q-in-Q)

Since RouterOS v6.43 it is possible to use a provider bridge (IEEE 802.1ad) and Tag Stacking VLAN filtering, and hardware offloading at the same time. The configuration is described in the [Bridge VLAN Tunneling (Q-in-Q)](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-VLANTunneling(QinQ)) section.

Devices with switch chip Marvell-98DX3257 (e.g. CRS354 series) do not support VLAN filtering on 1Gbps Ethernet interfaces for other VLAN types (`0x88a8` and `0x9100`).

## Ingress VLAN translation

It is possible to translate a certain VLAN ID to a different VLAN ID using ACL rules on an ingress port. In this example we create two ACL rules, allowing bidirectional communication. This can be done by doing the following.

Create a new bridge and add ports to it with hardware offloading:

[?](https://help.mikrotik.com/docs/display/ROS/CRS3xx%2C+CRS5xx%2C+CCR2116%2C+CCR2216+switch+chip+features#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=bridge1</code> <code class="ros value">vlan-filtering</code><code class="ros plain">=no</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge port</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=ether1</code> <code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">hw</code><code class="ros plain">=yes</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=ether2</code> <code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">hw</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

Add ACL rules to translate a VLAN ID in each direction:

[?](https://help.mikrotik.com/docs/display/ROS/CRS3xx%2C+CRS5xx%2C+CCR2116%2C+CCR2216+switch+chip+features#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface ethernet switch rule</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">new-dst-ports</code><code class="ros plain">=ether2</code> <code class="ros value">new-vlan-id</code><code class="ros plain">=20</code> <code class="ros value">ports</code><code class="ros plain">=ether1</code> <code class="ros value">switch</code><code class="ros plain">=switch1</code> <code class="ros value">vlan-id</code><code class="ros plain">=10</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">new-dst-ports</code><code class="ros plain">=ether1</code> <code class="ros value">new-vlan-id</code><code class="ros plain">=10</code> <code class="ros value">ports</code><code class="ros plain">=ether2</code> <code class="ros value">switch</code><code class="ros plain">=switch1</code> <code class="ros value">vlan-id</code><code class="ros plain">=20</code></div></div></td></tr></tbody></table>

Add both VLAN IDs to the bridge VLAN table:

[?](https://help.mikrotik.com/docs/display/ROS/CRS3xx%2C+CRS5xx%2C+CCR2116%2C+CCR2216+switch+chip+features#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge vlan</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">tagged</code><code class="ros plain">=ether1</code> <code class="ros value">vlan-ids</code><code class="ros plain">=10</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">tagged</code><code class="ros plain">=ether2</code> <code class="ros value">vlan-ids</code><code class="ros plain">=20</code></div></div></td></tr></tbody></table>

Enable bridge VLAN filtering:

[?](https://help.mikrotik.com/docs/display/ROS/CRS3xx%2C+CRS5xx%2C+CCR2116%2C+CCR2216+switch+chip+features#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge </code><code class="ros functions">set </code><code class="ros plain">bridge1 </code><code class="ros value">vlan-filtering</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

Bidirectional communication is limited only between two switch ports. Translating VLAN ID between more ports can cause traffic flooding or incorrect forwarding between the same VLAN ports.

By enabling `vlan-filtering` you will be filtering out traffic destined to the CPU, before enabling VLAN filtering you should make sure that you set up a [Management port](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-Managementaccessconfiguration).

# (R/M)STP

___

CRS3xx, CRS5xx series switches, and CCR2116, CCR2216 routers are capable of running STP, RSTP, and MSTP on a hardware level. For more detailed information you should check out the [Spanning Tree Protocol](https://help.mikrotik.com/docs/display/ROS/Spanning+Tree+Protocol) manual page.

# Bonding

___

CRS3xx, CRS5xx series switches and CCR2116, CCR2216 routers support hardware offloading with bonding interfaces. Only `802.3ad` and `balance-xor` bonding modes are hardware offloaded, other bonding modes will use the CPU's resources. You can find more information about the bonding interfaces in the [Bonding Interface](https://help.mikrotik.com/docs/display/ROS/Bonding) section. If `802.3ad` mode is used, then LACP (Link Aggregation Control Protocol) is supported.

To create a hardware offloaded bonding interface, you must create a bonding interface with a supported bonding mode:

[?](https://help.mikrotik.com/docs/display/ROS/CRS3xx%2C+CRS5xx%2C+CCR2116%2C+CCR2216+switch+chip+features#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bonding</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">mode</code><code class="ros plain">=802.3ad</code> <code class="ros value">name</code><code class="ros plain">=bond1</code> <code class="ros value">slaves</code><code class="ros plain">=ether1,ether2</code></div></div></td></tr></tbody></table>

This interface can be added to a bridge alongside other interfaces:

[?](https://help.mikrotik.com/docs/display/ROS/CRS3xx%2C+CRS5xx%2C+CCR2116%2C+CCR2216+switch+chip+features#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=bridge</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge port</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">interface</code><code class="ros plain">=bond1</code> <code class="ros value">hw</code><code class="ros plain">=yes</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">interface</code><code class="ros plain">=ether3</code> <code class="ros value">hw</code><code class="ros plain">=yes</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">interface</code><code class="ros plain">=ether4</code> <code class="ros value">hw</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

Do not add interfaces to a bridge that are already in a bond, RouterOS will not allow you to add an interface to bridge that is already a slave port for bonding.

Make sure that the bonding interface is hardware offloaded by checking the "H" flag:

[?](https://help.mikrotik.com/docs/display/ROS/CRS3xx%2C+CRS5xx%2C+CCR2116%2C+CCR2216+switch+chip+features#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="text plain">/interface bridge port print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="text plain">Flags: X - disabled, I - inactive, D - dynamic, H - hw-offload</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;</code><code class="text plain">#&nbsp;&nbsp;&nbsp;&nbsp; INTERFACE&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; BRIDGE&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; HW</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;</code><code class="text plain">0&nbsp;&nbsp; H bond1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; bridge&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; yes</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;</code><code class="text plain">1&nbsp;&nbsp; H ether3&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; bridge&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; yes</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;</code><code class="text plain">2&nbsp;&nbsp; H ether4&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; bridge&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; yes</code></div></div></td></tr></tbody></table>

With HW-offloaded bonding interfaces, the built-in switch chip will always use Layer2+Layer3+Layer4 for a transmit hash policy, changing the transmit hash policy manually will have no effect.

# Multi-chassis Link Aggregation Group

___

MLAG (Multi-chassis Link Aggregation Group) implementation in RouterOS allows configuring LACP bonds on two separate devices, while the client device believes to be connected on the same machine. This provides a physical redundancy in case of switch failure. All CRS3xx, CRS5xx series and CCR2116, CCR2216 devices can be configured with MLAG. Read [here](https://help.mikrotik.com/docs/display/ROS/Multi-chassis+Link+Aggregation+Group) for more information.

# L3 Hardware Offloading

___

Layer3 hardware offloading (otherwise known as IP switching or HW routing) will allow to offload some of the router features onto the switch chip. This allows reaching wire speeds when routing packets, which simply would not be possible with the CPU. 

Offloaded feature set depends on the used chipset. Read [here](https://help.mikrotik.com/docs/display/ROS/L3+Hardware+Offloading) for more info.

# Port isolation

___

Since RouterOS v6.43 is it possible to create a Private VLAN setup, an example can be found in the [Switch chip port isolation](https://help.mikrotik.com/docs/display/ROS/Switch+Chip+Features#SwitchChipFeatures-Portisolation) manual page. Hardware offloaded bonding interfaces are not included in the switch port-isolation menu, but it is still possible to configure port-isolation individually on each secondary interface of the bonding.

# IGMP/MLD Snooping

___

CRS3xx, CRS5xx series switches and CCR2116, CCR2216 routers are capable of using IGMP/MLD Snooping on a hardware level. To see more detailed information, you should check out the [IGMP/MLD snooping](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=59277403) manual page.

# DHCP Snooping and DHCP Option 82

___

CRS3xx, CRS5xx series switches and CCR2116, CCR2216 routers are capable of using DHCP Snooping with Option 82 on a hardware level. The switch will create a dynamic ACL rule to capture the DHCP packets and redirect them to the main CPU for further processing. To see more detailed information, please visit the [DHCP Snooping and DHCP Option 82](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-DHCPSnoopingandDHCPOption82) manual page.

DHCP snooping will not work when hardware offloading bonding interfaces are created.

# Controller Bridge and Port Extender

___

Controller Bridge (CB) and Port Extender (PE) is an IEEE 802.1BR standard implementation in RouterOS. It allows virtually extending the CB ports with a PE device and managing these extended interfaces from a single controlling device. Such configuration provides a simplified network topology, flexibility, increased port density, and ease of manageability. See more details on [Controller Bridge and Port Extender manual](https://help.mikrotik.com/docs/display/ROS/Controller+Bridge+and+Port+Extender).

# Mirroring

___

Mirroring lets the switch sniff all traffic that is going in a switch chip and send a copy of those packets out to another port (mirror-target). This feature can be used to easily set up a tap device that allows you to inspect the traffic on your network on a traffic analyzer device. It is possible to set up a simple port-based mirroring, but it is also possible to set up more complex mirroring based on various parameters. Note that mirror-target port has to belong to the same switch (see which port belongs to which switch in `/interface ethernet` menu). Also, mirror-target can have a special 'cpu' value, which means that sniffed packets will be sent out of switch chips CPU port. There are many possibilities that can be used to mirror certain traffic, below you can find the most common mirroring examples:

Port Based Mirroring:

[?](https://help.mikrotik.com/docs/display/ROS/CRS3xx%2C+CRS5xx%2C+CCR2116%2C+CCR2216+switch+chip+features#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface ethernet switch</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">switch1 </code><code class="ros value">mirror-source</code><code class="ros plain">=ether2</code> <code class="ros value">mirror-target</code><code class="ros plain">=ether3</code></div></div></td></tr></tbody></table>

Property `mirror-source` will send an ingress and egress packet copies to the `mirror-target` port. Both `mirror-source` and `mirror-target` are limited to a single interface.

[?](https://help.mikrotik.com/docs/display/ROS/CRS3xx%2C+CRS5xx%2C+CCR2116%2C+CCR2216+switch+chip+features#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface ethernet switch</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">switch1 </code><code class="ros value">mirror-source</code><code class="ros plain">=none</code> <code class="ros value">mirror-target</code><code class="ros plain">=ether3</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/interface ethernet switch rule</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">mirror</code><code class="ros plain">=yes</code> <code class="ros value">ports</code><code class="ros plain">=ether1,ether2</code> <code class="ros value">switch</code><code class="ros plain">=switch1</code></div></div></td></tr></tbody></table>

Using ACL rules, it is possible to mirror packets from multiple `ports` interfaces. Only ingress packets are mirrored to `mirror-target` interface.

VLAN Based Mirroring:

[?](https://help.mikrotik.com/docs/display/ROS/CRS3xx%2C+CRS5xx%2C+CCR2116%2C+CCR2216+switch+chip+features#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">bridge1 </code><code class="ros value">vlan-filtering</code><code class="ros plain">=yes</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/interface ethernet switch</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">switch1 </code><code class="ros value">mirror-target</code><code class="ros plain">=ether3</code> <code class="ros value">mirror-source</code><code class="ros plain">=none</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros constants">/interface ethernet switch rule</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">mirror</code><code class="ros plain">=yes</code> <code class="ros value">ports</code><code class="ros plain">=ether1</code> <code class="ros value">switch</code><code class="ros plain">=switch1</code> <code class="ros value">vlan-id</code><code class="ros plain">=11</code></div></div></td></tr></tbody></table>

By enabling `vlan-filtering` you will be filtering out traffic destined to the CPU, before enabling VLAN filtering you should make sure that you set up a [Management port](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-Managementaccessconfiguration).

  

MAC Based Mirroring:

[?](https://help.mikrotik.com/docs/display/ROS/CRS3xx%2C+CRS5xx%2C+CCR2116%2C+CCR2216+switch+chip+features#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface ethernet switch</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">switch1 </code><code class="ros value">mirror-target</code><code class="ros plain">=ether3</code> <code class="ros value">mirror-source</code><code class="ros plain">=none</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/interface ethernet switch rule</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">mirror</code><code class="ros plain">=yes</code> <code class="ros value">ports</code><code class="ros plain">=ether1</code> <code class="ros value">switch</code><code class="ros plain">=switch1</code> <code class="ros value">dst-mac-address</code><code class="ros plain">=64:D1:54:D9:27:E6/FF:FF:FF:FF:FF:FF</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">mirror</code><code class="ros plain">=yes</code> <code class="ros value">ports</code><code class="ros plain">=ether1</code> <code class="ros value">switch</code><code class="ros plain">=switch1</code> <code class="ros value">src-mac-address</code><code class="ros plain">=64:D1:54:D9:27:E6/FF:FF:FF:FF:FF:FF</code></div></div></td></tr></tbody></table>

Protocol Based Mirroring:

[?](https://help.mikrotik.com/docs/display/ROS/CRS3xx%2C+CRS5xx%2C+CCR2116%2C+CCR2216+switch+chip+features#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface ethernet switch</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">switch1 </code><code class="ros value">mirror-target</code><code class="ros plain">=ether3</code> <code class="ros value">mirror-source</code><code class="ros plain">=none</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/interface ethernet switch rule</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">mirror</code><code class="ros plain">=yes</code> <code class="ros value">ports</code><code class="ros plain">=ether1</code> <code class="ros value">switch</code><code class="ros plain">=switch1</code> <code class="ros value">mac-protocol</code><code class="ros plain">=ipx</code></div></div></td></tr></tbody></table>

IP Based Mirroring:

[?](https://help.mikrotik.com/docs/display/ROS/CRS3xx%2C+CRS5xx%2C+CCR2116%2C+CCR2216+switch+chip+features#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface ethernet switch</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">switch1 </code><code class="ros value">mirror-target</code><code class="ros plain">=ether3</code> <code class="ros value">mirror-source</code><code class="ros plain">=none</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/interface ethernet switch rule</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">mirror</code><code class="ros plain">=yes</code> <code class="ros value">ports</code><code class="ros plain">=ether1</code> <code class="ros value">switch</code><code class="ros plain">=switch1</code> <code class="ros value">src-address</code><code class="ros plain">=192.168.88.0/24</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">mirror</code><code class="ros plain">=yes</code> <code class="ros value">ports</code><code class="ros plain">=ether1</code> <code class="ros value">switch</code><code class="ros plain">=switch1</code> <code class="ros value">dst-address</code><code class="ros plain">=192.168.88.0/24</code></div></div></td></tr></tbody></table>

There are other options as well, check the [ACL section](https://help.mikrotik.com/docs/display/ROS/CRS3xx%2C+CRS5xx%2C+CCR2116%2C+CCR2216+switch+chip+features#CRS3xx,CRS5xx,CCR2116,CCR2216switchchipfeatures-SwitchRules(ACL)) to find out all possible parameters that can be used to match packets.

# Traffic Shaping

___

It is possible to limit ingress traffic that matches certain parameters with ACL rules and it is possible to limit ingress/egress traffic per port basis. The policer is used for ingress traffic, the shaper is used for egress traffic. The ingress policer controls the received traffic with packet drops. Everything that exceeds the defined limit will get dropped. This can affect the TCP congestion control mechanism on end hosts and achieved bandwidth can be actually less than defined. The egress shaper tries to queue packets that exceed the limit instead of dropping them. Eventually, it will also drop packets when the output queue gets full, however, it should allow utilizing the defined throughput better.

Port-based traffic police and shaper:

[?](https://help.mikrotik.com/docs/display/ROS/CRS3xx%2C+CRS5xx%2C+CCR2116%2C+CCR2216+switch+chip+features#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface ethernet switch port</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">ether1 </code><code class="ros value">ingress-rate</code><code class="ros plain">=10M</code> <code class="ros value">egress-rate</code><code class="ros plain">=5M</code></div></div></td></tr></tbody></table>

MAC-based traffic policer:

[?](https://help.mikrotik.com/docs/display/ROS/CRS3xx%2C+CRS5xx%2C+CCR2116%2C+CCR2216+switch+chip+features#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface ethernet switch rule</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">ports</code><code class="ros plain">=ether1</code> <code class="ros value">switch</code><code class="ros plain">=switch1</code> <code class="ros value">src-mac-address</code><code class="ros plain">=64:D1:54:D9:27:E6/FF:FF:FF:FF:FF:FF</code> <code class="ros value">rate</code><code class="ros plain">=10M</code></div></div></td></tr></tbody></table>

VLAN-based traffic policer:

[?](https://help.mikrotik.com/docs/display/ROS/CRS3xx%2C+CRS5xx%2C+CCR2116%2C+CCR2216+switch+chip+features#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">bridge1 </code><code class="ros value">vlan-filtering</code><code class="ros plain">=yes</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/interface ethernet switch rule</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">ports</code><code class="ros plain">=ether1</code> <code class="ros value">switch</code><code class="ros plain">=switch1</code> <code class="ros value">vlan-id</code><code class="ros plain">=11</code> <code class="ros value">rate</code><code class="ros plain">=10M</code></div></div></td></tr></tbody></table>

By enabling `vlan-filtering` you will be filtering out traffic destined to the CPU, before enabling VLAN filtering you should make sure that you set up a [Management port](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-Managementaccessconfiguration).

Protocol-based traffic policer:

[?](https://help.mikrotik.com/docs/display/ROS/CRS3xx%2C+CRS5xx%2C+CCR2116%2C+CCR2216+switch+chip+features#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface ethernet switch rule</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">ports</code><code class="ros plain">=ether1</code> <code class="ros value">switch</code><code class="ros plain">=switch1</code> <code class="ros value">mac-protocol</code><code class="ros plain">=ipx</code> <code class="ros value">rate</code><code class="ros plain">=10M</code></div></div></td></tr></tbody></table>

There are other options as well, check the [ACL section](https://help.mikrotik.com/docs/display/ROS/CRS3xx%2C+CRS5xx%2C+CCR2116%2C+CCR2216+switch+chip+features#CRS3xx,CRS5xx,CCR2116,CCR2216switchchipfeatures-SwitchRules(ACL)) to find out all possible parameters that can be used to match packets.

The Switch Rule table is used for QoS functionality, see [this table](https://help.mikrotik.com/docs/display/ROS/CRS3xx%2C+CRS5xx%2C+CCR2116%2C+CCR2216+switch+chip+features#CRS3xx,CRS5xx,CCR2116,CCR2216switchchipfeatures-Models) on how many rules each device supports.

# Traffic Storm Control

___

Since RouterOS v6.42 it is possible to enable traffic storm control. A traffic storm can emerge when certain frames are continuously flooded on the network. For example, if a network loop has been created and no loop avoidance mechanisms are used (e.g. [Spanning Tree Protocol](https://help.mikrotik.com/docs/display/ROS/Spanning+Tree+Protocol)), broadcast or multicast frames can quickly overwhelm the network, causing degraded network performance or even complete network breakdown. With CRS3xx, CRS5xx series switches and CCR2116, CCR2216 routers it is possible to limit broadcast, unknown multicast and unknown unicast traffic. Unknown unicast traffic is considered when a switch does not contain a host entry for the destined MAC address. Unknown multicast traffic is considered when a switch does not contain a multicast group entry in the `/interface bridge mdb` menu. Storm control settings should be applied to ingress ports, the egress traffic will be limited.

The storm control parameter is specified in percentage (%) of the link speed. If your link speed is 1Gbps, then specifying `storm-rate` as `10` will allow only 100Mbps of broadcast, unknown multicast and/or unknown unicast traffic to be forwarded.

**Sub-menu:** `/interface ethernet switch port`

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

 |                                                     |
 | --------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
 | **limit-broadcasts** (_yes                          | no_; Default: **yes**)                                                                                               | Limit broadcast traffic on a switch port.         |
 | **limit-unknown-multicasts** (_yes                  | no_; Default: **no**)                                                                                                | Limit unknown multicast traffic on a switch port. |
 | **limit-unknown-unicasts** (_yes                    | no_; Default: **no**)                                                                                                | Limit unknown unicast traffic on a switch port.   |
 | **storm-rate** (_integer 0..100_; Default: **100**) | Amount of broadcast, unknown multicast and/or unknown unicast traffic is limited to in percentage of the link speed. |

Devices with Marvell-98DX3236 switch chip cannot distinguish unknown multicast traffic from all multicast traffic. For example, CRS326-24G-2S+ will limit all multicast traffic when `limit-unknown-multicasts` and `storm-rate` is used. For other devices, for example, CRS317-1G-16S+ the `limit-unknown-multicasts` parameter will limit only unknown multicast traffic (addresses that are not present in `/interface bridge mdb).`

For example, to limit 1% (10Mbps) of broadcast and unknown unicast traffic on ether1 (1Gbps), use the following commands:

[?](https://help.mikrotik.com/docs/display/ROS/CRS3xx%2C+CRS5xx%2C+CCR2116%2C+CCR2216+switch+chip+features#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface ethernet switch port</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">ether1 </code><code class="ros value">storm-rate</code><code class="ros plain">=1</code> <code class="ros value">limit-broadcasts</code><code class="ros plain">=yes</code> <code class="ros value">limit-unknown-unicasts</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

# MPLS hardware offloading

___

Since RouterOS v6.41 it is possible to offload certain MPLS functions to the switch chip, the switch must be a (P)rovider router in a PE-P-PE setup in order to achieve hardware offloading. A setup example can be found in the [Basic MPLS setup example](https://wiki.mikrotik.com/wiki/Manual:Basic_MPLS_setup_example "Manual:Basic MPLS setup example") manual page. The hardware offloading will only take place when LDP interfaces are configured as physical switch interfaces (e.g. Ethernet, SFP, SFP+).

Currently only `CRS317-1G-16S+` and `CRS309-1G-8S+` using RouterOS v6.41 and newer are capable of hardware offloading certain MPLS functions. `CRS317-1G-16S+` and `CRS309-1G-8S+` built-in switch chip is not capable of popping MPLS labels from packets, in a PE-P-PE setup you either have to use explicit null or disable TTL propagation in MPLS network to achieve hardware offloading.

The MPLS hardware offloading has been removed since RouterOS v7.

  

# Switch Rules (ACL)

___

Access Control List contains ingress policy and egress policy engines. See [this table](https://help.mikrotik.com/docs/display/ROS/CRS3xx%2C+CRS5xx%2C+CCR2116%2C+CCR2216+switch+chip+features#CRS3xx,CRS5xx,CCR2116,CCR2216switchchipfeatures-Models) on how many rules each device supports. It is an advanced tool for wire-speed packet filtering, forwarding and modifying based on Layer2, Layer3 and Layer4 protocol header field conditions.

ACL rules are checked for each received packet until a match has been found. If there are multiple rules that can match, then only the first rule will be triggered. A rule without any action parameters is a rule to accept the packet.

When switch ACL rules are modified (e.g. added, removed, disabled, enabled, or moved), the existing switch rules will be inactive for a short time. This can cause some packet leakage during the ACL rule modifications.

  

**Sub-menu:** `/interface ethernet switch rule`

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

 |                                          |
 | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
 | **copy-to-cpu** (_no                     | yes_; Default: **no**)                                                                                                                                                                                                                      | Clones the matching packet and sends it to the CPU.                                             |
 | **disabled** (_yes                       | no_; Default: **no**)                                                                                                                                                                                                                       | Enables or disables ACL entry.                                                                  |
 | **dscp** (_0..63_)                       | Matching DSCP field of the packet.                                                                                                                                                                                                          |
 | **dst-address** (_IP address/Mask_)      | Matching destination IP address and mask, also matches destination IP in ARP packets.                                                                                                                                                       |
 | **dst-address6** (_IPv6 address/Mask_)   | Matching destination IPv6 address and mask, also matches source IP in ARP packets.                                                                                                                                                          |
 | **dst-mac-address** (_MAC address/Mask_) | Matching destination MAC address and mask.                                                                                                                                                                                                  |
 | **dst-port** (_0..65535_)                | Matching destination protocol port number.                                                                                                                                                                                                  |
 | **flow-label** (_0..1048575_)            | Matching IPv6 flow label.                                                                                                                                                                                                                   |
 | **mac-protocol** (_802.2                 | arp                                                                                                                                                                                                                                         | homeplug-av                                                                                     | ip    | ipv6    | ipx | lldp | loop-protect | mpls-multicast | mpls-unicast | packing-compr | packing-simple | pppoe   | pppoe-discovery | rarp     | service-vlan | vlan | or 0..65535 | or 0x0000-0xffff_) | Matching particular MAC protocol specified by protocol name or number |
 | **mirror** (_no                          | yes_)                                                                                                                                                                                                                                       | Clones the matching packet and sends it to the mirror-target port.                              |
 | **new-dst-ports** (_ports_)              | Changes the destination port as specified. An empty setting will drop the packet. A specified port will redirect the packet to it. When the parameter is not used, the packet will be accepted. Multiple "new-dst-ports" are not supported. |
 | **new-vlan-id** (_0..4095_)              | Changes the VLAN ID to the specified value. Requires `vlan-filtering=yes`.                                                                                                                                                                  |
 | **new-vlan-priority** (_0..7_)           | Changes the VLAN priority (priority code point). Requires `vlan-filtering=yes`.                                                                                                                                                             |
 | **ports** (_ports_)                      | Matching ports on which will the rule apply on received traffic.                                                                                                                                                                            |
 | **protocol** (_dccp                      | ddp                                                                                                                                                                                                                                         | egp                                                                                             | encap | etherip | ggp | gre  | hmp          | icmp           | icmpv6       | idpr-cmtp     | igmp           | ipencap | ipip            | ipsec-ah | ipsec-esp    | ipv6 | ipv6-frag   | ipv6-nonxt         | ipv6-opts                                                             | ipv6-route | iso-tp4 | l2tp | ospf | pim | pup | rdp | rspf | rsvp | sctp | st | tcp | udp | udp-lite | vmtp | vrrp | xns-idp | xtp | or 0..255_) | Matching particular IP protocol specified by protocol name or number. |
 | **rate** (_0..4294967295_)               | Sets ingress traffic limitation (bits per second) for matched traffic.                                                                                                                                                                      |
 | **redirect-to-cpu** (_no                 | yes_)                                                                                                                                                                                                                                       | Changes the destination port of a matching packet to the CPU.                                   |
 | **src-address** (_IP address/Mask_)      | Matching source IP address and mask.                                                                                                                                                                                                        |
 | **src-address6** (_IPv6 address/Mask_)   | Matching source IPv6 address and mask.                                                                                                                                                                                                      |
 | **src-mac-address** (_MAC address/Mask_) | Matching source MAC address and mask.                                                                                                                                                                                                       |
 | **src-port** (_0..65535_)                | Matching source protocol port number.                                                                                                                                                                                                       |
 | **switch** (_switch group_)              | Matching switch group on which will the rule apply.                                                                                                                                                                                         |
 | **traffic-class** (_0..255_)             | Matching IPv6 traffic class.                                                                                                                                                                                                                |
 | **vlan-id** (_0..4095_)                  | Matching VLAN ID. Requires `vlan-filtering=yes`.                                                                                                                                                                                            |
 | **vlan-header** (_not-present            | present_)                                                                                                                                                                                                                                   | Matching VLAN header, whether the VLAN header is present or not. Requires `vlan-filtering=yes`. |
 | **vlan-priority** (_0..7_)               | Matching VLAN priority (priority code point).                                                                                                                                                                                               |

Action parameters:

-   copy-to-cpu
-   redirect-to-cpu
-   mirror
-   new-dst-ports (can be used to drop packets)
-   new-vlan-id
-   new-vlan-priority
-   rate

Layer2 condition parameters:

-   dst-mac-address
-   mac-protocol
-   src-mac-address
-   vlan-id
-   vlan-header
-   vlan-priority

Layer3 condition parameters:

-   dscp
-   protocol
-   IPv4 conditions:
    -   dst-address
    -   src-address
-   IPv6 conditions:
    -   dst-address6
    -   flow-label
    -   src-address6
    -   traffic-class

Layer4 condition parameters:

-   dst-port
-   src-port

  

For VLAN related matchers or VLAN related action parameters to work, you need to enable `vlan-filtering` on the bridge interface and make sure that hardware offloading is enabled on those ports, otherwise, these parameters will not have any effect.

When bridge interface `ether-type` is set to `0x8100`, then VLAN related ACL rules are relevant to 0x8100 (CVID) packets, this includes `vlan-id` and `new-vlan-id`. When bridge interface `ether-type` is set to `0x88a8`, then ACL rules are relevant to 0x88A8 (SVID) packets.

# Port Security

___

It is possible to limit allowed MAC addresses on a single switch port. For example, to allow 64:D1:54:81:EF:8E MAC address on a switch port, start by switching multiple ports together, in this example 64:D1:54:81:EF:8E is going to be located behind **ether1**. 

Create an ACL rule to allow the given MAC address and drop all other traffic on **ether1** (for ingress traffic):

[?](https://help.mikrotik.com/docs/display/ROS/CRS3xx%2C+CRS5xx%2C+CCR2116%2C+CCR2216+switch+chip+features#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface ethernet switch rule</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">ports</code><code class="ros plain">=ether1</code> <code class="ros value">src-mac-address</code><code class="ros plain">=64:D1:54:81:EF:8E/FF:FF:FF:FF:FF:FF</code> <code class="ros value">switch</code><code class="ros plain">=switch1</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">new-dst-ports</code><code class="ros plain">=</code><code class="ros string">""</code> <code class="ros value">ports</code><code class="ros plain">=ether1</code> <code class="ros value">switch</code><code class="ros plain">=switch1</code></div></div></td></tr></tbody></table>

Switch all required ports together, disable MAC learning and disable unknown unicast flooding on **ether1**:

[?](https://help.mikrotik.com/docs/display/ROS/CRS3xx%2C+CRS5xx%2C+CCR2116%2C+CCR2216+switch+chip+features#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=bridge1</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge port</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether1</code> <code class="ros value">hw</code><code class="ros plain">=yes</code> <code class="ros value">learn</code><code class="ros plain">=no</code> <code class="ros value">unknown-unicast-flood</code><code class="ros plain">=no</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether2</code> <code class="ros value">hw</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

Add a static hosts entry for 64:D1:54:81:EF:8E (for egress traffic):

[?](https://help.mikrotik.com/docs/display/ROS/CRS3xx%2C+CRS5xx%2C+CCR2116%2C+CCR2216+switch+chip+features#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge host</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether1</code> <code class="ros value">mac-address</code><code class="ros plain">=64:D1:54:81:EF:8E</code></div></div></td></tr></tbody></table>

Broadcast traffic will still be sent out from **ether1**. To limit broadcast traffic flood on a bridge port, you can use the `broadcast-flood` parameter to toggle it. Do note that some protocols depend on broadcast traffic, such as streaming protocols and DHCP.

# Dual Boot

___

The “dual boot” feature allows you to choose which operating system you prefer to use on CRS3xx series switches, RouterOS or SwOS. Device operating system could be changed using:

-   Command-line (`/system routerboard settings set boot-os=swos`)
-   Winbox
-   Webfig
-   Serial Console

More details about SwOS are described here: [SwOS manual](https://help.mikrotik.com/docs/display/SWOS/SwOS)

# Configuring SwOS using RouterOS

___

Since RouterOS 6.43 it is possible to load, save and reset SwOS configuration, as well as upgrade SwOS and set an IP address for the CRS3xx series switches by using RouterOS.

-   Save configuration with `/system swos save-config`

The configuration will be saved on the same device with `swos.config` as a filename, make sure you download the file from your device since the configuration file will be removed after a reboot.

-   Load configuration with `/system swos load-config`
-   Change password with `/system swos password`
-   Reset configuration with `/system swos reset-config`
-   Upgrade SwOS from RouterOS using `/system swos upgrade`

The upgrade command will automatically install the latest available SwOS primary backup version, make sure that your device has access to the Internet in order for the upgrade process to work properly. When the device is booted into SwOS, the version number will include the letter "p", indicating a primary backup version. You can then install the latest available SwOS secondary main version from the SwOS "Upgrade" menu.

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

 |                                          |
 | ---------------------------------------- | ------------------ |
 | **address-acquisition-mode** (_dhcp-only | dhcp-with-fallback | static_; Default: **dhcp-with-fallback**) | Changes address acquisition method: |

dhcp-only \- uses only a DHCP client to acquire address

dhcp-with-fallback \- for the first 10 seconds will try to acquire address using a DHCP client. If the request is unsuccessful, then address falls back to static as defined by static-ip-address property

static \- address is set as defined by static-ip-address property

 |
| **allow-from** (_IP/Mask_; Default: **0.0.0.0/0**) | IP address or a network from which the switch is accessible. By default, the switch is accessible by any IP address. |
| **allow-from-ports** (_name_; Default: ) | List of switch ports from which the device is accessible. By default, all ports are allowed to access the switch |
| **allow-from-vlan** (_integer: 0..4094_; Default: **0**) | VLAN ID from which the device is accessible. By default, all VLANs are allowed |
| **identity** (_name_; Default: **Mikrotik**) | Name of the switch (used for Mikrotik Neighbor Discovery protocol) |
| **static-ip-address** (_IP_; Default: **192.168.88.1**) | IP address of the switch in case address-acquisition-mode is either set to dhcp-with-fallback or static. By setting a static IP address, the address acquisition process does not change, which is DHCP with fallback by default. This means that the configured static IP address will become active only when there is going to be no DHCP servers in the same broadcast domain |

# See also

[CRS Router](https://wiki.mikrotik.com/wiki/Manual:CRS_Router "Manual:CRS Router")

[CRS3xx VLANs with Bonds](https://wiki.mikrotik.com/wiki/Manual:CRS3xx_VLANs_with_Bonds "Manual:CRS3xx VLANs with Bonds")

[Basic VLAN switching](https://help.mikrotik.com/docs/display/ROS/Basic+VLAN+switching)

[Bridge Hardware Offloading](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-BridgeHardwareOffloading)

[Route Hardware Offloading](https://help.mikrotik.com/docs/display/ROS/L3+Hardware+Offloading)

[Spanning Tree Protocol](https://help.mikrotik.com/docs/display/ROS/Spanning+Tree+Protocol)

[MTU on RouterBOARD](https://help.mikrotik.com/docs/display/ROS/MTU+in+RouterOS)

[Layer2 misconfiguration](https://help.mikrotik.com/docs/display/ROS/Layer2+misconfiguration)

[Bridge VLAN Table](https://help.mikrotik.com/docs/display/ROS/Bridge+VLAN+Table)

[Bridge IGMP/MLD snooping](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=59277403)

[Multi-chassis Link Aggregation Group](https://help.mikrotik.com/docs/display/ROS/Multi-chassis+Link+Aggregation+Group)