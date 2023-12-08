# 概述

路由是指在网络中选择路径，将数据包从一个主机转移到另一个主机的过程。

## 路由如何工作

看一个基本的配置例子，说明路由是如何在两个本地网络之间转发数据包并传送到互联网的。

在这个设置中，有几个网络：

- 两个客户网络（192.168.2.0/24和192.168.1.0/24）；
- 一个连接路由器的网络（172.16.1.0/30），通常称为主干网；
- 最后一个网络（10.1.1.0/24）将网关路由器（Router1）连接到互联网。


![](https://help.mikrotik.com/docs/download/attachments/328084/How-routing-works.jpg?version=2&modificationDate=1572856689444&api=v2)

Router2:

```shell
/ip address
add address=172.16.1.2/30 interface=ether1
add address=192.168.2.1/24 interface=bridge2
```

Router1（网关），ether1连接到互联网：

```shell
/ip address
add address=10.1.1.2/24 interface=ether1
add address=172.16.1.1/30 interface=ether2
add address=192.168.1.1/24 interface=bridge1
```

如果看一下Router1的路由表，可以看到该路由器只知道直接连接的网络。因此当LAN1的客户试图到达LAN2的客户（192.168.2.0/24）时，数据包将在路由器上被丢弃，因为目的地对特定的路由器来说是未知的：

```shell
[admin@MikroTik] > /ip/route> print
Flags: D - dynamic; X - disabled, I - inactive, A - active; C - connect, S - static, r - ri
p, b - bgp, o - ospf, d - dhcp, v - vpn
Columns: DST-ADDRESS, GATEWAY, Distance
    DST-ADDRESS    GATEWAY D
DAC 10.1.1.0/24    ether1  0
DAC 172.16.1.0/30  ether2  0
DAC 192.168.1.0/24 bridge1 0
```

为了解决这个问题，要添加一个路由，告诉路由器什么是网络中到达目的地的下一个设备。 在这个例子中，下一跳是Router2，所以要添加一个指向Router2连接地址的网关的路由：

```shell
[admin@MikroTik] > /ip route add dst-address=192.168.2.0/24 gateway=172.16.1.2
[admin@MikroTik] > /ip/route> print
Flags: D - dynamic; X - disabled, I - inactive, A - active; C - connect, S - static, r - ri
p, b - bgp, o - ospf, d - dhcp, v - vpn
Columns: DST-ADDRESS, GATEWAY,       Distance
        DST-ADDRESS    GATEWAY       D
    DAC 10.1.1.0/24    ether1        0
    DAC 172.16.1.0/30  ether2        0
    DAC 192.168.1.0/24 bridge1       0
0   AS  192.168.2.0/24 172.16.1.2
```

此时，来自LAN1的数据包成功转发到LAN2，但还没有结束。Router2不知道如何到达LAN1，所以来自LAN2的任何数据包都会在Router2上丢弃。

再看一下网络图，可以清楚地看到，Router2只有一个出口点。可以认为，所有其他未知的网络都应该通过与Router1的链接到达。最简单的方法是添加一个 **default route**： 要添加一个默认路由，设置目的地为0.0.0.0/0或留空：

`/ip route add gateway=172.16.1.1`

正如设置的例子中看到的，不同的路由组基于它们的来源和属性。

## 路由信息

RouterOS的路由信息由两个主要部分组成：

- **FIB** （转发信息库），用于做出数据包转发决定。它包含必要的路由信息的副本。
- **RIB** （路由信息库）包含所有从路由协议（连接的、静态的、BGP、RIP、OSPF）学到的前缀。

![](https://help.mikrotik.com/docs/download/attachments/328084/RIB_FIB.png?version=1&modificationDate=1570777722022&api=v2)

### 路由信息库

![](https://help.mikrotik.com/docs/download/attachments/328084/routing-hops.jpg?version=1&modificationDate=1572931725399&api=v2)

路由信息库是一个数据库，列出了特定网络目的地的条目及其网关（沿路下一个设备的地址或简称下一跳）。路由表中的一个这样的条目被称为route。

当一个数据包从一个网段传到另一个网段时，就发生了一跳。

默认情况下，所有的路由都被组织在一个主路由表中。可以设置一个以上的路由表，将在本文中进一步讨论，但现在为了简单起见，假设只有一个主路由表。

RIB表包含完整的路由信息，包括用户配置的静态路由和策略路由规则、从动态路由协议（RIP、OSPF、BGP）学到的路由信息，以及连接网络的信息。

它的目的不仅仅是存储路由，还包括过滤路由信息以计算每个目标前缀的最佳路由，建立和更新转发信息库，以及在不同路由协议之间分配路由。

#### 连接的路由

连接的路由代表了可以直接到达主机的网络（直接附加到第二层广播域）。这些路由是为每个至少有一个启用的接口连接到它的IP网络自动创建的（如在 _/ip address_ 或 _/ipv6 address_ 配置中指定）。RIB跟踪连接路由的状态，但不修改它们。对于每个连接的路由，有一个IP地址：

- 连接路由的 _dst-address_ 的 **address** 部分等于一个网络的IP地址项。
- 连接路由的 _dst-address_ 的 **netmask** 部分等于IP地址项目的地址的netmask部分。
- 连接路由的 **网关** 等于IP地址项的实际 _interface_（与接口相同，但桥接接口端口除外），代表一个可以到达特定第三层网络的直接连接主机的接口。

对于连接的路由，**首选源** 不再使用。FIB根据输出接口来选择源地址。这使得在ROS v6和更早的版本中的设置被认为是无效的。更多细节请见 [示例](https://wiki.mikrotik.com/wiki/Manual:Route_lookup_example)。

#### 默认路由

当目的地不能被路由表中的任何其他路由解决时，就会使用默认路由。在RouterOS中，默认路由的 _dst-address_ 是 **0.0.0.0/0** （用于IPv4）和 **:/0** （用于IPv6）路由。如果路由表包含一个活跃的默认路由，那么在这个表中的路由表查询就不会失败。

通常情况下，家庭路由器的路由表只包含连接的网络和一个默认路由，将所有出站流量转发到ISP的网关：

```shell
[admin@TempTest] /ip/route> print
Flags: D - dynamic; X - disabled, I - inactive, A - active; C - connect, S - static, r - ri
p, b - bgp, o - ospf, d - dhcp, v - vpn
Columns: DST-ADDRESS, GATEWAY, Distance
#      DST-ADDRESS     GATEWAY      D
   DAd 0.0.0.0/0       10.155.125.1 1
   DAC 10.155.125.0/24 ether12      0
   DAC 192.168.1.0/24  vlan2        0
```

#### 多路径（ECMP）路由

为了实现某些设置，如负载平衡，可能需要使用一个以上的路径到达指定的目的地。

![](https://help.mikrotik.com/docs/download/attachments/328084/basic.png?version=1&modificationDate=1621415362384&api=v2)

ECMP（等价多路径）路由有多个网关（下一跳）值。所有可到达的下一跳都被复制到FIB，并用于转发数据包。

这些路由可以手动创建，也可以由任何动态路由协议（OSPF、BGP、RIP）动态创建。通往同一目的地的多条同样优先的路由将被分配+标志，并由RouterOS自动分组（见下面的例子）。

```shell
[admin@TempTest] /ip/route> print
Flags: D - DYNAMIC; I - INACTIVE, A - ACTIVE; C - CONNECT, S - STATIC, m - MODEM; + - ECMP
Columns: DST-ADDRESS, GATEWAY, DISTANCE
#       DST-ADDRESS      GATEWAY       D
0   AS+ 192.168.2.0/24   10.155.125.1  1
1   AS+ 192.168.2.0/24   172.16.1.2    1
```

#### 路线选择

从各种路由协议和静态配置中收到的同一目的地的路由可能有多条，但只有一个（最佳）目的地可用于数据包的转发。为了确定最佳路径，RIB运行一个路由选择算法，从每个目的地的所有候选路由中挑选出最佳路由。

只有满足以下条件的路由才能参与路由选择过程：

- 路由没有被禁用。
- 如果路由的类型是 _unicast_，它必须至少有一个可到达的下一跳。(如果一个网关来自连接的网络，并且有连接的路由处于活动状态，那么该网关被认为是可到达的) 
- 路由不应该是合成的。

具有最低距离的候选路由成为活动路由。如果有一个以上的候选路由具有相同的距离，那么活动路由的选择是任意的。

#### 联网查询

![](https://help.mikrotik.com/docs/download/attachments/328084/scope_and_target_scope.png?version=1&modificationDate=1570784336566&api=v2)

下一跳查询是路由选择过程的一部分。其主要目的是找到一个可直接到达的网关地址（下一跳）。只有在选择了一个有效的下一跳后，路由器才知道使用哪个接口来转发数据包。

如果路由的网关地址离这个路由器有几跳的距离（例如iBGP、多跳eBGP），那么下一跳的查找就变得更加复杂。在下一跳选择算法确定了可直接到达的网关地址（即时下一跳）之后，这样的路由会被安装在FIB中。

有必要限制可用于查找即时下一跳的路由集。例如，RIP或OSPF路由的Nexthop值应该是可以直接到达的，并且应该只使用连接的路由来查询。这是用范围和目标范围属性实现的。

范围大于最大接受值的路由不会被用于下一跳的查找。每个路由都在target-scope属性中为其nextthop指定最大接受范围值。这个属性的默认值只允许通过连接的路由来查找节点，但iBGP路由除外，它的默认值较大，也可以通过IGP和静态路由来查找节点。

RouterOS v7的nexthop查询有变化。

路由是按范围顺序处理的，对范围较大的路由的更新不能影响范围较小的路由的节点查询状态。

考虑一下 v6 的一个例子：

```shell
/ip route add dst-address=10.0.1.0/24 gateway=10.0.0.1
    scope=50 target-scope=30 comment=A
/ip route add dst-address=10.0.2.0/24 gateway=10.0.0.1
    scope=30 target-scope=20 comment=B
/ip route add dst-address=10.0.0.0/24 scope=20 gateway=WHATEVER
    comment=C
```

网关10.0.0.1通过C使用最小的引用范围（来自路由B的范围20）递归解析，两条路由都是活动的。现在我们同时改变A和B：

`/ip route set A target-scope=10`

突然间，对路由A的更新使得路由B的网关不活跃。这是因为在v6中，每个地址只有一个网关对象。

v7为每个地址保留多个网关对象，范围和网关检查的每个组合都有一个。

在v7中改变一个路由的目标范围或网关检查，**不会影响其他路由**，就像在v6中一样。在v7中，target-scope和gateway-check是内部附加在网关上的属性，而不是附加在路由上。

#### 路由存储

路由信息的存储是为了在普通情况下尽可能少地占用内存。这些优化有非明显的最坏情况和对性能的影响。

所有的路由和网关都按前缀/地址保存在一个单一的层次结构中。

```
    Dst [4]/0 1/0+4                             18  <-- number of prefixes
         ^  ^ ^ ^ ^
         |  | | | |
         |  | | | \- bytes taken by Route distinguisher or Interface Id
         |  | | \--- vrf/routing table
         |  | \----- AFI
         |  \------- netmask length of prefix
         \---------- bytes taken by prefix value

         [stuff subject to change without notice]
    
```

每个 "Dst" 都对应于一个独特的"dst-address "路由或网关地址。每个"Dst"也需要一个或多个 "T2Node" 对象。

所有具有相同 "dst-address "的路由被保存在Dst中，并按路由优先级排序。 
**注意：** 最糟糕的情况是：有很多具有相同"dst-address "的路由真的很慢！即使它们是不活动的！因为更新一个有数万个元素的排序列表很慢

只有当路由属性改变时，路由顺序才会改变。如果路由变得活跃/不活跃，顺序不会改变。

![](https://help.mikrotik.com/docs/download/attachments/328084/Rib.png?version=1&modificationDate=1570784399412&api=v2)

每个路由有三份路由属性：

- **private** -- 在通过in-filters之前，从对等体收到的东西。
- **updated** -- 应用in-filters的结果。
- **current** -- 路由当前使用的属性是什么。


定期 **update** 属性会从 **private** 属性中计算出来。这发生在收到路由更新时，或者是in-filter被更新时。

当路由表被重新计算时，**current** 属性被设置为 **updated** 属性的值。

这意味着，通常情况下，如果没有改变路由属性的内置过滤器，**private**，**updated** 和 **current** 共享相同的值。

路由属性保存在几个组中：

- L1数据 - 所有标志、额外属性列表、as-path；
- L2数据 - nexthops、RIP、OSPF、BGP度量、路由标签、发起人等。
- L3数据 - 距离、范围、内核类型、MPLS东西
- 额外的属性 - 社区、发起人、聚集者-ID、群集-列表、未知数

例如，有许多不同的 **distance** 和 **scope** 路由属性的组合，将使用更多的内存

使用regexp匹配社区或as-path会缓存结果，以加快过滤速度。每个as-path或社区值都有一个所有regexp的缓存，它按需填充匹配结果。 

**注意：** 最坏的情况是：在in-filter中改变属性会使路由程序使用更多的内存 因为'私有'和'更新'的属性将是不同的! 有很多不同的表达式会使匹配速度变慢，并使用大量的内存! 因为每个值都会有一个有成千上万个条目的缓存!

关于路由协议使用的内存的详细信息可以在 `/routing stats memory` 菜单中看到

### 转发信息库

FIB（转发信息库）包含数据包转发所需的信息副本：

- 所有活动路由
- 策略路由规则

每个路由都有 **dst-address** 属性，它指定了这个路由可用于的所有目标地址。如果有几个路由适用于一个特定的IP地址，则使用最具体的一个（有最大的网络掩码）。这个操作（找到与给定地址相匹配的最具体的路由）被称为 "路由表查询"。

只有一个最佳路由可用于数据包的转发。在路由表包含有几条具有相同 **dst-address** 的路由的情况下，所有同样最好的路由被合并成一条 [ECMP](https://help.mikrotik.com/docs/display/ROS/How+Packets+Are+Routed#HowPacketsAreRouted-Multipath(ECMP)routes) 路由。最佳路由被安装到FIB中，并被标记为 "活动"。

当转发决定使用额外的信息，如数据包的源地址，它被称为 **策略路由**。策略路由是以策略路由规则列表的形式实现的，它根据目的地址、源地址、源接口和数据包的路由标记（可由防火墙 mangle规则改变）选择不同的路由表。

#### Routing table lookup

![](https://help.mikrotik.com/docs/download/attachments/328084/Fib.png?version=1&modificationDate=1570784533347&api=v2)

FIB使用数据包的以下信息来确定其目的地：

- 源地址
- 目的地址
- 源接口
- 路由标记

可能的路由决定是

- 本地接收数据包
- 丢弃数据包（默许或向数据包的发送者发送ICMP消息）
- 将数据包发送到特定接口上的特定IP地址
  
运行路由决策：

- 检查数据包是否必须在本地交付（目的地址是路由器的地址）。
- 处理隐含的策略路由规则
- 处理由用户添加的策略路由规则
- 处理隐含的万能规则，在 "主 "路由表中查找目的地。
- 返回的结果是 "网络不可达"。

路由决定的结果可以是：

- nexthop的IP地址+接口
- 点对点接口
- 本地发送
- 丢弃
- ICMP禁止
- ICMP主机不可达
- ICMP网络不可达

不匹配当前数据包的规则会被忽略。如果一个规则有动作：

- **drop** 或 **unreachable**，那么它将作为路由决策过程的结果返回。
- **lookup** 数据包的目的地址就会在规则中指定的路由表中查找。如果查找失败（没有匹配数据包目的地址的路由），那么FIB就会进入下一条规则。
- **lookup-only** 类似于 **lookup**，但如果表中没有任何路由与数据包匹配，则查找失败。

否则：

- 如果该路由的类型是 _黑洞_ 、_禁止_ 或 _不可达_，那么返回这个动作作为路由决策结果；
- 如果这是一个连接的路由或以一个接口为 **网关** 值的路由，那么返回这个接口和数据包的目的地址作为路由决策结果；
- 如果这个路由有一个IP地址作为 **网关** 的值，那么返回这个地址和相关的接口作为路由决策结果；
- 如果这个路由有多个nexthop的值，那么就以轮流的方式选择其中一个。

##  显示路由

在RouterOS中，你有三个菜单可以查看路由表中的路由的当前状态：

- `/ip route` - 列出IPv4路由和基本属性
- `/ipv6路由` - 列出IPv6路由和基本属性
- `/routing route` - 列出所有具有扩展属性的路由

`/routing route` 菜单目前是只读的。要添加或删除路由，应该使用 `/ip(ipv6)route` 菜单。


**示例输出**

```shell
[admin@MikroTik] /ip/route> print
Flags: D - dynamic; X - disabled, I - inactive, A - active; C - connect, S - stati
c, r - rip, b - bgp, o - ospf, d - dhcp, v - vpn
Columns: DST-ADDRESS, GATEWAY, DIstance
#       DST-ADDRESS      GATEWAY      DI
0   XS   10.155.101.0/24  1.1.1.10
1   XS                    11.11.11.10
   D d   0.0.0.0/0        10.155.101.1 10
2   AS   0.0.0.0/0        10.155.101.1 1
3   AS + 1.1.1.0/24       10.155.101.1 10
4   AS + 1.1.1.0/24       10.155.101.2 10
5   AS   8.8.8.8          2.2.2.2      1
   DAC   10.155.101.0/24  ether12      0
 
 
|  ||| |   |                 |         |
|  ||| |   |                 |         \----Distance
|  ||| |   |                 \--Configured gateway
|  ||| |   \-- dst prefix
|  ||| \----- ECMP flag
|  ||\------- protocol flag (bgp, osf,static,connected etc.)
|  |\-------- route status flag (active, inactive, disabled)
|  \--------- shows if route is dynamic
\----------- console order number (shown only for static editable routes)
```

`routing route` 的输出与ip route非常相似，只是它在一个菜单中显示所有地址族的路由，同时也列出了过滤的路由。

```shell
[admin@MikroTik] /routing/route> print
Flags: X - disabled, I - inactive, F - filtered, U - unreachable, A - active; c - connect, s - static,
r - rip, b - bgp, o - ospf, d - dhcp, v - vpn, a - ldp-address, l - ldp-mapping
Columns: DST-ADDRESS, GATEWAY, DIStance, SCOpe, TARget-scope, IMMEDIATE-GW
     DST-ADDRESS            GATEWAY      DIS SCO TAR IMMEDIATE-GW
Xs   10.155.101.0/24
Xs
d    0.0.0.0/0              10.155.101.1 10  30  10  10.155.101.1%ether12
As   0.0.0.0/0              10.155.101.1 1   30  10  10.155.101.1%ether12
As   1.1.1.0/24             10.155.101.1 10  30  10  10.155.101.1%ether12
As   8.8.8.8                2.2.2.2      1   254 254 10.155.101.1%ether12
Ac   10.155.101.0/24        ether12      0   10      ether12
Ic   2001:db8:2::/64        ether2       0   10
Io   2001:db8:3::/64        ether12      110 20  10
Ic   fe80::%ether2/64       ether2       0   10
Ac   fe80::%ether12/64      ether12      0   10      ether12
Ac   fe80::%bridge-main/64  bridge-main  0   10      bridge-main
A    ether12                             0   250
A    bridge-main                         0   250
```

`Routing route print detail` 显示更多的高级信息，对调试有用。

```shell
[admin@MikroTik] /routing route> print detail
Flags: X - disabled, I - inactive, F - filtered, U - unreachable, A - active;
c - connect, s - static, r - rip, b - bgp, o - ospf, d - dhcp, v - vpn, a - ldp-address, l - ldp-ma>
+ - ecmp
Xs dst-address=10.155.101.0/24
Xs
d afi=ip4 contribution=best-candidate dst-address=0.0.0.0/0 gateway=10.155.101.1
immediate-gw=10.155.101.1%ether12 distance=10 scope=30 target-scope=10
belongs-to="DHCP route" mpls.in-label=0 .out-label=0 debug.fwp-ptr=0x201C2000
 
As afi=ip4 contribution=active dst-address=0.0.0.0/0 gateway=10.155.101.1
immediate-gw=10.155.101.1%ether12 distance=1 scope=30 target-scope=10
belongs-to="Static route" mpls.in-label=0 .out-label=0 debug.fwp-ptr=0x201C2000
```