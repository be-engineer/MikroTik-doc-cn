# 概述

OSPF是内部网关协议（IGP），设计用在属于同一自治系统（AS）的路由器之间分配路由信息。

该协议以链路状态技术为基础，与RIP等距离矢量协议相比，有几个优点：

- 没有跳数限制；
- 使用组播寻址来发送路由信息更新；
- 只有在网络拓扑结构发生变化时才会发送更新；
- 网络的逻辑定义，路由器被划分为区域
- 传输和标记注入AS的外部路由。

然而，也有一些缺点：

- 由于SPF算法和维护多份路由信息，OSPF相当消耗CPU和内存；
- 与RIP相比，实现的协议更复杂；

RouterOS实现了以下标准：

- RFC [2328](https://tools.ietf.org/html/rfc2328) - OSPF Version 2
- RFC [3101](https://tools.ietf.org/html/rfc3101) - The OSPF Not-So-Stubby Area (NSSA) Option
- RFC [3630](https://tools.ietf.org/html/rfc3630) - Traffic Engineering (TE) Extensions to OSPF Version 2
- RFC [4577](https://tools.ietf.org/html/rfc4577) - OSPF as the Provider/Customer Edge Protocol for BGP/MPLS IP Virtual Private Networks (VPNs)
- RFC [5329](https://tools.ietf.org/html/rfc5329) - Traffic Engineering Extensions to OSPF Version 3
- RFC [5340](https://tools.ietf.org/html/rfc5340) - OSPF for IPv6
- RFC [5643](https://tools.ietf.org/html/rfc5643) - Management Information Base for OSPFv3
- RFC [6549](https://tools.ietf.org/html/rfc6549) - OSPFv2 Multi-Instance Extensions
- RFC [6565](https://tools.ietf.org/html/rfc6565) - OSPFv3 as a Provider Edge to Customer Edge (PE-CE) Routing Protocol
- RFC [6845](https://tools.ietf.org/html/rfc6845) - OSPF Hybrid Broadcast and Point-to-Multipoint Interface Type
- RFC [7471](https://tools.ietf.org/html/rfc7471) - OSPF Traffic Engineering (TE) Metric Extensions

# OSPF术语

在继续之前，先熟悉一下对理解OSPF的操作很重要的术语。这些术语将在整个文章中使用。

- **Neighbor** - 正在运行OSPF的连接（相邻）路由器，其相邻的接口被分配到同一区域。邻居是通过Hello数据包找到的（除了手动配置的）。
- **Adjacency** - 路由器与其对应的DR和BDR之间的逻辑连接。除非形成邻接，否则不交换路由信息。
- **Link** - 链接是指分配给任何特定网络的网络或路由器接口。
- **Interface** - 路由器上的物理接口。当接口被添加到OSPF时被认为是一个链接。用来建立链路数据库。
- **LSA** - 链接状态通告，数据包包含链接状态和路由信息，在OSPF邻居之间共享。
- **DR** - 指定的路由器，选择的路由器以最小化形成的邻接数量。该选项在广播网络中使用。
- **BDR** -后备指定路由器，DR的热备。BDR接收来自相邻路由器的所有路由更新，但它不泛滥LSA更新。
- **Area** - 区域被用来建立一个分层网络。
- **ABR** - 区域边界路由器，连接到多个区域的路由器。ABRs 负责连接区域之间的汇总和更新抑制。
- **ASBR** - 自治系统边界路由器，连接到外部网络（在不同的AS中）的路由器。如果你从路由器导入其他协议路由到OSPF，它现在被认为是ASBR。
- **NBMA** - 非广播多址，网络允许多址但没有广播能力。对于这些网络需要额外的OSPF邻居配置。
- **Broadcast** - 允许广播的网络，例如以太网。
- **Point-to-point** - 网络类型消除了对DR和BDR的需求
- **Router-ID** - 用来识别OSPF路由器的IP地址。如果OSPF Router-ID没有被手动配置，路由器使用分配给路由器的一个IP地址作为其Router-ID。
- **Link State** - 术语链接状态是指两个路由器之间链接的状态。它定义了一个路由器的接口和其相邻的路由器之间的关系。
- **Cost** - 链接状态协议给每个链接分配一个值，称为开销。开销值取决于媒体的速度。开销与每个路由器接口的外部相关联。这被称为接口输出开销。
- **Autonomous System** - 自治系统是一组使用共同路由协议交换路由信息的路由器。

# 基本配置实例

要启动OSPF v2和v3实例，首先要做的是添加实例和骨干区域：

```shell
/routing ospf instance
add name=v2inst version=2 router-id=1.2.3.4
add name=v3inst version=3 router-id=1.2.3.4
/routing ospf area
add name=backbone_v2 area-id=0.0.0.0 instance=v2inst
add name=backbone_v3 area-id=0.0.0.0 instance=v3inst
```

可以添加一个模板。模板用于匹配应该运行OSPF的接口，可以通过直接指定网络或接口来完成。

```shell
/routing ospf interface-template
add networks=192.168.0.0/24 area=backbone_v2
add networks=2001:db8::/64 area=backbone_v3
add interfaces=ether1 area=backbone_v3
```

# 路由表的计算

链路状态数据库描述了路由器和相互连接并适合转发的链路。它还包含每个链接的开销（metric）。这个开销用来计算到目标网络的最短路径。 
每个路由器都可以为自己的链接方向公布不同的开销，这使非对称链接成为可能（到目的地的数据包通过一条路径传输，但响应则通过不同的路径传输）。非对称路径不是很流行，因为它使人们更难发现路由问题。 
开销值可以在 [OSPF接口模板配置菜单](https://help.mikrotik.com/docs/display/ROS/OSPF#OSPF-InterfaceTemplates) 中改变，例如，添加一个开销为100的ether2接口：

```shell
/routing ospf interface-template
add interfaces=ether2 cost=100 area=backbone_v2
```

思科路由器上一个接口的开销与该接口的带宽成反比。较高的带宽表示较低的开销。如果在RouterOS上需要类似的开销，那么使用以下公式：

开销=100000000/bw，单位为bps。
  
OSPF路由器是使用Dijkstra的最短路径优先（SPF）算法来计算最短路径。该算法将路由器置于树的根部，并根据到达目的地所需的累积开销计算出到达每个目的地的最短路径。每个路由器都计算自己的树，即使所有路由器都使用相同的链路状态数据库。

## SPT计算

假设有以下网络。该网络由4（四）个路由器组成。出站接口的OSPF费用显示在代表链接的线附近。为了建立路由器R1的最短路径树，需要把R1作为根，并计算每个目的地的最小开销。

![](https://help.mikrotik.com/docs/download/attachments/9863229/image2020-2-26_11-9-11.png?version=3&modificationDate=1621333788215&api=v2)![](https://help.mikrotik.com/docs/download/attachments/9863229/image2020-2-26_11-9-32.png?version=5&modificationDate=1621333798873&api=v2)

从上图可以看出，已经找到了多条通往172.16.1.0网络的最短路径，允许对通往该目的地的流量进行负载平衡，称为 [等成本多路径（ECMP）](https://help.mikrotik.com/docs/display/ROS/How+Packets+Are+Routed#HowPacketsAreRouted-Multipath(ECMP)route) 。最短路径树建立后，路由器开始建立相应的路由表。网络会根据树上计算的成本到达。

路由表的计算看起来很简单，但是，当使用一些OSPF扩展或计算OSPF区域时，路由计算会变得更加复杂。

## 转发地址

OSPF路由器可以将转发地址设置为除自己以外的其他地址，这表明有可能存在另一个下一跳。大多数转发地址被设置为 **0.0.0.0**，表明该路由只能通过通告路由器到达。

如果满足以下条件，转发地址将设置在LSA中：

- 必须在下一跳接口上启用OSPF
- 下一跳地址落入OSPF网络提供的网络中

如果OSPF能够解析转发地址，收到这种LSA的路由器可以使用转发地址。如果转发地址没有被直接解析-路由器将LSA中转发地址的节点设置为网关，如果转发地址没有被解析-网关将是发起人ID。解析只发生在OSPF实例路由中，而不是整个路由表中。
  
看看下面的例子设置：

![](https://help.mikrotik.com/docs/download/attachments/9863229/Ospf-forwarding-traffic.png?version=1&modificationDate=1671111904418&api=v2)

路由器R1有一个静态路由到外部网络192.168.0.0/24。OSPF在R1、R2和R3之间运行，静态路由分布在OSPF网络中。

这种设置的问题很明显，R2不能直接到达外部网络。从R2到LAN网络的流量将通过路由器R1转发，但如果看一下网络图，就会发现更多的R2可以直接到达LAN网络所在的路由器。
  
所以知道了转发地址的条件，可以让路由器R1来设置转发地址。只需要在路由器的R1配置中把10.1.101.0/24网络加入OSPF网络：

```shell
/routing/ospf/interface-template add area=backbone_v2 networks=10.1.101.0/24
```

现在验证一下转发地址是否在工作： 

```shell
[admin@r2] /ip/route> print where dst-address=192.168.0.0/24
Flags: D - DYNAMIC; A - ACTIVE; o, y - COPY
Columns: DST-ADDRESS, GATEWAY, DISTANCE
    DST-ADDRESS       GATEWAY            DISTANCE
DAo 192.168.0.0/24    10.1.101.1%ether1       110
```

在所有的OSPF路由器上可以看到LSA设置的转发地址不是0.0.0.0。

```shell
[admin@r2] /routing/ospf/lsa> print where id=192.168.0.0
Flags: S - self-originated, F - flushing, W - wraparound; D - dynamic
 
 1  D instance=default_ip4 type="external" originator=10.1.101.10 id=192.168.0.0
      sequence=0x80000001 age=19 checksum=0xF336 body=
        options=E
        netmask=255.255.255.0
        forwarding-address=10.1.101.1
        metric=10 type-1
        route-tag=0
```

10.1.101.0/24网络中的路由器之间的OSPF邻接是不需要的

# 邻居关系和毗邻关系

OSPF是一个链接状态协议，它假定路由器的接口被认为是OSPF链接。每当OSPF启动时，它在本地链接状态数据库中添加所有链接的状态。

在OSPF网络变得完全有效之前，有几个步骤：

- 邻里发现
- 数据库同步
- 路由计算

链路状态路由协议是分发和复制描述路由拓扑结构的数据库。链路状态协议的泛滥算法确保每个路由器都有一个相同的链路状态数据库，路由表是根据这个数据库计算的。

在上述所有步骤完成后，每个邻居的链路状态数据库包含完整的路由域拓扑结构（网络中还有多少个路由器，路由器有多少个接口，路由器之间有哪些网络链接，每个链接的开销等等）。

## OSPF路由器之间的通信

OSPF使用协议号89在IP网络层上运行。 
一个目标IP地址被设置为邻居的IP地址或OSPF多播地址之一AllSPFRouters（224.0.0.5）或AllDRRouters（224.0.0.6）。这些地址的使用将在本文的后面描述。 
每个OSPF数据包以一个标准的24字节的头开始。

![](https://help.mikrotik.com/docs/download/attachments/9863229/OSPF_Header.png?version=1&modificationDate=1576853835217&api=v2)

| 字段                      | 说明                                                                                                                                                              |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Packet type**           | OSPF数据包有几种类型： Hello包，数据库描述（DD）包，链路状态请求包，链路状态更新包，以及链路状态确认包。除了Hello数据包，所有这些数据包都用于链路状态数据库同步。 |
| **Router ID**             | 路由器的一个IP地址，除了手动配置的。                                                                                                                              |
| **Area ID**               | 允许OSPF路由器将数据包关联到适当的OSPF区域。                                                                                                                      |
| **Checksum**              | 允许接收路由器确定数据包是否在传输过程中被损坏。                                                                                                                  |
| **Authentication fields** | 这些字段允许接收路由器验证数据包的内容没有被修改，并且数据包确实来自路由器ID出现在数据包中的OSPF路由器。                                                          |

有五种不同的OSPF数据包类型，用于确保在OSPF网络上正确地泛滥LSA。

- **Hello packet** - 用于发现OSPF邻居并建立邻接关系。
- **数据库描述（DD）** - 检查路由器之间的数据库同步情况。在建立邻接关系后进行交换。
- **链接状态请求（LSR）** - 用于请求邻居的数据库的最新部分。路由数据库的过期部分在DD交换后确定。
- 链接状态更新（LSU）** - 携带特别请求的链接状态记录的集合。
- **链接状态确认（LSack）** - 用于确认其他数据包类型，从而引入可靠的通信。

## 邻居发现

OSPF通过定期从配置的接口发送Hello包来发现潜在的邻居。默认情况下Hello数据包是以10秒的间隔发送的，可以通过在OSPF接口设置中设置 [hello-interval](https://help.mikrotik.com/docs/display/ROS/OSPF#OSPF-InterfaceTemplates) 来改变。当路由器收到邻居的 "hello "时，它就会知道邻居的存在，并返回匹配的参数。

Hello包的发送和接收也允许路由器检测邻居的故障。如果在 [dead-interval](https://help.mikrotik.com/docs/display/ROS/OSPF#OSPF-InterfaceTemplates) (默认为40秒)内没有收到Hello数据包，路由器就开始绕过故障路由数据包。"Hello "协议确保相邻的路由器在Hello间隔和Dead间隔参数上达成一致，防止不及时收到的Hello数据包错误地导致链路中断的情况。

![](https://help.mikrotik.com/docs/download/attachments/9863229/Hello_data.png?version=2&modificationDate=1576854102846&api=v2)

| 字段                     | 说明                                                                   |
| ------------------------ | ---------------------------------------------------------------------- |
| **network mask**         | 发端路由器的接口IP地址掩码                                             |
| **hello interval**       | Hello数据包的间隔时间(默认为10s)                                       |
| **options**              | OSPF邻居信息选项                                                       |
| **router priority**      | 一个8位值，帮助选举DR和BDR。(不在p2p链接中设置)                        |
| **router dead interval** | 必须在收到时间间隔后才会认为邻居已经死机。(默认情况下是Hello间隔的4倍) |
| **DR**                   | 当前DR的路由器ID                                                       |
| **BDR**                  | 当前BDR的路由器ID                                                      |
| **Neighbor router IDs**  | 所有发端路由器的邻居路由器ID列表                                       |

在每种类型的网段上，Hello协议的工作方式有些不同。很明显，在点对点网段上只有一个邻居是可能的，不需要额外的动作。然而，如果在网段上可以有一个以上的邻居，则要采取额外的行动，使OSPF功能更加有效。

除非满足以下条件，否则两个路由器不会成为邻居。

- 路由器之间的双向通信是可能的。通过泛滥的Hello数据包来确定。
- 接口应属于同一区域；
- 接口应该属于同一个子网，并且有相同的网络掩码，除非它的网络类型被配置为点对点；
- 路由器应该有相同的认证选项，并且必须交换相同的密码（如果有的话）；
- 在Hello数据包中，Hello和Dead的间隔应该是相同的；
- 在Hello数据包中，外部路由和NSSA标志应该是相同的。

网络掩码、优先级、DR和BDR字段仅在邻居由广播或NBMA网段连接时使用。

### 广播子网发现

广播子网的附加节点可以发送一个数据包，该数据包会被所有其他附加节点接收。这对于自动配置和信息复制是非常有用的。广播子网的另一个有用的能力是组播。这种能力允许发送一个单一的数据包，该数据包将被配置为接收多播数据包的节点所接收。OSPF正在使用这种能力来寻找OSPF邻居并检测双向连接。

考虑下图所示的以太网网络。

[图片](https://wiki.mikrotik.com/index.php?title=Special:Upload&wpDestFile=Ospf-bcast.png)

每个 OSPF 路由器都加入 IP 多播组 AllSPFRouters (224.0.0.5)，然后路由器定期将其 Hello 数据包多播到 IP 地址 224.0.0.5。 加入同一组的所有其他路由器将收到多播的 Hello 数据包。 这样，OSPF 路由器通过发送单个数据包而不是向网段上的每个邻居发送单独的数据包来维护与所有其他 OSPF 路由器的关系。

这种方法有几个优点：

通过多播或广播 Hello 数据包自动发现邻居。 与其他子网类型相比，带宽使用量更少。 在广播段上，有 n*(n-1)/2 个邻居关系，但这些关系是通过只发送 n 个 Hello 来维持的。 如果广播具有多播能力，则 OSPF 运行时不会干扰广播段上的非 OSPF 节点。 如果不支持多播功能，即使节点不是 OSPF 路由器，所有路由器都将接收广播的 Hello 数据包。

### 在 NBMA 子网上发现

非广播多路访问 (NBMA) 段类似于广播。 支持两个以上的路由器，唯一的区别是NBMA不支持数据链路广播能力。 由于此限制，必须首先通过配置发现 OSPF 邻居。 在 RouterOS 静态邻居配置中设置了 [/routing ospf static-neighbor](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328218#id-/routing/ospf-/routing/ospf/static-neighbor) 菜单。 为减少 Hello 流量，大多数连接到 NBMA 子网的路由器应分配为0的路由器优先级（在 RouterOS 中默认设置）。 有资格成为指定路由器的路由器的优先级值不应为0。它确保在DR和BDR选举期间，只向符合条件的路由器发送问候。

### 在 PTMP 子网上发现

点对多点将网络视为点对点链接的集合。

根据设计，PTMP 网络不应具有广播功能，这意味着必须首先通过配置发现 OSPF 邻居（与 NBMA 网络的方式相同），并且所有通信都是通过直接在邻居之间发送单播数据包来进行的。 在 RouterOS 静态邻居配置中设置 [/routing ospf static-neighbor](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328218#id-/routing/ospf-/routing/ospf/static-neighbor) 菜单。 点对多点子网上不选举指定路由器和备份指定路由器。

对于支持广播的PTMP网络，可以使用名为“ptmp-broadcast”的混合类型。 这种网络类型使用多播Hello来自动发现邻居并检测邻居之间的双向通信。 邻居检测后，“ptmp-broacast”将单播数据包直接发送到发现的邻居。 此模式与RouterOS v6“ptmp”类型兼容。

## 主从关系

在数据库同步开始之前，必须建立交换信息的层次结构顺序，这决定了哪个路由器首先发送数据库描述符DD数据包（Master）。 主路由器是根据最高优先级选出的，如果未设置优先级，则将使用路由器 ID。 请注意，它是一种基于路由器优先级的关系来安排邻居之间的交换数据，这不会影响 DR/BDR 选举（意味着DR并不总是必须是 Master）。

## 数据库同步

OSPF 路由器之间的链路状态数据库同步非常重要。 不同步的数据库可能会导致路由表计算错误，从而导致路由环路或黑洞。

有两种类型的数据库同步：

- 初始数据库同步
- 可靠的泛滥。

当两个邻居之间的连接首次出现时，_initial database synchronization_ 将会发生。 当邻居连接首次出现时，OSPF 使用显式数据库下载。 此过程称为 **数据库交换**。 OSPF 路由器不发送整个数据库，而是仅发送一系列 OSPF **数据库描述 (DD)** 数据包中的 LSA 标头。 只有当前一个数据包被确认时，路由器才会发送下一个 DD 数据包。 当收到完整的 DD 数据包序列时，路由器知道哪些 LSA 没有，哪些 LSA 是最近的。 然后，路由器发送 **链路状态请求 (LSR)** 数据包请求所需的 LSA，邻居通过在  **链路状态更新 (LSU)** 数据包中泛洪 LSA 进行响应。 在收到所有更新后，邻居被称为 **完全相邻**。

可靠洪泛是另一种数据库同步方法。 当邻接关系已经建立并且 OSPF 路由器想要通知其他路由器有关 LSA 更改时使用它。 当 OSPF 路由器收到这样的链路状态更新时，它会在链路状态数据库中安装一个新的 LSA，将确认数据包发送回发送方，将 LSA 重新打包到新的 LSU 中，并将其发送到除接收到该更新的接口之外的所有接口 首先是LSA。

OSPF 通过比较序列号来确定 LSA 是否是最新的。 序列号从0×80000001开始，数字越大，LSA越新。 每次记录被淹没时，序列号都会递增，并且接收更新的邻居会重置最大老化计时器。 LSA 每 30 分钟刷新一次，但如果不刷新，LSA 在数据库中的最长保留时间为 60 分钟。

数据库并不总是在所有 OSPF 邻居之间同步，OSPF 根据网段决定数据库是否需要同步，例如，在点对点链路上，数据库总是在路由器之间同步，但在以太网网络上，数据库在某些 邻居对。

### 广播子网上的同步

在广播网段上，有 n*(n-1)/2 个邻居关系，如果 OSPF 路由器尝试与广播网段上的每个 OSPF 路由器同步，将通过子网发送大量的链路状态更新和确认消息子网。

![](https://help.mikrotik.com/docs/download/attachments/9863229/Ospf-adjacency.jpg?version=1&modificationDate=1652186344641&api=v2)

这个问题通过为每个广播子网选择一个指定路由器和一个备份指定路由器来解决。 所有其他路由器仅与这两个选定路由器同步并形成邻接关系。 这种方法将邻接数从 n*(n-1)/2 减少到仅 2n-3。

右图说明了广播子网上的邻接结构。 路由器 R1 和 R2 分别是指定路由器和备份指定路由器。 例如，如果 R3 想要向 R1 和 R2 发送链路状态更新 (LSU)，路由器会将 LSU 发送到 IP 多播地址 AllDRouters (224.0.0.6)，并且只有 DR 和 BDR 侦听此多播地址。 然后 Designated Router 发送寻址到 AllSPFRouters 的 LSU，更新其余路由器。

#### DR选举

DR 和 BDR 路由器是根据 Hello 数据包中收到的数据选出的。 子网上的第一个 OSPF 路由器总是被选为指定路由器，当添加第二个路由器时，它成为备用指定路由器。 当现有 DR 或 BDR 出现故障时，将选择新的 DR 或 BDR 以考虑配置的 [路由器优先级](https://help.mikrotik.com/docs/display/ROS/OSPF#OSPF-InterfaceTemplates)。 具有最高优先级的路由器成为新的 DR 或 BDR。

作为指定路由器或备用指定路由器会消耗额外的资源。 如果 Router Priority 设置为0，则路由器不参与选举过程。 如果某些较慢的路由器不能成为 DR 或 BDR，这非常有用。

### 在 NBMA 子网上同步

NBMA 网络上的数据库同步类似于广播网络上的数据库同步。 选举 DR 和 BDR，最初仅与 DR 和 BDR 路由器交换数据库，并且泛洪总是通过 DR。 唯一的区别是链路状态更新必须被复制并分别发送到每个相邻路由器。

### 在 PTMP 子网上同步

在 PTMP 子网上，OSPF 路由器与它可以直接通信的所有其他路由相邻。

# 了解 OSPF 区域

OSPF 的一个显著特征是可以将 AS 划分为多个路由区域，这些路由区域包含它们自己的邻居集。
想象一个拥有 300 多个路由器和它们之间的多条链路的大型网络。 每当网络中发生链路抖动或其他一些拓扑变化时，这种变化将泛滥到网络中的所有 OSPF 设备，从而导致网络负载相当大，甚至停机，因为对于这么大的网络，网络收敛可能需要一些时间。

大型单区域网络会产生严重的问题：

- 每当网络拓扑发生变化时，每个路由器都会重新计算数据库，该过程占用 CPU 资源。
- 每个路由器都拥有一个完整的链路状态数据库，它显示了整个网络的拓扑结构，它占用内存资源。
- 路由表的完整副本和路由表条目的数量可能明显大于网络的数量，这会占用更多的内存资源。
- 更新大型数据库需要更多带宽。

区域的引入允许更好的资源管理，因为一个区域内的拓扑变化不会扩散到网络中的其他区域。 区域的概念可以简化网络管理以及区域之间的路由汇总，从而显着减少需要存储在每个 OSPF 邻居上的数据库大小。 这意味着每个区域都有自己的链路状态数据库和对应的最短路径树。

一个区域的结构对其他区域是不可见的。 如果使用多个区域，这种知识隔离使协议更具可扩展性； 路由表计算占用更少的CPU资源，减少路由流量。

但是，多区域设置会带来额外的复杂性。 不建议将少于 50 个路由器的区域分开。 一个区域中路由器的最大数量主要取决于用于路由表计算的 CPU 能力。

![](https://help.mikrotik.com/docs/download/attachments/9863229/OSPF_AREAS.png?version=1&modificationDate=1583499155552&api=v2)

OSPF 区域具有唯一的 32 位标识（区域 ID），区域 ID 为 0.0.0.0 的区域（称为骨干区域）是任何其他区域应该连接的主要区域。 连接多个区域的路由器称为ABR（Area Border Routers），它们的主要职责是连接区域之间的汇总和更新抑制。 连接到另一个路由域的路由器称为ASBR（Autonomous System Boundary Router）。

每个区域都有自己的链路状态数据库，由路由器 LSA 和网络 LSA 组成，描述该区域内所有路由器如何互连。 所有其他区域都隐藏了该区域拓扑的详细信息； router-LSAs 和 network-LSAs 不会扩散到区域边界之外。 区域边界路由器 (ABR) 在 OSPF 汇总 LSA 中将寻址信息从一个区域泄漏到另一个区域。 这允许人们在将数据从另一个区域转发到目的地时选择最佳区域边界路由器，称为区域内路由。

区域之间的路由信息交换本质上是一种距离矢量算法，为了防止算法收敛问题，例如计数到无穷大，所有区域都需要直接连接到骨干区域，形成一个简单的星型拓扑。 骨干区域的area-ID始终为0.0.0.0，不可更改。

RouterOS 区域配置在 `/routing/ospf/area` 菜单中完成。 例如，具有多个附加区域、一个 Stub 区域和一个默认区域的 ABR 路由器的配置：

```shell
/routing ospf area
add name=backbone_v2 area-id=0.0.0.0 instance=v2inst
add name=stub_area area-id=1.1.1.1 instance=v2inst type=stub
add name=another_area area-id=2.2.2.2 instance=v2inst type=default
```

OSPF 可以有 5 种类型的区域。 每个区域类型定义该区域支持的 LSA 类型：

- standard/default - 该区域可以正常传输OSPF报文，支持1、2、3、4、5类LSA
- 主干 - 如前所述，这是连接任何其他区域的主要区域。 它与标准区域基本相同，但标识为ID 0.0.0.0
- stub - 这个区域不接受任何外部路由
- totally stubby - 末节区域的变体
- not-so-stubby (NSSA) - 末节区域的变体

## LSA 类型

在我们继续详细了解每种区域类型之前，让我们先熟悉一下 LSA 类型：

- **type 1** - (Router LSA) 由区域内的路由器发送，包括直接连接的链接列表。 不要穿过 ABR 或 ASBR。
- **类型 2** -（网络 LSA）为区域内的每个“传输网络”生成。 一个传输网络至少有两个直接连接的 OSPF 路由器。 以太网是传输网络的一个例子。 类型 2 LSA 列出组成传输网络的每个连接路由器，由 DR 生成。
- **type 3** - (Summary LSA) ABR发送Type 3 Summary LSA。 类型 3 LSA 将一个区域拥有的任何网络通告给 OSPF AS 中的其余区域。 默认情况下，OSPF 为始发区域中定义的每个子网通告类型 3 LSA，这可能会导致泛洪问题，因此最好在 ABR 处使用手动汇总。
- **type 4** - (ASBR-Summary LSA) 它宣布 ASBR 地址，它显示 ASBR 所在的“位置”，宣布其地址而不是其路由表。
- _**type 5** -（外部 LSA）宣布通过 ASBR 获悉的路由，被泛洪到除存根区域之外的所有区域。 这个LSA分为两个子类型：**external type 1** 和 **external type 2**。
- **type 6** -（组成员 LSA）这是为 OSPF 的多播扩展定义的，RouterOS 不使用它。
- **type 7** - 类型 7 LSA 用于告知 ABR 有关这些引入 NSSA 区域的外部路由。 区域边界路由器然后将这些 LSA 转换为 **类型 5** 外部 LSA 并像往常一样泛洪到 OSPF 网络的其余部分
- **type 8** - 外部属性 LSA (OSPFv2) / 链路本地 LSA (OSPFv3)
- **type 9** - 链路本地范围不透明 (OSPFv2) / 区域内前缀 LSA (OSPFv3)。 这种类型的 LSA 不会扩散到本地（子）网络之外。
- **type 10** - 区域局部范围不透明。 这种类型的 LSA 不会超出其相关区域的范围。
- **type 11** - 在整个 AS 中泛洪的不透明 LSA（范围与 **type 5** 相同）。 它不会在存根区域和 NSSA 中被淹没。

如果没有ASBR，则网络中没有类型4和类型5的LSA。

## 标准面积

该区域支持1、2、3、4、5种LSA。

![](https://help.mikrotik.com/docs/download/attachments/9863229/Basic-multi-area.jpg?version=1&modificationDate=1652186431683&api=v2)

使用默认区域的简单多区域网络。本例中，来自area1的所有网络都被扩散到骨干网络，来自骨干网络的所有网络都被扩散到area1。
R1:

```shell
/ip address add address=10.0.3.1/24 interface=ether1
/ip address add address=10.0.2.1/24 interface=ether2
/routing ospf instance
add name=v2inst version=2 router-id=1.0.0.1
/routing ospf area
add name=backbone_v2 area-id=0.0.0.0 instance=v2inst
add name=area1 area-id=1.1.1.1 type=default instance=v2inst
/routing ospf interface-template
add networks=10.0.2.0/24 area=backbone_v2
add networks=10.0.3.0/24 area=area1
```

R2:

```shell
/ip address add address=10.0.1.1/24 interface=ether2
/ip address add address=10.0.2.2/24 interface=ether1
/routing ospf instance
add name=v2inst version=2 router-id=1.0.0.2
/routing ospf area
add name=backbone_v2 area-id=0.0.0.0
/routing ospf interface-template
add networks=10.0.2.0/24 area=backbone_v2
add networks=10.0.1.0/24 area=backbone_v2
```

R3:

```shell
/ip address add address=10.0.3.2/24 interface=ether2
/ip address add address=10.0.4.1/24 interface=ether1
/routing ospf instance
add name=v2inst version=2 router-id=1.0.0.3
/routing ospf area
add name=area1 area-id=1.1.1.1 type=stub instance=v2inst
/routing ospf interface-template
add networks=10.0.3.0/24 area=area1
add networks=10.0.4.0/24 area=area1
```

## Stub区域

stub区域的主要目的是防止这些区域携带外部路由。从这些区域到外部世界的路由基于缺省路由。stub区域减少了区域内数据库的大小，降低了区域内路由器对内存的需求。

![](https://help.mikrotik.com/docs/download/attachments/9863229/Stub-example.jpg?version=1&modificationDate=1652186474544&api=v2)

stub区域有一些限制，ASBR路由器不能进入该区域，stub区域不能作为虚连接的中转区域。由于stub区域主要配置为不承载外部路由，所以需要进行这些限制。

该区域支持1、2、3种LSA。

考虑一下上面的例子。Area1被配置为stub区域，这意味着路由器R2和R3将不会从骨干区域接收到除缺省路由以外的任何路由信息。

R1:

```shell
/routing ospf instance
add name=v2inst version=2 router-id=1.0.0.1
/routing ospf area
add name=backbone_v2 area-id=0.0.0.0 instance=v2inst
add name=area1 area-id=1.1.1.1 type=stub instance=v2inst
  
/routing ospf interface-template
add networks=10.0.0.0/24 area=backbone_v2
add networks=10.0.1.0/24 area=area1
add networks=10.0.3.0/24 area=area1
```

R2:

```shell
/routing ospf instance
add name=v2inst version=2 router-id=1.0.0.2
/routing ospf area
add name=area1 area-id=1.1.1.1 type=stub instance=v2inst
/routing ospf interface-template
add networks=10.0.1.0/24 area=area1
```

R3:

```shell
/routing ospf instance
add name=v2inst version=2 router-id=1.0.0.3
/routing ospf area
add name=area1 area-id=1.1.1.1 type=stub instance=v2inst
/routing ospf interface-template
add networks=10.0.3.0/24 area=area1
```

## 完全存根区

完全存根区是存根区的一个延伸。一个完全存根区域阻止外部路由和汇总（区间）路由进入该区域。只有区内路由被注入到该区域。完全存根区被配置为存根区，有一个额外的 "no-summaries "标志。这个区域支持1类、2类LSA和3类LSA与缺省路由。

```shell
/routing ospf area
add name=totally_stubby_area area-id=1.1.1.1 instance=v2inst type=stub no-summaries
```

## NSSA

当需要注入外部路由，但不需要注入type - 5 LSA路由时，NSSA (not -so-stubby area)非常有用。

![](https://help.mikrotik.com/docs/download/attachments/9863229/Nssa-example.jpg?version=1&modificationDate=1652186503863&api=v2)

该图显示了两个区域(骨干和area1)以及与位于“area1”的路由器的RIP连接。需要将“area1”配置为stub区域，但也需要在骨干区域注入外部RIP路由。此时应将Area1配置为NSSA。

 本配置举例不涉及 [RIP](https://help.mikrotik.com/docs/display/ROS/RIP) 的配置。
  
R1:

```shell
/routing ospf instance
add name=v2inst version=2 router-id=1.0.0.1
/routing ospf area
add name=backbone_v2 area-id=0.0.0.0 instance=v2inst
add name=area1 area-id=1.1.1.1 type=nssa instance=v2inst
/routing ospf interface-template
add networks=10.0.0.0/24 area=backbone_v2
add networks=10.0.1.0/24 area=area1
```

R2:

```shell
/routing ospf instance
add name=v2inst version=2 router-id=1.0.0.2
/routing ospf area
add name=area1 area-id=1.1.1.1 type=nssa instance=v2inst
/routing ospf interface-template
add networks=10.0.1.0/24 area=area1
```

不支持在NSSA区域使用虚连接。

外部路由信息和默认路由

在OSPF路由域的边缘，可以找到运行其中一种路由协议的AS边界路由器(asbr)。这些路由器的任务是将从其他路由协议中学到的路由信息引入OSPF路由域。外部路由可以根据度量类型在两个不同的级别上导入。

- type1 - OSPF度量值是OSPF内部开销和外部路由开销的总和
- type2 - OSPF的度量值只等于外部路由开销。

外部路由可以通过实例重分配参数导入。下面的例子将挑选并重新分配所有静态路由和RIP路由:

```shell
/routing ospf instance
add name=v2inst version=2 router-id=1.2.3.4 redistribute=static,rip
```

重新分配默认路由是一种特殊情况，应该使用' originate-default '参数:

```shell
/routing ospf instance
set v2inst originate-default=if-installed
```

由于重分发是由“originate-default”和“redistribute”参数控制的，因此引入了一些默认路由过滤的极端情况。

- 如果redistribute使能，则选择所有匹配redistribute参数的路由
- 如果“originate-default=never”，默认路由将被拒绝
- 通过' out-select-chain '运行所选路由(如果配置了)
- 通过out-filter-chain配置所选路由(如果配置了)
- 如果' originate-default '被设置为' always '或' if-installed ':
  - OSPF创建不带属性的假缺省路由;
  - 通过' out-filter-chain '运行此路由，其中可以应用属性，但忽略动作(总是接受);

有关重新分配值的完整列表，请参阅参考手册。

## 路由汇总

路由摘要是将多条路由合并到一个单独的通告中。它通常在区域边界(区域边界路由器)完成。

最好是沿着主干的方向总结。这样主干接收到所有聚合的路由，并将它们注入到其他已经汇总的区域。聚合有两种类型:区域间聚合和外部路由聚合。

区域间路由聚合作用于区域边界(abr)，不适用于通过重新分配注入OSPF的外部路由。缺省情况下，ABR为特定区域内的每条路由创建汇总LSA，并在相邻区域发布。

使用范围可以为多条路由只创建一条汇总 LSA，并且只向相邻区域发送一条通告，或者完全抑制通告。

如果配置了advertise参数，则如果该区域内存在路由，则对每个区域发布一条汇总LSA。否则(当advertise参数去使能时)不会创建汇总lsa并在区域边界外发布。

可以在 [OSPF区域范围](https://wiki.mikrotik.com/wiki/OSPF-reference#Area_Rangehttps://help.mikrotik.com/docs/display/ROS/OSPF#OSPF-AreaRange) 菜单中配置区域间路由聚合。

假设有两个区域backbone和area1, area1有几条来自10.0.0.0/16范围的/24路由，如果可以汇总，就不需要用每个/24子网淹没骨干区域。在连接area1和骨干网络的路由器上，可以设置区域范围:

```shell
/routing ospf area range
add prefix=10.0.0.0/16 area=area1 advertise=yes cost=10
```

对于一个活动范围(即至少有一条来自指定区域的OSPF路由落在它下面)，创建一条“黑洞”类型的路由并安装在路由表中。

外部路由聚合可以使用路由过滤器来实现。让我们考虑与上面相同的例子，只是area1重新分配了来自其他协议的/24路由。要发送一条汇总 - LSA，必须添加一条黑洞路由，并添加适当的路由过滤器，只接受汇总- LSA:

```shell
/ip route add dst-address=10.0.0.0/16 blackhole
/routing ospf instance
set v2inst out-filter-chain=ospf_out
/routing filter rule
add chain=ospf_out rule="if (dst == 10.0.0.0/16) {accept} else {reject}"
```

## 虚连接

正如前面提到的，所有OSPF区域都必须连接到骨干区域，但有时物理连接是不可能的。为了克服这个问题，可以通过使用虚拟链接来逻辑地连接区域。

使用虚连接的常见场景有两种:

- 将支离破碎的骨干区域粘合在一起
- 连接没有直接连接到骨干网的远程设备

![](https://help.mikrotik.com/docs/download/attachments/9863229/Vlink-backbone.jpg?version=1&modificationDate=1652186526347&api=v2)

### 分区主干

OSPF允许骨干区域中不连续的部分通过虚连接连接起来。当两个独立的OSPF网络合并为一个大网络时，可能需要这样做。可以在各个abr之间配置虚连接，这些abr与骨干区域相互接触，并且有一个公共区域。

如上图所示，当公共区域不存在时，额外的区域可以被创建为过境区域。

对非骨干区域进行分区时，不需要虚连接。OSPF不主动尝试修复区域分区，当一个区域被分区时，每个组件只是成为一个单独的区域。主干网在新区域之间进行路由。有些目的地可以通过区域内路由到达，区域分区需要区域间路由。

但是，为了在分区后保持完整的路由，地址范围不能在区域分区的多个组件之间分割。

![](https://help.mikrotik.com/docs/download/attachments/9863229/virtual-link2.jpg?version=1&modificationDate=1652188202645&api=v2)

### 没有物理连接到骨干网

当一个区域与骨干网没有物理连接时，虚连接可以为断开的区域的骨干网提供一条逻辑路径。必须在两个ABR之间建立一条链路，这些ABR有一个公共区域，其中一个ABR连接到主干。

可以看到R1和R2都是abr, R1连接到骨干区域。Area2将用作中转区，而R1是进入骨干区的入口点。两台路由器上都需要配置虚连接。

OSPF接口模板中添加虚连接配置。如果我们从“无物理连接”的例子中选择设置，那么虚拟链路的配置看起来是这样的:

R1:

```shell
/routing ospf interface-template
add vlink-transit-area=area2 area=backbone_v2 type=virtual-link vlink-neighbor-id=2.2.2.2
```

R2:

```shell
/routing ospf interface-template
add vlink-transit-area=area2 area=backbone_v2 type=virtual-link vlink-neighbor-id=1.1.1.1
```

# 属性参考

## 实例

**Sub-menu:** `/routing/ospf/instance`

| 属性                                                                              | 说明                                                                                                                                                                                                                                                    |
| --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **domain-id** (_Hex \| Address_)                                                  | mpls相关参数。标识实例所属的OSPF域。该值附加在作为VPNv4路由在BGP中重新分发的OSPF路由上，作为BGP扩展团体属性。当BGP VPNv4路由重新分发回OSPF时，使用该值来决定该路由是否生成区域间LSA或as -external LSA。缺省情况下，使用Null domain-id，如RFC 4577所述。 |
| **domain-tag** (_integer[0..4294967295]_)                                         | 如果设置，则用于路由重新分配(在该路由器生成的所有外部lsa中作为route-tag)和路由计算(所有具有此路由标签的外部lsa都被忽略)。需要和旧的思科系统互操作，缺省情况下不设置。                                                                                   |
| **in-filter** (_string_)                                                          | 用于传入前缀的 [路由过滤器](https://help.mikrotik.com/docs/display/ROS/Routing+Filters) 链的名称                                                                                                                                                        |
| **MPLS -te-address** (_string_)                                                   | 用于MPLS流量工程的区域。TE Opaque lsa是在该区域生成的。配置mpls-te-area的OSPF实例不能超过一个。                                                                                                                                                         |
| **MPLS -te-area** (_string_)                                                      | 用于MPLS流量工程的区域。TE Opaque lsa是在该区域生成的。配置mpls-te-area的OSPF实例不能超过一个。                                                                                                                                                         |
| **original -default** (_always \| if-installed \| never_;Default:**never**)       | 指定默认路由(0.0.0.0/0)的分发方式。                                                                                                                                                                                                                     |
| **out-filter-chain** (_name)                                                      | 用于过滤外发前缀的 [路由过滤器](https://help.mikrotik.com/docs/display/ROS/Routing+Filters) 链名                                                                                                                                                        |
| **out-filter-select** (_name)                                                     | 路由过滤器选择链的名称，用于输出选择                                                                                                                                                                                                                    |
| **redistribute** (_bgp，connected,copy,dhcp,fantasy,modem,ospf,rip,static,vpn_; ) | 启用特定路由类型的重分发。                                                                                                                                                                                                                              |
| **router-id** (_IP \| name_;Default:**main**)                                     | OSPF路由器ID。可以显式设置为IP地址，也可以设置为router-id实例的名称。                                                                                                                                                                                   |
| **version**(_2 \| 3;_Default:**2**)                                               | 此实例将运行的OSPF版本(IPv4为v2, IPv6为v3)。                                                                                                                                                                                                            |
| **vrf**(_name of a routing table_;Default:**main**)                               | 此OSPF实例运行的VRF表                                                                                                                                                                                                                                   |
| **use-dn** (_yes \| no_)                                                          | 强制使用或忽略DN位。在某些CE - PE场景下，可以将区域内路由注入VRF。如果不设置参数，则根据RFC使用DN位。从v6rc12开始可用。                                                                                                                                 |

### 注释

OSPF协议支持两种类型的度量:

- type1 - OSPF度量值是OSPF内部开销和外部路由开销的总和
- type2 - OSPF的度量值只等于外部路由开销。

## 区域

**Sub-menu:** `/routing/ospf/area`

| 属性                                                     | 说明                                                                                                                                                                                                                                                                                            |
| -------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **area-id** (_IP地址_;Default:**0.0.0.0**)               | OSPF区域标识符。如果路由器在多个区域中有网络，则必须始终存在一个area-id=0.0.0.0(骨干)的区域。主干总是包含所有的区域边界路由器。骨干网负责在非骨干区域之间分发路由信息。骨干网必须是连续的，即不能有断开的网段。但是，区域边界路由器不需要与骨干网物理连接，可以使用虚连接来模拟与骨干网的连接。 |
| **default-cost** (_integer_;unset)                       | 区域内注入lsa的缺省开销。如果不设置该值，则不会产生stub区域type-3缺省LSA。                                                                                                                                                                                                                      |
| **instance** (_name_;mandatory)                          | 该区域所属的OSPF实例名称。                                                                                                                                                                                                                                                                      |
| **no-summaries**()                                       | 标志参数，如果设置了该参数，则不扩散stub区域内的summary lsa。                                                                                                                                                                                                                                   |
| **name** (_string_)                                      | 区域名称                                                                                                                                                                                                                                                                                        |
| **nssa-translate** (_yes \| no \| candidate_)            | 该参数表示将使用哪个ABR作为type7到type5 LSA的转换器。仅当区域类型为NSSA时适用<br>- yes，路由器会一直被用作转换器<br>- no，路由器永远不会被用作转换器<br>- candidate - OSPF选择一个候选路由器作为转换器                                                                                          |
| **type** (_default \| nssa \| stub_;Default:**Default**) | 区域类型。阅读更多关于OSPF案例研究中的区域类型。                                                                                                                                                                                                                                                |

## 区域范围

**Sub-menu:** `/routing/ospf/area/range`

| 属性                                    | 说明                                                                             |
| --------------------------------------- | -------------------------------------------------------------------------------- |
| **advertise** (_yes \| no_;Default:yes) | 是否创建summary LSA并发布到邻近区域。                                            |
| **area** (_name_;mandatory)             | 与此范围关联的OSPF区域                                                           |
| **cost** (_integer[0..4294967295]_)     | 此范围将创建的汇总LSA的开销<br>Default -使用开销值最大的路由(即在此范围内的路由) |
| **prefix** (_IP prefix_; mandatory)     | 此范围的网络前缀                                                                 |

## 接口

**Sub-menu:** `/routing/ospf/interface`

只读匹配接口菜单

## 接口模板

**Sub-menu:** `/routing/ospf/interface-template`

接口模板定义了常见的网络和接口匹配，以及为匹配的接口分配的参数。

### 匹配器

| 属性                      | 说明                                                                                                                                                               |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **interfaces** (_name_)   | 要匹配的接口。接受指定的接口名称或接口列表的名称。                                                                                                                 |
| **network** (_IP prefix_) | 与该区域关联的网络前缀。在此范围内至少有一个地址的所有接口都会启动OSPF。请注意，此检查使用地址的网络前缀(即不是本地地址)。对于点到点接口，这意味着远程端点的地址。 |

### 指派参数

| 属性                                                                                                    | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| ------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **area** (_name_; mandatory)                                                                            | 匹配接口要关联到的OSPF区域。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| **auth** (_simple \| md5 \| sha1 \| sha256 \| sha384 \| sha512_)                                        | 指定OSPF协议消息的认证方式。<br>- simple -明文认证<br>- md5 - keyyed消息摘要5认证<br>- sha - HMAC-SHA认证RFC5709<br>如果未设置该参数，则不使用身份验证。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| **auth-id** (_integer_)                                                                                 | 密钥id用于计算消息摘要(启用MD5或SHA认证时使用)。该值应该匹配同一区域内的所有OSPF路由器。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| **authentication-key** (_string)_                                                                       | 要使用的认证密钥，必须在网段的所有邻居上匹配。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| **comment**(_string)_                                                                                   |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| **cost**(_integer[0..65535])_                                                                           | 以链路状态度量表示的接口开销。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| **dead-interval** (_time_;Default:**40s**)                                                              | 指定邻居被宣告死亡的时间间隔。该时间间隔在hello报文中发布。该值对于同一网络中的所有路由器必须相同，否则不会形成邻接关系                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| **disabled**(_yes \| no)_                                                                               |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| **hello-interval** (_time_;Default:**10s**)                                                             | 路由器发送该接口的HELLO报文间隔时间。该间隔越小，检测到拓扑变化的速度越快，权衡的是更多的OSPF协议流量。同一网络中的所有路由器必须设置相同的值，否则路由器之间不会形成邻接关系。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| **instance-id** (i_integer [0..255]_;Default:**0**)                                                     |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| **passive**()                                                                                           | 如果使能，则在匹配的接口上不发送或接收OSPF流量                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| **prefix-list** (name)                                                                                  | 需要发布到v3接口的网络的地址列表名称。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| **priority** (_integer: 0..255_; Default: **128**)                                                      | 路由器的优先级。用于确定广播网络中指定的路由器。优先级高的路由器优先。优先级值为0表示路由器根本没有资格成为指定或备份指定路由器。<br>ROS v7的默认值是128(在RFC中定义)，而ROS v6的默认值是1，如果您为DR/BDR选举设置了严格的优先级，请记住这一点。                                                                                                                                                                                                                                                                                                                                                                                                                               |
| **retransmit-interval** (_time_;Default:**5s**)                                                         | 丢失的lsa重新发送的时间间隔。当一台路由器向它的邻居发送一条LSA (link state advertisement)时，该LSA将一直保存到收到确认为止。如果没有及时收到确认(参见transmit-delay)，路由器将尝试重传LSA。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **transmit-delay** (_time_;Default:**1s**)                                                              | 链路状态发送延迟是接口发送链路状态更新报文所需的估计时间。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| **type** (_broadcast \| nbma \| ptp \| ptmp \| ptp-unnumbered \| virtual-link_; Default: **broadcast**) | 接口上的OSPF网络类型。注意，如果没有接口配置，则PtP接口的默认网络类型为“点对点”，其他所有接口的默认网络类型为“广播”。<br>- broadcast -网络类型适用于以太网和其他多播能力的链路层。选择指定路由器<br>- nbma -非广播多路接入。协议报文被发送到每个邻居的单播地址。需要手工配置邻居。选择指定路由器<br>- ptp -适用于只有两个节点的网络。不选择指定路由器<br>- ptmp -点到多点。比NBMA更容易配置，因为它不需要手动配置邻居。不要选择指定的路由器。这是最强大的网络类型，因此适用于无线网络，如果“广播”模式不能很好地为他们工作<br>- ptp-unnumbered -作用与ptp相同，只是远端邻居没有与特定ptp接口关联的IP地址。例如，在Cisco设备上使用未编号的IP。<br>- virtual-link用于建立虚连接。 |
| **vlink-neighbor-id** (_IP_)                                                                            | 虚连接邻居的 **router-id**。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| **vlink-transit-area** (_name)                                                                          | 两台路由器共有的非骨干区域，虚连接将建立在该区域上。stub区域不能建立虚连接。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |

## Lsa

**Sub-menu:** `/routing/ospf/lsa`

当前在LSA数据库中的所有LSA的只读列表。

| 属性                              | 说明                           |
| --------------------------------- | ------------------------------ |
| **age** (_integer_)               | 上次更新发生的时间(以秒为单位) |
| **area** (_string_)               | 该LSA所属的区域。              |
| **body** (_string_)               |                                |
| **checksum** (_string_)           | LSA校验和                      |
| **dynamic** (_yes \| no_)         |                                |
| **flushing** (_yes \| no_)        |                                |
| **id** (_IP_)                     | LSA记录id                      |
| **instance** (_string_)           | LSA所属的实例名。              |
| **link** (_string_)               |                                |
| **link-instance-id** (_IP_)       |                                |
| **originator** (_IP_)             | LSA记录的发起者。              |
| **self-originated** (_yes \| no_) | LSA是否来自路由器自身。        |
| **sequence** (_string_)           | 一条链路的LSA更新次数。        |
| **type** (_string_)               |                                |
| **wraparound** (_string_)         |                                |

## 邻居

**Sub-menu:** `/routing/ospf/neighbor`

当前激活的OSPF邻居的只读列表。

| 属性                                                                                     | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **address** (_IP_)                                                                       | OSPF邻居路由器的IP地址                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| **adjacency** (_time_)                                                                   | 自邻接关系形成以来经过的时间                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| **area** (_string_)                                                                      |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| **bdr** (_string_)                                                                       | 备份指定路由器的IP地址                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| **comment** (_string_)                                                                   |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| **db-summaries** (_integer_)                                                             |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| **dr** (_IP_)                                                                            | 指定路由器的IP地址                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| **dynamic** (_yes \| no_)                                                                |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| **inactive** (_yes \| no_)                                                               |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| **instance** (_string_)                                                                  |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| **ls-requests** (_integer_)                                                              |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| **ls-retransmits** (_integer_)                                                           |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| **priority** (_integer_)                                                                 | 邻居配置的优先级                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **router-id** (_IP_)                                                                     | 邻居路由器的RouterID                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| **state** (_down \| attempt \| init \| 2-way \| ExStart \| Exchange \| Loading \| full_) | - **Down** -没有收到邻居的Hello报文。<br>- **Attempt** -仅适用于NBMA云。表示最近没有收到邻居的信息。<br>- **Init** -收到邻居的Hello报文，但没有建立双向通信(RouterID不在Hello报文中列出)。<br>- **2-way** -双向通信已经建立。在此状态下进行DR和BDR选举，路由器根据路由器是DR还是BDR建立邻接关系，链路是点对点还是虚连接。<br>- **ExStart** -路由器尝试建立用于报文信息交换的初始序列号。ID较高的路由器成为主路由器并开始交换。<br>- **Exchange** -路由器交换DD (database description)报文。<br>- **Loading** -在此状态下交换实际的链路状态信息。Link State Request报文发送给邻居，请求在Exchange状态下发现新的lsa。<br>- **Full** -邻接状态完全，邻居路由器完全相邻。相邻路由器之间同步LSA信息。路由器只有在自己的DR和BDR中才能达到full状态，P2P链路除外。 |
| **state-changes** (_integer_)                                                            | OSPF自邻居识别以来状态变化的总数                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |

## 静态邻居配置

**Sub-menu:** `/routing/ospf/static-neighbor`

OSPF邻居的静态配置。适用于非广播多址网络。

| 属性                                           | 说明                                                                                                                        |
| ---------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| **address** (_IP%iface_;mandatory )            | 单播IP地址和接口，用来到达邻居的IP地址。例如，“address=1.2.3.4%ether1”表示在_ether1_接口上有IP地址为 _1.2.3.4_ 的邻居可达。 |
| **area** (_name_;mandatory )                   | 邻居所属区域名称。                                                                                                          |
| **comment** (_string)_                         |                                                                                                                             |
| **disabled** (_yes \| no)_                     |                                                                                                                             |
| **instance-id** (_integer [0..255]_;Default:0) |                                                                                                                             |
| **poll-interval** (_time_;Default:**2m**)      | 向处于“down”状态(即没有流量)的邻居发送hello消息的频率                                                                       |
