# 流量引擎

**属性**

**Sub-menu:** `/interface traffic-eng`

  

| 属性                                                                           | 说明                                                                                                                                                                                            |
| ------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **affinity-exclude** (_integer_; Default: **not set**)                         | 如果 [resource-class](https://wiki.mikrotik.com/wiki/Manual:MPLS/Traffic-eng#Interface "Manual:MPLS/Traffic-eng") 匹配任意一个指定位，则不使用接口。                                            |
| **affinity-include-all** (_integer_;Default: **not set**)                      | 只有当 [resource-class](https://wiki.mikrotik.com/wiki/Manual:MPLS/Traffic-eng#Interface "Manual:MPLS/Traffic-eng") 匹配所有指定位时才使用接口。                                                |
| **affinity-include-any** (_integer_;Default: **not set**)                      | 如果 [resource-class](https://wiki.mikrotik.com/wiki/Manual:MPLS/Traffic-eng#Interface "Manual:MPLS/Traffic-eng") 匹配任意指定位，则使用接口。                                                  |
| **auto-bandwidth-avg-interval** (_time_;Default:**5m**)                        | 测量实际数据量的间隔，从中计算平均带宽。                                                                                                                                                        |
| **auto-bandwidth-range** (_Disabled\| Min[bps][-Max[bps]]_; Default: **0bps**) | 自动带宽调节范围。[阅读更多](https://wiki.mikrotik.com/wiki/Manual:TE_tunnel_auto_bandwidth“Manual:TE tunnel auto bandwidth”)                                                                   |
| **auto-bandwidth-reserve** (_integer[%]_;Default:**0%**)                       | 预留额外带宽的百分比。[阅读更多 ](https://wiki.mikrotik.com/wiki/Manual:TE_tunnel_auto_bandwidth "Manual:TE tunnel auto bandwidth")                                                             |
| **auto-bandwidth-update-interval** (_time_;Default:**1h**)                     | 隧道记录最高平均速率的时间间隔。                                                                                                                                                                |
| **bandwidth** (_integer[bps]_;Default:**0bps**)                                | 为TE隧道预留多少带宽。值的单位是比特每秒。[阅读更多](https://wiki.mikrotik.com/wiki/Manual:TE_tunnel_auto_bandwidth#Bandwidth_limitation "Manual:TE tunnel auto bandwidth")                     |
| **bandwidth-limit** (_disabled \| integer[%]_; Default: **disabled**)          | 定义TE隧道的实际带宽限制。限制以指定隧道“带宽”的百分比配置。[阅读更多](https://wiki.mikrotik.com/wiki/Manual:TE_tunnel_auto_bandwidth#Bandwidth_limitation“Manual:TE tunnel auto bandwidth”)    |
| **comment** (_string_;Default:)                                                | 简短描述                                                                                                                                                                                        |
| **disable-running-check** (_yes\| no_;Default:**no**)                          | 是否检测接口是否正在运行。如果设置为**no**接口将总是有'running'标志。                                                                                                                           |
| **disabled** (_yes \| no_;Default:**yes**)                                     | 定义项是被忽略还是被使用。                                                                                                                                                                      |
| **from-address** (_auto\| IP_; Default: **auto**)                              | 隧道入口地址。如果设置为**auto**，则选择最少的IP地址。                                                                                                                                          |
| **holding-priority** (_integer [0..7]_;Default: **not set**)                   | 用于决定该会话是否可以被另一个会话抢占。0设置最高优先级。                                                                                                                                       |
| **mtu** (_integer_;Default:**1500**)                                           | Layer3最大传输单元                                                                                                                                                                              |
| **name** (_string_;Default:)                                                   | 接口名称                                                                                                                                                                                        |
| **primary-path** (_string_; Default: )                                         | Primary label switching paths defined in `[/mpls traffic-eng tunnel-path](https://wiki.mikrotik.com/wiki/Manual:MPLS/Traffic-eng#Tunnel_Path "Manual:MPLS/Traffic-eng")` menu.                  |
| **primary-retry-interval** (_time_; Default: **1m**)                           | 隧道尝试使用主路径的时间间隔。                                                                                                                                                                  |
| **record-route** (_yes\| no_;Default: **not set**)                             | 启用后，发送节点将接收LSP隧道实际经过的路由信息。记录路由类似于路径向量，因此可以用于环路检测。                                                                                                 |
| **reoptimize-interval** (_time_;Default: **not set**)                          | 隧道重新优化当前路径的间隔时间。如果当前路径不是最佳路径，那么优化后将使用最佳路径。[阅读更多](https://wiki.mikrotik.com/wiki/Manual:Interface/Traffic_Engineering#Reoptimization)              |
| **secondary-paths** (_string[,string]_; Default: )                             | 主路径故障时TE隧道使用的标签交换路径列表。路径在 [/mpls traffic-eng tunnel-path](https://wiki.mikrotik.com/wiki/Manual:MPLS/Traffic-eng#Tunnel_Path "Manual: mpls / traffic-eng ") 菜单中定义。 |
| **setup-priority** (_integer[0..7]_;Default: **not set**)                      | 该参数用于决定该会话是否可以抢占另一个会话。0设置最高优先级。                                                                                                                                   |
| **to-address** (_IP_;Default:**0.0.0.0**)                                      | TE隧道对端。                                                                                                                                                                                    |

## 监控

如果需要验证TE隧道的状态，可以使用 **monitor** 命令。

```shell
/interface traffic-eng monitor 0
tunnel-id: 12
primary-path-state: on-hold
secondary-path-state: established
secondary-path: static
active-path: static
active-lspid: 3
active-label: 66
explicit-route: "S:192.168.55.10/32,L:192.168.55.13/32,L:192.168.55.17/32"
recorded-route: "192.168.55.13[66],192.168.55.17[59],192.168.55.18[3]"
reserved-bandwidth: 5.0Mbps
```

  

## 重新优化

输入命令/interface traffic-eng reoptimize [id] (其中 [id] 为项目号或接口名)，可以手动重新优化路径。网络管理员可以根据带宽、流量、管理策略或其他因素的变化，对已经建立的lsp进行重新优化。

假设在最佳路径上的链路发生故障后，TE隧道选择了另一条路径。如果启用 [record-route](https://wiki.mikrotik.com/wiki/Manual:MPLS/Traffic-eng#Tunnel_Path "Manual:MPLS/Traffic-eng") 参数，可以通过查看 **explicit-route** 或 **recorded-route** 值来验证优化。

```shell
/interface traffic-eng monitor 0
tunnel-id: 12
primary-path-state: established
primary-path: dyn
secondary-path-state: not-necessary
active-path: dyn active-lspid: 1
active-label: 67
explicit-route: "S:192.168.55.10/32,S:192.168.55.13/32,S:192.168.55.14/32,
S:192.168.55.17/32,S:192.168.55.18/32"
recorded-route: "192.168.55.13[67],192.168.55.17[60],192.168.55.18[3]"
reserved-bandwidth: 5.0Mbps
```


每当链路返回时，TE隧道将使用相同的路径，即使它不是最佳路径(除非配置了 [reoptimize-interval](https://wiki.mikrotik.com/wiki/Manual:MPLS/Traffic-eng#Tunnel_Path "Manual:MPLS/Traffic-eng"))。为了解决这个问题，可以手动重新优化隧道路径。

`/interface traffic-eng reoptimize 0`

  
```shell
/interface traffic-eng monitor 0
tunnel-id: 12
primary-path-state: established
primary-path: dyn
secondary-path-state: not-necessary
active-path: dyn
active-lspid: 2 active-label: 81
explicit-route: "S:192.168.55.5/32,S:192.168.55.2/32,S:192.168.55.1/32"
recorded-route: "192.168.55.2[81],192.168.55.1[3]"
reserved-bandwidth: 5.0Mbps
```
 

请注意，明确的路线和记录的路由如何变为较短的路径。