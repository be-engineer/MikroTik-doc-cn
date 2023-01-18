# WMM如何工作

___

WMM的工作原理是将流量分为4个接入类别：background, best effort, video, voice。QoS策略（对接入类别的不同处理）适用于传输的数据包，因此传输设备对不同的数据包进行不同的处理，例如，AP不能控制客户如何传输数据包，客户也不能控制AP如何传输数据包。

Mikrotik AP和客户端根据分配给它们的优先级对数据包进行分类，根据表格（按照WMM规范）。1,2 - background 0,3 - best effort 4,5 - video 6,7 - voice。

为了能够使用多个WMM接入类别，而不仅仅是默认优先级为0的所有数据包的最大努力，必须为这些数据包设置优先级。默认情况下，路由器内的所有数据包（传入的和本地生成的）的优先级为0。

数据包的 "较好 "接入类别不一定意味着它将在所有其他 "较差 "接入类别的数据包之前被发送。WMM的工作原理是通过对每个接入类别（EDCF）进行不同的设置来执行DCF方法，这基本上意味着 "更好 "的接入类别有更高的概率获得介质--启用WMM的站可以被认为是4个站，每个接入类别一个，具有 "更好 "接入类别的站使用的设置使它们更有可能在所有争夺介质时获得发送机会（使用更短的回退超时）。细节可以在802.11e和WMM规范中学习。

WMM支持可以通过`wmm-support`设置来启用。它只适用于B和G频段，其他频段将启用它而不管这个设置。 

# VLAN优先权如何工作

___

VLAN优先级是VLAN标记头中的一个3位字段，称为优先级代码点（PCP），数值在0到7之间。它用于在网桥和交换机上实现QoS。MikroTik设备默认发送的VLAN数据包（本地生成或封装）的优先级为0。 RouterOS网桥转发VLAN标记的数据包时不作任何改变，这意味着收到的具有一定VLAN优先级的VLAN标记数据包将以相同的VLAN优先级离开网桥。唯一的例外是当网桥取消了数据包的标记，在这种情况下，由于VLAN头的缺失，VLAN优先级不会被保留。 

更多细节可以在 IEEE 802.1p 规范中研究。

# 如何设置优先权

___

数据包的优先级可以通过IP防火墙的mangle规则或网桥过滤器/nat规则的`action=set-priority'来设置。优先级可以设置为一个特定的值，也可以使用 "from-ingress "设置从入口处的优先级中获取。入站优先级是在传入数据包上检测到的优先级值，如果有的话。目前，有两个来源的入站优先级--VLAN头中的优先级和通过无线接口收到的WMM数据包的优先级。对于所有其他的数据包，入站优先级是0。

注意，入站优先级值不会自动复制到IP mangle `priority`值，需要设置正确的规则才能做到。

基本上有2种控制优先级的方法--用具有特定匹配器（协议、地址等）的规则分配优先级，或者从入口优先级设置。这两种方法都需要设置正确的规则。

这意味着，如果不可能或不想通过规则对数据包进行分类，网络的配置必须使路由器能够从进入的帧中提取入站优先级。记住，目前有2个来源--数据包中的VLAN标签和收到的WMM数据包。

不要把队列的优先级和分配给数据包的优先级混在一起。队列的优先级是单独工作的，指定了队列的 "重要性"，并且只在特定的队列设置中具有意义。把数据包的优先级看作是某种标记，它通过规则附加到数据包上。还要考虑到这个标记目前只用于通过启用WMM的链路发出的数据包，以及发出的VLAN标记的数据包（无论该数据包是本地标记还是网桥的）。

## 基于特定匹配器设置VLAN或WMM优先级

可以根据 IP mangle 或网桥过滤器/nat 规则中的特定匹配器来改变 VLAN 和 WMM 优先级。在这个例子中，所有传出的 ICMP 数据包都将使用 IP mangle 规则，以 VLAN 或 WMM 优先级发送。

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip firewall mangle</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=set-priority</code> <code class="ros value">chain</code><code class="ros plain">=output</code> <code class="ros value">new-priority</code><code class="ros plain">=2</code> <code class="ros value">protocol</code><code class="ros plain">=icmp</code></div></div></td></tr></tbody></table>

## 自定义优先级映射

有时，某些VLAN或WMM的优先级需要被改变或清除为默认值。我们可以在IP mangle或网桥防火墙/nat规则中使用`ingress-priority`匹配器，只过滤需要的优先级，并使用`new-priority`动作设置将其改为不同的值。例如，通过网桥转发的VLAN标签数据包的优先级为5，需要将其改为0。

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge filter</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=set-priority</code> <code class="ros value">chain</code><code class="ros plain">=forward</code> <code class="ros value">ingress-priority</code><code class="ros plain">=5</code> <code class="ros value">new-priority</code><code class="ros plain">=0</code></div></div></td></tr></tbody></table>

## 在网桥内将 WMM 优先级转换为 VLAN 优先级

当收到一个已经设置了 WMM 优先级的无线数据包时，RouterOS 网桥不会自动将其转换为 VLAN 头。这意味着，收到带有 WMM 优先级的无线数据包，如果被网桥标记为 VLAN，则会以 0 的 VLAN 优先级转发。 然而，我们可以使用带有 `from-ingress` 设置的网桥过滤规则来保持 VLAN 数据包的优先级。例如，我们希望通过 ether2 转发带有 VLAN 10 标头的无线数据包，并保留已经设置的 WMM 优先级（由无线客户端设置）。

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=bridge1</code> <code class="ros value">vlan-filtering</code><code class="ros plain">=yes</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge port</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether2</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=wlan2</code> <code class="ros value">pvid</code><code class="ros plain">=10</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros constants">/interface bridge vlan</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">tagged</code><code class="ros plain">=ether2</code> <code class="ros value">vlan-ids</code><code class="ros plain">=10</code></div><div class="line number8 index7 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros comments"># translates WMM priority to VLAN priority</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros constants">/interface bridge filter</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=set-priority</code> <code class="ros value">chain</code><code class="ros plain">=forward</code> <code class="ros value">new-priority</code><code class="ros plain">=from-ingress</code> <code class="ros value">out-interface</code><code class="ros plain">=ether2</code></div></div></td></tr></tbody></table>

The same situation applies when wireless packets are VLAN tagged by the wireless interface using the `vlan-mode=use-tag` and `vlan-id` settings. You still need to use the same bridge filter rule to translate WMM priority to VLAN priority:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface wireless</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">[ </code><code class="ros functions">find </code><code class="ros value">default-name</code><code class="ros plain">=wlan2</code> <code class="ros plain">] </code><code class="ros value">vlan-mode</code><code class="ros plain">=use-tag</code> <code class="ros value">vlan-id</code><code class="ros plain">=10</code></div><div class="line number3 index2 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros constants">/interface bridge</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=bridge1</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros constants">/interface bridge port</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether2</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=wlan2</code></div><div class="line number9 index8 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros comments"># translates WMM priority to VLAN priority</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge filter</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=set-priority</code> <code class="ros value">chain</code><code class="ros plain">=forward</code> <code class="ros value">new-priority</code><code class="ros plain">=from-ingress</code> <code class="ros value">out-interface</code><code class="ros plain">=ether2</code></div></div></td></tr></tbody></table>

The same principles apply in the other direction. RouterOS does not automatically translate VLAN priority to WMM priority. The same rule `new-priority=from-ingress` can be used to translate VLAN priority to WMM priority. 

RouterOS bridge forwards VLAN tagged packets unaltered, which means that received VLAN tagged packets with a certain VLAN priority will leave the bridge with the same VLAN priority. The only exception is when the bridge untags the packet, in this situation VLAN priority is not preserved due to the missing VLAN header. 

# Priority from DSCP

___

Another way of setting VLAN or WMM priority is by using the DSCP field in the IP header, this can only be done by the IP firewall mangle rule with `new-priority=``from-dscp` or `new-priority=from-dscp-high-3-bits` settings and `set-priority` action property. Note that DSCP in IP header can have values 0-63, but priority only 0-7. When using the `new-priority=``from-dscp` setting, the priority will be 3 low bits of the DSCP value, but when using `new-priority=from-dscp-high-3-bits` the priority will be 3 high bits of DSCP value.

Remember that DSCP can only be accessed on IP packets and DSCP value in IP header should be set somewhere (either by client devices or IP mangle rules).

It is best to set the DSCP value in the IP header of packets on some border router (e.g. main router used for connection to the Internet), based on traffic type e.g. set DSCP value for packets coming from the Internet belonging to SIP connections to 7, and 0 for the rest. This way packets must be marked only in one place. Then all APs on the network can set packet priority from DSCP value with just one rule.

## Set VLAN or WMM priority from DSCP

In this example, the AP device will set WMM priority from DSCP when packets are routed through the wireless interface.

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip firewall mangle</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=set-priority</code> <code class="ros value">chain</code><code class="ros plain">=forward</code> <code class="ros value">new-priority</code><code class="ros plain">=from-dscp</code> <code class="ros value">out-interface</code><code class="ros plain">=wlan2</code></div></div></td></tr></tbody></table>

  

When packets are forwarded through a bridge, it is possible to pass packets through IP mangle rules with `use-ip-firewall=yes` under the bridge settings.

# DSCP from Priority

___

Similarly, the DSCP value can be set if the received packet contains VLAN or WMM priority. This can be achieved with IP mangle rules with `new-dscp=from-priority` or `new-dscp=from-priority-to-high-3-bits` settings and `change-dscp` action property. Note that priority in VLAN or WMM packets can have values 0-7, but DSCP in IP headers are 0-63. When using the `new-dscp=from-priority` setting, the value of priority will set the 3 low bits of the DSCP, but when using `new-dscp=from-priority-to-high-3-bits`  the value of priority will set the 3 high bits of the DSCP. 

However, this setting cannot directly use ingress priority from received VLAN or WMM packets. You first need to set priority using IP mangle or bridge filter/nat rules (ingress priority can be used in this case), and only then apply the DSCP rule.

## Set DSCP from VLAN or WMM priority

In this example, the AP device needs to set DSCP from WMM priority when packets are routed. First, add a rule to set priority, it will be needed for the DSCP rule in order to correctly change the DSCP value. This rule can take priority from ingress. Then add the DSCP rule to change its value.

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip firewall mangle</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=set-priority</code> <code class="ros value">chain</code><code class="ros plain">=prerouting</code> <code class="ros value">in-interface</code><code class="ros plain">=wlan2</code> <code class="ros value">new-priority</code><code class="ros plain">=from-ingress</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=change-dscp</code> <code class="ros value">chain</code><code class="ros plain">=prerouting</code> <code class="ros value">in-interface</code><code class="ros plain">=wlan2</code> <code class="ros value">new-dscp</code><code class="ros plain">=from-priority</code></div></div></td></tr></tbody></table>

When packets are forwarded through a bridge, it is possible to pass packets through IP mangle rules with `use-ip-firewall=yes` under the bridge settings.

# Combining priority setting and handling solutions

___

Complex networks and different situations can be handled by combining different approaches of carrying priority information to ensure QoS and optimize the use of resources, based on the "building blocks" described above. Several suggestions:

-   The fewer number of filter rules in the whole network, the better (faster). Try classifying packets only when necessary, prefer to do that on fast routers as most probably connection tracking will be required.
-   Use DSCP to carry priority information in IP packets forwarded in your network, this way you can use it when needed.
-   Use VLANs where necessary, as they also carry priority information, make sure Ethernet bridges and switches in the way are not clearing priority information in the VLAN tag.
-   Remember that QoS does not improve the throughput of links, it just treats different packets differently, and also that WMM traffic over the wireless link will discriminate regular traffic in the air.

# See also

___

-   [Packet Flow in RouterOS](https://help.mikrotik.com/docs/display/ROS/Packet+Flow+in+RouterOS)
-   [IP mangle](https://help.mikrotik.com/docs/display/ROS/Mangle)
-   [Bridge firewall](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-BridgeFirewall)