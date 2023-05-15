# Summary

**Sub-menu:** `/interface 6to4`

6to4 is a special mechanism that allows IPv6 packets to be transmitted over IPv4 networks without the need of explicitly configured tunnel interfaces. It is especially useful for connecting two or more IPv6 networks over a network that does not have IPv6 support. There are two different ways of 6to4 mechanism. If _remote-address_ is not configured, the router will encapsulate and send an IPv6 packet directly over IPv4 if the first 16 bits are _2002_, using the next 32 bits as the destination (IPv4 address converted to hex). In other case, the IPv6 packet will be sent directly to the IPv4 _remote-address_.

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

|                                                                            |
| -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **clamp-tcp-mss** (_yes                                                    | no_; Default: **yes**)                                                                                                                                                                                                                                                                                                                                                                                                                                  | Controls whether to change MSS size for received TCP SYN packets. When enabled, a router will change the MSS size for received TCP SYN packets if the current MSS size exceeds the tunnel interface MTU (taking into account the TCP/IP overhead). The received encapsulated packet will still contain the original MSS, and only after decapsulation the MSS is changed. |
| **comment** (_string_; Default: )                                          | Short description of the interface.                                                                                                                                                                                                                                                                                                                                                                                                                     |
| **disabled** (_yes                                                         | no_; Default: **no**)                                                                                                                                                                                                                                                                                                                                                                                                                                   | Whether an item is disabled.                                                                                                                                                                                                                                                                                                                                              |
| **dont-fragment** (_inherit                                                | no_; Default: **no**)                                                                                                                                                                                                                                                                                                                                                                                                                                   | Whether to include DF bit in related packets.                                                                                                                                                                                                                                                                                                                             |
| **dscp** (_integer: 0-63_; Default: **inherited**)                         | DSCP value of packet. Inherited option means that DSCP value will be inherited from packet which is going to be encapsulated.                                                                                                                                                                                                                                                                                                                           |
| **ipsec-secret** (_string_; Default: )                                     | When secret is specified, router adds dynamic IPsec peer to remote-address with pre-shared key and policy (by default phase2 uses sha1/aes128cbc).                                                                                                                                                                                                                                                                                                      |
| **keepalive** (_integer\[/time\],integer 0..4294967295_; Default: **0,0**) | Tunnel keepalive parameter sets the time interval in which the tunnel running flag will remain even if the remote end of tunnel goes down. If configured time,retries fail, interface running flag is removed. Parameters are written in following format: `KeepaliveInterval,KeepaliveRetries` where `KeepaliveInterval` is time interval and `KeepaliveRetries` - number of retry attempts. By default keepalive is set to 10 seconds and 10 retries. |
| **local-address** (_IP_; Default: )                                        | Source address of the packets, local on the router.                                                                                                                                                                                                                                                                                                                                                                                                     |
| **mtu** (_integer_; Default: **auto**)                                     | Layer3 maximum transmission unit.                                                                                                                                                                                                                                                                                                                                                                                                                       |
| **name** (_string_; Default: )                                             | Interface name.                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| **remote-address** (_IP_; Default: )                                       | IP address of remote end of 6to4 tunnel. If left unspecified, IPv4 address from 2002::/16 gateway address will be derived.                                                                                                                                                                                                                                                                                                                              |

# Configuration Examples

## Simple 6to4 tunnel encapsulation (Currently not working)

![](https://help.mikrotik.com/docs/download/attachments/135004174/6to4-tunnel.jpg?version=1&modificationDate=1656683221465&api=v2)

It is possible to simply route IPv6 packets over IPv4 network by utilizing the 2002::/16 allocated address space. All 6to4 nodes has to have reachable IPv4 addresses - if you are running this setup over the Internet, all IPv4's must be public addresses.

**R1 configuration:**

Create the 6to4 tunnel interface:

[?](https://help.mikrotik.com/docs/display/ROS/6to4#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface 6to4</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=6to4-tunnel1</code></div></div></td></tr></tbody></table>

Assign an IPv6 address with '2002' as the first 16 bits and IPv4 in hex format as the next 32 bits. For example, if the router's IP address is 10.0.1.1, the IPv6 address is 2002:A00:101::

[?](https://help.mikrotik.com/docs/display/ROS/6to4#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ipv6 address</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=2002:a00:101::/128</code> <code class="ros value">advertise</code><code class="ros plain">=no</code> <code class="ros value">interface</code><code class="ros plain">=6to4-tunnel1</code></div></div></td></tr></tbody></table>

Add a route to specially allocated 6to4 tunnel range over the 6to4-tunnel interface.

[?](https://help.mikrotik.com/docs/display/ROS/6to4#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ipv6 route</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">dst-address</code><code class="ros plain">=2002::/16</code> <code class="ros value">gateway</code><code class="ros plain">=6to4-tunnel1</code></div></div></td></tr></tbody></table>

**R2 configuration:**

Create the 6to4 tunnel interface:

[?](https://help.mikrotik.com/docs/display/ROS/6to4#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface 6to4</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=6to4-tunnel1</code></div></div></td></tr></tbody></table>

Assign an IPv6 address that is generated by the same principles as R1. In this case, 10.0.2.1 translates to 2002:A00:201::

[?](https://help.mikrotik.com/docs/display/ROS/6to4#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ipv6 address</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=2002:a00:201::/128</code> <code class="ros value">advertise</code><code class="ros plain">=no</code> <code class="ros value">interface</code><code class="ros plain">=6to4-tunnel1</code></div></div></td></tr></tbody></table>

The 6to4 route is necessary on this side as well.

[?](https://help.mikrotik.com/docs/display/ROS/6to4#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ipv6 route</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">dst-address</code><code class="ros plain">=2002::/16</code> <code class="ros value">gateway</code><code class="ros plain">=6to4-tunnel1</code></div></div></td></tr></tbody></table>

**Testing:**

After configuring both devices, it should be possible to ping the IPv6 addresses if they were generated correctly.

From R1:

[?](https://help.mikrotik.com/docs/display/ROS/6to4#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/</code><code class="ros functions">ping </code><code class="ros plain">2002</code><code class="ros constants">:a00:201::</code></div></div></td></tr></tbody></table>

## Hurricane Electric Tunnel Broker Example

Following example will show how to get IPv6 connectivity on a RouterOS device through IPv4 network using 6to4 tunnel.

To be able to create the tunnel, you have to have a public IPv4 address and enable ping from Tunnel Broker IPv4 server.

When you create a tunnel using [Hurricane Electric Tunnel Broker](https://tunnelbroker.net), you will be given a routed /64 IPv6 prefix and additional information necessary for setting up the tunnel.

_![](https://help.mikrotik.com/docs/download/attachments/135004174/TunnelBrokerIPv6.png?version=1&modificationDate=1656679624575&api=v2)_

_This example presumes that your public IPv4 address is 194.105.56.170_

Hurricane Electric provides ready to use commands for RouterOS in the 'Example Configurations' section:

[?](https://help.mikrotik.com/docs/display/ROS/6to4#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface 6to4</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">comment</code><code class="ros plain">=</code><code class="ros string">"Hurricane Electric IPv6 Tunnel Broker"</code> <code class="ros value">disabled</code><code class="ros plain">=no</code> <code class="ros value">local-address</code><code class="ros plain">=194.105.56.170</code> <code class="ros value">mtu</code><code class="ros plain">=1280</code> <code class="ros value">name</code><code class="ros plain">=sit1</code> <code class="ros value">remote-address</code><code class="ros plain">=216.66.80.90</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/ipv6 route</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">comment</code><code class="ros plain">=</code><code class="ros string">""</code> <code class="ros value">disabled</code><code class="ros plain">=no</code> <code class="ros value">distance</code><code class="ros plain">=1</code> <code class="ros value">dst-address</code><code class="ros plain">=2000::/3</code> <code class="ros value">gateway</code><code class="ros plain">=2001:470:27:37e::1</code> <code class="ros value">scope</code><code class="ros plain">=30</code> <code class="ros value">target-scope</code><code class="ros plain">=10</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros constants">/ipv6 address</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=2001:470:27:37e::2/64</code> <code class="ros value">advertise</code><code class="ros plain">=no</code> <code class="ros value">disabled</code><code class="ros plain">=no</code> <code class="ros value">eui-64</code><code class="ros plain">=no</code> <code class="ros value">interface</code><code class="ros plain">=sit1</code></div></div></td></tr></tbody></table>

These commands will setup the tunnel itself - the router will be able to connect to IPv6 hosts, but end-user devices (computers, tablets, phones) will not yet have IPv6 connectivity.

To be able to assign IPv6 addresses to your clients you have to add the Routed IPv6 Prefix to your internal interface (by default bridge-local).

[?](https://help.mikrotik.com/docs/display/ROS/6to4#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ipv6 address </code><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=2001:470:28:37e::</code> <code class="ros value">interface</code><code class="ros plain">=bridge-local</code> <code class="ros value">advertise</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

Enable DNS server advertising through network discovery

[?](https://help.mikrotik.com/docs/display/ROS/6to4#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ipv6 nd </code><code class="ros functions">set </code><code class="ros plain">[ </code><code class="ros functions">find </code><code class="ros value">default</code><code class="ros plain">=yes</code> <code class="ros plain">] </code><code class="ros value">advertise-dns</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

And finally add IPv6 DNS servers (these are Google public DNS servers, you can also use the one which is provided by Hurricane Electric - 2001:470:20::2).

[?](https://help.mikrotik.com/docs/display/ROS/6to4#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip dns </code><code class="ros functions">set </code><code class="ros value">allow-remote-requests</code><code class="ros plain">=yes</code> <code class="ros value">servers</code><code class="ros plain">=2001:4860:4860::8888,2001:4860:4860::8844</code></div></div></td></tr></tbody></table>

Afterwards enable IPv6 on your device and you should have IPv6 connectivity. [http://ipv6-test.com](http://ipv6-test.com) can be used to test IPv6 connectivity.