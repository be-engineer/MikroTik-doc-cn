# WMM和VLAN优先级

___

WMM的工作原理是将流量分为4个接入类别：background, best effort, video, voice。QoS策略（对接入类别的不同处理）适用于传输的数据包，因此传输设备对不同的数据包进行不同的处理，例如，AP不能控制客户如何传输数据包，客户也不能控制AP如何传输数据包。

Mikrotik AP和客户端根据分配给它们的优先级对数据包进行分类，根据表格（按照WMM规范）。1,2 - background 0,3 - best effort 4,5 - video 6,7 - voice。

为了能够使用多个WMM接入类别，而不仅仅是默认优先级为0的所有数据包的最大努力，必须为这些数据包设置优先级。默认情况下，路由器内的所有数据包（传入的和本地生成的）的优先级为0。

数据包的 "较好 "接入类别不一定意味着它将在所有其他 "较差 "接入类别的数据包之前被发送。WMM的工作原理是通过对每个接入类别（EDCF）进行不同的设置来执行DCF方法，这基本上意味着 "更好 "的接入类别有更高的概率获得介质--启用WMM的站可以被认为是4个站，每个接入类别一个，具有 "更好 "接入类别的站使用的设置使它们更有可能在所有争夺介质时获得发送机会（使用更短的回退超时）。细节可以在802.11e和WMM规范中学习。

WMM支持可以通过`wmm-support`设置来启用。它只适用于B和G频段，其他频段将启用它而不管这个设置。 

## VLAN优先权如何工作

___

VLAN优先级是VLAN标记头中的一个3位字段，称为优先级代码点（PCP），数值在0到7之间。它用于在网桥和交换机上实现QoS。MikroTik设备默认发送的VLAN数据包（本地生成或封装）的优先级为0。 RouterOS网桥转发VLAN标记的数据包时不作任何改变，这意味着收到的具有一定VLAN优先级的VLAN标记数据包将以相同的VLAN优先级离开网桥。唯一的例外是当网桥取消了数据包的标记，在这种情况下，由于VLAN头的缺失，VLAN优先级不会被保留。 

更多细节可以在 IEEE 802.1p 规范中研究。

## 如何设置优先权

___

数据包的优先级可以通过IP防火墙的mangle规则或网桥过滤器/nat规则的`action=set-priority'来设置。优先级可以设置为一个特定的值，也可以使用 "from-ingress "设置从入口处的优先级中获取。入站优先级是在传入数据包上检测到的优先级值，如果有的话。目前，有两个来源的入站优先级--VLAN头中的优先级和通过无线接口收到的WMM数据包的优先级。对于所有其他的数据包，入站优先级是0。

注意，入站优先级值不会自动复制到IP mangle `priority`值，需要设置正确的规则才能做到。

基本上有2种控制优先级的方法--用具有特定匹配器（协议、地址等）的规则分配优先级，或者从入口优先级设置。这两种方法都需要设置正确的规则。

这意味着，如果不可能或不想通过规则对数据包进行分类，网络的配置必须使路由器能够从进入的帧中提取入站优先级。记住，目前有2个来源--数据包中的VLAN标签和收到的WMM数据包。

不要把队列的优先级和分配给数据包的优先级混在一起。队列的优先级是单独工作的，指定了队列的 "重要性"，并且只在特定的队列设置中具有意义。把数据包的优先级看作是某种标记，它通过规则附加到数据包上。还要考虑到这个标记目前只用于通过启用WMM的链路发出的数据包，以及发出的VLAN标记的数据包（无论该数据包是本地标记还是网桥的）。

### 基于特定匹配器设置VLAN或WMM优先级

可以根据 IP mangle 或网桥过滤器/nat 规则中的特定匹配器来改变 VLAN 和 WMM 优先级。在这个例子中，所有传出的 ICMP 数据包都将使用 IP mangle 规则，以 VLAN 或 WMM 优先级发送。

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip firewall mangle</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=set-priority</code> <code class="ros value">chain</code><code class="ros plain">=output</code> <code class="ros value">new-priority</code><code class="ros plain">=2</code> <code class="ros value">protocol</code><code class="ros plain">=icmp</code></div></div></td></tr></tbody></table>

### 自定义优先级映射

有时，某些VLAN或WMM的优先级需要被改变或清除为默认值。我们可以在IP mangle或网桥防火墙/nat规则中使用`ingress-priority`匹配器，只过滤需要的优先级，并使用`new-priority`动作设置将其改为不同的值。例如，通过网桥转发的VLAN标签数据包的优先级为5，需要将其改为0。

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge filter</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=set-priority</code> <code class="ros value">chain</code><code class="ros plain">=forward</code> <code class="ros value">ingress-priority</code><code class="ros plain">=5</code> <code class="ros value">new-priority</code><code class="ros plain">=0</code></div></div></td></tr></tbody></table>

### 在网桥内将 WMM 优先级转换为 VLAN 优先级

当收到一个已经设置了 WMM 优先级的无线数据包时，RouterOS 网桥不会自动将其转换为 VLAN 头。这意味着，收到带有 WMM 优先级的无线数据包，如果被网桥标记为 VLAN，则会以 0 的 VLAN 优先级转发。 然而，我们可以使用带有 `from-ingress` 设置的网桥过滤规则来保持 VLAN 数据包的优先级。例如，我们希望通过 ether2 转发带有 VLAN 10 标头的无线数据包，并保留已经设置的 WMM 优先级（由无线客户端设置）。

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=bridge1</code> <code class="ros value">vlan-filtering</code><code class="ros plain">=yes</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge port</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether2</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=wlan2</code> <code class="ros value">pvid</code><code class="ros plain">=10</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros constants">/interface bridge vlan</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">tagged</code><code class="ros plain">=ether2</code> <code class="ros value">vlan-ids</code><code class="ros plain">=10</code></div><div class="line number8 index7 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros comments"># translates WMM priority to VLAN priority</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros constants">/interface bridge filter</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=set-priority</code> <code class="ros value">chain</code><code class="ros plain">=forward</code> <code class="ros value">new-priority</code><code class="ros plain">=from-ingress</code> <code class="ros value">out-interface</code><code class="ros plain">=ether2</code></div></div></td></tr></tbody></table>

当无线数据包被无线接口用 `vlan-mode=use-tag` 和 `vlan-id` 打上 VLAN 标签时，情况也是如此。仍然需要使用相同的网桥过滤规则来将 WMM 优先级转换为 VLAN 优先级。

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface wireless</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">[ </code><code class="ros functions">find </code><code class="ros value">default-name</code><code class="ros plain">=wlan2</code> <code class="ros plain">] </code><code class="ros value">vlan-mode</code><code class="ros plain">=use-tag</code> <code class="ros value">vlan-id</code><code class="ros plain">=10</code></div><div class="line number3 index2 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros constants">/interface bridge</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=bridge1</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros constants">/interface bridge port</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether2</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=wlan2</code></div><div class="line number9 index8 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros comments"># translates WMM priority to VLAN priority</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge filter</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=set-priority</code> <code class="ros value">chain</code><code class="ros plain">=forward</code> <code class="ros value">new-priority</code><code class="ros plain">=from-ingress</code> <code class="ros value">out-interface</code><code class="ros plain">=ether2</code></div></div></td></tr></tbody></table>

同样的原则也适用于另一个方向。RouterOS不会自动将VLAN优先级转换为WMM优先级。同样的规则`new-priority=from-ingress`可以用来将VLAN优先级转换为WMM优先级。 

RouterOS 网桥转发 VLAN 标记的数据包时，不作任何改变，这意味着收到的具有一定 VLAN 优先级的 VLAN 标记的数据包将以相同的 VLAN 优先级离开网桥。唯一的例外是当网桥取消了数据包的标记，在这种情况下，由于VLAN头的缺失，VLAN优先级不会被保留。

## 来自DSCP的优先级

___

另一种设置VLAN或WMM优先级的方法是使用IP头中的DSCP字段，这只能由IP防火墙的mangle规则来完成，该规则有`new-priority=`from-dscp`或`new-priority=from-dscp-high-3-bits`设置和`set-priority`动作属性。注意，IP头中的DSCP可以有0-63的值，但优先级只有0-7。当使用`new-priority=`from-dscp`设置时，优先级将是DSCP值的3个低位，但当使用`new-priority=from-dscp-high-3-bits`时，优先级将是DSCP值的3个高位。

请记住，DSCP只能在IP数据包上访问，IP头中的DSCP值应该在某处设置（由客户端设备或IP混合规则）。

最好是在一些边界路由器（例如用于连接互联网的主路由器）上，根据流量类型，在数据包的IP头中设置DSCP值，例如，将来自互联网的属于SIP连接的数据包的DSCP值设置为7，其余为0。这样，数据包只在一个地方被标记。然后，网络上的所有AP都可以通过DSCP值设置数据包的优先级，只需一条规则。

### 从DSCP设置VLAN或WMM优先级

在这个例子中，当数据包通过无线接口路由时，AP设备将从DSCP设置WMM优先级。

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip firewall mangle</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=set-priority</code> <code class="ros value">chain</code><code class="ros plain">=forward</code> <code class="ros value">new-priority</code><code class="ros plain">=from-dscp</code> <code class="ros value">out-interface</code><code class="ros plain">=wlan2</code></div></div></td></tr></tbody></table>
  
当数据包通过网桥转发时，可以通过网桥设置下的 `use-ip-firewall=yes` 的 IP 混淆规则来传递数据。

## DSCP 从优先级

___

同样，如果收到的数据包包含 VLAN 或 WMM 优先级，也可以设置 DSCP 值。这可以通过 IP mangle 规则来实现，该规则具有 `new-dscp=from-priority` 或 `new-dscp=from-priority-to-high-3-bits` 设置和 `change-dscp` 动作属性。注意，VLAN或WMM数据包中的优先级可以有0-7的值，但IP头中的DSCP是0-63。当使用`new-dscp=from-priority`设置时，优先级的值将设置DSCP的3个低位，但当使用`new-dscp=from-priority-to-high-3-bits`，优先级的值将设置DSCP的3个高位。

然而，这种设置不能直接使用从收到的VLAN或WMM数据包中的入口优先级。首先需要使用IP mangle或网桥过滤/nat规则设置优先级（在此情况下可以使用入口优先级），然后才能应用DSCP规则。

### 从VLAN或WMM优先级设置DSCP

在这个例子中，当数据包被路由时，AP设备需要从WMM优先级设置DSCP。首先，添加一个规则来设置优先级，为了正确改变DSCP值，DSCP规则需要它。这个规则可以从入口处获得优先权。然后添加DSCP规则来改变其值。

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip firewall mangle</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=set-priority</code> <code class="ros value">chain</code><code class="ros plain">=prerouting</code> <code class="ros value">in-interface</code><code class="ros plain">=wlan2</code> <code class="ros value">new-priority</code><code class="ros plain">=from-ingress</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=change-dscp</code> <code class="ros value">chain</code><code class="ros plain">=prerouting</code> <code class="ros value">in-interface</code><code class="ros plain">=wlan2</code> <code class="ros value">new-dscp</code><code class="ros plain">=from-priority</code></div></div></td></tr></tbody></table>

当数据包通过网桥转发时，可以通过网桥设置下 `use-ip-firewall=yes` 的 IP 混淆规则来传递数据。

## 结合优先级设置和处理的方案

___

复杂的网络和不同的情况可以通过结合不同的承载优先级信息的方法来处理，以确保QoS和优化资源的使用，基于上述的 "构建模块"。有几个建议。

- 整个网络中的过滤规则数量越少越好（越快）。只在必要时对数据包进行分类，最好在快速路由器上这样做，因为很可能需要进行连接跟踪。
- 在网络中转发的IP数据包中使用DSCP来携带优先级信息，这样就可以在需要时使用它。
- 必要时使用VLAN，因为它们也携带优先级信息，确保碍事的以太网桥和交换机不清除VLAN标签中的优先级信息。
- 记住，QoS并不能提高链路的吞吐量，它只是对不同的数据包进行不同的处理，另外，无线链路上的WMM流量会对空中的常规流量进行判别。

## 参考文档

___

- [Packet Flow in RouterOS](https://help.mikrotik.com/docs/display/ROS/Packet+Flow+in+RouterOS)
- [IP mangle](https://help.mikrotik.com/docs/display/ROS/Mangle)
- [Bridge firewall](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-BridgeFirewall)