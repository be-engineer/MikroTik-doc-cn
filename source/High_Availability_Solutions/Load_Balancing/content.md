# 介绍

网络负载均衡是在不使用BGP等路由协议的情况下，在两个或多个广域网链路上平衡流量的能力。

负载均衡的目的是将流量分散到多个链路上，以获得更好的链路使用率。可以在每个数据包或每个连接的基础上进行。


| Method                                                       | Per-connection | Per-packet |
| ------------------------------------------------------------ | -------------- | ---------- |
| With the Firewall features - Firewall marking                | **Yes**        | **Yes**    |
| With the Firewall features - ECMP (Equal Cost Multi-Path)    | **Yes**        | No         |
| With the Firewall features - PCC (Per Connection Classifier) | **Yes**        | No         |
| With the Firewall features -  Nth                            | **Yes**        | **Yes**    |
| Bonding                                                      | No             | **Yes**    |
| OSPF                                                         | **Yes**        | No         |
| BGP                                                          | **Yes**        | No         |

## 路由故障转移

这个例子解释了如何使用多个网关，当第一个网关发生故障时由另一个网关接管。首先是添加网关。为第二个网关配置更大的 **距离** 值，为第一个网关配置 **check-gateway** 。

```shell
/ip route add gateway=192.168.1.1 distance=1 check-gateway=ping
/ip route add gateway=192.168.2.1 distance=2
```

第一个网关开始，因为它的距离较小（默认为1）；_check-gateway_ 确保正常。当ping失败时，它禁用第一个网关，第二个网关会接管，当第一个网关恢复时，将恢复其功能。
