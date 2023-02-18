# 基本概念介绍

![](https://help.mikrotik.com/docs/download/attachments/328229/firewall-fundamental.jpg?version=2&modificationDate=1572439380369&api=v2)

防火墙实现了有状态（通过利用连接跟踪）和无状态数据包过滤，从而提供了安全功能，用于管理进出路由器的数据流。与网络地址转换（NAT）一起，可以防止未经授权访问直接连接的网络和路由器本身的工具，也是出站流量的一个过滤器。

网络防火墙使外部威胁远离网络内部的敏感数据。每当不同的网络连接在一起时，总是有一种威胁，即来自网络之外的人闯入你的局域网。这种闯入可能导致私人数据被盗和传播，有价值的数据被改变或破坏，或整个硬盘被删除。防火墙用作防止或尽量减少连接到其他网络的固有安全风险的手段。正确配置的防火墙在高效和安全的网络基础设施部署中发挥着关键作用。

MikroTik RouterOS有一个非常强大的防火墙，功能包括。

- 状态包检查
- 点对点协议过滤
- 通过以下方式进行流量分类
  - 源MAC地址
  - IP地址（网络或列表）和地址类型（广播、本地、多播、单播）。
  - 端口或端口范围
  - IP协议
  - 协议选项（ICMP类型和代码域、TCP标志、IP选项和MSS）。
  - 数据包到达或离开的接口
  - 内部流量和连接标记
  - DSCP字节
  - 数据包内容
  - 数据包到达的速率和序列号
  - 数据包大小
  - 数据包到达时间

还有更多!

## 它如何工作

防火墙通过防火墙规则运行。每个规则由两部分组成-**匹配器**，根据给定的条件匹配流量，以及 **动作**，定义如何处理匹配的数据包。

RouterOS利用防火墙的5个子功能：

- Connection tracking
- Filters
- NAT
- Mangle
- RAW

### 连接状态

要完全理解防火墙规则，首先必须了解可能适用于特定网络数据包的各种状态。在RouterOS中，有五种连接状态。

- **NEW** - 新状态告诉我们，该数据包是看到的第一个数据包。意味着conntrack模块看到的第一个数据包，在一个特定的连接中被匹配。例如，如果我们看到一个SYN数据包，并且它是看到的一个连接中的第一个数据包，它将被匹配。
- **ESTABLISHED -** _ESTABLISHED_ 状态在两个方向都看到了流量，然后会持续匹配这些数据包。_ESTABLISHED_ 连接是相当容易理解的。进入 _ESTABLISHED_ 状态的唯一要求是一台主机发送了一个数据包，随后它从另一台主机得到了一个回复。在收到回复数据包后，_NEW_ 状态将改变为_ESTABLISHED_ 状态，或通过防火墙。
- **RELATED** - 连接被认为是_RELATED_，当它与另一个已经_ESTABLISHED_ 的连接有关。为了使一个连接被认为是 _RELATED_，必须首先有一个被认为是 _ESTABLISHED_ 的连接，然后 _ESTABLISHED_ 连接将在主连接之外产生一个连接。然后新产生的连接将被认为是 _RELATED_，例如，一个开始FTP数据连接的数据包。
- **INVALID**- _INVALID_ 状态意味着数据包无法被识别，或者没有任何状态。 建议在这种状态下 _DROP_ 一切。
- **UNTRACKED** - 一个数据包设置为绕过防火墙RAW表中的连接跟踪。  

### 配置实例

看一下保护路由器的基本防火墙设置。默认情况下，RouterOS防火墙接受一切，阻断是通过在所有规则的末尾添加一个过滤规则来丢弃一切。对路由器只想允许ICMP、ssh和Winbox，而丢弃其他的。

```shell
/ip firewall filter
add chain=input connection-state=invalid action=drop comment="Drop Invalid connections"
add chain=input connection-state=established,related,untracked action=accept comment="Allow Established/Related/Untracked connections"
add chain=input protocol=icmp action=accept ;comment="Allow ICMP"
add chain=input protocol=tcp ports=8291,22 action=accept comment="Allow Winbox and SSH"
add chain=input action=drop comment="Drop everything else"
```

RouterOS还允许在连接跟踪前过滤数据包，并有选择地只发送特定的流量到连接跟踪。这能够大大减少CPU的负荷，并减轻DOS/DDoS攻击。这种规则的配置是在RAW过滤表中完成的。

额外的 _/ip firewall filter_ 配置例子可在 [建立你的第一个防火墙](https://help.mikrotik.com/docs/display/ROS/Building+Your+First+Firewall) 部分找到。

## 连接跟踪

连接跟踪允许内核跟踪所有的逻辑网络连接或会话，从而将可能构成该连接的所有数据包联系起来。NAT依靠这一信息，以同样的方式翻译所有相关的数据包。连接跟踪可以使用有状态防火墙功能，也可以是无状态协议，如UDP。

跟踪的连接列表可以在ipv4的 _/ip firewall connection_ 和IPv6的 _/ipv6 firewall connection_ 中看到。

```shell
[admin@MirkoTik] /ip firewall connection> print
Flags: S - seen-reply, A - assured
# PR.. SRC-ADDRESS DST-ADDRESS TCP-STATE TIMEOUT
0 udp 10.5.8.176:5678 255.255.255.255:5678 0s
1 udp 10.5.101.3:646 224.0.0.2:646 5s
2 ospf 10.5.101.161 224.0.0.5 9m58s
3 udp 10.5.8.140:5678 255.255.255.255:5678 8s
4 SA tcp 10.5.101.147:48984 10.5.101.1:8291 established 4m59s
```
  
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
