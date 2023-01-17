# Introduction

___

Virtual eXtensible Local Area Network (VXLAN) is a tunneling protocol designed to solve the problem of limited VLAN IDs (4096) in IEEE 802.1Q, and it is described by IETF RFC 7348. With VXLAN the size of the identifier is expanded to 24 bits (16777216). It creates a Layer 2 overlay scheme on a Layer 3 network and the protocol runs over UDP. RouterOS VXLAN interface supports IPv4 or IPv6 (since version 7.6), but dual-stack is not supported.

VXLAN creates a 50-byte overhead for IPv4 and a 70-byte overhead for IPv6. When configuring VXLAN, it is recommended to ensure that the size of the encapsulated Ethernet frame does not exceed the MTU of the underlying network, by configuring the MTU accordingly or by limiting the size of the Ethernet frames.

Only devices within the same VXLAN segment can communicate with each other.  Each VXLAN segment is identified through a 24-bit segment ID, termed the VXLAN Network Identifier (VNI). Unlike most tunnels, a VXLAN is a 1 to N network, not just point to point. A VXLAN device can learn the IP address of the other endpoint dynamically in a manner similar to a learning bridge. Multicast or unicast is used to flood broadcast, unknown unicast, and multicast traffic. VXLAN endpoints, which terminate VXLAN tunnels are known as VXLAN tunnel endpoints (VTEPs). 

# Configuration options

___

This section describes the VXLAN interface and VTEP configuration options.

**Sub-menu:** `/interface vxlan`

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



 |                    |
 | ------------------ | ------- |
 | **arp** (_disabled | enabled | local-proxy-arp | proxy-arp | reply-only_; Default: **enabled**) | Address Resolution Protocol setting |

-   `disabled` \- the interface will not use ARP
-   `enabled` \- the interface will use ARP
-   `local-proxy-arp` \-  the router performs proxy ARP on the interface and sends replies to the same interface
-   `proxy-arp` \- the router performs proxy ARP on the interface and sends replies to other interfaces
-   `reply-only` \- the interface will only reply to requests originating from matching IP address/MAC address combinations which are entered as static entries in the IP/ARP table. No dynamic entries will be automatically stored in the IP/ARP table. Therefore for communications to be successful, a valid static entry must already exist.

 |
| **arp-timeout** (_auto | integer_; Default: **auto**) | How long the ARP record is kept in the ARP table after no packets are received from IP. Value `auto` equals to the value of `arp-timeout` in IP/Settings, default is the 30s. |
| **comment** (_string_; Default: ) | Short description of the interface. |
| **disabled** (_yes | no_; Default: **no**) | Changes whether the interface is disabled. |
| **dont-fragment** (_disabled | enabled | inherit_; Default: **disabled**) | 

The Don't Fragment (DF) flag controls whether a packet can be broken into smaller packets, called fragments, before being sent over a network. When configuring VXLAN, this setting determines the presence of the DF flag on the outer IPv4 header and can control packet fragmentation if the encapsulated packet exceeds the outgoing interface MTU. This setting has three options:

-   `disabled` \- the DF flag is not set on the outer IPv4 header, which means that packets can be fragmented if they are too large to be sent over the outgoing interface. This also allows packet fragmentation when VXLAN uses IPv6 underlay.
-   `enabled` \- the DF flag is always set on the outer IPv4 header, which means that packets will not be fragmented and will be dropped if they exceed the outgoing interface's MTU. This also avoids packet fragmentation when VXLAN uses IPv6 underlay.
-   `inherit` \- The DF flag on the outer IPv4 header is based on the inner IPv4 DF flag. If the inner IPv4 header has the DF flag set, the outer IPv4 header will also have it set. If the packet exceeds the outgoing interface's MTU and DF is set, it will be dropped. If the inner packet is non-IP, the outer IPv4 header will not have the DF flag set and packets can be fragmented. If the inner packet is IPv6, the outer IPv4 header will always set the DF flag and packets cannot be fragmented. Note that when VXLAN uses IPv6 underlay, this setting does not have any effect and is treated the same as `disabled`.

The setting is available since RouterOS version 7.8.

 |
| **group** (_IPv4 | IPv6_; Default: ) | When specified, a multicast group address can be used to forward broadcast, unknown unicast, and multicast traffic between VTEPs. This property requires specifying the `interface` setting. The interface will use IGMP or MLD to join the specified multicast group, make sure to add the necessary PIM and IGMP/MDL configuration. When this property is set, the `vteps-ip-version` automatically gets updated to the used multicast IP version. |
| **interface** (_name_; Default: ) | Interface name used for multicast forwarding. This property requires specifying the `group` setting. |
| **local-address** (_IPv4 | IPv6_; Default: ) | Specifies the local source address for the VXLAN interface. If not set, one IP address of the egress interface will be selected as a source address for VXLAN packets. When the property is set, the `vteps-ip-version` automatically gets updated to the used local IP version. The setting is available since RouterOS version 7.7. |
| **mac-address** (_read-only,_ Default: ) | 

Automatically assigned interface MAC address. This setting cannot be changed.

 |
| **mtu** (_integer_; Default: **1500**) | 

For the maximum transmission unit, the VXLAN interface will set MTU to 1500 by default. The `l2mtu` will be set automatically according to the associated `interface` (subtracting 50 bytes corresponding to the VXLAN header). If no interface is specified, the `l2mtu` value of 65535 is used. The `l2mtu` cannot be changed.

 |
| **name** (_text_; Default: **vxlan1**) | Name of the interface. |
| **port** (_integer: 1_..65535__; Default: **8472**) | 

Used UDP port number.

 |
| **vni** (_integer: 1..16777216_; Default: ) | 

VXLAN Network Identifier (VNI).

 |
| 

**vrf** (_name_; Default: **main**)

 | Set VRF for the VXLAN interface on which the VTEPs listen and make connections. VRF is not supported when using `interface` and multicast `group` settings. The setting is available since RouterOS version 7.7. |
| **vteps-ip-version** (_ipv4 | ipv6_; Default: **ipv4**) | 

Used IP protocol version for statically configured VTEPs. RouterOS VXLAN interface does not support dual-stack, any configured remote VTEPs with the opposite IP version will be ignored. When multicast `group` or `local-address` properties are set, the `vteps-ip-version` automatically gets updated to the used IP version. The setting is available since RouterOS version 7.6.

 |

  

**Sub-menu:** `/interface vxlan vteps`

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
 | --------------------------------------------------- | ---------------------------- |
 | **interface** (_name_; Default: )                   | Name of the VXLAN interface. |
 | **port** (_integer: 1_..65535__; Default: **8472**) |

Used UDP port number.

 |
| **remote-ip** (_IPv4 | IPv6_; Default: ) | 

The IPv4 or IPv6 destination address of remote VTEP.

 |

# Configuration example

___

This configuration example creates a single VXLAN tunnel between two statically configured VTEP endpoints.

First, create VXLAN interfaces on both routers.

[?](https://help.mikrotik.com/docs/display/ROS/VXLAN#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface vxlan</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=vxlan1</code> <code class="ros value">port</code><code class="ros plain">=8472</code> <code class="ros value">vni</code><code class="ros plain">=10</code></div></div></td></tr></tbody></table>

Then configure VTEPs on both routers with respective IPv4 destination addresses. Both devices should have an active route toward the destination address.

[?](https://help.mikrotik.com/docs/display/ROS/VXLAN#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros comments"># Router1</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros constants">/interface vxlan vteps</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=vxlan1</code> <code class="ros value">remote-ip</code><code class="ros plain">=192.168.10.10</code></div><div class="line number4 index3 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros comments"># Router2</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros constants">/interface vxlan vteps</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=vxlan1</code> <code class="ros value">remote-ip</code><code class="ros plain">=192.168.20.20</code></div></div></td></tr></tbody></table>

Configuration is complete. It is possible to include the VXLAN interface into a bridge with other Ethernet interfaces.