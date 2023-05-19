## 组播协议介绍

组管理协议允许任何接口成为组播流的接收器。允许在不使用专门的IGMP或MLD客户端的情况下测试组播路由和交换设置。该选项从RouterOS v7.4开始提供，支持IGMP v1, v2, v3和MLD v1, v2协议。 

接口默认使用的是IGMP v3和MLD v2。如果收到IGMP v1、v2或MLD v1查询，接口将退回到适当的版本。一旦在接口上创建了组管理协议，将发送一个不请自来的成员报告（加入）数据包，并响应查询信息。如果配置被删除或禁用，接口将发送一个离开消息。

# 配置选项


本节介绍组管理协议的配置选项。

**Sub-menu:** `/routing gmp`

| 属性                                                    | 说明                                                                                                                     |
| ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| **groups** (_IPv4                  \| IPv6_; Default: ) | 接口要使用的组播组地址，支持多个组地址。                                                                                 |
| **interfaces** (_name_; Default: )                      | 接口的名称，支持多个接口和接口列表。                                                                                     |
| **exclude** (Default: )                                 | 设置 "exclude"时，接口期望拒绝来自配置的 "sources "的组播数据。不使用此选项时，接口将为配置的 "source"发出特定源的连接。 |
| **sources** (_IPv4 \| IPv6_; Default: )                 | 接口使用的源地址列表，支持多个源地址。当IGMPv3或MLDv2协议激活时，此设置会产生影响。                                      |

# 例子


这个例子显示了如何在接口上配置一个简单的多播监听器。

首先，在接口上添加一个IP地址：

```shell
/ip address
add address=192.168.10.10/24 interface=ether1 network=192.168.10.0
```

然后在同一接口上配置组管理协议：

```shell
/routing gmp
add groups=229.1.1.1 interfaces=ether1
```

现在就可以检查你的组播网络了，看看路由器或交换机是否创建了适当的组播转发条目，以及接口上是否收到了组播数据（查看接口统计，或使用 [Packet Sniffer](https://help.mikrotik.com/docs/display/ROS/Packet+Sniffer) 和 [Torch](https://help.mikrotik.com/docs/display/ROS/Torch)）。