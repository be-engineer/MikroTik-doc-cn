# 概述

队列是一个数据包的集合，集体等待由网络设备使用预先定义的结构方法进行传输。队列工作原理基本与银行或超市使用的方法相同，即根据客户到来的先后进行处理。

队列用于：

- 限制某些IP地址、子网、协议、端口等的速率。
- 限制点对点的流量。
- 数据包优先级。
- 配置流量突发，进行流量加速。
- 应用不同的基于时间的限制。
- 在用户之间平等地分享可用的流量，或根据信道的负载情况来分享。

MikroTik RouterOS的队列实现是基于分层令牌桶（HTB）。HTB允许创建一个分层的队列结构并确定队列之间的关系。这些分层结构可以连接在两个不同的地方，[数据包流量图](https://help.mikrotik.com/docs/display/ROS/Packet+Flow+in+RouterOS) 说明了 _input_ 和 _postrouting_ 链。

在RouterOS中，有两种不同的方法来配置队列：

- **/queue simple** -旨在方便配置简单的、日常的队列任务（如单个客户上传/下载限制、P2P流量限制等）。
- **/queue tree** - 用于执行高级排队任务（如全局优先策略、用户组限制）。需要从 [/ip firewall mangle](https://help.mikrotik.com/docs/display/ROS/Basic+Concepts) 中标记数据包流量。

## 速率限制原则

速率限制用来控制网络接口上发送或接收流量的速率。小于等于指定速率的流量被发送，而超过该速率的流量则被丢弃或延迟。

速率限制可以通过两种方式进行：

1. 丢弃所有超过速率限制的数据包 - _**速率限制(丢弃或整形)**_ _（当队列大小=0时，100%的速率限制)_ 。
2. 将超过特定速率限制的数据包延迟在队列中，并在可能的情况下传输 _**速率均衡(调度器)**_ （当 _queue-size=unlimited_ 时，100%速率均衡）。

下图解释了 _速率限制_ 和 _速率均衡_ 之间的区别：

![](https://help.mikrotik.com/docs/download/attachments/328088/Image8001.png?version=2&modificationDate=1615377025309&api=v2)

正如所看到的，在第一种情况下，所有的流量都超过了特定的速率而被丢弃。在另一种情况下，流量超过了特定的速率，在队列中被延迟，以后再传输，但要注意，队列不满时数据包才会被延迟。如果队列缓冲区中没有更多的空间，数据包就会被丢弃。

对于每个队列，可以定义两个速率限制：

- **CIR** （承诺信息速率）-（RouterOS中的 **limit-at** ）最坏情况下，无论其他流量如何，该流量将获得这个速率。在任何时候带宽都不应该低于这个承诺速率。
- **MIR**  (最大信息速率) - (RouterOS中的 **max-limit** ) 最佳情况下，如果有空闲的带宽，流的最大可用速率。

## 简单队列

`/queue simple`

简单队列是一个简单的方式，用来限制特定目标的流量。此外，可以使用简单队列来建立先进的QoS应用程序，具有有用的功能：

- 点对点流量排队。
- 在选定的时间间隔上应用队列规则。
- 确定优先次序。
- 使用来自 _/ip firewall mangle_ 的多个数据包标记。
- 双向流量的整形（调度）（对上传+下载的总量有一个限制）。

简单的队列有一个严格的顺序-每个数据包必须经过队列，直到到达符合数据包参数条件的队列，或者直到到达队列列表的末端。例如，在有1000个队列的情况下，最后一个队列的数据包将需要通过999个队列才能到达目的地。

### 配置示例

在下面的例子中，有一个SOHO设备，有两个连接的单位PC和服务器。

![](https://help.mikrotik.com/docs/download/attachments/328088/Simple%20Queue.jpg?version=1&modificationDate=1571740133102&api=v2)

在这种情况下，有一个来自ISP的15Mbps的连接。要确保服务器收到足够的流量，需要配置一个简单的队列，其中有一个 _limit-at_ 参数，保证服务器收到5Mbps。

```shell
/queue simple
add limit-at=5M/5M max-limit=15M/15M name=queue1 target=192.168.88.251/32
```

这就是全部。服务器将获得5 Mbps的流量速率，而不考虑其他流量。如果使用的是默认配置，要确保为这一特定流量禁用FastTrack规则，否则它将绕过简单队列，无法工作。

## 队列树

`/queue tree`

队列树只在一个HTB中创建一个单向队列。这也是如何在一个单独的接口上添加队列的唯一方法。这样可以减轻配置上的纠结-不需要为下载和上传做单独的标记-上传会进入公共接口，下载会进入私有接口。与简单队列的主要区别是，队列树不是有序的-所有流量一起通过。

### 配置示例

在下面的例子中，将标记所有来自预先配置的 _in-interface-list=LAN_ 的数据包，并根据这些数据包标记用队列树限制流量。

创建一个防火墙地址列表：

```shell
[admin@MikroTik] > /ip firewall address-list
add address=www.youtube.com list=Youtube
[admin@MikroTik] > ip firewall address-list print
Flags: X - disabled, D - dynamic
 #   LIST                                                       ADDRESS                                                                        CREATION-TIME        TIMEOUT            
 0   Youtube                                                    www.youtube.com                                                                oct/17/2019 14:47:11
 1 D ;;; www.youtube.com
     Youtube                                                    216.58.211.14                                                                  oct/17/2019 14:47:11
 2 D ;;; www.youtube.com
     Youtube                                                    216.58.207.238                                                                 oct/17/2019 14:47:11
 3 D ;;; www.youtube.com
     Youtube                                                    216.58.207.206                                                                 oct/17/2019 14:47:11
 4 D ;;; www.youtube.com
     Youtube                                                    172.217.21.174                                                                 oct/17/2019 14:47:11
 5 D ;;; www.youtube.com
     Youtube                                                    216.58.211.142                                                                 oct/17/2019 14:47:11
 6 D ;;; www.youtube.com
     Youtube                                                    172.217.22.174                                                                 oct/17/2019 14:47:21
 7 D ;;; www.youtube.com
     Youtube                                                    172.217.21.142                                                                 oct/17/2019 14:52:21
```

用防火墙mangle标记数据包:

```shell
[admin@MikroTik] > /ip firewall mangle
add action=mark-packet chain=forward dst-address-list=Youtube in-interface-list=LAN new-packet-mark=pmark-Youtube passthrough=yes
```

根据之前标记的数据包配置队列树:

```shell
[admin@MikroTik] /queue tree
add max-limit=5M name=Limiting-Youtube packet-mark=pmark-Youtube parent=global
```

检查队列树的统计数据，确保流量是匹配的:

```shell
[admin@MikroTik] > queue tree print stats
Flags: X - disabled, I - invalid
 0   name="Limiting-Youtube" parent=global packet-mark=pmark-Youtube rate=0 packet-rate=0 queued-bytes=0 queued-packets=0 bytes=67887 packets=355 dropped=0
```

## 队列类型

`/queue type`

这个子菜单列出了默认创建的队列类型，允许添加新的用户特定队列。

默认情况下，RouterOS创建了以下预定义的队列类型：

```shell
[admin@MikroTik] > /queue type print
Flags: * - default
 0 * name="default" kind=pfifo pfifo-limit=50
 
 1 * name="ethernet-default" kind=pfifo pfifo-limit=50
 
 2 * name="wireless-default" kind=sfq sfq-perturb=5 sfq-allot=1514
 
 3 * name="synchronous-default" kind=red red-limit=60 red-min-threshold=10 red-max-threshold=50 red-burst=20 red-avg-packet=1000
 
 4 * name="hotspot-default" kind=sfq sfq-perturb=5 sfq-allot=1514
 
 5 * name="pcq-upload-default" kind=pcq pcq-rate=0 pcq-limit=50KiB pcq-classifier=src-address pcq-total-limit=2000KiB pcq-burst-rate=0 pcq-burst-threshold=0 pcq-burst-time=10s pcq-src-address-mask=32
     pcq-dst-address-mask=32 pcq-src-address6-mask=128 pcq-dst-address6-mask=128
 
 6 * name="pcq-download-default" kind=pcq pcq-rate=0 pcq-limit=50KiB pcq-classifier=dst-address pcq-total-limit=2000KiB pcq-burst-rate=0 pcq-burst-threshold=0 pcq-burst-time=10s pcq-src-address-mask=32
     pcq-dst-address-mask=32 pcq-src-address6-mask=128 pcq-dst-address6-mask=128
 
 7 * name="only-hardware-queue" kind=none
 
 8 * name="multi-queue-ethernet-default" kind=mq-pfifo mq-pfifo-limit=50
 
 9 * name="default-small" kind=pfifo pfifo-limit=10
```

所有的RouterBOARD都有默认的队列类型 "**only-hardware-queue**" 和 "kind=none"。"only-hardware-queue "使接口只有硬件传输描述符环形缓冲区，它本身就像一个队列。通常情况下，至少有100个数据包可以在发送描述符环形缓冲区中排队等待发送。对于不同类型的以太网MAC，传输描述符环形缓冲区的大小和可排队的数据包数量各不相同。软件队列对SMP系统不会特别有利，因为它消除了从不同的CPU/cores同步访问它的要求，这是资源密集型的。设置 "only-hardware-queue "需要以太网驱动程序支持，所以它只适用于某些以太网接口，主要是在RouterBOARD上。

一个 **multi-queue-ethernet-default** 在SMP系统上是有益的，该系统的以太网接口支持多个传输队列，并且有一个Linux驱动支持多个传输队列。为每个硬件队列配备一个软件队列，也许会减少同步访问它们的时间。

only-hardware-queue和multi-queue-ethernet-default的改进只有在没有"/queue tree "条目以特定接口为父级时才会出现。

### 种类

队列种类是数据包处理算法。类型描述了哪一个数据包将在队列中传送。RouterOS支持以下种类：

- FIFO (BFIFO, PFIFO, MQ PFIFO)
- RED
- SFQ
- PCQ

#### FIFO

这些种类基于FIFO算法（先进先出）。**PFIFO** 和 **BFIFO** 之间的区别是，一个是以数据包为单位，另一个是以字节为单位。这些队列使用 **pfifo-limit** 和 **bfifo-limit** 参数。

每一个不能排队的数据包（如果队列已满）都会被丢弃。大的队列规模会增加延迟，但可以更好地利用通道。

**MQ-PFIFO** 是 _pfifo_，支持多个发送队列。这种队列在具有以太网接口的SMP系统上是有益的，这些以太网接口支持多个发送队列，并且有支持多个发送队列的Linux驱动（主要在x86平台）。它使用 **mq-pfifo-limit** 参数。

#### RED

Random Early Drop 是一种队列机制，它试图通过控制平均队列大小来避免网络拥塞。 将平均队列大小与两个阈值进行比较：最小 (min\ :sub:`th`>)和最大(max<sub>th</sub>) 阈值。 如果平均队列大小 (avg<sub>q</sub>) 小于最小阈值，则不会丢弃任何数据包。 当平均队列大小大于最大阈值时，将丢弃所有传入数据包。 但是，如果平均队列大小介于最小和最大阈值之间，则数据包将以概率 P<sub>d</sub> 随机丢弃，其中概率是平均队列大小的函数：P<sub>d</sub> = P<sub>max</sub>(avg<sub>q</sub> – min<sub>th</sub>)/ (max<sub>th</sub> - min<sub>th</sub> >). 如果平均队列增长，则丢弃传入数据包的概率也会增长。 P<sub>max</sub> - ratio，可以调节丢包概率的陡峭性，（最简单的情况下P<sub>max</sub>可以等于1)。
图8.2显示了丢包概率的RED算法。

![](https://help.mikrotik.com/docs/download/attachments/328088/Image8002.png?version=2&modificationDate=1615377059686&api=v2)

#### SFQ

随机公平队列 (SFQ) 由哈希和循环算法确保。 SFQ 之所以被称为“随机”，是因为它并没有真正为每个流分配一个队列，它有一个算法，使用哈希算法将流量分配到有限数量的队列 (1024) 上。

流量可以由 4 个选项（_src-address、dst-address、src-port、_ 和 _dst-port_ ）唯一标识，因此 SFQ 哈希算法使用这些参数将数据包分类到 1024 个可能的子流之一 . 然后循环算法将开始向所有子流分配可用带宽，在每一轮中给出 **sfq-allot** 字节的流量。 整个SFQ队列可以包含128个数据包，有1024个子流可用。  
图8.3显示了 SFQ 操作：

![](https://help.mikrotik.com/docs/download/attachments/328088/Image8003.png?version=2&modificationDate=1615377078449&api=v2)

#### PCQ

PCQ 算法非常简单——首先，它使用选定的分类器将一个子流与另一个子流区分开来，然后对每个子流应用单独的 FIFO 队列大小和限制，然后将所有子流组合在一起并应用全局队列大小和限制 .

PCQ参数：

- **pcq-classifier** (dst-address | dst-port | src-address | src-port; default: "") : 选择子流标识符
- **pcq-rate** (数字): 每个子流的最大可用速率
- **pcq-limit**（数字):单个子流的队列大小（以 KiB 为单位）
- **pcq-total-limit** (数字): 所有子流中的最大排队量（以 KiB 为单位）

可以用 **pcq-rate** 选项为子流分配速度限制。 如果“pcq-rate=0”，子流将平均分配可用流量。

![](https://help.mikrotik.com/docs/download/attachments/328088/PCQ_Alg.png?version=3&modificationDate=1615377092954&api=v2)

例如，有一个 PCQ 队列和 100 个子流，而不是有 100 个下载限制为 1000kbps 的队列

PCQ 具有与简单队列和队列树相同的突发实现：

- **pcq-burst-rate**（数字）：允许子流突发时可以达到的最大上传/下载数据速率
- **pcq-burst-threshold**（数字）：这是突发开/关值
- **pcq-burst-time**（时间）：计算平均速率的时间段（以秒为单位）。 （不是实际突发的时间）

PCQ 还允许用不同大小的 IPv4 和 IPv6 网络作为子流标识符， 在它被锁定到单个 IP 地址之前。 这主要针对 IPv6 完成，因为从 ISP 的角度来看，客户将用 /64 网络表示，但客户网络中的设备是 /128。 PCQ 可用于这两种情况以及更多情况。 PCQ参数：

- **pcq-dst-address-mask**（数字）：用作 dst-address 子流标识符的 IPv4 网络的大小
- **pcq-src-address-mask**（数字）：用作 src-address 子流标识符的 IPv4 网络的大小
- **pcq-dst-address6-mask**（数字）：用作 dst-address 子流标识符的 IPV6 网络的大小
- **pcq-src-address6-mask**（数字）：用作 src-address 子流标识符的 IPV6 网络的大小

以下队列类型 CoDel、FQ-Codel 和 CAKE 从 RouterOS 版本 7.1beta3 开始可用。

#### CoDel

CoDel（Controlled-Delay Active Queue Management）算法使用局部最小队列作为持久队列的度量，类似地，它使用最小延迟参数作为保持队列延迟的度量。 队列大小是使用队列中的数据包停留时间计算的。

**属性**

| 属性                                       | 说明                                                                  |
| ------------------------------------------ | --------------------------------------------------------------------- |
| **codel-ce-threshold**（_default_：）      | 使用 ECN 标记高于配置阈值的数据包。                                   |
| **codel-ecn**（_default_：**no**）         | 用于标记数据包而不是丢弃它们。                                        |
| **codel-interval**（_default_：**100ms**） | 间隔要按照最坏情况 RTT 的顺序设置，通过瓶颈给端点足够的时间做出反应。 |
| **codel-limit** (_default_: **1000**)      | 队列限制，当达到限制时，传入的数据包将被丢弃。                        |
| **codel-target** (_default_: **5ms**)      | 表示可接受的最小持续队列延迟。                                        |

#### FQ-Codel

CoDel - 具有受控延迟 (CoDel) 的公平队列 (FQ) 使用随机确定的模型将传入数据包分类到不同的流中，并用于为使用队列的所有流提供公平的带宽份额。 每个流都使用内部 FIFO 算法的 CoDel 排队规则进行管理。

**属性**

| 属性                                          | 说明                                                                                              |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| **fq-codel-ce-threshold**（_default_：）      | 使用 ECN 标记高于设定阈值的数据包。                                                               |
| **fq-codel-ecn**（_default_：**yes**）        | 标记数据包而不是丢弃。                                                                            |
| **fq-codel-flows**（default：**1024**）       | 传入数据包分类的流的数量。                                                                        |
| **fq-codel-interval** (_default_: **100ms**)  | 间隔要按照最坏情况 RTT 的顺序设置，通过瓶颈给端点足够的时间做出反应。                             |
| **fq-codel-limit**（_default_：**10240**）    | 队列限制，当达到限制时，传入的数据包将被丢弃。                                                    |
| **fq-codel-memlimit**（default：**32.0MiB**） | 可以在此 FQ-CoDel 实例中排队的字节总数。 将从 _fq-codel-limit_ 参数强制执行。                     |
| **fq-codel-quantum**（_default_：**1514**）   | 在公平队列算法中用作“不足”的字节数。 默认值（1514 字节）对应以太网 MTU 加上 14 字节的硬件头长度。 |
| **fq-codel-target**（_default_：**5ms**）     | 表示可接受的最小持续队列延迟。                                                                    |

#### CAKE

CAKE-作为Linux内核的 _queue discipline_ （qdisc）实现的Common Applications Kept Enhanced（CAKE）使用COBALT（结合Codel和BLUE的AQM算法）和DRR++的一个变种进行流量隔离。换句话说，Cake的基本设计目标是用户友好性。所有的设置都是可选的；选择默认设置是为了在大多数常见的部署中更实用。在大多数情况下，配置只需要一个带宽参数就可以得到有用的结果。

**属性**

| 属性                                                                                                                              | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| --------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **cake-ack-filter** _(default:_ **none** )                                                                                        |
| **cake-atm** _(default:_ )                                                                                                        | 补偿ATM单元帧，这通常出现在ADSL链路上。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| **cake-autorate-ingress** _(yes\/no, default:_ )                                                                                  | 根据到达该qdisc的流量进行自动容量估计。这对蜂窝状链路有可能有用，因为蜂窝状链路的质量往往是随机变化的。 带宽限制参数可结合使用以指定一个初始估计值。整形器定期被设置为略低于估计速率的带宽。 评估器不能估计自己下游链路的带宽。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| **cake-bandwidth** _(default：_ )                                                                                                 | 设置整形器带宽。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| **cake-diffserv** _(default:_ **diffserv3**)                                                                                      | CAKE可以根据Diffserv字段将流量分为 "tins"。<br>- **diffserv4** 提供一个通用的Diffserv实现，有四个tins：Bulk（CS1），6.25%的阈值，一般为低优先级。Best effort（常规），100%阈值。Video（AF4x、AF3x、CS3、AF2x、CS2、TOS4、TOS1），50%阈值。Voice（CS7、CS6、EF、VA、CS5、CS4），25%阈值。<br>- **diffserv3** 默认提供一个简单的、通用的Diffserv实现，有三个门限。Bulk（CS1），6.25%阈值，一般为低优先级。Best effort（常规），100%阈值。Voice（CS7、CS6、EF、VA、TOS4），25%阈值，减少Codel间隔。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| **cake-flowmode** _(dsthost/dual-dsthost/dual-srchost/flowblind/flows/hosts/srchost/triple-isolate, default:_ **triple-isolate**) | - **flowblind** - 禁用流量隔离； 所有流量都通过tin队列。<br>- **srchost** - 流仅由源地址定义。<br>- **dsthost** 流仅由目标地址定义。<br>- **hosts** - 流由源-目标主机对定义。 这是主机隔离，而不是流隔离。<br>- **flows** - 流由源地址、目标地址、传输协议、源端口和目标端口的整个 5 元组定义。 这是 SFQ 和 fq_codel 执行的流隔离类型。<br>- **dual-srchost** 流由 5 元组定义，公平性首先应用于源地址，然后应用于各个流。 适用于从 LAN 到 Internet 的出口流量，它可以防止任何 LAN 主机独占上行链路，无论他们使用多少流量。<br>- **dual-dsthost** 流由 5 元组定义，公平性首先用于目标地址，然后用于各个流。 适用于从 Internet 到 LAN 的入口流量，它可以防止任何 LAN 主机独占下行链路，无论使用多少流量。<br>- **triple-isolate** - 流由 5 元组定义，公平性应用于源 *和* 目标地址智能（即不仅仅是主机对），也适用于单个流。<br>- **nat** 指示 Cake 在应用流隔离规则之前执行 NAT 查找，确定数据包的真实地址和端口号，提高 NAT“内部”主机之间的公平性。 这在“flowblind”或“flows”模式下没有实际效果，或者如果 NAT 在不同的主机上执行。<br>- **nonat**（默认）CAKE不会执行 NAT 查找。 流量隔离将使用 Cake 所连接的接口直接可见的地址和端口号来执行。 |
| **cake-memlimit** _(default:_ )                                                                                                   | 将 Cake 消耗的内存限制为 LIMIT 字节。 默认情况下，限制是根据带宽和 RTT 设置计算的。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **cake-mpu** _( -64 ... 256，default：_ )                                                                                         | 将每个数据包（包括开销）四舍五入到最小长度 BYTES。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| **cake-nat** _（default：_ **no**)                                                                                                | 指示 Cake 在应用流隔离规则之前执行 NAT 查找。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| **cake-overhead** _( -64 ... 256，default：_ )                                                                                    | 将 BYTES 添加到每个数据包的大小。 BYTES 可能为负数。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **cake-overhead-scheme** _（default：_）                                                                                          |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| **cake-rtt** _（default：_ **100 ms**）                                                                                           | 手动指定 RTT。 默认 100ms 适用于大多数 Internet 流量。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| **cake-rtt-scheme** _(datacentre/internet/interplanetary/lan/metro/none/oceanic/regional/satellite, default:_ )                   | - **datacentre** - 仅适用于极高性能的 10GigE+ 网络。 相当于 **RTT 100us**<br>- **lan** - 适用于家庭或办公室的纯以太网（非 Wi-Fi）网络。 在为 Internet 访问链接整形时不要使用它。 相当于 **RTT 1ms**<br>- **metro** - 主要用于单个城市内的交通。 相当于 **RTT** **10ms** **区域性** 适用于主要位于欧洲大小国家/地区内的流量。 相当于 **RTT 30ms**<br>- **internet**（默认）这适用于大多数 Internet 流量。 相当于 **RTT 100ms**<br>- **oceanic** - 对于延迟通常高于平均水平的互联网流量，例如澳大利亚居民遭受的延迟。 相当于 **RTT 300ms**<br>- **satellite** - 用于通过地球静止卫星进行的通信。 相当于 **RTT** **1000ms**<br>- **interplanetary** - 如此命名是因为木星距离地球约 1 光时。 用来（禁用 AQM 操作。 相当于 **RTT 3600s**                                                                                                                                                                                                                                                                                                                                                                                                           |
| **cake-wash** _（default：_ **no**）                                                                                              | 在优先级队列发生后，用清洗选项清除所有额外的 DiffServ（不包括 ECN 位）。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |

## 接口队列

`/queue interface`

在通过接口发送数据之前，由队列处理。 此子菜单列出了 RouterOS 中的所有可用接口，允许更改特定接口的队列类型。 该表是自动生成的。

```shell
[admin@MikroTik] > queue interface print
Columns: INTERFACE, QUEUE, ACTIVE-QUEUE
# INTERFACE QUEUE ACTIVE-QUEUE
0 ether1 only-hardware-queue only-hardware-queue
1 ether2 only-hardware-queue only-hardware-queue
2 ether3 only-hardware-queue only-hardware-queue
3 ether4 only-hardware-queue only-hardware-queue
4 ether5 only-hardware-queue only-hardware-queue
5 ether6 only-hardware-queue only-hardware-queue
6 ether7 only-hardware-queue only-hardware-queue
7 ether8 only-hardware-queue only-hardware-queue
8 ether9 only-hardware-queue only-hardware-queue
9 ether10 only-hardware-queue only-hardware-queue
10 sfp-sfpplus1 only-hardware-queue only-hardware-queue
11 wlan1 wireless-default wireless-default
12 wlan2 wireless-default wireless-default 
```
