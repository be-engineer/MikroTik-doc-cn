# 生成树协议

___

生成树协议的目的是提供创建无环路第二层拓扑的能力，同时拥有冗余链接。在连接多个网桥或是交叉连接网桥端口时，有可能产生网络环路，严重影响网络的稳定性。生成树协议旨在通过引入根桥的概念来解决这个问题，二层的所有网桥将交换到根桥最短路径的信息。之后，每个网桥将协商使用哪些端口来到达根桥。这种信息交换是在网桥协议数据单元（BPDU）的帮助下完成的。STP将禁用每个网桥的某些端口，避免环路，同时仍然确保所有网桥能够相互通信。关于协议的深入描述，请参考802.1Q。

作为一个最佳实践，建议手动设置每个网桥的优先级、端口优先级和端口路径开销，以确保在任何时候都有正确的二层功能。对于由 1 到 2 个启用了 (R/M)STP 的网桥组成的网络来说，将 STP 的相关值保留为默认值是可以接受的，但对于更大的网络，强烈建议手动设置这些值。由于 STP 是通过检查网络上网桥的 STP 相关值来选择根桥和根端口的，如果将 STP 设置为自动，可能会选出一个不想要的根桥和根端口，在硬件故障的情况下，会导致网络无法访问。

## 监测

___

可以使用 `/interface bridge monitor` 命令来检查网桥的STP状态，例如：

```shell
/interface bridge monitor bridge
                  state: enabled
    current-mac-address: 64:D1:54:D9:27:E6
            root-bridge: yes
         root-bridge-id: 0x3000.64:D1:54:D9:27:E6
         root-path-cost: 0
              root-port: none
             port-count: 5
  designated-port-count: 5

```

注意，根桥没有任何根端口，只有指定端口。

可以使用 `/interface bridge port monitor` 命令来检查某个网桥端口的 STP 状态，例如：

```shell
/interface bridge port monitor 2
               interface: ether3
                  status: in-bridge
             port-number: 3
                    role: root-port
               edge-port: no
     edge-port-discovery: yes
     point-to-point-port: yes
            external-fdb: no
            sending-rstp: yes
                learning: yes
              forwarding: yes
          root-path-cost: 10
       designated-bridge: 0x3000.64:D1:54:D9:27:E6
         designated-cost: 0
  designated-port-number: 4
        hw-offload-group: switch1

```

注意，"根桥ID"由网桥优先级和网桥的MAC地址组成，对于非根桥，根桥将显示为 "指定桥"。在启用STP的网络中，一个端口可以有一个角色，下面是端口角色列表。

- **root-port** - 端口面向根桥，用于转发根桥的流量。
- **alternate-port** - 面向根桥的端口，但不用来转发流量（根桥的备份）。
- **backup-port** - 面向根桥的端口，但不转发流量（非根端口的备用端口）。
- **designated-port** -远离根桥的端口，将转发流量。
- **disabled-port** - 禁用或不活跃的端口。

当用 802.1Q 作为 EtherType 的网桥时，它们会向 01:80:C2:00:00:00 发送 BPDUs，这被 MSTP、RSTP 和 STP 使用。当使用802.1ad作为网桥VLAN协议时，BPDUs与802.1Q网桥不兼容，它们会被发送到01:80:C2:00:00:08。 如果整个二层网络有不同的网桥VLAN协议，(R/M)STP将不能正常工作。

## STP和RSTP

___

STP和Rapid STP在许多网络中广泛使用，但几乎所有的网络都只使用RSTP，因为它有很多好处。STP是一个非常古老的协议，它的收敛时间（完全了解网络拓扑结构变化并继续正确转发流量所需的时间）长达50秒。RSTP的收敛时间小很多，几秒甚至几毫秒。建议使用RSTP而不是STP，因为它的速度要快得多，而且还能向后兼容STP。RSTP更快的原因之一是减少了可能的端口状态，下面是STP端口状态列表：

- **Forwarding** - 端口参与流量转发，正在学习MAC地址，正在接收BPDU。
- **Listening** - 端口不参与流量转发，不学习MAC地址，正在接收BPDU。
- **Learning** - 端口不参与流量转发，但正在学习MAC地址。
- **Blocking**  - 端口被阻断，因为它造成环路，但正在接收BPDUs。
- **Disabled** - 端口被禁用或不活跃。

在RSTP中，禁用、监听和阻塞的端口状态被一个称为 **丢弃** 的状态所取代。

- **Forwarding** - 端口参与流量转发，正在学习MAC地址，正在接收BPDUs（forwarding=yes）。
- **Learning** - 端口不参与流量转发，但正在学习MAC地址（learning=yes）。
- **Discarding** - 端口不参与流量转发，不学习MAC地址，正在接收BPDUs（forwarding=no）。

在STP中，网桥之间的连接是由邻居网桥之间发送和接收BPDU决定的。指定的端口正在向根端口发送BPDU。如果连续3次没有收到BPDU的 **HelloTime**，那么连接被认为是不可用的，网络拓扑收敛将开始。在某些情况下，STP有可能通过减少 "转发延迟 "计时器来减少收敛时间，该计时器负责端口在学习/监听状态的时间。

在RouterOS中，可以指定哪些网桥端口是边缘端口。边缘端口是指不接收任何BPDU的端口，这很有好处，因为这允许STP跳过学习和监听状态，直接进入转发状态。这个功能有时被称为 **PortFast**，你可以把这个参数保留为默认值，也就是 **auto**，但也可以手动指定，可以为那些后面不应该有任何网桥的端口手动设置为边缘端口，通常这些端口是接入端口。

此外，桥接端口 `point-to-point` ，指定了一个桥接端口是否使用点对点链路连接到一个网桥，以便在发生故障时更快地收敛。将此属性设置为 `yes` 就等于强制为点对点链接，会跳过检查机制，即检测并等待来自该单一链接的其他设备的BPDU，将此属性设置为 `no` 就意味着一个链接可以接收来自多个设备的BPDU。通过将该属性设置为 "yes"，将大大改善（R/M）STP收敛时间。一般来说，只应该把这个属性设置为 "no"，如果一个链路之间有可能连接另一个设备，这主要和无线媒介和以太网集线器有关。如果以太网链路是全双工的，`auto` 会启用点对点功能。当协议模式设置为 "none"时，该属性没有影响。

### 默认值

在创建网桥或向网桥添加端口时， 以下是 RouterOS 分配的默认值。

- 默认的网桥优先级。 **32768** / **0x8000**
- 默认的网桥端口路径开销。 **10**
- 默认的网桥端口优先级。 **0x80**
- BPDU信息寿命增量。 **1**
- HelloTime。 **2**
- 默认最大报文寿命。 **20**

RouterOS不根据链路速度改变端口的路径开销，对于10M、100M、1000M和10000M的链路速度，当一个端口添加到网桥时，默认的路径开销值总是 **10**。BPDU的寿命由BPDU通过的网桥数乘以消息寿命决定，因为RouterOS使用 **1** 作为消息寿命的增量，那么BPDU数据包可以通过多少个网桥，就可以在 `max-message-age` 参数中指定。默认情况下，这个值被设置为 **20**，这意味着在第20个网桥之后，BPDU数据包将被丢弃，下一个网桥将成为根桥。注意，如果设置了 `max-message-age=20`，那么就很难预测哪些端口将成为第21个网桥的指定端口，可能导致流量无法正常转发。

如果使用网桥过滤规则，请确保允许带有 DST-MAC 地址 **01:80:C2:00:00:00** 的数据包，因为这些数据包携带 BPDU，对 STP 的正常工作至关重要。

### 选举过程

要在网络中正确配置 STP，需要了解选举过程，以及哪些参数以何种顺序参与。在RouterOS中，根桥会根据最小的优先级和最小的MAC地址以这种特定的顺序被选出。

1. 网桥优先级（最低）
2. 网桥MAC地址（最低）

在RouterOS中，根端口的选择是基于最低的根端口路径开销、最低的网桥标识符和最低的网桥端口ID，具体顺序如下。

1. 根端口的路径开销(最低)
2. 网桥标识符(最低)
3. 网桥端口ID（最低）

首先，当设备考虑选择哪个端口作为根端口时，它会检查其端口看到的 **根路径开销**。如果两个或多个端口的根路径开销相同，那么会检查 **上游** 设备的 **桥标识符**，与最低网桥标识符相连的端口将成为根端口。如果在两个或多个端口上看到相同的网桥标识符，那么将检查 **上游** 设备的 **网桥端口标识符**。

属性的说明。

根路径成本，所有网桥都有一个根路径开销。根桥的根路径开销为0，对于所有其他桥，它是到根桥的最小成本路径上的端口路径开销之和。可以在"/interface bridge port "下修改本地端口路径开销。

网桥标识符是 "网桥优先级 "和 "网桥MAC "的组合，可在"/interface bridge "下配置。

网桥端口 ID 是 "唯一 ID "和 "网桥端口优先级 "的组合，唯一 ID 在添加到网桥时自动分配给网桥端口，不能编辑。可以在 WinBox 的 "桥接端口""端口号 "栏下看到，或者用"/interface bridge port monitor"，作为 "端口号"。

确保在正确的端口上使用了路径开销和优先级。例如，对处于根桥中的端口设置路径开销是没有影响的，只有端口优先级对它们有影响。根路径开销对面向根桥的端口有影响，而端口优先级对远离根桥的端口有影响。网桥标识符并不影响设备自身的根端口选举，相反，它会影响下游设备的根端口选举。

在RouterOS中，可以为网桥优先级设置0到65535之间的任何数值，IEEE 802.1W标准规定，网桥优先级必须以4096为单位。这可能会导致不支持这种值的设备之间的不兼容问题。为了避免不兼容的问题，建议只使用这些优先级。0, 4096, 8192, 12288, 16384, 20480, 24576, 28672, 32768, 36864, 40960, 45056, 49152, 53248, 57344, 61440.

### 示例

#### 根路径开销示例

![](https://help.mikrotik.com/docs/download/attachments/21725254/RootPath.png?version=3&modificationDate=1585736384808&api=v2)

这个例子概述了根路径开销是如何工作的。由于SW1的优先级最低，为0x1000，因此它将成为根桥。每个网桥都会计算到根桥的路径开销。在计算根路径开销时，网桥会考虑到其端口上配置的路径开销 + 邻近网桥公布的根路径开销。 

**SW1**：由于它是根桥，它向邻居公布的根路径成本是0，尽管它的配置路径成本是10。 

**SW2:** **ether1** 的根路径开销为0+25= **25**。在 **ether2** 的路径开销将是10+10+10+0= **30**。

**SW3:** **ether2**，根路径开销为0+25= **25**。在 **ether4** 的路径开销将是10+5+25+0= **40**。

**SW4:** **ether1**, 根路径开销为0+25+5= **30**. 在 **ether4** 上的路径开销将是10+10+0= **20**。

路径成本最低的端口将被选为根端口。STP拓扑中的每个网桥都需要一条通往根桥的路径，在找到最佳路径后，多余的路径将被阻断，本例中是SW2和SW4之间的路径。

可以在根桥上配置路径开销，但只有在该桥失去根桥地位时才会被考虑。 

#### STP示例

![](https://help.mikrotik.com/docs/download/attachments/21725254/STPexample1.png?version=1&modificationDate=1585739167256&api=v2)

在这个例子中，要确保从ServerA到ServerB的连接有二层的冗余。如果一个端口连接到一个不是网桥且没有运行(R)STP的设备上，那么这个端口就被认为是一个边缘端口，在这个例子中，ServerA和ServerB被连接到一个边缘端口。这可以通过在网络中使用STP来实现。下面是每个交换机的配置例子。

- SW1的配置。

```shell
/interface bridge
add name=bridge priority=0x1000
/interface bridge port
add bridge=bridge interface=ether1 priority=0x60
add bridge=bridge interface=ether2 priority=0x50
add bridge=bridge interface=ether3 priority=0x40
add bridge=bridge interface=ether4 priority=0x30
add bridge=bridge interface=ether5

```

- SW2配置:

```shell
/interface bridge
add name=bridge priority=0x2000
/interface bridge port
add bridge=bridge interface=ether1
add bridge=bridge interface=ether2
add bridge=bridge interface=ether3

```

- SW3配置:

```shell
/interface bridge
add name=bridge priority=0x4000
/interface bridge port
add bridge=bridge interface=ether1
add bridge=bridge interface=ether2 path-cost=20
add bridge=bridge interface=ether3

```

- SW4配置:

```shell
/interface bridge
add name=bridge priority=0x4000
/interface bridge port
add bridge=bridge interface=ether1
add bridge=bridge interface=ether2 path-cost=20
add bridge=bridge interface=ether3

```

在这个例子中，**SW1** 是根桥，因为它有最低的网桥优先级。 **SW2** 和 **SW3** 的ether1,ether2连接到根桥，ether3连接到 **SW4**。当所有的交换机都正常工作时，流量将从服务器A通过SW1/ether2，通过SW2，通过SW4流向服务器B。在 **SW1** 故障的情况下，**SW2** 成为根桥，因为它的优先级次之，由图中虚线表示。下面是每个交换机的端口及其作用的列表。

- **root-port** - SW2_ether2, SW3_ether2, SW4_ether1
- **alternate-port** - SW2_ether1, SW3_ether1, SW4_ether2
- **designated-port** - SW1_ether1, SW1_ether2, SW1_ether3, SW1_ether4, SW1_ether5, SW2_ether3, SW2_ether3, SW4_ether3

**注意：** 根据802.1Q的建议，应该以4096为单位使用网桥优先级。要设置推荐的优先级，使用十六进制的符号更方便，例如，0是0x0000，4096是0x1000，8192是0x2000，以此类推（0...F）。

## 多重生成树协议

___

多重生成树协议(MSTP)用于网桥接口，确保多个VLAN之间的无环路拓扑，MSTP还可以提供二层的冗余，还可以作为VLAN的负载均衡技术，因为它有能力在不同的VLAN之间有不同的路径。MSTP的操作与(R)STP非常相似，(R)STP的许多概念可以应用于MSTP，强烈建议在使用MSTP之前了解(R)STP的原理，但在设计启用MSTP的网络时必须考虑到一些差异。

在使用 (R)STP 时，BPDUs 会在网桥的所有物理接口上发送，以确定是否有环路，并在造成环路的情况下阻止端口转发流量。如果在某个VLAN内有一个环路，(R)STP可能无法发现它。一些STP变种通过在每个VLAN上运行一个STP实例来解决这个问题（PVST），但这已被证明是低效的；一些STP变种通过在所有VLAN上运行一个STP实例来解决这个问题（CST），但它缺乏为每个VLAN或VLAN组做负载均衡的可能性。MSTP倾向于通过使用MST实例来解决这两个问题，MST实例可以定义一组VLAN（VLAN映射），用于负载均衡和冗余，这意味着每个VLAN组可以有一个不同的根桥和不同的路径。注意，将多个VLAN分组在一个实例中是有益的，可以减少每次网络拓扑变化的CPU周期量。

 在启用了 MSTP 的 RouterOS 中， 网桥优先级是 CIST 的根桥优先级， 按照 IEEE 802.1Q 标准， 网桥优先级必须以 4096 为单位， 最低的 12 位被忽略。这些是有效的网桥优先级。0, 4096, 8192, 12288, 16384, 20480, 24576, 28672, 32768, 36864, 40960, 45056, 49152, 53248, 57344, 61440. 当设置一个无效的网桥优先级时，RouterOS 会警告，并将该值转为有效值，但会在配置中保存原来的值，因为无效的网桥优先级仍然可以在运行 RouterOS 的设备之间用于 (R)STP，尽管建议使用有效的网桥优先级。

### MSTP区域

MSTP以区域为单位工作，每个区域都有一个区域根桥，区域之间也会有一个根桥。MSTP将使用内部生成树（IST）来构建区域内的网络拓扑结构，在区域外使用普通生成树（CST）来构建多个区域间的网络拓扑结构，MSTP将这两个协议合并为普通和内部生成树（CIST），它拥有区域内和区域间拓扑结构的信息。从CST的角度来看，一个区域似乎将作为一个单一的虚拟网桥，正因为如此，MSTP被认为对大型网络有很好的扩展性。为了使网桥处于同一区域，它们的配置必须匹配，BPDU不包括VLAN映射，因为它们可能很大，而是传输一个计算的哈希。如果一个网桥通过一个端口收到BPDU，而配置不匹配，那么MSTP将认为该端口是一个边界端口，它可以被用来到达其他区域。下面是需要匹配的参数列表，以便MSTP考虑来自同一区域的BPDU。

- 区域名称
- 区域修订
- VLAN 与 MST 实例 ID 的映射（计算的哈希）。

在没有区域的情况下，也可以创建启用了 MSTP 的网络，不过为了能够对每个 VLAN 组进行负载均衡，需要一个网桥从与之相连的网桥上接收 BPDU，其参数与上面提到的相同。在RouterOS中，默认的区域名称是空的，区域修订是0，这些都是有效的值，但必须确保它们是匹配的，以便在一个MSTP区域中获得多个网桥。如果一个区域的网桥分散在网络上，那这个区域就不可能存在，这些网桥必须至少以一种方式连接在一起，在这种情况下，它们可以发送和接收BPDU而不离开这个区域，例如，如果一个具有不同区域相关参数的网桥在两个具有相同区域相关参数的网桥之间，那么至少会存在3个不同的MSTP区域。

![](https://help.mikrotik.com/docs/download/attachments/21725254/MSTPtopology.png?version=1&modificationDate=1585743773949&api=v2)

在一个MSTP区域内运行每一个网桥的缺点是多余的CPU周期。相比之下，PVST(+)为网络上存在的每个VLAN ID创建一个生成树实例，由于网络中能存在的路径会非常有限，那么这种方法会有大量的开销和不必要的CPU周期，意味着这种方法的扩展性不是很好，会使CPU不强大的交换机过载。MSTP解决了这个问题，它将网络划分为MSTP区域，这个区域内的每个网桥将交换和处理存在于同一区域内的VLAN的信息，但会在后台运行单一的生成树协议实例来维护区域间的网络拓扑结构。这种方法已经证明更有效，而且更具有可扩展性，这意味着区域应该用于更大的网络，以减少CPU周期。

在区域中，可以定义 MST 实例，用于配置每个 VLAN 组的负载均衡和选举区域根桥。值得一提的是，在每个区域都有一个预定义的 MST 实例，在大多数文档中，它被称为 **MSTI0** 这个 MST 实例被认为是默认的 MST 实例，有一些参数适用于这个特殊的 MST 实例。当流量通过一个启用了MSTP的网桥时，MSTP会寻找一个有匹配的VLAN映射的MST实例，但如果某个VLAN ID不存在VLAN映射，那么流量将落在 **MSTI0**。

由于 MSTP 需要在网桥接口上启用 VLAN 过滤，那么请确保在 `/interface bridge vlan` 中允许所有需要的 VLAN ID，否则，流量将不会被转发，并且可能看起来是 MSTP 配置错误，尽管这是一个 VLAN 过滤的错误配置。

### 选举过程

MSTP的选举过程可以分为两个部分，即区域内和区域间。为了使MSTP正常工作，总是需要有一个区域根，即区域内的根桥，和一个CIST根，即区域间的根桥。区域根是区域内的根桥，区域根桥需要为区域内的VLAN组正确设置负载均衡。CIST 根将被用来配置哪些端口是备用/备份端口（非活动），哪些端口是根端口（活动）。

在区域之间，每个VLAN组没有负载均衡，MSTP区域之间的根端口选举过程和端口阻塞的方式与(R)STP相同。如果CIST封锁了一个MSTP区域内的端口，以防止MSTP区域之间的流量循环，那么这个端口仍然可以为IST激活，以便在MSTP区域内的每个VLAN组做负载均衡。

- 在MSTP区域内选举一个区域根桥或根端口时，需要用到以下参数：

| 特性                                                                                                       | 说明                                                                                                        |
| ---------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| **priority** (_integer: 0..65535 decimal format or 0x0000-0xffff hex format_; Default: **32768 / 0x8000**) | /interface bridge msti，MST实例优先级，用于在MSTP区域内选出区域根。                                         |
| **internal-path-cost** (_integer: 1..4294967295_; Default: **10**)                                         | /interface桥接端口，未知VLAN ID（MSTI0）的区域根的路径开销，用于MSTP区域内的根端口。                        |
| **priority** (_integer: 0..240_; Default: **128**)                                                         | /interface bridge port mst-override, 定义的 MST 实例的 MST 端口优先级，用于区域根桥上的桥口。               |
| **internal-path-cost** (_integer: 1..200000000_; Default: **10**)                                          | /interface bridge port mst-override, 定义的 MST 实例的 MST 端口路径开销，在 MSTP 区域内的非根桥端口上使用。 |
  
- 选举 CIST 根桥或 CIST 根端口时涉及以下参数：

| 特性                                                                                                       | 说明                                                                                  |
| ---------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| **priority** (_integer: 0..65535 decimal format or 0x0000-0xffff hex format_; Default: **32768 / 0x8000**) | /interface bridge，CIST网桥优先级，用于选举CIST根桥。                                 |
| **priority** (_integer: 0..240_; Default: **128**)                                                         | /interface bridge port, CIST port priority, 在CIST根桥上用于选举CIST根端口。          |
| **path-cost** (_integer: 1..4294967295_; Default: **10**)                                                  | /interface bridge port, CIST 端口路径开销, 用在CIST非根桥端口上，用于选举CIST根端口。 |

 MSTP检查选举根桥/端口的参数顺序与(R)STP相同，可以在(R)STP选举过程部分阅读更多信息。

### MST实例

**Sub-menu:** `/interface bridge msti`.

本节用于将多个 VLAN ID 分成一个实例，以便在 MSTP 区域内为每个 VLAN 组创建不同的根桥。

| 特性                                                                                                       | 说明                                                                                                                 |
| ---------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| **bridge** (_text_; Default: )                                                                             | 为其分配MST实例网桥。                                                                                                |
| **identifier** (_integer: 1..31_; Default: )                                                               | MST实例标识符。                                                                                                      |
| **priority** (_integer: 0..65535 decimal format or 0x0000-0xffff hex format_; Default: **32768 / 0x8000**) | MST实例优先级，用于确定MSTP区域内一组VLAN的根桥。                                                                    |
| **vlan-mapping** (_integer: 1..4094_; Default: )                                                           | 要分配给MST实例的VLAN ID的列表。此设置接受VLAN ID范围，以及逗号分隔的值。例如 `vlan-mapping=100-115,120,122,128-130` |

### MST 覆盖

**Sub-menu：** `/interface bridge port mst-override`。

本节用于为MSTP区域内的每个VLAN映射选择所需路径。

| 特性                                                                                       | 说明                                                                                      |
| ------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------- |
| **disabled** (_yes                                                \| no_; Default: **no**) | 入口是否被禁用。                                                                          |
| **internal-path-cost** (_integer: 1..200000000_; Default: **10**)                          | MST实例的VLAN映射的路径成本，用于面向根桥的VLAN上，以操纵路径选择，较低的路径成本是首选。 |
| **identifier** (_integer: 1..31_; Default: )                                               | MST实例标识符。                                                                           |
| **priority** (_integer: 0..240_; Default: **128**)                                         | MST实例的VLAN的优先级，用于远离根桥的VLAN上，以操纵路径选择，优先级越低越好。             |
| **interface** (_name_; Default: )                                                          | 使用配置的MST实例的VLAN映射和定义的路径成本和优先级的端口的名称。                         |

### 监控

与(R)STP类似，也可以监控MSTP状态。通过监控网桥接口本身，可以看到当前的 CIST 根桥和当前的 MSTI0 区域根桥，也可以看到 MST 实例标识符和 VLAN 映射的计算哈希值，这在确保某些网桥处于同一 MSTP 区域时很有用。下面是一个监控MSTP网桥的例子。

```shell
/interface bridge monitor bridge
                    state: enabled
      current-mac-address: 6C:3B:6B:7B:F0:AA
              root-bridge: no
           root-bridge-id: 0x1000.64:D1:54:24:23:72
  regional-root-bridge-id: 0x4000.6C:3B:6B:7B:F0:AA
           root-path-cost: 10
                root-port: ether4
               port-count: 5
    designated-port-count: 3
        mst-config-digest: 74edbeefdbf82cf63a70cf60e43a56f3

```

在MSTP中，可以对MST实例进行监控，这对于确定某个MST实例和VLAN组的当前区域根桥是很有用的，下面是一个监控MST实例的例子。

```shell
/interface bridge msti monitor 1
                    state: enabled
               identifier: 2
      current-mac-address: 6C:3B:6B:7B:F0:AA
              root-bridge: no
           root-bridge-id: 0.00:00:00:00:00:00
  regional-root-bridge-id: 0x1002.6C:3B:6B:7B:F9:08
           root-path-cost: 0
                root-port: ether2
               port-count: 5
    designated-port-count: 1

```

也可以监控某个MST覆盖条目，这对于在MSTP区域配置根端口和备用/后备端口时确定某个MST实例的端口角色很有用，下面是一个监控MST覆盖条目的例子。

```shell
/interface bridge port mst-override monitor 1
                      port: ether3
                    status: active
                identifier: 2
                      role: alternate-port
                  learning: no
                forwarding: no
   internal-root-path-cost: 15
         designated-bridge: 0x1002.6C:3B:6B:7B:F9:08
  designated-internal-cost: 0
    designated-port-number: 130

```

### MSTP例子

假设需要设计拓扑结构并配置MSTP，使VLAN 10,20在一个路径中转发，但VLAN 30,40在另一个路径中转发，而所有其他VLAN ID将在其中一个路径中转发。可以通过设置MST实例和分配端口路径开销来轻松实现，下面是一个网络拓扑结构，在3个独立的区域内对每个VLAN组进行负载均衡的例子。

![](https://help.mikrotik.com/docs/download/attachments/21725254/MSTPexample.png?version=3&modificationDate=1585822305765&api=v2) 
一个启用了MSTP的网络的拓扑结构，每个VLAN组的负载均衡。

首先将每个接口添加到一个网桥中，最初应该创建一个没有启用 VLAN 过滤的 (R)STP 网桥，这是为了防止失去对 CPU 的访问。这个例子中的每个设备都是由它所在的区域(Rx)和设备编号(\_x)命名的。对于较大的网络，由于链接和设备的数量，配置MSTP可能会很混乱，建议使用The Dude来监控和设计网络拓扑结构。

- 在 **R1_1**, **R1_3**, **R2_1**, **R2_3**, **R3_3** 上使用以下命令。

```shell
/interface bridge
add name=bridge protocol-mode=rstp vlan-filtering=no
/interface bridge port
add bridge=bridge interface=ether1
add bridge=bridge interface=ether2
add bridge=bridge interface=ether3
add bridge=bridge interface=ether4

```

- 在 **R1_2**、**R2_2**、**R3_2** 上使用以下命令：

```shell
/interface bridge
add name=bridge protocol-mode=rstp vlan-filtering=no
/interface bridge port
add bridge=bridge interface=ether1
add bridge=bridge interface=ether2

```

- 确保在这些设备上允许所需的VLAN ID，这里考虑每个设备将接收需要按VLAN组进行负载均衡的标记流量，在 **R1_1**, **R1_3**, **R2_1**, **R2_3**, **R3_3** 上使用这些命令。

```shell
/interface bridge vlan
add bridge=bridge tagged=ether1,ether2,ether3,ether4 vlan-ids=10,20,30,40

```
  
- 在 **R1_2**, **R2_2**, **R3_2** 上使用以下命令:

```shell
/interface bridge vlan
add bridge=bridge tagged=ether1,ether2 vlan-ids=10,20,30,40

```

 确保将所有需要的 VLAN ID 和端口添加到网桥 VLAN 表中，否则设备将无法转发所有需要的 VLAN，并且将失去对设备的访问。

要为每个需要在一个 MSTP 区域内的网桥指定一个区域名称，也可以指定区域的修订，但这是可选的，不过它们需要匹配。在这个例子中，如果所有网桥有相同的区域名称，那么它们都会在一个MSTP网桥中。在这个例子中，我们想把一组3个网桥分开在不同的MSTP区域中，做每个VLAN组的负载均衡，并创造多样性和可扩展性。

- 为每个网桥设置合适的区域名称（和区域修订），在每个设备上使用以下命令**修改区域名称！**。

```shell
/interface bridge
set bridge region-name=Rx region-revision=1

```

在创建了3个不同的MSTP区域后，需要确定哪个设备将成为每个VLAN组的区域根。为了保持一致性，要把每个区域的第一个设备（_1）设置为VLAN 10,20的区域根，把每个区域的第三个设备（_3）设置为VLAN 30,40的区域根。可以通过为每个 VLAN 组创建一个 MST 实例并为其分配网桥优先级来实现。MST实例的标识符只在 MSTP 区域内相关， 在 MSTP 区域外， 这些标识符可以是不同的， 并映射到不同的 VLAN 组。

- 在 **R1_1**, **R2_1**, **R3_1** 上使用以下命令。

```shell
/interface bridge msti
add bridge=bridge identifier=1 priority=0x1000 vlan-mapping=10,20
add bridge=bridge identifier=2 priority=0x3000 vlan-mapping=30,40

```

- 在 **R1_3**, **R2_3**, **R3_3** 上使用以下命令:

```shell
/interface bridge msti
add bridge=bridge identifier=1 priority=0x3000 vlan-mapping=10,20
add bridge=bridge identifier=2 priority=0x1000 vlan-mapping=30,40

```
  
- 在 **R1_2**, **R2_2**, **R3_2** 上使用以下命令:

```shell
/interface bridge msti
add bridge=bridge identifier=1 priority=0x2000 vlan-mapping=10,20
add bridge=bridge identifier=2 priority=0x2000 vlan-mapping=30,40

```

现在需要覆盖每个MST实例端口路径开销和端口优先级。可以通过为每个端口和每个MST实例添加一个MST-Override条目来完成。为了实现某一MST实例的流量路径不同，只需要确保端口的路径开销和优先级更大。可以增加端口路径开销，或者减少端口路径开销，使其面向区域根桥的端口。增加或减少数值并不重要，重要的是最后一个端口的路径开销要比另一个大。

- 在 **R1_1**, **R2_1**, **R3_1** 上使用以下命令:

```shell
/interface bridge port mst-override
add identifier=2 interface=ether1 internal-path-cost=5
add identifier=2 interface=ether2 internal-path-cost=15

```

- 在 **R1_2**, **R2_2**, **R3_2** 上使用以下命令:

```shell
/interface bridge port mst-override
add identifier=1 interface=ether1 internal-path-cost=5
add identifier=2 interface=ether2 internal-path-cost=9

```

- 在 **R1_3**, **R2_3**, **R3_3** 上使用以下命令:

```shell
/interface bridge port mst-override
add identifier=1 interface=ether2 internal-path-cost=5
add identifier=1 interface=ether3 internal-path-cost=9

```

对于VLAN 10,20从第一台设备到达第三台设备，它会在ether1和ether2之间选择，一个端口将被封锁并被设置为备用端口，ether1的路径开销为 `5+9=14`，ether2的路径开销为 `10`，ether2将被选为第三台设备上MSTI1的根端口。在VLAN 30,40从第三台设备到达第一台设备的情况下，ether1的路径开销为 `5+9=14`，ether2的路径开销为 `15`， ether1将被选为第三台设备上MSTI2的根端口。

现在可以为 **MSTI0** 配置根端口，其中将属于所有未分配给特定MST实例的VLAN，如在这个例子中，VLAN 10,20和VLAN 30,40。要配置这个特殊的 MST 实例，需要为网桥端口指定 `internal-path-cost`。这个值只与 MSTP 区域有关，在 MSTP 区域外没有任何影响。在这个例子中，选择所有未知的 VLAN 与 VLAN 30,40 在同一路径上转发，简单地增加其中一个端口的路径开销。

- 在 **R1_3**, **R2_3**, **R3_3** 上使用以下命令:

```shell
/interface bridge port
set [find where interface=ether3] internal-path-cost=25

```

至此，一个单一区域的MSTP可以认为是配置好的，一般来说，MSTP完全可以运行。强烈建议配置CIST部分，但为了测试的目的，可以保留默认值。在做任何测试之前，需要在所有网桥上启用MSTP。

- 在 **所有** 设备上使用以下命令：

```shell
/interface bridge
set bridge protocol-mode=mstp vlan-filtering=yes

```

当 MSTP 区域配置完成后，可以通过转发流量来检查它们是否配置正确，例如，从第一台设备向第三台设备发送带标签的流量，并改变标签流量的 VLAN ID，观察基于 VLAN ID 的不同路径。当这一切都按预期进行时，就可以继续配置 CIST 相关参数，选出 CIST 根桥和 CIST 根端口。为了保持一致性，选择第一个区域的第一台设备作为 CIST 根桥，为了确保故障时的一致性，给所有其他桥设置一个更高的优先级。

- 在 **R1_1** 上使用以下命令：

```shell
/interface bridge
set bridge priority=0x1000

```

- 在 **R1_2** 上使用以下命令:

```shell
/interface bridge
set bridge priority=0x2000

```

- ...

- 在 **R3_3** 上使用以下命令:

```shell
/interface bridge port
set [find where interface=ether2] path-cost=30
set [find where interface=ether3] path-cost=40
set [find where interface=ether4] path-cost=20

```

还需要在每个网桥上选出一个根端口，为了简单起见，选择离 **R1_1** 最近的端口作为根端口，并且跳数最少。这样选举根端口的程序与(R)STP的程序相同。

- 在 **R3_3** 上使用以下命令：

```shell
/interface bridge port
set [find where interface=ether2] path-cost=30
set [find where interface=ether3] path-cost=40
set [find where interface=ether4] path-cost=20

```

- 在 **R1_3** 和 **R2_3** 上使用下面的命令：

```shell
/interface bridge port
set [find where interface=ether2] path-cost=20
set [find where interface=ether3] path-cost=30

```

- 在 **R1_2** 上使用下面的命令:

```shell
/interface bridge port
set [find where interface=ether1] path-cost=30

```
