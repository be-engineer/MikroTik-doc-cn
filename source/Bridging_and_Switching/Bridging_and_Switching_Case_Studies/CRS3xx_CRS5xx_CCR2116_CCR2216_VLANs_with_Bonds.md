# CRS3xx, CRS5xx, CCR2116, CCR2216带绑定的VLAN

本页将展示如何配置多个交换机以使用绑定接口和基于端口的VLAN，它还将展示一个带有DHCP服务器、VLAN间路由、管理IP和无效VLAN过滤配置的实例。

本文适用于CRS3xx、CRS5xx、CCR2116和CCR2216设备，而不是CRS1xx/CRS2xx。

在这个网络拓扑中，我们将使用两台CRS326-24G-2S+、一台CRS317-1G-16S+和一台CCR1072-1G-8S+，但同样的原则可以应用于任何CRS3xx、CRS5xx系列设备和一台路由器。 

![](https://help.mikrotik.com/docs/download/attachments/139526180/700px-Crs3xx_vlans_with_bonds.jpg?version=1&modificationDate=1659443322300&api=v2)  
  
在这个设置中，SwitchA和SwitchC将把来自端口ether1-ether8的所有流量标记为VLAN ID 10，ether9-ether16标记为VLAN ID 20， ether17-ether24标记为VLAN ID 30。只有当用户从SwitchA或SwitchB上的ether1用标记的流量连接到VLAN ID 99时，才有可能进行管理，从路由器用标记的流量连接到所有设备也是有可能的，这个设置中的SFP+端口将被用作VLAN聚合端口，同时被绑定以创建一个LAG接口。

## 绑定

绑定接口是在需要较大带宽时使用的，这是通过创建一个链路聚合组来实现的，它还为交换机提供硬件自动故障切换和负载平衡。通过添加两个10Gbps的接口进行绑定，你可以将理论带宽限制增加到20Gbps。确保所有绑定的接口都链接到相同的速率。

当使用硬件卸载网桥时，CRS3xx、CRS5xx、CCR2116和CCR2216设备使用内置的交换芯片聚合流量，而不使用CPU资源。为了路由流量，需要一个具有强大CPU的路由器来处理聚合的流量。

要在SwitchA到SwitchB之间以及SwitchC到SwitchB之间从sfp-sfpplus1和sfp-sfpplus2创建一个20Gbps的绑定接口，请在**SwitchA**和**SwitchC**上使用这些命令。

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bonding</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">mode</code><code class="ros plain">=802.3ad</code> <code class="ros value">name</code><code class="ros plain">=bond_1-2</code> <code class="ros value">slaves</code><code class="ros plain">=sfp-sfpplus1,sfp-sfpplus2</code></div></div></td></tr></tbody></table>

要在SwitchB和Router之间创建一个40Gbps的绑定接口，在SwitchA和SwitchC之间创建20Gbps的绑定接口，在**SwitchB**上使用这些命令。

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bonding</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">mode</code><code class="ros plain">=802.3ad</code> <code class="ros value">name</code><code class="ros plain">=bond_1-2</code> <code class="ros value">slaves</code><code class="ros plain">=sfp-sfpplus1,sfp-sfpplus2</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">mode</code><code class="ros plain">=802.3ad</code> <code class="ros value">name</code><code class="ros plain">=bond_3-4</code> <code class="ros value">slaves</code><code class="ros plain">=sfp-sfpplus3,sfp-sfpplus4</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">mode</code><code class="ros plain">=802.3ad</code> <code class="ros value">name</code><code class="ros plain">=bond_5-6-7-8</code> <code class="ros value">slaves</code><code class="ros plain">=sfp-sfpplus5,sfp-sfpplus6,sfp-sfpplus7,sfp-sfpplus8</code></div></div></td></tr></tbody></table>

在我们的案例中，路由器需要一个基于软件的绑定接口，在**路由器**上使用这些命令。

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bonding</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">mode</code><code class="ros plain">=802.3ad</code> <code class="ros value">name</code><code class="ros plain">=bond_1-2-3-4</code> <code class="ros value">slaves</code><code class="ros plain">=sfp-sfpplus1,sfp-sfpplus2,sfp-sfpplus3,sfp-sfpplus4</code></div></div></td></tr></tbody></table>

接口绑定不会创建一个具有更大链接速度的接口。接口绑定创建了一个虚拟接口，可以在多个接口上负载平衡流量。更多细节可以在[LAG接口和负载平衡](https://help.mikrotik.com/docs/display/ROS/Layer2+misconfiguration#Layer2misconfiguration-LAGinterfacesandloadbalancing)页面找到。

## 端口交换

此设置中的所有交换机要求所有使用的端口都被交换到一起。对于绑定，你应该把绑定接口作为一个桥接端口，而不是单独的绑定端口。在**SwitchA**和**SwitchC**上使用这些命令。

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=bridge</code> <code class="ros value">vlan-filtering</code><code class="ros plain">=no</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge port</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">interface</code><code class="ros plain">=ether1</code> <code class="ros value">pvid</code><code class="ros plain">=10</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">interface</code><code class="ros plain">=ether2</code> <code class="ros value">pvid</code><code class="ros plain">=10</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">interface</code><code class="ros plain">=ether3</code> <code class="ros value">pvid</code><code class="ros plain">=10</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">interface</code><code class="ros plain">=ether4</code> <code class="ros value">pvid</code><code class="ros plain">=10</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">interface</code><code class="ros plain">=ether5</code> <code class="ros value">pvid</code><code class="ros plain">=10</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">interface</code><code class="ros plain">=ether6</code> <code class="ros value">pvid</code><code class="ros plain">=10</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">interface</code><code class="ros plain">=ether7</code> <code class="ros value">pvid</code><code class="ros plain">=10</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">interface</code><code class="ros plain">=ether8</code> <code class="ros value">pvid</code><code class="ros plain">=10</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">interface</code><code class="ros plain">=ether9</code> <code class="ros value">pvid</code><code class="ros plain">=20</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">interface</code><code class="ros plain">=ether10</code> <code class="ros value">pvid</code><code class="ros plain">=20</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">interface</code><code class="ros plain">=ether11</code> <code class="ros value">pvid</code><code class="ros plain">=20</code></div><div class="line number15 index14 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">interface</code><code class="ros plain">=ether12</code> <code class="ros value">pvid</code><code class="ros plain">=20</code></div><div class="line number16 index15 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">interface</code><code class="ros plain">=ether13</code> <code class="ros value">pvid</code><code class="ros plain">=20</code></div><div class="line number17 index16 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">interface</code><code class="ros plain">=ether14</code> <code class="ros value">pvid</code><code class="ros plain">=20</code></div><div class="line number18 index17 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">interface</code><code class="ros plain">=ether15</code> <code class="ros value">pvid</code><code class="ros plain">=20</code></div><div class="line number19 index18 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">interface</code><code class="ros plain">=ether16</code> <code class="ros value">pvid</code><code class="ros plain">=20</code></div><div class="line number20 index19 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">interface</code><code class="ros plain">=ether17</code> <code class="ros value">pvid</code><code class="ros plain">=30</code></div><div class="line number21 index20 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">interface</code><code class="ros plain">=ether18</code> <code class="ros value">pvid</code><code class="ros plain">=30</code></div><div class="line number22 index21 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">interface</code><code class="ros plain">=ether19</code> <code class="ros value">pvid</code><code class="ros plain">=30</code></div><div class="line number23 index22 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">interface</code><code class="ros plain">=ether20</code> <code class="ros value">pvid</code><code class="ros plain">=30</code></div><div class="line number24 index23 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">interface</code><code class="ros plain">=ether21</code> <code class="ros value">pvid</code><code class="ros plain">=30</code></div><div class="line number25 index24 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">interface</code><code class="ros plain">=ether22</code> <code class="ros value">pvid</code><code class="ros plain">=30</code></div><div class="line number26 index25 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">interface</code><code class="ros plain">=ether23</code> <code class="ros value">pvid</code><code class="ros plain">=30</code></div><div class="line number27 index26 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">interface</code><code class="ros plain">=ether24</code> <code class="ros value">pvid</code><code class="ros plain">=30</code></div><div class="line number28 index27 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">interface</code><code class="ros plain">=bond_1-2</code></div></div></td></tr></tbody></table>

通过在 **SwitchB** 上使用这些命令，将所有绑定接口添加到 SwitchB 上的一个网桥。

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=bridge</code> <code class="ros value">vlan-filtering</code><code class="ros plain">=no</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge port</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">interface</code><code class="ros plain">=bond_1-2</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">interface</code><code class="ros plain">=bond_3-4</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">interface</code><code class="ros plain">=bond_5-6-7-8</code></div></div></td></tr></tbody></table>

## 管理IP

为了保持对交换机的访问，创建一个管理接口并给它分配一个IP地址是非常有用的。这在更新你的交换机时也非常有用，因为在启用无效的VLAN过滤时，到交换机的这种流量将被阻止。

在**SwitchA**、**SwitchB、**和**SwitchC**上创建一个可路由的VLAN接口。

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface vlan</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=bridge</code> <code class="ros value">name</code><code class="ros plain">=MGMT</code> <code class="ros value">vlan-id</code><code class="ros plain">=99</code></div></div></td></tr></tbody></table>

路由器需要在绑定接口上创建一个可路由的VLAN接口，使用这些命令在**路由器**上创建一个VLAN接口。

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface vlan</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=bond_1-2-3-4</code> <code class="ros value">name</code><code class="ros plain">=MGMT</code> <code class="ros value">vlan-id</code><code class="ros plain">=99</code></div></div></td></tr></tbody></table>

在本指南中，我们将对每个设备使用这些地址。

| 设备    | 地址         |
| ------- | ------------ |
| Router  | 192.168.99.1 |
| SwitchA | 192.168.99.2 |
| SwitchB | 192.168.99.3 |
| SwitchC | 192.168.99.4 |

为VLAN接口上的每个交换机设备添加一个IP地址（将X改为适当的数字）。

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip address</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=192.168.99.X/24</code> <code class="ros value">interface</code><code class="ros plain">=MGMT</code></div></div></td></tr></tbody></table>

不要忘记在交换机设备上添加默认网关并指定一个DNS服务器。

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip route</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">gateway</code><code class="ros plain">=192.168.99.1</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/ip dns</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros value">servers</code><code class="ros plain">=192.168.99.1</code></div></div></td></tr></tbody></table>

在**路由器**上添加IP地址。

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip address</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=192.168.99.1/24</code> <code class="ros value">interface</code><code class="ros plain">=MGMT</code></div></div></td></tr></tbody></table>

## 无效的VLAN过滤

由于SwitchA和SwitchC上的大多数端口都将是接入端口，你可以将所有端口设置为只接受某些类型的数据包，在这种情况下，我们希望SwitchA和SwitchC只接受无标记的数据包，在**SwitchA**和**SwitchC**上使用这些命令。

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge port</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">[ </code><code class="ros functions">find </code><code class="ros plain">] </code><code class="ros value">frame-types</code><code class="ros plain">=admit-only-untagged-and-priority-tagged</code></div></div></td></tr></tbody></table>

在SwitchA和SwitchC上的帧类型有一个例外，在这个设置中，需要从ether1和bonding接口进行管理，这要求可以转发标签流量。在**SwitchA**和**SwitchC**上使用这些命令。

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge port</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">[</code><code class="ros functions">find </code><code class="ros plain">where </code><code class="ros value">interface</code><code class="ros plain">=ether1]</code> <code class="ros value">frame-types</code><code class="ros plain">=admit-all</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">[</code><code class="ros functions">find </code><code class="ros plain">where </code><code class="ros value">interface</code><code class="ros plain">=bond_1-2]</code> <code class="ros value">frame-types</code><code class="ros plain">=admit-only-vlan-tagged</code></div></div></td></tr></tbody></table>

在SwitchB上，只有标签数据包应该被转发，在**SwitchB**上使用这些命令。

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge port</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">[ </code><code class="ros functions">find </code><code class="ros plain">] </code><code class="ros value">frame-types</code><code class="ros plain">=admit-only-vlan-tagged</code></div></div></td></tr></tbody></table>

一个可选的步骤是在网桥接口上设置 `frame-types=admit-only-vlan-tagged`， 以便禁用默认的无标记 VLAN 1 (`pvid=1`)。我们在网桥上使用带标签的 VLAN 来进行管理， 所以没有必要在网桥上接受无标签的流量。在 **SwitchA**, **SwitchB** 和 **SwitchC** 上使用这些命令。

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge </code><code class="ros functions">set </code><code class="ros plain">[</code><code class="ros functions">find </code><code class="ros value">name</code><code class="ros plain">=bridge]</code> <code class="ros value">frame-types</code><code class="ros plain">=admit-only-vlan-tagged</code></div></div></td></tr></tbody></table>

需要设置一个桥接VLAN表。在这个网络设置中，我们需要在ether1-ether8上允许VLAN 10，在ether9-ether16上允许VLAN 20，在ether17-ether24上允许VLAN 30，在bond/_1-2上允许VLAN 10,20,30,99，还有一个特殊情况，就是ether1允许在SwitchA和SwitchC上转发VLAN 99。在**SwitchA**和**SwitchC**上使用这些命令。

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge vlan</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">tagged</code><code class="ros plain">=bond_1-2</code> <code class="ros value">vlan-ids</code><code class="ros plain">=10</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">tagged</code><code class="ros plain">=bond_1-2</code> <code class="ros value">vlan-ids</code><code class="ros plain">=20</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">tagged</code><code class="ros plain">=bond_1-2</code> <code class="ros value">vlan-ids</code><code class="ros plain">=30</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">tagged</code><code class="ros plain">=bridge,bond_1-2,ether1</code> <code class="ros value">vlan-ids</code><code class="ros plain">=99</code></div></div></td></tr></tbody></table>

将 "frame-types "设置为 "admit-all "或 "admit-only-untagged-and-priority-tagged "的网桥端口将被自动添加为 "pvid "VLAN的untagged端口。

同样地，需要为SwitchB设置一个桥接VLAN表。在**SwitchB**上使用这些命令。

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge vlan</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">tagged</code><code class="ros plain">=bond_1-2,bond_3-4,bond_5-6-7-8</code> <code class="ros value">vlan-ids</code><code class="ros plain">=10,20,30</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">tagged</code><code class="ros plain">=bond_1-2,bond_3-4,bond_5-6-7-8,bridge</code> <code class="ros value">vlan-ids</code><code class="ros plain">=99</code></div></div></td></tr></tbody></table>

当一切配置完毕后，启用VLAN过滤。在**SwitchA**、**SwitchB、**和**SwitchC**上使用这些命令。

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">bridge </code><code class="ros value">vlan-filtering</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

仔细检查是否正确设置了基于端口的VLAN。如果犯了错误，你可能会丢失对交换机的访问，只有通过重置配置或使用串行控制台才能重新获取。

VLAN过滤在[Bridge VLAN Filtering](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-BridgeVLANFiltering)部分有更多描述。

## VLAN间路由

要创建VLAN间路由，必须在路由器上为每个客户VLAN ID创建VLAN接口，并且必须为其分配一个IP地址。该VLAN接口必须在之前创建的绑定接口上创建。

在**路由器**上使用这些命令。

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface vlan</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=bond_1-2-3-4</code> <code class="ros value">name</code><code class="ros plain">=VLAN10</code> <code class="ros value">vlan-id</code><code class="ros plain">=10</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=bond_1-2-3-4</code> <code class="ros value">name</code><code class="ros plain">=VLAN20</code> <code class="ros value">vlan-id</code><code class="ros plain">=20</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=bond_1-2-3-4</code> <code class="ros value">name</code><code class="ros plain">=VLAN30</code> <code class="ros value">vlan-id</code><code class="ros plain">=30</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros constants">/ip address</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=192.168.10.1/24</code> <code class="ros value">interface</code><code class="ros plain">=VLAN10</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=192.168.20.1/24</code> <code class="ros value">interface</code><code class="ros plain">=VLAN20</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=192.168.30.1/24</code> <code class="ros value">interface</code><code class="ros plain">=VLAN30</code></div></div></td></tr></tbody></table>

这些命令对DHCP服务器来说是必需的。如果不需要VLAN间的路由，但需要在一台路由器上设置DHCP服务器，那么可以使用[Firewall Filter](https://help.mikrotik.com/docs/display/ROS/Filter)来阻止不同子网间的访问。

从RouterOS v7开始，可以使用某些设备上的L3硬件卸载来路由流量。请看更多关于[L3硬件卸载](https://help.mikrotik.com/docs/display/ROS/L3+Hardware+Offloading)的细节。

## DHCP服务器

为了使每个VLAN ID的DHCP服务器工作，必须在先前创建的VLAN接口上设置服务器（每个VLAN ID一个服务器）。最好是每个VLAN ID都有自己的子网和自己的IP池。DNS服务器可以被指定为特定VLAN ID的路由器IP地址，也可以使用一个全局的DNS服务器，但这个地址必须是可达的。

要设置DHCP服务器，请在**路由器**上使用这些命令。

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip pool</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=VLAN10_POOL</code> <code class="ros value">ranges</code><code class="ros plain">=192.168.10.100-192.168.10.200</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=VLAN20_POOL</code> <code class="ros value">ranges</code><code class="ros plain">=192.168.20.100-192.168.20.200</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=VLAN30_POOL</code> <code class="ros value">ranges</code><code class="ros plain">=192.168.30.100-192.168.30.200</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros constants">/ip dhcp-server</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address-pool</code><code class="ros plain">=VLAN10_POOL</code> <code class="ros value">disabled</code><code class="ros plain">=no</code> <code class="ros value">interface</code><code class="ros plain">=VLAN10</code> <code class="ros value">name</code><code class="ros plain">=VLAN10_DHCP</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address-pool</code><code class="ros plain">=VLAN20_POOL</code> <code class="ros value">disabled</code><code class="ros plain">=no</code> <code class="ros value">interface</code><code class="ros plain">=VLAN20</code> <code class="ros value">name</code><code class="ros plain">=VLAN20_DHCP</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address-pool</code><code class="ros plain">=VLAN30_POOL</code> <code class="ros value">disabled</code><code class="ros plain">=no</code> <code class="ros value">interface</code><code class="ros plain">=VLAN30</code> <code class="ros value">name</code><code class="ros plain">=VLAN30_DHCP</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros constants">/ip dhcp-server network</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=192.168.10.0/24</code> <code class="ros value">dns-server</code><code class="ros plain">=192.168.10.1</code> <code class="ros value">gateway</code><code class="ros plain">=192.168.10.1</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=192.168.20.0/24</code> <code class="ros value">dns-server</code><code class="ros plain">=192.168.20.1</code> <code class="ros value">gateway</code><code class="ros plain">=192.168.20.1</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=192.168.30.0/24</code> <code class="ros value">dns-server</code><code class="ros plain">=192.168.30.1</code> <code class="ros value">gateway</code><code class="ros plain">=192.168.30.1</code></div></div></td></tr></tbody></table>

如果使用的是路由器的DNS服务器，切记要允许远程请求，并确保在路由器上配置了DNS服务器。在**路由器**上使用这些命令。

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip dns</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros value">allow-remote-requests</code><code class="ros plain">=yes</code> <code class="ros value">servers</code><code class="ros plain">=8.8.8.8</code></div></div></td></tr></tbody></table>

当 "允许远程请求 "设置为 "是 "时，确保从外部用防火墙保护你的本地DNS服务器，因为如果你的DNS服务器可以被任何人从互联网上访问，它就可以被用来进行DDoS攻击。

不要忘记创建NAT，假设sfp-sfpplus8被用作WAN端口，在**路由器**上使用这些命令。

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip firewall nat</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=masquerade</code> <code class="ros value">chain</code><code class="ros plain">=srcnat</code> <code class="ros value">out-interface</code><code class="ros plain">=sfp-sfpplus8</code></div></div></td></tr></tbody></table>

## 巨型帧

在该设置中，可以通过启用巨型帧来增加总吞吐量。这通过增加最大传输单元（MTU）来减少数据包的开销。如果你网络中的一个设备不支持巨型帧，那它将不会从更大的MTU中受益。通常情况下，整个网络不支持巨型帧，但在支持巨型帧的设备之间发送数据时，包括路径中的所有交换机，仍然可从中受益。

在这种情况下，如果SwitchA后面的客户和SwitchC后面的客户支持巨型帧，那么启用巨型帧将是有益的。在启用巨型帧之前，请使用此命令确定MAX-L2MTU。

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@SwitchA] &gt; interface </code><code class="ros functions">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: R - RUNNING</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">Columns</code><code class="ros constants">: NAME, TYPE, ACTUAL-MTU, L2MTU, MAX-L2MTU, MAC-ADDRESS</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros comments">#&nbsp;&nbsp; NAME&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; TYPE&nbsp;&nbsp; ACTUAL-MTU&nbsp; L2MTU&nbsp; MAX-L2MTU&nbsp; MAC-ADDRESS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">1 R sfp-sfpplus1&nbsp;&nbsp; ether&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 1500&nbsp;&nbsp; 1584&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 10218&nbsp; 64</code><code class="ros constants">:D1:54:FF:E3:7F</code></div></div></td></tr></tbody></table>

更多信息可以在[MTU手册](https://help.mikrotik.com/docs/display/ROS/MTU+in+RouterOS)页面找到。

当MAX-L2MTU确定后，根据网络上的流量选择MTU大小，在**SwitchA**、**SwitchB**和**SwitchC**使用此命令。

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface ethernet</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">[ </code><code class="ros functions">find </code><code class="ros plain">] </code><code class="ros value">l2mtu</code><code class="ros plain">=10218</code> <code class="ros value">mtu</code><code class="ros plain">=10218</code></div></div></td></tr></tbody></table>

切记在你的客户设备上也要更改MTU，否则，上述设置将没有任何效果。