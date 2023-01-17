# 概述

**标准:** `IEEE 802.1Q, IEEE 802.1ad`

Virtual Local Area Network (VLAN) is a Layer 2 method that allows multiple Virtual LANs on a single physical interface (ethernet, wireless, etc.), giving the ability to segregate LANs efficiently.

You can use MikroTik RouterOS (as well as Cisco IOS, Linux, and other router systems) to mark these packets as well as to accept and route marked ones.

As VLAN works on OSI Layer 2, it can be used just like any other network interface without any restrictions. VLAN successfully passes through regular Ethernet bridges.

You can also transport VLANs over wireless links and put multiple VLAN interfaces on a single wireless interface. Note that as VLAN is not a full tunnel protocol (i.e., it does not have additional fields to transport MAC addresses of sender and recipient), the same limitation applies to bridging over VLAN as to bridging plain wireless interfaces. In other words, while wireless clients may participate in VLANs put on wireless interfaces, it is not possible to have VLAN put on a wireless interface in station mode bridged with any other interface.

# 802.1Q

The most commonly used protocol for Virtual LANs (VLANs) is IEEE 802.1Q. It is a standardized encapsulation protocol that defines how to insert a four-byte VLAN identifier into the Ethernet header.

Each VLAN is treated as a separate subnet. It means that by default, a host in a specific VLAN cannot communicate with a host that is a member of another VLAN, although they are connected in the same switch. So if you want inter-VLAN communication you need a router. RouterOS supports up to 4095 VLAN interfaces, each with a unique VLAN ID, per interface. VLAN priorities may also be used and manipulated.

When the VLAN extends over more than one switch, the inter-switch link has to become a 'trunk', where packets are tagged to indicate which VLAN they belong to. A trunk carries the traffic of multiple VLANs; it is like a point-to-point link that carries tagged packets between switches or between a switch and router.

The IEEE 802.1Q standard has reserved VLAN IDs with special use cases, the following VLAN IDs should not be used in generic VLAN setups: 0, 1, 4095

# Q-in-Q

Original 802.1Q allows only one VLAN header, Q-in-Q on the other hand allows two or more VLAN headers. In RouterOS, Q-in-Q can be configured by adding one VLAN interface over another. Example:

[?](https://help.mikrotik.com/docs/display/ROS/VLAN#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface vlan</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=vlan1</code> <code class="ros value">vlan-id</code><code class="ros plain">=11</code> <code class="ros value">interface</code><code class="ros plain">=ether1</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=vlan2</code> <code class="ros value">vlan-id</code><code class="ros plain">=12</code> <code class="ros value">interface</code><code class="ros plain">=vlan1</code></div></div></td></tr></tbody></table>

  

If any packet is sent over the 'vlan2' interface, two VLAN tags will be added to the Ethernet header - '11' and '12'.

# Properties

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

 |                    |
 | ------------------ | ------- |
 | **arp** (_disabled | enabled | local-proxy-arp | proxy-arp | reply-only_; Default: **enabled**) | Address Resolution Protocol setting |

-   `disabled` \- the interface will not use ARP
-   `enabled` \- the interface will use ARP
-   `local-proxy-arp` \-  the router performs proxy ARP on the interface and sends replies to the same interface
-   `proxy-arp` \- the router performs proxy ARP on the interface and sends replies to other interfaces
-   `reply-only` \- the interface will only reply to requests originated from matching IP address/MAC address combinations which are entered as static entries in the IP/ARP table. No dynamic entries will be automatically stored in the IP/ARP table. Therefore for communications to be successful, a valid static entry must already exist.

 |
| **arp-timeout** (_auto | integer_; Default: **auto**) | How long the ARP record is kept in the ARP table after no packets are received from IP. Value `auto` equals to the value of `arp-timeout` in IP/Settings, default is 30s. |
| **disabled** (_yes | no_; Default: **no**) | Changes whether the bridge is disabled. |
| **interface** (_name_; Default: ) | Name of the interface on top of which VLAN will work |
| **mtu** (_integer_; Default: **1500**) | Layer3 Maximum transmission unit |
| **name** (_string_; Default: ) | Interface name |
| **use-service-tag** (_yes | no_; Default: ) | IEEE 802.1ad compatible Service Tag |
| **vlan-id** (_integer: 4095_; Default: **1**) | Virtual LAN identifier or tag that is used to distinguish VLANs. Must be equal for all computers that belong to the same VLAN. |

MTU should be set to 1500 bytes same as on Ethernet interfaces. But this may not work with some Ethernet cards that do not support receiving/transmitting of full-size Ethernet packets with VLAN header added (1500 bytes data + 4 bytes VLAN header + 14 bytes Ethernet header). In this situation, MTU 1496 can be used, but note that this will cause packet fragmentation if larger packets have to be sent over the interface. At the same time remember that MTU 1496 may cause problems if path MTU discovery is not working properly between source and destination.

# Setup examples

## Layer2 VLAN examples

There are multiple possible configurations that you can use, but each configuration type is designed for a special set of devices since some configuration methods will give you the benefits of the built-in switch chip and gain larger throughput. Check the [Basic VLAN switching](https://help.mikrotik.com/docs/display/ROS/Basic+VLAN+switching) guide to see which configuration to use for each type of device to gain maximum possible throughput and compatibility, the guide shows how to setup a very basic VLAN trunk/access port configuration.

There are some other ways to setup VLAN tagging or VLAN switching, but the recommended way is to use [Bridge VLAN Filtering](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-BridgeVLANFiltering). Make sure you have not used any [known Layer2 misconfigurations](https://help.mikrotik.com/docs/display/ROS/Layer2+misconfiguration).

## Layer3 VLAN examples

### Simple VLAN routing

Let us assume that we have several MikroTik routers connected to a hub. Remember that a hub is an OSI physical layer device (if there is a hub between routers, then from the L3 point of view it is the same as an Ethernet cable connection between them). For simplification assume that all routers are connected to the hub using the ether1 interface and have assigned IP addresses as illustrated in the figure below. Then on each of them the VLAN interface is created.

Configuration for R2 and R4 is shown below:

R2:

[?](https://help.mikrotik.com/docs/display/ROS/VLAN#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] </code><code class="ros constants">/interface vlan&gt; </code><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=VLAN2</code> <code class="ros value">vlan-id</code><code class="ros plain">=2</code> <code class="ros value">interface</code><code class="ros plain">=ether1</code> <code class="ros value">disabled</code><code class="ros plain">=no</code></div><div class="line number2 index1 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] </code><code class="ros constants">/interface vlan&gt; </code><code class="ros functions">print</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disabled, R - running, S - slave</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros comments">#&nbsp;&nbsp;&nbsp; NAME&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; MTU&nbsp;&nbsp; ARP&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; VLAN-ID INTERFACE&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">0 R&nbsp; VLAN2&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 1500&nbsp; enabled&nbsp;&nbsp;&nbsp; 2&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ether1</code></div></div></td></tr></tbody></table>

R4:

[?](https://help.mikrotik.com/docs/display/ROS/VLAN#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] </code><code class="ros constants">/interface vlan&gt; </code><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=VLAN2</code> <code class="ros value">vlan-id</code><code class="ros plain">=2</code> <code class="ros value">interface</code><code class="ros plain">=ether1</code> <code class="ros value">disabled</code><code class="ros plain">=no</code></div><div class="line number2 index1 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] </code><code class="ros constants">/interface vlan&gt; </code><code class="ros functions">print</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disabled, R - running, S - slave</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros comments">#&nbsp;&nbsp;&nbsp; NAME&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; MTU&nbsp;&nbsp; ARP&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; VLAN-ID INTERFACE&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">0 R&nbsp; VLAN2&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 1500&nbsp; enabled&nbsp;&nbsp;&nbsp; 2&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ether1</code></div></div></td></tr></tbody></table>

The next step is to assign IP addresses to the VLAN interfaces.

R2:

[?](https://help.mikrotik.com/docs/display/ROS/VLAN#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] ip address&gt; </code><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=10.10.10.3/24</code> <code class="ros value">interface</code><code class="ros plain">=VLAN2</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] ip address&gt; print</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disabled, I - invalid, D - dynamic</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros comments">#&nbsp;&nbsp; ADDRESS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; NETWORK&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; BROADCAST&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; INTERFACE</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">0&nbsp;&nbsp; </code><code class="ros color1">10.0.1.4/24</code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <code class="ros plain">10.0.1.0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 10.0.1.255&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ether1</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">1&nbsp;&nbsp; </code><code class="ros color1">10.20.0.1/24</code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <code class="ros plain">10.20.0.0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 10.20.0.255&nbsp;&nbsp;&nbsp;&nbsp; pc1</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">2&nbsp;&nbsp; </code><code class="ros color1">10.10.10.3/24</code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <code class="ros plain">10.10.10.0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 10.10.10.255&nbsp;&nbsp;&nbsp; vlan2</code></div><div class="line number8 index7 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] ip address&gt;</code></div></div></td></tr></tbody></table>

R4:

[?](https://help.mikrotik.com/docs/display/ROS/VLAN#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] ip address&gt; </code><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=10.10.10.5/24</code> <code class="ros value">interface</code><code class="ros plain">=VLAN2</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">[admin@MikroTik] ip address&gt; print</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">Flags</code><code class="ros constants">: X - disabled, I - invalid, D - dynamic</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros comments">#&nbsp;&nbsp; ADDRESS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; NETWORK&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; BROADCAST&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; INTERFACE</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros plain">0&nbsp;&nbsp; </code><code class="ros color1">10.0.1.5/24</code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <code class="ros plain">10.0.1.0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 10.0.1.255&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ether1</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros plain">1&nbsp;&nbsp; </code><code class="ros color1">10.30.0.1/24</code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <code class="ros plain">10.30.0.0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 10.30.0.255&nbsp;&nbsp;&nbsp;&nbsp; pc2</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros plain">2&nbsp;&nbsp; </code><code class="ros color1">10.10.10.5/24</code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <code class="ros plain">10.10.10.0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 10.10.10.255&nbsp;&nbsp;&nbsp; vlan2</code></div><div class="line number8 index7 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] ip address&gt;</code></div></div></td></tr></tbody></table>

At this point it should be possible to ping router R4 from router R2 and vice versa:

[?](https://help.mikrotik.com/docs/display/ROS/VLAN#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros string">"Ping from R2 to R4:"</code></div><div class="line number2 index1 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] ip address&gt; </code><code class="ros constants">/</code><code class="ros functions">ping </code><code class="ros plain">10.10.10.5</code></div><div class="line number4 index3 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">10.10.10.5 64 byte ping</code><code class="ros constants">: ttl=255 time=4 ms</code></div><div class="line number6 index5 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">10.10.10.5 64 byte ping</code><code class="ros constants">: ttl=255 time=1 ms</code></div><div class="line number8 index7 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros plain">2 packets transmitted, 2 packets received, 0% packet loss</code></div><div class="line number10 index9 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros plain">round-trip min</code><code class="ros constants">/avg/max = 1/2.5/4 ms</code></div><div class="line number12 index11 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number13 index12 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="ros string">"From R4 to R2:"</code></div><div class="line number15 index14 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number16 index15 alt1" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] ip address&gt; </code><code class="ros constants">/</code><code class="ros functions">ping </code><code class="ros plain">10.10.10.3</code></div><div class="line number17 index16 alt2" data-bidi-marker="true"><code class="ros plain">10.10.10.3 64 byte ping</code><code class="ros constants">: ttl=255 time=6 ms</code></div><div class="line number18 index17 alt1" data-bidi-marker="true"><code class="ros plain">10.10.10.3 64 byte ping</code><code class="ros constants">: ttl=255 time=1 ms</code></div><div class="line number19 index18 alt2" data-bidi-marker="true"><code class="ros plain">2 packets transmitted, 2 packets received, 0% packet loss</code></div><div class="line number20 index19 alt1" data-bidi-marker="true"><code class="ros plain">round-trip min</code><code class="ros constants">/avg/max = 1/3.5/6 ms</code></div></div></td></tr></tbody></table>

  

To make sure if the VLAN setup is working properly, try to ping R1 from R2. If pings are timing out then VLANs are successfully isolated.

[?](https://help.mikrotik.com/docs/display/ROS/VLAN#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros string">"From R2 to R1:"</code></div><div class="line number2 index1 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] ip address&gt; </code><code class="ros constants">/</code><code class="ros functions">ping </code><code class="ros plain">10.10.10.2</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">10.10.10.2 </code><code class="ros functions">ping </code><code class="ros plain">timeout</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">10.10.10.2 </code><code class="ros functions">ping </code><code class="ros plain">timeout</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">3 packets transmitted, 0 packets received, 100% packet loss</code></div></div></td></tr></tbody></table>

### InterVLAN routing

If separate VLANs are implemented on a switch, then a router is required to provide communication between VLANs. A switch works at OSI layer 2 so it uses only Ethernet header to forward and does not check IP header. For this reason, we must use the router that is working as a gateway for each VLAN. Without a router, a host is unable to communicate outside of its own VLAN. The routing process between VLANs described above is called inter-VLAN communication.

To illustrate inter-VLAN communication, we will create a trunk that will carry traffic from three VLANs (VLAN2 and VLAN3, VLAN4) across a single link between a Mikrotik router and a manageable switch that supports VLAN trunking.

Each VLAN has its own separate subnet (broadcast domain) as we see in figure above:

-   VLAN 2 – 10.10.20.0/24;
-   VLAN 3 – 10.10.30.0/24;
-   VLAN 4 – 10.10.40.0./24.

VLAN configuration on most switches is straightforward, basically, we need to define which ports are members of the VLANs and define a 'trunk' port that can carry tagged frames between the switch and the router.

Create VLAN interfaces:

[?](https://help.mikrotik.com/docs/display/ROS/VLAN#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface vlan</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=VLAN2</code> <code class="ros value">vlan-id</code><code class="ros plain">=2</code> <code class="ros value">interface</code><code class="ros plain">=ether1</code> <code class="ros value">disabled</code><code class="ros plain">=no</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=VLAN3</code> <code class="ros value">vlan-id</code><code class="ros plain">=3</code> <code class="ros value">interface</code><code class="ros plain">=ether1</code> <code class="ros value">disabled</code><code class="ros plain">=no</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=VLAN4</code> <code class="ros value">vlan-id</code><code class="ros plain">=4</code> <code class="ros value">interface</code><code class="ros plain">=ether1</code> <code class="ros value">disabled</code><code class="ros plain">=no</code></div></div></td></tr></tbody></table>

  

Add IP addresses to VLANs:

[?](https://help.mikrotik.com/docs/display/ROS/VLAN#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip address</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=10.10.20.1/24</code> <code class="ros value">interface</code><code class="ros plain">=VLAN2</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=10.10.30.1/24</code> <code class="ros value">interface</code><code class="ros plain">=VLAN3</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=10.10.40.1/24</code> <code class="ros value">interface</code><code class="ros plain">=VLAN4</code></div></div></td></tr></tbody></table>

### RouterOS /32 and IP unnumbered addresses

In RouterOS, to create a point-to-point tunnel with addresses you have to use the address with a network mask of '/32' that effectively brings you the same features as some vendors unnumbered IP address.

There are 2 routers RouterA and RouterB where each is part of networks 10.22.0.0/24 and 10.23.0.0/24 respectively and to connect these routers using VLANs as a carrier with the following configuration:

RouterA:

[?](https://help.mikrotik.com/docs/display/ROS/VLAN#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip address </code><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=10.22.0.1/24</code> <code class="ros value">interface</code><code class="ros plain">=ether1</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros constants">/interface vlan </code><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=ether2</code> <code class="ros value">vlan-id</code><code class="ros plain">=1</code> <code class="ros value">name</code><code class="ros plain">=vlan1</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/ip address </code><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=10.22.0.1/32</code> <code class="ros value">interface</code><code class="ros plain">=vlan1</code> <code class="ros value">network</code><code class="ros plain">=10.23.0.1</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros constants">/ip route </code><code class="ros functions">add </code><code class="ros value">gateway</code><code class="ros plain">=10.23.0.1</code> <code class="ros value">dst-address</code><code class="ros plain">=10.23.0.0/24</code></div></div></td></tr></tbody></table>

RouterB:

[?](https://help.mikrotik.com/docs/display/ROS/VLAN#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip address </code><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=10.23.0.1/24</code> <code class="ros value">interface</code><code class="ros plain">=ether1</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros constants">/interface vlan </code><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=ether2</code> <code class="ros value">vlan-id</code><code class="ros plain">=1</code> <code class="ros value">name</code><code class="ros plain">=vlan1</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/ip address </code><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=10.23.0.1/32</code> <code class="ros value">interface</code><code class="ros plain">=vlan1</code> <code class="ros value">network</code><code class="ros plain">=10.22.0.1</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros constants">/ip route </code><code class="ros functions">add </code><code class="ros value">gateway</code><code class="ros plain">=10.22.0.1</code> <code class="ros value">dst-address</code><code class="ros plain">=10.22.0.0/24</code></div></div></td></tr></tbody></table>
