# 概述

协议独立组播-稀疏模式（PIM-SM或PIM）使RouterOS能够支持网络区域的组播流。几个配置好的PIM路由器将组成一个多播云，客户设备可以使用IGMP来管理流订阅。当网络拓扑结构复杂或流源被连接到多播云时，应使用PIM。连续云必须为组播组配置一个独特的会合点，其他参与者应该知道如何到达会合点。简单情况下，在网络的部分可能只居住着潜在的客户，而没有源，那么可以用 [IGMP代理](https://help.mikrotik.com/docs/display/ROS/IGMP+Proxy) 来代替，以保存资源。

该功能不支持SMIPS设备（hAP lite、hAP lite TC和hAP mini）。

# 属性参考

## 实例

实例菜单定义了主要的 PIM-SM 设置。然后该实例用于所有其他与 PIM 相关的配置，如接口模板、静态 RP 和 Bootstrap Router。

**Sub-menu:** `/routing pimsm instance`


| 属性                                                                                              | 说明                                                                                                                                              |
| ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| **afi** (_ipv4 \| ipv6_; Default: **ipv4**)                                                       | 指定PIM的地址族。                                                                                                                                 |
| **bsm-forward-back** (_yes \| no_;Default: )                                                      | 目前没有实现。                                                                                                                                    |
| **crp-advertise-contained** (_yes \| no_; Default: )                                              | 目前没有实现。                                                                                                                                    |
| **name** (_text_; Default: )                                                                      | 实例名称。                                                                                                                                        |
| **rp-hash-mask-length** (_integer： 0...4294967295_; Default： **30**（IPv4），或**126**（IPv6）) | 哈希掩码允许改变多少个组来映射到一个匹配的RP。                                                                                                    |
| **rp-static-override** (_yes \| no_; Default: **no**)                                             | 改变静态RP的选择优先级。当禁用时，自举RP集有更高的优先级。当启用时，静态RP有更高的优先级。                                                        |
| **ssm-range** (_IPv4 \| IPv6_; Default: )                                                         | 目前没有实现。                                                                                                                                    |
| **switch-to-spt** (_yes \| no_; Default: **yes**)                                                 | 如果达到组播数据带宽阈值，是否切换到最短路径树（SPT）。如果该选项被禁用，路由器将不会从协议第一阶段（注册封装）进入本地组播流量。建议启用该选项。 |
| **switch-to-spt-bytes** (_integer: 0...4294967295_; Default: **0**)                               | 多播数据带宽阈值。如果在指定的时间间隔内达到这个阈值，就会切换到最短路径树（SPT）。如果配置的值为0，则切换将立即发生。                            |
| **switch-to-spt-interval** (_time_; Default: )                                                    | 考虑多播数据带宽的时间间隔，与 `switch-to-spt-bytes` 一起使用，以确定是否达到切换阈值。                                                           |
| **vrf** (_name_; Default: main)                                                                   | VRF的名称。                                                                                                                                       |

## 接口模板

接口模板菜单定义了哪些接口将参与PIM，以及每个接口将使用什么配置。

**Sub-menu:** `/routing pimsm interface-template`


| 属性                                                      | 说明                                                                                                                                                                                                                                                          |
| --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **hello-delay** (_time_; Default: **5s**)                 | 接口启动或检测新邻居时初始Hello消息的随机化间隔。                                                                                                                                                                                                             |
| **hello-period** (_time_; Default: **30s*)                | Hello信息的周期性间隔。                                                                                                                                                                                                                                       |
| **instance** (_name_; Default: )                          | 接口模板所属的PIM实例名称。                                                                                                                                                                                                                                   |
| **interfaces** (_name_; Default: **all**)                 | 参与PIM的接口列表。                                                                                                                                                                                                                                           |
| **join-prune-period** (_time_; Default: **1m**)           |                                                                                                                                                                                                                                                               |
| **join-tracking-support** (_yes \| no_; Default: **yes**) | 设置Hello消息中LAN Prune Delay选项的跟踪（T）位的值。启用时，路由器宣传它愿意禁用加入抑制，如果加入抑制被禁用，上游路由器有可能明确地跟踪各个下游路由器的加入成员。 除非一条链路上的所有PIM路由器都协商了这种能力，否则显式跟踪和禁用加入抑制机制是不可用的。 |
| **overrid-interval** (_time_; Default: **2s500ms**)       | 设置最大的时间段，在启用了连接抑制的网络上调度延迟覆盖的连接信息时，要随机化。                                                                                                                                                                                |
| **priority** (_integer: 0...4294967295_; Default: **1**)  | 指定路由器（DR）的优先级。每个网络上都会选出一个指定的路由器。只有在所有邻居都公布了优先权选项时，才会使用该优先权。数字上最大的优先级是首选。如果出现平局或不使用优先权，则优先使用数字最大的IP地址。                                                        |
| **propagation-delay** (_time_; Default: **500ms**)        | 设置修剪等待计时器的值。它被上游路由器用来计算在修剪启用了连接抑制的接口之前，应该等待连接覆盖消息多长时间。                                                                                                                                                  |
| **source-addresses** (_IPv4 \| IPv6_; Default: )          |                                                                                                                                                                                                                                                               |

## 接口

接口菜单显示当前参与PIM的所有接口及其状态。这个菜单包含动态的和只读的条目，由定义的接口模板创建。

**Sub-menu:** `/routing pimsm interface`


| 属性                                    | 说明                        |
| --------------------------------------- | --------------------------- |
| **address** (_IP%interface@vrf_)        | 显示IP地址、接口和VRF。     |
| **designated-router** (_yes \| no_)     |                             |
| **dr** (_yes \| no_)                    |                             |
| **dynamic** (_yes \| no_)               |                             |
| **instance** (_name_)                   | 接口模板所属的PIM实例名称。 |
| **join-tracking** (_yes \| no_)         |                             |
| **override-interval** (_time_)          |                             |
| **priority** (_integer: 0..4294967295_) |                             |
| **propagation-delay** (_time_)          |                             |

## 邻居

邻居菜单显示所有检测到的正在运行PIM的邻居和它们的状态。该菜单包含动态和只读条目。

**Sub-menu:** `/routing pimsm neighbor`


| 属性                                     | 说明                                                                                                 |
| ---------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| **address** (_IP%interface_)             | 显示邻居的IP地址和邻居被检测到的本地接口。                                                           |
| **designated-router** (_YES \| NO_)      | 显示邻居是否被选为指定路由器（DR）。                                                                 |
| **instance** (_name_)                    | 检测到该邻居的PIM实例的名称。                                                                        |
| **join-tracking** (_yes \| no_)          | 显示邻居在Hello消息中的LAN Prune Delay选项中的跟踪（T）位的值。                                      |
| **overrid-interval** (_time_)            | 表示邻居在Hello消息中LAN Prune Delay选项中的覆盖间隔值。                                             |
| **priority** (_integer: 0...4294967295_) | 表示邻居的优先级值。                                                                                 |
| **propagation-delay** (_time_)           | 表示邻居在Hello消息中的LAN Prune Delay选项中的传播延迟值。                                           |
| **timeout** (_time_)                     | 显示如果没有收到新的Hello消息，邻居被从列表中删除后的提醒时间。保持时间等于邻居的 hello-period*3.5。 |

## 静态RP

static-rp菜单允许手动定义组播组与RP的映射关系。这种机制对故障并不健全，但至少提供了一个基本的互操作性机制。

**Sub-menu:** `/routing pimsm static-rp`


| 属性                                                 | 说明                      |
| ---------------------------------------------------- | ------------------------- |
| **address** (_IPv4 \| IPv6_; Default: )              | 静态RP的IP地址。          |
| **group** (_IPv4 \| IPv6_; Default: **224.0.0.0/4**) | 属于特定RP的组播组。      |
| **instance** (_name_; Default: )                     | 静态RP所属的PIM实例名称。 |

## 上游信息库

上游信息库菜单显示任意源组播(*,G)和特定源组播(S,G)组以及它们的状态。这些菜单只包含只读条目。

**Sub-menu:** `/routing pimsm uib-g`


| 属性                       | 说明                                                              |
| -------------------------- | ----------------------------------------------------------------- |
| **group** (_IPv4 \| IPv6_) | 组播组地址。                                                      |
| **instance** (_name_)      | 创建组播组的PIM实例名称。                                         |
| **rp** (_IPv4 \| IPv6_)    | 这个组的会合点地址。                                              |
| **rp-local** (_yes \| no_) | 表示组播路由器本身是否为RP。                                      |
| **rpf** (_IP%interface_)   | 反向路径转发(RPF)表示该组的加入信息所指向的路由器地址和出站接口。 |

**Sub-menu:** `/routing pimsm uib-sg`


| 属性                                           | 说明                                                                                                                                                                                                                                                                     |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **group** (_IPv4 \| IPv6_)                     | 组播组地址。                                                                                                                                                                                                                                                             |
| **instance** (_name_)                          | 创建组播组的PIM实例名称。                                                                                                                                                                                                                                                |
| **keepalive** (_yes \| no_)                    |                                                                                                                                                                                                                                                                          |
| **register** (_join \| join-pending \| prune_) |
| **rpf** (_IP%interface_)                       | 反向路径转发(RPF)表示该组的加入信息所指向的路由器地址和出站接口。                                                                                                                                                                                                        |
| **source** (_IPv4 \| IPv6_)                    | 组播组的源IP地址。                                                                                                                                                                                                                                                       |
| **spt-bit** (_yes \| no_)                      | 最短路径树(SPT)位表示转发是在(S,G)最短路径树上进行还是在(*,G)树上进行。一个路由器可以有一个(S,G)状态，并且在构建特定来源树的间隔期间，仍然在(*,G)状态上进行转发。当SPT位为假时，只有(*,G)转发状态被用来转发从S到G的数据包；当SPT位为真时，(*,G)和(S,G)转发状态都被使用。 |