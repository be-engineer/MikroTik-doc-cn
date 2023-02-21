# 了解数据包流

更高级的防火墙设置或复杂的任务，如流量优先级、路由策略，要利用一个以上的RouterOS设施，需要相关知识。这些设施如何协同工作？什么时候发生，为什么？

RouterOS数据包流程图和流程实例将试图回答这些问题。

如果用一张图来表示数据包的情况会非常复杂，因此数据包流程图分为三个部分。

- 整体图。
- 详细的桥接、路由和MPLS流程图。
- 图中显示了在预路由、输入、转发、输出和后路由中包括哪些设施和顺序。

## 整体包流图

看一下整体图。开始看起来很复杂，但用例子看完图后，将变得更加清晰。

![](https://help.mikrotik.com/docs/download/attachments/328227/PacketFlowDiagram_v6_a.svg?version=1&modificationDate=1569859439358&api=v2)

在图的中央有4个方框。桥接、路由、Mpls决策和本地路由器进程。举例来说，如果数据包要通过路由器进行路由，数据包的流程如下图所示。在不深入了解每个设施的情况下，数据包进入in-interface，路由器确定它是IP流量，需要进行路由，数据包经过所有的路由过程，从out-interface出来。

![](https://help.mikrotik.com/docs/download/attachments/328227/01c_Routing_concept.png?version=1&modificationDate=1569859502606&api=v2)

让我们看一下另一个例子，说明如果数据包的目的地是路由器会发生什么。例如，in-interface收到ICMP（ping）数据包，它的目的地是路由器本身，所以数据包将进行 _local-in_ 处理。数据包处理后，ICMP（ping）回复在路由器内部产生 _local-out_ 处理，并通过out-interface发送出去。

![](https://help.mikrotik.com/docs/download/attachments/328227/01d_Communication_with_router.png?version=1&modificationDate=1570627553904&api=v2)

在进一步举例说明之前，先对每个盒子进行简单解释：

- **physical in-interface** - 路由器收到的数据包的起始点。
- **logical in-interface** - 解封后的数据包的起点（来自隧道、IPsec等）。
- **local in** - 以路由器本身为目的地的数据包的最后一点。
- **interface HTB (Hierarchical Token Bucket)** - 接口队列。
- **physical out-interface** - 数据包在实际发送前的最后一点。
- **logical out-interface** - 数据包在封装前的最后一点（到隧道、IPsec等）。
- **local out** - 路由器产生的数据包的起点。

现在深入研究桥接、MPLS和路由流内部发生了什么。

![](https://help.mikrotik.com/docs/download/attachments/328227/PacketFlowDiagram_v6_b.svg?version=1&modificationDate=1570627617915&api=v2)

在进一步举例说明之前，先对每个盒子进行简单的解释:

- **routing decision** - 通过路由表中的路由，找到与数据包的目标IP地址相匹配的路由。匹配时数据包将进一步处理，如果没有匹配，数据包将丢弃。
- **mpls decision** - 根据MPLS转发表对数据包进行处理。
- **bridging decision** - 桥接通过MAC地址表来寻找数据包的目的MAC地址的匹配。匹配时数据包将进一步处理，如果没有匹配，会创建数据包的多个副本，数据包将被泛滥（通过所有网桥端口发送出去）。一个数据包的副本也会到达网桥输入链，因为网桥接口本身就是众多目的地之一。当使用 `vlan-filtering=yes` 时，由于 "/interface bridge vlan" 表不允许的数据包，将在这个阶段被丢弃。
- **use-ip-firewall** - 在网桥设置中是否启用了 _use-ip-firewall_ 选项。
- **ipsec-policy** - 数据包是否符合任何配置的 IPsec 策略。

### 链

RouterOS由一些默认的链组成。这些链允许在不同点上过滤数据包。

- **PREROUTING** 链。这个链中的规则适用于刚刚到达网络接口的数据包。这条链存在于 _nat_ 、_mangle_ 和 _raw_ 表中。
- **INPUT** 链。这个链中的规则适用于刚刚被交给本地进程的数据包。这条链存在于 _mangle_ 和 _filter_ 表中。
- **OUTPUT** 链。这里的规则适用于刚刚由进程产生的数据包。这个链存在于 _raw_ , _mangle_ , _nat_ 和 _filter_ 表中。
- **FORWARD** 链。这里的规则适用于任何通过当前主机路由的数据包。这个链只存在于 _mangle_ 和 _filter_ 表中。
- **POSTROUTING** 链。这个链中的规则适用于刚刚离开网络接口的数据包。这条链存在于 _nat_ 和 _mangle_ 表中。

每个预路由、输入、转发、输出和后路由块都包含更多的设施，这些设施在数据包流程图的第三部分进行了说明:

![](https://help.mikrotik.com/docs/download/attachments/328227/Pfd.png?version=1&modificationDate=1570627732451&api=v2)

在进一步举例说明之前，先简单解释一下每个方框:

- **Hotspot-in** - 允许捕获被连接跟踪丢弃的流量 - 这样热点功能就能够提供连接，即使网络设置是一个不完整的块。
- **RAW Prerouting** - RAW表预路由链。
- **Connection tracking** - 数据包由连接跟踪处理。
- **Mangle Prerouting** - Mangle prerouting链。
- **Mangle Input** - Mangle输入链。
- **Filter Input** - 防火墙过滤器输入链。
- **HTB Global** - 队列树。
- **Simple Queues** - 是一个用于限制特定目标流量的功能。
- **TTL** - 表示路由数据包的生存时间（TTL）减少1的确切位置，如果TTL变为0，数据包将被丢弃。
- **Mangle Forward** - Mangle转发链。
- **Filter Forward** - 过滤转发链。
- **Accounting** - 认证、授权和审计功能处理。
- **RAW Output** - RAW表输出链。
- **Mangle Output** - Mangle输出链。
- **Filter Output** - 防火墙过滤器输出链。
- **Routing Adjustment** - 这是一个变通方法，可以在Mangle链输出中设置策略路由（路由标记）。
- **Mangle postrouting** - Mangle postrouting链。
- **Src Nat** - 网络地址转换srcnat链。
- **Dst Nat** - 网络地址转换dstnat链。
- **Hotspot-out** - 撤销Hotspot-in对返回客户端的数据包的所有操作。

## 路由数据包的流程

### 转发

现在来看看第一个例子，数据包在路由器上路由，以便深入了解数据包的去向。

数据包进入in-interface，路由器确定它是一个IP数据包，需要路由，这里开始了复杂的过程：

1. 数据包进入预路由处理。
   1. 检查是否有热点，并修改数据包用于热点
   2. 通过RAW预路由链处理数据包。
   3. 通过连接跟踪发送数据包。
   4. 通过Mangle预路由链处理数据包。
   5. 通过NAT dst-nat链处理数据包。
2. 通过路由表运行数据包，做出路由决定。
3. 数据包进入转发过程。
   1. 检查TTL值。
   2. 通过Mangle转发链处理数据包。
   3. 通过过滤器转发链处理数据包。
   4. 将数据包发送到审计流程。 
4. 一个数据包进入后路由过程。
   1. 通过Mangle后路由链处理数据包。
   2. 通过NAT src-nat链处理数据包。
   3. 如果有热点，撤消在热点进入中所作的任何修改。
   4. 通过队列树（HTB Global）处理数据包。
   5. 通过简单队列处理数据包。 
5. 检查是否有IPsec，然后通过IPsec策略进行处理。

![](https://help.mikrotik.com/docs/download/attachments/328227/02a_routing_forward.png?version=1&modificationDate=1570627796980&api=v2)

![](https://help.mikrotik.com/docs/download/attachments/328227/02a_routing_forward_chains.png?version=1&modificationDate=1570627984173&api=v2)

### 输入

前面已经知道，数据包进入接口，路由器判断它是一个IP数据包，需要进行路由，开始了复杂的过程：

1. 当数据包的目的地是路由器时，会发生一个非常类似的过程（路由输入）。数据包进入预路由处理。
    1. 检查是否有热点，并修改数据包用于热点。
    2. 通过RAW预路由链处理数据包。
    3. 通过连接跟踪发送数据包。
    4. 通过Mangle预路由链处理数据包。
    5. 通过NAT dst-nat链处理数据包。 
2. 通过路由表运行数据包，做出路由决定。 
3. 一个数据包进入输入过程。
    1. 通过Mangle输入链处理数据包。
    2. 通过过滤器输入链处理数据包。
    3. 通过队列树（HTB Global）处理数据包。
    4. 通过简单队列处理数据包。 
4. 检查是否有IPsec，然后通过IPsec策略进行处理。

![](https://help.mikrotik.com/docs/download/attachments/328227/02b_routing_input.png?version=1&modificationDate=1570628270223&api=v2)

![](https://help.mikrotik.com/docs/download/attachments/328227/02b_routing_input_chains.png?version=1&modificationDate=1570628305887&api=v2)

### 输出

当数据包从路由器发起时（路由输出）：

1. 数据包是由路由器本身发出的
    1. 数据包经过路由表，做出路由决定  
2. 数据包进入输出过程
    1. 通过桥接决策处理数据包。
    2. 通过连接跟踪发送数据包。
    3. 通过Mangle输出链处理数据包。
    4. 通过过滤器输出链处理数据包。
    5. 将数据包发送到路由调整（策略路由）。 
3. 数据包进入后路由过程。
    1. 通过Mangle后路由链处理数据包。
    2. 通过NAT src-nat链处理数据包。
    3. 如果有一个热点，撤销在热点进入中的任何修改。
    4. 通过队列树（HTB Global）处理数据包。
    5. 通过简单的队列处理数据包。 
4. 检查是否有IPsec，然后通过IPsec策略进行处理。

![](https://help.mikrotik.com/docs/download/attachments/328227/02c_routing_output.png?version=1&modificationDate=1570628337574&api=v2)![](https://help.mikrotik.com/docs/download/attachments/328227/02c_routing_output_chains.png?version=1&modificationDate=1570628357260&api=v2)

## 桥接数据包流

下面讨论的是RouterOS中的一般桥接过程。大多数数据包将遵循相同的处理路径，但在某些配置中（例如，启用了VLAN过滤、horizon、STP、DHCP或IGMP嗅探），有些数据包处理会不同。请访问桥接手册了解更多信息。

### ![](https://help.mikrotik.com/docs/download/attachments/328227/01a_bridging_concept.png?version=1&modificationDate=1570629397406&api=v2)

### 桥接转发

桥接转发是指数据包从一个桥接端口转发到另一个桥接端口时发生的过程，本质上是连接同一网络上的多个设备。设备在接收到内接口的数据包后，确定内接口是一个桥接端口，通过桥接过程。

1. 数据包经过桥接NAT dst-nat链，MAC目的地和优先级可以改变，除此之外，数据包可以简单地接受、丢弃或标记。
2. 检查网桥设置中是否启用了use-ip-firewall选项。
3. 通过网桥主机表运行数据包，做出转发决定。最终被泛滥的数据包(如广播、组播、未知单播流量)会在每个网桥端口加倍，然后在网桥转发链中进一步处理。当使用 "vlan-filtering=yes "时，由于"/interface bridge vlan"表不允许的数据包，将在这个阶段丢弃。
4. 数据包会经过网桥过滤转发链，在这里可以改变优先级，也可以简单地接受、丢弃或标记数据包。
5. 检查网桥设置中是否启用了 use-ip-firewall 选项。
6. 数据包经过网桥NAT src-nat链，其中MAC源和优先级可以改变，除此之外，数据包可以被简单接受、丢弃或标记。
7. 检查网桥设置中是否启用了 use-ip-firewall 选项。

![](https://help.mikrotik.com/docs/download/attachments/328227/04c_bridging_forward1.png?version=1&modificationDate=1570629442285&api=v2)

**适用于RouterOS v6：**  

当网桥 "vlan-filtering "启用时，收到的无标记数据包可能会在 "DST-NAT"块之前封装到VLAN头，意味着这些数据包可以用 "mac-protocol=vlan"和 "vlan-encap"设置来过滤。如果出站接口的 "frame-types"设置为 "admit-all"或 "admit-only-untagged and-priority-tagged"，封装就会发生。

标记的数据包可能在"桥接决定"块上被解封，这意味着这些数据包将不再符合 `mac-protocol=vlan` 和 `vlan-encap` 设置。如果数据包的VLAN ID与出站端口的无标记VLAN成员相匹配，就会发生解封装。 
  
**适用于RouterOS v7和更新版本：**

当网桥 `vlan-filtering` 启用时，收到的无标记数据包可能被封装到 "BRIDGING-DECISION "块的VLAN头中，这意味着这些数据包可以使用 `mac-protocol=vlan` 和 `vlan-encap` 设置进行过滤。 如果出站接口的 "frame-types"设置为 "admit-all"或 "admit-only-untagged and-priority-tagged"，就会发生封装。

标记的数据包可能在 "BRIDGING DECISION"块上解封装，意味着这些数据包不再符合 `mac-protocol=vlan` 和 `vlan-encap` 设置。如果数据包的VLAN ID与出站端口的无标记VLAN成员相匹配，就会发生解封装。

### 网桥输入

网桥输入是当数据包以网桥接口为目的地时发生的一个过程。最常见的情况是，当你需要到达在网桥接口上运行的某些服务 (例如 DHCP 服务器) 或需要将流量路由到其他网络时，就会发生这种情况。最开始的步骤与桥接转发过程类似-接收到in-interface上的数据包后，设备确定in-interface是一个桥接端口，传递到桥接过程。

1. 数据包经过网桥NAT dst-nat链，其中MAC目的地和优先级可以改变，除此之外，数据包可以被简单地接受、丢弃或标记。
2. 检查网桥设置中是否启用了use-ip-firewall 选项。
3. 通过网桥主机表运行数据包，做出转发决定。目标 MAC 地址与网桥 MAC 地址匹配的数据包传递到网桥输入链。最终泛滥的数据包 (如广播、组播、未知单播流量)也会到达网桥输入链，因为网桥接口本身就是众多目的地之一。
4. 数据包经过网桥过滤器输入链，在那里可以改变优先级，或者简单地接受、丢弃或标记数据包。

![](https://help.mikrotik.com/docs/download/attachments/328227/04b_bridging_input.png?version=1&modificationDate=1570629442007&api=v2)

### 网桥输出

网桥输出是当数据包通过一个或多个桥接端口离开设备时发生的过程。最常见的情况是，当一个网桥接口本身试图连接到某个网桥端口的设备时（例如，运行在网桥接口上的 DHCP 服务器响应一个 DHCP 客户端时）。当数据包在其他更高级别的 RouterOS 进程中被处理，并且设备最终确定输出接口是一个网桥时，数据包就会通过网桥进程：

1. 通过桥接主机表运行数据包，做出转发决定。最终泛滥的数据包（如广播、多播、未知单播流量）会乘以网桥端口，然后在网桥输出链中进一步处理。
2. 数据包经过网桥过滤输出链，优先级可以改变，或者数据包可以简单地接受、丢弃或标记。
3. 数据包经过网桥NAT src-nat链，其中MAC源和优先级可以改变，除此之外，数据包可以简单地接受、丢弃或标记。
4. 检查网桥设置中是否启用了use-ip-firewall 选项。

![](https://help.mikrotik.com/docs/download/attachments/328227/04a_bridging_output.png?version=1&modificationDate=1570629441843&api=v2)

### 启用了防火墙的转发

在某些网络配置中，可能要在路由链上对桥接流量进行额外的处理，例如，使用简单队列或 IP 防火墙。可以在桥接设置下启用use-ip-firewall时进行。注意，额外的处理将消耗更多的 CPU 资源来处理这些数据包。所有的步骤已经在前面讨论过了，下面是一个回顾：

1. 数据包通过网桥的 NAT dst-nat 链。
2. 启用use-ip-firewall选项后，数据包将在预路由链中进一步处理。
3. 数据包进入预路由处理。
4. 通过网桥主机表运行数据包，做出转发决定。
5. 数据包经过网桥过滤器转发链。
6. 如果启用use-ip-firewall选项，数据包将在路由转发链中进一步处理。
7. 数据包进入路由转发处理。
8. 数据包通过桥接NAT src-nat链。
9. 如果启用use-ip-firewall选项，数据包将在后路由链中进一步处理。
10. 数据包进入预路由处理。

![](https://help.mikrotik.com/docs/download/attachments/328227/04d_bridging_forward_with_use_ip_firewall.png?version=1&modificationDate=1570629442425&api=v2)![](https://help.mikrotik.com/docs/download/attachments/328227/04d_bridging_forward_with_use_ip_firewall_chains.png?version=1&modificationDate=1570629442561&api=v2)

## 硬件卸载数据包的流程

在上一个话题中，只讨论了软件桥接，需要主要的CPU处理来通过正确的桥接端口转发数据包。大多数MikroTik设备都配备了专用的交换硬件，即所谓的交换芯片或交换ASIC。可以将一些桥接功能，如桥接端口之间的数据包转发或数据包过滤，卸载到这个专门的硬件芯片上，而不消耗任何CPU资源。在RouterOS中将这个功能命名为桥接硬件（HW）卸载。不同的MikroTik设备可能有不同的交换芯片，每个芯片都有不同的可用功能，所以一定要看这篇文章获得更多的细节-[桥接硬件卸载](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-BridgeHardwareOffloading)。

![](https://help.mikrotik.com/docs/download/attachments/328227/Switch_packetFlow_example1.png?version=2&modificationDate=1591601254209&api=v2)

当输出接口被硬件卸载且网桥快速路径未激活时，接口HTB将无法正常工作。

![](https://help.mikrotik.com/docs/download/attachments/328227/Detailed_switch_flow_redArrows.png?version=1&modificationDate=1591601275958&api=v2)

- **switching decision** - 取决于交换机的型号。该块控制所有与交换有关的任务，如主机学习、数据包转发、过滤、速率限制、VLAN标记/untagging、镜像等。某些交换机的配置可以改变数据包的流向。
- **switch-cpu port** - 一个特殊用途的交换机端口，用于主CPU和其他交换机端口之间的通信。注意，除了交换机菜单，switch-cpu端口不会出现在RouterOS的任何地方，任何与软件有关的配置（如接口列表）都不能用到这个端口。到达CPU的数据包会自动与物理内接口关联。

然而，硬件卸载并不限制设备只有硬件的有限功能，而是可以同时利用硬件和软件处理的优势。这需要深刻理解数据包如何通过交换芯片，以及它们究竟何时被传递到主CPU。

### 交换机转发

将进一步讨论当网桥硬件卸载启用，数据包在单个交换芯片上的两个交换端口之间转发时的数据流。这是最常见的，也是最简单的例子。

1. 交换机检查in-interface是否是一个硬件卸载接口。
2. 通过交换机主机表运行数据包，做出转发决定。如果交换机发现目标MAC地址匹配，数据包就会通过物理接口发出去。最终被泛滥的数据包（如广播、组播、未知的单播流量）会倍增并发送至每个硬件卸载的交换机端口。

![](https://help.mikrotik.com/docs/download/attachments/328227/Detailed_switch_flow_redArrowsv1.png?version=1&modificationDate=1591601309910&api=v2)

### 交换到CPU输入

这个过程发生在物理接口接收数据包时，它被指定到switch-cpu端口进行进一步的软件处理。有两条通往交换机CPU的路径。一条不使用硬件卸载和交换（例如，用于路由的独立接口或桥接接口，但故意禁用硬件卸载），所以数据包只是进一步传递给软件处理。当硬件卸载在接口上激活时，就会采取另一条路径。这导致数据包通过交换决定，有各种原因导致交换机可能将数据包转发到交换机cpu端口。

- 数据包的目标MAC地址与本地MAC地址相匹配，例如，当数据包的目的地是本地网桥接口时。
- 数据包可能被泛滥到所有的交换机端口，包括交换机的CPU端口，例如收到广播、多播或未知的单播流量时。
- 交换机可能已经了解到一些主机只能通过CPU到达（交换机-CPU端口学习将在下一节讨论），例如，当一个网桥包含HW和非HW卸载接口时，如无线、EoIP甚至以太网接口。
- 一个数据包被故意复制到交换机-cpu上，例如数据包检查。
- 数据包是由交换机配置触发的，应该在软件中处理，例如DHCP或IGMP嗅探。

请看一个in-interface被硬件卸载时的数据包演练：

1. 交换机检查in-interface是否是硬件卸载的接口。
2. 通过交换机主机表运行数据包做出转发决定。如果上述结果为真，数据包就会被转发到交换机cpu端口。
3. 数据包通过交换机-cpu端口流出，会被RouterOS数据包流进一步处理。

![](https://help.mikrotik.com/docs/download/attachments/328227/Detailed_switch_flow_redArrowsv2.png?version=1&modificationDate=1591601576823&api=v2)

任何被交换机芯片泛滥的接收数据包都不会被软件网桥再次泛滥到同一个HW卸载的交换机组。防止重复数据包的形成。

### CPU输出到交换机

这个过程发生在数据包离开RouterOS软件处理并在交换机cpu端口上被接收时。同样，数据包有两条路径可供选择。一条不使用硬件卸载和交换（例如，用于路由的独立接口或桥接接口，但故意禁用硬件卸载），所以数据包只是通过物理输出接口发出去。当硬件卸载在输出接口上激活时，就会用另一种途径。会导致数据包通过交换决定。就像其他交换机端口一样，交换机将从交换机-cpu端口上收到的数据包中了解源MAC地址。如果网桥包含HW和非HW的卸载接口时确实很有用，交换机可以了解哪些帧应该被转发到CPU。请看一个输出接口是硬件卸载时的数据包演练：

1. 退出RouterOS软件处理的数据包在交换机-cpu端口上被接收。
2. 交换机检查out-interface是否是硬件卸载的接口。
3. 通过交换机主机表运行数据包，做出转发决定。如果交换机发现目标MAC地址的匹配，数据包就会通过物理接口发送出去。最终被泛滥的数据包（如广播、组播、未知的单播流量）会倍增并发送至每个硬件卸载的交换机端口。

![](https://help.mikrotik.com/docs/download/attachments/328227/Detailed_switch_flow_redArrowsv3.png?version=1&modificationDate=1591601660656&api=v2)

通过HW卸载接口发送泛滥数据包的软件网桥只在每个HW卸载的交换机组而不是每个HW卸载的接口上发送一个数据包副本。实际的泛滥将由交换机芯片完成，防止形成重复的数据包。

## MPLS数据包的流程

![](https://help.mikrotik.com/docs/download/attachments/328227/01b_mpls_concept.png?version=1&modificationDate=1570629350781&api=v2)

### Pop标签

![](https://help.mikrotik.com/docs/download/attachments/328227/03_mpls_input.png?version=1&modificationDate=1570629230741&api=v2)

### 交换标签

![](https://help.mikrotik.com/docs/download/attachments/328227/03_mpls_forward.png?version=1&modificationDate=1570629224054&api=v2)

### Push标签

![](https://help.mikrotik.com/docs/download/attachments/328227/03_mpls_output.png?version=1&modificationDate=1570629234391&api=v2)

## 逻辑接口

这里演示了输入或输出接口是实际的物理接口（以太网、无线）时的例子，如果路由器收到隧道封装的数据包，数据包将如何流动？

![](https://help.mikrotik.com/docs/download/attachments/328227/01e_encapsulate_decapsulate.png?version=1&modificationDate=1570629109801&api=v2)

假设有IPIP数据包进入路由器。它是一个普通的IPv4数据包，将通过所有与路由有关的设施进行处理（直到图中的 "J"）。然后路由器将查看该数据包是否需要解封装，这种情况下，它是一个IPIP数据包，所以"要"把该数据包发送到解封装。之后，数据包通过所有设施进行另一个循环，但这次作为一个解封装的IPv4数据包。

这一点非常重要，因为数据包实际上要经过两次防火墙，所以如果有一个严格的防火墙，那么对于IPIP封装的数据包和解封装的IP数据包都应该有 "接受 "规则。

启用了"vlan-filtering "的网桥进行数据包封装和解封装，与逻辑接口无关。参见桥接部分更多细节。

IPSec策略

看一下另一种隧道类型-IPSec。这种类型的VPN没有逻辑接口，但其处理方式类似。

数据包通过IPSec策略处理而不是逻辑接口。在路由决策（2）和输入防火墙处理（3）之后，路由器试图将源和目的地与IPsec策略相匹配。当策略与数据包相匹配时，它被发送到解密（5）。解密后的数据包再次进入PREROUTING处理（6），并开始另一个处理循环，但现在是解封后的数据包。

![](https://help.mikrotik.com/docs/download/attachments/328227/02d_ipsec_decryption.png?version=1&modificationDate=1570628963779&api=v2)

同样的过程是封装，但顺序相反。第一个IP数据包通过设施得到处理，然后与IPsec政策相匹配（5），封装（6），然后发送到第二个循环的处理（7-10）。

![](https://help.mikrotik.com/docs/download/attachments/328227/02d_ipsec_encryption.png?version=1&modificationDate=1570628991706&api=v2)

## 快速路径

从目前所学的知识来看，这样的数据包处理需要大量的CPU资源。为了加快速度，FastPath在第一个RouterOS v6中被引入。它的作用是跳过Linux内核的处理，基本上是用RouterOS的一些功能换取性能。为了使FastPath发挥作用，需要接口驱动支持和特定的配置条件。

### 快速路径如何工作

FastPath是一个接口驱动程序扩展，它允许驱动程序直接与特定的RouterOS设施对话，而跳过其他设施。

![](https://help.mikrotik.com/docs/download/attachments/328227/fastpath.svg?version=1&modificationDate=1570628869555&api=v2)

只有在至少源接口支持快速路径的情况下，数据包才能被快速路径处理程序转发。对于完整的快速转发，还需要目的地接口的支持。

目前，RouterOS有以下快速路径处理程序：

- IPv4
- IPv4 FastTrack
- Traffic Generator
- MPLS
- Bridge

如果满足以下条件，则使用IPv4 FastPath处理程序。

- 没有配置防火墙规则。
- 没有配置简单队列或 _parent=global_ 的队列树。
- 没有配置Mesh、metarouter接口。
- 嗅探器或Torch没有运行。
- 连接跟踪没有激活。
- IP会计被禁用。
- 没有配置VRF（`/ip route vrf`为空）。
- 没有使用热点（`/ip hotspot`没有接口）。
- 没有配置IPSec策略。
- `/tool mac-scan`未被积极使用。
- `/tool ip-scan'未被积极使用。

如果使用FastTrack，无论是否满足上述条件，数据包都以FastPath的方式传输。

如果接口支持该功能，流量生成器和MPLS会自动使用FastPath。目前，MPLS快速路径只适用于MPLS交换流量（以MPLS形式进入路由器的帧，必须以MPLS形式离开路由器）-MPLS入站和出站（包括做VPLS编码/解码的VPLS隧道端点）将和以前一样操作。

如果满足以下条件，则使用网桥处理程序。

- 没有桥接Calea、过滤器、NAT规则。
- _use-ip-firewall_ 被禁用。
- 没有Mesh、MetaRouter接口配置。
- 嗅探器、Torch 和流量生成器没有运行。
- bridge vlan-filtering 被禁用 (从 RouterOS 7.2 版本开始，该条件被移除)。
- 网桥 dhcp-snooping 被禁用。

vlan过滤网桥上的FastPath不支持有优先级标记的数据包(有VLAN头但VLAN ID=0的数据包)。这些数据包会通过慢速路径重定向。

支持 FastPath 的接口。

| RouterBoard       | 接口                                                                                                                                                                                  |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **RB6xx series**  | ether1,2                                                                                                                                                                              |
| **RB800**         | ether1,2                                                                                                                                                                              |
| **RB1100 series** | ether1-11                                                                                                                                                                             |
| **All devices**   | 以太网接口<br> wireless interfaces<br> bridge interfaces<br> VLAN, VRRP interfaces<br> bonding interfaces (RX only)<br> PPPoE, L2TP interfaces<br> EoIP, GRE, IPIP, VXLAN interfaces. |

EoIP、Gre、IPIP、VXLAN和L2TP接口有每个接口的设置 _allow-fast-path_ 。允许这些接口上的快速路径有一个副作用，即绕过防火墙、连接跟踪、简单队列、parent=global的队列树、IP审计、IPsec、Hotspot通用客户端、通过快速路径封装数据的vrf分配。另外，在FastPath中不接收数据包碎片。

可以通过检查 `/interface print detail` 中的fast-path属性值来验证是否支持FastPath。

唯一能保证FastPath的接口队列是only-hardware-queue。如果你需要硬件以外的接口队列，那么数据包将不会完全走FastPath，但对性能影响不大，因为 "接口队列 "是数据包流程中的最后一步。

数据包可以从FastPath切换到SlowPath而走半FastPath，但不能反过来走。因此，如果接收接口有FastPath支持，但输出接口没有，那么路由器将通过FastPath处理程序尽可能地处理数据包，然后用SlowPath进行处理。如果接收接口不支持FastPath，但输出接口支持FastPath，那么数据包将由SlowPath一路通过路由器进行处理。

![](https://help.mikrotik.com/docs/download/attachments/328227/half-fastpath.png?version=1&modificationDate=1570628812692&api=v2)

## FastTrack

Fasttrack可以解读为快速路径+连接跟踪。允许把连接标记为 "快速跟踪"，标记属于快速跟踪连接的数据包将以快速路径方式发送。这种连接的连接表项现在会有一个快速跟踪的标志。

![](https://help.mikrotik.com/docs/download/attachments/328227/fasttrack.png?version=1&modificationDate=1570628705594&api=v2)

快速跟踪数据包可以绕过防火墙、连接跟踪、简单队列、parent=global的队列树、IP流量（6.33中取消了限制）、IP审计、IPSec、热点通用客户端、VRF分配，因此，管理员要确保快速跟踪不干扰其他配置。

为了把一个连接标记为快速跟踪，实施了新的操作 "_fasttrack-connection_"，用于防火墙过滤和纠错。目前，只有IPv4 TCP和UDP连接可以被快速跟踪，为了维护连接跟踪条目，一些随机数据包仍然会发送到慢速路径上。在设计启用 "快速跟踪 "防火墙时必须考虑到这一点。

快速跟踪处理程序还支持源和目的地NAT，因此不需要对NAT连接进行特殊的处理。

属于快速跟踪连接的流量在FastPath中处理，意味着它不会被其他路由器的L3设施（防火墙、队列、IPsec、IP核算、VRF分配等）看到。快速通道在设置路由标记之前查找路由，所以只对主路由表起作用。

在家用路由器上使用该功能的最简单方法是为所有 _已建立的、相关的_ 连接启用 "快速跟踪"。

```shell
/ip firewall filter
add chain=forward action=fasttrack-connection connection-state=established,related \
  comment="fasttrack established/related"
add chain=forward action=accept connection-state=established,related \
  comment="accept established/related"
```

注意，第一条规则把已建立的/相关的连接标记为快速跟踪，第二条规则仍然需要接受属于这些连接的数据包。原因是如前面提到的，一些来自快速跟踪连接的随机数据包仍然被发送到慢速路径，只有UDP和TCP是快速跟踪的，但我们仍然希望接受其他协议的数据包。

![](https://help.mikrotik.com/docs/download/attachments/328227/fasttrack1_example.png?version=1&modificationDate=1570630152952&api=v2)![](https://help.mikrotik.com/docs/download/attachments/328227/fasttrack1_example2.png?version=1&modificationDate=1570630153168&api=v2)

在添加了 "FastTrack "规则后，列表的顶部出现了特殊的假规则。这不是一个实际的规则，它是为了显示一些流量是在快速路径上行驶，不会到达其他防火墙规则的视觉信息。

只要有至少一个快速跟踪的连接跟踪条目，这些规则就会出现，在连接表中最后一个快速跟踪的连接超时后就会消失。

连接是快速跟踪的，直到连接关闭、超时或路由器重启。

### 要求

如果满足以下条件，IPv4快速跟踪会激活。

- 没有Mesh、metarouter接口配置。
- 嗅探器、Torch和流量发生器没有运行。
- "/tool mac-scan"没有被积极使用。
- "/tool ip-scan"没有被主动使用。
- IP/Settings下的FastPath和Route缓存已启用。

## 视力障碍者的数据包流

以下是DOCX格式的文件，以优化的方式为视障人士描述了该图。这些描述是由Benetech的Apex CoVantage提供的。它们没有更新。

- [Packet flow, optimized document](https://box.mikrotik.com/f/673207754e4d40638fae/?dl=1)
