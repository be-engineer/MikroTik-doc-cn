# 概述

___

Cloud Router Switch 系列是高度集成的交换机，具有高性能 MIPS CPU 和功能丰富的数据包处理器。 CRS 交换机可以设计成各种以太网应用，包括非管理型交换机、第 2 层管理型交换机、运营商交换机和无线/有线统一数据包处理设备。 参见[Cloud Router Switch](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=103841836) 配置示例。

本文适用于 CRS1xx 和 CRS2xx 系列交换机，不适用于 CRS3xx 系列交换机。 对于 CRS3xx 系列设备，请阅读 [CRS3xx、CRS5xx 系列交换机和 CCR2116、CCR2216 路由器](https://help.mikrotik.com/docs/display/ROS/CRS3xx%2C+CRS5xx%2C+CCR2116%2C+CCR2216+switch+chip+features)手册。
  
| Features                       | Description                                                                                                                                                                                                                                                                                                                                                      |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Forwarding**                 | - 用于交换或路由的可配置端口<br>- 完全无阻塞的线速交换<br>- 单播 FDB 中最多 16k MAC 项，用于第 2 层单播转发<br>- 多播 FDB 中最多 1k MAC 项用于组播转发<br>- 保留 FDB 中最多 256 个 MAC 项用于控制和管理目的<br>- 所有转发数据库都支持 IVL 和 SVL<br>- 可配置的基于端口的 MAC 学习限制<br>- 巨型帧支持（CRS1xx：4064 字节；CRS2xx：9204 字节）<br>- 支持IGMP 侦听 |
| **Mirroring**                  | 各种类型的镜像：<br>- 基于端口的镜像<br>- 基于 VLAN 的镜像<br>- 基于 MAC 的镜像<br>2个独立的镜像分析器端口                                                                                                                                                                                                                                                       |
| **VLAN**                       | 完全兼容IEEE802.1Q和IEEE802.1ad VLAN<br>4k 活动 VLAN<br>灵活的VLAN分配：<br>- 基于端口的VLAN<br>- 基于协议的VLAN<br>- 基于MAC的VLAN<br>任意 VLAN之间的转换和交换<br>1:1 VLAN 交换 - VLAN 到端口映射<br>VLAN过滤                                                                                                                                                  |
| **Port Isolation and Leakage** | - 适用于私有 VLAN的实施<br>- 3 种端口配置文件类型：混杂、隔离和Community<br>- 最多 28 个Community配置<br>- 泄漏配置文件允许绕过出站 VLAN 过滤                                                                                                                                                                                                                    |
| **Trunking**                   | - 支持静态链路聚合组<br>- 多达 8 个 Port Trunk 群组<br>- 每个端口中继组最多 8 个成员端口<br>- 硬件自动故障转移和负载平衡                                                                                                                                                                                                                                         |
| **Quality of Service (QoS)**   | 灵活的 QoS 分类和分配：<br>- 基于端口<br>- 基于MAC<br>- 基于VLAN<br>- 基于协议<br>- 基于 PCP/DEI<br>- 基于 DSCP<br>- 基于ACL<br>服务提供商和客户端网络之间 QoS 域转换的 QoS 重新标记和重新映射<br>根据配置的优先级覆盖每个 QoS 分配                                                                                                                              |
| **Shaping and Scheduling**     | - 每个物理端口上有 8 个队列<br>- 按端口、按队列、按队列组整形                                                                                                                                                                                                                                                                                                    |
| **Access Control List**        | - 入站和出站 ACL 表<br>- 最多 128 个 ACL 规则（受 RouterOS 限制）<br>- 基于端口、L2、L3、L4协议头字段的分类<br>- ACL动作包括过滤、转发、修改协议头字段                                                                                                                                                                                                           |

# Cloud Router 交换机型号

___

下表说明了 Cloud Router 交换机型号之间的主要区别。

<table class="wrapped confluenceTable" style="text-align: center;" resolved=""><tbody><tr><td class="highlight-grey confluenceTd" data-highlight-colour="grey" title="Background color : "><strong title=""><u>型号</u></strong></td><td class="highlight-grey confluenceTd" data-highlight-colour="grey" title="Background color : "><strong title="">交换芯片</strong></td><td class="highlight-grey confluenceTd" data-highlight-colour="grey" title="Background color : "><strong title="">CPU</strong></td><td class="highlight-grey confluenceTd" data-highlight-colour="grey" title="Background color : "><strong title="">Wireless</strong></td><td class="highlight-grey confluenceTd" data-highlight-colour="grey" title="Background color : "><strong title="">SFP+ port</strong></td><td class="highlight-grey confluenceTd" data-highlight-colour="grey" title="Background color : "><strong title="">Access Control List</strong></td><td class="highlight-grey confluenceTd" data-highlight-colour="grey" title="Background color : "><strong title="">Jumbo Frame (Bytes)</strong></td></tr><tr><td class="highlight-grey confluenceTd" data-highlight-colour="grey" title="Background color : "><strong>CRS105-5S-FB</strong></td><td class="confluenceTd">QCA-8511</td><td class="confluenceTd">400MHz</td><td class="confluenceTd">-</td><td class="confluenceTd">-</td><td class="confluenceTd">+</td><td class="confluenceTd">9204</td></tr><tr><td class="highlight-grey confluenceTd" data-highlight-colour="grey" title="Background color : "><strong>CRS106-1C-5S</strong></td><td class="confluenceTd">QCA-8511</td><td class="confluenceTd">400MHz</td><td class="confluenceTd">-</td><td class="confluenceTd">-</td><td class="confluenceTd">+</td><td class="confluenceTd">9204</td></tr><tr><td class="highlight-grey confluenceTd" data-highlight-colour="grey" title="Background color : "><strong>CRS112-8G-4S</strong></td><td class="confluenceTd">QCA-8511</td><td class="confluenceTd">400MHz</td><td class="confluenceTd">-</td><td class="confluenceTd">-</td><td class="confluenceTd">+</td><td class="confluenceTd">9204</td></tr><tr><td class="highlight-grey confluenceTd" data-highlight-colour="grey" title="Background color : "><strong>CRS210-8G-2S+</strong></td><td class="confluenceTd">QCA-8519</td><td class="confluenceTd">400MHz</td><td class="confluenceTd">-</td><td class="confluenceTd">+</td><td class="confluenceTd">+</td><td class="confluenceTd">9204</td></tr><tr><td class="highlight-grey confluenceTd" data-highlight-colour="grey" title="Background color : "><strong>CRS212-1G-10S-1S+</strong></td><td class="confluenceTd">QCA-8519</td><td class="confluenceTd">400MHz</td><td class="confluenceTd">-</td><td class="confluenceTd">+</td><td class="confluenceTd">+</td><td class="confluenceTd">9204</td></tr><tr><td class="highlight-grey confluenceTd" data-highlight-colour="grey" title="Background color : "><strong>CRS226-24G-2S+</strong></td><td class="confluenceTd">QCA-8519</td><td class="confluenceTd">400MHz</td><td class="confluenceTd">-</td><td class="confluenceTd">+</td><td class="confluenceTd">+</td><td class="confluenceTd">9204</td></tr><tr><td class="highlight-grey confluenceTd" data-highlight-colour="grey" title="Background color : "><strong>CRS125-24G-1S</strong></td><td class="confluenceTd">QCA-8513L</td><td class="confluenceTd">600MHz</td><td class="confluenceTd">-</td><td class="confluenceTd">-</td><td class="confluenceTd">-</td><td class="confluenceTd">4064</td></tr><tr><td class="highlight-grey confluenceTd" data-highlight-colour="grey" title="Background color : "><strong>CRS125-24G-1S-2HnD</strong></td><td class="confluenceTd">QCA-8513L</td><td class="confluenceTd">600MHz</td><td class="confluenceTd">+</td><td class="confluenceTd">-</td><td class="confluenceTd">-</td><td class="confluenceTd">4064</td></tr><tr><td class="highlight-grey confluenceTd" data-highlight-colour="grey" title="Background color : "><strong>CRS109-8G-1S-2HnD</strong></td><td class="confluenceTd">QCA-8513L</td><td class="confluenceTd">600MHz</td><td class="confluenceTd">+</td><td class="confluenceTd">-</td><td class="confluenceTd">-</td><td class="confluenceTd">4064</td></tr></tbody></table>

# 缩略语和解释

___

CVID - 客户VLAN ID：IEEE 802.1ad帧的内部VLAN标签ID

SVID - 服务VLAN id：IEEE 802.1ad帧的外部VLAN标签id。

IVL - 独立VLAN学习 - 学习/查询是基于MAC地址和VLAN ID。

SVL - 共享VLAN学习 - 学习/查询是基于MAC地址 - 而不是VLAN ID。

TPID - 标签协议标识符

PCP - 优先级代码点：一个3位字段，指的是IEEE 802.1p优先级

DEI - 丢弃资格指标

DSCP - 差异化服务代码点

Drop precedence - CRS交换机内部QoS属性，用于数据包的排队或丢弃。

# 端口交换

___

为了在CRS1xx/2xx系列交换机上设置端口交换，请查看【网桥硬件卸载】(https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-BridgeHardwareOffloading)页面。

!!!warning 在创建硬件卸载网桥，添加交换端口组时，会在CRS交换机中创建动态保留的VLAN项（如VLAN4091；VLAN4090；VLAN4089等等）。这些VLAN是内部操作所必需的，其优先级低于用户配置的VLAN。

## 多个交换组

CRS1xx/2xx系列交换机允许你使用带有硬件卸载的多个网桥，可以轻松地隔离多个交换机组。可以通过简单地创建多个网桥和启用硬件卸载来实现。

!!!warning 多个硬件卸载的网桥配置被设计为快速和简单的端口隔离解决方案，但它限制了CRS交换芯片支持的一部分VLAN功能。对于高级配置，在CRS交换芯片内为所有端口使用一个网桥，配置VLAN，用端口隔离配置文件隔离端口组。
  
CRS1xx/2xx系列交换机能够在启用(R)STP的情况下运行多个硬件卸载网桥，但不建议这样做，因为该设备的设计不是为了在硬件层面上运行多个(R)STP实例。要隔离多个交换机组并启用(R)STP，你应该用端口隔离配置文件配置来隔离端口组。

# 全局设置

___

CRS交换芯片可从`/interface ethernet switch`控制台菜单中配置。

**子菜单:** `/interface ethernet switch`
| 属性                                                                                                                                                          | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **name** (_string value_; Default: **switch1**)                                                                                                               | 交换名称                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| **bridge-type** (_customer-vid-used-as-lookup-vid                           \| service-vid-used-as-lookup-vid_; Default: **customer-vid-used-as-lookup-vid**) | 网桥类型定义了哪个VLAN标签被用作Lookup-VID。Lookup-VID作为所有基于VLAN的查询的VLAN密钥。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| **mac-level-isolation** (_yes                     \| no_; Default: **yes**)                                                                                   | 全局性地启用或禁用MAC级隔离。一旦启用，交换机将从单播转发表中检查源和目的MAC地址项及其隔离配置文件。默认情况下，交换机将学习MAC地址并将其放入 "混杂 "隔离配置文件。在创建静态单播项时可以使用其他隔离配置文件。如果源MAC地址或目的MAC地址位于`promiscuous`隔离配置文件上，数据包将被转发。如果源MAC地址和目的MAC地址都位于同一个 "community1 "或 "community2 "隔离配置上，数据包将被转发。当源和目的MAC地址隔离配置文件为 "isolated"，或源和目的MAC地址隔离配置文件来自不同的社区（例如，源MAC地址是 "community1"，目的MAC地址是 "community2"）时，数据包将被丢弃。当MAC级隔离被全局禁用时，隔离将被绕过。 |
| **use-svid-in-one2one-vlan-lookup** (_yes         \| no_; Default: **no**)                                                                                    | 是否使用服务VLAN id进行1:1 VLAN交换查询。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| **use-cvid-in-one2one-vlan-lookup** (_yes         \| no_; Default: **yes**)                                                                                   | 是否使用客户VLAN id进行1:1 VLAN交换查询。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| **multicast-lookup-mode** (_dst-ip-and-vid-for-ipv4 \| dst-mac-and-vid-always_;Default:**dst-ip-and-vid-for-ipv4**)                                           | IPv4 组播网桥的查找模式。<br>- dst-mac-and-vid-always \- 对于所有数据包类型，查找关键字是目标 MAC 和 VLAN id。<br>- dst-ip-and-vid-for-ipv4 \- 对于 IPv4 数据包查找关键字是目标 IP 和 VLAN id。 对于其他数据包类型，查找关键字是目标 MAC 和 VLAN id。                                                                                                                                                                                                                                                                                                                                                      |
| **unicast-fdb-timeout** (_time interval_; Default: **5m**)                                                                                                    | 单播FDB项的超时时间。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| **override-existing-when-ufdb-full** (_yes \| no_; Default: **no**)                                                                                           | 启用或禁用来覆盖现有的项，当UFDB已满时，该项具有最低的老化值。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |

| 属性                                                                                                                                | 说明                                                                  |
| ----------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| **drop-if-no-vlan-assignment-on-ports** (_ports_; Default: **none**)                                                                | 放弃帧的端口，如果没有应用基于MAC，基于协议的VLAN分配或入站VLAN转换。 |
| **drop-if-invalid-or-src-port-                                       \|\-not-member-of-vlan-on-ports** (_ports_; Default: **none**) | 丢弃无效和其他端口VLAN id帧的端口。                                   |
| **unknown-vlan-lookup-mode** (_ivl \| svl_; Default: **svl**)                                                                       | 无效VLAN的数据包的查找和学习模式。                                    |
| **forward-unknown-vlan** (_yes \| no_; Default: **yes**)                                                                            | 是否允许转发不属于VLAN表成员的VLAN。                                  |

| 属性                                                                     | 说明                                                                                                                                 |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------ |
| **bypass-vlan-ingress-filter-for** (_protocols_; Default: **none**)      | 从入站VLAN过滤中排除的协议。这些协议如果有无效的VLAN就不会被丢弃。(arp, dhcpv4, dhcpv6, eapol, igmp, mld, nd, pppo-discovery, ripv1) |
| **bypass-ingress-port-policing-for** (_protocols_; Default: **none**)    | 被排除在入站端口管制之外的协议。(arp, dhcpv4, dhcpv6, eapol, igmp, mld, nd, pppo-discovery, ripv1)                                   |
| **bypass-l2-security-check-filter-for** (_protocols_; Default: **none**) | 被排除在策略规则安全检查之外的协议。(arp, dhcpv4, dhcpv6, eapol, igmp, mld, nd, pppo-discovery, ripv1)                               |

| 属性                                                                                                                          | 说明                                                                                                                                                                                                                                                                                                                                       |
| ----------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **ingress-mirror0** (_port \| trunk,format_; Default: **none,modified**)                                                      | 第一个入站镜像分析器端口或聚合和镜像格式。<br>- analyzer-configured \- 数据包与到达目的地的数据包相同。 VLAN格式根据分析器端口的VLAN配置修改。<br>- modified \- 数据包与到达目的地的数据包相同。 VLAN格式根据出端口的VLAN配置修改。<br>- original \- 流量被镜像，没有对原始传入数据包格式进行任何更改。 但是在边缘端口剥离了业务VLAN标签。 |
| **ingress-mirror1** (_port \| trunk,format_; Default: **none,modified**)                                                      | 第二个入站镜像分析器端口或聚合和镜像格式：<br>- analyzer-configured \- 数据包与到达目的地的数据包相同。 VLAN格式根据分析器端口的VLAN配置修改。<br>- modified \- 数据包与到达目的地的数据包相同。 VLAN格式根据出端口的VLAN配置修改。<br>- original \- 流量被镜像，没有对原始传入数据包格式进行任何更改。 但是在边缘端口剥离了业务VLAN标签。 |
| **ingress-mirror-ratio** (_1/32768..1/1_; Default: **1/1**)                                                                   | 入站镜像数据包占所有数据包的比例。                                                                                                                                                                                                                                                                                                         |
| **egress-mirror0** (_port \| trunk,format_; Default: **none,modified**)                                                       | 第一个出站镜像分析器端口或聚合和镜像格式：<br>- analyzer-configured \- 数据包与到达目的地的数据包相同。 VLAN格式根据分析器端口的VLAN配置修改。<br>- modified \- 数据包与到达目的地的数据包相同。 VLAN格式根据出端口的VLAN配置修改。<br>- original \- 流量被镜像，没有对原始传入数据包格式进行任何更改。 但是在边缘端口剥离了业务VLAN标签。 |
| **egress-mirror1** (_port \| trunk,format_; Default: **none,modified**)                                                       | 第二出站镜像分析器端口或聚合和镜像格式：<br>- analyzer-configured \- 数据包与到达目的地的数据包相同。 VLAN格式根据分析器端口的VLAN配置修改。<br>- modified \- 数据包与到达目的地的数据包相同。 VLAN格式根据出端口的VLAN配置修改。<br>- original \- 流量被镜像，没有对原始传入数据包格式进行任何更改。 但是在边缘端口剥离了业务VLAN标签。   |
| **egress-mirror-ratio** (_1/32768..1\/1_; Default: **1/1**)                                                                   | 出站镜像数据包与所有数据包的比例。                                                                                                                                                                                                                                                                                                         |
| **mirror-egress-if-ingress-mirrored** (_yes \| no_; Default: **no**)                                                          | 当一个数据包同时应用于入站和出站镜像时，如果此设置被禁用，则只对数据包执行入站镜像。如果此设置被启用，两种镜像类型都被应用。                                                                                                                                                                                                               |
| **mirror-tx-on-mirror-port** (_yes \| no_; Default: **no**)                                                                   |                                                                                                                                                                                                                                                                                                                                            |
| **mirrored-packet-qos-priority** (_0..7_; Default: **0**)                                                                     | 镜像数据包中标注的优先级。                                                                                                                                                                                                                                                                                                                 |
| **mirrored-packet-drop-precedence** (_drop \| green \| red \| yellow_; Default: **green**)                                    | 镜像数据包中标注的丢弃优先级。这个QoS属性用于镜像数据包的排队或丢弃。                                                                                                                                                                                                                                                                      |
| **fdb-uses** (_mirror0                                                                     \| mirror1_; Default: **mirror0**) | 用于FDB的镜像的分析器端口。                                                                                                                                                                                                                                                                                                                |
| **vlan-uses** (_mirror0                                                                    \| mirror1_; Default: **mirror0**) | 用于VLAN的镜像的分析器端口。                                                                                                                                                                                                                                                                                                               |

# 端口设置

___

**子菜单:** `/interface ethernet switch port`

| 属性                                                                                                                                                | 说明                                                                                                                                                                                                                                                                                                  |
| --------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **vlan-type** (_edge-port                    \| network-port_; Default: **network-port**)                                                           | 端口VLAN类型指定在UFDB学习中是否使用VLAN id。网络端口在UFDB中学习VLAN id，边缘端口不学习--VLAN 0。 它只能在IVL学习模式下观察。                                                                                                                                                                        |
| **isolation-leakage-profile-override** (_yes \| no_; Default: <br>**!isolation-leakage-profile-override**)**isolation-leakage-profile** (_0..31_; ) | 用于端口隔离/泄漏配置的自定义端口配置文件。<br>- 端口级隔离配置文件 0。 上行端口 - 允许端口与设备中的所有端口通信。<br>- Port-level isolation profile 1. Isolated port - 允许端口只与上行端口通信。<br>- Port-level isolation profile 2 - 31. Community port - 允许相同社区端口和上行端口之间的通信。 |
| **learn-override** (_yes \| no_; Default: **!learn-override**)<br>**learn-limit** (_1..1023_; Default: **!learn-limit**)                            | 启用或禁用MAC地址学习并在端口上设置MAC限制。当 !learning-override 和 !learning-limit 时，MAC学习限制默认为禁用。从RouterOS v6.42开始，在`/interface bridge port`菜单下，属性learn-override被替换为learn。                                                                                             |
| **drop-when-ufdb-entry-src-drop** (_yes \| no_; Default: **yes**)                                                                                   | 当UFDB项有src-drop动作时，启用或禁止丢弃数据包。                                                                                                                                                                                                                                                      |
| **allow-unicast-loopback** (_yes \| no_; Default: **no**)                                                                                           | 端口上的单播环回。启用后，当源端口和目的端口是同一个已知的单播数据包时，允许发回。                                                                                                                                                                                                                    |
| **allow-multicast-loopback** (_yes \| no_; Default: **no**)                                                                                         | 端口上的多播环回。启用后，当源端口和目的端口相同时，允许回送注册的组播或广播数据包。                                                                                                                                                                                                                  |
| **action-on-static-station-move** (_copy-to-cpu \| drop \| forward \| redirect-to-cpu_; Default: **forward**)                                       | 当UFDB已经包含了具有这种MAC地址但具有不同端口的静态项时，对数据包采取行动。                                                                                                                                                                                                                           |
| **drop-dynamic-mac-move** (_yes \| no_; Default: **no**)                                                                                            | 如果MAC地址已经在其他端口上学习了，则在UFDB超时前禁止重新学习MAC地址。                                                                                                                                                                                                                                |

| 属性                                                                                                                                                        | 说明                                                                                                                                                                          |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **allow-fdb-based-vlan-translate** (_yes                     \| no_; Default: **no**)                                                                       | 在端口上启用或禁用基于MAC地址的VLAN转换。                                                                                                                                     |
| **allow-mac-based-service-vlan-assignment-for** (_all-frames \| none  \| _tagged-frame-only \| untagged-and-priority-tagged-frame-only_; Default:**none**)  | 应用基于MAC地址的服务VLAN转换的帧类型。                                                                                                                                       |
| **allow-mac-based-customer-vlan-assignment-for** ( _all-frames \| none \| tagged-frame-only \| untagged-and-priority-tagged-frame-only_ ; Default:**none**) | 适用于基于MAC地址的客户VLAN转换的帧类型。                                                                                                                                     |
| **default-customer-pcp** (_0..7_; Default: **0**)                                                                                                           | 端口的默认客户PCP。                                                                                                                                                           |
| **default-service-pcp** (_0..7_; Default: **0**)                                                                                                            | 端口的默认服务PCP。                                                                                                                                                           |
| **pcp-propagation-for-initial-pcp** (_yes \| no_; Default: **no**)                                                                                          | 为入站处的初始 PCP 分配启用或禁用 PCP 传播。<br>- 如果端口 vlan-type 是边缘端口，则服务 PCP 从客户 PCP 复制。<br>- 如果端口 vlan-type 是网络端口，则从服务 PCP 复制客户 PCP。 |
| **filter-untagged-frame** (_yes \| no_; Default: **no**)                                                                                                    | 是否在端口上过滤未标记的帧。                                                                                                                                                  |
| **filter-priority-tagged-frame** (_yes \| no_; Default: **no**)                                                                                             | 是否在端口上过滤有优先权标记的帧。                                                                                                                                            |
| **filter-tagged-frame** (_yes \| no_; Default: **no**)                                                                                                      | 是否要过滤端口上的标记帧。                                                                                                                                                    |

| 属性                                                                                                     | 说明                                                                                                                                                                                                                                                                |
| -------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **egress-vlan-tag-table-lookup-key** (_according-to-bridge-type \| egress-vid_; Default: **egress-vid**) | 出站VLAN表（VLAN标签）查询。<br>- egress-vid \- 查找 VLAN id 在配置边缘端口时为 CVID，在配置网络端口时为 SVID。<br>- according-to-bridge-type \- 配置客户 VLAN 网桥时查找 VLAN id 为 CVID，配置服务 VLAN 网桥时为 SVID。 服务 VLAN 网桥中边缘端口的客户标签未修改。 |
| **egress-vlan-mode** (_tagged \| unmodified \| untagged_; Default: **unmodified**)                       | 端口上的出站 VLAN 标记操作。                                                                                                                                                                                                                                        |
| **egress-pcp-propagation** (_yes \| no_; Default: **no**)                                                | 启用或禁用出站 PCP 传播。<br>- 如果端口 vlan-type 是边缘端口，则服务 PCP 从客户 PCP 复制。<br>- 如果端口 vlan-type 是网络端口，则从服务 PCP 复制客户 PCP。                                                                                                          |

| 属性                                                                                                | 说明                           |
| --------------------------------------------------------------------------------------------------- | ------------------------------ |
| **ingress-mirror-to** (_mirror0               \| mirror1               \| none_; Default: **none**) | 基于端口的入站镜像的分析端口。 |
| **ingress-mirroring-according-to-vlan** (_yes \| no_; Default: **no**)                              |
|                                                                                                     |
| **egress-mirror-to** (_mirror0                \| mirror1               \| none_; Default: **none**) | 基于端口的出站镜像的分析端口。 |

| 属性                                                                                                                                                                                                                   | 说明                                                                                                                                                    |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **qos-scheme-precedence** (_da-based \| dscp-based \| ingress-acl-based \| pcp-based \| protocol-based \| sa-based \| vlan-based_; Default: **pcp-based, sa-based, da-based, dscp-based, protocol-based, vlan-based**) | 指定在端口入站处应用的QoS分配方案<br>- 基于da<br>- 基于 dscp<br>- 基于入站 acl<br>- 基于 pcp<br>- 基于协议<br>- 基于sa<br>- 基于vlan                    |
| **pcp-or-dscp-based-qos-change-dei** (_yes \| no_; Default: **no**)                                                                                                                                                    | 启用或禁用基于PCP或DSCP的端口DEI改变。                                                                                                                  |
| **pcp-or-dscp-based-qos-change-pcp** (_yes \| no_; Default: **no**)                                                                                                                                                    | 启用或禁用端口上的PCP或基于DSCP的PCP改变。                                                                                                              |
| **pcp-or-dscp-based-qos-change-dscp** (_yes \| no_; Default: **no**)                                                                                                                                                   | 启用或禁用端口上基于PCP或DSCP的DSCP改变。                                                                                                               |
| **dscp-based-qos-dscp-to-dscp-mapping** (_yes \| no_; Default: **yes**)                                                                                                                                                | 启用或禁用端口上的DSCP到内部DSCP的映射。                                                                                                                |
| **pcp-based-qos-drop-precedence-mapping** (_PCP/DEI-range:drop-precedence_; Default: **0-15:green**)                                                                                                                   | drop precedence 的新值，用于 PCP\/DEI 到 drop precedence (drop \| green \| red \| yellow) 映射。 多个映射允许用逗号分隔，例如 “0-7：黄色，8-15：红色”。 |
| **pcp-based-qos-dscp-mapping** (_PCP/DEI-range:DEI_; Default: **0-15:0**)                                                                                                                                              | PCP/DEI 到 DSCP (0..63) 映射的 DSCP 新值。 多个映射允许用逗号分隔，例如 “0-7：25，8-15：50”。                                                           |
| **pcp-based-qos-dei-mapping** (_PCP/DEI-range:DEI_; Default: **0-15:0**)                                                                                                                                               | PCP\/DEI 到 DEI (0..1) 映射的新 DEI 值。 多个映射允许用逗号分隔，例如 “0-7:0,8-15:1”。                                                                  |
| **pcp-based-qos-pcp-mapping** (_PCP/DEI-range:DEI_; Default: **0-15:0**)                                                                                                                                               | PCP\/DEI 到 PCP (0..7) 映射的新 PCP 值。 多个映射允许用逗号分隔，例如 “0-7：3，8-15：4”。                                                               |
| **pcp-based-qos-priority-mapping** (_PCP/DEI-range:DEI_; Default: **0-15:0**)                                                                                                                                          | PCP\/DEI 到优先级 (0..15) 映射的内部优先级的新值。 多个映射允许用逗号分隔，例如 “0-7：5，8-15：15”。                                                    |

| 属性                                                                                                                                                                                   | 说明                                                                       |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| **priority-to-queue** (_priority-range:queue_; Default: **0-15:0,1:1,2:2,3:3**)                                                                                                        | 每个端口的内部优先级（0...15）与队列（0...7）的映射。                      |
| **per-queue-scheduling** (_Scheduling-type:Weight_;<br>Default: **wrr-group0:1,wrr-group0:2,wrr-group0:4,wrr-group0:8,wrr-group0:16,wrr-group0:32,** **wrr-group0:64,wrr-group0:128**) | 设置端口对每个队列组的流量整形使用严格或加权循环策略，每个队列用逗号分隔。 |
  
| 属性                                                                                                                                                  | 说明                                                                                                                                         |
| ----------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **ingress-customer-tpid-override** (_yes \| no_;Default:**!ingress-customer-tpid-override**)                                                          |
| **ingress-customer-tpid** (_0..10000_; Default: **0x8100**)                                                                                           | 入站客户TPID覆盖允许接受具有自定义客户标签TPID的特定帧。默认值是针对802.1Q帧的标签。                                                         |
| **egress-customer-tpid-override** (_yes \| no_; Default: **!egress-customer-tpid-override**)                                                          |
| **egress-customer-tpid** (_0..10000_; Default:**0x8100**)                                                                                             | Egress customer TPID override allows custom identification for egress frames with a customer tag. Default value is for tag of 802.1Q frames. |
| **ingress-service-tpid-override** (_yes \| no_; Default:**!ingress-service-tpid-override**)**ingress-service-tpid** (_0..10000_; Default: **0x88A8**) | 入站服务TPID覆盖允许接受具有自定义服务标签TPID的特定帧。默认值是针对802.1AD帧的服务标签。                                                    |
| **egress-service-tpid-override** (_yes \| no_; Default:**!egress-service-tpid-override**) **egress-service-tpid** (_0..10000_; Default:**0x88A8**)    | 出站服务TPID覆盖允许对带有服务标签的出站帧进行自定义识别。默认值是针对802.1AD帧的服务标签。                                                  |

| 属性                                                                    | 说明                                                                                                                                                                                                                                                                                                                              |
| ----------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **custom-drop-counter-includes** (_counters_; Default: **none**)        | 自定义包括计算交换机端口的丢弃数据包，自定义丢弃数据包计数器。<br>- **device-loopback**<br>- **fdb-hash-violation**<br>- **exceeded-port-learn-limitation**。<br>- **dynamic-station-move**<br>- **static-station-move**<br>- **ufdb-source-drop**<br>- **host-source-drop**<br>- **unknown-host**<br>- **ingress-vlan-filtered** |
| **queue-custom-drop-counter0-includes** (_counters_; Default: **none**) | 自定义包括计算交换机端口tx-queue-custom0-drop-packet的丢包和tx-queue-custom0-drop-byte计数器的字节。<br>- **red**<br>- **yellow**<br>- **green**<br>- **queue0**<br>- **...**<br>- **queue7**                                                                                                                                     |
| **queue-custom-drop-counter1-includes** (_counters_; Default: **none**) | 自定义包括计算交换机端口tx-queue-custom1-drop-packet的丢包和tx-queue-custom1-drop-byte计数器的字节。<br>- **red**<br>- **yellow**<br>- **green**<br>- **queue0**<br>- **...**<br>- **queue7**                                                                                                                                     |
| **policy-drop-counter-includes** (_counters_; Default: **none**)        | 自定义包括为交换机端口策略计算丢弃的数据包--丢弃数据包计数器。<br>- **ingress-policing**<br>- **ingress-acl**<br>- **egress-policing**<br>- **egress-acl**                                                                                                                                                                        |

# 转发数据库

___

## 单播FDB

单播转发数据库最多支持16318个MAC项。

**子菜单:** `/interface ethernet switch unicast-fdb`

| 属性                                                                                                    | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **action** (_action_; Default: **forward**)                                                             | UFDB项的动作。<br>- dst-drop 当数据包的目的MAC与该项匹配时，数据包被丢弃。<br>- dst-redirect-to-cpu （当数据包的目的MAC与项匹配时，数据包将被重定向到CPU。<br>- forward （转发）- 数据包被转发。<br>- src-and-dst-drop 当数据包的源MAC或目的MAC与项匹配时，数据包被丢弃。<br>- src-and-dst-redirect-to-cpu （当数据包的源MAC或目的MAC与项匹配时，数据包会被重定向到CPU。<br>- src-drop （当数据包的源MAC与项匹配时，数据包被丢弃。<br>- src-redirect-to-cpu （当数据包的源MAC与项匹配时，数据包会被重定向到CPU。 |
| **disabled** (_yes \| no_; Default: **no**)                                                             | 启用或禁用单播FDB项                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| **isolation-profile** (_community1 \| community2 \| isolated \| promiscuous_; Default: **promiscuous**) | MAC级别隔离配置文件。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| **mac-address** (_MAC address_)                                                                         | 当目标 MAC 或源 MAC 与项匹配时，操作命令适用于数据包。                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **mirror** (_yes \| no_; Default: **no**)                                                               | 启用或禁用基于源 MAC 或目标 MAC 的镜像。                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| **port** (_port_)                                                                                       | 单播 FDB 项的匹配端口。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **qos-group** (_none_; Default: **none**)                                                               | 从 QoS 组菜单中定义的 QoS 组。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| **svl** (_yes \| no_; Default: **no**)                                                                  | 单播FDB学习模式。<br>共享VLAN学习（svl）--学习/查询基于MAC地址--不基于VLAN ID。<br>独立VLAN学习（ivl）--学习/查询是基于MAC地址和VLAN ID。                                                                                                                                                                                                                                                                                                                                                                        |
| **vlan-id** (_0..4095_)                                                                                 | 单播FDB查询/学习VLAN ID。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |

## 多播FDB

CRS125交换机芯片在MFDB中最多支持1024个项，用于组播转发。对于每个组播数据包，都会在MFDB中进行目的MAC或目的IP的查找。MFDB项不会被自动学习，只能被配置。

**子菜单:** `/interface ethernet switch multicast-fdb`

| 属性                                                               | 说明                                                                                                                                          |
| ------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------- |
| **address** (_X.X.X.X                     \| XX:XX:XX:XX:XX:XX_)   | 匹配多播数据包的IP地址或MAC地址。                                                                                                             |
| **bypass-vlan-filter** (_yes              \| no_; Default: **no**) | 允许绕过VLAN过滤，用于匹配多播数据包。                                                                                                        |
| **disabled** (_yes                        \| no_; Default: **no**) | 启用或禁用多播FDB项。                                                                                                                         |
| **ports** (_ports_)                                                | 用于多播流量的成员端口。                                                                                                                      |
| **qos-group** (_none_; Default: **none**)                          | 从QoS组菜单中定义的QoS组。                                                                                                                    |
| **svl** (_yes                             \| no_; Default: **no**) | 多播FDB学习模式。<br>- 共享VLAN学习（svl）--学习/查询基于MAC地址--不基于VLAN ID。<br>- 独立VLAN学习（ivl）--学习/查询是基于MAC地址和VLAN ID。 |
| **vlan-id** (_0..4095_; Default: **0**)                            | 多播FDB查找VLAN id。如果VLAN学习模式是IVL，VLAN id就是查找id，否则VLAN id = 0。                                                               |

## 保留FDB

Cloud Router Switch支持256个RFDB项。每个RFDB项可以存储带有特定命令的第2层单播或多播MAC地址。

**子菜单:** `/interface ethernet switch reserved-fdb`

| 属性                                                                                   | 说明                                                                                                                                                                                                                                                                                       |
| -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **action** (_copy-to-cpu \| drop \| forward \| redirect-to-cpu_; Default: **forward**) | RFDB项的动作。<br>- copy-to-cpu 当数据包的目的MAC与该项匹配时，数据包被复制到CPU。<br>- drop- 当数据包的目的MAC与项匹配时，数据包被丢弃。<br>- forward （转发）- 当数据包的目的MAC与该项相匹配时，数据包被转发。<br>- redirect-to-cpu （当数据包的目的MAC与项匹配时，数据包被重定向到CPU。 |
| **bypass-ingress-port-policing** (_yes \| no_; Default: **no**)                        | 允许绕过入站端口规则器的匹配数据包。                                                                                                                                                                                                                                                       |
| **bypass-ingress-vlan-filter** (_yes \| no_; Default: **no**)                          | 允许绕过VLAN过滤的匹配数据包。                                                                                                                                                                                                                                                             |
| **disabled** (_yes \| no_; Default: **no**)                                            | 启用或禁用保留的FDB项。                                                                                                                                                                                                                                                                    |
| **mac-address** (_MAC address_; Default: **00:00:00:00:00:00**)                        | 匹配的MAC地址为保留的FDB项。                                                                                                                                                                                                                                                               |
| **qos-group** (_none_; Default: **none**)                                              | 从QoS组菜单中定义的QoS组。                                                                                                                                                                                                                                                                 |

# VLAN

___

## VLAN表

VLAN表支持4096个项，用于存储VLAN成员信息以及其他VLAN信息，如QoS、隔离、强制VLAN、学习和镜像。

**子菜单:** `/interface ethernet switch vlan`

| 属性                                              | 说明                                                                                                                                                              |
| ------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **disabled** (_yes \| no_; Default: **no**)       | 指示VLAN项是否被禁用。只有启用的项才被应用于查找过程和转发决策。                                                                                                  |
| **flood** (_yes    \| no_; Default: **no**)       | 启用或停用每个VLAN的强制VLAN泛滥。如果该功能被启用，UFDB或MFDB中目标MAC查询的结果被忽略，数据包被强制在VLAN中泛滥。                                               |
| **ingress-mirror** (_yes \| no_; Default: **no**) | 启用每个VLAN的入站镜像，以支持基于VLAN的镜像功能。                                                                                                                |
| **learn** (_yes \| no_; Default: **yes**)         | 启用或禁用VLAN的源MAC学习。                                                                                                                                       |
| **ports** (_ports_)                               | VLAN的成员端口                                                                                                                                                    |
| **qos-group** (_none_; Default: **none**)         | 从QoS组菜单中定义的QoS组。                                                                                                                                        |
| **svl** (_yes \| no_; Default: **no**)            | FDB查询模式用于UFDB和MFDB中的查询。<br>- 共享VLAN学习（svl）--学习/查询是基于MAC地址，而不是VLAN ID。<br>- 独立VLAN学习（ivl）--学习/查询是基于MAC地址和VLAN ID。 |
| **vlan-id** (_0..4095_)                           | VLAN成员项的VLAN id。                                                                                                                                             |

## 出站VLAN标签

出站数据包可以被分配不同的VLAN标签格式。当数据包被发送到出站端口（目标端口）时，VLAN标签可以被移除、添加或保持原样。每个端口对出站的VLAN标签格式有专门的控制。标签格式包括。

- 无标签的
- 有标签
- 未修改的

出站VLAN标签表包括4096个项用于VLAN标签选择。

**子菜单:** `/interface ethernet switch egress-vlan-tag`

| Property                                            | Description                |
| --------------------------------------------------- | -------------------------- |
| **disabled** (_yes         \| no_; Default: **no**) | 启用或禁用出站VLAN标签项。 |
| **tagged-ports** (_ports_)                          | 在出站处被标记的端口。     |
| **vlan-id** (_0..4095_)                             | 在出站处被标记的VLAN ID。  |

## 入站/出站VLAN转换

入站VLAN转换表允许每个端口有多达15个项。可以从数据包头中选择一个或多个字段，以便在Ingress VLAN Translation表中查找。在第一个匹配项中配置的S-VLAN或C-VLAN或两者都被分配给数据包。

**子菜单:** `/interface ethernet switch ingress-vlan-translation`

**子菜单:** `/interface ethernet switch egress-vlan-translation`

| 属性                                                                                                                                                                                                                                                                                            | 说明                                                                                                                           |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| **customer-dei** (_0..1_; Default: **none**)                                                                                                                                                                                                                                                    | 与客户标签的DEI相匹配。                                                                                                        |
| **customer-pcp** (_0..7_; Default: **none**)                                                                                                                                                                                                                                                    | 与客户标签的PCP相匹配。                                                                                                        |
| **customer-vid** (_0..4095_; Default: **none**)                                                                                                                                                                                                                                                 | 与客户标签匹配的VLAN ID。                                                                                                      |
| **customer-vlan-format** (_any                      \| priority-tagged-or-tagged                                                                                                                        \| tagged                                      \| untagged-or-tagged_; Default:**any**) | VLAN转换规则有效的带有客户标签的帧的类型。                                                                                     |
| **disabled** (_yes                                  \| no_; Default: **no**)                                                                                                                                                                                                                    | 启用或禁用VLAN转换项。                                                                                                         |
| **new-customer-vid** (_0..4095_; Default: **none**)                                                                                                                                                                                                                                             | 取代匹配的客户VLAN ID的新客户VLAN ID。如果设置为4095并使用入站VLAN转换，则流量会被丢弃。                                       |
| **new-service-vid** (_0..4095_; Default: **none**)                                                                                                                                                                                                                                              | 替换匹配的服务VLAN id的新服务VLAN id。                                                                                         |
| **pcp-propagation** (_yes                           \| no_; Default: **no**)                                                                                                                                                                                                                    | 启用或禁用PCP传播。<br>- 如果端口类型是Edge，客户PCP将从服务PCP中复制。<br>- 如果端口类型是Network，服务PCP将从客户PCP中复制。 |
| **ports** (_ports_)                                                                                                                                                                                                                                                                             | 为VLAN转换规则匹配的交换机端口。                                                                                               |
| **protocol** (_protocols_; Default: **none**)                                                                                                                                                                                                                                                   | 匹配的以太网协议。 _(仅用于入站VLAN转换)_                                                                                      |
| **sa-learning** (_yes \| no_; Default: **no**)                                                                                                                                                                                                                                                  | 启用或禁用VLAN转换后的源MAC学习。 (仅适用于入站VLAN转换)_                                                                      |
| **service-dei** (_0..1_; Default: **none**)                                                                                                                                                                                                                                                     | 与服务标签的DEI匹配。                                                                                                          |
| **service-pcp** (_0..7_; Default: **none**)                                                                                                                                                                                                                                                     | 与服务标签的PCP匹配。                                                                                                          |
| **service-vid** (_0..4095_; Default: **none**)                                                                                                                                                                                                                                                  | 与服务标签的VLAN ID匹配。                                                                                                      |
| **service-vlan-format** (_any \| priority-tagged-or-tagged \| tagged \| untagged-or-tagged_; Default:**any**)                                                                                                                                                                                   | VLAN转换规则有效的带有服务标签的帧类型。                                                                                       |

下面是一个触发设置了某种VLAN格式规则的流量表，注意，用VLAN ID 0标记的流量是一种特殊情况，也会被考虑在内。

| 属性                          | 说明                                                                                                             |
| ----------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| **any**                       | 接受：<br>- 未标记的流量<br>- 标签流量<br>- 设置了优先级的标签流量<br>- VLAN 0流量<br>- 设置了优先级的VLAN 0流量 |
| **priority-tagged-or-tagged** | 接受：<br>- 标签流量<br>- 设置了优先级的标签流量<br>- VLAN 0流量<br>- 设置了优先级的VLAN 0流量                   |
| **tagged**                    | 接受：<br>- 标签流量<br>- 设置了优先权的标签流量                                                                 |
| **untagged-or-tagged**        | 接受：<br>- 未标记的流量<br>- 标签流量<br>- 已设置优先级的标签流量                                               |

如果`VLAN-format`设置为`any`，那么`customer-vid/service-vid`设置为`0`将触发VLAN 0流量的交换规则。在这种情况下，交换机规则将寻找无标签的流量或带有VLAN 0标签的流量，在这种情况下，只有`untagged-or-tagged`会过滤掉VLAN 0流量。

## 基于协议的VLAN

基于协议的VLAN表用于为每个端口的相关协议包分配VID和QoS属性。

**子菜单:** `/interface ethernet switch protocol-based-vlan`

| Property                                                                                                                                                                                                                                                                                         | Description                                                                        |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------- |
| **disabled** (_yes                               \| no_; Default: **no**)                                                                                                                                                                                                                        | 启用或禁用基于协议的VLAN项。                                                       |
| **frame-type** (_ethernet                        \| llc                                                                                                                                    \| rfc-1042_; Default: **ethernet**)                                                                  | 匹配的帧的封装类型。                                                               |
| **new-customer-vid** (_0..4095_; Default: **0**)                                                                                                                                                                                                                                                 | 新的客户VLAN ID，用于替代指定协议的原始客户VLAN ID。如果设置为4095，则流量被丢弃。 |
| **new-service-vid** (_0..4095_; Default: **0**)                                                                                                                                                                                                                                                  | 新服务的VLAN ID，它取代了指定协议的原始服务VLAN ID。                               |
| **ports** (_ports_)                                                                                                                                                                                                                                                                              | 为基于协议的VLAN规则匹配交换机端口。                                               |
| **protocol** (_protocol_; Default: **0**)                                                                                                                                                                                                                                                        | 基于协议的VLAN规则的匹配协议。                                                     |
| **qos-group** (_none_; Default: **none**)                                                                                                                                                                                                                                                        | 从QoS组菜单中定义的QoS组。                                                         |
| **set-customer-vid-for** (_all                   \| none                                                                                                                                   \| tagged                                         \| untagged-or-priority-tagged_; Default: **all**)  | 针对不同数据包类型的客户VLAN id分配命令。                                          |
| **set-qos-for** (_all                            \| none                                                                                                                                   \| tagged                                         \| untagged-or-priority-tagged_; Default: **none**) | 适用于QoS分配命令的帧类型。                                                        |
| **set-service-vid-for** (_all                    \| none                                                                                                                                   \| tagged                                         \| untagged-or-priority-tagged_; Default: **all**)  | 针对不同数据包类型的服务VLAN id分配命令。                                          |

## 基于MAC地址的VLAN

基于MAC的VLAN表是根据源MAC分配VLAN的。

**子菜单:** `/interface ethernet switch mac-based-vlan`

| 属性                                                                      | 说明                                                                                 |
| ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| **disabled** (_yes                               \| no_; Default: **no**) | 启用或禁用基于MAC的VLAN项。                                                          |
| **new-customer-vid** (_0..4095_; Default: **0**)                          | 新的客户VLAN ID，它取代了匹配数据包的原始服务VLAN ID。如果设置为4095，则流量被丢弃。 |
| **new-service-vid** (_0..4095_; Default: **0**)                           | The new service VLAN id which replaces original service VLAN id for matched packets. |
| **src-mac-address** (_MAC address_)                                       | 基于MAC的VLAN规则的匹配源MAC地址。                                                   |
  
所有CRS1xx/2xx系列交换机支持多达1024个基于MAC的VLAN项。

## 1:1 VLAN 交换

1:1 VLAN交换可以用来取代匹配数据包的常规L2网桥。当一个数据包碰到一个1:1 VLAN交换项时，该项中的目标端口信息就会被分配给该数据包。UFDB和MFDB条目中的匹配目标信息不再适用于该数据包。

**子菜单:** `/interface ethernet switch one2one-vlan-switching`

| Property                                                              | Description                                              |
| --------------------------------------------------------------------- | -------------------------------------------------------- |
| **customer-vid** (_0..4095_; Default: **0**)                          | Matching customer VLAN id for 1:1 VLAN switching.        |
| **disabled** (_yes                           \| no_; Default: **no**) | Enables or disables 1:1 VLAN switching table entry.      |
| **dst-port** (_port_)                                                 | Destination port for matched 1:1 VLAN switching packets. |
| **service-vid** (_0..4095_; Default: **0**)                           | Matching customer VLAN id for 1:1 VLAN switching.        |

# 端口隔离/泄露

___

The CRS switches support flexible multi-level isolation features, which can be used for user access control, traffic engineering and advanced security and network management. The isolation features provide an organized fabric structure allowing user to easily program and control the access by port, MAC address, VLAN, protocol, flow and frame type. The following isolation and leakage features are supported:

- Port-level isolation
- MAC-level isolation
- VLAN-level isolation
- Protocol-level isolation
- Flow-level isolation
- Free combination of the above

Port-level isolation supports different control schemes on source port and destination port. Each entry can be programmed with access control for either source port or destination port.

- When the entry is programmed with source port access control, the entry is applied to the ingress packets.

- When the entry is programmed with destination port access control, the entry is applied to the egress packets.

Port leakage allows bypassing egress VLAN filtering on the port. Leaky port is allowed to access other ports for various applications such as security, network control and management. Note: When both isolation and leakage is applied to the same port, the port is isolated.

**子菜单:** `/interface ethernet switch port-isolation`

**子菜单:** `/interface ethernet switch port-leakage`

| Property                                                                                                                                                                                                                                                                                 | Description                                                                                    |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| **disabled** (_yes                                                                            \| no_; Default: **no**)                                                                                                                                                                   | Enables or disables port isolation/leakage entry.                                              |
| **flow-id** (_0..63_; Default: **none**)                                                                                                                                                                                                                                                 |
|                                                                                                                                                                                                                                                                                          |
| **forwarding-type** (_bridged; routed_; Default: **bridged,routed**)                                                                                                                                                                                                                     | Matching traffic forwarding type on Cloud Router Switch.                                       |
| **mac-profile** (_community1                                                                  \| community2                                                                                     \| isolated                                          \| promiscuous_; Default: **none**) | Matching MAC isolation/leakage profile.                                                        |
| **port-profile** (_0..31_; Default: **none**)                                                                                                                                                                                                                                            | Matching Port isolation/leakage profile.                                                       |
| **ports** (_ports_; Default: **none**)                                                                                                                                                                                                                                                   | Isolated/leaked ports.                                                                         |
| **protocol-type** (_arp; nd; dhcpv4; dhcpv6; ripv1_; Default: **arp,nd,dhcpv4,dhcpv6,ripv1**)                                                                                                                                                                                            | Included protocols for isolation/leakage.                                                      |
| **registration-status** (_known; unknown_; Default: **known,unknown**)                                                                                                                                                                                                                   | Registration status for matching packets. Known are present in UFDB and MFDB, unknown are not. |
| **traffic-type** (_unicast; multicast; broadcast_; Default: **unicast,multicast,broadcast**)                                                                                                                                                                                             | Matching traffic type.                                                                         |
| **type** (_dst                                                                                \| src_; Default: **src**)                                                                                                                                                                 | Lookup type of the isolation/leakage entry:                                                    |
- src \- Entry applies to ingress packets of the ports.
- dst \- Entry applies to egress packets of the ports.

 |
| **vlan-profile** (_community1 \| community2 \| isolated \| promiscuous_; Default: **none**) | Matching VLAN isolation/leakage profile. |

# 聚合

___

The Trunking in the Cloud Router Switches provides static link aggregation groups with hardware automatic failover and load balancing. IEEE802.3ad and IEEE802.1ax compatible Link Aggregation Control Protocol is not supported. Up to 8 Trunk groups are supported with up to 8 Trunk member ports per Trunk group. CRS Port Trunking calculates transmit-hash based on all following parameters: L2 src-dst MAC + L3 src-dst IP + L4 src-dst Port.

**子菜单:** `/interface ethernet switch trunk`

| Property                                                                | Description                              |
| ----------------------------------------------------------------------- | ---------------------------------------- |
| **disabled** (_yes                             \| no_; Default: **no**) | Enables or disables port trunking entry. |
| **member-ports** (_ports_)                                              | Member ports of the Trunk group.         |
| **name** (_string value_; Default: **trunkX**)                          | Name of the Trunk group.                 |

# Quality of Service

___

## 整形器

Traffic shaping restricts the rate and burst size of the flow which is transmitted out from the interface. The shaper is implemented by a token bucket. If the packet exceeds the maximum rate or the burst size, which means no enough token for the packet, the packet is stored to buffer until there is enough token to transmit it.

**子菜单:** `/interface ethernet switch shaper`

| Property                                                                                                                                              | escription                                                               |
| ----------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| **burst** (_integer_; Default: **100k**)                                                                                                              | Maximum data rate which can be transmitted while the burst is allowed.   |
| **disabled** (_yes                       \| no_; Default: **no**)                                                                                     | Enables or disables traffic shaper entry.                                |
| **meter-unit** (_bit                     \| packet_; Default: **bit**)                                                                                | Measuring units for traffic shaper rate.                                 |
| **port** (_port_)                                                                                                                                     | Physical port for traffic shaper.                                        |
| **rate** (_integer_; Default: **1M**)                                                                                                                 | Maximum data rate limit.                                                 |
| **target** (_port                        \| queueX                                                                 \| wrr-groupX_; Default: **port**) | Three levels of shapers are supported on each port (including CPU port): |
- Port level \- Entry applies to the port of the switch-chip.
- WRR group level \- Entry applies to one of the 2 Weighted Round Robin queue groups (wrr-group0, wrr-group1) on the port.
- Queue level \- Entry applies to one of the 8 queues (queue0 - queue7) on the port. |

## Ingress Port Policer

**子菜单:** `/interface ethernet switch ingress-port-policer`

| Property                                                          | Description                                                            |
| ----------------------------------------------------------------- | ---------------------------------------------------------------------- |
| **burst** (_integer_; Default: **100k**)                          | Maximum data rate which can be transmitted while the burst is allowed. |
| **disabled** (_yes                       \| no_; Default: **no**) | Enables or disables ingress port policer entry.                        |
| **meter-len** (_layer-1                  \| layer-2               | layer-3_; Default: **layer-1**)                                        | Packet classification which sets the packet byte length for metering. |
- layer-1 \- includes entire layer-2 frame + FCS + inter-packet gap + preamble.
- layer-2 \- includes layer-2 frame + FCS.
- layer-3 \- includes only layer-3 + ethernet padding without layer-2 header and FCS. |
| **meter-unit** (_bit \| packet_; Default: **bit**) | Measuring units for traffic ingress port policer rate. |
| **new-dei-for-yellow** (_0..1 \| remap_; Default: **none**) | Remarked DEI for exceeded traffic if yellow-action is remark. |
| **new-dscp-for-yellow** (_0..63 \| remap_; Default: **none**) | Remarked DSCP for exceeded traffic if yellow-action is remark. |
| **new-pcp-for-yellow** (_0..7 \| remap_; Default: **none**) | Remarked PCP for exceeded traffic if yellow-action is remark. |
| **packet-types** (_packet-types_; Default: **all types from description**) | Matching packet types for which ingress port policer entry is valid. |
| **port** (_port_) | Physical port or trunk for ingress port policer entry. |
| **rate** (_integer_) | Maximum data rate limit. |
| **yellow-action** (_drop | forward | remark_; Default: **drop**) | Performed action for exceeded traffic. |

## QoS Group

The global QoS group table is used for VLAN-based, Protocol-based and MAC-based QoS group assignment configuration.

**子菜单:** `/interface ethernet switch qos-group`

| Property                                                                                                                                                                                                                                                                             | Description                                                                                                                                       |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| **dei** (_0..1_; Default: **none**)                                                                                                                                                                                                                                                  | The new value of DEI for the QoS group.                                                                                                           |
| **disabled** (_yes                             \| no_; Default: **no**)                                                                                                                                                                                                              | Enables or disables protocol QoS group entry.                                                                                                     |
| **drop-precedence** (_drop                     \| green                                                                                                                                             \| red                                           \| yellow_; Default: **green**) | Drop precedence is internal QoS attribute used for packet enqueuing or dropping.                                                                  |
| **dscp** (_0..63_; Default: **none**)                                                                                                                                                                                                                                                | The new value of DSCP for the QoS group.                                                                                                          |
| **name** (_string value_; Default: **groupX**)                                                                                                                                                                                                                                       | Name of the QoS group.                                                                                                                            |
| **pcp** (_0..7_; Default: **none**)                                                                                                                                                                                                                                                  | The new value of PCP for the QoS group.                                                                                                           |
| **priority** (_0..15_; Default: **0**)                                                                                                                                                                                                                                               | Internal priority is a local significance of priority for classifying traffics to different egress queues on a port. (1 is highest, 15 is lowest) |

## DSCP QoS Map

The global DSCP to QOS mapping table is used for mapping from the DSCP of the packet to new QoS attributes configured in the table.

**子菜单:** `/interface ethernet switch dscp-qos-map`

| Property                                                                                                               | Description                                                           |
| ---------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| **dei** (_0..1_)                                                                                                       | The new value of DEI for the DSCP to QOS mapping entry.               |
| **drop-precedence** (_drop \| green                                                                 \| red \| yellow_) | The new value of Drop precedence for the DSCP to QOS mapping entry.   |
| **pcp** (_0..7_)                                                                                                       | The new value of PCP for the DSCP to QOS mapping entry.               |
| **priority** (_0..15_)                                                                                                 | The new value of internal priority for the DSCP to QOS mapping entry. |

## DSCP To DSCP Map

The global DSCP to DSCP mapping table is used for mapping from the packet's original DSCP to new DSCP value configured in the table.

**子菜单:** `/interface ethernet switch dscp-to-dscp`

| Property               | Description                                               |
| ---------------------- | --------------------------------------------------------- |
| **new-dscp** (_0..63_) | The new value of DSCP for the DSCP to DSCP mapping entry. |

## Policer QoS Map

**子菜单:** `/interface ethernet switch policer-qos-map`

| Property                                      | Description                                      |
| --------------------------------------------- | ------------------------------------------------ |
| **dei-for-red** (_0..1_; Default: **0**)      | Policer DEI remapping value for red packets.     |
| **dei-for-yellow** (_0..1_; Default: **0**)   | Policer DEI remapping value for yellow packets.  |
| **dscp-for-red** (_0..63_; Default: **0**)    | Policer DSCP remapping value for red packets.    |
| **dscp-for-yellow** (_0..63_; Default: **0**) | Policer DSCP remapping value for yellow packets. |
| **pcp-for-red** (_0..7_; Default: **0**)      | Policer PCP remapping value for red packets.     |
| **pcp-for-yellow** (_0..7_; Default: **0**)   | Policer PCP remapping value for yellow packets.  |

# Access Control List

___

Access Control List contains of ingress policy and egress policy engines and allows to configure up to 128 policy rules (limited by RouterOS). It is advanced tool for wire-speed packet filtering, forwarding, shaping and modifying based on Layer2, Layer3 and Layer4 protocol header field conditions.

See Summary section for Access Control List supported Cloud Router Switch devices.

Due to hardware limitations, it is not possible to match broadcast/multicast traffic on specific ports. You should use port isolation, drop traffic on ingress ports or use VLAN filtering to prevent certain broadcast/multicast traffic from being forwarded.

**子菜单:** `/interface ethernet switch acl`

ACL condition part for MAC-related fields of packets.

| Property                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | Description                                                                                                                                             |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **disabled** (_yes                       \| no_; Default: **no**)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Enables or disables ACL entry.                                                                                                                          |
| **table** (_egress                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | ingress_; Default: **ingress**)                                                                                                                         | Selects policy table for incoming or outgoing packets. |
| **invert-match** (_yes                   \| no_; Default: **no**)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Inverts whole ACL rule matching.                                                                                                                        |
| **src-ports** (_ports,trunks_)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | Matching physical source ports or trunks.                                                                                                               |
| **dst-ports** (_ports,trunks_)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | Matching physical destination ports or trunks. It is not possible to match broadcast/multicast traffic on the egress port due to a hardware limitation. |
| **mac-src-address** (_MAC address/Mask_)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | Source MAC address and mask.                                                                                                                            |
| **mac-dst-address** (_MAC address/Mask_)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | Destination MAC address and mask.                                                                                                                       |
| **dst-addr-registered** (_yes            \| no_)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Defines whether to match packets with registered state - packets which destination MAC address is in UFDB/MFDB/RFDB. Valid only in egress table.        |
| **mac-protocol** (_802.2                 \| arp                                                                                                                                                     \| homeplug-av                                                                                                                                      \| ip \| ip-or-ipv6 \| ipv6 \| ipx \| lldp \| loop-protect \| mpls-multicast \| mpls-unicast \| non-ip \| packing-compr \| packing-simple \| pppoe \| pppoe-discovery \| rarp \| service-vlan \| vlan or integer: 0..65535 decimal format or 0x0000-0xffff hex format_) | Ethernet payload type (MAC-level protocol)                                                                                                              |
- **802.2** \- 802.2 Frames (0x0004)
- **arp** \- Address Resolution Protocol (0x0806)
- **homeplug-av** \- HomePlug AV MME (0x88E1)
- **ip** \- Internet Protocol version 4 (0x0800)
- **ip-or-ipv6** \- IPv4 or IPv6 (0x0800 or 0x86DD)
- **ipv6** \- Internet Protocol Version 6 (0x86DD)
- **ipx** \- Internetwork Packet Exchange (0x8137)
- **lldp** \- Link Layer Discovery Protocol (0x88CC)
- **loop-protect** \- Loop Protect Protocol (0x9003)
- **mpls-multicast** \- MPLS multicast (0x8848)
- **mpls-unicast** \- MPLS unicast (0x8847)
- **non-ip** \- Not Internet Protocol version 4 (not 0x0800)
- **packing-compr** \- Encapsulated packets with compressed [IP packing](https://wiki.mikrotik.com/wiki/Manual:IP/Packing "Manual:IP/Packing") (0x9001)
- **packing-simple** \- Encapsulated packets with simple [IP packing](https://wiki.mikrotik.com/wiki/Manual:IP/Packing "Manual:IP/Packing") (0x9000)
- **pppoe** \- PPPoE Session Stage (0x8864)
- **pppoe-discovery** \- PPPoE Discovery Stage (0x8863)
- **rarp** \- Reverse Address Resolution Protocol (0x8035)
- **service-vlan** \- Provider Bridging (IEEE 802.1ad) & Shortest Path Bridging IEEE 802.1aq (0x88A8)
- **vlan** \- VLAN-tagged frame (IEEE 802.1Q) and Shortest Path Bridging IEEE 802.1aq with NNI compatibility (0x8100) |
| **drop-precedence** (_drop \| green \| red \| yellow_) | Matching internal drop precedence. Valid only in egress table. |
| **custom-fields** ||
ACL condition part for VLAN-related fields of packets.

| Property                           | Description                                                                 |
| ---------------------------------- | --------------------------------------------------------------------------- |
| **lookup-vid** (_0..4095_)         | VLAN id used in lookup. It can be changed before reaching the egress table. |
| **service-vid** (_0-4095_)         | Matching service VLAN id.                                                   |
| **service-pcp** (_0..7_)           | Matching service PCP.                                                       |
| **service-dei** (_0..1_)           | Matching service DEI.                                                       |
| **service-tag** (_priority-tagged  | tagged                                                                      | tagged-or-priority-tagged | untagged_) | Format of the service tag.  |
| **customer-vid** (_0-4095_)        | Matching customer VLAN id.                                                  |
| **customer-pcp** (_0..7_)          | Matching customer PCP.                                                      |
| **customer-dei** (_0..1_)          | Matching customer DEI.                                                      |
| **customer-tag** (_priority-tagged | tagged                                                                      | tagged-or-priority-tagged | untagged_) | Format of the customer tag. |
| **priority** (_0..15_)             | Matching internal priority. Valid only in egress table.                     |

ACL condition part for IPv4 and IPv6 related fields of packets.

| Property                                                                                                                                                                                        | Description                                                                                                                                                 |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **ip-src** (_IPv4/0..32_)                                                                                                                                                                       | Matching source IPv4 address.                                                                                                                               |
| **ip-dst** (_IPv4/0..32_)                                                                                                                                                                       | Matching destination IPv4 address.                                                                                                                          |
| **ip-protocol** (_tcp                         \| udp                                \| udp-lite                                                                        \| other_)               | IP protocol type.                                                                                                                                           |
| **src-l3-port** (_0-65535_)                                                                                                                                                                     | Matching Layer3 source port.                                                                                                                                |
| **dst-l3-port** (_0-65535_)                                                                                                                                                                     | Matching Layer3 destination port.                                                                                                                           |
| **ttl** (_0                                   \| 1                                 \| max                                                                             \| other_)                | Matching TTL field of the packet.                                                                                                                           |
| **dscp** (_0..63_)                                                                                                                                                                              | Matching DSCP field of the packet.                                                                                                                          |
| **ecn** (_0..3_)                                                                                                                                                                                | Matching ECN field of the packet.                                                                                                                           |
| **fragmented** (_yes                          \| no_)                                                                                                                                           | Whether to match fragmented packets.                                                                                                                        |
| **first-fragment** (_yes                      \| no_)                                                                                                                                           | YES matches not fragmented and the first fragments, NO matches other fragments.                                                                             |
| **ipv6-src** (_IPv6/0..128_)                                                                                                                                                                    | Matching source IPv6 address.                                                                                                                               |
| **ipv6-dst** (_IPv6/0..128_)                                                                                                                                                                    | Matching destination IPv6 address.                                                                                                                          |
| **mac-isolation-profile** (_community1        \| community2                         \| isolated                                                                        \| promiscuous_)         | Matches isolation profile based on UFDB. Valid only in the egress policy table.                                                                             |
| **src-mac-addr-state** (_dynamic-station-move \| sa-found                           \| sa-not-found                                                                    \| static-station-move_) | Defines whether to match packets with registered state - packets which destination MAC address is in UFDB/MFDB/RFDB. Valid only in the egress policy table. |
| **flow-id** (_0..63_)                                                                                                                                                                           |
|                                                                                                                                                                                                 |

ACL rule action part.

| Property                                             | Description |
| ---------------------------------------------------- | ----------- |
| **action** (_copy-to-cpu \| drop \| forward          | _           |
| _redirect-to-cpu \| send-to-new-dst-ports_; Default: |

**forward**)
- copy-to-cpu \- Packets are copied to CPU if they match the ACL conditions.
- drop \- Packets are dropped if they match the ACL conditions.
- forward \- Packets are forwarded if they match the ACL conditions.
- redirect-to-cpu \- Packets are redirected to CPU if they match the ACL conditions.
- send-to-new-dst-ports \- Packets are sent to new destination ports if they match the ACL conditions.

 |
| **new-dst-ports** (_ports,trunks_) | If the action is "send-to-new-dst-ports", then this property sets which ports/trunks are the new destinations. |
| **mirror-to** (_mirror0 | mirror1_) | Mirroring destination for ACL packets. |
| **policer** (_policer_) | Applied ACL Policer for ACL packets. |
| **src-mac-learn** (_yes | no_) | Whether to learn source MAC of the matched ACL packets. Valid only in the ingress policy table. |
| **new-service-vid** (_0..4095_) | New service VLAN id for ACL packets. |
| **new-service-pcp** (_0..7_) | New service PCP for ACL packets. |
| **new-service-dei** (_0..1_) | New service DEI for ACL packets. |
| **new-customer-vid** (_0..4095_) | New customer VLAN id for ACL packets. If set to 4095, then traffic is dropped. |
| **new-customer-pcp** (_0..7_) | New customer PCP for ACL packets. |
| **new-customer-dei** (_0..1_) | New customer DEI for ACL packets. |
| **new-dscp** (_0..63_) | New DSCP for ACL packets. |
| **new-priority** (_0..15_) | New internal priority for ACL packets. |
| **new-drop-precedence** (_drop | green | red | yellow_) | New internal drop precedence for ACL packets. |
| **new-registered-state** (_yes | no_) | Whether to modify packet status. YES sets packet status to registered, NO - unregistered. Valid only in the ingress policy table. |
| **new-flow-id** (_0..63_) |   
 |

Filter bypassing part for ACL packets.

| Property                               | Description           |
| -------------------------------------- | --------------------- |
| **attack-filter-bypass** (_yes         | no_; Default: **no**) |
|                                        |
| **ingress-vlan-filter-bypass** (_yes   | no_; Default: **no**) | Allows bypassing ingress VLAN filtering in the VLAN table for matching packets. Applies only to ingress policy table. |
| **egress-vlan-filter-bypass** (_yes    | no_; Default: **no**) | Allows bypassing egress VLAN filtering in the VLAN table for matching packets. Applies only to ingress policy table.  |
| **isolation-filter-bypass** (_yes      | no_; Default: **no**) | Allows bypassing the Isolation table for matching packets. Applies only to ingress policy table.                      |
| **egress-vlan-translate-bypass** (_yes | no_; Default: **no**) | Allows bypassing egress VLAN translation table for matching packets.                                                  |

## ACL Policer

**子菜单:** `/interface ethernet switch acl policer`

| Property                                                                                                                                                                                         | Description                                                                                                    |  |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------- |
| **name** (_string_; Default: **policerX**)                                                                                                                                                       | Name of the Policer used in ACL.                                                                               |
| **yellow-rate** (_integer_)                                                                                                                                                                      | Maximum data rate limit for packets with yellow drop precedence.                                               |
| **yellow-burst** (_integer_; Default: **0**)                                                                                                                                                     | Maximum data rate which can be transmitted while the burst is allowed for packets with yellow drop precedence. |
| **red-rate** (_integer_); Default: **0**)                                                                                                                                                        | Maximum data rate limit for packets with red drop precedence.                                                  |
| **red-burst** (_integer_; Default: **0**)                                                                                                                                                        | Maximum data rate which can be transmitted while the burst is allowed for packets with red drop precedence.    |
| **meter-unit** (_bit                        \| packet_; Default: **bit**)                                                                                                                        | Measuring units for ACL traffic rate.                                                                          |
| **meter-len** (_layer-1                     \| layer-2                                                                                                        \| layer-3_; Default: **layer-1**) | Packet classification which sets the packet byte length for metering.                                          |

- layer-1 \- includes entire layer-2 frame + FCS + inter-packet gap + preamble.
- layer-2 \- includes layer-2 frame + FCS.
- layer-3 \- includes only layer-3 + ethernet padding without layer-2 header and FCS.

 |
| **color-awareness** (_yes \| no_; Default: **no**) | YES makes policer to take into account pre-colored drop precedence, NO - ignores drop precedence. |
| **bucket-coupling** (_yes \| no_; Default: **no**) |   
 |
| **yellow-action** (_drop \| forward | remark_; Default: **drop**) | Performed action for exceeded traffic with yellow drop precedence. |
| **new-dei-for-yellow** (_0..1 \| remap_) | New DEI for yellow drop precedence packets. |
| **new-pcp-for-yellow** (_0..7 \| remap_) | New PCP for yellow drop precedence packets. |
| **new-dscp-for-yellow** (_0..63 | remap_) | New DSCP for yellow drop precedence packets. |
| **red-action** (_drop \| forward \| remark_; Default: **drop**) | Performed action for exceeded traffic with red drop precedence. |
| **new-dei-for-red** (_0..1 \| remap_) | New DEI for red drop precedence packets. |
| **new-pcp-for-red** (_0..7 \| remap_) | New PCP for red drop precedence packets. |
| **new-dscp-for-red** (_0..63 \| remap_) | New DSCP for red drop precedence packets. |

# See also

___

- [CRS1xx/2xx series switches examples](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=103841836)
- [CRS Router](https://wiki.mikrotik.com/wiki/Manual:CRS_Router "Manual:CRS Router")
- [CRS1xx/2xx VLANs with Trunks](https://wiki.mikrotik.com/wiki/Manual:CRS1xx/2xx_VLANs_with_Trunks "Manual:CRS1xx/2xx VLANs with Trunks")
- [Basic VLAN switching](https://help.mikrotik.com/docs/display/ROS/Basic+VLAN+switching)
- [Bridge Hardware Offloading](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-BridgeHardwareOffloading)
- [Spanning Tree Protocol](https://help.mikrotik.com/docs/display/ROS/Spanning+Tree+Protocol)
- [IGMP Snooping](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=59277403)
- [DHCP Snooping and Option 82](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-DHCPSnoopingandDHCPOption82)
- [MTU on RouterBOARD](https://help.mikrotik.com/docs/display/ROS/MTU+in+RouterOS)
- [Layer2 misconfiguratio](https://help.mikrotik.com/docs/display/ROS/Layer2+misconfiguration)