# 概述

**标准：** RFC 2462，RFC 2461，RFC 4861`

Routeros使用路由器广告守护程序（RADVD）具有IPv6邻居发现和无状态地址自动配置支持。

## 节点描述

节点是实现IPv6的设备。 在IPv6网络中，节点分为两种类型：

 -  **路由器**  - 转发IPv6数据包的节点未明确地解决自身。
 -  **主机**  - 任何不是路由器的节点。

路由器和主机严格分开，这意味着路由器不能是主机，并且主机不能同时是路由器。

## 无状态地址自动配置

有几种类型的自动配置：

 -  _stateless_ -地址配置是通过接收路由器广告消息来完成的。 这些消息包括无状态地址前缀，并要求主机不使用状态地址配置协议。
-_stateful _ -地址配置是通过使用状态地址配置协议（DHCPV6）完成的。 如果RA消息不包括地址前缀，则使用状态协议。
 -  _BOTH_ - RA消息包括无状态地址前缀，并要求主机使用状态地址配置协议。

IPv6的一个非常有用的功能是能够在不使用诸如DHCP之类的状态配置协议的情况下自动配置自身([请参阅](https://wiki.mikrotik.com/wiki/wiki/wiki/manual：ipv6/nd#statpateless_autoconfiguration_example))。

**注意：** 地址自动配置只能在具有多播功能的界面上执行。

-IPv6子网前缀
 - 默认路由器链接 - 本地地址
 - 可能是可选的其他参数：链接MTU，默认的HOP限制和路由器寿命。

然后主机捕获广播，配置全局IPv6地址和默认路由器。 全局IPv6地址是由广播 [子网前缀](https://wiki.mikrotik.com/wiki/Manual:IPv6/Address#Prefix"Manual:IPv6/Address") 生成和eui-64 [界面标识符](https://wiki.mikrotik.com/wiki/Manual:IPv6/Address#Interface_Identifier "Manual:IPv6/Address")。

主机可以通过发送ICMPV6“路由器广告”数据包来询问路由器的广播，这是可选的。 在Linux **rtsol** 实用程序传输路由器请求数据包。 如果正在运行移动节点，则可能需要定期发送路由器请求。

### 地址状态

当一个自动配置的地址被分配时，它可以处于以下状态之一：

- **tentative** - 在这种状态下，主机会验证地址是否唯一。验证是通过重复的地址检测进行的。
- **preferred** - 在此状态下，地址被验证为唯一的，节点可以发送和接收来自首选地址的单播流量。优先状态的时间段包含在RA消息中。
- **deprecated** - 该地址仍然有效，但不用于新的连接。
- **invalid** - 节点不能再发送或接收单播流量。一个地址在有效期限过后进入无效状态。

下面的图片说明了状态和寿命之间的关系。 

[![](https://help.mikrotik.com/docs/download/attachments/40992815/Ipv6-lifetime.png?version=1&modificationDate=1602228610903&api=v2)](https://wiki.mikrotik.com/wiki/File:Ipv6-lifetime.png)

## 邻居发现

**Sub-menu:** `/ipv6 nd`

在这个子菜单中，配置了IPv6邻居发现（ND）协议。

邻居发现（ND）是一组确定相邻节点之间关系的消息和过程。与IPv4相比，ND取代了地址解析协议（ARP）、互联网控制消息协议（ICMP）路由器发现和ICMP重定向，并提供额外的功能。

ND被主机用：

- 发现邻近的路由器。
- 发现地址、地址前缀和其他配置参数。

路由器使用ND来：

- 广播他们的存在、主机配置参数和链路前缀。
- 通知主机一个更好的下一跳地址来转发数据包到特定的目的地。

节点用ND来：

- 解决被转发的IPv6数据包的邻接节点的链路层地址，并确定邻接节点的链路层地址何时改变。
- 确定IPv6数据包是否可以发送到邻居和从邻居接收。

**属性**

| 属性                                                                             | 说明                                                                                                                                                                                                                                                                                |
| -------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **advertise-dns** (_yes_ \| _no_; Default: **no**)                               | 选择使用RADVD重新分配DNS服务器信息。需要一个运行中的支持Router Advertisement DNS的客户端软件，以利用广播的 [DNS](https://wiki.mikrotik.com/wiki/Manual:IP/DNS "Manual:IP/DNS") 信息。 [阅读更多](https://wiki.mikrotik.com/wiki/Manual:IPv6/ND#Stateless_autoconfiguration_example) |
| **advertise-mac-address** (_yes_ \| _no_; Default: **yes**)                      | 设置时，出站接口的链路层地址将包括在RA中。                                                                                                                                                                                                                                          |
| **comment** (_string_; Default: )                                                | 项目的描述名称。                                                                                                                                                                                                                                                                    |
| **dns-servers** (_unspecified_ _ipv6 addresses_; Default: **unspecified**)       | 指定单个IPv6地址或地址列表，提供给主机用于配置DNS服务器。                                                                                                                                                                                                                           |
| **disabled** (_yes_                                                              | _no_; Default: **no**)                                                                                                                                                                                                                                                              | 项目是否被禁用。默认情况下，条目是启用的。 |
| **hop-limit** (_unspecified_\| _integer_[_0..255_]; Default: **unspecified**)    | 放在出站（单播）IP数据包的IP头的Hop Count字段中的默认值。                                                                                                                                                                                                                           |
| **interface** (_all_ \| _string_; Default: )                                     | 运行邻居发现的接口。<br>- all - 在所有运行的接口上运行ND。                                                                                                                                                                                                                          |
| **managed-address-configuration** (_yes_ \| _no_; Default: **no**)               | 该标志表明主机是否应该使用有状态的自动配置（DHCPv6）来获得地址。                                                                                                                                                                                                                    |
| **mtu** (_unspecified_ \| _integer_[_0..4294967295_]; Default: **unspecified**)  | MTU选项在路由器广播信息中使用，确保在链路MTU不为人所知的情况下，链路上的所有节点使用相同的MTU值。<br>- **unspecified** - 不发送MTU选项。                                                                                                                                            |
| **other-configuration** (_yes_ \| _no_; Default: **no**)                         | 该标志表明主机是否应该使用有状态的自动配置来获得额外的信息（不包括地址）。                                                                                                                                                                                                          |
| **pref64-prefixes** (_unspecified_ \| _ipv6 prefixes_; Default: **unspecified**) | 指定IPv6前缀或/32, /40. /48、/56、/64或/96子网内的IPv6前缀或前缀列表，它们将作为NAT64前缀提供给主机。                                                                                                                                                                               |
| **ra-delay** (_time_; Default: **3s**)                                           | 从接口发送多播路由器广播之间允许的最小时间。                                                                                                                                                                                                                                        |
| **ra-interval** (_time_[_3s..20m50s_]_-time_[_4s..30m_]; Default: **3m20s-10m**) | 允许从接口发送非请求多播路由器广播的最小-最大间隔时间。                                                                                                                                                                                                                             |
| **ra-preference** (_low_ \| _medium_ \| _high_; Default: **medium**)             | 指定通过路由器广播传达给IPv6主机的路由器偏好。路由器广播中的 "preference "值使IPv6主机能够选择一个默认的路由器来到达远程目的地。                                                                                                                                                    |
| **ra-lifetime** (_none_ \| _time_; Default: **30m**)                             |                                                                                                                                                                                                                                                                                     |
| **reachable-time** (_unspecified_ \| _time_[_0..1h_]; Default: **unspecified**)  | 一个节点在收到可达性确认后假设邻居可达的时间。由邻居不可达性检测算法使用(见RFC 2461第7.3节)                                                                                                                                                                                         |
| **retransmit-interval** (_unspecified \| time_; Default: **unspecified**)        | 重发邻居请求信息的间隔时间。用于地址解析和邻居不可达性检测算法（见RFC 2461第7.2和7.3节）。                                                                                                                                                                                          |

如果ND是由LTE配置自动生成的，那么RA的最大寿命将被限制在1小时。

## 前缀

**Sub-menu：** `/ipv6 nd prefix`。

无状态地址自动配置所使用的RA消息中发送的前缀信息。

**注意：** 自动配置过程只适用于主机，而不是路由器。

**属性**

| 属性                                                                      |                                                                                                                                                                                                                                  |
| ------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **6to4-interface** (_none                      \| string_; Default: )     | 如果指定了这个选项，这个前缀将与接口名称的IPv4地址相结合，产生一个有效的6to4前缀。这个前缀的前16位将被2002替换，接下来的32位将被配置时分配给接口名称的IPv4地址替换。前缀的其余80位（包括SLA ID）将按照配置文件中的规定进行宣传。 |
| **autonomous** (_yes\| no_; Default: **yes**)                             | 设置时，表示此前缀可用于自治地址配置。否则，前缀信息将沉默忽略。                                                                                                                                                                 |
| **comment** (_string_; Default: )                                         | 一个项目的描述名称。                                                                                                                                                                                                             |
| **disabled** (_yes \| no_; Default: **no**)                               | 项目是否被禁用。默认情况下是启用的。                                                                                                                                                                                             |
| **on-link** (_yes\| no_; Default: **yes**)                                | 设置时表示该前缀可用于确定on-link。未设置时，广告不对前缀的链路上或链路下的属性做任何说明。例如，该前缀可能被用于地址配置，其中一些属于该前缀的地址是链路上的，而另一些则是链路外的。                                            |
| **preferred-lifetime** (_infinity              \| time_; Default: **1w**) | 时间框架（相对于数据包的发送时间），在这之后，生成的地址会变成 "废弃的"。废弃的只用于已经存在的连接，并且在有效期限到期之前可以使用。 [阅读全文](https://wiki.mikrotik.com/wiki/Manual:IPv6/ND#Address_states)                   |
| **prefix** (_ipv6 prefix_; Default: **::/64**)                            | 一个前缀，无状态地址自动配置由此产生有效地址。                                                                                                                                                                                   |
| **valid-lifetime** (_infinity \| time_; Default: **4w2d**)                | 地址保持有效状态的时间长度（相对于数据包的发送时间）。有效寿命必须大于或等于首选寿命。 [阅读全文](https://wiki.mikrotik.com/wiki/Manual:IPv6/ND#Address_states)                                                                  |
| **interface** (_string_; Default: )                                       | 无状态自动配置运行的接口名称。                                                                                                                                                                                                   |

## 邻居列表

**Sub-menu:** `/ipv6 neighbor`

通过IPv6邻居发现协议（邻居缓存）发现的所有节点列表。

**只读属性**

| 属性                                                                                                                                                      | 描述                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| --------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **address** (_ipv6 address_)                                                                                                                              | 节点的链接本地地址。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| **comment** (_string_)                                                                                                                                    |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| **interface** (_string_)                                                                                                                                  | 检测到该节点的接口。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| **mac-address** (_string_)                                                                                                                                | 被发现节点的Mac地址。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| **router** (_yes             \| no_)                                                                                                                      | 被发现的节点是否是一个路由器                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| **status** (_noarp           \| incomplete                                    \| stale                                   \| reachable \| delay \| probe_) | 缓存条目的状态：<br>- **noarp** - 邻居条目是有效的。不会尝试验证这个条目，寿命到期时，可以将其删除。<br>- **incomplete** - 地址解析正在进行中，邻居的链路层地址还没有确定；<br>- **reachable** -已知该邻居最近（几十秒前）是可以到达的；<br>- **stale** - 邻居不再是已知可达的，但在向邻居发送流量之前，不尝试验证其可达性；<br>- **delay** - 邻居不再是已知可达的，并且最近向邻居发送了流量，探测被延迟了一小段时间，以便给上层协议提供可达性确认的机会；<br>- **probe** - 邻居不再是已知可达的，并且正在发送单播邻居请求探测以验证可达性。 |

## 示例

### 无状态自动配置的例子


```shell
[admin@MikroTik] > ipv6 address print
Flags: X - disabled, I - invalid, D - dynamic, G - global, L - link-local
# ADDRESS INTERFACE ADVERTISE
0 G 2001:db8::1/64 ether1 yes
```

一个例子，**advertise** 标志启用，表明动态添加了 `/ipv6 nd prefix` 条目


```shell
[admin@MikroTik] > ipv6 nd prefix print
Flags: X - disabled, I - invalid, D - dynamic
0 D prefix=2001:db8::/64 interface=ether1 on-link=yes autonomous=yes
 valid-lifetime=4w2d preferred-lifetime=1w
```

在一个直接连接到路由器的主机上看到一个地址被添加。该地址由前缀部分（前64位）和主机部分（后64位）组成，前者从前缀广播中获取前缀，后者从本地MAC地址中自动生成：

```shell
atis@atis-desktop:~$ ip -6 addr
 1: lo: <LOOPBACK,UP,LOWER_UP> mtu 16436
inet6 ::1/128 scope host
valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qlen 1000
inet6 2001:db8::21a:4dff:fe56:1f4d/64 scope global dynamic
 valid_lft 2588363sec preferred_lft 601163sec
inet6 fe80::21a:4dff:fe56:1f4d/64 scope link
valid_lft forever preferred_lft forever
```

主机已经从路由器收到_2001:db8::/64_前缀，并用它配置了一个地址。

还有一个选项是使用RADVD重新分配 [DNS](https://wiki.mikrotik.com/wiki/Manual:IP/DNS "Manual:IP/DNS") 服务器信息：


```shell
[admin@MikroTik] > ip dns set server=2001:db8::2
[admin@MikroTik] > ip dns print servers: 2001:db8::2
 ...
[admin@MikroTik] > ipv6 nd set [f] advertise-dns=yes
```
 

需要一个支持路由器广播DNS的客户端软件来广播DNS信息。

在Ubuntu/Debian Linux发行版上，可以安装 **rdnssd** 包，它能接收广播的DNS地址。

`mrz@bumba:/$ sudo apt-get install rdnssd`


```shell
mrz@bumba:/$ cat /etc/resolv.conf
# Dynamic resolv.conf(5) file for glibc resolver(3) generated by resolvconf(8)
 # DO NOT EDIT THIS FILE BY HAND -- YOUR CHANGES WILL BE OVERWRITTEN
 nameserver 2001:db8::2
 
mrz@bumba:/$ ping6 www.mikrotik.com
PING www.mikrotik.com(2a02:610:7501:1000::2) 56 data bytes
 64 bytes from 2a02:610:7501:1000::2: icmp_seq=1 ttl=61 time=2.11 ms
 64 bytes from 2a02:610:7501:1000::2: icmp_seq=2 ttl=61 time=1.33 ms
^C
 --- www.mikrotik.com ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 1.334/1.725/2.117/0.393 ms
mrz@bumba:/$
```
