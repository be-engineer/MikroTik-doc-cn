# 概述


互联网组管理协议（IGMP）代理可以实现组播路由。它在转发IGMP帧，通常在不需要PIM等更高级协议时使用。

**IGMP代理的特点：**

- 如何进行组播路由的最简单方法；
- 可用于PIM-SM因某种原因不适合的拓扑结构中；
- 占用的资源比PIM-SM略少；
- 易于配置。

另一方面，IGMP代理不是很适合复杂的组播路由设置。与基于PIM的解决方案相比，IGMP代理不支持一个以上的上游接口，而且不能检测或避免路由循环。

默认情况下，IGMP代理的上游接口将发送IGMPv3成员报告，将根据收到的查询，检测上游设备（如多播路由器）使用的是什么IGMP版本。如果收到IGMPv1/v2查询，上游端口将退回到较低的IGMP版本。当IGMPv1/v2查询器存在的计时器（400s）到期时，它将转换回IGMPv3。IGMP代理的下游接口将只发送IGMPv2查询。

RouterOS v7在主 **系统** 包中有IGMP代理配置。旧的RouterOS版本需要安装一个额外的 **multicast** 包，以便使用IGMP代理。请看更多关于 [包](https://help.mikrotik.com/docs/display/ROS/Packages) 的细节。

# 配置选项


常规IGMP代理配置

**Sub-menu:** `/routing igmp-proxy`

| 属性                                                            | 说明                                                                                                                                                                  |
| --------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **query-interval** (_time: 1s..1h_; Default: **2m5s**)          | 通过下游接口发送IGMP查询信息的频率。                                                                                                                                  |
| **query-response-interval** (_time: 1s...1h_; Default: **10s**) | 等待IGMP查询信息回复的时间。                                                                                                                                          |
| **quick-leave**                                                 | 指定对IGMP离开消息的操作。如果快速离开是开启的，那么一旦从下游接口的第一个客户端收到离开消息，就会向上游发送IGMP离开消息。仅在代理后面只有一个用户的情况下为 **是**。 |

配置哪些接口将作为路由器上的IGMP代理接口参与。如果一个接口没有被配置为IGMP代理接口，那么它收到的所有IGMP流量都将被忽略。

**Sub-menu:** `/routing igmp-proxy interface`

| 属性                                                                               | 说明                                                                                                                                                                                       |
| ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **alternative-subnets** (_IP/Mask_; Default: )                                     | 默认情况下，只接受来自直接连接子网的数据包。这个参数可以用来指定其他有效的数据包源子网的列表，包括数据或IGMP数据包。只对上游接口有影响。当组播数据的源头经常在不同的IP网络中时，应该使用。 |
| **interface** (_name_; Default: **all**)                                           | 接口名称。                                                                                                                                                                                 |
| **threshold** (_integer: 0...4294967295_; Default: **1**)                          | 最小TTL。收到的TTL值较低的数据包会被忽略。                                                                                                                                                 |
| **upstream** (_yes                                        \| no_; Default: **no**) | 如果该接口在组播根的方向，则称为 "上游"。一个IGMP转发路由器必须正好配置一个上游接口。上游接口是用来发送IGMP成员请求的。                                                                    |

可以用print status命令获得每个接口的详细状态信息。

```shell
[admin@MikroTik] /routing igmp-proxy interface print status
Flags: X - disabled, I - inactive, D - dynamic; U - upstream
 0  U interface=ether2 threshold=1 alternative-subnets="" upstream=yes source-ip-address=192.168.10.10 rx-bytes=3018487500 rx-packets=2012325 tx-bytes=0 tx-packets=0
 
 1    interface=ether3 threshold=1 alternative-subnets="" upstream=no querier=yes source-ip-address=192.168.20.10 rx-bytes=0 rx-packets=0 tx-bytes=2973486000 tx-packets=1982324
 
 2    interface=ether4 threshold=1 alternative-subnets="" upstream=no querier=yes source-ip-address=192.168.30.10 rx-bytes=0 rx-packets=0 tx-bytes=152019000 tx-packets=101346
```

| 属性                                            | 说明                             |
| ----------------------------------------------- | -------------------------------- |
| **querier** (_read-only; yes \| no_)            | 该接口是否作为IGMP查询器。       |
| **source-ip-address** (_read-only; IP address_) | 该接口检测到的源IP。             |
| **rx-bytes** (_read-only; integer_)             | 该接口收到的组播流量总量。       |
| **rx-packet** (_read-only; integer_)            | 该接口上收到的组播数据包的总量。 |
| **tx-bytes** (_read-only; integer_)             | 该接口上传输的组播流量的总量。   |
| **tx-packet** (_read-only; integer_)            | 该接口上传输的组播数据包的总量。 |

组播转发缓存（MFC）状态。

**Sub-menu:** `/routing igmp-proxy mfc`

| 属性                                                 | 说明                                                                               |
| ---------------------------------------------------- | ---------------------------------------------------------------------------------- |
| **active-downstream-interfaces** (_read-only: name_) | 数据包流正通过这个接口流出路由器。                                                 |
| **bytes** (_read-only: integer_)                     | 收到的组播流量的总量。                                                             |
| **group** (_read-only: IP address_)                  | IGMP组地址。                                                                       |
| **packets** (_read-only: integer_)                   | 收到的组播数据包的总量。                                                           |
| **source** (_read-only: IP address_)                 | 组播数据发起人地址。                                                               |
| **upstream-interface** (_read-only: name_)           | 数据包流通过这个接口进入路由器。                                                   |
| **wrong-packets** (_read-only: integer_)             | 收到的组播数据包到达错误接口的总量，例如，组播流是在下游接口而不是上游接口收到的。 |

RouterOS支持IGMP代理的静态组播转发规则。如果添加了静态规则，该组的所有动态规则将被忽略。 这些规则只有在配置了IGMP-proxy接口的情况下才会生效（上游和下游接口应该被设置），否则这些规则将不会被激活。

| 属性                                          | 说明                           |
| --------------------------------------------- | ------------------------------ |
| **downstream-interfaces** (_name_; Default: ) | 收到的流将只发送到列出的接口。 |
| **group** (_read-only: IP address_)           | 本规则适用的组播组地址。       |
| **source** (_read-only: IP address_)          | 组播数据发起人地址。           |
| **upstream-interface** (_read-only: name_)    | 接收流数据的接口。             |

# 例子


要把来自 ether2 接口的所有组播数据转发到下游桥接接口，即用户连接的地方，请使用下面的配置。两个接口都要有IP地址。

```shell
/routing igmp-proxy interface
add interface=ether2 upstream=yes
add interface=bridge1
 
[admin@MikroTik] /routing igmp-proxy interface print
Flags: U - UPSTREAM
Columns: INTERFACE, THRESHOLD
#   INTERFACE  THRESHOLD
0 U ether2             1
1   bridge1            1
```

可能还需要在上游接口上配置“替代子网”，以防组播发送者地址位于本地路由器不能直接到达的IP子网中：

```shell
/routing igmp-proxy interface
设置 [find upstream=yes] alternative-subnets=192.168.50.0/24, 192.168.60.0/24
```

要启用 "快速离开"，使用下面的设置：

```shell
/routing igmp-proxy
set quick-leave=yes
```