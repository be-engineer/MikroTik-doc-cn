# 介绍

MikroTik Traffic-Flow是一个通过路由器数据包的统计系统。除了网络监控和计算，系统管理员还可以识别网络中可能出现的各种问题。在Traffic-Flow的帮助下，可以分析和优化整个网络性能。Traffic-Flow与思科NetFlow兼容，可以和各种实用程序一起使用，这是为思科的NetFlow设计的。

Traffic-Flow支持以下NetFlow格式。

- **版本1** - NetFlow数据格式的第一个版本，不要使用它，除非没有其他选择
- **版本5** - 除了版本1之外，版本5有可能包括BGP AS和流量序列号信息。目前，RouterOS不包括BGP AS号码。
- **版本9** - 一个新的格式，可以用新的字段和记录类型来扩展，感谢其模板式设计

## 常规

**Sub-menu:** `/ip traffic-flow`

本节列出了数据流的配置属性。

| 属性                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | 说明                                                                                                                                                                         |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **interfaces** (_string                              \| all_; Default: **all**)                                                                                                                                                                                                                                                                                                                                                                                                                                           | 这些接口的名称将用来收集流量统计信息。要指定一个以上的接口，请用逗号分开。                                                                                                   |
| **cache-entries** (_128k                             \| 16k                                                                                                                                                                                                                                                                     \| 1k                                                                                                                                            \| 256k \| 2k \| ..._ ; Default: **4k**) | 路由器内存中可同时存在的流量数。                                                                                                                                             |
| **active-flow-timeout** (_time_; Default: **30m**)                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | 流量的最大寿命时间。                                                                                                                                                         |
| **inactive-flow-timeout** (_time_; Default: **15s**)                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | 如果流量是空闲的，要保持多长的活动时间。如果连接在这个超时内没有任何数据包，那么traffic-flow将发送一个新的流量数据包出去。如果这个超时太小，会产生大量的流量，并溢出缓冲区。 |
| **packet-sampling** (_no                             \| yes_; Default: **no**)                                                                                                                                                                                                                                                                                                                                                                                                                                            | 启用或禁用数据包取样功能。                                                                                                                                                   |
| **sampling-interval** (_integer_; Default: **0**)                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | 连续取样的数据包数量。                                                                                                                                                       |
| **sampling-space** (_integer_; Default: **0**)                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | 连续忽略的数据包的数量。                                                                                                                                                     |

从RouterOS **v7.1rc5** 开始提供数据包取样!

在下面的例子中：

`/ip/traffic-flow/set packet-sampling=yes sampling-interval=2222 sampling-space=1111`

2222个连续的数据包被取样，1111个数据包被忽略。取样周期重复进行。

## 目标

**Sub-menu:** `/ip traffic-flow target`

通过流量目标，可以指定从路由器收集流量信息的主机。

| 属性                                                 | 说明                                                       |
| ---------------------------------------------------- | ---------------------------------------------------------- |
| **address** (_IP:port_; Default: )                   | 从路由器接收流量统计包的主机IP地址和端口（UDP）。          |
| **v9-template-refresh** (_integer_; Default: **20**) | 向接收主机发送模板后的数据包数量（仅适用于NetFlow版本9）。 |
| **v9-template-timeout** (_time_; Default: )          | 如果模板没有发送，则在多长时间后发送。                     |
| **version** (_1\| 5\| 9_; Default: )                 | 使用哪种NetFlow的版本格式。                                |

### 注释

通过查看 [包流量图](https://help.mikrotik.com/docs/display/ROS/Packet+Flow+in+RouterOS)，可以看到流量是在输入、转发和输出链的末端。即只计算到达这些链之一的流量。

例如，在交换机上设置了一个镜像端口，将镜像端口连接到路由器上，并将流量设置为计算镜像数据包。但是这样的设置不起作用，因为镜像的数据包在到达输入链之前就被丢弃了。

如果流量经过其他接口和监测接口，其他接口将出现在报告中。

## 示例

这个例子显示如何在路由器上配置Traffic-Flow

在路由器上启用Traffic-Flow。

```shell
[admin@MikroTik] ip traffic-flow> set enabled=yes
[admin@MikroTik] ip traffic-flow> print
                enabled: yes
             interfaces: all
          cache-entries: 1k
    active-flow-timeout: 30m
  inactive-flow-timeout: 15s
[admin@MikroTik] ip traffic-flow>
```

指定主机的IP地址和端口，它将接收Traffic-Flow数据包。

```shell
[admin@MikroTik] ip traffic-flow target> add dst-address=192.168.0.2 port=2055 version=9
[admin@MikroTik] ip traffic-flow target> print
Flags: X - disabled
 #   SRC-ADDRESS       DST-ADDRESS        PORT     VERSION
 0   0.0.0.0           192.168.0.2        2055     9 
[admin@MikroTik] ip traffic-flow target>
```

现在，路由器开始发送带有Traffic-Flow信息的数据包。

注意:要在MikroTik上使用ntp-ng，需要用Nprobe，它是付费软件。

### 参考文档

- [NetFlow Fundamentals](https://etutorials.org/Networking/network+management/Part+II+Implementations+on+the+Cisco+Devices/Chapter+7.+NetFlow/Fundamentals+of+NetFlow/)
- [Traffic flow with Ntop on MikroTik](https://github.com/ntop/ntopng/issues/1575)