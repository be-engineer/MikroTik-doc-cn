# 介绍

本文档描述了把 RouterOS 升级到 v7 主要版本的推荐步骤以及注意事项。

从 v6 升级到 v7 的方式和在 v6 版本内升级的方式完全相同。 请按照[升级手册](https://help.mikrotik.com/docs/display/ROS/Upgrading+and+installation) 了解更多详细步骤。 如果你当前运行的是 RouterOS 版本 6 或更早版本，我们首先建议升级到 v6 中的最新稳定版或长期版（目前为 6.48.6 长期版或 6.49.7 稳定版）。

> 在上述 v6 版本上运行良好的大多数 RouterOS 设置中，不需要额外的步骤。 升级到 v7 将自动转换配置，你的设备将立即运行。

## 功能列表兼容性

如前所述，几乎所有 RouterOS 系统都可以使用“检查更新”功能并单击几下即可升级到 v7，但有一些功能可能需要额外的步骤：

| 属性             | 状态                                                                                                             |
| ---------------- | ---------------------------------------------------------------------------------------------------------------- |
| CAPsMAN          | OK                                                                                                               |
| Interfaces       | OK                                                                                                               |
| Wireless         |
| Bridge/Switching | OK                                                                                                               |
| Tunnels/PPP      | OK                                                                                                               |
| IPv6             | OK                                                                                                               |
| BGP              | OK, 需要注意  [\*](https://help.mikrotik.com/docs/display/ROS/Upgrading+to+v7#Upgradingtov7-bgp)                 |
| OSPF             | OK, 需要注意 [\*\*](https://help.mikrotik.com/docs/display/ROS/Upgrading+to+v7#Upgradingtov7-ospf)               |
| MPLS             | OK, 需要注意 [\*\*\*](https://help.mikrotik.com/docs/display/ROS/Upgrading+to+v7#Upgradingtov7-mpls)             |
| Routing filters  | OK, 需要注意 [\*\*\*\*](https://help.mikrotik.com/docs/display/ROS/Upgrading+to+v7#Upgradingtov7-routingfilters) |
| Tools            | OK                                                                                                               |
| Queues           | OK                                                                                                               |
| Firewall         | OK                                                                                                               |
| HotSpot          | OK                                                                                                               |
| Static Routing   | OK                                                                                                               |
| User Manager     | 见[注释](https://help.mikrotik.com/docs/display/ROS/Upgrading+to+v7#Upgradingtov7-usermanager)                   |

### 注意

> 路由协议配置升级只触发一次。 这意味着如果路由器降级到 ROSv6，配置被修改并且路由器升级回 ROSv7，那么生成的配置是降级之前存在的配置。 要重新触发 v6 配置转换，请使用选项“force-v6-to-v7-configuration-upgrade=yes”加载 ROSv6 备份。

### BGP

所有已知配置都将成功从 6.x 升级到 7.x。 但请记住，配置已完全重新设计。 v7 BGP 实现提供了 **`connection`**、**`template`** 和 **`session`** 菜单。

**`Template`** 包含所有 BGP 协议相关的配置选项。 可以用作动态对等点的模板，并将类似的配置应用于一组对等点。 大多数参数与之前的实现相似，除了一些参数被分组在输出和输入部分，使配置更具可读性和更容易理解该选项是应用于输入还是输出。

BGP **`connection`** 最小参数集是 `remote.address`、`template、 connect`、`listen` 和 `local.role`
连接和侦听参数指定对等点是尝试连接和侦听远程地址，还是只是连接或只是侦听。 在对等方使用多跳连接的设置中，也必须配置 local.address 。 Peer role 现在是强制参数，对于基本设置，可以只使用 ibgp、ebgp。

现在你可以从“/routing bgp session”菜单监控所有连接和断开连接的对等点的状态。
可以从“/routing stats”菜单中监视有关所有路由进程的其他重要调试信息。

网络被添加到防火墙地址列表中，并在 BGP **`connection`** 配置中被引用。

### OSPF

所有已知配置都将成功从 6.x 升级到 7.x。
OSPFv2 和 OSPFv3 现在合并到一个菜单“/routing ospf”中。 目前没有默认实例和区域。 要启动 OSPF，需要创建一个实例，然后将 are 添加到该实例。

RouterOSv7 使用模板将接口与模板进行匹配，并应用来自匹配模板的配置。 OSPF 菜单“interface”和“neighbor”包含用于状态监控的只读条目。

### MPLS

谨慎升级 MPLS 设置，并确保在升级前备份配置。

### Routing filters

所有支持的选项都可以毫无问题地升级，如果是不支持的选项 - 将创建一个空条目。 路由过滤器配置更改为类似脚本的配置。

该规则现在可以使用“if .. then”语法来设置参数或根据“if”语句中的条件应用操作。

没有动作的多个规则堆叠在一个规则中并像防火墙一样按顺序执行，原因是“set”参数顺序很重要，每行写一个“set”，可以从上到下更容易理解 应用了哪些操作。

更多 RouterOSv7 路由过滤器示例在 [此处](https://help.mikrotik.com/docs/display/ROS/ROSv7+Basic+Routing+Examples#ROSv7BasicRoutingExamples-RoutingFilters)。

### 用户管理

RouterOSv7 提供了新的和重新设计的用户管理器，配置集成到 RouterOS WinBox 和控制台中，更多信息可在 [此处](https://help.mikrotik.com/docs/display/ROS/User+Manager) 获得。 从旧的用户管理器直接迁移是不可能的，可以从 /user-manager/database/migrate-legacy-db 迁移旧的数据库但是，从头开始配置可能是个好主意。

## 新特性

新内核在 RouterOSv7 中实现，由于路由缓存导致性能变化，并且某些任务可能需要更高的 CPU 和 RAM 用于不同的进程。

- 全新的 NTP 客户端和服务器实现
- 合并了单独的包，只剩下捆绑包和一些额外的包
- 新的命令行界面 (CLI) 样式（仍然支持 RouterOS v6 命令）
- 支持 Let's Encrypt 证书生成
- 支持 REST API
- 支持 x86 上的 UEFI 启动模式
- CHR FastPath 支持“vmxnet3”和“virtio-net”驱动程序
- 支持“Cake”和“FQ\_Codel”类型的队列
- 支持 IPv6 NAT
- 支持所有 CRS3xx 设备上的第 3 层硬件加速
- 支持具有基本功能的 MBIM 驱动程序支持所有具有 MBIM 模式的调制解调器
- 支持 CRS3xx 设备上的 MLAG
- 支持节点间VRRP分组和连接跟踪数据同步
- 支持虚拟可扩展局域网 (VXLAN)
- 支持 L2TPv3
- 支持 OpenVPN UDP 传输协议
- 支持 WireGuard
- 支持 RTL8367（RB4011、RB100AHx4）和 MT7621（hEX、hEX S、RBM33G）交换机上的硬件卸载 VLAN 过滤
- 支持 ARM 和 ARM64 设备上的 ZeroTier
- 全新的替代无线包“wifiwave2”，支持 802.11ac Wave2、WPA3 和 802.11w 管理框架保护（需要 ARM CPU 和 256MB RAM）
- 支持 RTL8367（RB4011、RB100AHx4）和 MT7621（hEX、hEX S、RBM33G）交换机上的硬件卸载 VLAN 过滤
- 支持 x86 设备的 CPU 频率调整
