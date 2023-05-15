# Introduction

**Sub-menu:** `/interface gre`  
**Standards:** [RFC1701](https://tools.ietf.org/html/rfc1701)

GRE (Generic Routing Encapsulation) is a tunneling protocol that was originally developed by Cisco. It can encapsulate a wide variety of protocols creating a virtual point-to-point link.

GRE is the same as IPIP and EoIP which were originally developed as stateless tunnels. This means that if the remote end of the tunnel goes down, all traffic that was routed over the tunnels will get blackholed. To solve this problem, RouterOS has added a 'keepalive' feature for GRE tunnels.

GRE tunnel adds a 24 byte overhead (4-byte gre header + 20-byte IP header). GRE tunnel can forward only IP and IPv6 packets (ethernet type 800 and 86dd). Do not use the "Check gateway" option "arp" when a GRE tunnel is used as a route gateway.

# Properties

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

|                                   |
| --------------------------------- | -------------------------------- |
| **allow-fast-path** (_yes         | no_; Default: **yes**)           | Whether to allow FastPath processing. Must be disabled if IPsec tunneling is used.                                                                                                                                                                                                                                                                                        |
| **clamp-tcp-mss** (_yes           | no_; Default: **yes**)           | Controls whether to change MSS size for received TCP SYN packets. When enabled, a router will change the MSS size for received TCP SYN packets if the current MSS size exceeds the tunnel interface MTU (taking into account the TCP/IP overhead). The received encapsulated packet will still contain the original MSS, and only after decapsulation the MSS is changed. |
| **comment** (_string_; Default: ) | Short description of the tunnel. |
| **disabled** (_yes                | no_; Default: **no**)            | Enables/disables tunnel.                                                                                                                                                                                                                                                                                                                                                  |
| **dont-fragment** (_inherit       | no_; Default: **no**)            | Whether to include DF bit in related packets:                                                                                                                                                                                                                                                                                                                             |

_no_ - fragment if needed, _inherit_ - use Dont Fragment flag of original packet.

(Without Dont Fragment: inherit - packet may be fragmented).

 |
| **dscp** (_inherit | integer \[0-63\]_; Default: ) | Set dscp value in Gre header to a fixed value or inherit from dscp value taken from tunnelled traffic |
| **ipsec-secret** (_string_; Default: ) | When secret is specified, router adds dynamic IPsec peer to remote-address with pre-shared key and policy (by default phase2 uses sha1/aes128cbc). |
| **keepalive** (_integer\[/time\],integer 0..4294967295_; Default: **10s,10**) | Tunnel keepalive parameter sets the time interval in which the tunnel running flag will remain even if the remote end of tunnel goes down. If configured time,retries fail, interface running flag is removed. Parameters are written in following format: `KeepaliveInterval,KeepaliveRetries` where KeepaliveInterval is time interval and KeepaliveRetries - number of retry attempts. By default keepalive is set to 10 seconds and 10 retries. |
| **l2mtu** (_integer \[0..65536\]_; Default: **65535**) | Layer2 Maximum transmission unit. |
| **local-address** (_IP_; Default: **0.0.0.0**) | IP address that will be used for local tunnel end. If set to 0.0.0.0 then IP address of outgoing interface will be used. |
| **mtu** (_integer \[0..65536\]_; Default: **1476**) | Layer3 Maximum transmission unit. |
| **name** (_string_; Default: ) | Name of the tunnel. |
| **remote-address** (_IP_; Default: ) | IP address of remote tunnel end. |

# Setup example

The goal of this example is to get Layer 3 connectivity between two remote sites over the internet

![](https://help.mikrotik.com/docs/download/attachments/24805531/Site-to-site-gre-example.jpg?version=1&modificationDate=1612794055516&api=v2)

We have two sites, **Site1** with local network range 10.1.101.0/24 and **Site2** with local network range 10.1.202.0/24.

The first step is to create GRE tunnels. A router on site 1:

[?](https://help.mikrotik.com/docs/display/ROS/GRE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface gre </code><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=myGre</code> <code class="ros value">remote-address</code><code class="ros plain">=192.168.90.1</code> <code class="ros value">local-address</code><code class="ros plain">=192.168.80.1</code></div></div></td></tr></tbody></table>

A router on site 2:

[?](https://help.mikrotik.com/docs/display/ROS/GRE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface gre </code><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=myGre</code> <code class="ros value">remote-address</code><code class="ros plain">=192.168.80.1</code> <code class="ros value">local-address</code><code class="ros plain">=192.168.90.1</code></div></div></td></tr></tbody></table>

As you can see tunnel configuration is quite simple.

In this example, a keepalive is not configured, so tunnel interface will have a **running** flag even if remote tunnel end is not reachable

Now we just need to set up tunnel addresses and proper routing. A router on site 1:

[?](https://help.mikrotik.com/docs/display/ROS/GRE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip address </code><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=172.16.1.1/30</code> <code class="ros value">interface</code><code class="ros plain">=myGre</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros constants">/ip route </code><code class="ros functions">add </code><code class="ros value">dst-address</code><code class="ros plain">=10.1.202.0/24</code> <code class="ros value">gateway</code><code class="ros plain">=172.16.1.2</code></div></div></td></tr></tbody></table>

A router on site 2:

[?](https://help.mikrotik.com/docs/display/ROS/GRE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip address </code><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=172.16.1.2/30</code> <code class="ros value">interface</code><code class="ros plain">=myGre</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros constants">/ip route </code><code class="ros functions">add </code><code class="ros value">dst-address</code><code class="ros plain">=10.1.101.0/24</code> <code class="ros value">gateway</code><code class="ros plain">=172.16.1.1</code></div></div></td></tr></tbody></table>

At this point, both sites have Layer 3 connectivity over the GRE tunnel.