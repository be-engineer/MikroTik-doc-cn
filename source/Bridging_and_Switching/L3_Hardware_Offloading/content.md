＃ 介绍

**第 3 层硬件卸载**（**L3HW**，也称为 IP 交换或硬件路由）允许将某些路由器功能卸载到交换芯片上。 允许路由数据包时达到线速，这对于 CPU 来说是不可能的。

# 交换配置

要启用第 3 层硬件卸载，请为交换机设置 **l3-hw-offloading=yes**：

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface/ethernet/switch </code><code class="ros functions">set </code><code class="ros plain">0 </code><code class="ros value">l3-hw-offloading</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

## Switch Port Configuration

Layer 3 Hardware Offloading can be configured for each physical switch port. For example:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface/ethernet/switch/port </code><code class="ros functions">set </code><code class="ros plain">sfp-sfpplus1 </code><code class="ros value">l3-hw-offloading</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

Note that l3hw settings for switch and ports are different:

-   Setting `l3-hw-offloading``=no` for the switch completely disables offloading - all packets will be routed by CPU.
-   However, setting `l3-hw-offloading``=no` for a switch port only disables hardware routing from/to this particular port. Moreover, the port can still participate in Fastrack connection offloading. 

To enable full hardware routing, enable l3hw on all switch ports:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface/ethernet/switch </code><code class="ros functions">set </code><code class="ros plain">0 </code><code class="ros value">l3-hw-offloading</code><code class="ros plain">=yes</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros constants">/interface/ethernet/switch/port </code><code class="ros functions">set </code><code class="ros plain">[find] </code><code class="ros value">l3-hw-offloading</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

To make all packets go through the CPU first, and offload only the Fasttrack connections, disable l3hw on all ports but keep it enabled on the switch chip itself:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface/ethernet/switch </code><code class="ros functions">set </code><code class="ros plain">0 </code><code class="ros value">l3-hw-offloading</code><code class="ros plain">=yes</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros constants">/interface/ethernet/switch/port </code><code class="ros functions">set </code><code class="ros plain">[find] </code><code class="ros value">l3-hw-offloading</code><code class="ros plain">=no</code></div></div></td></tr></tbody></table>

**Packets get routed by the hardware only if both source and destination ports have `l3-hw-offloading=yes`.** If at least one of them has `l3-hw-offloading=no`, packets will go through the CPU/Firewall while offloading only the Fasttrack connections.

The next example enables hardware routing on all ports but the upstream port (sfp-sfpplus16). Packets going to/from sfp-sfpplus16 will enter the CPU and, therefore, subject to Firewall/NAT processing.

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface/ethernet/switch </code><code class="ros functions">set </code><code class="ros plain">0 </code><code class="ros value">l3-hw-offloading</code><code class="ros plain">=yes</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros constants">/interface/ethernet/switch/port </code><code class="ros functions">set </code><code class="ros plain">[find] </code><code class="ros value">l3-hw-offloading</code><code class="ros plain">=yes</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/interface/ethernet/switch/port </code><code class="ros functions">set </code><code class="ros plain">sfp-sfpplus16 </code><code class="ros value">l3-hw-offloading</code><code class="ros plain">=no</code></div></div></td></tr></tbody></table>

The existing connections may be unaffected by the `l3-hw-offloading` setting change.

## L3HW Settings

The L3HW Settings menu has been introduced in RouterOS version 7.6.

**Sub-menu:** `/interface ethernet switch l3hw-settings`

| 
Property



 | 

Description



 |     |
 | --- ||
 |     |

Property



 | 

Description



 |                               |
 | ----------------------------- | ------------------------------------- |
 | **fasttrack-hw** (_yes        | no_; Default: **yes** (if supported)) | Enables or disables FastTrack HW Offloading. Keep it enabled unless HW TCAM memory reservation is required, e.g., for dynamic switch ACL rules creation. Not all switch chips support FastTrack HW Offloading (see **hw-supports-fasttrack**).                                                                                                                                                                     |
 | **ipv6-hw** (_yes             | no_; Default: **no**)                 | Enables or disables IPv6 Hardware Offloading. Since IPv6 routes occupy a lot of HW memory, enable it only if IPv6 traffic speed is significant enough to benefit from hardware routing.                                                                                                                                                                                                                            |
 | **icmp-reply-on-error** (_yes | no_; Default: **yes**)                | Since the hardware cannot send ICMP messages, the packet must be redirected to the CPU to send an ICMP reply in case of an error (e.g., "Time Exceeded", "Fragmentation required", etc.). Enabling icmp-reply-on-error helps with network diagnostics but may open potential vulnerabilities for DDoS attacks. Disabling icmp-reply-on-error silently drops the packets on the hardware level in case of an error. |

**Read-Only Properties**

| 
Property



 | 

Description



 |     |
 | --- ||
 |     |

Property



 | 

Description



 |                                  |
 | -------------------------------- | ----- |
 | **hw-supports-fasttrack** (__yes | no__) | Indicates if the hardware (switch chip) supports FastTrack HW Offloading. |

## Interface Lists

It is impossible to use interface lists directly to control `l3-hw-offloading` because an interface list may contain virtual interfaces (such as VLAN) while the `l3-hw-offloading` setting must be applied to physical switch ports only. For example, if there are two VLAN interfaces (vlan20 and vlan30) running on the same switch port (trunk port), it is impossible to enable hardware routing on vlan20 but keep it disabled on vlan30.

However, an interface list may be used as a port selector. The following example demonstrates how to enable hardware routing on LAN ports (ports that belong to the "LAN" interface list) and disable it on WAN ports:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">:</code><code class="ros functions">foreach </code><code class="ros plain">i </code><code class="ros value">in</code><code class="ros plain">=[/interface/list/member/find</code> <code class="ros plain">where </code><code class="ros value">list</code><code class="ros plain">=LAN]</code> <code class="ros value">do</code><code class="ros plain">=</code><code class="ros plain">{</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros constants">/interface/ethernet/switch/port </code><code class="ros functions">set </code><code class="ros plain">[</code><code class="ros constants">/interface/list/member/</code><code class="ros functions">get </code><code class="ros keyword">$i</code> <code class="ros plain">interface] </code><code class="ros value">l3-hw-offloading</code><code class="ros plain">=yes</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">}</code></div><div class="line number4 index3 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros constants">:</code><code class="ros functions">foreach </code><code class="ros plain">i </code><code class="ros value">in</code><code class="ros plain">=[/interface/list/member/find</code> <code class="ros plain">where </code><code class="ros value">list</code><code class="ros plain">=WAN]</code> <code class="ros value">do</code><code class="ros plain">=</code><code class="ros plain">{</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros constants">/interface/ethernet/switch/port </code><code class="ros functions">set </code><code class="ros plain">[</code><code class="ros constants">/interface/list/member/</code><code class="ros functions">get </code><code class="ros keyword">$i</code> <code class="ros plain">interface] </code><code class="ros value">l3-hw-offloading</code><code class="ros plain">=no</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">}</code></div></div></td></tr></tbody></table>

Please take into account that since interface lists are not used directly in the hardware routing control, **modifying the interface list also does not automatically reflect into l3hw changes**. For instance, adding a switch port to the "LAN" interface list does not automatically enable `l3-hw-offloading` on that. The user has to rerun the above script to apply the changes.

## MTU

The hardware supports up to 8 MTU profiles, meaning that the user can set up to 8 different MTU values for interfaces: the default 1500 + seven custom ones.

It is recommended to disable `l3-hw-offloading` while changing the MTU/L2MTU values on the interfaces.

**MTU Change Example**

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface/ethernet/switch </code><code class="ros functions">set </code><code class="ros plain">0 </code><code class="ros value">l3-hw-offloading</code><code class="ros plain">=no</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros constants">/interface </code><code class="ros functions">set </code><code class="ros plain">sfp-sfpplus1 </code><code class="ros value">mtu</code><code class="ros plain">=9000</code> <code class="ros value">l2mtu</code><code class="ros plain">=9022</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/interface </code><code class="ros functions">set </code><code class="ros plain">sfp-sfpplus2 </code><code class="ros value">mtu</code><code class="ros plain">=9000</code> <code class="ros value">l2mtu</code><code class="ros plain">=9022</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros constants">/interface </code><code class="ros functions">set </code><code class="ros plain">sfp-sfpplus3 </code><code class="ros value">mtu</code><code class="ros plain">=10000</code> <code class="ros value">l2mtu</code><code class="ros plain">=10022</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros constants">/interface/ethernet/switch </code><code class="ros functions">set </code><code class="ros plain">0 </code><code class="ros value">l3-hw-offloading</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

## Layer 2 Dependency

Layer 3 hardware processing lies on top of Layer 2 hardware processing. Therefore, L3HW offloading requires L2HW offloading on the underlying interfaces. The latter is enabled by default, but there are some exceptions. For example, CRS3xx devices support only one hardware bridge. If there are multiple bridges, others are processed by the CPU and are not subject to L3HW. 

Another example is ACL rules. If a rule redirects traffic to the CPU for software processing, then hardware routing (L3HW) is not triggered:

**ACL rule to disable hardware processing on a specific port**

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface/ethernet/switch/rule/</code><code class="ros functions">add </code><code class="ros value">switch</code><code class="ros plain">=switch1</code> <code class="ros value">ports</code><code class="ros plain">=ether1</code> <code class="ros value">redirect-to-cpu</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

It is recommended to turn off L3HW offloading during L2 configuration.

To make sure that Layer 3 is in sync with Layer 2 on both the software and hardware sides, we recommend disabling L3HW while configuring Layer 2 features. The recommendation applies to the following configuration:

-   adding/removing/enabling/disabling bridge;
-   adding/removing switch ports to/from the bridge;
-   bonding switch ports / removing bond;
-   changing VLAN settings;
-   changing MTU/L2MTU on switch ports;
-   changing ethernet (MAC) addresses.

In short, disable `l3-hw-offloading` while making changes under `/interface/bridge/` and `/interface/vlan/`:

**Layer 2 Configuration Template**

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface/ethernet/switch </code><code class="ros functions">set </code><code class="ros plain">0 </code><code class="ros value">l3-hw-offloading</code><code class="ros plain">=no</code></div><div class="line number2 index1 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/interface/bridge</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros comments"># put bridge configuration changes here</code></div><div class="line number5 index4 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros constants">/interface/vlan</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros comments"># define/change VLAN interfaces</code></div><div class="line number8 index7 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros constants">/interface/ethernet/switch </code><code class="ros functions">set </code><code class="ros plain">0 </code><code class="ros value">l3-hw-offloading</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

## MAC telnet and RoMON

There is a limitation for MAC telnet and RoMON when L3HW offloading is enabled on **98DX8xxx**, **98DX4xxx** or **98DX325x** switch chips. Packets from these protocols are dropped and do not reach the CPU, thus access to the device will fail.

If MAC telnet or RoMON are desired in combination with L3HW, certain ACL rules can be created to force these packets to the CPU.

For example, if MAC telnet access on sfp-sfpplus1 and sfp-sfpplus2 is needed, you will need to add this ACL rule. It is possible to select even more interfaces with the `ports` setting.

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface ethernet switch rule</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">dst-port</code><code class="ros plain">=20561</code> <code class="ros value">ports</code><code class="ros plain">=sfp-sfpplus1,sfp-sfpplus2</code> <code class="ros value">protocol</code><code class="ros plain">=udp</code> <code class="ros value">redirect-to-cpu</code><code class="ros plain">=yes</code> <code class="ros value">switch</code><code class="ros plain">=switch1</code></div></div></td></tr></tbody></table>

For example, if RoMON access on sfp-sfpplus2 is needed, you will need to add this ACL rule.

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface ethernet switch rule</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">mac-protocol</code><code class="ros plain">=0x88BF</code> <code class="ros value">ports</code><code class="ros plain">=sfp-sfpplus2</code> <code class="ros value">redirect-to-cpu</code><code class="ros plain">=yes</code> <code class="ros value">switch</code><code class="ros plain">=switch1</code></div></div></td></tr></tbody></table>

## Inter-VLAN Routing

Since L3HW depends on L2HW, and L2HW is the one that does VLAN processing, Inter-VLAN _hardware_ routing requires a hardware bridge underneath. Even if a particular VLAN has only one tagged port member, the latter must be a bridge member. Do not assign a VLAN interface directly on a switch port! Otherwise, L3HW offloading fails and the traffic will get processed by the CPU:

`~/interface/vlan add interface=ether2 name=vlan20 vlan-id=20~`

Assign VLAN interface to the bridge instead. This way, VLAN configuration gets offloaded to the hardware, and, with L3HW enabled, the traffic is subject to inter-VLAN hardware routing.

**VLAN Configuration Example**

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface/ethernet/switch </code><code class="ros functions">set </code><code class="ros plain">0 </code><code class="ros value">l3-hw-offloading</code><code class="ros plain">=no</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros constants">/interface/bridge/port </code><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">interface</code><code class="ros plain">=ether2</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/interface/bridge/vlan </code><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">tagged</code><code class="ros plain">=bridge,ether2</code> <code class="ros value">vlan-ids</code><code class="ros plain">=20</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros constants">/interface/vlan </code><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=bridge</code> <code class="ros value">name</code><code class="ros plain">=vlan20</code> <code class="ros value">vlan-id</code><code class="ros plain">=20</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros constants">/ip/address </code><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=192.0.2.1/24</code> <code class="ros value">interface</code><code class="ros plain">=vlan20</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros constants">/interface/bridge </code><code class="ros functions">set </code><code class="ros plain">bridge </code><code class="ros value">vlan-filtering</code><code class="ros plain">=yes</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros constants">/interface/ethernet/switch </code><code class="ros functions">set </code><code class="ros plain">0 </code><code class="ros value">l3-hw-offloading</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

For Inter-VLAN routing, the bridge interface must be a tagged member of every routable `/interface/bridge/vlan/` entry.

## L3HW MAC Address Range Limitation (DX2000/DX3000 series only)

Marvell Prestera DX2000 and DX3000 switch chips have a hardware limitation that allows configuring only the last (least significant) octet of the MAC address for each interface. The other five (most significant) octets are configurated globally and, therefore, must be equal for all interfaces (switch ports, bridge, VLANs). In other words, the MAC addresses must be in the format "**XX:XX:XX:XX:XX:??**", where:

-   "**XX:XX:XX:XX:XX**" part is common for all interfaces.
-   "**??**" is a variable part.

**This requirement applies only to Layer 3 (routing).** Layer 2 (bridging) does not use the switch's ethernet addresses. Moreover, it does not apply to bridge ports because they use the bridge's MAC address.

The requirement for common five octets applies to:

-   Standalone switch ports (not bridge members) with hardware routing enabled (`l3-hw-offloading=yes`).
-   Bridge itself.
-   VLAN interfaces (those are using bridge's MAC address by default).

# Route Configuration

## Suppressing HW Offload

By default, all the routes are participating to be hardware candidate routes. To further fine-tune which traffic to offload, there is an option for each route to disable/enable **`suppress-hw-offload`**. 

For example, if we know that majority of traffic flows to the network where servers are located, we can enable offloading only to that specific destination:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip/route </code><code class="ros functions">set </code><code class="ros plain">[</code><code class="ros functions">find </code><code class="ros plain">where static &amp;&amp; dst-address!</code><code class="ros plain">=</code><code class="ros string">"192.168.3.0/24"</code><code class="ros plain">] </code><code class="ros value">suppress-hw-offload</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

Now only the route to 192.168.3.0/24 has H-flag, indicating that it will be the only one eligible to be selected for HW offloading:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; </code><code class="ros constants">/ip/route </code><code class="ros functions">print </code><code class="ros plain">where static</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: A - ACTIVE; s - STATIC, y - COPY; H - HW-OFFLOADED</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">Columns</code><code class="ros constants">: DST-ADDRESS, GATEWAY, DISTANCE</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros comments">#&nbsp;&nbsp;&nbsp;&nbsp; DST-ADDRESS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; GATEWAY&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; D</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">0 As&nbsp; </code><code class="ros color1">0.0.0.0/0</code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <code class="ros plain">172.16.2.1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 1</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">1 As&nbsp; </code><code class="ros color1">10.0.0.0/8</code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <code class="ros plain">10.155.121.254&nbsp; 1</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">2 AsH </code><code class="ros color1">192.168.3.0/24</code>&nbsp;&nbsp;&nbsp; <code class="ros plain">172.16.2.1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 1</code></div></div></td></tr></tbody></table>

H-flag does not indicate that route is actually HW offloaded, it indicates only that route can be selected to be HW offloaded.

## Routing Filters

For dynamic routing protocols like OSFP and BGP, it is possible to suppress HW offloading using [routing filters](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=74678285). For example, to suppress HW offloading on all OSFP instance routes, use "**`suppress-hw-offload yes`**" property:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/routing/ospf/instance</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">[</code><code class="ros functions">find </code><code class="ros value">name</code><code class="ros plain">=instance1]</code> <code class="ros value">in-filter-chain</code><code class="ros plain">=ospf-input</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/routing/filter/rule</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">chain</code><code class="ros plain">=</code><code class="ros string">"ospf-input"</code> <code class="ros value">rule</code><code class="ros plain">=</code><code class="ros string">"set suppress-hw-offload yes; accept"</code></div></div></td></tr></tbody></table>

## Offloading Fasttrack Connections

Firewall filter rules have **`hw-offload`** option for Fasttrack, allowing fine-tuning connection offloading. Since the hardware memory for Fasttrack connections is very limited, we can choose what type of connections to offload and, therefore, benefit from near-the-wire-speed traffic. The next example offloads only TCP connections while UDP packets are routed via the CPU and do not occupy HW memory:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip/firewall/filter</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=fasttrack-connection</code> <code class="ros value">chain</code><code class="ros plain">=forward</code> <code class="ros value">connection-state</code><code class="ros plain">=established,related</code> <code class="ros value">hw-offload</code><code class="ros plain">=yes</code> <code class="ros value">protocol</code><code class="ros plain">=tcp</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=fasttrack-connection</code> <code class="ros value">chain</code><code class="ros plain">=forward</code> <code class="ros value">connection-state</code><code class="ros plain">=established,related</code> <code class="ros value">hw-offload</code><code class="ros plain">=no</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=accept</code> <code class="ros value">chain</code><code class="ros plain">=forward</code> <code class="ros value">connection-state</code><code class="ros plain">=established,related</code></div></div></td></tr></tbody></table>

## Stateless Hardware Firewall

While connection tracking and stateful firewalling can be performed only by the CPU, the hardware can perform stateless firewalling via [switch rules (ACL)](https://help.mikrotik.com/docs/display/ROS/CRS3xx%2C+CRS5xx%2C+CCR2116%2C+CCR2216+switch+chip+features#CRS3xx,CRS5xx,CCR2116,CCR2216switchchipfeatures-SwitchRules(ACL)). The next example prevents (on a hardware level) accessing a MySQL server from the ether1, and redirects to the CPU/Firewall packets from ether2 and ether3:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface ethernet switch rule</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">switch</code><code class="ros plain">=switch1</code> <code class="ros value">dst-address</code><code class="ros plain">=10.0.1.2/32</code> <code class="ros value">dst-port</code><code class="ros plain">=3306</code> <code class="ros value">ports</code><code class="ros plain">=ether1</code> <code class="ros value">new-dst-ports</code><code class="ros plain">=</code><code class="ros string">""</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">switch</code><code class="ros plain">=switch1</code> <code class="ros value">dst-address</code><code class="ros plain">=10.0.1.2/32</code> <code class="ros value">dst-port</code><code class="ros plain">=3306</code> <code class="ros value">ports</code><code class="ros plain">=ether2,ether3</code> <code class="ros value">redirect-to-cpu</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

## Switch Rules (ACL) vs. Fasttrack HW Offloading

Some firewall rules may be implemented both via [switch rules (ACL)](https://help.mikrotik.com/docs/display/ROS/CRS3xx%2C+CRS5xx%2C+CCR2116%2C+CCR2216+switch+chip+features#CRS3xx,CRS5xx,CCR2116,CCR2216switchchipfeatures-SwitchRules(ACL)) and CPU [Firewall Filter](https://help.mikrotik.com/docs/display/ROS/Filter) \+ Fasttrack HW Offloading. Both options grant near-the-wire-speed performance. So the question is which one to use?

First, [not all devices support Fasttrack HW Offloading](https://help.mikrotik.com/docs/display/ROS/L3+Hardware+Offloading#L3HardwareOffloading-L3HWDeviceSupport). And without HW offloading, Firewall Filter uses only software routing, which is dramatically slower than its hardware counterpart. Second, even if Fasttrack HW Offloading is an option, a rule of thumb is:

Always use Switch Rules (ACL), if possible.

Switch rules share the hardware memory with Fastrack connections. However, hardware resources are allocated for each Fasttrack connection while a single ACL rule can match multiple connections. For example, if you have a guest WiFi network connected to sfp-sfpplus1 VLAN 10 and you don't want it to access your internal network, simply create an ACL rule:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface/ethernet/switch/rule</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">switch</code><code class="ros plain">=switch1</code> <code class="ros value">ports</code><code class="ros plain">=sfp-sfpplus1</code> <code class="ros value">vlan-id</code><code class="ros plain">=10</code> <code class="ros value">dst-address</code><code class="ros plain">=10.0.0.0/8</code> <code class="ros value">new-dst-ports</code><code class="ros plain">=</code><code class="ros string">""</code></div></div></td></tr></tbody></table>

The matched packets will be dropped on the hardware level. It is much better than letting _all_ guest packets to the CPU for Firewall filtering.

Of course, ACL rules cannot match everything. For instance, ACL rules cannot filter connection states: accept established, drop others. That is where Fasttrack HW Offloading gets into action - redirect the packets to the CPU by default for firewall filtering, then offload the established Fasttrack connections. However, disabling `l3-hw-offloading` for the entire switch port is not the only option.

Define ACL rules with `**redirect-to-cpu=yes**` instead of setting `l3-hw-offloading=no` of the switch port for narrowing down the traffic that goes to the CPU.

# Configuration Examples

## Inter-VLAN Routing with Upstream Port Behind Firewall/NAT

This example demonstrates how to benefit from near-to-wire-speed inter-VLAN routing while keeping Firewall and NAT running on the upstream port. Moreover, Fasttrack connections to the upstream port get offloaded to hardware as well, boosting the traffic speed close to wire-level. Inter-VLAN traffic is fully routed by the hardware, not entering the CPU/Firewall, and, therefore, not occupying the hardware memory of Fasttrack connections.

We use the **CRS317-1G-16S+** model with the following setup:

-   sfp1-sfp4 - bridged ports, VLAN ID 20, untagged
-   sfp5-sfp8 - bridged ports, VLAN ID 30, untagged
-   sfp16 - the upstream port
-   ether1 - management port

  

Setup interface lists for easy access:

**Interface Lists**

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface list</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=LAN</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=WAN</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=MGMT</code></div><div class="line number5 index4 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros constants">/interface list member</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=sfp-sfpplus1</code> <code class="ros value">list</code><code class="ros plain">=LAN</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=sfp-sfpplus2</code> <code class="ros value">list</code><code class="ros plain">=LAN</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=sfp-sfpplus3</code> <code class="ros value">list</code><code class="ros plain">=LAN</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=sfp-sfpplus4</code> <code class="ros value">list</code><code class="ros plain">=LAN</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=sfp-sfpplus5</code> <code class="ros value">list</code><code class="ros plain">=LAN</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=sfp-sfpplus6</code> <code class="ros value">list</code><code class="ros plain">=LAN</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=sfp-sfpplus7</code> <code class="ros value">list</code><code class="ros plain">=LAN</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=sfp-sfpplus8</code> <code class="ros value">list</code><code class="ros plain">=LAN</code></div><div class="line number15 index14 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=sfp-sfpplus16</code> <code class="ros value">list</code><code class="ros plain">=WAN</code></div><div class="line number16 index15 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=ether1</code> <code class="ros value">list</code><code class="ros plain">=MGMT</code></div></div></td></tr></tbody></table>

**Bridge Setup**

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=bridge</code> <code class="ros value">vlan-filtering</code><code class="ros plain">=yes</code></div><div class="line number3 index2 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros constants">/interface bridge port</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">interface</code><code class="ros plain">=sfp-sfpplus1</code> <code class="ros value">pvid</code><code class="ros plain">=20</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">interface</code><code class="ros plain">=sfp-sfpplus2</code> <code class="ros value">pvid</code><code class="ros plain">=20</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">interface</code><code class="ros plain">=sfp-sfpplus3</code> <code class="ros value">pvid</code><code class="ros plain">=20</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">interface</code><code class="ros plain">=sfp-sfpplus4</code> <code class="ros value">pvid</code><code class="ros plain">=20</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">interface</code><code class="ros plain">=sfp-sfpplus5</code> <code class="ros value">pvid</code><code class="ros plain">=30</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">interface</code><code class="ros plain">=sfp-sfpplus6</code> <code class="ros value">pvid</code><code class="ros plain">=30</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">interface</code><code class="ros plain">=sfp-sfpplus7</code> <code class="ros value">pvid</code><code class="ros plain">=30</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">interface</code><code class="ros plain">=sfp-sfpplus8</code> <code class="ros value">pvid</code><code class="ros plain">=30</code></div><div class="line number13 index12 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="ros constants">/interface bridge vlan</code></div><div class="line number15 index14 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">tagged</code><code class="ros plain">=bridge</code> <code class="ros value">untagged</code><code class="ros plain">=sfp-sfpplus1,sfp-sfpplus2,sfp-sfpplus3,sfp-sfpplus4</code> <code class="ros value">vlan-ids</code><code class="ros plain">=20</code></div><div class="line number16 index15 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">tagged</code><code class="ros plain">=bridge</code> <code class="ros value">untagged</code><code class="ros plain">=sfp-sfpplus5,sfp-sfpplus6,sfp-sfpplus7,sfp-sfpplus8</code> <code class="ros value">vlan-ids</code><code class="ros plain">=30</code></div></div></td></tr></tbody></table>

Routing requires dedicated VLAN interfaces. For standard L2 VLAN bridging (without inter-VLAN routing), the next step can be omitted.

**VLAN Interface Setup for Routing**

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface vlan</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=bridge</code> <code class="ros value">name</code><code class="ros plain">=vlan20</code> <code class="ros value">vlan-id</code><code class="ros plain">=20</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=bridge</code> <code class="ros value">name</code><code class="ros plain">=vlan30</code> <code class="ros value">vlan-id</code><code class="ros plain">=30</code></div><div class="line number4 index3 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros constants">/ip address</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=192.168.20.17/24</code> <code class="ros value">interface</code><code class="ros plain">=vlan20</code> <code class="ros value">network</code><code class="ros plain">=192.168.20.0</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=192.168.30.17/24</code> <code class="ros value">interface</code><code class="ros plain">=vlan30</code> <code class="ros value">network</code><code class="ros plain">=192.168.30.0</code></div></div></td></tr></tbody></table>

Configure management and upstream ports, a basic firewall, NAT, and enable hardware offloading of Fasttrack connections:

**Firewall Setup**

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip address</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=192.168.88.1/24</code> <code class="ros value">interface</code><code class="ros plain">=ether1</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=10.0.0.17/24</code> <code class="ros value">interface</code><code class="ros plain">=sfp-sfpplus16</code></div><div class="line number4 index3 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros constants">/ip route</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">gateway</code><code class="ros plain">=10.0.0.1</code></div><div class="line number7 index6 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros constants">/ip firewall filter</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=fasttrack-connection</code> <code class="ros value">chain</code><code class="ros plain">=forward</code> <code class="ros value">connection-state</code><code class="ros plain">=established,related</code> <code class="ros value">hw-offload</code><code class="ros plain">=yes</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=accept</code> <code class="ros value">chain</code><code class="ros plain">=forward</code> <code class="ros value">connection-state</code><code class="ros plain">=established,related</code></div><div class="line number11 index10 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros constants">/ip firewall nat</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=masquerade</code> <code class="ros value">chain</code><code class="ros plain">=srcnat</code> <code class="ros value">out-interface-list</code><code class="ros plain">=WAN</code></div></div></td></tr></tbody></table>

At this moment, all routing still is performed by the CPU. Enable hardware routing on the switch chip:

**Enable Layer 3 Hardware Offloading**

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros comments"># Enable full hardware routing on LAN ports</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros constants">:</code><code class="ros functions">foreach </code><code class="ros plain">i </code><code class="ros value">in</code><code class="ros plain">=[/interface/list/member/find</code> <code class="ros plain">where </code><code class="ros value">list</code><code class="ros plain">=LAN]</code> <code class="ros value">do</code><code class="ros plain">=</code><code class="ros plain">{</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros constants">/interface/ethernet/switch/port </code><code class="ros functions">set </code><code class="ros plain">[</code><code class="ros constants">/interface/list/member/</code><code class="ros functions">get </code><code class="ros keyword">$i</code> <code class="ros plain">interface] </code><code class="ros value">l3-hw-offloading</code><code class="ros plain">=yes</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">}</code></div><div class="line number5 index4 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros comments"># Disable full hardware routing on WAN or Management ports</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros constants">:</code><code class="ros functions">foreach </code><code class="ros plain">i </code><code class="ros value">in</code><code class="ros plain">=[/interface/list/member/find</code> <code class="ros plain">where </code><code class="ros value">list</code><code class="ros plain">=WAN</code> <code class="ros variable">or</code> <code class="ros value">list</code><code class="ros plain">=MGMT]</code> <code class="ros value">do</code><code class="ros plain">=</code><code class="ros plain">{</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros constants">/interface/ethernet/switch/port </code><code class="ros functions">set </code><code class="ros plain">[</code><code class="ros constants">/interface/list/member/</code><code class="ros functions">get </code><code class="ros keyword">$i</code> <code class="ros plain">interface] </code><code class="ros value">l3-hw-offloading</code><code class="ros plain">=no</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros plain">}</code></div><div class="line number10 index9 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros comments"># Activate Layer 3 Hardware Offloading on the switch chip</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros constants">/interface/ethernet/switch/</code><code class="ros functions">set </code><code class="ros plain">0 </code><code class="ros value">l3-hw-offloading</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

Results:

-   Within the same VLAN (e.g., sfp1-sfp4), traffic is forwarded by the hardware on Layer 2 _(L2HW)_.
-   Inter-VLAN traffic (e.g. sfp1-sfp5) is routed by the hardware on Layer 3 _(L3HW)._
-   Traffic from/to WAN port gets processed by the CPU/Firewall first. Then Fasttrack connections get offloaded to the hardware _(Hardware-Accelerated L4 Stateful Firewall)._ NAT applies both on CPU- and HW-processed packets.
-   Traffic to the management port is protected by the Firewall.

# Typical Misconfiguration

Below are typical user errors of configuring Layer 3 Hardware Offloading.

## VLAN interface on a switch port

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface vlan </code><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=vlan10</code> <code class="ros value">vlan-id</code><code class="ros plain">=10</code> <code class="ros value">interface</code><code class="ros plain">=sfp-sfpplus1</code></div></div></td></tr></tbody></table>

VLAN interface must be set on the bridge due to Layer 2 Dependency. Otherwise, L3HW will not work. The correct configuration is:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge port </code><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=sfp-sfpplus1</code> <code class="ros value">pvid</code><code class="ros plain">=10</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros constants">/interface bridge vlan </code><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">tagged</code><code class="ros plain">=bridge1,sfp-sfpplus1</code> <code class="ros value">vlan-ids</code><code class="ros plain">=10</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/interface vlan </code><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=vlan10</code> <code class="ros value">vlan-id</code><code class="ros plain">=10</code> <code class="ros value">interface</code><code class="ros plain">=bridge1</code></div></div></td></tr></tbody></table>

## Not adding the bridge interface to /in/br/vlan

For Inter-VLAN routing, the bridge interface itself needs to be added to the tagged members of the given VLANs. In the next example, Inter-VLAN routing works between VLAN 10 and 11, but packets are NOT routed to VLAN 20. 

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge vlan</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">vlan-ids</code><code class="ros plain">=10</code> <code class="ros value">tagged</code><code class="ros plain">=bridge1,sfp-sfpplus1</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">vlan-ids</code><code class="ros plain">=11</code> <code class="ros value">tagged</code><code class="ros plain">=bridge1</code> <code class="ros value">untagged</code><code class="ros plain">=sfp-sfpplus2,sfp-sfpplus3</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">vlan-ids</code><code class="ros plain">=20</code> <code class="ros value">tagged</code><code class="ros plain">=sfp-sfpplus1</code> <code class="ros value">untagged</code><code class="ros plain">=sfp-sfpplus4,sfp-sfpplus5</code></div></div></td></tr></tbody></table>

The above example does not always mean an error. Sometimes, you may want the device to act as a simple L2 switch in some/all VLANs. Just make sure you set such behavior on purpose, not due to a mistake.

## Creating multiple bridges

The devices support only one hardware bridge. If there are multiple bridges created, only one gets hardware offloading. While for L2 that means software forwarding for other bridges, in the case of L3HW, multiple bridges may lead to undefined behavior.

Instead of creating multiple bridges, create one and segregate L2 networks with VLAN filtering.

## Using ports that do not belong to the switch

Some devices have two switch chips or the management port directly connected to the CPU. For example, **CRS312-4C+8XG** has an **ether9** port connected to a separate switch chip. Trying to add this port to a bridge or involve it in the L3HW setup leads to unexpected results. Leave the management port for management!

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@crs312] </code><code class="ros constants">/interface/ethernet/switch&gt; </code><code class="ros plain">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Columns</code><code class="ros constants">: NAME, TYPE, L3-HW-OFFLOADING</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros comments"># NAME&nbsp;&nbsp;&nbsp;&nbsp; TYPE&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; L3-HW-OFFLOADING</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">0&nbsp;switch1&nbsp; Marvell-98DX8212&nbsp; yes&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">1&nbsp;switch2&nbsp; Atheros-8227&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;no&nbsp;&nbsp;&nbsp;</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code>&nbsp;</div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">[admin@crs312] </code><code class="ros constants">/interface/ethernet/switch&gt; port </code><code class="ros plain">print</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros plain">Columns</code><code class="ros constants">: NAME, SWITCH, L3-HW-OFFLOADING, STORM-RATE</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros comments"># NAME&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; SWITCH&nbsp;&nbsp; L3-HW-OFFLOADING&nbsp; STORM-RATE</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">0&nbsp;ether9&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; switch2&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">1&nbsp;ether1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; switch1&nbsp; yes&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;100</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">2&nbsp;ether2&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; switch1 &nbsp;yes &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;100</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">3&nbsp;ether3&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; switch1 &nbsp;yes &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;100</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">4&nbsp;ether4&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; switch1 &nbsp;yes &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;100</code></div><div class="line number15 index14 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">5&nbsp;ether5&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; switch1 &nbsp;yes &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;100</code></div><div class="line number16 index15 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">6&nbsp;ether6&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; switch1 &nbsp;yes &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;100</code></div><div class="line number17 index16 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">7&nbsp;ether7&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; switch1 &nbsp;yes &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;100</code></div><div class="line number18 index17 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">8&nbsp;ether8&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; switch1 &nbsp;yes &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;100</code></div><div class="line number19 index18 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">9&nbsp;combo1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; switch1 &nbsp;yes &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;100</code></div><div class="line number20 index19 alt1" data-bidi-marker="true"><code class="ros plain">10&nbsp;combo2&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; switch1 &nbsp;yes &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;100</code></div><div class="line number21 index20 alt2" data-bidi-marker="true"><code class="ros plain">11&nbsp;combo3&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; switch1 &nbsp;yes &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;100</code></div><div class="line number22 index21 alt1" data-bidi-marker="true"><code class="ros plain">12&nbsp;combo4&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; switch1 &nbsp;yes &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;100</code></div><div class="line number23 index22 alt2" data-bidi-marker="true"><code class="ros plain">13&nbsp;switch1-cpu&nbsp; switch1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;100</code></div><div class="line number24 index23 alt1" data-bidi-marker="true"><code class="ros plain">14&nbsp;switch2-cpu&nbsp; switch2</code></div></div></td></tr></tbody></table>

## Relying on Fasttrack HW Offloading too much

Since Fasttrack HW Offloading offers near-the-wire-speed performance at zero configuration overhead, the users tempt to use it as the default solution. However, the number of HW Fasttrack connections is very limited, leaving the other traffic for the CPU. Try using the hardware routing as much as possible, reduce the CPU traffic to the minimum via switch ACL rules, and then fine-tune which Fasttrack connections to offload with firewall filter rules.

# L3HW Feature Support

-   **HW** \- the feature is supported and offloaded to the hardware.
-   **CPU** \- the feature is supported but performed by software (CPU)
-   **N/A** \- the feature is not available together with L3HW. Layer 3 hardware offloading must be completely disabled (**switch** `l3-hw-offloading=no`) to make this feature work.
-   **FW** \- the feature requires `l3-hw-offloading``=no` for a given **switch port**. On the **switch** level, `l3-hw-offloading=yes`.

  

| 
Feature

 | 

Support

 | 

Comments

 | 

Release

 |     |
 | --- ||  |  |
 |     |

Feature

 | 

Support

 | 

Comments

 | 

Release

 |     |
 | --- |||  |
 | IPv4 Unicast Routing | **HW** |
 | 7.1                  |
 | IPv6 Unicast Routing | **HW** |

```
/interface/ethernet/switch/l3hw-settings/set ipv6-hw=yes
```

 | 7.6 |
| IPv4 Multicast Routing | **CPU** |   
 |   
 |
| IPv6 Multicast Routing | **CPU** |   
 |   
 |
| ECMP | **HW** | Multipath routing | 7.1 |
| Blackholes | **HW** | 

```
/ip/route add dst-address=10.0.99.0/24 blackhole
```

 | 7.1 |
| gateway=<interface\_name> | **CPU/HW** | 

```
/ip/route add dst-address=10.0.0.0/24 gateway=ether1 
```

This works only for directly connected networks. Since HW does not know how to send ARP requests,  
CPU sends an ARP request and waits for a reply to find out a DST MAC address on the first received packet of the connection that matches a DST IP address.  
After DST MAC is determined, HW entry is added and all further packets will be processed by the switch chip.

 | 7.1 |
| BRIDGE | **HW** | IP Routing from/to [hardware-offloaded bridge](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-BridgeHardwareOffloading) interface. | 7.1 |
| VLAN | **HW** | Routing between VLAN interfaces that are created on hardware-offloaded bridge interface with [vlan-filtering](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-BridgeVLANFiltering). | 7.1 |
| Bonding | **HW** | 

```
/interface/bonding
```

 | 7.1 |
| IPv4 Firewall | **FW** | Users must choose either HW-accelerated routing or firewall.  
Firewall rules get processed by the CPU. _**Fasttrack**_ connections get offloaded to HW. | 7.1 |
| IPv4 NAT | **FW** | NAT rules applied to the offloaded _**Fasttrack**_ connections get processed by HW too. | 7.1 |
| MLAG | **N/A** |   
 |   
 |
| VRF | **N/A** | Only the **main** routing table gets offloaded. |   
 |
| VRRP | **N/A** |   
 |   
 |
| VXLAN | **CPU** |   
 |   
 |
| MTU | **HW** | The hardware supports up to 8 MTU profiles. | 7.1 |
| QinQ and tag-stacking | **CPU** | Stacked VLAN interfaces will lose HW offloading, while other VLANs created directly on the bridge interface can still use HW offloading. |   
 |

Only the devices listed in the table below support L3 HW Offloading.

# L3HW Device Support

Only the devices listed in the table below support L3 HW Offloading.

## CRS3xx: Switch DX3000 and DX2000 Series

The devices below are based on **Marvell **98DX224S, 98DX226S****, or ****98DX3236**** switch chip models. These devices do not support Fasttrack or NAT connection offloading.

The **98DX3255** and **98DX3257** models are exceptions, which have a feature set of the DX8000 rather than the DX3000 series.

| 
Model

 | 

Switch Chip

 | 

Release

 | 

IPv4 Route Prefixes<sup>1</sup>

 | 

IPv6 Route Prefixes<sup>2</sup>

 | 

Nexthops

 | 

ECMP paths per prefix<sup>3</sup>

 |     |
 | --- ||  |  |  |  |  |
 |     |

Model

 | 

Switch Chip

 | 

Release

 | 

IPv4 Route Prefixes<sup>1</sup>

 | 

IPv6 Route Prefixes<sup>2</sup>

 | 

Nexthops

 | 

ECMP paths per prefix<sup>3</sup>

 |                        |
 | ---------------------- | ---------------- | --- | ----- | ---- | --- | --- |
 | **CRS305-1G-4S+**      | ****98DX3236**** | 7.1 | 13312 | 3328 | 4K  | 8   |
 | **CRS310-1G-5S-4S+**   | ****98DX226S**** | 7.1 | 13312 | 3328 | 4K  | 8   |
 | **CRS318-1Fi-15Fr-2S** | ****98DX224S**** | 7.1 | 13312 | 3328 | 4K  | 8   |
 | **CRS318-16P-2S+**     | ****98DX226S**** | 7.1 | 13312 | 3328 | 4K  | 8   |
 | **CRS326-24G-2S+**     | ****98DX3236**** | 7.1 | 13312 | 3328 | 4K  | 8   |
 | **CRS328-24P-4S+**     | ****98DX3236**** | 7.1 | 13312 | 3328 | 4K  | 8   |
 | **CRS328-4C-20S-4S+**  | ****98DX3236**** | 7.1 | 13312 | 3328 | 4K  | 8   |

_<sup>1</sup> Since the total amount of routes that can be offloaded is limited, prefixes with higher netmask are preferred to be forwarded by hardware (e.g., /32, /30, /29, etc.), any other prefixes that do not fit in the HW table will be processed by the CPU. Directly connected hosts are offloaded as /32 (IPv4) or /128 (IPv6) route prefixes. The number of hosts is also limited by max-neighbor-entries in [IP Settings](https://help.mikrotik.com/docs/display/ROS/IP+Settings#IPSettings-IPv4Settings) / [IPv6 Settings](https://help.mikrotik.com/docs/display/ROS/IP+Settings#IPSettings-IPv6Settings)._

_<sup>2</sup> IPv4 and IPv6 routing tables share the same hardware memory._

_<sup>3</sup> If a route has more paths than the hardware ECMP limit (X), only the first X paths get offloaded._

## CRS3xx, CRS5xx: Switch DX8000 and DX4000 Series

The devices below are based on **Marvell 98DX8xxx**, **98DX4xxx** switch chips, or **98DX325x** model.

| 
Model

 | 

Switch Chip

 | 

Release

 | 

IPv4 Routes <sup>1</sup>

 | 

IPv4 Hosts <sup>7</sup>

 | 

IPv6 Routes<sup>8</sup>

 | 

IPv6 Hosts<sup>7</sup>

 | 

Nexthops

 | 

**Fasttrack** **connections <sup>2,3,4</sup>**

 | 

NAT entries <sup>2,5</sup> 

 |     |
 | --- ||  |  |  |  |  |  |  |  |
 |     |

Model

 | 

Switch Chip

 | 

Release

 | 

IPv4 Routes <sup>1</sup>

 | 

IPv4 Hosts <sup>7</sup>

 | 

IPv6 Routes<sup>8</sup>

 | 

IPv6 Hosts<sup>7</sup>

 | 

Nexthops

 | 

**Fasttrack** **connections <sup>2,3,4</sup>**

 | 

NAT entries <sup>2,5</sup> 

 |                                          |
 | ---------------------------------------- | ----------------------------- | --- | ----------- | --- | --------- | --- | --- | ----- | ----- |
 | **CRS317-1G-16S+**                       | ****98DX8216****              | 7.1 | 120K - 240K | 64K | 30K - 40K | 32K | 8K  | 4.5K  | 4K    |
 | **CRS309-1G-8S+**                        | ****98DX8208****              | 7.1 | 16K - 36K   | 16K | 4K - 6K   | 8K  | 8K  | 4.5K  | 3.9K  |
 | **CRS312-4C+8XG**                        | ****98DX8212****              | 7.1 | 16K - 36K   | 16K | 4K - 6K   | 8K  | 8K  | 2.25K | 2.25K |
 | **CRS326-24S+2Q+**                       | ****98DX8332****              | 7.1 | 16K - 36K   | 16K | 4K - 6K   | 8K  | 8K  | 2.25K | 2.25K |
 | **CRS354-48G-4S+2Q+, CRS354-48P-4S+2Q+** | ****98DX3257 <sup>6</sup>**** | 7.1 | 16K - 36K   | 16K | 4K - 6K   | 8K  | 8K  | 2.25K | 2.25K |
 | **CRS504-4XQ**                           | ****98DX4310****              | 7.1 | 60K - 120K  | 64K | 15K - 20K | 32K | 8K  | 4.5K  | 4K    |
 | **CRS518-16XS-2XQ**                      | **98DX8525**                  | 7.3 | 60K - 120K  | 64K | 15K - 20K | 32K | 8K  | 4.5K  | 4K    |

_<sup>1</sup> Depends on the complexity of the routing table. Whole-byte IP prefixes (/8, /16, /24, etc.) occupy less HW space than others (e.g., /22). Starting with **RouterOS v7.3**, when the Routing HW table gets full, only routes with longer subnet prefixes are offloaded (/30, /29, /28, etc.) while the CPU processes the shorter prefixes. In RouterOS v7.2 and before, Routing HW memory overflow led to undefined behavior. Users can fine-tune what routes to offload via routing filters (for dynamic routes) or suppressing hardware offload of static routes. IPv4 and IPv6 routing tables share the same hardware memory._

_<sup>2</sup> When the HW limit of Fasttrack or NAT entries is reached, other connections will fall back to the CPU. MikroTik's smart connection offload algorithm ensures that the connections with the most traffic are offloaded to the hardware._

_<sup>3</sup> Fasttrack connections share the same HW memory with ACL rules. Depending on the complexity, one ACL rule may occupy the memory of 3-6 Fasttrack connections._

_<sup>4</sup>_ _MPLS shares the HW memory with Fasttrack connections. Moreover, enabling MPLS requires the allocation of the entire memory region, which could otherwise store up to 768 (0.75K) Fasttrack connections. The same applies to Bridge Port Extender. However, MPLS and BPE may use the same memory region, so enabling them both doesn't double the limitation of Fasttrack connections._

_<sup>5</sup> If a Fasttrack connection requires Network Address Translation, a hardware NAT entry is created. The hardware supports both SRCNAT and DSTNAT._

_<sup>6</sup> The switch chip has a feature set of the DX8000 series._

_<sup>7</sup> DX4000/DX8000 switch chips store directly connected hosts, IPv4 /32, and IPv6 /128 route entries in the FDB table rather than the routing table. The HW memory is shared between regular FDB L2 entries (MAC), IPv4, and IPv6 addresses. The number of hosts is also limited by max-neighbor-entries in [IP Settings](https://help.mikrotik.com/docs/display/ROS/IP+Settings#IPSettings-IPv4Settings) / [IPv6 Settings](https://help.mikrotik.com/docs/display/ROS/IP+Settings#IPSettings-IPv6Settings)._

_<sup>8</sup> IPv4 and IPv6 routing tables share the same hardware memory._

# CCR2000

| 
Model

 | 

Switch Chip

 | 

Release

 | 

IPv4 Routes

 | 

IPv4 Hosts

 | 

IPv6 Routes

 | 

IPv6 Hosts

 | 

Nexthops

 | 

**Fasttrack** **connections**

 | 

NAT entries

 |     |
 | --- ||  |  |  |  |  |  |  |  |
 |     |

Model

 | 

Switch Chip

 | 

Release

 | 

IPv4 Routes

 | 

IPv4 Hosts

 | 

IPv6 Routes

 | 

IPv6 Hosts

 | 

Nexthops

 | 

**Fasttrack** **connections**

 | 

NAT entries

 |                         |
 | ----------------------- | ------------------------- | --- | ---------- | --- | --------- | --- | --- | ----- | ----- |
 | **CCR2116-12G-4S+**     | **98DX3255** <sup>1</sup> | 7.1 | 16K - 36K  | 16K | 4K - 6K   | 8K  | 8K  | 2.25K | 2.25K |
 | **CCR2216-1G-12XS-2XQ** | **98DX8525**              | 7.1 | 60K - 120K | 64K | 15K - 20K | 32K | 8k  | 4.5K  | 4K    |

_<sup>1</sup> The switch chip has a feature set of the DX8000 series._