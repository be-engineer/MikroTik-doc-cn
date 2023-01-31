# 介绍

___

众所周知，有些配置在设计上存在重大缺陷，应尽可能避免。错误的Layer2配置有时会导致难以察觉的网络错误、随机的性能下降、网络的某些部分无法到达、某些网络服务出现故障，或者完全的网络故障。本页将包含一些常见和不太常见的配置，这些配置会在你的网络中引起问题。

# 单个交换芯片上的网桥

___

考虑以下情况，有一个内置交换芯片的设备，需要将某些端口相互隔离，为此，你创建了多个网桥，并在上面启用了硬件卸载功能。由于每个网桥都位于不同的二层域上，那么二层帧就不会在这些网桥之间转发，因此，每个网桥中的端口与不同网桥上的其他端口是隔离的。

## 配置

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=bridge1</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=bridge2</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros constants">/interface bridge port</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether1</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether2</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge2</code> <code class="ros value">interface</code><code class="ros plain">=ether3</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge2</code> <code class="ros value">interface</code><code class="ros plain">=ether4</code></div></div></td></tr></tbody></table>

## 问题

经过简单的性能测试，你可能会注意到一个网桥能够以线速转发流量，而第二个、第三个等网桥却不能像第一个网桥那样转发大量数据。另一个症状可能是，需要路由的数据包存在巨大的延迟。经过快速检查，你可能会注意到 CPU 总是处于满负荷状态，这是因为硬件卸载并不是在所有网桥上都可用，而是只在一个网桥上可用。通过检查硬件卸载的状态，你会发现只有一个网桥是激活的。

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; </code><code class="ros constants">/interface bridge port </code><code class="ros plain">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disabled, I - inactive, D - dynamic, H - hw-offload</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros comments">#&nbsp;&nbsp;&nbsp;&nbsp; INTERFACE&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; BRIDGE&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; HW</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">0&nbsp;&nbsp; H ether1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; bridge1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; yes</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">1&nbsp;&nbsp; H ether2&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; bridge1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; yes</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">2&nbsp;&nbsp;&nbsp;&nbsp; ether3&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; bridge2&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; yes</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">3&nbsp;&nbsp;&nbsp;&nbsp; ether4&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; bridge2&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; yes</code></div></div></td></tr></tbody></table>

之所以只有一个网桥有硬件卸载标志可用，是因为设备不支持端口隔离。如果不支持端口隔离，那么只有一个网桥能够将流量卸载到交换机芯片上。

## 症状

下面列出了可能是这种错误配置造成的症状。

- 网桥端口缺少 "H "标志
- 吞吐量低
- CPU使用率高

##解决方案

不是所有的设备都支持端口隔离，目前只有CRS1xx/CRS2xx系列设备支持，而且只同时支持7个隔离和硬件卸载的网桥，其他设备必须使用CPU来转发其他网桥上的数据包。这通常是一个硬件限制，可能需要不同的设备。网桥split-horizon参数是一个软件功能，可以禁用硬件卸载，当使用网桥过滤规则时，需要启用转发所有数据包到CPU，这需要禁用硬件卸载。可以通过`hw=yes`标志来控制哪个网桥将被硬件卸载，也可以通过给其他网桥设置`hw=no`来控制，例如。

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge port </code><code class="ros functions">set </code><code class="ros plain">[</code><code class="ros functions">find </code><code class="ros plain">where </code><code class="ros value">bridge</code><code class="ros plain">=bridge1]</code> <code class="ros value">hw</code><code class="ros plain">=no</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros constants">/interface bridge port </code><code class="ros functions">set </code><code class="ros plain">[</code><code class="ros functions">find </code><code class="ros plain">where </code><code class="ros value">bridge</code><code class="ros plain">=bridge2]</code> <code class="ros value">hw</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

有时可以重组网络拓扑结构，使用VLAN，这是隔离第二层网络的正确方式。

# 用硬件卸载和MAC学习的包流

___

考虑以下情况，你设置了一个网桥，并启用了硬件卸载，以便最大限度地提高设备的吞吐量，结果你的设备作为交换机工作，但你想使用 [Sniffer](https://help.mikrotik.com/docs/display/ROS/Packet+Sniffer) 或 [Torch](https://help.mikrotik.com/docs/display/ROS/Torch) 工具进行调试，也可能你需要实现数据包记录。

## 配置

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=bridge1</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge port</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">hw</code><code class="ros plain">=yes</code> <code class="ros value">interface</code><code class="ros plain">=ether1</code> <code class="ros value">learn</code><code class="ros plain">=yes</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">hw</code><code class="ros plain">=yes</code> <code class="ros value">interface</code><code class="ros plain">=ether2</code> <code class="ros value">learn</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

## 问题

当运行[Sniffer](https://help.mikrotik.com/docs/display/ROS/Packet+Sniffer)或[Torch](https://help.mikrotik.com/docs/display/ROS/Torch)工具来捕获数据包时，可能几乎看不到任何数据包，只有一些单播数据包，但大部分是广播/多播数据包被捕获，而接口报告说流经某些接口的流量比捕获的流量大得多。自RouterOS v6.41以来，如果你将两个或更多的以太网接口添加到一个网桥中，并启用[Hardware Offloading](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-BridgeHardwareOffloading)，那么交换芯片将被用来在端口之间转发数据包。为了理解为什么只有部分数据包被捕获，我们必须首先检查交换芯片是如何与CPU互连的，在这个例子中，我们可以使用一个通用的5端口以太网路由器的框图。

![](https://help.mikrotik.com/docs/download/attachments/19136718/Switch_chip_block_diagram.png?version=2&modificationDate=1618319143136&api=v2)

对于这个设备，每个以太网端口都和交换芯片相连，交换芯片使用CPU端口（有时称为**交换机-cpu**端口）和CPU相连。为了使数据包在Sniffer或Torch工具中可见，数据包必须从一个以太网端口发送到CPU端口，这意味着数据包必须以CPU端口为目的地（数据包的目的MAC地址与网桥的MAC地址相匹配），或者数据包的MAC地址没有被学习（数据包被转发到所有端口）。

交换芯片保存了一个MAC地址和端口的列表，称为**主机表**。 每当有数据包需要转发时，交换芯片就会根据主机表检查数据包的目的MAC地址，以找到应该用哪个端口来转发数据包。如果交换芯片找不到目的MAC地址，那么数据包就会被转发到所有的端口（包括CPU端口）。在这样的情况下，一个数据包应该从ether1转发到ether2，而ether2后面的设备的MAC地址在主机表中，那么这个数据包就不会被发送到CPU，因此不会被Sniffer或Torch工具发现。

## 症状

以下可能是这种错误配置的结果的症状列表。

- 数据包不能被Sniffer或Torch工具看到
- 过滤规则不起作用

## 解决方案

由于数据包没有被转发到所有的端口，所以带有已学习的目标MAC地址的数据包将不会被发送到CPU。如果你需要为数据包分析器或防火墙发送某些数据包到CPU，那可以通过使用ACL规则将数据包复制或重定向到CPU。下面的例子，说明如何发送一份针对**4C:5E:0C:4D:12:4B**的数据包。

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface ethernet switch rule</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">copy-to-cpu</code><code class="ros plain">=yes</code> <code class="ros value">dst-mac-address</code><code class="ros plain">=4C:5E:0C:4D:12:4B/FF:FF:FF:FF:FF:FF</code> <code class="ros value">ports</code><code class="ros plain">=ether1</code> <code class="ros value">switch</code><code class="ros plain">=switch1</code></div></div></td></tr></tbody></table>

如果数据包被发送到CPU，那么该数据包必须由CPU处理，这就增加了CPU的负载。

# LAG接口和负载平衡

___

考虑以下情况，你创建了一个LAG接口来增加两个网络节点之间的总带宽，通常，这些节点是交换机。为了测试，确保LAG接口工作正常，你连接了两个传输数据的服务器，最常用的是著名的网络性能测量工具[https://en.wikipedia.org/wiki/Iperf](https://en.wikipedia.org/wiki/Iperf)来测试这种设置。例如，你可能用两个千兆以太网端口做了一个LAG接口，这样就有了一个虚拟接口，可以在两个接口上负载平衡流量，理论上可以达到2Gbps的吞吐量，而服务器则使用10Gbps接口连接，例如SFP+。

![](https://help.mikrotik.com/docs/download/attachments/19136718/Lacp.png?version=2&modificationDate=1618319179534&api=v2)

## 配置

以下配置与**SW1**和**SW2**有关。

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bonding</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">mode</code><code class="ros plain">=802.3ad</code> <code class="ros value">name</code><code class="ros plain">=bond1</code> <code class="ros value">slaves</code><code class="ros plain">=ether1,ether2</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=bridge1</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge port</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=bond1</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=sfp-sfpplus1</code></div></div></td></tr></tbody></table>

## 问题

经过初步测试，你立即注意到网络吞吐量从未超过1Gbps的限制，即使服务器和网络节点（本例中为交换机）的CPU负载很低，但吞吐量仍被限制在只有1Gbps。这背后的原因是LACP（802.ad）使用发送散列策略，以确定流量是否可以在多个LAG成员上平衡，在这种情况下，一个LAG接口不会创建一个2Gbps的接口，而是一个可以在多个从属接口上平衡流量的接口，只要有可能。对于每个数据包，都会产生一个传输散列，这决定了数据包将通过哪个LAG成员发送，避免数据包被打乱顺序，有一个选项可以选择传输散列策略，这个选项可以在二层（MAC）、三层（IP）和四层（端口）之间选择，在RouterOS中，可以使用`传输散列策略`参数来选择。在这种情况下，传输哈希值是相同的，因为你把数据包发送到相同的目标MAC地址，以及相同的IP地址，Iperf也使用相同的端口，这对所有数据包产生相同的传输哈希值，LAG成员之间的负载平衡是不可能的。请注意，即使目的地不同，也不是所有的数据包都会在LAG成员之间得到平衡，这是因为标准化的传输散列策略可以为不同的目的地产生相同的传输散列，例如，192.168.0.1/192.168.0.2将得到平衡，但192.168.0.2/192.168.0.4将得不到平衡，如果使用 "2-3层 "传输散列策略且目的地MAC地址是相同的话。

## 症状

以下可能是这种错误配置导致的症状列表。

- 流量只通过一个LAG成员

##解决方案

选择适当的传输散列策略，正确测试网络的吞吐量。测试这种设置的最简单方法是使用多个目的地，例如，不要只向一个服务器发送数据，而是向多个服务器发送数据，这将为每个数据包产生不同的传输散列，并使跨LAG成员的负载均衡成为可能。对于一些设置，你可能想改变粘合接口模式，以增加总吞吐量，对于UDP流量`均衡-rr`模式可能足够了，但对于TCP流量可能会引起问题，你可以阅读更多关于为你的设置选择正确模式的信息，见[这里](https://help.mikrotik.com/docs/display/ROS/Bonding#Bonding-Bondingmodes)。

# 从属接口上的VLAN接口

___

考虑以下情况，你创建了一个网桥，你希望DHCP服务器只给某个标记的VLAN流量发放IP地址，为此，你创建了一个VLAN接口，指定了一个VLAN ID，并在上面创建了一个DHCP服务器，但由于某些原因，它不能正常工作。

## 配置

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=bridge1</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge port</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=ether1</code> <code class="ros value">bridge</code><code class="ros plain">=bridge1</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=ether2</code> <code class="ros value">bridge</code><code class="ros plain">=bridge1</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros constants">/interface vlan</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=VLAN99</code> <code class="ros value">interface</code><code class="ros plain">=ether1</code> <code class="ros value">vlan-id</code><code class="ros plain">=99</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros constants">/ip pool</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=VLAN99_POOL</code> <code class="ros value">range</code><code class="ros plain">=192.168.99.100-192.168.99.200</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros constants">/ip address </code><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=192.168.99.1/24</code> <code class="ros value">interface</code><code class="ros plain">=VLAN99</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros constants">/ip dhcp-server</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=VLAN99</code> <code class="ros value">address-pool</code><code class="ros plain">=VLAN99_POOL</code> <code class="ros value">disabled</code><code class="ros plain">=no</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="ros constants">/ip dhcp-server network</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=192.168.99.0/24</code> <code class="ros value">gateway</code><code class="ros plain">=192.168.99.1</code> <code class="ros value">dns-server</code><code class="ros plain">=192.168.99.1</code></div></div></td></tr></tbody></table>

## 问题

当在网桥上增加一个接口时，网桥就成了主接口，所有网桥端口都成了从接口，这意味着网桥端口上收到的所有流量都被网桥接口捕获，所有流量都通过网桥接口而不是物理接口转发给 CPU。因此，在从属接口上创建的VLAN接口根本不会捕获任何流量，因为在进行任何数据包处理之前，它就被立即转发到主接口。通常的副作用是，有些DHCP客户收到IP地址，有些则没有。

## 症状

以下可能是这种错误配置的结果的症状列表。

- DHCP客户/服务器不能正常工作。
- 设备无法到达。
- 网桥后面的设备在有标签的情况下无法到达。

## 解决方案

改变VLAN接口监听流量的接口，将其改为主接口。

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface vlan </code><code class="ros functions">set </code><code class="ros plain">VLAN99 </code><code class="ros value">interface</code><code class="ros plain">=bridge1</code></div></div></td></tr></tbody></table>

# 网桥中的网桥上的VLAN

___

考虑以下情况，有一组接口（不一定是物理接口），你希望所有的接口都在同一个二层网段中，解决方案是把它们加到一个网桥上，但你要求从一个端口来的流量把所有流量都标记到某个VLAN中。这可以通过在网桥接口之上创建一个 VLAN 接口，并创建一个单独的网桥，其中包含这个新创建的 VLAN 接口，这个接口应该为所有收到的流量添加一个 VLAN 标签来实现。下面是一张网络图。

![](https://help.mikrotik.com/docs/download/attachments/19136718/Vlan_on_bridge_in_bridge.png?version=2&modificationDate=1618319364846&api=v2)

## 配置

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=bridge1</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=bridge2</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros constants">/interface vlan</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=bridge1</code> <code class="ros value">name</code><code class="ros plain">=VLAN</code> <code class="ros value">vlan-id</code><code class="ros plain">=99</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros constants">/interface bridge port</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether1</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether2</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge2</code> <code class="ros value">interface</code><code class="ros plain">=VLAN</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge2</code> <code class="ros value">interface</code><code class="ros plain">=ether3</code></div></div></td></tr></tbody></table>

## 问题

为了更好地理解根本问题，让我们先看看桥接主机表。

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@switch] </code><code class="ros constants">/interface bridge host </code><code class="ros functions">print </code><code class="ros plain">where !</code><code class="ros functions">local</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disabled, I - invalid, D - dynamic, L - local, E - external</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros comments">#&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; MAC-ADDRESS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; VID ON-INTERFACE&nbsp;&nbsp;&nbsp; BRIDGE</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">0&nbsp;&nbsp; D&nbsp;&nbsp; CC</code><code class="ros constants">:2D:E0:E4:B3:A1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ether1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; bridge1</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">1&nbsp;&nbsp; D&nbsp;&nbsp; CC</code><code class="ros constants">:2D:E0:E4:B3:A2&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ether2&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; bridge1</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">2&nbsp;&nbsp; D&nbsp;&nbsp; CC</code><code class="ros constants">:2D:E0:E4:B3:A1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; VLAN&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; bridge2</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">3&nbsp;&nbsp; D&nbsp;&nbsp; CC</code><code class="ros constants">:2D:E0:E4:B3:A2&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; VLAN&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; bridge2</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">4&nbsp;&nbsp; D&nbsp;&nbsp; CC</code><code class="ros constants">:2D:E0:E4:B3:A3&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ether3&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; bridge2</code></div></div></td></tr></tbody></table>

在**ether1**和**ether2**上的设备需要发送带有VLAN-ID 99的标签数据包，以便到达**ether3**上的主机（其他数据包不会被传到VLAN接口并进一步与ether3桥接）。我们可以在主机表中看到，**bridge2**已在**bridge1**中泛滥。但由于MAC学习只能在网桥端口之间进行，而不能在网桥接口之上创建的接口上进行，从**ether2**发往**ether3**的数据包将在**bridge1**被经学会了这些主机。从**ether3**到**ether1**的数据包将被正确地送出标记，流量不会泛滥。

另外，如果**ether3**后面的设备正在使用(R)STP，那么**ether1**和**ether2**将发送标记的BPDU，这违反了IEEE 802.1W标准。由于MAC学习功能被破坏和(R)STP被破坏，这种设置和配置必须被避免。人们还知道，在某些设置中，这种配置会使你无法通过使用MAC telnet连接到设备上。

## 症状

以下可能是这种错误配置导致的症状列表。

- 端口被RSTP封锁
- 网络中的环路
- 端口跳动
- 流量被转发到所有端口
- MAC telnet无法连接
- 设备无法访问

## 解决方案

使用网桥VLAN过滤。标记流量的正确方法是在流量进入网桥时分配一个VLAN ID，这种行为可以通过为网桥端口指定**PVID**值，并指定哪些端口是**标记的**（聚合）端口，哪些是**不标记的**（接入）端口来轻松实现。下面是一个例子，说明该如何配置。

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=bridge1</code> <code class="ros value">vlan-filtering</code><code class="ros plain">=yes</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge port</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether1</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether2</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether3</code> <code class="ros value">pvid</code><code class="ros plain">=99</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge vlan</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">tagged</code><code class="ros plain">=ether1,ether2</code> <code class="ros value">untagged</code><code class="ros plain">=ether3</code> <code class="ros value">vlan-ids</code><code class="ros plain">=99</code></div></div></td></tr></tbody></table>
  
通过启用`vlan-filtering`，你将过滤掉以CPU为目的地的流量，在启用VLAN过滤之前，确保你设置了一个[管理端口]（https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-Managementaccessconfiguration）。

# VLAN在一个有物理接口的网桥中

___

与[VLAN on a bridge in a bridge](https://help.mikrotik.com/docs/display/ROS/Layer2+misconfiguration#Layer2misconfiguration-VLANonabridgeinabridge)的情况非常相似，有多种可能的情况，最流行的用例是你想通过一个物理接口发送带标签的流量时，你希望一个接口的流量只接收某些带标签的流量，通过一个物理接口（简化聚合/接入端口设置）将这些带标签的流量作为标签发送，只需使用VLAN接口和一个桥。

## 配置

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface vlan</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=ether1</code> <code class="ros value">name</code><code class="ros plain">=VLAN99</code> <code class="ros value">vlan-id</code><code class="ros plain">=99</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=bridge1</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge port</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=ether2</code> <code class="ros value">bridge</code><code class="ros plain">=bridge1</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=VLAN99</code> <code class="ros value">bridge</code><code class="ros plain">=bridge1</code></div></div></td></tr></tbody></table>

## 问题

这种设置和配置在大多数情况下是可行的，但在使用(R)STP时，它违反了IEEE 802.1W标准。如果这是你的第二层域中唯一的设备，那么这应该不会造成问题，但当有其他厂商的交换机时，问题就会出现。原因是在网桥接口上的(R)STP是默认启用的，来自**ether1**的BPDU将被标记送出，因为所有送入**ether1**的东西都将作为标记流量通过**ether2**送出，并非所有交换机都能理解标记BPDU。在一个比较复杂的网络中，对于某些（一组）VLAN有多种网络拓扑结构，这种配置应该谨慎，这与混合供应商设备的MSTP和PVSTP(+)有关。在对某些VLAN有多种网络拓扑的环形拓扑中，交换机的一个端口将被阻塞，但在MSTP和PVSTP(+)中，可以为某个VLAN打开一条路径，在这种情况下，不支持PVSTP(+)的设备有可能会取消BPDU的标签，转发BPDU，结果，交换机会收到自己的数据包，触发环路检测，阻塞一个端口，这种情况也可能发生在其他协议上，但（R）STP是最常见的例子。如果交换机正在使用BPDU防护功能，那么这种类型的配置会触发它，导致一个端口被STP阻塞。据报道，在使用6.41或更高版本时，这种类型的配置可以阻止流量在某些网桥端口上长期转发。这种类型的配置不仅会破坏(R/M)STP，而且会引起环路警告，这可能是由MNDP数据包或任何其他直接从接口发出的数据包引起的。

## 症状

以下可能是这种错误配置导致的症状列表。

- 端口被RSTP封锁
- 网络中的环路
- 端口跳动
- 随着时间的推移，流量停止转发
- BPDU被其他启用RSTP的设备所忽略

## 解决方案

为了避免兼容性问题，你应该使用网桥VLAN过滤。下面你可以找到一个例子，说明如何用网桥VLAN过滤配置实现同样的流量标记效果。

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=bridge1</code> <code class="ros value">vlan-filtering</code><code class="ros plain">=yes</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge port</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether1</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether2</code> <code class="ros value">pvid</code><code class="ros plain">=99</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros constants">/interface bridge vlan</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">tagged</code><code class="ros plain">=ether1</code> <code class="ros value">untagged</code><code class="ros plain">=ether2</code> <code class="ros value">vlan-ids</code><code class="ros plain">=99</code></div></div></td></tr></tbody></table>

  

多达28个共有配置文件通过`vlan-filtering`启用，将过滤掉以CPU为目的地的流量，在启用VLAN过滤之前，要确保设置了一个[管理端口](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-Managementaccessconfiguration) 。

# 物理接口上的桥接VLAN

___

和[桥中桥VLAN](https://help.mikrotik.com/docs/display/ROS/Layer2+misconfiguration#Layer2misconfiguration-VLANonabridgeinabridge)非常相似的情况，考虑以下情况，网络中有几台交换机，需要用VLAN来隔离某些第二层域，并将这些交换机连接到一个分配地址的路由器，并将流量路由到全世界。为了实现冗余，将所有的交换机直接连接到路由器上，并启用了RSTP，但是为了能够设置DHCP服务器，你决定在连接到交换机的每个物理接口上为每个VLAN创建一个VLAN接口，并将这些VLAN接口添加到一个网桥中。下面是一张网络图。

![](https://help.mikrotik.com/docs/download/attachments/19136718/Bridged_vlans.png?version=2&modificationDate=1618319386972&api=v2)

## 配置

只有路由器部分与本案例有关，交换机的配置其实并不重要，只要端口是交换的。路由器的配置可以在下面找到。

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=bridge10</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=bridge20</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros constants">/interface vlan</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=ether1</code> <code class="ros value">name</code><code class="ros plain">=ether1_v10</code> <code class="ros value">vlan-id</code><code class="ros plain">=10</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=ether1</code> <code class="ros value">name</code><code class="ros plain">=ether1_v20</code> <code class="ros value">vlan-id</code><code class="ros plain">=20</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=ether2</code> <code class="ros value">name</code><code class="ros plain">=ether2_v10</code> <code class="ros value">vlan-id</code><code class="ros plain">=10</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=ether2</code> <code class="ros value">name</code><code class="ros plain">=ether2_v20</code> <code class="ros value">vlan-id</code><code class="ros plain">=20</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge port</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge10</code> <code class="ros value">interface</code><code class="ros plain">=ether1_v10</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge10</code> <code class="ros value">interface</code><code class="ros plain">=ether2_v10</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge20</code> <code class="ros value">interface</code><code class="ros plain">=ether1_v20</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge20</code> <code class="ros value">interface</code><code class="ros plain">=ether2_v20</code></div></div></td></tr></tbody></table>

## 问题

可能网络会有一些奇怪的延迟，甚至网络没有反应，可能会检测到有一个环路（用自己的MAC地址接收的数据包），有些流量不知从哪里产生。这个问题的出现是因为来自**路由器上创建的VLAN接口之一的广播数据包将被送出物理接口，数据包将通过物理接口被转发。在这种情况下，从**ether1_v10**发出的广播数据包将在**ether2**上收到，数据包将被**ether2_v10**捕获，它与**ether1_v10**桥接，并将在同一路径上再次转发（循环）。(R)STP不一定能发现这个环路，因为(R)STP不知道任何VLAN，环路不存在于无标签的流量，但存在于有标签的流量。因此，发现环路是非常明显的，但在更复杂的设置中，发现网络设计缺陷并不容易。有时，如果你的网络不使用广播流量，这种网络设计缺陷可能会在很长一段时间内被忽视，通常，[邻居发现协议](https://help.mikrotik.com/docs/display/ROS/Neighbor+discovery)从VLAN接口广播数据包，在这种设置中通常会触发环路检测。有时捕获触发环路检测的数据包是很有用的，可以通过嗅探器和分析数据包捕获文件:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/tool sniffer</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros value">filter-mac-address</code><code class="ros plain">=4C:5E:0C:4D:12:44/FF:FF:FF:FF:FF:FF</code> <code class="ros plain">\</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros value">filter-interface</code><code class="ros plain">=ether1</code> <code class="ros value">filter-direction</code><code class="ros plain">=rx</code> <code class="ros value">file-name</code><code class="ros plain">=loop_packet.pcap</code></div></div></td></tr></tbody></table>

或者使用更方便的记录方式。

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge filter</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=log</code> <code class="ros value">chain</code><code class="ros plain">=forward</code> <code class="ros value">src-mac-address</code><code class="ros plain">=4C:5E:0C:4D:12:44/FF:FF:FF:FF:FF:FF</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=log</code> <code class="ros value">chain</code><code class="ros plain">=input</code> <code class="ros value">src-mac-address</code><code class="ros plain">=4C:5E:0C:4D:12:44/FF:FF:FF:FF:FF:FF</code></div></div></td></tr></tbody></table>

## 症状

以下可能是这种错误配置结果的症状列表。

- 端口被(R)STP封锁。
- 网络中的环路。
- 吞吐量低。
- 端口跳动。
- 网络无法访问。

## 解决方案

一个解决方案是使用网桥VLAN过滤，以使所有网桥与IEEE 802.1W和IEEE 802.1Q兼容。

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=bridge</code> <code class="ros value">vlan-filtering</code><code class="ros plain">=yes</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge port</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">interface</code><code class="ros plain">=ether1</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">interface</code><code class="ros plain">=ether2</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros constants">/interface bridge vlan</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">tagged</code><code class="ros plain">=ether1,ether2,bridge</code> <code class="ros value">vlan-ids</code><code class="ros plain">=10</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">tagged</code><code class="ros plain">=ether1,ether2,bridge</code> <code class="ros value">vlan-ids</code><code class="ros plain">=20</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros constants">/interface vlan</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=vlan10</code> <code class="ros value">interface</code><code class="ros plain">=bridge</code> <code class="ros value">vlan-id</code><code class="ros plain">=10</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=vlan20</code> <code class="ros value">interface</code><code class="ros plain">=bridge</code> <code class="ros value">vlan-id</code><code class="ros plain">=20</code></div></div></td></tr></tbody></table>

  

通过启用`vlan-filtering`，将过滤掉以CPU为目的地的流量，在启用VLAN过滤之前，要确保设置了一个[管理端口]（https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-Managementaccessconfiguration）。

# 网桥VLAN

___

[物理接口上的网桥VLAN](https://help.mikrotik.com/docs/display/ROS/Layer2+misconfiguration#Layer2misconfiguration-BridgedVLANonphysicalinterfaces)的更简化方案，这种情况下，你只是想把创建在不同物理接口上的两个或多个VLAN桥接起来。这是一种常见的设置，值得单独写一篇文章，因为错误配置这种类型的设置已经造成了多个网络故障。这种类型的设置也被用于VLAN转换。

## 配置

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface vlan</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=ether1</code> <code class="ros value">name</code><code class="ros plain">=ether1_v10</code> <code class="ros value">vlan-id</code><code class="ros plain">=10</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=ether2</code> <code class="ros value">name</code><code class="ros plain">=ether2_v10</code> <code class="ros value">vlan-id</code><code class="ros plain">=10</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros constants">/interface bridge</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=bridge1</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros constants">/interface bridge port</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether1_v10</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether2_v10</code></div></div></td></tr></tbody></table>

问题

你可能会注意到，网络的某些部分无法访问或某些链接一直在跳动。这是由于(R)STP这种类型的配置迫使设备发送标记的BPDU，这可能不被其他设备支持，包括RouterOS。设备收到一个畸形的数据包（运行(R)STP时，网络中不应该存在标记的BPDU，这违反了IEEE 802.1W和IEEE 802.1Q），设备将不能正确解释数据包，并可能出现意外的行为。

## 症状

以下可能是这种错误配置结果的症状列表。

- 端口被(R)STP封锁。
- 端口跳动。
- 网络无法访问。

## 解决方案

最简单的解决办法是在网桥上禁用(R)STP。

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">bridge1 </code><code class="ros value">protocol-mode</code><code class="ros plain">=none</code></div></div></td></tr></tbody></table>
  
建议重写你的配置，以使用网桥VLAN过滤。

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=bridge1</code> <code class="ros value">vlan-filtering</code><code class="ros plain">=yes</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge port</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether1</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether2</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros constants">/interface bridge vlan</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">tagged</code><code class="ros plain">=ether1,ether2</code> <code class="ros value">vlan-ids</code><code class="ros plain">=10</code></div></div></td></tr></tbody></table>
  

通过启用`vlan-filtering`，将过滤掉以CPU为目的的流量，在启用VLAN过滤之前，要确保设置了一个[管理端口](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-Managementaccessconfiguration)。

# non-CRS3xx上的网桥VLAN过滤

___

考虑以下情况，你发现了新的网桥VLAN过滤功能，你决定改变你设备上的配置，你有一个非常简单的聚合/接入端口设置，你喜欢网桥VLAN过滤的概念。

## 配置

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=bridge1</code> <code class="ros value">vlan-filtering</code><code class="ros plain">=yes</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge port</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether1</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether2</code> <code class="ros value">pvid</code><code class="ros plain">=20</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether3</code> <code class="ros value">pvid</code><code class="ros plain">=30</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether4</code> <code class="ros value">pvid</code><code class="ros plain">=40</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros constants">/interface bridge vlan</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">tagged</code><code class="ros plain">=ether1</code> <code class="ros value">untagged</code><code class="ros plain">=ether2</code> <code class="ros value">vlan-ids</code><code class="ros plain">=20</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">tagged</code><code class="ros plain">=ether1</code> <code class="ros value">untagged</code><code class="ros plain">=ether3</code> <code class="ros value">vlan-ids</code><code class="ros plain">=30</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">tagged</code><code class="ros plain">=ether1</code> <code class="ros value">untagged</code><code class="ros plain">=ether4</code> <code class="ros value">vlan-ids</code><code class="ros plain">=40</code></div></div></td></tr></tbody></table>

## 问题

例如，在CRS1xx/CRS2xx系列设备上使用这种配置，你注意到CPU的使用率非常高，当运行性能测试检查网络的吞吐量时，总的吞吐量只有线速的一小部分。问题的原因是，并非所有设备都在硬件层面上支持桥接VLAN过滤。所有的设备都能够被配置成桥接VLAN过滤，但只有少数设备能够将流量卸载到交换芯片上。如果在有内置交换芯片的设备上使用不恰当的配置方法，那么CPU将被用来转发流量。

## 症状

下面列出了可能是这种错误配置造成的症状。

- 在桥接端口上缺少 "H "标志
- 吞吐量低
- CPU使用率高

## 解决方案

在使用网桥VLAN过滤之前，请检查设备是否在硬件层面上支持它，在[Bridge Hardware Offloading](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-BridgeHardwareOffloading)部分可以找到一个兼容性表格。每种类型的设备都需要不同的配置方法，下面列出使用硬件卸载的好处，应该在设备上使用哪些配置。

- [CRS3xx series devices](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-BridgeVLANFiltering)
- [CRS1xx/CRS2xx series devices](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=103841836#CRS1xx/2xxseriesswitchesexamples-VLAN)
- [Other devices with a switch chip](https://help.mikrotik.com/docs/display/ROS/Switch+Chip+Features#SwitchChipFeatures-SetupExamples)

# VLAN过滤与多个交换芯片

___

考虑以下情况，设备有两个或更多的交换芯片，你决定使用一个单网桥，并在硬件层面设置VLAN过滤（通过使用`/interface ethernet switch`菜单），以便能够在网络上达到线速性能。这对于RB2011和RB3011系列设备来说是非常重要的。在这个例子中，假设你想有一个聚合端口，其他端口都是接入端口，例如，**ether10**是我们的聚合端口，**ether1-ether9**是我们的接入端口。

## 配置

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=bridge1</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge port</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether1</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether2</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether3</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether4</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether5</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether6</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether7</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether8</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether9</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether10</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="ros constants">/interface vlan</code></div><div class="line number15 index14 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=bridge1</code> <code class="ros value">name</code><code class="ros plain">=VLAN10</code> <code class="ros value">vlan-id</code><code class="ros plain">=10</code></div><div class="line number16 index15 alt1" data-bidi-marker="true"><code class="ros constants">/interface ethernet switch port</code></div><div class="line number17 index16 alt2" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">ether1,ether2,ether3,ether4,ether5,ether6,ether7,ether8,ether9 </code><code class="ros value">default-vlan-id</code><code class="ros plain">=10</code> <code class="ros value">vlan-header</code><code class="ros plain">=always-strip</code> <code class="ros value">vlan-mode</code><code class="ros plain">=secure</code></div><div class="line number18 index17 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">ether10 </code><code class="ros value">vlan-header</code><code class="ros plain">=add-if-missing</code> <code class="ros value">vlan-mode</code><code class="ros plain">=secure</code></div><div class="line number19 index18 alt2" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">switch1-cpu,switch2-cpu </code><code class="ros value">vlan-mode</code><code class="ros plain">=secure</code></div><div class="line number20 index19 alt1" data-bidi-marker="true"><code class="ros constants">/interface ethernet switch vlan</code></div><div class="line number21 index20 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">ports</code><code class="ros plain">=ether1,ether2,ether3,ether4,ether5,switch1-cpu</code> <code class="ros value">switch</code><code class="ros plain">=switch1</code> <code class="ros value">vlan-id</code><code class="ros plain">=10</code></div><div class="line number22 index21 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">ports</code><code class="ros plain">=ether6,ether7,ether8,ether9,ether10,switch2-cpu</code> <code class="ros value">switch</code><code class="ros plain">=switch2</code> <code class="ros value">vlan-id</code><code class="ros plain">=10</code></div></div></td></tr></tbody></table>

## 问题

在进行了一些测试后，可能会注意到，来自**ether6-ether10**的数据包被如期转发，但来自**ether1-ether5**的数据包并不总是被正确转发（特别是通过聚合端口）。最明显的问题是来自**ether1-ether5**到**ether10**的数据包被简单地丢弃，这是因为这些端口位于不同的交换芯片上，这意味着VLAN过滤在硬件层面上是不行的，因为交换芯片不知道不同交换芯片上的VLAN表的内容。位于不同交换芯片上的端口之间转发的数据包也由CPU处理，意味着你将无法实现线速性能。

## 症状

以下可能是错误配置结果的症状列表。

- 数据包被丢弃。
- 吞吐量低。

##解决方案

正确的解决方案是考虑到硬件设计，相应地规划网络拓扑结构。为了解决这个问题，必须创建两个独立的网桥，并在每个交换芯片上配置VLAN过滤，这就限制了在交换芯片之间转发数据包的可能性，不过也可以在两个网桥之间配置路由（如果连接在每个交换芯片上的设备使用不同的网络子网）。

有一种方法可以将设备配置成所有的端口一起交换，但又能在硬件层面上使用VLAN过滤，不过这个方案有一些注意事项。这个想法是在每个交换芯片上牺牲一个单一的以太网端口，作为聚合端口在交换芯片之间转发数据包，这可以通过在两个交换芯片之间插入以太网线来实现，例如，在**ether5**和**ether6**之间插入一根以太网线，然后重新配置你的设备，假设这些端口是聚合端口。

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge port</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether1</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether2</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether3</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether4</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether5</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge2</code> <code class="ros value">interface</code><code class="ros plain">=ether6</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge2</code> <code class="ros value">interface</code><code class="ros plain">=ether7</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge2</code> <code class="ros value">interface</code><code class="ros plain">=ether8</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge2</code> <code class="ros value">interface</code><code class="ros plain">=ether9</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge2</code> <code class="ros value">interface</code><code class="ros plain">=ether10</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros constants">/interface ethernet switch port</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">ether1,ether2,ether3,ether4,ether7,ether8,ether9 </code><code class="ros value">default-vlan-id</code><code class="ros plain">=10</code> <code class="ros value">vlan-header</code><code class="ros plain">=always-strip</code> <code class="ros value">vlan-mode</code><code class="ros plain">=secure</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">ether5,ether6,ether10 </code><code class="ros value">vlan-header</code><code class="ros plain">=add-if-missing</code> <code class="ros value">vlan-mode</code><code class="ros plain">=secure</code> <code class="ros value">default-vlan-id</code><code class="ros plain">=auto</code></div><div class="line number15 index14 alt2" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">switch1-cpu,switch2-cpu </code><code class="ros value">vlan-mode</code><code class="ros plain">=secure</code></div><div class="line number16 index15 alt1" data-bidi-marker="true"><code class="ros constants">/interface ethernet switch vlan</code></div><div class="line number17 index16 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">ports</code><code class="ros plain">=ether1,ether2,ether3,ether4,ether5,switch1-cpu</code> <code class="ros value">switch</code><code class="ros plain">=switch1</code> <code class="ros value">vlan-id</code><code class="ros plain">=10</code></div><div class="line number18 index17 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">ports</code><code class="ros plain">=ether6,ether7,ether8,ether9,ether10,switch2-cpu</code> <code class="ros value">switch</code><code class="ros plain">=switch2</code> <code class="ros value">vlan-id</code><code class="ros plain">=10</code></div></div></td></tr></tbody></table>

  

对于100Mbps交换芯片，使用`default-vlan-id=0`而不是`default-vlan-id=auto`。

# 用简化的网桥VLAN表进行VLAN过滤

___

需要创建一个网络设置，其中多个客户连接到不同的接入端口，并通过不同的VLAN进行隔离，这些流量要被标记并发送到相应的聚合端口。接入端口是使用pvid属性来配置的。由于聚合端口在两个VLAN上都使用，要通过添加一个桥接VLAN表项来简化配置，并用逗号来分隔VLAN。当在大量的 VLAN 或某些 VLAN 范围内使用标记的聚合端口时（例如 vlan-id=100-200），这一点特别有用。请看下面的网络图和配置。

![](https://help.mikrotik.com/docs/download/attachments/19136718/Switch_multiple_untagged.png?version=4&modificationDate=1583336457386&api=v2)

## 配置

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=bridge1</code> <code class="ros value">vlan-filtering</code><code class="ros plain">=yes</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge port</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether2</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether3</code> <code class="ros value">pvid</code><code class="ros plain">=10</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether4</code> <code class="ros value">pvid</code><code class="ros plain">=20</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge vlan</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">tagged</code><code class="ros plain">=ether2</code> <code class="ros value">vlan-ids</code><code class="ros plain">=10,20</code></div></div></td></tr></tbody></table>

## 问题

从接入端口到聚合端口的流量被正确地转发和标记，但一些广播或组播数据包实际上在两个未标记的接入端口之间被转发，尽管它们应该在不同的VLAN上。此外，来自标记端口的广播和组播流量也被转发到两个接入端口。这可能会引起一些安全问题，因为来自不同网络的流量可以被嗅探到。当你查看网桥VLAN表时，为VLAN 10和20创建了一个条目，而且这两个无标记的端口都属于同一个VLAN组。

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@SW1] </code><code class="ros constants">/interface bridge vlan </code><code class="ros functions">print </code><code class="ros plain">where </code><code class="ros value">tagged</code><code class="ros plain">=ether2</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Columns</code><code class="ros constants">: BRIDGE, VLAN-IDS, CURRENT-TAGGED, CURRENT-UNTAGGED</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros comments"># BRIDGE&nbsp;&nbsp; VLAN-IDS&nbsp; CURRENT-TAGGED&nbsp; CURRENT-UNTAGGED</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">;;; port with pvid added to untagged group which might cause problems, consider adding a separate VLAN entry</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">0 bridge1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 10&nbsp; ether2&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ether3&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">20&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ether4</code></div></div></td></tr></tbody></table>

## 症状

- 流量在不同的VLAN之间被转发
- 红色警告："有pvid的端口被添加到无标记组，可能会导致问题，考虑添加一个单独的VLAN条目"。

## 解决方案 

当使用 pvid 属性配置了访问端口时，它们会被动态地添加到适当的 VLAN 条目中。在创建一个具有多个VLAN或VLAN范围的静态VLAN条目后，具有匹配的pvid的无标记访问端口也被包括在同一VLAN组或范围内。使用一个配置行定义大量的VLAN可能是有用的，但在配置接入端口时应格外小心。对于这个例子，应该创建单独的VLAN条目。

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge vlan</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">tagged</code><code class="ros plain">=ether2</code> <code class="ros value">untagged</code><code class="ros plain">=ether3</code> <code class="ros value">vlan-ids</code><code class="ros plain">=10</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">tagged</code><code class="ros plain">=ether2</code> <code class="ros value">untagged</code><code class="ros plain">=ether4</code> <code class="ros value">vlan-ids</code><code class="ros plain">=20</code></div></div></td></tr></tbody></table>

# 主接口的MTU

___

考虑以下情况， 你创建了一个网桥， 并向其添加了一些接口， 还在网桥接口之上创建了一个 VLAN 接口， 但你需要增加 VLAN 接口的 MTU 大小， 以便接收更大的数据包。

## 配置

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=bridge1</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge port</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether1</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether2</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros constants">/interface vlan</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=bridge1</code> <code class="ros value">name</code><code class="ros plain">=VLAN99</code> <code class="ros value">vlan-id</code><code class="ros plain">=99</code></div></div></td></tr></tbody></table>

## 问题

当你试图增加VLAN接口的MTU大小时，你会收到一个错误：RouterOS **无法设置MTU**。这可能发生在你试图设置MTU大于L2MTU的时候。在这种情况下，需要增加所有从属接口上的 L2MTU 大小，这将更新桥接接口上的 L2MTU 大小。之后，你就可以在 VLAN 接口上设置更大的 MTU。这个原则也适用于绑定接口。只有当所有物理从属接口都设置了适当的 L2MTU 时，才能在 VLAN、MPLS、VPLS、Bonding 等接口上增加 MTU。

## 症状

下面可能是错误配置造成的症状列表。

- 不能改变MTU

## 解决方案

在改变主接口的MTU之前，增加从属接口上的L2MTU。

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface ethernet</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">ether1,ether2 </code><code class="ros value">l2mtu</code><code class="ros plain">=9018</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/interface vlan</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">VLAN99 </code><code class="ros value">mtu</code><code class="ros plain">=9000</code></div></div></td></tr></tbody></table>

# MTU矛盾的地方

___

Consider the following scenario, you have multiple devices in your network, most of them are used as a switch/bridge in your network and there are certain endpoints that are supposed to receive and process traffic. To decrease the overhead in your network, you have decided to increase the MTU size so you set a larger MTU size on both endpoints, but you start to notice that some packets are being dropped.

![](https://help.mikrotik.com/docs/download/attachments/19136718/MTU.png?version=2&modificationDate=1618319477879&api=v2)

## Configuration

In this case, both endpoints can be any type of device, we will assume that they are both Linux servers that are supposed to transfer a large amount of data. In such a scenario, you would have probably set interface MTU to 9000 on **ServerA** and **ServerB a**nd on your **Switch** you have probably have set something similar to this:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=bridge1</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge port</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=ether1</code> <code class="ros value">bridge</code><code class="ros plain">=bridge1</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=ether2</code> <code class="ros value">bridge</code><code class="ros plain">=bridge1</code></div></div></td></tr></tbody></table>

## Problem

This is a very simplified problem, but in larger networks, this might not be very easy to detect. For instance, ping might be working since a generic ping packet will be 70 bytes long (14 bytes for Ethernet header, 20 bytes for IPv4 header, 8 bytes for ICMP header, 28 bytes for ICMP payload), but data transfer might not work properly. The reason why some packets might not get forwarded is that MikroTik devices running RouterOS by default has MTU set to 1500 and L2MTU set to something around 1580 bytes (depends on the device), but the Ethernet interface will silently drop anything that does not fit into the L2MTU size. Note that the L2MTU parameter is not relevant to x86 or CHR devices. For a device that is only supposed to forward packets, there is no need to increase the MTU size, it is only required to increase the L2MTU size, RouterOS will not allow you to increase the MTU size that is larger than the L2MTU size. If you require the packet to be received on the interface and the device needs to process this packet rather than just forwarding it, for example, in the case of routing, then it is required to increase the L2MTU and the MTU size, but you can leave the MTU size on the interface to the default value if you are using only IP traffic (that supports packet fragmentation) and don't mind that packets are being fragmented. You can use the ping utility to make sure that all devices are able to forward jumbo frames:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/</code><code class="ros functions">ping </code><code class="ros plain">192.168.88.1 </code><code class="ros value">size</code><code class="ros plain">=9000</code> <code class="ros plain">do-not-fragment</code></div></div></td></tr></tbody></table>

Remember that the L2MTU and MTU size needs to be larger or equal to the ping packet size on the device from which and to which you are sending a ping packet since ping (ICMP) is IP traffic that is sent out from an interface over Layer3.

## Symptoms

Below is a list of possible symptoms that might be a result of this kind of misconfiguration:

- Web pages are not able to load up, but ping works properly;
- Tunnels dropping traffic;
- Specific protocols are broken;
- Large packet loss;

## Solution

Increase the L2MTU size on your **Switch**:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface ethernet</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">ether1,ether2 </code><code class="ros value">l2mtu</code><code class="ros plain">=9000</code></div></div></td></tr></tbody></table>

In case your traffic is encapsulated (VLAN, VPN, MPLS, VPLS, or other), then you might need to consider setting an even larger L2MTU size. In this scenario, it is not needed to increase the MTU size for the reason described above.

Full frame MTU is not the same as L2MTU. L2MTU size does not include the Ethernet header (14 bytes) and the CRC checksum (FCS) field. The FCS field is stripped by the Ethernet's driver and RouterOS will never show the extra 4 bytes to any packet. For example, if you set MTU and L2MTU to 9000, then the full-frame MTU is 9014 bytes long, this can also be observed when sniffing packets with "`/tool sniffer quick"` command.

# Bridge and reserved MAC addresses

___

Consider the following scenario, you want to transparently bridge two network segments together, either those are tunnel interfaces like EoIP, Wireless interfaces, Ethernet interface, or any other kind of interfaces that can be added to a bridge. Such a setup allows you to seamlessly connect two devices together like there was only a physical cable between them, this is sometimes called a **transparent bridge** from **DeviceA** to **DeviceB**.

## Configuration

For both devices **DeviceA** and **DeviceB** there should be a very similar configuration.

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=bridge1</code> <code class="ros value">protocol-mode</code><code class="ros plain">=rstp</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge port</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=ether1</code> <code class="ros value">bridge</code><code class="ros plain">=bridge1</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=eoip1</code> <code class="ros value">bridge</code><code class="ros plain">=bridge1</code></div></div></td></tr></tbody></table>

## Problem

Both devices are able to communicate with each other, but some protocols do not work properly. The reason is that as soon as you use any STP variant (STP, RSTP, MSTP), you make the bridge compliant with IEEE 802.1D and IEEE 802.1Q, these standards recommend that packets that are destined to **01:80:C2:00:00:0X** should **NOT** be forwarded. In cases where there are only 2 ports added to a bridge (R/M)STP should not be used since a loop cannot occur from 2 interfaces and if a loop does occur, the cause is elsewhere and should be fixed on a different bridge. Since (R/M)STP is not needed in transparent bridge setups, it can be disabled. As soon as (R/M)STP is disabled, the RouterOS bridge is not compliant with IEEE 802.1D and IEEE 802.1Q and therefore will forward packets that are destined to **01:80:C2:00:00:0X**.

## Symptoms

Below is a list of possible symptoms that might be a result of this kind of misconfiguration:

- LLDP neighbors not showing up;
- 802.1x authentication (dot1x) not working;
- LACP interface not passing traffic;

## Solution

Since RouterOS v6.43 it is possible to partly disable compliance with IEEE 802.1D and IEEE 802.1Q, this can be done by changing the bridge protocol mode.

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">bridge1 </code><code class="ros value">protocol-mode</code><code class="ros plain">=none</code></div></div></td></tr></tbody></table>

The IEEE 802.1x standard is meant to be used between a switch and a client directly. If it is possible to connect a device between the switch and the client, then this creates a security threat. For this reason, it is not recommended to disable the compliance with IEEE 802.1D and IEEE 802.1Q, but rather design a proper network topology.

# Bonding between Wireless links

___

Consider the following scenario, you have set up multiple Wireless links and to achieve maximum throughput and yet to achieve redundancy you have decided to place Ethernet interfaces into a bond and depending on the traffic that is being forwarded you have chosen a certain bonding mode. This scenario can be applied to any case, where a bonding interface is created between links, that are not directly connected to each other.

![](https://help.mikrotik.com/docs/download/attachments/19136718/Lacp_wlan.png?version=2&modificationDate=1618319504857&api=v2)

## Configuration

The following configuration is relevant to **R1** and **R2**:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bonding</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">mode</code><code class="ros plain">=802.3ad</code> <code class="ros value">name</code><code class="ros plain">=bond1</code> <code class="ros value">slaves</code><code class="ros plain">=ether1,ether2</code> <code class="ros value">transmit-hash-policy</code><code class="ros plain">=layer-2-and-3</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/ip address</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=192.168.1.X/24</code> <code class="ros value">interface</code><code class="ros plain">=bond1</code></div></div></td></tr></tbody></table>

While the following configuration is relevant to **AP1**, **AP2**, **ST1,** and **ST2**, where **X** corresponds to an IP address for each device.

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=bridge1</code> <code class="ros value">protocol-mode</code><code class="ros plain">=none</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge port</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=ether1</code> <code class="ros value">bridge</code><code class="ros plain">=bridge1</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=wlan1</code> <code class="ros value">bridge</code><code class="ros plain">=bridge1</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros constants">/ip address</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=192.168.1.X/24</code> <code class="ros value">interface</code><code class="ros plain">=bridge1</code></div></div></td></tr></tbody></table>

## Problem

While traffic is being forwarded properly between **R1** and **R2**, load balancing, link failover is working properly as well, but devices between **R1** and **R2** are not always accessible or some of them are completely inaccessible (in most cases **AP2** and **ST2** are inaccessible). After examining the problem you might notice that packets do not always get forwarded over the required bonding slave and as a result, never is received by the device you are trying to access. This is a network design and bonding protocol limitation. As soon as a packet needs to be sent out through a bonding interface (in this case you might be trying to send ICMP packets to **AP2** or **ST2**), the bonding interface will create a hash based on the selected bonding mode and transmit-hash-policy and will select an interface, through which to send the packet out, regardless of the destination is only reachable through a certain interface. Some devices will be accessible because the generated hash matches the interface, on which the device is located on, but it might not choose the needed interface as well, which will result in inaccessible device. Only broadcast bonding mode does not have this kind of protocol limitation, but this bonding mode has a very limited use case.

## Symptoms

Below is a list of possible symptoms that might be a result of this kind of misconfiguration:

- Limited connectivity
- Unstable links (in case of balance-rr)

## Solution

Bonding interfaces are not supposed to be connected using in-direct links, but it is still possible to create a workaround. The idea behind this workaround is to find a way to bypass packets being sent out using the bonding interface. There are multiple ways to force a packet not to be sent out using the bonding interface, but essentially the solution is to create new interfaces on top of physical interfaces and add these newly created interfaces to a bond instead of the physical interfaces. One way to achieve this is to create EoIP tunnels on each physical interface, but that creates a huge overhead and will reduce overall throughput. You should create a VLAN interface on top of each physical interface instead, this creates a much smaller overhead and will not impact overall performance noticeably. Here is an example of how **R1** and **R2** should be reconfigured:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface vlan</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=ether1</code> <code class="ros value">name</code><code class="ros plain">=VLAN_ether1</code> <code class="ros value">vlan-id</code><code class="ros plain">=999</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=ether2</code> <code class="ros value">name</code><code class="ros plain">=VLAN_ether2</code> <code class="ros value">vlan-id</code><code class="ros plain">=999</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros constants">/interface bonding</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">mode</code><code class="ros plain">=balance-xor</code> <code class="ros value">name</code><code class="ros plain">=bond1</code> <code class="ros value">slaves</code><code class="ros plain">=VLAN_ether1,VLAN_ether2</code> <code class="ros value">transmit-hash-policy</code><code class="ros plain">=layer-2-and-3</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros constants">/ip address</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=192.168.1.X/24</code> <code class="ros value">interface</code><code class="ros plain">=bond1</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=192.168.11.X/24</code> <code class="ros value">interface</code><code class="ros plain">=ether1</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=192.168.22.X/24</code> <code class="ros value">interface</code><code class="ros plain">=ether2</code></div></div></td></tr></tbody></table>

**AP1** and **ST1** only need updated IP addresses to the correct subnet:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip address</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=192.168.11.X/24</code> <code class="ros value">interface</code><code class="ros plain">=bridge1</code></div></div></td></tr></tbody></table>

Same changes must be applied to **AP2** and **ST2** (make sure to use the correct subnet):

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip address</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=192.168.22.X/24</code> <code class="ros value">interface</code><code class="ros plain">=bridge1</code></div></div></td></tr></tbody></table>

With this approach, you create the least overhead and the least configuration changes are required.

LACP (802.3ad) is not mean to be used in setups, where devices bonding slaves are not directly connected, in this case, it is not recommended to use LACP if there are Wireless links between both routers. LACP requires both bonding slaves to be at the same link speeds, Wireless links can change their rates at any time, which will decrease overall performance and stability. Other bonding modes should be used instead.

# Bandwidth testing

___

Consider the following scenario, you set up a link between two devices, this can be any link, an Ethernet cable, a wireless link, a tunnel or any other connection. You decide that you want to test the link's bandwidth, but for convenience reasons, you decide to start testing the link with the same devices that are running the link.

![](https://help.mikrotik.com/docs/download/attachments/19136718/Bandwidth_bad.png?version=2&modificationDate=1618319523215&api=v2)

## Problem

As soon as you start [Bandwidth test](https://help.mikrotik.com/docs/display/ROS/Bandwidth+Test) or [Traffic generator](https://wiki.mikrotik.com/wiki/Manual:Tools/Traffic_Generator "Manual:Tools/Traffic Generator") you notice that the throughput is much smaller than expected. For very powerful routers, which should be able to forward many Gigabits per second (Gbps) you notice that only a few Gigabits per second gets forwarded. The reason why this is happening is because of the testing method you are using, you should never test throughput on a router while using the same router for generating traffic because you are adding an additional load on the CPU that reduces the total throughput.

## Symptoms

Below is a list of possible symptoms that might be a result of this kind of misconfiguration:

- Low throughput;
- High CPU usage;

## Solution

Use a proper testing method. Don't use Bandwidth-test to test large capacity links and don't run any tool that generates traffic on the same device you are testing. Design your network properly so you can attach devices that will generate and receive traffic on both ends. If you are familiar with **Iperf**, then this concept should be clear. Remember that in real-world a router or a switch does not generate large amounts of traffic (at least it shouldn't, otherwise, it might indicate an existing security issue), a server/client generates the traffic while a router/switch forwards the traffic (and does some manipulations to the traffic in appropriate cases).

![](https://help.mikrotik.com/docs/download/attachments/19136718/Bandwidth_good.png?version=2&modificationDate=1618319534552&api=v2)

# Bridge split-horizon usage

___

Consider the following scenario, you have a bridge and you need to isolate certain bridge ports from each other. There are options to use a built-in switch chip to isolate certain ports on certain switch chips, you can use bridge firewall rules to prevent certain ports to be able to send any traffic to other ports, you can isolate ports in a PVLAN type of setup using port isolation, but there is also a software-based solution to use bridge split-horizon (which disables hardware offloading on all switch chips).

## Configuration

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=bridge1</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge port</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">horizon</code><code class="ros plain">=1</code> <code class="ros value">hw</code><code class="ros plain">=no</code> <code class="ros value">interface</code><code class="ros plain">=ether1</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">horizon</code><code class="ros plain">=2</code> <code class="ros value">hw</code><code class="ros plain">=no</code> <code class="ros value">interface</code><code class="ros plain">=ether2</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">horizon</code><code class="ros plain">=3</code> <code class="ros value">hw</code><code class="ros plain">=no</code> <code class="ros value">interface</code><code class="ros plain">=ether3</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">horizon</code><code class="ros plain">=4</code> <code class="ros value">hw</code><code class="ros plain">=no</code> <code class="ros value">interface</code><code class="ros plain">=ether4</code></div></div></td></tr></tbody></table>

## Problem

After setting the bridge split-horizon on each port, you start to notice that each port is still able to send data between each other. The reason for this is the misuse of bridge split-horizon. A bridge port is only not able to communicate with ports that are in the same horizon, for example, horizon=1 is not able to communicate with horizon=1, but is able to communicate with horizon=2, horizon=3, and so on.

## Symptoms

Below is a list of possible symptoms that might be a result of this kind of misconfiguration:

- Traffic is being forwarded on different bridge split-horizons

## Solution

Set a proper value as the bridge split-horizon. In case you want to isolate each port from each other (a common scenario for PPPoE setups) and each port is only able to communicate with the bridge itself, then all ports must be in the same bridge split-horizon.

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge port</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">[f] </code><code class="ros value">horizon</code><code class="ros plain">=1</code></div></div></td></tr></tbody></table>

  

Setting all bridge ports in the same bridge split-horizon will result in traffic being only able to reach the bridge interface itself, then packets can only be routed. This is useful when you want other devices to filter out certain traffic. Similar behavior can be achieved using bridge filter rules.

# Unsupported SFP modules

___

Consider the following scenario, you have decided to use optical fiber cables to connect your devices together by using SFP or SFP+ optical modules, but for convenience reasons, you have decided to use SFP optical modules that were available.

## Problem

As soon as you configure your devices to have connectivity on the ports that are using these SFP optical modules, you might notice that either the link is working properly or experiencing random connectivity issues. There are many vendors that manufacture SFP optical modules, but not all vendors strictly follow SFP MSA, SFF, and IEEE 802.3 standards, which can lead to unpredictable compatibility issues, which is a very common issue when using not well known or unsupported SFP optical modules in MikroTik devices.

## Symptoms

Below is a list of possible symptoms that might be a result of this kind of misconfiguration:

- SFP interface does not link up
- Random packet drop
- Unstable link (flapping)
- SFP module not running after a reboot
- SFP module not running after power-cycle
- SFP module running only on one side

## Solution

You should only use supported SFP modules. Always check the [SFP compatibility table](https://wiki.mikrotik.com/wiki/MikroTik_SFP_module_compatibility_table "MikroTik SFP module compatibility table") if you are intending to use SFP modules manufactured by MikroTik. There are other SFP modules that do work with MikroTik devices as well, check the [Supported peripherals table](https://help.mikrotik.com/docs/display/ROS/Peripherals#Peripherals-SFPmodules) to find other SFP modules that have been confirmed to work with MikroTik devices. Some unsupported modules might not be working properly at certain speeds and with auto-negotiation, you might want to try to disable it and manually set a link speed.
