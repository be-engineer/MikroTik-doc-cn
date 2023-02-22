# 概述

___

绑定是一种技术，允许把多个类似的以太网接口聚合到一个单一的虚拟链接中，从而获得更高的速率并提供故障转移功能。

接口绑定并不创建一个具有更大链接速度的接口。接口绑定创建了一个虚拟接口，可以在多个接口上实现流量的负载均衡。更多细节可以在 [LAG接口和负载平衡](https://help.mikrotik.com/docs/display/ROS/Layer2+misconfiguration#Layer2misconfiguration-LAGinterfacesandloadbalancing) 页面中找到。

CRS3xx、CRS5xx系列交换机和CCR2116、CCR2216路由器支持带有绑定接口的网桥硬件卸载。只有 "802.3ad "和 "balance-xor"绑定模式是硬件卸载的，其他绑定模式会使用CPU的资源。内置交换芯片始终使用Layer2+Layer3+Layer4的传输散列策略，手动改变传输散列策略没有效果。更多详情请见 [CRS3xx、CRS5xx、CCR2116、CCR2216交换芯片特性](https://help.mikrotik.com/docs/display/ROS/CRS3xx,+CRS5xx,+CCR2116,+CCR2216+switch+chip+features#CRS3xx,CRS5xx,CCR2116,CCR2216switchchipfeatures-Bonding)

## Quick Setup Guide

___

Let us assume that we have two Ethernet interfaces on each router (Router1 and Router2) and want to get the maximum data rate between these two routers. To make this possible, follow these steps:

1. Make sure that you do not have IP addresses on interfaces that will be enslaved for bonding interface.
2. Add bonding interface and IP address on the Router1:

```shell
/interface bonding add slaves=ether1,ether2 name=bond1
/ip address add address=172.16.0.1/24 interface=bond1
```

3. 在Router2上做同样的事:

```shell
/interface bonding add slaves=ether1,ether2 name=bond1
/ip address add address=172.16.0.2/24 interface=bond1
```

4. 从Router1测试连接:

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

第3和第4层的传输散列模式与LACP不完全兼容。更多细节可以在[https://www.kernel.org/doc/Documentation/networking/bonding.txt](https://www.kernel.org/doc/Documentation/networking/bonding.txt) 中找到。

### balance-xor

这种模式根据散列的协议头信息在活动端口之间平衡出站流量，并接受来自任何活动端口的入站流量。该模式与 [LACP](https://wiki.mikrotik.com/wiki/Manual:Interface/Bonding#802.3ad) 非常相似，只是它没有标准化，与 **Layer-3和-4** 的哈希策略一起工作。该模式可以和静态链路聚合组（LAG）接口一起工作。

### balance-rr

如果设置了这种模式，数据包会按顺序从第一个可用的从机到最后一个进行传输。balance-rr是唯一能在属于同一TCP/IP连接的多个接口上发送数据包的模式。当利用多条发送和多条接收链路时，数据包经常不按顺序接收，这会导致分段重传，对于其他协议，如UDP，如果客户端软件能容忍不按顺序的数据包，这不是问题。如果使用交换机将链路聚合在一起，那么就需要适当的交换机端口配置，然而许多交换机不支持balance-rr。[快速设置指南](https://wiki.mikrotik.com/wiki/Manual:Interface/Bonding#Quick_Setup_Guide) 演示了balance-rr绑定模式的用法。正如看到的，它的设置非常简单的。Balance-rr对于绑定几个无线链路也很有用，但是，它要求所有被绑定的链路有相同的带宽。如果一个绑定链路的带宽下降了，那么绑定的总带宽将等于最慢的绑定链路的带宽。

### active-backup

This mode uses only one active slave to transmit packets. The additional slave only becomes active if the primary slave fails. The MAC address of the bonding interface is presented onto the active port to avoid confusing the switch. Active-backup is the best choice in high availability setups with multiple switches that are interconnected.

The ARP monitoring in this mode will not work correctly if both routers are directly connected. In such setups, MII monitoring must be used or a switch should be put between routers.

### broadcast

When ports are configured with broadcast mode, all slave ports transmit the same packets to the destination to provide fault tolerance. This mode does not provide load balancing.

### balance-tlb

This mode balances outgoing traffic by peer. Each link can be a different speed and duplex mode and no specific switch configuration is required as for the other modes. The downside of this mode is that only MII link monitoring is supported (ARP link monitoring is ignored when configured) and incoming traffic is not balanced. Incoming traffic will use the link that is configured as "primary".

#### Configuration example

Let's assume that the router has two links - **ether1** max bandwidth is 10Mbps and **ether2** max bandwidth is 5Mbps. The first link has more bandwidth so we set it as a primary link:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bonding </code><code class="ros functions">add </code><code class="ros value">mode</code><code class="ros plain">=balance-tlb</code> <code class="ros value">slaves</code><code class="ros plain">=ether1,ether2</code> <code class="ros value">primary</code><code class="ros plain">=ether1</code></div></div></td></tr></tbody></table>

![](https://help.mikrotik.com/docs/download/attachments/8323193/Bon-tlb.jpg?version=1&modificationDate=1612794101762&api=v2)

No additional configuration is required for the switch. The image above illustrates how balance-tlb mode works. As you can see router can communicate to all the clients connected to the switch with a total bandwidth of both links (15Mbps). But as you already know, balance-tlb is not balancing incoming traffic. In our example, clients can communicate to the router with a total bandwidth of primary link which is 10Mbps in our configuration.

### balance-alb

The mode is basically the same as balance-tlb but incoming IPv4 traffic is also balanced. The receive load balancing is achieved by ARP negotiation. The bonding driver intercepts locally generated ARP messages on their way out and overwrites the source hardware address with the unique address of one of the slaves in the bond such that different peers use different hardware addresses. Only MII link monitoring is supported (ARP link monitoring is ignored when configured), the additional downside of this mode is that it requires device driver capability to change MAC address. The mode is not compatible with local-proxy-arp setting.

![](https://help.mikrotik.com/docs/download/attachments/8323193/Bon-alb.jpg?version=1&modificationDate=1612794108649&api=v2)  
The image above illustrates how balance-alb mode works. Compared to balance-tlb mode, traffic from clients can also use the secondary link to communicate with the router.

## Bonding monitoring

___

Since RouterOS 6.48 version, it is possible to monitor the bonding interface and bonding ports. For the `802.3ad` bonding mode, more detailed monitoring options are available.

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="text plain">/interface bonding monitor [find]</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">mode: 802.3ad&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; active-backup</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">active-ports: ether4&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ether6</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">ether5&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">inactive-ports:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ether7</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">lacp-system-id: CC:2D:E0:11:22:33</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">lacp-system-priority: 65535&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">lacp-partner-system-id: B8:69:F4:44:55:66</code></div></div></td></tr></tbody></table>

| Property                                   | Description                                                            |
| ------------------------------------------ | ---------------------------------------------------------------------- |
| **mode** (_802.3ad                         | active-backup                                                          | balance-alb | balance-rr | balance-tlb | balance-xor | broadcast_) | Used bonding mode |
| **active-ports** (_interface_)             | Shows the active bonding ports                                         |
| **inactive-ports** (_interface_)           | Shows the inactive bonding ports (e.g. a disabled or backup interface) |
| **lacp-system-id** (_MAC address_)         | Shows the local LACP system ID                                         |
| **lacp-system-priority** (_integer_)       | Shows the local LACP priority                                          |
| **lacp-partner-system-id** (_MAC address_) | Shows the partner LACP system ID                                       |

To monitor individual bonding ports, use a `monitor-slaves` command.

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="text plain">/interface bonding monitor-slaves bond1</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="text plain">Flags: A - active, P - partner</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;</code><code class="text plain">AP port=ether4 key=17 flags="A-GSCD--" partner-sys-id=D4:CA:6D:12:06:65 partner-sys-priority=65535 partner-key=9 partner-flags="A-GSCD--"</code></div><div class="line number4 index3 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;</code><code class="text plain">AP port=ether5 key=17 flags="A-GSCD--" partner-sys-id=D4:CA:6D:12:06:65 partner-sys-priority=65535 partner-key=9 partner-flags="A-GSCD--"</code></div></div></td></tr></tbody></table>

| Property               | Description                                                                                                                                                                                                                                           |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **port** (_interface_) | Used bonding port                                                                                                                                                                                                                                     |
| **key** (_integer_)    | Shows the local LACP aggregation key. The lower 6 bits are automatically assigned based on individual port link speed and duplex. The upper 10 bits can be manually specified using the `lacp-user-key` setting (available only since RouterOS v7.3). |
| **flags** (_string_)   |

Shows the local LACP flags:

A - activity (link is active, otherwise passive)  
T - timeout (link is using short 1-second timeout, otherwise using 30-second timeout)  
G - aggregation (link can be aggregatable)  
S - synchronization (link is synchronized)  
C - collecting (link is able to collect incoming frames)  
D - distributing (link is able to distribute outgoing frames)  
F - defaulted (link is using defaulted partner information, indicated that no LACPDU has been received from the partner)  
E - expired (link has expired state) |
| **partner-sys-id** (_MAC address_) | Shows the partner LACP system ID |
| **partner-sys-priority** (_integer_) | Shows the partner LACP priority |
| **partner-key** (_integer_) | Shows the partner LACP aggregation key |
| **partner-flags** (_string_) | Shows the partner LACP flags |

## Property Description

___

This section describes the available bonding settings. 

| Property           | Description |
| ------------------ | ----------- |
| **arp** (_disabled | enabled     | proxy-arp | reply-only_; Default: **enabled**) | Address Resolution Protocol for the interface. |
- disabled \- the interface will not use ARP
- enabled \- the interface will use ARP
- proxy-arp \- the interface will use the ARP proxy feature
- reply-only \- the interface will only reply to requests originated from matching IP address/MAC address combinations which are entered as static entries in the "/ip arp" table. No dynamic entries will be automatically stored in the "/ip arp" table. Therefore for communications to be successful, a valid static entry must already exist. |
| **arp-interval** (_time_; Default: **00:00:00.100**) | Time in milliseconds defines how often to monitor ARP requests |
| **arp-ip-targets** (_IP address_; Default: ) | IP target address which will be monitored if link-monitoring is set to arp. You can specify multiple IP addresses, separated by a comma |
| **comment** (_string_; Default: ) | Short description of the interface |
| **disabled** (_yes | no_; Default: **no**) | Changes whether the bonding interface is disabled |
| **down-delay** (_time_; Default: **00:00:00**) | If a link failure has been detected, the bonding interface is disabled for a down-delay time. The value should be a multiple of mii-interval, otherwise, it will be rounded down to the nearest value. This property only has an effect when `link-monitoring` is set to `mii`. |
| **forced-mac-address** (_MAC address_; Default: **none**) | By default, the bonding interface will use the MAC address of the first selected slave interface. This property allows to configure static MAC address for the bond interface (all zeros, broadcast or multicast addresses will not apply). RouterOS will automatically change the MAC address for slave interfaces and it will be visible in `/interface ethernet` configuration export |
| **lacp-rate** (_1sec | 30secs_; Default: **30secs**) | Link Aggregation Control Protocol rate specifies how often to exchange with LACPDUs between bonding peers. Used to determine whether a link is up or other changes have occurred in the network. LACP tries to adapt to these changes providing failover. |
| **lacp-user-key** (_integer: 0..1023_; Default: **0**) | Specifies the upper 10 bits of the port key. The lower 6 bits are automatically assigned based on individual port link speed and duplex. The setting is available only since RouterOS v7.3. |
| **link-monitoring** (_arp | mii | none_; Default: **mii**) | Method to use for monitoring the link (whether it is up or down)

- arp \- uses Address Resolution Protocol to determine whether the remote interface is reachable
- mii \- uses Media Independent Interface to determine link status. Link status determination relies on the device driver.
- none \- no method for link monitoring is used.

**Note:** some bonding modes require specific link monitoring to work properly. |
| **min-links** (_integer: 0..4294967295_; Default: **0**) | How many active slave links needed for bonding to become active |
| **mii-interval** (_time_; Default: **00:00:00.100**) | How often to monitor the link for failures (the parameter used only if link-monitoring is mii) |
| **mlag-id** (__integer: 0..4294967295_;_ Default:) | Changes MLAG ID for bonding interface. The same MLAG ID should be used on both peer devices to successfully create a single MLAG. See more details on [MLAG](https://help.mikrotik.com/docs/display/ROS/Multi-chassis+Link+Aggregation+Group). |
| **mode** (_802.3ad | active-backup | balance-alb | balance-rr | balance-tlb | balance-xor | broadcast_; Default: **balance-rr**) | Specifies one of the bonding policies

- 802.3ad \- IEEE 802.3ad dynamic link aggregation. In this mode, the interfaces are aggregated in a group where each slave shares the same speed. It provides fault tolerance and load balancing. Slave selection for outgoing traffic is done according to the transmit-hash-policy [more>](https://wiki.mikrotik.com/wiki/Manual:Interface/Bonding#802.3ad)
- active-backup \- provides link backup. Only one slave can be active at a time. Another slave only becomes active, if the first one fails. [more>](https://wiki.mikrotik.com/wiki/Manual:Interface/Bonding#active-backup)
- balance-alb \- adaptive load balancing. The same as balance-tlb but received traffic is also balanced. The device driver should have support for changing it's MAC address. [more>](https://wiki.mikrotik.com/wiki/Manual:Interface/Bonding#balance-alb)
- balance-rr \- round-robin load balancing. Slaves in a bonding interface will transmit and receive data in sequential order. It provides load balancing and fault tolerance. [more>](https://wiki.mikrotik.com/wiki/Manual:Interface/Bonding#balance-rr)
- balance-tlb \- Outgoing traffic is distributed according to the current load on each slave. Incoming traffic is not balanced and is received by the current slave. If receiving slave fails, then another slave takes the MAC address of the failed slave. [more>](https://wiki.mikrotik.com/wiki/Manual:Interface/Bonding#balance-tlb)
- balance-xor \- Transmit based on the selected transmit-hash-policy. This mode provides load balancing and fault tolerance. [more>](https://wiki.mikrotik.com/wiki/Manual:Interface/Bonding#balance-xor)
- broadcast \- Broadcasts the same data on all interfaces at once. This provides fault tolerance but slows down traffic throughput on some slow machines. [more>](https://wiki.mikrotik.com/wiki/Manual:Interface/Bonding#broadcast)

 |
| **mtu** (_integer_; Default: **1500**) | Maximum Transmit Unit in bytes. Must be smaller or equal to the smallest L2MTU value of a bonding slave. L2MTU of a bonding interface is determined by the lowest L2MTU value among its slave interfaces |
| **name** (_string_; Default: ) | Name of the bonding interface |
| **primary** (_string_; Default: **none**) | Controls the primary interface between active slave ports, works only for active-backup, balance-tlb and balance-alb modes. For active-backup mode, it controls which running interface is supposed to send and receive the traffic. For balance-tlb mode, it controls which running interface is supposed to receive all the traffic, but for balance-alb mode, it controls which interface is supposed to receive the unbalanced traffic (the non-IPv4 traffic). When none of the interfaces are selected as primary, device will automatically select the interface that is configured as the first one. |
| **slaves** (_string_; Default: **none**) | At least two ethernet-like interfaces separated by a comma, which will be used for bonding |
| **up-delay** (_time_; Default: **00:00:00**) | If a link has been brought up, the bonding interface is disabled for up-delay time and after this time it is enabled. The value should be a multiple of mii-interval, otherwise, it will be rounded down to the nearest value. This property only has an effect when `link-monitoring` is set to `mii`. |
| **transmit-hash-policy** (_layer-2 | layer-2-and-3 | layer-3-and-4_; Default: **layer-2**) | Selects the transmit hash policy to use for slave selection in balance-xor and 802.3ad modes

- layer-2 - Uses XOR of hardware MAC addresses to generate the hash. This algorithm will place all traffic to a particular network peer on the same slave. This algorithm is 802.3ad compliant.
- layer-2-and-3 - This policy uses a combination of layer2 and layer3 protocol information to generate the hash. Uses XOR of hardware MAC addresses and IP addresses to generate the hash. This algorithm will place all traffic to a particular network peer on the same slave. For non-IP traffic, the formula is the same as for the layer2 transmit hash policy. This policy is intended to provide a more balanced distribution of traffic than layer2 alone, especially in environments where a layer3 gateway device is required to reach most destinations. This algorithm is 802.3ad compliant.
- layer-3-and-4 - This policy uses upper layer protocol information, when available, to generate the hash. This allows for traffic to a particular network peer to span multiple slaves, although a single connection will not span multiple slaves. For fragmented TCP or UDP packets and all other IP protocol traffic, the source and destination port information is omitted. For non-IP traffic, the formula is the same as for the layer2 transmit hash policy. This algorithm is not fully 802.3ad compliant.|

## 参见

- [Bonding presentation at the MUM](https://wiki.mikrotik.com/images/f/f7/X1-Bondingv01.2006.pdf)
- [Bonding Examples](https://wiki.mikrotik.com/wiki/Bonding_Examples "Bonding Examples")