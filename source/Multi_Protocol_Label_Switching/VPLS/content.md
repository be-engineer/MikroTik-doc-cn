# 概述

VPLS (virtual Private Lan Service)接口和 [EoIP](https://help.mikrotik.com/docs/display/ROS/EoIP) 接口一样，可以看作是一个隧道接口。在客户站点之间实现透明的以太网段转发。

VPLS隧道的协商可以通过LDP协议或MP-BGP协议来完成——隧道的两端交换标签，它们将在隧道中使用。

隧道中的数据转发是通过在数据包上施加两个标签来实现的:隧道标签和传输标签——传输标签是一种确保流量能够传递到隧道另一端的标签。


microtik RouterOS实现了以下VPLS特性:

- VPLS LDP信令(RFC 4762)
- Cisco风格的静态VPLS伪线(RFC 4447 FEC类型0x80)
- VPLS伪线分片和重组(RFC 4623)
- 基于VPLS MP-BGP的自动发现和信令(RFC 4761)
- Cisco VPLS基于bgp的自动发现(draft-ietf-l2vpn-signaling-08)
- 支持基于BGP的VPLS的多个导入/导出路由目标扩展团体(RFC 4761和draft-ietf-l2vpn-signaling-08)

  

# VPLS必备条件

为了使VPLS能够传输MPLS数据包，骨干网上必须已经运行其中一个标签分发协议，它可以是LDP、RSVP-TE或静态绑定。

在继续之前，请先熟悉 [LDP的先决条件](https://help.mikrotik.com/docs/display/ROS/LDP#LDP-PrerequisitesforMPLS) 和RSVP-TE的先决条件。

在这种情况下，如果 BGP 应该用作 VPLS 发现和信令协议，则骨干网应该最好运行带有路由反射器的 iBGP。

  

# 示例设置

考虑已经从 [LDP配置示例](https://help.mikrotik.com/docs/display/ROS/LDP#LDP-ExampleSetup) 中获得了一个工作的LDP设置。

R1、R3和R4连接客户A站点，R1和R3连接客户B站点。客户需要站点之间透明的L2连接。

  
  

# 参考

## 常规的

**Sub-menu:** `/interface vpls`

  
所有VPLS接口列表。该菜单还显示了动态创建的基于bgp的VPLS接口。

**属性**

| 属性                                                                            | 说明                                                                                                                                                                                        |
| ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **arp** (_disabled \| enabled\| proxy-arp\| reply-only_; Default: **enabled**)  | 地址解析协议                                                                                                                                                                                |
| **arp-timeout** (_time interval                                                 | auto_;Default:auto)                                                                                                                                                                         |  |
| **bridge** (_name_;Default : )                                                  |                                                                                                                                                                                             |  |
| **bridge-cost** (_integer [0..4294967295]_;Default:**50**)                      | 网桥端口的开销。                                                                                                                                                                            |
| **bridge-horizon** (_none \| integer_; Default:**none**)                        | 如果设置为 **none** 网桥水平线将不会使用。                                                                                                                                                  |
| **cisco-static-id** (_integer [0 . . 4294967295] _;Default:**0**)               | cisco式VPLS隧道ID。                                                                                                                                                                         |
| **comment** (_string_; Default: )                                               | 注释                                                                                                                                                                                        |
| **disable-running-check** (_yes \| no_;Default:**no**)                          | 是否检测接口是否正在运行。如果设置为 **no** 接口将始终具有'running'标志。                                                                                                                   |
| **disabled** (_yes \| no_;Default:**yes**)                                      | 定义项是被忽略还是被使用。缺省情况下，VPLS接口处于禁用状态。                                                                                                                                |
| **mac-address** (_MAC_; Default: )                                              |                                                                                                                                                                                             |  |
| **mtu** (_integer [32..65536]_; Default: **1500**)                              |                                                                                                                                                                                             |  |
| **name** (_string_; Default: )                                                  | 接口名称                                                                                                                                                                                    |
| **pw-l2mtu** (_integer [0..65536]_;Default:**1500**)                            | 通告给远端对等体的L2MTU值。                                                                                                                                                                 |
| **pw-type** (_raw-ethernet \| tagged-ethernet \| vpls_;默认值:**raw-ethernet**) | 伪线类型                                                                                                                                                                                    |
| **peer** (_IP_;Default:)                                                        | 远端对等体IP地址。                                                                                                                                                                          |
| **pw-control-word** (_disabled\| enabled\| default_;Default:**Default**)        | 启用/禁用控制字使用。常规VPLS隧道和思科VPLS隧道的缺省值不同。思科风格默认禁用控制词使用。在 [VPLS控制词](https://help.mikrotik.com/docs/display/ROS/VPLS+Control+Word) 文章中阅读更多内容。 |
| **vpls-id** (_AsNum \| AsIp_;Default:)                                          | 唯一标识VPLS隧道的编号。编码方式为2byte+4byte或4byte+2byte。                                                                                                                                |

  
**只读属性**

| 属性                                  | 说明                                                                                                      |
| ------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| **cisco-bgp-signaling** (_yes \| no_) |                                                                                                           |  |
| **vpls** (_string_)                   | 用于创建动态vpls接口的 [bgp-vpls实例](https://wiki.mikrotik.com/wiki/Manual:Interface/VPLS#BGP_VPLS) 名称 |
| **bgp-signaled**                      |                                                                                                           |  |
| **bgp-vpls**                          |                                                                                                           |  |
| **bgp-vpls-prfx**                     |                                                                                                           |  |
| **dynamic** (_yes \| no_)             |                                                                                                           |  |
| **l2mtu** (integer)                   |                                                                                                           |  |
| **running** (_yes            \| no_)  |                                                                                                           |  |

### 监控

命令/interface vpls monitor [id]将显示当前vpls接口的状态

例如:

```shell
[admin@10.0.11.23] /interface vpls> monitor vpls2
remote-label: 800000
local-label: 43
remote-status:
transport: 10.255.11.201/32
transport-nexthop: 10.0.11.201
imposed-labels: 800000
```

可用的只读属性:

| 属性                                | 说明                                                   |
| ----------------------------------- | ------------------------------------------------------ |
| **imposed-label** (_integer_)       | VPLS强制标签                                           |
| **Local -label** (_integer_)        | 本地VPLS标签                                           |
| **remote-group** ()                 |                                                        |
| **Remote -label** (_integer_)       | 远端VPLS标签                                           |
| **remote-status** (_integer_)       |                                                        |
| **transport-nexthop** (_IP prefix_) | 显示使用的传输地址(通常是Loopback地址)。               |
| **transport** (_string_)            | 传输接口的名称。如果VPLS运行在流量工程隧道上，请设置。 |

# VPLS控制字概述

VPLS允许远程站点通过分组交换网络(PSN)上的伪线(PW)隧道连接站点来共享以太网广播域。由于VPLS封装增加了额外的开销，所以LSP中的每个接口都应该能够传输足够大的报文。

每个以太网芯片组都对其可以传输的最大数据包大小有硬件限制。即使现在也有只支持一个Vlan标签的以太网，这意味着没有以太网报头和校验和(L2MTU)的最大数据包大小是1504字节。显然，转发VPLS封装的以太网帧而不分片是不够的(至少需要1524 L2MTU支持)。routerboard支持的最大l2mtu请参见 [RouterOS中的MTU](https://help.mikrotik.com/docs/display/ROS/MTU+in+RouterOS)。

由于并不是所有的routerboard都支持足够的L2MTU来传输VPLS封装的无分片报文，所以RouterOS根据RFC 4623使用4字节控制字(CW)增加了伪线分片和重组(PWE3)支持。

# 控制词使用

在RouterOS中，控制字用于VPLS隧道内的报文分片和重组，通过可选的控制字(CW)实现。CW被添加到PW标签(解复用)和数据包负载之间，并增加了额外的4字节开销。

未实现重新排序的OOO数据包，将丢弃订单片段

CW用法由VPLS配置中的“用法控制”参数控制。

![](https://help.mikrotik.com/docs/download/attachments/128974851/VPLS_CW.png?version=1&modificationDate=1653634938423&api=v2)

正如所看到的，控制字分为5个字段:

- 0000 - 4位标识数据包是PW(不是IP)
- 标志- 4位
- fragg - 2bits值，表示有效载荷分片。
- Len - 6bits
- Seq - 16位序号，用于检测丢包或错序。

根据RFC生成和处理序列号是可选的。