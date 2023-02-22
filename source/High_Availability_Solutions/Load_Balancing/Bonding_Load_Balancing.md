# 绑定负载均衡概述

Bonding is a technology that allows the aggregation of multiple ethernet-like interfaces into a single virtual link, thus getting higher data rates and providing failover.

![](https://help.mikrotik.com/docs/download/attachments/63406084/Lacp.png?version=1&modificationDate=1618901948934&api=v2)

## 配置实例

假设在每个路由器上有两个以太网接口（SW1和SW2），希望在这两个路由器之间获得最大的速率。为了实现这一点，请按以下步骤：

1. 确保接口上没有IP地址，这些接口将被设为绑定接口。
2. 在SW1上添加绑定接口和IP地址:
    
    `/interface bonding add mode =802.3ad slaves =ether1,ether2 name =bond1`
    
    `/ip address add address =172.16.0.1/24 interface =bond1`
    
3. 在SW2做同样的设置:
    
    `/interface bonding add mode =802.3ad slaves =ether1,ether2 name =bond1`
    
    `/ip address add address =172.16.0.2/24 interface =bond1`
    
4. 从Router1测试连接:

```shell
    [admin@Router1] > ping 172.16.0.2
      SEQ HOST                                 SIZE TTL TIME  STATUS                  
        0 172.16.0.2                             56  64 0ms 
        1 172.16.0.2                             56  64 0ms 
        2 172.16.0.2                             56  64 0ms 
        sent =3 received =3 packet-loss =0% min-rtt =0ms avg-rtt =0ms max-rtt =0ms
```

The bonding interface has to be configured on both hosts and needs a couple of seconds to get connectivity with its peers.

## 平衡模式

## 802.3ad

802.3ad模式是一个IEEE标准，也叫LACP（链路聚合控制协议）。包括聚合体的自动配置，要对交换机进行最小配置。标准规定，帧将按顺序传送，连接不应出现数据包的错误排序。标准还规定，聚合中的所有设备必须以相同的速度和双工模式运行。

LACP根据散列的协议头信息在活动端口之间平衡出站流量，接受来自任何活动端口的入站流量。哈希值包括以太网源和目标地址，如果有的话，还包括VLAN标签，以及IPv4/IPv6源和目标地址。如何计算取决于传输哈希策略参数。不建议使用ARP链路监控，因为LACP对等设备上的发送散列策略，ARP回复可能只到达一个从属端口。可能导致不平衡的传输流量，所以推荐使用MII链路监控。

## balance-xor

这种模式根据散列的协议头信息在活动端口之间平衡出站流量，接受来自任何活动端口的入站流量。该模式和 [LACP](https://wiki.mikrotik.com/wiki/Manual:Interface/Bonding#802.3ad) 非常相似，只是没有标准化，与 **layer-3-and-4** 的哈希策略一起工作。该模式可以和静态链路聚合组（LAG）接口一起工作。

## 其他信息

更多信息 [Bonding in RouterOS!](https://help.mikrotik.com/docs/display/ROS/Bonding)
