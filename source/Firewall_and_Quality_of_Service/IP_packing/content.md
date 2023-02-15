# 概览

IP Packing 提供网络链路上的数据包打包服务。 可以把简单的数据包聚合成更大的数据包并压缩数据包的内容。

## 要求

数据包打包是系统包的一部分，必须在接口上启用发现协议。

### 配置

`/ip packing`

要在两个地方配置，两个路由器要对称设置：

- _ip packing_ - 在接口上启用数据包聚合和压缩
- _/ip neighbor discovery_- 在接口上启用发现协议

### 打包配置

| Property                                                                                                                                                                                                                                                                               | Description                                                                                                                                                                                                                                                                            |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| aggregated-size (_20 .. 16384 default:**1500**_)                                                                                                                                                                                                                                       | 在网络上发送数据包之前试图达到的聚合数据包的大小                                                                                                                                                                                                                                       |
| disabled (_yes                                   \| no_)                                                                                                                                                                                                                               | 打包规则的状态，如果是 _yes_，将被忽略，不会成为活动配置的一部分。                                                                                                                                                                                                                     |
| interface (_interface name_)                                                                                                                                                                                                                                                           | packing will try to aggregate and/or compress packets from this interface                                                                                                                                                                                                              |
| packing (_simple                                 \| compress-all                                                                                           \| compress-headers                                                                                               \| none_) | 当数据包离开配置的接口打包规则时，执行的动作：<br>- simple - 只进行数据包聚合<br>- compress-all - 进行聚合并压缩数据包头和有效载荷<br>- compress-headers - 进行聚合，并尝试压缩数据包的标题和有效载荷，保持原样<br>- none - 按原样发送数据包                                           |
| unpacking (_simple\|compress-all\|compress-headers\|none_)                                                                                                                                                                                                                             | 当打包规则配置的接口上收到数据包时，执行的动作：<br>- simple - 从接口上收到的聚合数据包中解压缩收到的数据包<br>- compress-all - 解除聚合的数据包，并解压缩数据包的头和有效载荷<br>- compress-headers - 解除聚合数据包的打包，并解压数据包的标题<br>- none - 对收到的数据包不做任何处理 |

路由器被看作要启用打包的接口上的路由器的邻居。如果在邻居列表中没有显示打包的条目，打包是不工作的!

打包可能会增加配置链接的延迟。

## 示例

Router-A和Router-B用电缆连接，接口ether1在Router-A上，ether3在Router-B上。这个例子将聚合来自Router-A的数据包，但会保留来自Router-B的数据包 在Router-A上。

确保发现功能已经启用：

`/ip neighbor discovery set ether1 discover=yes`

接口添加打包规则:

`/ip packing add interface=ether1 aggregated-size=1500 packing=simple unpacking=none`

在Router-B上:

确保已经启用发现功能:

`/ip neighbor discovery set ether3 discover=yes`

Add packing rule for the interface:

`/ip packing add interface=ether3 aggregated-size=1500 packing=none unpacking=simple`
