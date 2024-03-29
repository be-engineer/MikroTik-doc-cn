# 概述

本章介绍了RouterOS中的虚拟路由器冗余协议（VRRP）。

大多数情况下，在较大的局域网中使用动态路由协议（OSPF或RIP），然而，有一些因素使用动态路由协议不可取。一种是使用静态路由，但如果静态配置的第一跳失败，那么主机将无法与其他主机进行通信。

在IPv6网络中，主机通过接收邻居发现（ND）协议的路由器通告了解路由器。ND有一个内置机制来确定不可达的路由器。然而，它可能需要长达38秒的时间来检测一个不可到达的路由器。可以改变参数使检测速度更快，但会增加ND流量开销，特别是在有很多主机的情况下。VRRP允许在3秒内检测到不可到达的路由器，而没有额外的流量开销。

虚拟路由器冗余协议（VRRP）提供了一个解决方案，将一些路由器组合成一个叫做 _虚拟路由器_ （VR）的逻辑组。RouterOS中的VRRP实现是基于VRRPv2 RFC 3768和VRRPv3 RFC 5798。

建议所有设备使用相同版本的RouterOS，并使用相同的VRID来实现VRRP。

 根据RFC，认证在VRRPv3中已废弃。

## 协议概览

![](https://help.mikrotik.com/docs/download/attachments/81362945/Vrrp-simple.png?version=1&modificationDate=1630399353666&api=v2)

VRRP的目的是和所有与虚拟路由器ID相关的VRRP路由器进行通信，并通过它们之间的优先选举过程来支持路由器的冗余。

所有的信息传递都通过使用协议112（VRRP）的IPv4或IPv6组播包完成。IPv4数据包的目的地址是 _224.0.0.18_ ，对于IPv6是 _FF02：0：0：0：0：0：0：0：12_ 。数据包的源地址始终是发送该数据包接口的主要IP地址。在IPv6网络中，源地址是一个接口的链接本地地址。

这些数据包总是以TTL=255发送，并且不被路由器转发。如果由于任何原因，路由器收到的数据包的TTL更低，那么数据包将被丢弃。

每个VR节点都有一个MAC地址。这个MAC地址用作Master发送的所有定期消息的来源。

虚拟路由器是由VRID和映射的IPv4或IPv6地址集定义的。主路由器认为是映射的IPv4/IPv6地址的 **所有者** 。对IPv4和IPv6使用相同的VRID是没有限制的，但这是两个不同的虚拟路由器。

只有主路由器会定期发送通告信息以减少流量。只有一个备份路由器有较高的优先级并且不禁止抢占时，它才会尝试抢占主路由器。

所有属于同一VR的VRRP路由器必须配置相同的通告间隔。如果间隔时间不匹配，路由器将丢弃收到的通告包。

## 虚拟路由器(VR)

虚拟路由器（VR）由一个主路由器和一个或多个属于同一网络的备份路由器组成。

VR包括：

- 在每个VRRP路由器上配置的VRID
- 每个路由器上都有相同的虚拟IP
- 在每个路由器上配置的所有者和备份。在给定的VR上，只能有一个所有者。

### 虚拟MAC地址

VRRP根据VRRP数据包标准MAC前缀和VRID号码，自动为VRRP接口分配MAC地址。前五个八位字节数是00:00:5E:00:01，最后一个八位字节数是配置的VRID。例如，如果虚拟路由器VRID是49，那么虚拟MAC地址将是 _00:00:5E:00:01:31_ 。

虚拟MAC地址不能手动设置或编辑。

## Master

一个VR的Master路由器是默认的主路由器，作为VR中包含的所有子网的所有者运行。Master路由器的优先级必须是最高值（255），虚拟IP与真实IP相同（拥有虚拟IP地址）。

RouterOS不能配置为所有者。纯粹的虚拟IP配置是唯一有效的配置，除非一个非RouterOS设备被设置为所有者。

## 主路由器

VR中的主路由器作为所配置的网络的物理网关运行。主路由器的选择是由优先级值控制的。主路由器状态描述了主路由器的行为。例如网络，**R1** 是主路由器。当R1不再可用时，R2成为主路由器。

## 备份路由器

VR必须至少包含一个备份路由器。备份路由器必须配置与该VR的主路由器相同的虚拟IP。备份路由器的默认优先级是100。当主路由器不再可用时，有最高优先级的备份路由器将成为当前的主路由器。每次当有更高优先级的路由器可用时，它就会切换成主路由器。有时这种行为是不必要的。要废除它，可以禁用抢占模式。

## 虚拟地址

![](https://help.mikrotik.com/docs/download/attachments/81362945/Vrrp-no-owner.png?version=1&modificationDate=1630399462359&api=v2)

与VR相关的虚拟IP必须是相同的，并在所有VR节点上设置。所有的虚拟和真实地址应该来自同一个网络。

RouterOS不能配置为主路由器。VRRP地址和真实IP地址不能相同。

如果VR的主路由器与多个IP地址相关联，那么属于同一VR的备份路由器也必须与同一组虚拟IP地址关联。如果主路由器上的虚拟地址不在备份路由器上，则存在错误的配置，VRRP通告包将被丢弃。

所有的虚拟路由器成员都可以配置为使虚拟IP与物理IP不相同。这样的虚拟地址称为浮动或纯虚拟IP地址。这种设置的优点是给管理员提供了灵活性。由于虚拟IP地址不是任何一个参与路由器的真实地址，管理员可以改变这些物理路由器或其地址，而不需要重新配置虚拟路由器本身。

在IPv6网络中，第一个地址总是与VR相关的链接本地地址。如果配置了多个IPv6地址，那它们会添加到通告包的链路本地地址之后。

### IPv4 ARP

给定的VR的主路由器用该VR分配的MAC地址来响应ARP请求。虚拟MAC地址也用作主路由器发送的通告包的源MAC地址。对于非虚拟IP的ARP请求，地址路由器用系统MAC地址响应。备份路由器对虚拟IP的ARP请求不做响应。

### IPv6 ND

在IPv6网络中，使用邻居发现协议来代替ARP。当一个路由器成为主路由器时，为每个与虚拟路由器相关的IPv6地址发送一个带有路由器标志的非请求的ND邻居通告。

## VRRP状态机

![](https://help.mikrotik.com/docs/download/attachments/81362945/Vrrp-State.png?version=1&modificationDate=1630399487184&api=v2)

从图中可以看出，每个VRRP节点可以处于以下三种状态之一:

- 初始状态
- 备份状态
- 主状态

### 初始状态

这个状态的目的是等待一个启动事件。当收到该事件时，将采取以下行动：

- 如果优先级为255
- 对于 IPv4 发送通告包和广播 ARP 请求
- 对于IPv6，为每个与虚拟路由器相关的IPv6地址发送一个非请求的ND邻居通告，并把目标地址设置为与VR相关的链路本地地址。
- 转移到主站状态。
- 否则就转入备份状态。

### 备份状态

当处于备份状态时

- 在IPv4网络中，节点不响应ARP请求，不转发与VR相关的IP流量。
- 在IPv6网络中，节点不响应ND邻居请求消息，也不为VR相关的IPv6地址发送ND路由器通告消息。

路由器的主要任务是接收通告包并检查主节点是否可用。

两种情况下，备份路由器会将自己传送到主节点状态。

- 如果通告包中的优先级为0。
- 当Preemption_Mode设置为yes，且通告中的优先级低于本地优先级时

在过渡到主状态后，节点是：

- 在IPv4中广播无偿的ARP请求。
- 在IPv6中为每个相关的IPv6地址发送一个非请求的ND邻居通告。

在其他情况下，通告数据包将丢弃。当收到关机事件时，转入初始状态。

如果所有者路由器可用，抢占模式将被忽略。

### 主状态

当MASTER状态被设置时，该节点作为与VR相关的IPv4/IPv6地址的转发路由器发挥作用。

在IPv4网络中，主节点会响应与VR相关的IPv4地址的ARP请求。在IPv6网络中，主节点：

- 响应相关IPv6地址的ND邻居请求消息。
- 为相关的IPv6地址发送ND路由器通告。

如果通告包被主节点收到：

- 如果优先级为0，立即发送通告。
- 如果通告包中的优先级大于节点的优先级，则转入备份状态
- 如果通告包的优先级等于节点的优先级，并且发送者的主IP地址大于本地主IP地址，则转入备份状态。
- 忽略其他情况下的通告

当收到关机事件时，发送优先级为0的通告包，转入初始状态。

## 连接跟踪同步

和不同的高可用性功能类似，RouterOS v7支持VRRP连接跟踪同步。

VRRP连接跟踪同步需要RouterOS的 [连接跟踪](https://help.mikrotik.com/docs/display/ROS/Connection+tracking) 正在运行。默认情况下，连接跟踪是在 "自动"模式下工作。如果VRRP设备不包含任何防火墙规则，则需要手动启用连接跟踪：

`/ip/firewall/connection/tracking/ set enabled =yes`

要同步连接跟踪条目，请按以下方式配置设备：

`/interface/vrrp/ set vrrp1 sync-connection-tracking =yes`

在日志部分验证配置：

`16 :14:06 vrrp, info vrrp1 now MASTER, master down timer`

`16 :14:06 vrrp, info vrrp1 stop CONNTRACK`

`16 :14:06 vrrp, info vrrp1 starting CONNTRACK MASTER`

连接跟踪条目只从主设备同步到备份设备。

当 **同步连接跟踪** 和 **抢占模式** 都启用时，如果一个具有较高VRRP优先级的路由器上线，连接会先被同步，然后有较高优先级的路由器才会成为VRRP主设备。

如果两个单元之间配置了多个VRRP接口，只需在一个（最好是主）VRRP接口上启用sync-connection-tracking=yes即可。

## 配置VRRP

### IPv4

设置虚拟路由器非常简单，只需要两个动作 - 创建VRRP接口和设置虚拟路由器的IP地址。

例如，为ether1添加VRRP，并设置VR地址为192.168.1.1

`/interface vrrp add name =vrrp1 interface =ether1`

`/ip address add address =192.168.1.2/24 interface =ether1`

`/ip address add address =192.168.1.1/32 interface =vrrp1`

注意，在添加VRRP时只指定了 "接口 "参数。这是唯一需要手动设置的参数，其他参数如果没有指定将被设置为默认值。`vrid=1, priority=100` 和 `authentication=none` 。

如果在VRRP上配置的地址与路由器的其他接口上的地址来自同一个子网，那么VRRP接口上的地址必须有/32的掩码。

在VRRP正确运行之前，ether1上需要有正确的IP地址。在这个例子中是192.168.1.2/24。

### IPV6

为了使VRRP在IPv6网络中工作，必须启用几个额外的选项-需要v3支持，协议类型应设置为IPv6：

`/interface vrrp add name =vrrp1 interface =ether1 version =3 v3-protocol =ipv6`。

现在，当VRRP接口设置完毕后，可以添加一个全局地址并启用ND通告。

`/ipv6 address add address =FEC0:0:0:FFFF::1/64 advertise =yes interface =vrrp1`。

不需要像IPv4那样进行额外的地址配置。IPv6使用链路本地地址在节点之间进行通信。

## 参数

| 属性                                                                             | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| -------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **arp** (_disabled \| enabled \| proxy-arp \| reply-only_; Default: **enabled**) | ARP解析协议模式                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **arp-timeout** _(integer; Default: auto)_                                       |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **authentication** (_ah \| none \| simple_; Default: **none**)                   | VRRP通告包使用的验证方法。<br>- none - 只在低安全性的网络中使用（例如，局域网中的两个VRRP节点）。<br>- ah - IP认证报头。这种算法对配置错误、重放攻击和数据包损坏/修改提供了强有力的保护。当局域网上的节点管理控制有限时推荐使用。<br>- simple - 使用一个明文密码。防止本地网络上的路由器的意外错误配置。                                                                                                                                                                                                                                                                                  |
| **group-master** (_interface;_ Default: **none**)                                | 允许结合多个VRRP接口，在组内保持相同的VRRP状态。例如，VRRP实例在LAN和WAN网络上运行，中间有NAT。如果一个VRRP实例是主控，而另一个是同一设备上的备份，整个网络就会因NAT失效而发生故障。将局域网和广域网的VRRP接口分组，可以确保两者都是VRRP主站或备份站。<br>在一个VRRP组中，VRRP控制流量只由组内主站发送。这就是为什么在典型的WAN+LAN设置中，建议使用LAN网络作为主组，使VRRP控制流量保持在内部网络。<br> /interface vrrp<br>add name=vrrp-wan interface=sfp-sfpplus1 vrid=1 priority=100<br>add name=vrrp-lan interface=bridge1 vrid=2 priority=100<br>set [find] group-master=vrrp-lan<br> |
| **interface** (_string_; Default: )                                              | VRRP实例将在其上运行的接口名称                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| **interval** (_time [10ms..4m15s]_; Default: **1s**)                             | VRRP更新间隔，单位为秒。定义了主站发送通告包的频率                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| **mtu** (_integer_; Default: **1500**)                                           | 第三层MTU大小。从RouterOS v7.7开始，VRRP接口总是使用从属接口的MTU                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| **name** (_string_; Default: )                                                   | VRRP接口名称                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| **on-backup** (_string_; Default: )                                              | 节点切换到备份状态时执行的脚本                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **on-master** (_string_; Default: )                                              | 节点切换到主控状态时执行的脚本                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| **on-fail** (_string_; Default: )                                                | 当节点发生故障时执行的脚本                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| **password** (_string_; Default: )                                               | 验证密码。如果不使用认证，可以忽略不计                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| **preemption-mode** (_yes \| no_; Default: **yes**)                              | 主节点是否总是有优先权。当设置为“no“时，备份节点将不会被选为主节点，直到当前主节点失效，即使备份节点的优先级比当前主节点高。如果所有者路由器可用，该设置将被忽略。                                                                                                                                                                                                                                                                                                                                                                                                                        |
| **priority** (_integer: 1...254_; Default: **100**)                              | 在Master选举算法中使用的VRRP节点的优先级。数字越大优先级越高。"255"保留给拥有VR IP的路由器，"0"保留给Master路由器，表示它正在释放责任。                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| **remote-address** (_IPv4;_ Default: )                                           | 指定另一个VRRP路由器的远程地址，用于同步连接跟踪。如果不设置，系统会通过VRRP自动检测远程地址。只有当sync-connection-tracking=yes时，才会使用远程地址。明确设置一个远程地址有以下好处。<br>- 连接同步开始得更快，因为不需要等待VRRP的初始消息交换来检测远程地址。<br>- 更快的VRRP主站选举。<br>- 允许通过不同的网络接口（例如，两个路由器之间的专用安全线路）发送连接跟踪数据。<br>同步连接跟踪使用UDP端口8275。                                                                                                                                                                           |
| **v3-protocol** (_ipv4 \| ipv6_; Default: **ipv4**)                              | VRRPv3使用的协议。只有 **版本** 为3时才有效                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| **version** (_integer [2, 3]_; Default: **3**)                                   | 要使用的VRRP版本                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **vrid** (_integer: 1..255_; Default: **1**)                                     | 虚拟路由器标识。每个虚拟路由器必须有一个唯一的标识号                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| **sync-connection-tracking** (_string_; Default: **no**)                         | 从主设备到备份设备同步连接跟踪条目。VRRP连接跟踪的同步需要RouterOS的 [连接跟踪](https://help.mikrotik.com/docs/display/ROS/Connection+tracking) 正在运行。                                                                                                                                                                                                                                                                                                                                                                                                                                |
