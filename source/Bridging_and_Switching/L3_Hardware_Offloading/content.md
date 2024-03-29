# 硬件卸载介绍

**第三层硬件卸载**（ L3HW也称为 IP 交换或硬件路由）允许将某些路由器功能卸载到交换芯片上。 这样路由数据包可以达到线速，这对 CPU 来说是不可能的。

## 交换配置

要启用第 3 层硬件卸载，请为交换机设置 **l3-hw-offloading=yes**：

`/interface/ethernet/switch set 0 l3-hw-offloading=yes`

### 交换机端口配置

可以为每个物理交换机端口配置第 3 层硬件卸载。 例如：

`/interface/ethernet/switch/port set sfp-sfpplus1 l3-hw-offloading=yes`

请注意，交换机和端口的 l3hw 设置不同：

- 为交换机设置 `l3-hw-offloading``=no` 完全禁用卸载 - 所有数据包都将由 CPU 路由。
- 但是，为交换机端口设置 `l3-hw-offloading``=no` 只会禁用来自/到该特定端口的硬件路由。 此外，端口仍然可以参与 Fastrack 连接卸载。

要启用完整的硬件路由，请在所有交换机端口上启用 l3hw：

```shell
/interface/ethernet/switch set 0 l3-hw-offloading=yes
/interface/ethernet/switch/port set [find] l3-hw-offloading=yes

```

要让所有数据包首先通过 CPU，并仅卸载 Fasttrack 连接，请在所有端口上禁用 l3hw，但在交换机芯片本身上保持启用：

```shell
/interface/ethernet/switch set 0 l3-hw-offloading=yes
/interface/ethernet/switch/port set [find] l3-hw-offloading=no

```

**仅当源端口和目标端口都具有 `l3-hw-offloading=yes` 时，数据包才会被硬件路由。**如果其中至少一个具有 `l3-hw-offloading=no`，则数据包将通过 CPU/防火墙，同时仅卸载 Fasttrack 连接。

下一个示例在除上游端口 (sfp-sfpplus16) 之外的所有端口上启用硬件路由。 进出 sfp-sfpplus16 的数据包将进入 CPU，因此需要进行防火墙/NAT 处理。

```shell
/interface/ethernet/switch set 0 l3-hw-offloading=yes
/interface/ethernet/switch/port set [find] l3-hw-offloading=yes
/interface/ethernet/switch/port set sfp-sfpplus16 l3-hw-offloading=no

```

现有连接可能不受“l3-hw-offloading”设置更改的影响。

### L3HW 设置

L3HW 设置菜单已在 RouterOS 版本 7.6 中引入。

**Sub-menu:** `/interface ethernet switch l3hw-settings`

| 属性                                                                   | 说明                                                                                                                                                                                                                                                                  |
| ---------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **fasttrack-hw** (_yes        \| no_; Default: **yes** (if supported)) | 启用或禁用 FastTrack HW 卸载。 除非需要 HW TCAM 内存保留，否则保持启用状态，例如，用于动态交换机 ACL 规则创建。 并非所有交换机芯片都支持 FastTrack HW 卸载（请参阅**hw-supports-fasttrack**）。                                                                       |
| **ipv6-hw** (_yes             \| no_; Default: **no**)                 | 启用或禁用 IPv6 硬件卸载。 由于 IPv6 路由占用大量硬件内存，因此仅当 IPv6 流量速度足够快并从硬件路由中受益时才启用它。                                                                                                                                                 |
| **icmp-reply-on-error** (_yes \| no_; Default: **yes**)                | 由于硬件无法发送 ICMP 消息，因此必须将数据包重定向到 CPU 以在出现错误（例如，“超时”、“需要分片”等）时发送 ICMP 回复。 启用 icmp-reply-on-error 有助于网络诊断，但可能会为 DDoS 攻击打开潜在漏洞。 如果出现错误，禁用 icmp-reply-on-error 会在硬件级别静默丢弃数据包。 |

**只读属性**

| 属性                                      | 说明                                                   |
| ----------------------------------------- | ------------------------------------------------------ |
| **hw-supports-fasttrack** (__yes \| no__) | 指示硬件（交换芯片）是否支持 FastTrack HW Offloading。 |

### 接口列表

无法直接使用接口列表来控制 `l3-hw-offloading`，因为接口列表可能包含虚拟接口（例如 VLAN），而 `l3-hw-offloading` 设置必须仅应用于物理交换机端口。 例如，如果有两个 VLAN 接口（vlan20 和 vlan30）运行在同一个交换机端口（trunk 端口）上，则不可能在 vlan20 上启用硬件路由，而在 vlan30 上保持禁用。

但是，接口列表可以用作端口选择器。 以下示例演示如何在 LAN 端口（属于“LAN”接口列表的端口）上启用硬件路由并在 WAN 端口上禁用它：

```shell
:foreach i in=[/interface/list/member/find where list=LAN] do={
    /interface/ethernet/switch/port set [/interface/list/member/get $i interface] l3-hw-offloading=yes
}
 
:foreach i in=[/interface/list/member/find where list=WAN] do={
    /interface/ethernet/switch/port set [/interface/list/member/get $i interface] l3-hw-offloading=no
}

```

请注意，由于硬件路由控制中不直接使用接口列表，**修改接口列表也不会自动反映到 l3hw 更改中**。 例如，将交换机端口添加到“LAN”接口列表不会自动在其上启用“l3-hw-offloading”。 用户必须重新运行上述脚本才能应用更改。

### MTU

硬件支持多达 8 个 MTU 配置文件，这意味着用户可以为接口设置多达 8 个不同的 MTU 值：默认 1500 + 七个自定义值。

建议在更改接口上的 MTU/L2MTU 值时禁用`l3-hw-offloading`。

**MTU 修改示例**

```shell
/interface/ethernet/switch set 0 l3-hw-offloading=no
/interface set sfp-sfpplus1 mtu=9000 l2mtu=9022
/interface set sfp-sfpplus2 mtu=9000 l2mtu=9022
/interface set sfp-sfpplus3 mtu=10000 l2mtu=10022
/interface/ethernet/switch set 0 l3-hw-offloading=yes

```

### 二层依赖

第 3 层硬件处理位于第 2 层硬件处理之上。 因此，L3HW 卸载需要在底层接口上进行 L2HW 卸载。 后者默认启用，但也有一些例外。 例如，CRS3xx 设备仅支持一个硬件网桥。 如果有多个网桥，其他的由CPU处理，不受L3HW约束。

另一个例子是 ACL 规则。 如果规则将流量重定向到 CPU 进行软件处理，则不会触发硬件路由 (L3HW)：

**用于禁用特定端口上的硬件处理的 ACL 规则**

`/interface/ethernet/switch/rule/add switch=switch1 ports=ether1 redirect-to-cpu=yes`

建议在 L2 配置期间关闭 L3HW 卸载。

为确保第3层在软件和硬件方面与第2层同步，建议在配置第2层功能时禁用 L3HW。 适用于以下配置：

- 添加/删除/启用/禁用网桥；
- 向网桥添加/删除交换机端口；
- 绑定交换机端口/移除绑定；
- 更改 VLAN 设置；
- 更改交换机端口上的 MTU/L2MTU；
- 更改以太网 (MAC) 地址。

简而言之，在 `/interface/bridge/ 和 /interface/vlan/` 下进行更改时禁用`l3-hw-offloading`：

**Layer 2 Configuration Template**

```shell
/interface/ethernet/switch set 0 l3-hw-offloading=no
 
/interface/bridge
# put bridge configuration changes here
 
/interface/vlan
# define/change VLAN interfaces
 
/interface/ethernet/switch set 0 l3-hw-offloading=yes

```

### MAC telnet 和 RoMON

在 **98DX8xxx**、**98DX4xxx** 或 **98DX325x** 交换机芯片上启用 L3HW 卸载时，MAC telnet 和 RoMON 存在限制。 来自这些协议的数据包将被丢弃并且不会到达 CPU，因此对设备的访问将失败。

如果需要 MAC telnet 或 RoMON 与 L3HW 结合使用，则可以创建某些 ACL 规则以强制这些数据包进入 CPU。

例如，如果需要在 sfp-sfpplus1 和 sfp-sfpplus2 上进行 MAC telnet 访问，则需要添加此 ACL 规则。 可以使用 `ports` 设置选择更多接口。

```shell
/interface ethernet switch rule
add dst-port=20561 ports=sfp-sfpplus1,sfp-sfpplus2 protocol=udp redirect-to-cpu=yes switch=switch1

```

例如，如果需要对 sfp-sfpplus2 进行 RoMON 访问，则需要添加此 ACL 规则。

```shell
/interface ethernet switch rule
add mac-protocol=0x88BF ports=sfp-sfpplus2 redirect-to-cpu=yes switch=switch1

```

### VLAN间路由

由于L3HW依赖于L2HW，而L2HW是做VLAN处理的，所以Inter-VLAN_hardware_routing需要底层有硬件桥接。 即使特定 VLAN 只有一个标记端口成员，后者也必须是网桥成员。 不要直接在交换机端口上分配 VLAN 接口！ 否则，L3HW 卸载失败，流量将由 CPU 处理：

`~/interface/vlan add interface=ether2 name=vlan20 vlan-id=20~`

而是将 VLAN 接口分配给网桥。 这样，VLAN 配置被卸载到硬件，并且在启用 L3HW 的情况下，流量受 VLAN 间硬件路由的影响。

**VLAN配置示例**

```shell
/interface/ethernet/switch set 0 l3-hw-offloading=no
/interface/bridge/port add bridge=bridge interface=ether2
/interface/bridge/vlan add bridge=bridge tagged=bridge,ether2 vlan-ids=20
/interface/vlan add interface=bridge name=vlan20 vlan-id=20
/ip/address add address=192.0.2.1/24 interface=vlan20
/interface/bridge set bridge vlan-filtering=yes
/interface/ethernet/switch set 0 l3-hw-offloading=yes

```

对于 VLAN 间路由，网桥接口必须是每个可路由的“/interface/bridge/vlan/”条目的标记成员。

### L3HW MAC 地址范围限制（仅限 DX2000/DX3000 系列）

Marvell Prestera DX2000 和 DX3000 交换芯片有一个硬件限制，即只允许为每个接口配置 MAC 地址的最后一个（最不重要的）八位字节。 其他五个（最重要的）八位字节是全局配置的，因此对于所有接口（交换机端口、网桥、VLAN）必须相等。 换句话说，MAC 地址必须采用 **XX:XX:XX:XX:XX:??** 格式，其中：

- **XX:XX:XX:XX:XX** 部分对所有接口都是通用的。
- **??** 是可变部分。

**此要求仅适用于第 3 层（路由）** ，第 2 层（桥接）不使用交换机的以太网地址。 此外，它不适用于网桥端口，因为它们使用网桥的 MAC 地址。

公共的五个八位字节的要求适用于：

- 启用硬件路由的独立交换机端口（不是网桥成员）（`l3-hw-offloading = yes`）。
- 网桥本身。
- VLAN 接口（默认使用网桥的 MAC 地址）。

## 路由配置

### 抑制硬件卸载

默认情况下，所有路由都参与成为硬件候选路由。 为了进一步微调要卸载的流量，每个路由都有一个选项可以禁用/启用 `suppress-hw-offload` 。

例如，如果知道大部分流量流向服务器所在的网络，可以只启用卸载到该特定目的地：

`/ip/route set [find where static && dst-address!="192.168.3.0/24"] suppress-hw-offload=yes`

现在只有到 192.168.3.0/24 的路由有 H-flag，表明它将是唯一有资格被选中进行 HW 卸载的路由：

```shell
[admin@MikroTik] > /ip/route print where static
Flags: A - ACTIVE; s - STATIC, y - COPY; H - HW-OFFLOADED
Columns: DST-ADDRESS, GATEWAY, DISTANCE
#     DST-ADDRESS       GATEWAY         D
0 As  0.0.0.0/0         172.16.2.1      1
1 As  10.0.0.0/8        10.155.121.254  1
2 AsH 192.168.3.0/24    172.16.2.1      1

```

H-flag并不表示该route实际上是HW offloaded，它只是表示route可以被选为HW offloaded。

### 路由过滤器

对于 OSFP 和 BGP 等动态路由协议，可以使用 [路由过滤器](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=74678285) 来抑制 HW 卸载。 例如，要抑制所有 OSFP 实例路由上的 HW 卸载，请使用 `suppress-hw-offload yes` 属性：

```shell
/routing/ospf/instance
set [find name=instance1] in-filter-chain=ospf-input
/routing/filter/rule
add chain="ospf-input" rule="set suppress-hw-offload yes; accept"

```

### 卸载 Fasttrack 连接

防火墙过滤规则具有 Fasttrack 的 `hw-offload` 选项，允许微调连接卸载。 由于 Fasttrack 连接的硬件内存非常有限，我们可以选择要卸载的连接类型，因此受益于接近线速的流量。 下一个示例仅卸载 TCP 连接，而 UDP 数据包通过 CPU 路由并且不占用 HW 内存：

```shell
/ip/firewall/filter
add action=fasttrack-connection chain=forward connection-state=established,related hw-offload=yes protocol=tcp
add action=fasttrack-connection chain=forward connection-state=established,related hw-offload=no
add action=accept chain=forward connection-state=established,related

```

### 无状态硬件防火墙

虽然连接跟踪和状态防火墙只能由 CPU 执行，但硬件可以通过 [交换规则 (ACL)](https://help.mikrotik.com/docs/display/ROS/CRS3xx%2C+CRS5xx%2C+CCR2116%2C+CCR2216+switch+chip+features#CRS3xx,CRS5xx,CCR2116,CCR2216switchchipfeatures-SwitchRules(ACL)) 执行无状态防火墙。 下一个示例阻止（在硬件级别）从 ether1 访问 MySQL 服务器，并重定向到来自 ether2 和 ether3 的 CPU/防火墙数据包：

````shell
/interface ethernet switch rule
add switch=switch1 dst-address=10.0.1.2/32 dst-port=3306 ports=ether1 new-dst-ports=""
add switch=switch1 dst-address=10.0.1.2/32 dst-port=3306 ports=ether2,ether3 redirect-to-cpu=yes

````

### 交换规则 (ACL) 与 Fasttrack 硬件卸载

一些防火墙规则可以通过 [交换规则 (ACL)](https://help.mikrotik.com/docs/display/ROS/CRS3xx%2C+CRS5xx%2C+CCR2116%2C+CCR2216+switch+chip+features#CRS3xx,CRS5xx,CCR2116,CCR2216switchchipfeatures-SwitchRules(ACL)) 和 CPU [防火墙过滤器](https://help.mikrotik.com/docs/display/ROS/Filter) + Fasttrack HW 卸载。 这两个选项都提供接近线速的性能。 问题是使用哪一个？

首先，[并非所有设备都支持 Fasttrack HW 卸载](https://help.mikrotik.com/docs/display/ROS/L3+Hardware+Offloading#L3HardwareOffloading-L3HWDeviceSupport)。 在没有硬件卸载的情况下，Firewall Filter 仅使用软件路由，这比对应的硬件路由要慢得多。 其次，即使 Fasttrack HW Offloading 是一个选项，经验法则是：

如果可以，就始终使用交换规则 (ACL)。

交換规则与 Fastrack 连接共享硬件内存。 但是，硬件资源是为每个 Fasttrack 连接分配的，而单个 ACL 规则可以匹配多个连接。 例如，如果你有一个连接到 sfp-sfpplus1 VLAN 10 的访客 WiFi 网络并且不希望它访问你的内部网络，只需创建一个 ACL 规则：

```shell
/interface/ethernet/switch/rule
add switch=switch1 ports=sfp-sfpplus1 vlan-id=10 dst-address=10.0.0.0/8 new-dst-ports=""

```

匹配的数据包将在硬件级别被丢弃。 这比让 _所有_ 客户数据包到 CPU 进行防火墙过滤要好得多。

当然，ACL 规则并不能匹配所有。 例如，ACL 规则无法过滤连接状态：接受已建立、丢弃其他。 这就是 Fasttrack HW Offloading 发挥作用的地方——默认情况下将数据包重定向到 CPU 以进行防火墙过滤，然后卸载已建立的 Fasttrack 连接。 但是，为整个交换机端口禁用 `l3-hw-offloading` 并不是唯一的选择。

使用 `**redirect-to-cpu=yes**` 定义 ACL 规则，而不是设置交换机端口的 `l3-hw-offloading=no` 以减少进入 CPU 的流量。

## 配置示例

### 上游端口在防火墙/NAT 后面的 VLAN 间路由

此示例演示了如何从接近线速的 VLAN 间路由中获益，同时保持防火墙和 NAT 在上游端口上运行。 此外，到上游端口的 Fasttrack 连接也被卸载到硬件，将流量速度提高到接近线速。 VLAN 间流量完全由硬件路由，不进入 CPU/防火墙，因此不占用 Fasttrack 连接的硬件内存。

使用具有以下设置的 **CRS317-1G-16S+** 模型：

- sfp1-sfp4 - 桥接端口，VLAN ID 20，未标记
- sfp5-sfp8 - 桥接端口，VLAN ID 30，未标记
- sfp16 - 上游端口
- ether1 - 管理端口

易于访问的设置端口列表：

**端口列表**

```shell
/interface list
add name=LAN
add name=WAN
add name=MGMT
 
/interface list member
add interface=sfp-sfpplus1 list=LAN
add interface=sfp-sfpplus2 list=LAN
add interface=sfp-sfpplus3 list=LAN
add interface=sfp-sfpplus4 list=LAN
add interface=sfp-sfpplus5 list=LAN
add interface=sfp-sfpplus6 list=LAN
add interface=sfp-sfpplus7 list=LAN
add interface=sfp-sfpplus8 list=LAN
add interface=sfp-sfpplus16 list=WAN
add interface=ether1 list=MGMT

```

**网桥设置**

```shell
/interface bridge
add name=bridge vlan-filtering=yes
 
/interface bridge port
add bridge=bridge interface=sfp-sfpplus1 pvid=20
add bridge=bridge interface=sfp-sfpplus2 pvid=20
add bridge=bridge interface=sfp-sfpplus3 pvid=20
add bridge=bridge interface=sfp-sfpplus4 pvid=20
add bridge=bridge interface=sfp-sfpplus5 pvid=30
add bridge=bridge interface=sfp-sfpplus6 pvid=30
add bridge=bridge interface=sfp-sfpplus7 pvid=30
add bridge=bridge interface=sfp-sfpplus8 pvid=30
 
/interface bridge vlan
add bridge=bridge tagged=bridge untagged=sfp-sfpplus1,sfp-sfpplus2,sfp-sfpplus3,sfp-sfpplus4 vlan-ids=20
add bridge=bridge tagged=bridge untagged=sfp-sfpplus5,sfp-sfpplus6,sfp-sfpplus7,sfp-sfpplus8 vlan-ids=30

```

路由需要专用的 VLAN 接口。 对于标准的 L2 VLAN 桥接（没有 VLAN 间路由），可以省略下一步。

**用于路由的 VLAN 接口设置**

```shell
/ip address
add address=192.168.88.1/24 interface=ether1
add address=10.0.0.17/24 interface=sfp-sfpplus16
 
/ip route
add gateway=10.0.0.1
 
/ip firewall filter
add action=fasttrack-connection chain=forward connection-state=established,related hw-offload=yes
add action=accept chain=forward connection-state=established,related
 
/ip firewall nat
add action=masquerade chain=srcnat out-interface-list=WAN

```

配置管理和上游端口、基本防火墙、NAT，并启用 Fasttrack 连接的硬件卸载：

**防火墙设置**

```shell
/ip address
add address=192.168.88.1/24 interface=ether1
add address=10.0.0.17/24 interface=sfp-sfpplus16
 
/ip route
add gateway=10.0.0.1
 
/ip firewall filter
add action=fasttrack-connection chain=forward connection-state=established,related hw-offload=yes
add action=accept chain=forward connection-state=established,related
 
/ip firewall nat
add action=masquerade chain=srcnat out-interface-list=WAN

```

此时，所有路由仍然由CPU执行。 在交换芯片上启用硬件路由：

**启用第 3 层硬件卸载**

```shell
# Enable full hardware routing on LAN ports
:foreach i in=[/interface/list/member/find where list=LAN] do={
    /interface/ethernet/switch/port set [/interface/list/member/get $i interface] l3-hw-offloading=yes
}
 
# Disable full hardware routing on WAN or Management ports
:foreach i in=[/interface/list/member/find where list=WAN or list=MGMT] do={
    /interface/ethernet/switch/port set [/interface/list/member/get $i interface] l3-hw-offloading=no
}
 
# Activate Layer 3 Hardware Offloading on the switch chip
/interface/ethernet/switch/set 0 l3-hw-offloading=yes

```

结果：

- 在同一 VLAN 内（例如 sfp1-sfp4），流量由第 2 层_(L2HW)_ 上的硬件转发。
- VLAN 间流量（例如 sfp1-sfp5）由第 3 层  _(L3HW)_ 上的硬件路由。
- 来自/到 WAN 端口的流量首先由 CPU/防火墙处理。 然后 Fasttrack 连接被卸载到硬件 _（硬件加速 L4 状态防火墙）。_NAT适用于CPU_ 和 HW 处理的数据包。
- 到管理端口的流量受防火墙保护。

## 典型的错误配置

以下是配置第 3 层硬件卸载的典型用户错误。

### 交换机端口上的 VLAN 接口

`/interface vlan add name=vlan10 vlan-id=10 interface=sfp-sfpplus1`

由于第 2 层依赖性，必须在网桥上设置 VLAN 接口。 否则，L3HW 将无法工作。 正确的配置是：

```shell
/interface bridge port add bridge=bridge1 interface=sfp-sfpplus1 pvid=10
/interface bridge vlan add bridge=bridge1 tagged=bridge1,sfp-sfpplus1 vlan-ids=10
/interface vlan add name=vlan10 vlan-id=10 interface=bridge1

```

### 不将网桥接口添加到/in/br/vlan

对于 VLAN 间路由，桥接接口本身需要添加到给定 VLAN 的标记成员中。 在下一个示例中，VLAN 间路由在 VLAN 10 和 11 之间工作，但数据包不会路由到 VLAN 20。

```shell
/interface bridge vlan
add bridge=bridge1 vlan-ids=10 tagged=bridge1,sfp-sfpplus1
add bridge=bridge1 vlan-ids=11 tagged=bridge1 untagged=sfp-sfpplus2,sfp-sfpplus3
add bridge=bridge1 vlan-ids=20 tagged=sfp-sfpplus1 untagged=sfp-sfpplus4,sfp-sfpplus5

```

上面的例子并不总是出错。 有时，你可能希望设备在某些或全部 VLAN 中充当简单的 L2 交换机。 只要确定你是故意这样设置，而不是因为错误。

### 创建多个网桥

这些设备仅支持一个硬件桥。 如果创建了多个网桥，则只有一个网桥获得硬件卸载。 对于 L2，这意味着其他网桥是软件转发，在 L3HW 的情况下，多个网桥可能会导致未定义的行为。

与其创建多个网桥，不如创建一个并使用 VLAN 过滤隔离 L2 网络。

### 使用不属于交换机的端口

有些设备有两个交换芯片或直接连接到 CPU 的管理端口。 例如，**CRS312-4C+8XG** 有一个 **ether9** 端口连接到单独的交换芯片。 尝试将此端口添加到网桥或将其包含在 L3HW 设置中会导致意外结果。 记得留下管理端口进行管理！

```shell
[admin@crs312] /interface/ethernet/switch> print
Columns: NAME, TYPE, L3-HW-OFFLOADING
# NAME     TYPE              L3-HW-OFFLOADING
0 switch1  Marvell-98DX8212  yes            
1 switch2  Atheros-8227      no   
            
[admin@crs312] /interface/ethernet/switch> port print
Columns: NAME, SWITCH, L3-HW-OFFLOADING, STORM-RATE
 # NAME         SWITCH   L3-HW-OFFLOADING  STORM-RATE
 0 ether9       switch2                             
 1 ether1       switch1  yes                      100
 2 ether2       switch1  yes                      100
 3 ether3       switch1  yes                      100
 4 ether4       switch1  yes                      100
 5 ether5       switch1  yes                      100
 6 ether6       switch1  yes                      100
 7 ether7       switch1  yes                      100
 8 ether8       switch1  yes                      100
 9 combo1       switch1  yes                      100
10 combo2       switch1  yes                      100
11 combo3       switch1  yes                      100
12 combo4       switch1  yes                      100
13 switch1-cpu  switch1                           100
14 switch2-cpu  switch2

```

### 过度依赖 Fasttrack HW 卸载

由于 Fasttrack HW Offloading 以零配置开销提供接近线速的性能，因此用户倾向于将其用作默认解决方案。 但是，HW Fasttrack 连接的数量非常有限，将其他流量留给 CPU。 尝试尽可能使用硬件路由，通过交换机 ACL 规则将 CPU 流量减少到最低，然后使用防火墙过滤规则微调要卸载的 Fasttrack 连接。

## L3HW 功能支持

- **HW** \- 支持该功能并将其卸载到硬件。
- **CPU** \- 该功能受支持但由软件 (CPU) 执行
- **N/A** \- 该功能不可与 L3HW 一起使用。 必须完全禁用第 3 层硬件卸载（**开关** `l3-hw-offloading=no`）才能使此功能正常工作。
- **FW** \- 对于给定的 **交换机端口**，该功能需要 `l3-hw-offloading``=no`。 在 **switch** 级别，`l3-hw-offloading=yes`。

| 特性                      | 支持       | 注释                                                                                                                                                                                                                                                                                        | 发布 |
| ------------------------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---- |
| IPv4 Unicast Routing      | **HW**     |                                                                                                                                                                                                                                                                                             | 7.1  |
| IPv6 Unicast Routing      | **HW**     | /interface/ethernet/switch/l3hw-settings/set ipv6-hw=yes                                                                                                                                                                                                                                    |
| 7.6                       |
| IPv4 Multicast Routing    | **CPU**    |                                                                                                                                                                                                                                                                                             |      |
| IPv6 Multicast Routing    | **CPU**    |                                                                                                                                                                                                                                                                                             |      |
| ECMP                      | **HW**     | Multipath outing                                                                                                                                                                                                                                                                            | 7.1  |
| Blackholes                | **HW**     | /ip/route add dst-address=10.0.99.0/24 blackhole                                                                                                                                                                                                                                            | 7.1  |
| gateway=<interface\_name> | **CPU/HW** | /ip/route add dst-address=10.0.0.0/24 gateway=ether1<br>这仅适用于直接连接的网络。 由于 HW 不知道如何发送 ARP 请求，CPU 发送 ARP 请求并等待回复以在连接的第一个接收到的与 DST IP 地址匹配的数据包上找出 DST MAC 地址。<br>DST MAC 确定后，添加HW 条目，所有进一步的数据包将由交换芯片处理。 | 7.1  |
| BRIDGE                    | **HW**     | [硬件卸载网桥](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-BridgeHardwareOffloading) 接口的 IP 路由。                                                                                                                                            | 7.1  |
| VLAN                      | **HW**     | 使用 [vlan-filtering](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-BridgeVLANFiltering) 在硬件卸载桥接口上创建的 VLAN 接口之间的路由。                                                                                                            | 7.1  |
| Bonding                   | **HW**     | /interface/bonding                                                                                                                                                                                                                                                                          | 7.1  |
| IPv4 Firewall             | **FW**     | 用户必须选择硬件加速路由或防火墙。<br>防火墙规则由 CPU 处理。 _**Fasttrack**_ 连接被卸载到 HW。                                                                                                                                                                                             | 7.1  |
| IPv4 NAT                  | **FW**     | 应用于卸载的 _**Fasttrack**_ 连接的 NAT 规则也由 HW 处理。                                                                                                                                                                                                                                  | 7.1  |
| MLAG                      | **N/A**    |                                                                                                                                                                                                                                                                                             |      |
| VRF                       | **N/A**    | 只有 **main** 路由表被卸载。                                                                                                                                                                                                                                                                |      |
| VRRP                      | **N/A**    |                                                                                                                                                                                                                                                                                             |      |
| VXLAN                     | **CPU**    |                                                                                                                                                                                                                                                                                             |      |
| MTU                       | **HW**     | 硬件最多支持 8 个 MTU 配置文件。                                                                                                                                                                                                                                                            | 7.1  |
| QinQ and tag-stacking     | **CPU**    | 堆叠 VLAN 接口将失去 HW 卸载，而直接在桥接口上创建的其他 VLAN 仍然可以使用 HW 卸载。                                                                                                                                                                                                        |      |

只有下表中列出的设备支持 L3 硬件卸载。

## L3HW 设备支持

只有下表中列出的设备支持 L3 硬件卸载。

### CRS3xx：交换机 DX3000 和 DX2000 系列

以下设备基于 **Marvell 98DX224S、98DX226S** 或 **98DX3236** 交换芯片型号。 这些设备不支持 Fasttrack 或 NAT 连接卸载。

**98DX3255** 和 **98DX3257** 型号是例外，它们具有 DX8000 而非 DX3000 系列的功能集。

| 型号                   | 交换芯片     | 发布版本 | IPv4 Route Prefixes<sup>1</sup> | IPv6 Route Prefixes<sup>2</sup> | Nexthops | ECMP paths per prefix<sup>3</sup> |
| ---------------------- | ------------ | -------- | ------------------------------- | ------------------------------- | -------- | --------------------------------- |
| **CRS305-1G-4S+**      | **98DX3236** | 7.1      | 13312                           | 3328                            | 4K       | 8                                 |
| **CRS310-1G-5S-4S+**   | **98DX226S** | 7.1      | 13312                           | 3328                            | 4K       | 8                                 |
| **CRS318-1Fi-15Fr-2S** | **98DX224S** | 7.1      | 13312                           | 3328                            | 4K       | 8                                 |
| **CRS318-16P-2S+**     | **98DX226S** | 7.1      | 13312                           | 3328                            | 4K       | 8                                 |
| **CRS326-24G-2S+**     | **98DX3236** | 7.1      | 13312                           | 3328                            | 4K       | 8                                 |
| **CRS328-24P-4S+**     | **98DX3236** | 7.1      | 13312                           | 3328                            | 4K       | 8                                 |
| **CRS328-4C-20S-4S+**  | **98DX3236** | 7.1      | 13312                           | 3328                            | 4K       | 8                                 |

<sup>1</sup> _由于可以卸载的路由总量有限，具有较高网络掩码的前缀优先由硬件转发（例如 /32、/30、/29 等），任何 其他不适合 HW 表的前缀将由 CPU 处理。 直接连接的主机被卸载为 /32 (IPv4) 或 /128 (IPv6) 路由前缀。 主机数量也受 [IP 设置](https://help.mikrotik.com/docs/display/ROS/IP+Settings#IPSettings-IPv4Settings) / [IPv6 设置](https://help.mikrotik.com/docs/display/ROS/IP+Settings#IPSettings-IPv6Settings) 限制。

<sup>2</sup> _IPv4 和 IPv6 路由表共享相同的硬件内存。_

<sup>3</sup> _如果路由的路径多于硬件 ECMP 限制 (X)，则只有前 X 条路径被卸载。_

### CRS3xx、CRS5xx：交换机 DX8000 和 DX4000 系列

以下设备基于 **Marvell 98DX8xxx、98DX4xxx** 交换芯片或 **98DX325x** 型号。

**Fasttrack** 连接 <sup>2,3,4</sup>  

| 型号                                     | 交换芯片                  | 发布版本 | IPv4 Routes <sup>1</sup> | IPv4 Hosts <sup>7</sup> | IPv6 Routes<sup>8</sup> | IPv6 Hosts<sup>7</sup> | Nexthops | **Fasttrack** **连接<sup>2,3,4</sup>** | NAT entries <sup>2,5</sup> |
| ---------------------------------------- | ------------------------- | -------- | ------------------------ | ----------------------- | ----------------------- | ---------------------- | -------- | -------------------------------------- | -------------------------- |
| **CRS317-1G-16S+**                       | **98DX8216**              | 7.1      | 120K - 240K              | 64K                     | 30K - 40K               | 32K                    | 8K       | 4.5K                                   | 4K                         |
| **CRS309-1G-8S+**                        | **98DX8208**              | 7.1      | 16K - 36K                | 16K                     | 4K - 6K                 | 8K                     | 8K       | 4.5K                                   | 3.9K                       |
| **CRS312-4C+8XG**                        | **98DX8212**              | 7.1      | 16K - 36K                | 16K                     | 4K - 6K                 | 8K                     | 8K       | 2.25K                                  | 2.25K                      |
| **CRS326-24S+2Q+**                       | **98DX8332**              | 7.1      | 16K - 36K                | 16K                     | 4K - 6K                 | 8K                     | 8K       | 2.25K                                  | 2.25K                      |
| **CRS354-48G-4S+2Q+, CRS354-48P-4S+2Q+** | **98DX3257 <sup>6</sup>** | 7.1      | 16K - 36K                | 16K                     | 4K - 6K                 | 8K                     | 8K       | 2.25K                                  | 2.25K                      |
| **CRS504-4XQ**                           | **98DX4310**              | 7.1      | 60K - 120K               | 64K                     | 15K - 20K               | 32K                    | 8K       | 4.5K                                   | 4K                         |
| **CRS518-16XS-2XQ**                      | **98DX8525**              | 7.3      | 60K - 120K               | 64K                     | 15K - 20K               | 32K                    | 8K       | 4.5K                                   | 4K                         |

<sup>1</sup> _取决于路由表的复杂性。 整个字节 IP 前缀（/8、/16、/24 等）比其他前缀（例如 /22）占用更少的硬件空间。 从 **RouterOS v7.3** 开始，当路由 HW 表变满时，只有具有较长子网前缀的路由（/30、/29、/28 等）会被卸载，而 CPU 会处理较短的前缀。 在 RouterOS v7.2 及之前的版本中，Routing HW 内存溢出导致了未定义的行为。 用户可以通过路由过滤器（对于动态路由）或抑制静态路由的硬件卸载来微调要卸载的路由。 IPv4 和 IPv6 路由表共享相同的硬件内存。_

<sup>2</sup> _当达到 Fasttrack 或 NAT 条目的 HW 限制时，其他连接将回退到 CPU。 MikroTik 的智能连接卸载算法确保流量最大的连接被卸载到硬件。_

<sup>3</sup> _Fasttrack 连接与 ACL 规则共享相同的硬件内存。 根据复杂程度，一条ACL规则可能会占用3-6个Fasttrack连接的内存。_

<sup>4</sup> _MPLS 与 Fasttrack 连接共享硬件内存。 此外，启用 MPLS 需要分配整个内存区域，否则可以存储多达 768 (0.75K) 个 Fasttrack 连接。 这同样适用于桥接端口扩展器。 但是，MPLS 和 BPE 可能使用相同的内存区域，因此同时启用它们不会使 Fasttrack 连接的限制加倍。_

<sup>5</sup> _如果 Fasttrack 连接需要网络地址转换，则会创建硬件 NAT 条目。 硬件同时支持SRCNAT和DSTNAT._

<sup>6</sup> _交换芯片具有 DX8000 系列的功能集。_

<sup>7</sup> _DX4000/DX8000交换芯片将直连主机、IPv4/32、IPv6/128路由条目存储在FDB表中，而不是路由表中。 HW 内存在常规 FDB L2 条目 (MAC)、IPv4 和 IPv6 地址之间共享。 主机数量也受 [IP 设置](https://help.mikrotik.com/docs/display/ROS/IP+Settings#IPSettings-IPv4Settings) / [IPv6 设置](https://help.mikrotik.com/docs/display/ROS/IP+Settings#IPSettings-IPv6Settings) 限制。

<sup>8</sup> _IPv4 和 IPv6 路由表共享相同的硬件内存。_

### CCR2000

| 型号                    | 交换芯片                  | 发布版本 | IPv4 Routes | IPv4 Hosts | IPv6 Routes | IPv6 Hosts | Nexthops | **Fasttrack连接** | NAT entries |
| ----------------------- | ------------------------- | -------- | ----------- | ---------- | ----------- | ---------- | -------- | ----------------- | ----------- |
| **CCR2116-12G-4S+**     | **98DX3255** <sup>1</sup> | 7.1      | 16K - 36K   | 16K        | 4K - 6K     | 8K         | 8K       | 2.25K             | 2.25K       |
| **CCR2216-1G-12XS-2XQ** | **98DX8525**              | 7.1      | 60K - 120K  | 64K        | 15K - 20K   | 32K        | 8k       | 4.5K              | 4K          |

<sup>1</sup> _交换芯片具有DX8000系列的特性集。_
