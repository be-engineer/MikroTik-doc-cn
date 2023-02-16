# Introduction

![](https://help.mikrotik.com/docs/download/attachments/328229/firewall-fundamental.jpg?version=2&modificationDate=1572439380369&api=v2)

The firewall implements stateful (by utilizing connection tracking) and stateless packet filtering and thereby provides security functions that are used to manage data flow to, from, and through the router. Along with the Network Address Translation (NAT), it serves as a tool for preventing unauthorized access to directly attached networks and the router itself as well as a filter for outgoing traffic.

Network firewalls keep outside threats away from sensitive data available inside the network. Whenever different networks are joined together, there is always a threat that someone from outside of your network will break into your LAN. Such break-ins may result in private data being stolen and distributed, valuable data being altered or destroyed, or entire hard drives being erased. Firewalls are used as a means of preventing or minimizing the security risks inherent in connecting to other networks. A properly configured firewall plays a key role in efficient and secure network infrastructure deployment.

MikroTik RouterOS has a very powerful firewall implementation with features including:

- stateful packet inspection
- peer-to-peer protocols filtering
- traffic classification by:
  - source MAC address
  - IP addresses (network or list) and address types (broadcast, local, multicast, unicast)
  - port or port range
  - IP protocols
  - protocol options (ICMP type and code fields, TCP flags, IP options, and MSS)
  - interface the packet arrived from or left through
  - internal flow and connection marks
  - DSCP byte
  - packet content
  - rate at which packets arrive and sequence numbers
  - packet size
  - packet arrival time

And much more!

## How It works

The firewall operates by means of firewall rules. Each rule consists of two parts - the **matcher** which matches traffic flow against given conditions and the **action** which defines what to do with the matched packet.

RouterOS utilizes 5 sub-facilities of the firewall:

- Connection tracking
- Filters
- NAT
- Mangle
- RAW

### Connection states

To completely understand firewall rules, first, you have to understand various states which might apply to a particular network packet. There are five connection states in RouterOS:

- **NEW** - The NEW state tells us that the packet is the first packet that we see. This means that the first packet that the conntrack module sees, within a specific connection, will be matched. For example, if we see an SYN packet and it is the first packet in a connection that we see, it will match;
- **ESTABLISHED -** The _ESTABLISHED_ state has seen traffic in both directions and will then continuously match those packets. _ESTABLISHED_ connections are fairly easy to understand. The only requirement to get into an _ESTABLISHED_ state is that one host sends a packet and that it, later on, gets a reply from the other host. The _NEW_ state will upon receipt of the reply packet to or through the firewall change to the _ESTABLISHED_ state;
- **RELATED** \- A connection is considered _RELATED_ when it is related to another already _ESTABLISHED_ connection. For a connection to be considered as _RELATED,_ we must first have a connection that is considered _ESTABLISHED._ The _ESTABLISHED_ connection will then spawn a connection outside of the main connection. The newly spawned connection will then be considered _RELATED,_ for example, a packet that begins the FTP data connection;
- **INVALID** \- The _INVALID_ state means that the packet can't be identified or that it does not have any state.  It is suggested to _DROP_ everything in this state;
- **UNTRACKED** \- A packet that was set to bypass connection tracking in the Firewall RAW table;

  

### Configuration Example

Let's look at the basic firewall setup to protect the router. By default RouterOS firewall accepts everything, blocking is achieved by adding a filter rule to drop everything at the end of all rules. For out router we want to allow only ICMP, ssh, and Winbox and drop the rest:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip firewall filter</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">chain</code><code class="ros plain">=input</code> <code class="ros value">connection-state</code><code class="ros plain">=invalid</code> <code class="ros value">action</code><code class="ros plain">=drop</code> <code class="ros value">comment</code><code class="ros plain">=</code><code class="ros string">"Drop Invalid connections"</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">chain</code><code class="ros plain">=input</code> <code class="ros value">connection-state</code><code class="ros plain">=established,related,untracked</code> <code class="ros value">action</code><code class="ros plain">=accept</code> <code class="ros value">comment</code><code class="ros plain">=</code><code class="ros string">"Allow Established/Related/Untracked connections"</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">chain</code><code class="ros plain">=input</code> <code class="ros value">protocol</code><code class="ros plain">=icmp</code> <code class="ros value">action</code><code class="ros plain">=accept&nbsp;</code><code class="ros plain">;</code><code class="ros value">comment</code><code class="ros plain">=</code><code class="ros string">"Allow ICMP"</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">chain</code><code class="ros plain">=input</code> <code class="ros value">protocol</code><code class="ros plain">=tcp</code> <code class="ros value">ports</code><code class="ros plain">=8291,22</code> <code class="ros value">action</code><code class="ros plain">=accept</code> <code class="ros value">comment</code><code class="ros plain">=</code><code class="ros string">"Allow Winbox and SSH"</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">chain</code><code class="ros plain">=input</code> <code class="ros value">action</code><code class="ros plain">=drop</code> <code class="ros value">comment</code><code class="ros plain">=</code><code class="ros string">"Drop everything else"</code></div></div></td></tr></tbody></table>

RouterOS also allows filtering packets before connection tracking and selectively send only specific traffic to connection tracking. This allows us to significantly reduce the load on the CPU and mitigate DOS/DDoS attacks. Configuration of such rules is done in the RAW filtering table.

Additional _/ip firewall filter_ configuration examples find under the [Building Your First Firewall](https://help.mikrotik.com/docs/display/ROS/Building+Your+First+Firewall) section.

## Connection Tracking

Connection tracking allows the kernel to keep track of all logical network connections or sessions, and thereby relate all of the packets which may make up that connection. NAT relies on this information to translate all related packets in the same way. Because of connection tracking, you can use stateful firewall functionality even with stateless protocols such as UDP.

A list of tracked connections can be seen in the _/ip firewall connection_ for ipv4 and _/ipv6 firewall connection_ for IPv6.

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MirkoTik] </code><code class="ros constants">/ip firewall connection&gt; </code><code class="ros plain">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: S - seen-reply, A - assured</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros comments"># PR.. SRC-ADDRESS DST-ADDRESS TCP-STATE TIMEOUT</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">0 udp 10.5.8.176</code><code class="ros constants">:5678 255.255.255.255:5678 0s</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">1 udp 10.5.101.3</code><code class="ros constants">:646 224.0.0.2:646 5s</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">2 ospf 10.5.101.161 224.0.0.5 9m58s</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">3 udp 10.5.8.140</code><code class="ros constants">:5678 255.255.255.255:5678 8s</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros plain">4 SA tcp 10.5.101.147</code><code class="ros constants">:48984 10.5.101.1:8291 established 4m59s</code></div><div class="line number9 index8 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros plain">[admin@MirkoTik] </code><code class="ros constants">/ipv6 firewall connection&gt; </code><code class="ros plain">print</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: S - seen reply, A - assured</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros comments"># PRO.. SRC-ADDRESS DST-ADDRESS TCP-STATE</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="ros plain">0 udp fe80</code><code class="ros constants">::d6ca:6dff:fe77:3698 ff02::1</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="ros plain">1 udp fe80</code><code class="ros constants">::d6ca:6dff:fe98:7c28 ff02::1</code></div><div class="line number15 index14 alt2" data-bidi-marker="true"><code class="ros plain">2 ospf fe80</code><code class="ros constants">::d6ca:6dff:fe73:9822 ff02::5</code></div></div></td></tr></tbody></table>

  
Based on connection table entries arrived packet can get assigned one of the connection states: **new, invalid, established, related,** or **untracked**.

There are two different methods when the packet is considered **new**. The first one is in the case of stateless connections (like UDP) when there is no connection entry in the connection table. The other one is in the case of a stateful protocol (TCP). In this case, a new packet that starts a new connection is always a TCP packet with an _SYN_ flag.

If a packet is not new it can belong to either an _established_ or _related_ connection or not belong to any connection making it _invalid_. A packet with an _established_ state, as most of you already guessed, belongs to an existing connection from the connection tracking table. A _related_ state is very similar, except that packet belongs to a connection that is related to one of the existing connections, for example, ICMP error packets or FTP data connection packets.

Connection state **notrack** is a special case when RAW firewall rules are used to exclude connection from connection tracking. This one rule would make all forwarded traffic bypass the connection tracking engine speeding packet processing through the device.

Any other packet is considered _invalid_ and in most cases should be dropped.

Based on this information we can set a basic set of filter rules to speed up packet filtering and reduce the load on the CPU by accepting _established/related_ packets, dropping _invalid_ packets, and working on more detailed filtering only for _new_ packets.

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">ip firewall filter</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">chain</code><code class="ros plain">=input</code> <code class="ros value">connection-state</code><code class="ros plain">=invalid</code> <code class="ros value">action</code><code class="ros plain">=drop</code> <code class="ros value">comment</code><code class="ros plain">=</code><code class="ros string">"Drop Invalid connections"</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">chain</code><code class="ros plain">=input</code> <code class="ros value">connection-state</code><code class="ros plain">=established,related,untracked</code> <code class="ros value">action</code><code class="ros plain">=accept</code> <code class="ros value">comment</code><code class="ros plain">=</code><code class="ros plain">"Allow Established</code><code class="ros constants">/Related/Untracked connections</code></div></div></td></tr></tbody></table>

Such a rule set must not be applied on routers with asymmetric routing, because asymmetrically routed packets may be considered invalid and dropped.

## FastTrack

IPv4 FastTrack handler is automatically used for marked connections. Use firewall action "fasttrack-connection" to mark connections for FastTrack. Currently, only TCP and UDP connections can be actually FastTracked (even though any connection can be marked for FastTrack). IPv4 FastTrack handler supports NAT (SNAT, DNAT, or both).

Note that not all packets in a connection can be FastTracked, so it is likely to see some packets going through a slow path even though the connection is marked for FastTrack. This is the reason why fasttrack-connection is usually followed by an identical "_action=accept_" rule. FastTrack packets bypass firewall, connection tracking, simple queues, queue tree with _parent=global_, IP accounting, IPSec, hotspot universal client, VRF assignment, so it is up to the administrator to make sure FastTrack does not interfere with other configuration.

### Requirements

IPv4 FastTrack is active if the following conditions are met:

- no mesh, metarouter interface configuration;
- sniffer, torch, or traffic generator is not running;
- _/tool mac-scan_ is not actively used;
- _/tool ip-scan_ is not actively used;
- FastPath and Route cache is enabled under _IP/Settings_

### Example

For example, for SOHO routers with factory default configuration, you could FastTrack all LAN traffic with this one rule placed at the top of the Firewall Filter. The same configuration accept rule is required:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip firewall filter </code><code class="ros functions">add </code><code class="ros value">chain</code><code class="ros plain">=forward</code> <code class="ros value">action</code><code class="ros plain">=fasttrack-connection</code> <code class="ros value">connection-state</code><code class="ros plain">=established,related</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros constants">/ip firewall filter </code><code class="ros functions">add </code><code class="ros value">chain</code><code class="ros plain">=forward</code> <code class="ros value">action</code><code class="ros plain">=accept</code> <code class="ros value">connection-state</code><code class="ros plain">=established,related</code></div></div></td></tr></tbody></table>

- Connection is FastTracked until the connection is closed, timed-out, or router is rebooted.
- Dummy rules will disappear only after FastTrack firewall rules will be deleted/disabled and the router rebooted.
- While FastPath and FastTrack both are enabled on the device only one can be active at a time.

  

Queues (except Queue Trees parented to interfaces), firewall filter, and mangle rules will not be applied for FastTracked traffic.

## Services

This section lists protocols and ports used by various MikroTik RouterOS services. It helps you to determine why your MikroTik router listens to certain ports, and what you need to block/allow in case you want to prevent or grant access to certain services.  

The default services are:

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

 |             |
 | ----------- | ------------------------------------------------------------------------------------ |
 | **telnet**  | Telnet service                                                                       |
 | **ftp**     | FTP service                                                                          |
 | **www**     | Webfig http service                                                                  |
 | **ssh**     | SSH service                                                                          |
 | **www-ssl** | Webfig HTTPS service                                                                 |
 | **api**     | API service                                                                          |
 | **winbox**  | Responsible for Winbox tool access, as well as Tik-App smartphone app and Dude probe |
 | **api-ssl** | API over SSL service                                                                 |

## Properties

Note that it is not possible to add new services, only existing service modifications are allowed.

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

 |                                             |
 | ------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
 | **address** (_IP address/netmask            | IPv6/0..128_; Default: )                                                                                                                | List of IP/IPv6 prefixes from which the service is accessible. |
 | **certificate** (_name_; default: **none**) | The name of the certificate used by a particular service. Applicable only for services that depend on certificates (_www-ssl, api-ssl_) |
 | **name** (_name_; default: **none**)        | Service name                                                                                                                            |
 | **port** (_integer: 1..65535_; Default: )   | The port particular service listens on                                                                                                  |

To restrict Winbox service access to the device only from the **192.168.88.0/24** subnet, we have to configure the following:

```shell
[admin@MikroTik] > ip service set [find name~"winbox"] address=192.168.88.0/24
[admin@MikroTik] > ip service print
Flags: X - disabled, I - invalid
# NAME PORT ADDRESS CERTIFICATE
0 telnet 23
1 XI ftp 21
2 XI www 80
3 ssh 22
4 XI www-ssl 443 none
5 XI api 8728
6 winbox 8291 192.168.88.0/24
7 XI api-ssl 8729 none
```

We recommend disabling unused services.

## Address List

Firewall address lists allow a user to create lists of IP addresses grouped together under a common name. Firewall filter, Mangle, and NAT facilities can then use those address lists to match packets against them. The address list records can also be updated dynamically via the _action=add-src-to-address-list_ or _action=add-dst-to-address-list_ items found in NAT, Mangle, and Filter facilities.  
Firewall rules with action _add-src-to-address-list_ or _add-dst-to-address-list_ works in passthrough mode, which means that the matched packets will be passed to the next firewall rules. A basic example of a dynamically created address-list:

```shell
[admin@MirkoTik] > ip firewall address-list add address=www.mikrotik.com list=MikroTik
[admin@MirkoTik] > ip firewall address-list print
Flags: X - disabled, D - dynamic
# LIST ADDRESS CREATION-TIME TIMEOUT
0 MikroTik www.mikrotik.com oct/09/2019 14:53:14
1 D ;;; www.mikrotik.com
MikroTik 159.148.147.196 oct/09/2019 14:53:14
```

## Layer7-protocol

Layer7-protocol is a method of searching for patterns in ICMP/TCP/UDP streams. It collects the first 10 packets of a connection or the first 2KB of a connection and searches for the pattern in the collected data. If the pattern is not found in the collected data, the matcher stops inspecting further. Allocated memory is freed and the protocol is considered unknown. You should take into account that a lot of connections will significantly increase memory and CPU usage. To avoid this, add regular firewall matches to reduce the amount of data passed to layer-7 filters repeatedly.

An additional requirement is that the layer7 matcher must see both directions of traffic (incoming and outgoing). To satisfy this requirement l7 rules should be set in the forward chain. If a rule is set in the input/prerouting chain then the same rule must be also set in the output/postrouting chain, otherwise, the collected data may not be complete resulting in an incorrectly matched pattern.

In this example, we will use a pattern to match RDP packets.

`/ip firewall layer7-protocol add name=rdp regexp="rdpdr.*cliprdr.*rdpsnd"`

If the Layer7 matcher recognizes the connection, then the rule marks this connection as its "own" and other rules do not look at this connection anymore even if the two firewall rules with Layer7 matcher are identical.

When a user uses HTTPS, Layer7 rules will not be able to match this traffic. **Only unencrypted HTTP can be matched**.
