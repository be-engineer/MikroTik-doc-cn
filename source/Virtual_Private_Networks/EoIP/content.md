# Introduction

**Sub-menu:** `/interface eoip`

Ethernet over IP (EoIP) Tunneling is a MikroTik RouterOS protocol based on **[GRE RFC 1701](https://tools.ietf.org/html/rfc1701)** that creates an Ethernet tunnel between two routers on top of an IP connection. The EoIP tunnel may run over IPIP tunnel, PPTP tunnel, or any other connection capable of transporting IP.  
When the bridging function of the router is enabled, all Ethernet traffic (all Ethernet protocols) will be bridged just as if there where a physical Ethernet interface and cable between the two routers (with bridging enabled). This protocol makes multiple network schemes possible.

Network setups with EoIP interfaces:

-   Possibility to bridge LANs over the Internet
-   Possibility to bridge LANs over encrypted tunnels
-   Possibility to bridge LANs over 802.11b 'ad-hoc' wireless networks

The EoIP protocol encapsulates Ethernet frames in GRE (IP protocol number 47) packets (just like PPTP) and sends them to the remote side of the EoIP tunnel.

# Property Description

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

|                           |
| ------------------------- | ---------------------- |
| **allow-fast-path** (_yes | no_; Default: **yes**) | Whether to allow FastPath processing. Must be disabled if IPsec tunneling is used. |
| **arp (**_disabled        | enabled                | proxy-arp                                                                          | reply-only_; Default: **enabled)** | Address Resolution Protocol mode. |

-   disabled - the interface will not use ARP
-   enabled - the interface will use ARP
-   proxy-arp - the interface will use the ARP proxy feature
-   reply-only - the interface will only reply to requests originated from matching IP address/MAC address combinations which are entered as static entries in the "/ip arp" table. No dynamic entries will be automatically stored in the "/ip arp" table. Therefore for communications to be successful, a valid static entry must already exist.

 |
| **arp-timeout** (_integer\[/time\]_; Default: **auto**) | Time interval in which ARP entries should time out. |
| **clamp-tcp-mss** (_yes | no_; Default: **yes**) | Controls whether to change MSS size for received TCP SYN packets. When enabled, a router will change the MSS size for received TCP SYN packets if the current MSS size exceeds the tunnel interface MTU (taking into account the TCP/IP overhead).The received encapsulated packet will still contain the original MSS, and only after decapsulation the MSS is changed. |
| **comment** (_string_; Default: ) | Short description of the interface. |
| **disabled** (_yes | no_; Default: **no**) | Whether an item is disabled. |
| **dont-fragment** (_inherit | no_; Default: **no**) | Whether to include DF bit in related packets. |
| **dscp** (_integer: 0-63_; Default: **inherited**) | DSCP value of packet. Inherited option means that dscp value will be inherited from packet which is going to be encapsulated. |
| **ipsec-secret** (_string_; Default: ) | When secret is specified, router adds dynamic IPsec peer to remote-address with pre-shared key and policy (by default phase2 uses sha1/aes128cbc). |
| **keepalive** (_integer\[/time\],integer 0..4294967295_; Default: **10s,10**) | Tunnel keepalive parameter sets the time interval in which the tunnel running flag will remain even if the remote end of tunnel goes down. If configured time,retries fail, interface running flag is removed. Parameters are written in following format: `KeepaliveInterval,KeepaliveRetries` where `KeepaliveInterval` is time interval and `KeepaliveRetries` - number of retry attempts. By default keepalive is set to 10 seconds and 10 retries. |
| **l2mtu** (_integer; read-only_) | Layer2 Maximum transmission unit. Not configurable for EoIP. [MTU in RouterOS](https://help.mikrotik.com/docs/display/ROS/MTU+in+RouterOS) |
| **local-address** (_IP_; Default: ) | Source address of the tunnel packets, local on the router. |
| **loop-protect** |   
 |
| **loop-protect-disable-time** |   
 |
| **loop-protect-send-interval** |   
 |
| **mac-address** (_MAC_; Default: ) | Media Access Control number of an interface. The address numeration authority IANA allows the use of MAC addresses in the range from **00:00:5E:80:00:00 - 00:00:5E:FF:FF:FF** freely |
| **mtu** (_integer_; Default: **auto**) | Layer3 Maximum transmission unit |
| **name** (_string_; Default: ) | Interface name |
| **remote-address** (_IP_; Default: ) | IP address of remote end of EoIP tunnel |
| **tunnel-id** (_integer: 65536_; Default: ) | Unique tunnel identifier, which must match other side of the tunnel |

# Configuration Examples

Parameter tunnel-id is a method of identifying a tunnel. It must be unique for each EoIP tunnel.

EoIP tunnel adds at least 42 byte overhead (8byte GRE + 14 byte Ethernet + 20 byte IP). MTU should be set to 1500 to eliminate packet fragmentation inside the tunnel (that allows transparent bridging of Ethernet-like networks so that it would be possible to transport full-sized Ethernet frame over the tunnel).

When bridging EoIP tunnels, it is highly recommended to set unique MAC addresses for each tunnel for the bridge algorithms to work correctly. For EoIP interfaces you can use MAC addresses that are in the range from **00:00:5E:80:00:00 - 00:00:5E:FF:FF:FF** , which IANA has reserved for such cases. Alternatively, you can set the second bit of the first byte to modify the auto-assigned address into a 'locally administered address', assigned by the network administrator, and thus use any MAC address, you just need to ensure they are unique between the hosts connected to one bridge.

## Example

Let us assume we want to bridge two networks: 'Station' and 'AP'. By using EoIP setup can be made so that Station and AP LANs are in the same Layer2 broadcast domain.

Consider the following setup:

![](https://help.mikrotik.com/docs/download/attachments/24805521/Eoip-example.jpg?version=1&modificationDate=1612793527009&api=v2)

As you know wireless stations cannot be bridged, to overcome this limitation (not involving WDS) we will create an EoIP tunnel over the wireless link and bridge it with interfaces connected to local networks.

We will not cover wireless configuration in this example, let's assume that the wireless link is already established.

At first, we create an EoIP tunnel on our AP:

[?](https://help.mikrotik.com/docs/display/ROS/EoIP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface eoip </code><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=</code><code class="ros string">"eoip-remote"</code> <code class="ros value">tunnel-id</code><code class="ros plain">=0</code> <code class="ros value">remote-address</code><code class="ros plain">=10.0.0.2</code> <code class="ros value">disabled</code><code class="ros plain">=no</code></div></div></td></tr></tbody></table>

Verify the interface is created:

[?](https://help.mikrotik.com/docs/display/ROS/EoIP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@AP] &gt; </code><code class="ros constants">/interface eoip </code><code class="ros plain">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disabled; R - running</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">0&nbsp; R </code><code class="ros value">name</code><code class="ros plain">=</code><code class="ros string">"eoip-remote"</code> <code class="ros value">mtu</code><code class="ros plain">=auto</code> <code class="ros value">actual-mtu</code><code class="ros plain">=1458</code> <code class="ros value">l2mtu</code><code class="ros plain">=65535</code> <code class="ros value">mac-address</code><code class="ros plain">=FE:A5:6C:3F:26:C5</code> <code class="ros value">arp</code><code class="ros plain">=enabled</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">arp-timeout</code><code class="ros plain">=auto</code> <code class="ros value">loop-protect</code><code class="ros plain">=default</code> <code class="ros value">loop-protect-status</code><code class="ros plain">=off</code> <code class="ros value">loop-protect-send-interval</code><code class="ros plain">=5s</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">loop-protect-disable-time</code><code class="ros plain">=5m</code> <code class="ros value">local-address</code><code class="ros plain">=0.0.0.0</code> <code class="ros value">remote-address</code><code class="ros plain">=10.0.0.2</code> <code class="ros value">tunnel-id</code><code class="ros plain">=0</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">keepalive</code><code class="ros plain">=10s,10</code> <code class="ros value">dscp</code><code class="ros plain">=inherit</code> <code class="ros value">clamp-tcp-mss</code><code class="ros plain">=yes</code> <code class="ros value">dont-fragment</code><code class="ros plain">=no</code> <code class="ros value">allow-fast-path</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

Station router:

[?](https://help.mikrotik.com/docs/display/ROS/EoIP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface eoip </code><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=</code><code class="ros string">"eoip-main"</code> <code class="ros value">tunnel-id</code><code class="ros plain">=0</code> <code class="ros value">remote-address</code><code class="ros plain">=10.0.0.1</code> <code class="ros value">disabled</code><code class="ros plain">=no</code></div></div></td></tr></tbody></table>

Verify the interface is created:

[?](https://help.mikrotik.com/docs/display/ROS/EoIP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@Station] &gt;&nbsp; </code><code class="ros constants">/interface eoip </code><code class="ros plain">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disabled; R - running</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">0&nbsp; R </code><code class="ros value">name</code><code class="ros plain">=</code><code class="ros string">"eoip-main"</code> <code class="ros value">mtu</code><code class="ros plain">=auto</code> <code class="ros value">actual-mtu</code><code class="ros plain">=1458</code> <code class="ros value">l2mtu</code><code class="ros plain">=65535</code> <code class="ros value">mac-address</code><code class="ros plain">=FE:4B:71:05:EA:8B</code> <code class="ros value">arp</code><code class="ros plain">=enabled</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">arp-timeout</code><code class="ros plain">=auto</code> <code class="ros value">loop-protect</code><code class="ros plain">=default</code> <code class="ros value">loop-protect-status</code><code class="ros plain">=off</code> <code class="ros value">loop-protect-send-interval</code><code class="ros plain">=5s</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">loop-protect-disable-time</code><code class="ros plain">=5m</code> <code class="ros value">local-address</code><code class="ros plain">=0.0.0.0</code> <code class="ros value">remote-address</code><code class="ros plain">=10.0.0.1</code> <code class="ros value">tunnel-id</code><code class="ros plain">=0</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">keepalive</code><code class="ros plain">=10s,10</code> <code class="ros value">dscp</code><code class="ros plain">=inherit</code> <code class="ros value">clamp-tcp-mss</code><code class="ros plain">=yes</code> <code class="ros value">dont-fragment</code><code class="ros plain">=no</code> <code class="ros value">allow-fast-path</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

Next, we will bridge local interfaces with EoIP tunnel on our AP. If you already have a local bridge interface, simply add EoIP interface to it:  

[?](https://help.mikrotik.com/docs/display/ROS/EoIP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge port </code><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=eoip-remote</code></div></div></td></tr></tbody></table>

The bridge port list should list all local LAN interfaces and the EoIP interface:

[?](https://help.mikrotik.com/docs/display/ROS/EoIP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@AP] &gt; </code><code class="ros constants">/interface bridge port </code><code class="ros functions">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: I - INACTIVE; H - HW-OFFLOAD</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">Columns</code><code class="ros constants">: INTERFACE, BRIDGE, HW, PVID, PRIORITY, PATH-COST, INTERNAL-PATH-COST, HORIZON</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros comments">#&nbsp;&nbsp;&nbsp; INTERFACE &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; BRIDGE&nbsp;&nbsp; HW&nbsp;&nbsp; PVID&nbsp; PRIORITY&nbsp; PATH-COST&nbsp; INTERNAL-PATH-COST&nbsp; HORIZON</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">0&nbsp; H ether2 &nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; bridge1&nbsp; yes&nbsp;&nbsp;&nbsp;&nbsp; 1&nbsp; 0x80&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 10&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 10&nbsp; none&nbsp;&nbsp;</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">1&nbsp; H ether3 &nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; bridge1&nbsp; yes&nbsp;&nbsp;&nbsp;&nbsp; 1&nbsp; 0x80&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 10&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 10&nbsp; none &nbsp;&nbsp;</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">2 &nbsp; &nbsp;eoip-remote &nbsp; &nbsp; bridge1&nbsp; yes&nbsp;&nbsp;&nbsp;&nbsp; 1&nbsp; 0x80&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 10&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 10&nbsp; none</code></div></div></td></tr></tbody></table>

On Station router, if you do not have a local bridge interface, create a new bridge and add both EoIP and local LAN interfaces to it:  

[?](https://help.mikrotik.com/docs/display/ROS/EoIP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge </code><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=bridge1</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros constants">/interface bridge port </code><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether2</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge port </code><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=eoip-main</code></div></div></td></tr></tbody></table>

Verify the bridge port section:

[?](https://help.mikrotik.com/docs/display/ROS/EoIP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@Station] &gt; </code><code class="ros constants">/interface bridge port </code><code class="ros functions">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: I - INACTIVE; H - HW-OFFLOAD</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">Columns</code><code class="ros constants">: INTERFACE, BRIDGE, HW, PVID, PRIORITY, PATH-COST, INTERNAL-PATH-COST, HORIZON</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros comments">#&nbsp;&nbsp;&nbsp; INTERFACE &nbsp;&nbsp;&nbsp; BRIDGE&nbsp;&nbsp; HW&nbsp;&nbsp; PVID&nbsp; PRIORITY&nbsp; PATH-COST&nbsp; INTERNAL-PATH-COST&nbsp; HORIZON</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">0&nbsp; H ether2 &nbsp; &nbsp;&nbsp;&nbsp;&nbsp; bridge1&nbsp; yes&nbsp;&nbsp;&nbsp;&nbsp; 1&nbsp; 0x80&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 10&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 10&nbsp; none&nbsp;&nbsp;&nbsp;</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">2 &nbsp; &nbsp;eoip-main &nbsp; &nbsp; bridge1&nbsp; yes&nbsp;&nbsp;&nbsp;&nbsp; 1&nbsp; 0x80&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 10&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 10&nbsp; none</code></div></div></td></tr></tbody></table>

Now both sites are in the same Layer2 broadcast domain. You can set up IP addresses from the same network on both sites.