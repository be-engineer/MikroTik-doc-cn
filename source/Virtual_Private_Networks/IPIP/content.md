# Summary

**Sub-menu:** `/interface ipip   **Standards:** [RFC2003](https://tools.ietf.org/html/rfc2003)`

The IPIP tunneling implementation on the MikroTik RouterOS is RFC 2003 compliant. IPIP tunnel is a simple protocol that encapsulates IP packets in IP to make a tunnel between two routers. The IPIP tunnel interface appears as an interface under the interface list. Many routers, including Cisco and Linux, support this protocol. This protocol makes multiple network schemes possible.  
  
IP tunneling protocol adds the following possibilities to a network setup:

-   to tunnel Intranets over the Internet

-   to use it instead of source routing

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

|                                                                               |
| ----------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **clamp-tcp-mss** (_yes                                                       | no_; Default: **yes**)                                                                                                                                                                                                                                                                                                                                                                                                                              | Controls whether to change MSS size for received TCP SYN packets. When enabled, a router will change the MSS size for received TCP SYN packets if the current MSS size exceeds the tunnel interface MTU (taking into account the TCP/IP overhead).The received encapsulated packet will still contain the original MSS, and only after decapsulation the MSS is changed. |
| **dont-fragment** (_inherit                                                   | no_; Default: **no**)                                                                                                                                                                                                                                                                                                                                                                                                                               |
|                                                                               |
| **dscp** (_inherit                                                            | integer \[0-63\]_; Default: )                                                                                                                                                                                                                                                                                                                                                                                                                       | Set dscp value in IPIP header to a fixed value or inherit from dscp value taken from tunnelled traffic                                                                                                                                                                                                                                                                   |
| **ipsec-secret** (_string_; Default: )                                        | When secret is specified, router adds dynamic ipsec peer to remote-address with pre-shared key and policy with default values (by default phase2 uses sha1/aes128cbc).                                                                                                                                                                                                                                                                              |
| **local-address** (_IP_; Default: )                                           | IP address on a router that will be used by IPIP tunnel                                                                                                                                                                                                                                                                                                                                                                                             |
| **mtu** (_integer_; Default: **1500**)                                        | Layer3 Maximum transmission unit                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **keepalive** (_integer\[/time\],integer 0..4294967295_; Default: **10s,10**) | Tunnel keepalive parameter sets the time interval in which the tunnel running flag will remain even if the remote end of tunnel goes down. If configured time,retries fail, interface running flag is removed. Parameters are written in following format: `KeepaliveInterval,KeepaliveRetries` where KeepaliveInterval is time interval and KeepaliveRetries - number of retry attempts. By default keepalive is set to 10 seconds and 10 retries. |
| **name** (_string_; Default: )                                                | Interface name                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| **remote-address** (_IP_; Default: )                                          | IP address of remote end of IPIP tunnel                                                                                                                                                                                                                                                                                                                                                                                                             |

There is no authentication or 'state' for this interface. The bandwidth usage of the interface may be monitored with the monitor feature from the interface menu.

# Example

 Suppose we want to add an IPIP tunnel between routers R1 and R2: 

![](https://help.mikrotik.com/docs/download/attachments/47579173/Ipip-sample.jpg?version=1&modificationDate=1612793622487&api=v2)

At first, we need to configure IPIP interfaces and then add IP addresses to them.  
  
The configuration for router **R1** is as follows:

[?](https://help.mikrotik.com/docs/display/ROS/IPIP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] interface ipip&gt; add</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">local-address</code><code class="ros constants">: 10.0.0.1</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">remote-address</code><code class="ros constants">: 22.63.11.6</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] interface ipip&gt; print</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disabled, R - running</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros comments"># NAME MTU LOCAL-ADDRESS REMOTE-ADDRESS</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">0 X ipip1 1480 10.0.0.1 22.63.11.6</code></div><div class="line number8 index7 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] interface ipip&gt; en 0</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] interface ipip&gt; </code><code class="ros constants">/ip address </code><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=1.1.1.1/24</code> <code class="ros value">interface</code><code class="ros plain">=ipip1</code></div></div></td></tr></tbody></table>

The configuration of the **R2** is shown below:

[?](https://help.mikrotik.com/docs/display/ROS/IPIP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] interface ipip&gt; </code><code class="ros functions">add </code><code class="ros value">local-address</code><code class="ros plain">=22.63.11.6</code> <code class="ros value">remote-address</code><code class="ros plain">=10.</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">0.0.1</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] interface ipip&gt; print</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disabled, R - running</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros comments"># NAME MTU LOCAL-ADDRESS REMOTE-ADDRESS</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">0 X ipip1 1480 22.63.11.6 10.0.0.1</code></div><div class="line number7 index6 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] interface ipip&gt; </code><code class="ros functions">enable </code><code class="ros plain">0</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] interface ipip&gt; </code><code class="ros constants">/ip address </code><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=1.1.1.2/24</code> <code class="ros value">interface</code><code class="ros plain">=ipip1</code></div></div></td></tr></tbody></table>

Now both routers can ping each other: 

[?](https://help.mikrotik.com/docs/display/ROS/IPIP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] interface ipip&gt; </code><code class="ros constants">/</code><code class="ros functions">ping </code><code class="ros plain">1.1.1.2</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">1.1.1.2 64 byte ping</code><code class="ros constants">: ttl=64 time=24 ms</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">1.1.1.2 64 byte ping</code><code class="ros constants">: ttl=64 time=19 ms</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">1.1.1.2 64 byte ping</code><code class="ros constants">: ttl=64 time=20 ms</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">3 packets transmitted, 3 packets received, 0% packet loss</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">round-trip min</code><code class="ros constants">/avg/max = 19/21.0/24 ms</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] interface ipip&gt;</code></div></div></td></tr></tbody></table>