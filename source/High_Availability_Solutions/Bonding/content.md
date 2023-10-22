# 概述

___

绑定是一种技术，允许把多个类似的以太网接口聚合到一个单一的虚拟链接中，从而获得更高的速率并提供故障转移功能。

接口绑定并不创建一个具有更大链接速度的接口。接口绑定创建了一个虚拟接口，可以在多个接口上实现流量的负载均衡。更多细节可以在 [LAG接口和负载平衡](https://help.mikrotik.com/docs/display/ROS/Layer2+misconfiguration#Layer2misconfiguration-LAGinterfacesandloadbalancing) 页面中找到。

CRS3xx、CRS5xx系列交换机和CCR2116、CCR2216路由器支持带有绑定接口的网桥硬件卸载。只有 "802.3ad "和 "balance-xor"绑定模式是硬件卸载的，其他绑定模式会使用CPU的资源。内置交换芯片始终使用Layer2+Layer3+Layer4的传输散列策略，手动改变传输散列策略没有效果。更多详情请见 [CRS3xx、CRS5xx、CCR2116、CCR2216交换芯片特性](https://help.mikrotik.com/docs/display/ROS/CRS3xx,+CRS5xx,+CCR2116,+CCR2216+switch+chip+features#CRS3xx,CRS5xx,CCR2116,CCR2216switchchipfeatures-Bonding)

## 快速设置指南

___

假设每个路由器上有两个以太网接口（Router1 和 Router2），希望获得这两个路由器之间的最大速率。 按照下列步骤操作：

1.确保作为绑定接口从属的接口上没有 IP 地址。

2.在Router1上添加bonding接口和IP地址：

```shell
/interface bonding add slaves=ether1,ether2 name=bond1
/ip address add address=172.16.0.1/24 interface=bond1
```

3.在Router2上同样:

```shell
/interface bonding add slaves=ether1,ether2 name=bond1
/ip address add address=172.16.0.2/24 interface=bond1
```

4.从Router1测试连接:

```shell
[admin@Router1] > ping 172.16.0.2
  SEQ HOST                                 SIZE TTL TIME  STATUS                  
    0 172.16.0.2                             56  64 0ms 
    1 172.16.0.2                             56  64 0ms 
    2 172.16.0.2                             56  64 0ms 
    sent=3 received=3 packet-loss=0% min-rtt=0ms avg-rtt=0ms max-rtt=0ms
  ```

绑定接口需要几秒钟的时间来获得与对等点的连接。

## 链路监控

___

启用其中一个可用的链路监控选项是非常关键的。在上面的例子中，如果其中一个绑定的链路发生故障，绑定驱动仍会继续在故障链路上发送数据包，这会导致网络性能下降。RouterOS中的绑定支持两种方案来监控从属设备的链路状态。MII和ARP监控。由于绑定驱动程序的限制，不能同时使用这两种方法。

### ARP监控

ARP监测发送ARP查询，并用响应作为链路运行的指示。ARP回复没有被验证，从属接口收到的任何数据包都会导致从属接口被认为是活动的。这就保证了流量确实在链路上流动。如果设置了balance-rr和balance-xor模式，那么交换机应该配置为在所有链路上均匀地分配数据包。否则，所有来自ARP目标的回复都将在同一个链路上收到，这可能导致其他链路失效。ARP监控是通过设置三个属性来启用的-链路监控、arp-ip-targets和arp-interval。每个选项的含义将在本文后面描述。可以指定多个ARP目标，这在高可用性设置中很有用。如果只设置了一个目标，那么目标本身就可能失效。额外的目标可以增加ARP监控的可靠性。

在Router1上启用ARP监控:

`/interface bonding set [find name=bond1] link-monitoring=arp arp-ip-targets=172.16.0.2`

Router2:

`/interface bonding set [find name=bond1] link-monitoring=arp arp-ip-targets=172.16.0.1`

在这个例子中不会改变arp-interval的值，RouterOS默认将arp-interval设置为100ms。拔掉其中一根电缆，测试链路监控是否正常工作，可能会有一些ping超时，直到arp监控检测到链路故障。

```shell
[admin@MikroTik] > ping 172.16.0.2
  SEQ HOST                                     SIZE TTL TIME  STATUS                                
    0 172.16.0.2                                 56  64 0ms 
    1 172.16.0.2                                 56  64 0ms 
    2 172.16.0.2                                 56  64 0ms 
    3 172.16.0.2                                 56  64 0ms 
    4 172.16.0.2                                              timeout                               
    5 172.16.0.2                                 56  64 0ms 
    6 172.16.0.2                                 56  64 0ms 
    sent=7 received=6 packet-loss=14% min-rtt=0ms avg-rtt=0ms max-rtt=0ms
```

为了使ARP监控正常工作，不需要在设备上设置任何IP地址，无论在任何接口上设置了什么IP地址，ARP监控都会工作。

当使用ARP监控时，即使在和arp-ip-targets相同的子网中的VLAN接口上设置了IP地址，绑定从机也会发出没有VLAN标记的ARP请求。

### MII监控

MII监控只监控本地接口的状态。_MII Type 1_ - 设备驱动程序决定一个链接是向上还是向下。如果设备驱动程序不支持这个选项，那么链路就会显示为总是向上。主要的缺点是，MII监控无法判断链路是否真的可以传递数据包，即使链路被检测为向上。MII监控是通过设置变量来配置的，这些变量是link-monitoring和mii-interval。

要在Router1和Router2上启用MII Type1监控:

`/interface bonding set [find name=bond1] link-monitoring=mii`

We will leave mii-interval to its default value (100ms). When unplugging one of the cables, the failure will be detected almost instantly compared to ARP link monitoring.

## 绑定模式

___

### 802.3ad

802.3ad模式是一个IEEE标准，也叫LACP（链路聚合控制协议）。包括聚合的自动配置，因此需要对交换机进行最小的配置。标准还规定，帧将按顺序传送，连接不应出现数据包的错误排序。标准还规定，聚合中的所有设备必须以相同的速度和双工模式运行。

LACP根据散列的协议头信息在活动端口之间均衡出站流量，并接受来自任何活动端口的入站流量。哈希值包括以太网源和目标地址，如果有的话，还包括VLAN标签，以及IPv4/IPv6源和目标地址。如何计算取决于传输哈希策略参数。不建议使用ARP链路监控，因为LACP对等设备上的发送散列策略，ARP回复可能只到达一个从属端口。可能导致不平衡的传输流量，推荐使用MII链路监控。

第3和第4层的传输散列模式与LACP不完全兼容。更多细节可以在 [https://www.kernel.org/doc/Documentation/networking/bonding.txt](https://www.kernel.org/doc/Documentation/networking/bonding.txt) 中找到。

### balance-xor

这种模式根据散列的协议头信息在活动端口之间平衡出站流量，并接受来自任何活动端口的入站流量。该模式与 [LACP](https://wiki.mikrotik.com/wiki/Manual:Interface/Bonding#802.3ad) 非常相似，只是它没有标准化，与 **Layer-3和-4** 的哈希策略一起工作。该模式可以和静态链路聚合组（LAG）接口一起工作。

### balance-rr

如果设置了这种模式，数据包会按顺序从第一个可用的从机到最后一个进行传输。balance-rr是唯一能在属于同一TCP/IP连接的多个接口上发送数据包的模式。当利用多条发送和多条接收链路时，数据包经常不按顺序接收，这会导致分段重传，对于其他协议，如UDP，如果客户端软件能容忍不按顺序的数据包，这不是问题。如果使用交换机将链路聚合在一起，那么就需要适当的交换机端口配置，然而许多交换机不支持balance-rr。[快速设置指南](https://wiki.mikrotik.com/wiki/Manual:Interface/Bonding#Quick_Setup_Guide) 演示了balance-rr绑定模式的用法。正如看到的，它的设置非常简单的。Balance-rr对于绑定几个无线链路也很有用，但是，它要求所有被绑定的链路有相同的带宽。如果一个绑定链路的带宽下降了，那么绑定的总带宽将等于最慢的绑定链路的带宽。

### 主动-备份

该模式只使用活动从属设备来传输数据包。额外的从属设备只在主从属设备发生故障时才成为活动的。绑定接口的MAC地址会呈现在活动端口上以避免混淆交换机。主动备份是具有多个互连的交换机的高可用性设置中的最佳选择。

如果两个路由器是直连的，这种模式下的ARP监控将不能正确工作。在这种设置中，必须使用MII监控，或者在路由器之间放一个交换机。

### 广播

当端口配置为广播模式时，所有从属端口都向目的地传输相同的数据包来提供容错。这种模式不提供负载平衡。

### balance-tlb

这种模式按对等出站流量进行均衡。每个链路可以是不同的速度和双工模式，不需要像其他模式那样对交换机进行特定的配置。这种模式的缺点是只支持MII链路监控（配置时忽略ARP链路监控），而且传入流量不均衡。传入流量使用配置为 "主要"的链路。

#### 配置示例

假设路由器有两条链路 - **ether1** 最大带宽是10Mbps，**ether2** 最大带宽是5Mbps。第一条链路有更多的带宽，所以把它设置为主链路:

`/interface bonding add mode=balance-tlb slaves=ether1,ether2 primary=ether1`

![](https://help.mikrotik.com/docs/download/attachments/8323193/Bon-tlb.jpg?version=1&modificationDate=1612794101762&api=v2)

交换机不需要额外的配置。上面的图片说明了balance-tlb模式是如何工作的。可以看到路由器可以用两条链路的总带宽（15Mbps）和连接到交换机的所有客户进行通信。但balance-tlb并不均衡传入流量。在这个例子中，客户可以用主链路的总带宽和路由器通信，在这个配置中，主链路的带宽是10Mbps。

### balance-alb

该模式和balance-tlb基本相同，但传入的IPv4流量也被均衡。接收负载均衡是通过ARP协商实现的。绑定驱动程序拦截本地生成的ARP信息，用绑定的一个从机的唯一地址覆盖源硬件地址，这样不同的对等体使用不同的硬件地址。只支持MII链路监控（ARP链路监控在配置时被忽略），这种模式的额外缺点是需要设备驱动能力来改变MAC地址。该模式和local-proxy-arp设置不兼容。

![](https://help.mikrotik.com/docs/download/attachments/8323193/Bon-alb.jpg?version=1&modificationDate=1612794108649&api=v2)  

上面的图片说明了balance-alb模式的工作原理。和balance-tlb模式相比，来自客户端的流量也可以使用二级链路与路由器通信。

## 绑定监控

___

从RouterOS 6.48版本开始，可以对绑定接口和绑定端口进行监控。对于 `802.3ad` 绑定模式，有更详细的监控选项。

```shell
/interface bonding monitor [find]
                      mode: 802.3ad           active-backup
              active-ports: ether4            ether6
                            ether5           
            inactive-ports:                   ether7
            lacp-system-id: CC:2D:E0:11:22:33
      lacp-system-priority: 65535            
    lacp-partner-system-id: B8:69:F4:44:55:66
```

| 属性                                                                                                          | 说明                                       |
| ------------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| **mode** (_802.3ad \| active-backup \| balance-alb \| balance-rr \| balance-tlb \| balance-xor \| broadcast_) | 使用的绑定模式                             |
| **active-ports** (_interface_)                                                                                | 显示活动的绑定端口                         |
| **inactive-ports** (_interface_)                                                                              | 显示不活动的绑定端口(例如，禁用或备份接口) |
| **lacp-system-id** (_MAC address_)                                                                            | 显示本地LACP系统ID                         |
| **lacp-system-priority** (_integer_)                                                                          | 显示本地LACP的优先级                       |
| **lacp-partner-system-id** (_MAC address_)                                                                    | 显示合作伙伴的LACP系统ID                   |

要监控单个绑定的端口，请使用 `monitor-slaves` 命令。

```shell
/interface bonding monitor-slaves bond1
Flags: A - active, P - partner
 AP port=ether4 key=17 flags="A-GSCD--" partner-sys-id=D4:CA:6D:12:06:65 partner-sys-priority=65535 partner-key=9 partner-flags="A-GSCD--"
 
 AP port=ether5 key=17 flags="A-GSCD--" partner-sys-id=D4:CA:6D:12:06:65 partner-sys-priority=65535 partner-key=9 partner-flags="A-GSCD--"
```

| 属性                                 | 说明                                                                                                                                                                                                                                                                                                                                                        |
| ------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **port** (_interface_)               | 使用的绑定端口                                                                                                                                                                                                                                                                                                                                              |
| **key** (_integer_)                  | 显示本地LACP聚合密钥。低6位是根据各个端口的链路速度和双工自动分配的。高10位可以使用 `lacp-user-key` 设置手动指定（从RouterOS v7.3开始可用）。                                                                                                                                                                                                               |
| **flags** (_string_)                 | 显示本地LACP的标志。<br>A - 活动 (链接是活动的，否则是被动的)  <br>T - 超时(链路使用短的1秒超时，否则使用30秒超时)  <br>G - 聚合(链路可以是聚合的)  <br>S--同步(链路是同步的)  <br>C - 手机 (链路能够收集传入的帧)  <br>D - 分布(链路能够分布传出的帧)  <br>F - 默认的 (链路使用默认的伙伴信息，表示没有收到伙伴的LACPDU)  <br>E - 过期（链路处于过期状态） |
| **partner-sys-id** (_MAC address_)   | 显示合作伙伴的LACP系统ID                                                                                                                                                                                                                                                                                                                                    |
| **partner-sys-priority** (_integer_) | 显示合作伙伴的LACP优先级                                                                                                                                                                                                                                                                                                                                    |
| **partner-key** (_integer_)          | 显示合作伙伴的LACP聚合密钥                                                                                                                                                                                                                                                                                                                                  |
| **partner-flags** (_string_)         | 显示合作伙伴的LACP标志                                                                                                                                                                                                                                                                                                                                      |

## 属性说明

___

本节介绍了可用的绑定设置。

| 属性                                                                                                                                   | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| -------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **arp** (_disabled \| enabled \| proxy-arp \| reply-only_; Default: **enabled**)                                                       | 接口的地址解析协议。<br>- disabled - 接口不使用ARP<br>- enabled - 接口使用ARP<br>- proxy-arp - 接口使用ARP代理功能<br>- reply-only - 接口只回复来自匹配的IP地址/MAC地址组合的请求，这些组合在"/ip arp "表中输入为静态条目。动态条目不会自动存储在"/ip arp "表中。因此，要使通信成功，必须已经存在一个有效的静态条目。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| **arp-interval** (_time_; Default: **00:00:00.100**)                                                                                   | 以毫秒为单位的时间，定义监控ARP请求的频率                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| **arp-ip-targets** (_IP address_; Default: )                                                                                           | link-monitoring设置为arp时，要监测的IP目标地址。可以指定多个IP地址，用逗号隔开                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| **comment** (_string_; Default: )                                                                                                      | 接口的简短说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| **disabled** (_yes \| no_; Default: **no**)                                                                                            | 改变绑定接口是否被禁用                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| **down-delay** (_time_; Default: **00:00:00**)                                                                                         | 如果检测到链路故障，绑定接口将禁用一个down-delay时间。该值是mii-interval的倍数，否则会被四舍五入到最近的值。这个属性只有在 `link-monitoring` 被设置为 `mii` 时才有效                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| **forced-mac-address** (_MAC address_; Default: **none**)                                                                              | 默认情况下，绑定接口使用第一个选定的从属接口的MAC地址。这个属性允许为绑定接口配置静态MAC地址（全零、广播或多播地址不适用）。RouterOS自动改变从属接口的MAC地址，并在 `/interface ethernet` 配置中可见                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| **lacp-rate** (_1sec \| 30secs_; Default: **30secs**)                                                                                  | 链路聚合控制协议速率指定在绑定对等体之间交换LACPDU的频率。用于确定链路是否是上行或网络中是否发生了其他变化。LACP试图适应这些变化以提供故障转移。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| **lacp-user-key** (_integer: 0...1023_; Default: **0**)                                                                                | 指定端口密钥的高10位。低6位是根据各个端口的链路速度和双工自动分配的。该设置仅从RouterOS v7.3以后可用。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| **link-monitoring** (_arp \| mii \| none_; Default: **mii**)                                                                           | 监测链路的方法（无论是上行还是下行）。<br>- arp - 用地址解析协议来确定远程接口是否可达<br>- mii - 用媒体独立接口来确定链接状态。链接状态的确定依赖于设备驱动程序。<br>- none - 不使用链路监控方法。<br>**注意：** 某些绑定模式需要特定的链路监控才能正常工作。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| **min-links** (_integer: 0...4294967295_; Default: **0**)                                                                              | 绑定需要多少个活跃的从属链路才算活跃                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| **mii-interval** (_time_; Default: **00:00:00.100**)                                                                                   | 监测链路故障的频率（该参数仅在链路监测为mii时使用）                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| **mlag-id** (_integer: 0...4294967295_;Default:)                                                                                       | 更改绑定接口的MLAG ID。两个对等设备上要用相同的MLAG ID来成功创建一个MLAG。参见 [MLAG](https://help.mikrotik.com/docs/display/ROS/Multi-chassis+Link+Aggregation+Group) 的更多细节。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| **mode** (_802.3ad \| active-backup \| balance-alb \| balance-rr \| balance-tlb \| balance-xor \| broadcast_; Default: **balance-rr**) | 指定一个绑定策略:<br>- 802.3ad - IEEE 802.3ad动态链路聚合。在此模式下，接口聚合在一个组中，每个从属设备共享相同的速度。提供容错和负载均衡。根据传输哈希政策 [more>](https://wiki.mikrotik.com/wiki/Manual:Interface/Bonding#802.3ad)，对出站流量进行从属选择。<br>- active-backup - 提供链路备份。一次只能有一个从属设备是活动的。另一个从站只有在第一个从站发生故障时才会变成活动的。[more>](https://wiki.mikrotik.com/wiki/Manual:Interface/Bonding#active-backup)<br>- balance-alb - 自适应负载均衡。与 balance-tlb 相同，但接收的流量也是均衡的。设备驱动程序应该支持改变它的MAC地址。[more>](https://wiki.mikrotik.com/wiki/Manual:Interface/Bonding#balance-alb)<br>- balance-rr - 轮流负载均衡。绑定接口中的从机将按顺序发送和接收数据。它提供了负载均衡和容错功能。[more>](https://wiki.mikrotik.com/wiki/Manual:Interface/Bonding#balance-rr)<br>- balance-tlb - 传出的流量根据每个从属设备上的当前负载来分配。进入的流量不均衡，由当前的从属设备接收。如果接收的从属设备出现故障，那么另一个从属设备就会占用故障从属设备的MAC地址。[more>](https://wiki.mikrotik.com/wiki/Manual:Interface/Bonding#balance-tlb)<br>- balance-xor - 基于选定的传输哈希策略进行传输。这种模式提供负载均衡和容错。[more>](https://wiki.mikrotik.com/wiki/Manual:Interface/Bonding#balance-xor)<br>- broadcast - 一次在所有接口上广播相同的数据。提供了容错功能，但在一些慢速机器上会减慢流量吞吐量。[more>](https://wiki.mikrotik.com/wiki/Manual:Interface/Bonding#broadcast) |
| **mtu** (_integer_; Default: **1500**)                                                                                                 | 以字节为单位的最大传输单元。必须小于或等于绑定从属接口的最小L2MTU值。绑定接口的L2MTU是由从属接口中最低的L2MTU值决定的                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| **name** (_string_; Default: )                                                                                                         | 绑定接口名称                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **primary** (_string_; Default: **none**)                                                                                              | 控制活动从属端口之间的主接口，只对active-backup、balance-tlb和balance-alb模式起作用。对于active-backup模式，它控制哪个运行接口应该发送和接收流量。对于balance-tlb模式，它控制哪个运行接口应该接收所有流量，但对于balance-alb模式，它控制哪个接口应该接收不均衡的流量（非IPv4流量）。当没有接口选为主接口时，设备会自动选择配置为第一的接口。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **slaves** (_string_; Default: **none**)                                                                                               | 至少两个用逗号隔开的类似于以太网的接口，用于绑定                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| **up-delay** (_time_; Default: **00:00:00**)                                                                                           | 如果链路被提升，绑定接口会在up-delay时间内被禁用，在这个时间之后，它会被启用。该值是mii-interval的倍数，否则将被四舍五入到最近的值。这个属性只有在 `link-monitoring` 设置为 `mii` 时才有用。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **transmit-hash-policy** (_layer-2 \| layer-2-and-3 \| layer-3-and-4_; Default: **layer-2**)                                           | 选择在balance-xor和802.3ad模式下用于从属选择的传输哈希策略<br>- layer-2 - 用硬件MAC地址的XOR来生成哈希值。这种算法把所有到一个特定网络对等体的流量放在同一个从属设备上。这种算法符合802.3ad标准。<br>- layer-2-and-3 - 该策略用第2层和第3层协议信息的组合来生成哈希值。使用硬件MAC地址和IP地址的XOR来生成哈希值。这种算法将把所有到某一网络对等体的流量放在同一从机上。对于非IP流量，公式与第二层传输哈希策略相同。该策略提供比单独的第二层更均衡的流量分配，特别是需要第三层网关设备到达大多数目的地的环境中。这种算法符合802.3ad标准。<br>- layer-3-and-4 - 该策略使用上层协议信息（如果可用）来生成哈希值。允许到一个特定网络对等体的流量跨越多个从属体，尽管一个连接不会跨越多个从属体。对于碎片化的TCP或UDP数据包和所有其他IP协议流量，源和目的端口信息被省略。对于非IP流量，其公式与第二层传输散列策略相同。这种算法不完全符合802.3ad标准。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |

## 参见

- [Bonding presentation at the MUM](https://wiki.mikrotik.com/images/f/f7/X1-Bondingv01.2006.pdf)
- [Bonding Examples](https://wiki.mikrotik.com/wiki/Bonding_Examples "Bonding Examples")
