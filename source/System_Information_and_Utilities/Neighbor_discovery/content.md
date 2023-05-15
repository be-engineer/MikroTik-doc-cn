# Summary

Neighbor Discovery protocols allow us to find devices compatible with MNDP (MikroTik Neighbor Discovery Protocol), CDP (Cisco Discovery Protocol), or LLDP (Link Layer Discovery Protocol) in the Layer2 broadcast domain. It can be used to map out your network.

# Neighbor list

The neighbor list shows all discovered neighbors in the Layer2 broadcast domain. It shows to which interface neighbor is connected, its IP/MAC addresses, and other related parameters. The list is read-only, an example of a neighbor list is provided below:

[?](https://help.mikrotik.com/docs/display/ROS/Neighbor+discovery#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] </code><code class="ros constants">/ip neighbor </code><code class="ros functions">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros comments"># INTERFACE ADDRESS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; MAC-ADDRESS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; IDENTITY&nbsp;&nbsp; VERSION&nbsp;&nbsp;&nbsp; BOARD&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">0 ether13&nbsp;&nbsp; 192.168.33.2&nbsp;&nbsp;&nbsp; 00</code><code class="ros constants">:0C:42:00:38:9F MikroTik&nbsp;&nbsp; 5.99&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; RB1100AHx2</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">1 ether11&nbsp;&nbsp; 1.1.1.4&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 00</code><code class="ros constants">:0C:42:40:94:25 test-host&nbsp; 5.8&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; RB1000&nbsp;&nbsp;</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">2 Local&nbsp;&nbsp;&nbsp;&nbsp; 10.0.11.203&nbsp;&nbsp;&nbsp;&nbsp; 00</code><code class="ros constants">:02:B9:3E:AD:E0 c2611-r1&nbsp;&nbsp; Cisco I...&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">3 Local&nbsp;&nbsp;&nbsp;&nbsp; 10.0.11.47&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 00</code><code class="ros constants">:0C:42:84:25:BA 11.47-750&nbsp; 5.7&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; RB750&nbsp;</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">4 Local&nbsp;&nbsp;&nbsp;&nbsp; 10.0.11.254&nbsp;&nbsp;&nbsp;&nbsp; 00</code><code class="ros constants">:0C:42:70:04:83 tsys-sw1&nbsp;&nbsp; 5.8&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; RB750G&nbsp;&nbsp;&nbsp;</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">5 Local&nbsp;&nbsp;&nbsp;&nbsp; 10.0.11.202&nbsp;&nbsp;&nbsp;&nbsp; 00</code><code class="ros constants">:17:5A:90:66:08 c7200&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Cisco I...</code></div></div></td></tr></tbody></table>

**Sub-menu:** `/ip neighbor`

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

|                                    |
| ---------------------------------- | ------------------------------------------------------------------------------------------- |
| **address** (_IP_)                 | The highest IP address configured on a discovered device                                    |
| **address6** (_IPv6_)              | IPv6 address configured on a discovered device                                              |
| **age** (_time_)                   | Time interval since last discovery packet                                                   |
| **discovered-by** (_cdp            | lldp                                                                                        | mndp_)                                     | Shows the list of protocols the neighbor has been discovered by. The property is available since RouterOS version 7.7. |
| **board** (_string_)               | RouterBoard model. Displayed only to devices with installed RouterOS                        |
| **identity** (_string_)            | Configured system identity                                                                  |
| **interface** (_string_)           | Interface name to which discovered device is connected                                      |
| **interface-name** (_string_)      | Interface name on the neighbor device connected to the L2 broadcast domain. Applies to CDP. |
| **ipv6** (_yes                     | no_)                                                                                        | Shows whether the device has IPv6 enabled. |
| **mac-address** (_MAC_)            | Mac address of the remote device. Can be used to connect with mac-telnet.                   |
| **platform** (_string_)            | Name of the platform. For example "MikroTik", "cisco", etc.                                 |
| **software-id** (_string_)         | RouterOS software ID on a remote device. Applies only to devices installed with RouterOS.   |
| **system-caps** (_string_)         | System capabilities reported by the Link-Layer Discovery Protocol (LLDP).                   |
| **system-caps-enabled** (_string_) | Enabled system capabilities reported by the Link-Layer Discovery Protocol (LLDP).           |
| **unpack** (_none                  | simple                                                                                      | uncompressed-headers                       | uncompressed-all_)                                                                                                     | Shows the discovery packet compression type. |
| **uptime** (_time_)                | Uptime of remote device. Shown only to devices installed with RouterOS.                     |
| **version** (_string_)             | Version number of installed software on a remote device                                     |

Starting from RouterOS v6.45, the number of neighbor entries are limited to (total RAM in megabytes)\*16 per interface to avoid memory exhaustion.

# Discovery configuration

It is possible to change whether an interface participates in neighbor discovery or not using an Interface list. If the interface is included in the discovery interface list, it will send out basic information about the system and process received discovery packets broadcasted in the Layer2 network. Removing an interface from the interface list will disable both the discovery of neighbors on this interface and also the possibility of discovering this device itself on that interface.

[?](https://help.mikrotik.com/docs/display/ROS/Neighbor+discovery#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip neighbor&nbsp;discovery-settings</code></div></div></td></tr></tbody></table>

  

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

|                                                                         |
| ----------------------------------------------------------------------- | ------------------------------------------------------------------ |
| **discover-interface-list** (_string_; Default: **static**)             | Interface list on which members the discovery protocol will run on |
| **lldp-med-net-policy-vlan** (_integer 0..4094_; Default: **disabled**) |

Advertised VLAN ID for LLDP-MED Network Policy TLV. This allows assigning a VLAN ID for LLDP-MED capable devices, such as VoIP phones. The TLV will only be added to interfaces where LLDP-MED capable devices are discovered. Other TLV values are predefined and cannot be changed:

-   Application Type - Voice
-   VLAN Type - Tagged
-   L2 Priority - 0
-   DSCP Priority - 0

When used together with the bridge interface, the (R/M)STP protocol should be enabled with `protocol-mode` setting. 

Additionally, other neighbor discovery protocols (e.g. CDP) should be excluded using `protocol` setting to avoid LLDP-MED misconfiguration.

 |
| **mode** (_rx-only | tx-only | tx-and-rx_; Default: **tx-and-rx**) | 

Selects the neighbor discovery packet sending and receiving mode. The setting is available since RouterOS version 7.7.

 |
| **protocol** (_cdp | lldp | mndp_; Default: **cdp,lldp,mndp**) | List of used discovery protocols |

Since RouterOS v6.44, neighbor discovery is working on individual slave interfaces. Whenever a master interface (e.g. bonding or bridge) is included in the discovery interface list, all its slave interfaces will automatically participate in neighbor discovery. It is possible to allow neighbor discovery only to some slave interfaces. To do that, include the particular slave interface in the list and make sure that the master interface is not included.

[?](https://help.mikrotik.com/docs/display/ROS/Neighbor+discovery#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bonding</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=bond1</code> <code class="ros value">slaves</code><code class="ros plain">=ether5,ether6</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/interface list</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=only-ether5</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros constants">/interface list member</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=ether5</code> <code class="ros value">list</code><code class="ros plain">=only-ether5</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros constants">/ip neighbor discovery-settings</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros value">discover-interface-list</code><code class="ros plain">=only-ether5</code></div></div></td></tr></tbody></table>

Now the neighbor list shows a master interface and actual slave interface on which a discovery message was received.

[?](https://help.mikrotik.com/docs/display/ROS/Neighbor+discovery#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@R2] &gt; ip neighbor print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros comments"># INTERFACE ADDRESS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; MAC-ADDRESS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; IDENTITY&nbsp;&nbsp; VERSION&nbsp;&nbsp;&nbsp; BOARD&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">0 ether5&nbsp;&nbsp;&nbsp; 192.168.88.1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; CC</code><code class="ros constants">:2D:E0:11:22:33 R1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 6.45.4 ... CCR1036-8G-2S+</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros plain">bond1</code></div></div></td></tr></tbody></table>

# LLDP

Depending on RouterOS configuration, different type-length-value (TLV) can be sent in the LLDP message, this includes:

-   Chassis subtype (MAC address)
-   Port subtype (interface name)
-   Time To Live
-   System name (system identity)
-   System description (platform - MikroTik, software version - RouterOS version,  hardware name - RouterBoard name)
-   Management address (all IP addresses configured on the port)
-   System capabilities (enabled system capabilities, e.g. bridge or router)
-   LLDP-MED Media Capabilities (list of MED capabilities)
-   LLDP-MED Network Policy (assigned VLAN ID for voice traffic)
-   Port Extension (Port Extender and Controller Bridge advertisement)
-   End of LLDPDU