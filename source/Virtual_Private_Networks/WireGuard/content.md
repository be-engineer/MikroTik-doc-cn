# Introduction

-   1[Introduction](https://help.mikrotik.com/docs/display/ROS/WireGuard#WireGuard-Introduction)
-   2[Properties](https://help.mikrotik.com/docs/display/ROS/WireGuard#WireGuard-Properties)
    -   2.1[Read-only properties](https://help.mikrotik.com/docs/display/ROS/WireGuard#WireGuard-Read-onlyproperties)
-   3[Peers](https://help.mikrotik.com/docs/display/ROS/WireGuard#WireGuard-Peers)
    -   3.1[Read-only properties](https://help.mikrotik.com/docs/display/ROS/WireGuard#WireGuard-Read-onlyproperties.1)
-   4[Application examples](https://help.mikrotik.com/docs/display/ROS/WireGuard#WireGuard-Applicationexamples)
    -   4.1[Site to Site WireGuard tunnel](https://help.mikrotik.com/docs/display/ROS/WireGuard#WireGuard-SitetoSiteWireGuardtunnel)
        -   4.1.1[WireGuard interface configuration](https://help.mikrotik.com/docs/display/ROS/WireGuard#WireGuard-WireGuardinterfaceconfiguration)
        -   4.1.2[Peer configuration](https://help.mikrotik.com/docs/display/ROS/WireGuard#WireGuard-Peerconfiguration)
        -   4.1.3[IP and routing configuration](https://help.mikrotik.com/docs/display/ROS/WireGuard#WireGuard-IPandroutingconfiguration)
        -   4.1.4[Firewall considerations](https://help.mikrotik.com/docs/display/ROS/WireGuard#WireGuard-Firewallconsiderations)
-   5[RoadWarrior WireGuard tunnel](https://help.mikrotik.com/docs/display/ROS/WireGuard#WireGuard-RoadWarriorWireGuardtunnel)
    -   5.1[RouterOS configuration](https://help.mikrotik.com/docs/display/ROS/WireGuard#WireGuard-RouterOSconfiguration)
    -   5.2[iOS configuration](https://help.mikrotik.com/docs/display/ROS/WireGuard#WireGuard-iOSconfiguration)
    -   5.3[Windows 10 configuration](https://help.mikrotik.com/docs/display/ROS/WireGuard#WireGuard-Windows10configuration)

WireGuard<sup>®</sup> is an extremely simple yet fast and modern VPN that utilizes state-of-the-art cryptography. It aims to be faster, simpler, leaner, and more useful than IPsec while avoiding massive headaches. It intends to be considerably more performant than OpenVPN. WireGuard is designed as a general-purpose VPN for running on embedded interfaces and super computers alike, fit for many different circumstances. Initially released for the Linux kernel, it is now cross-platform (Windows, macOS, BSD, iOS, Android) and widely deployable.

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

|                                                     |
| --------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| **comment** (_string_; Default: )                   | Short description of the tunnel.                                                                    |
| **disabled** (_yes                                  | no_; Default: **no**)                                                                               | Enables/disables the tunnel. |
| **listen-port** (_integer; Default: 13231_)         | Port for WireGuard service to listen on for incoming sessions.                                      |
| **mtu** (_integer \[0..65536\]_; Default: **1420**) | Layer3 Maximum transmission unit.                                                                   |
| **name** (_string_; Default: )                      | Name of the tunnel.                                                                                 |
| **private-key** (_string_; Default: )               | A base64 private key. If not specified, it will be automatically generated upon interface creation. |

## Read-only properties

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
| ------------------------- | ------------------------------------------------------- |
| **public-key** (_string_) | A base64 public key is calculated from the private key. |
| **running** (_yes         | no_)                                                    |

Whether the interface is running.

 |

# Peers

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

|                                                           |
| --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **allowed-address** (_IP/IPv6 prefix_; Default: )         | List of IP (v4 or v6) addresses with CIDR masks from which incoming traffic for this peer is allowed and to which outgoing traffic for this peer is directed. The catch-all _0.0.0.0/0_ may be specified for matching all IPv4 addresses, and _::/0_ may be specified for matching all IPv6 addresses.                                                                                                                         |
| **comment** (_string_; Default: )                         | Short description of the peer.                                                                                                                                                                                                                                                                                                                                                                                                 |
| **disabled** (_yes                                        | no_; Default: **no**)                                                                                                                                                                                                                                                                                                                                                                                                          | Enables/disables the peer. |
| **endpoint-address** (_IP/Hostname_; Default: )           | An endpoint IP or hostname can be left blank to allow remote connection from any address.                                                                                                                                                                                                                                                                                                                                      |
| **endpoint-port** (_integer:0..65535__; Default:_ )       | An endpoint port can be left blank to allow remote connection from any port.                                                                                                                                                                                                                                                                                                                                                   |
| **interface** (_string; Default:_ )                       | Name of the WireGuard interface the peer belongs to.                                                                                                                                                                                                                                                                                                                                                                           |
| **persistent-keepalive** (_integer:0..65535; Default: 0_) | A seconds interval, between 1 and 65535 inclusive, of how often to send an authenticated empty packet to the peer for the purpose of keeping a stateful firewall or NAT mapping valid persistently. For example, if the interface very rarely sends traffic, but it might at anytime receive traffic from a peer, and it is behind NAT, the interface might benefit from having a persistent keepalive interval of 25 seconds. |
| **preshared-key** (_string; Default:_ )                   | A base64 preshared key. Optional, and may be omitted. This option adds an additional layer of symmetric-key cryptography to be mixed into the already existing public-key cryptography, for post-quantum resistance.                                                                                                                                                                                                           |
| **public-key** (_string; Default:_ )                      | The remote peer's calculated public key.                                                                                                                                                                                                                                                                                                                                                                                       |

## Read-only properties

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
| ---------------------------------------- | ----------------------------------------------------------------------------------- |
| **current-endpoint-address** (_IP/IPv6_) | The most recent source IP address of correctly authenticated packets from the peer. |
| **current-endpoint-port** (_integer_)    | The most recent source IP port of correctly authenticated packets from the peer.    |
| **last-handshake** (i_nteger_)           | Time in seconds after the last successful handshake.                                |
| **rx** (_integer_)                       | The total amount of bytes received from the peer.                                   |
| **tx** (_integer_)                       | The total amount of bytes transmitted to the peer.                                  |

# Application examples

## Site to Site WireGuard tunnel

Consider setup as illustrated below. Two remote office routers are connected to the internet and office workstations are behind NAT. Each office has its own local subnet, 10.1.202.0/24 for Office1 and 10.1.101.0/24 for Office2. Both remote offices need secure tunnels to local networks behind routers.

![](https://help.mikrotik.com/docs/download/attachments/69664792/Site-to-site-ipsec-example.png?version=1&modificationDate=1622538715602&api=v2)

### WireGuard interface configuration

First of all, WireGuard interfaces must be configured on both sites to allow automatic private and public key generation. The command is the same for both routers:

[?](https://help.mikrotik.com/docs/display/ROS/WireGuard#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface/wireguard</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">listen-port</code><code class="ros plain">=13231</code> <code class="ros value">name</code><code class="ros plain">=wireguard1</code></div></div></td></tr></tbody></table>

Now when printing the interface details, both private and public keys should be visible to allow an exchange.

Any private key will never be needed on the remote side device - hence the name private.

**Office1**

[?](https://help.mikrotik.com/docs/display/ROS/WireGuard#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface/wireguard </code><code class="ros functions">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disabled; R - running</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">0&nbsp; R </code><code class="ros value">name</code><code class="ros plain">=</code><code class="ros string">"wireguard1"</code> <code class="ros value">mtu</code><code class="ros plain">=1420</code> <code class="ros value">listen-port</code><code class="ros plain">=13231</code> <code class="ros value">private-key</code><code class="ros plain">=</code><code class="ros string">"yKt9NJ4e5qlaSgh48WnPCDCEkDmq+VsBTt/DDEBWfEo="</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">public-key</code><code class="ros plain">=</code><code class="ros string">"u7gYAg5tkioJDcm3hyS7pm79eADKPs/ZUGON6/fF3iI="</code></div></div></td></tr></tbody></table>

**Office2**

[?](https://help.mikrotik.com/docs/display/ROS/WireGuard#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface/wireguard/</code><code class="ros functions">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disabled; R - running</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">0&nbsp; R </code><code class="ros value">name</code><code class="ros plain">=</code><code class="ros string">"wireguard1"</code> <code class="ros value">mtu</code><code class="ros plain">=1420</code> <code class="ros value">listen-port</code><code class="ros plain">=13231</code> <code class="ros value">private-key</code><code class="ros plain">=</code><code class="ros string">"KMwxqe/iXAU8Jn9dd1o5pPdHep2blGxNWm9I944/I24="</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">public-key</code><code class="ros plain">=</code><code class="ros string">"v/oIzPyFm1FPHrqhytZgsKjU7mUToQHLrW+Tb5e601M="</code></div></div></td></tr></tbody></table>

### Peer configuration

Peer configuration defines who can use the WireGuard interface and what kind of traffic can be sent over it. To identify the remote peer, its public key must be specified together with the created WireGuard interface.

**Office1**

[?](https://help.mikrotik.com/docs/display/ROS/WireGuard#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface/wireguard/peers</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">allowed-address</code><code class="ros plain">=10.1.101.0/24</code> <code class="ros value">endpoint-address</code><code class="ros plain">=192.168.80.1</code> <code class="ros value">endpoint-port</code><code class="ros plain">=13231</code> <code class="ros value">interface</code><code class="ros plain">=wireguard1</code> <code class="ros plain">\</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros value">public-key</code><code class="ros plain">=</code><code class="ros string">"v/oIzPyFm1FPHrqhytZgsKjU7mUToQHLrW+Tb5e601M="</code></div></div></td></tr></tbody></table>

**Office2**

[?](https://help.mikrotik.com/docs/display/ROS/WireGuard#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface/wireguard/peers</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">allowed-address</code><code class="ros plain">=10.1.202.0/24</code> <code class="ros value">endpoint-address</code><code class="ros plain">=192.168.90.1</code> <code class="ros value">endpoint-port</code><code class="ros plain">=13231</code> <code class="ros value">interface</code><code class="ros plain">=wireguard1</code> <code class="ros plain">\</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros value">public-key</code><code class="ros plain">=</code><code class="ros string">"u7gYAg5tkioJDcm3hyS7pm79eADKPs/ZUGON6/fF3iI="</code></div></div></td></tr></tbody></table>

### IP and routing configuration

Lastly, IP and routing information must be configured to allow traffic to be sent over the tunnel.

**Office1**

[?](https://help.mikrotik.com/docs/display/ROS/WireGuard#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip/address</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=10.255.255.1/30</code> <code class="ros value">interface</code><code class="ros plain">=wireguard1</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/ip/route</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">dst-address</code><code class="ros plain">=10.1.101.0/24</code> <code class="ros value">gateway</code><code class="ros plain">=wireguard1</code></div></div></td></tr></tbody></table>

**Office2**

[?](https://help.mikrotik.com/docs/display/ROS/WireGuard#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip/address</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=10.255.255.2/30</code> <code class="ros value">interface</code><code class="ros plain">=wireguard1</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/ip/route</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">dst-address</code><code class="ros plain">=10.1.202.0/24</code> <code class="ros value">gateway</code><code class="ros plain">=wireguard1</code></div></div></td></tr></tbody></table>

### Firewall considerations

The default RouterOS firewall will block the tunnel from establishing properly. The traffic should be accepted in the "input" chain before any drop rules on both sites.

**Office1**

[?](https://help.mikrotik.com/docs/display/ROS/WireGuard#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip/firewall/filter</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=accept</code> <code class="ros value">chain</code><code class="ros plain">=input</code> <code class="ros value">dst-port</code><code class="ros plain">=13231</code> <code class="ros value">protocol</code><code class="ros plain">=udp</code> <code class="ros value">src-address</code><code class="ros plain">=192.168.80.1</code></div></div></td></tr></tbody></table>

**Office2**

[?](https://help.mikrotik.com/docs/display/ROS/WireGuard#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip/firewall/filter</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=accept</code> <code class="ros value">chain</code><code class="ros plain">=input</code> <code class="ros value">dst-port</code><code class="ros plain">=13231</code> <code class="ros value">protocol</code><code class="ros plain">=udp</code> <code class="ros value">src-address</code><code class="ros plain">=192.168.90.1</code></div></div></td></tr></tbody></table>

Additionally, it is possible that the "forward" chain restricts the communication between the subnets as well, so such traffic should be accepted before any drop rules as well.

**Office1**

[?](https://help.mikrotik.com/docs/display/ROS/WireGuard#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip/firewall/filter</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=accept</code> <code class="ros value">chain</code><code class="ros plain">=forward</code> <code class="ros value">dst-address</code><code class="ros plain">=10.1.202.0/24</code> <code class="ros value">src-address</code><code class="ros plain">=10.1.101.0/24</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=accept</code> <code class="ros value">chain</code><code class="ros plain">=forward</code> <code class="ros value">dst-address</code><code class="ros plain">=10.1.101.0/24</code> <code class="ros value">src-address</code><code class="ros plain">=10.1.202.0/24</code></div></div></td></tr></tbody></table>

**Office2**

[?](https://help.mikrotik.com/docs/display/ROS/WireGuard#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip/firewall/filter</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=accept</code> <code class="ros value">chain</code><code class="ros plain">=forward</code> <code class="ros value">dst-address</code><code class="ros plain">=10.1.101.0/24</code> <code class="ros value">src-address</code><code class="ros plain">=10.1.202.0/24</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=accept</code> <code class="ros value">chain</code><code class="ros plain">=forward</code> <code class="ros value">dst-address</code><code class="ros plain">=10.1.202.0/24</code> <code class="ros value">src-address</code><code class="ros plain">=10.1.101.0/24</code></div></div></td></tr></tbody></table>

# RoadWarrior WireGuard tunnel

## RouterOS configuration

Add a new WireGuard interface and assign an IP address to it.

[?](https://help.mikrotik.com/docs/display/ROS/WireGuard#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface wireguard</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">listen-port</code><code class="ros plain">=13231</code> <code class="ros value">name</code><code class="ros plain">=wireguard1</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/ip address</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=192.168.100.1/24</code> <code class="ros value">interface</code><code class="ros plain">=wireguard1</code></div></div></td></tr></tbody></table>

Adding a new WireGuard interface will automatically generate a pair of private and public keys. You will need to configure the public key on your remote devices. To obtain the public key value, simply print out the interface details.

[?](https://help.mikrotik.com/docs/display/ROS/WireGuard#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@home] &gt; </code><code class="ros constants">/interface wireguard </code><code class="ros functions">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disabled; R - running</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">0&nbsp; R </code><code class="ros value">name</code><code class="ros plain">=</code><code class="ros string">"wireguard1"</code> <code class="ros value">mtu</code><code class="ros plain">=1420</code> <code class="ros value">listen-port</code><code class="ros plain">=13231</code> <code class="ros value">private-key</code><code class="ros plain">=</code><code class="ros string">"cBPD6JNvbEQr73gJ7NmwepSrSPK3np381AWGvBk/QkU="</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">public-key</code><code class="ros plain">=</code><code class="ros string">"VmGMh+cwPdb8//NOhuf1i1VIThypkMQrKAO9Y55ghG8="</code></div></div></td></tr></tbody></table>

For the next steps, you will need to figure out the public key of the remote device. Once you have it, add a new peer by specifying the public key of the remote device and allowed addresses that will be allowed over the WireGuard tunnel.

[?](https://help.mikrotik.com/docs/display/ROS/WireGuard#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface wireguard peers</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">allowed-address</code><code class="ros plain">=192.168.100.2/32</code> <code class="ros value">interface</code><code class="ros plain">=wireguard1</code> <code class="ros value">public-key</code><code class="ros plain">=</code><code class="ros string">"&lt;paste public key from remote device here&gt;"</code></div></div></td></tr></tbody></table>

**Firewall considerations**

If you have default or strict firewall configured, you need to allow remote device to establish the WireGuard connection to your device.

[?](https://help.mikrotik.com/docs/display/ROS/WireGuard#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip firewall filter</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=accept</code> <code class="ros value">chain</code><code class="ros plain">=input</code> <code class="ros value">comment</code><code class="ros plain">=</code><code class="ros string">"allow WireGuard"</code> <code class="ros value">dst-port</code><code class="ros plain">=13231</code> <code class="ros value">protocol</code><code class="ros plain">=udp</code> <code class="ros value">place-before</code><code class="ros plain">=1</code></div></div></td></tr></tbody></table>

To allow remote devices to connect to the RouterOS services (e.g. request DNS), allow the WireGuard subnet in input chain.

[?](https://help.mikrotik.com/docs/display/ROS/WireGuard#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip firewall filter</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=accept</code> <code class="ros value">chain</code><code class="ros plain">=input</code> <code class="ros value">comment</code><code class="ros plain">=</code><code class="ros string">"allow WireGuard traffic"</code> <code class="ros value">src-address</code><code class="ros plain">=192.168.100.0/24</code> <code class="ros value">place-before</code><code class="ros plain">=1</code></div></div></td></tr></tbody></table>

Or simply add the WireGuard interface to "LAN" interface list.

[?](https://help.mikrotik.com/docs/display/ROS/WireGuard#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface list member</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=wireguard1</code> <code class="ros value">list</code><code class="ros plain">=LAN</code></div></div></td></tr></tbody></table>

## iOS configuration

Download the WireGuard application from the App Store. Open it up and create a new configuration from scratch.

![](https://help.mikrotik.com/docs/download/attachments/69664792/IMG_4392.PNG?version=1&modificationDate=1655382066647&api=v2)

First of all give your connection a "Name" and choose to generate a keypair. The generated public key is necessary for peer's configuration on RouterOS side.

**![](https://help.mikrotik.com/docs/download/attachments/69664792/IMG_4393.PNG?version=1&modificationDate=1655382081378&api=v2)  
**

Specify an IP address in "Addresses" field that is in the same subnet as configured on the server side. This address will be used for communication. For this example, we used 192.168.100.1/24 on the RouterOS side, you can use 192.168.100.2 here.

If necessary, configure the DNS servers. If allow-remote-requests is set to yes under IP/DNS section on the RouterOS side, you can specify the remote WireGuard IP address here.

**![](https://help.mikrotik.com/docs/download/attachments/69664792/IMG_4394.PNG?version=1&modificationDate=1655382092515&api=v2)  
**

Click "Add peer" which reveals more parameters.

The "Public key" value is the public key value that is generated on the WireGuard interface on RouterOS side.

"Endpoint" is the IP or DNS with port number of the RouterOS device that the iOS device can communicate with over the Internet.

"Allowed IPs" are set to 0.0.0.0/0 to allow all traffic to be sent over the WireGuard tunnel.

![](https://help.mikrotik.com/docs/download/attachments/69664792/IMG_4396.PNG?version=1&modificationDate=1655382100586&api=v2)

## Windows 10 configuration

Download WireGuard installer from Wireguard  
Run as Administrator.

![](https://help.mikrotik.com/docs/download/attachments/69664792/test.png?version=1&modificationDate=1679667322504&api=v2)

Press Ctrl+n to add new empty tunnel, add name for interface, Public key should be auto generated copy it to RouterOS peer configuration.  
Add to server configuration, so full configuration looks like this (keep your auto generated PrivateKey in \[Interface\] section:

呈现代码宏出错: 参数'com.atlassian.confluence.ext.code.render.InvalidValueException'的值无效

```
[Interface]
PrivateKey = your_autogenerated_public_key=
Address = 192.168.100.3/24
DNS = 192.168.100.1

[Peer]
PublicKey = your_MikroTik_public_KEY=
AllowedIPs = 0.0.0.0/0
Endpoint = example.com:13231
```

  
Save and Activate