# CRS3xx, CRS5xx, CCR2116, CCR2216带绑定的VLAN

本页将展示如何配置多个交换机以使用绑定接口和基于端口的VLAN，它还将展示一个带有DHCP服务器、VLAN间路由、管理IP和无效VLAN过滤配置的实例。

本文适用于CRS3xx、CRS5xx、CCR2116和CCR2216设备，而不是CRS1xx/CRS2xx。

在这个网络拓扑中，用两台CRS326-24G-2S+、一台CRS317-1G-16S+和一台CCR1072-1G-8S+，但同样的原则可以应用于任何CRS3xx、CRS5xx系列设备和一台路由器。

![](https://help.mikrotik.com/docs/download/attachments/139526180/700px-Crs3xx_vlans_with_bonds.jpg?version=1&modificationDate=1659443322300&api=v2)
  
在这个设置中，SwitchA和SwitchC将把来自端口ether1-ether8的所有流量标记为VLAN ID 10，ether9-ether16标记为VLAN ID 20， ether17-ether24标记为VLAN ID 30。只有当用户从SwitchA或SwitchB上的ether1用标记的流量连接到VLAN ID 99时，才有可能进行管理，从路由器用标记的流量连接到所有设备也是有可能的，这个设置中的SFP+端口将被用作VLAN聚合端口，同时被绑定以创建一个LAG接口。

## 绑定

绑定接口是在需要较大带宽时使用的，这是通过创建一个链路聚合组来实现的，它还为交换机提供硬件自动故障切换和负载均衡。通过添加两个10Gbps的接口进行绑定，你可以将理论带宽限制增加到20Gbps。确保所有绑定的接口都链接到相同的速率。

当使用硬件卸载网桥时，CRS3xx、CRS5xx、CCR2116和CCR2216设备使用内置的交换芯片聚合流量，而不使用CPU资源。为了路由流量，需要一个具有强大CPU的路由器来处理聚合的流量。

要在SwitchA到SwitchB之间以及SwitchC到SwitchB之间从sfp-sfpplus1和sfp-sfpplus2创建一个20Gbps的绑定接口，请在 **SwitchA** 和 **SwitchC** 上使用这些命令。

```shell
/interface bonding
add mode=802.3ad name=bond_1-2 slaves=sfp-sfpplus1,sfp-sfpplus2

```

要在SwitchB和Router之间创建一个40Gbps的绑定接口，在SwitchA和SwitchC之间创建20Gbps的绑定接口，在 **SwitchB** 上使用这些命令。

```shell
/interface bonding
add mode=802.3ad name=bond_1-2 slaves=sfp-sfpplus1,sfp-sfpplus2
add mode=802.3ad name=bond_3-4 slaves=sfp-sfpplus3,sfp-sfpplus4
add mode=802.3ad name=bond_5-6-7-8 slaves=sfp-sfpplus5,sfp-sfpplus6,sfp-sfpplus7,sfp-sfpplus8

```

在案例中，路由器需要一个基于软件的绑定接口，在 **路由器** 上使用这些命令。

```shell
/interface bonding
add mode=802.3ad name=bond_1-2-3-4 slaves=sfp-sfpplus1,sfp-sfpplus2,sfp-sfpplus3,sfp-sfpplus4

```

接口绑定不会创建一个具有更大链接速度的接口。接口绑定创建了一个虚拟接口，可以在多个接口上负载均衡流量。更多细节可以在 [LAG接口和负载均衡](https://help.mikrotik.com/docs/display/ROS/Layer2+misconfiguration#Layer2misconfiguration-LAGinterfacesandloadbalancing) 页面找到。

## 端口交换

此设置中的所有交换机要求所有使用的端口都被交换到一起。对于绑定，你应该把绑定接口作为一个桥接端口，而不是单独的绑定端口。在 **SwitchA** 和 **SwitchC** 上使用这些命令。

```shell
/interface bridge
add name=bridge vlan-filtering=no
/interface bridge port
add bridge=bridge interface=ether1 pvid=10
add bridge=bridge interface=ether2 pvid=10
add bridge=bridge interface=ether3 pvid=10
add bridge=bridge interface=ether4 pvid=10
add bridge=bridge interface=ether5 pvid=10
add bridge=bridge interface=ether6 pvid=10
add bridge=bridge interface=ether7 pvid=10
add bridge=bridge interface=ether8 pvid=10
add bridge=bridge interface=ether9 pvid=20
add bridge=bridge interface=ether10 pvid=20
add bridge=bridge interface=ether11 pvid=20
add bridge=bridge interface=ether12 pvid=20
add bridge=bridge interface=ether13 pvid=20
add bridge=bridge interface=ether14 pvid=20
add bridge=bridge interface=ether15 pvid=20
add bridge=bridge interface=ether16 pvid=20
add bridge=bridge interface=ether17 pvid=30
add bridge=bridge interface=ether18 pvid=30
add bridge=bridge interface=ether19 pvid=30
add bridge=bridge interface=ether20 pvid=30
add bridge=bridge interface=ether21 pvid=30
add bridge=bridge interface=ether22 pvid=30
add bridge=bridge interface=ether23 pvid=30
add bridge=bridge interface=ether24 pvid=30
add bridge=bridge interface=bond_1-2

```

通过在 **SwitchB** 上使用这些命令，将所有绑定接口添加到 SwitchB 上的一个网桥。

```shell
/interface bridge
add name=bridge vlan-filtering=no
/interface bridge port
add bridge=bridge interface=bond_1-2
add bridge=bridge interface=bond_3-4
add bridge=bridge interface=bond_5-6-7-8

```

## 管理IP

为了保持对交换机的访问，创建一个管理接口并给它分配一个IP地址是非常有用的。这在更新你的交换机时也非常有用，因为在启用无效的VLAN过滤时，到交换机的这种流量将被阻止。

在 **SwitchA** 、**SwitchB、** 和 **SwitchC** 上创建一个可路由的VLAN接口。

```shell
/interface vlan
add interface=bridge name=MGMT vlan-id=99

```

路由器需要在绑定接口上创建一个可路由的VLAN接口，使用这些命令在 **路由器** 上创建一个VLAN接口。

```shell
/interface vlan
add interface=bond_1-2-3-4 name=MGMT vlan-id=99

```

在本指南中对每个设备使用这些地址。

| 设备    | 地址         |
| ------- | ------------ |
| Router  | 192.168.99.1 |
| SwitchA | 192.168.99.2 |
| SwitchB | 192.168.99.3 |
| SwitchC | 192.168.99.4 |

为VLAN接口上的每个交换机设备添加一个IP地址（将X改为适当的数字）。

```shell
/ip address
add address=192.168.99.X/24 interface=MGMT

```

不要忘记在交换机设备上添加默认网关并指定一个DNS服务器。

```shell
/ip route
add gateway=192.168.99.1
/ip dns
set servers=192.168.99.1

```

在 **路由器** 上添加IP地址。

```shell
/ip address
add address=192.168.99.1/24 interface=MGMT

```

## 无效的VLAN过滤

由于SwitchA和SwitchC上的大多数端口都将是接入端口，你可以将所有端口设置为只接受某些类型的数据包，在这种情况下，我们希望SwitchA和SwitchC只接受无标记的数据包，在 **SwitchA** 和 **SwitchC** 上使用这些命令。

```shell
/interface bridge port
set [ find ] frame-types=admit-only-untagged-and-priority-tagged

```

在SwitchA和SwitchC上的帧类型有一个例外，在这个设置中，需要从ether1和bonding接口进行管理，这要求可以转发标签流量。在 **SwitchA** 和 **SwitchC** 上使用这些命令。

```shell
/interface bridge port
set [find where interface=ether1] frame-types=admit-all
set [find where interface=bond_1-2] frame-types=admit-only-vlan-tagged

```

在SwitchB上，只有标签数据包应该被转发，在 **SwitchB** 上使用这些命令。

```shell
/interface bridge port
set [ find ] frame-types=admit-only-vlan-tagged

```

一个可选的步骤是在网桥接口上设置 `frame-types=admit-only-vlan-tagged`， 以便禁用默认的无标记 VLAN 1 (`pvid=1`)。在网桥上用带标签的 VLAN 来进行管理， 所以没有必要在网桥上接受无标签的流量。在  **SwitchA**, **SwitchB** 和 **SwitchC** 上使用这些命令。

```shell
/interface bridge set [find name=bridge] frame-types=admit-only-vlan-tagged

```

需要设置一个桥接VLAN表。在这个网络设置中，要在ether1-ether8上允许VLAN 10，在ether9-ether16上允许VLAN 20，在ether17-ether24上允许VLAN 30，在bond/_1-2上允许VLAN 10,20,30,99，还有一个特殊情况，就是ether1允许在SwitchA和SwitchC上转发VLAN 99。在 **SwitchA** 和 **SwitchC** 上使用这些命令。

```shell
/interface bridge vlan
add bridge=bridge tagged=bond_1-2 vlan-ids=10
add bridge=bridge tagged=bond_1-2 vlan-ids=20
add bridge=bridge tagged=bond_1-2 vlan-ids=30
add bridge=bridge tagged=bridge,bond_1-2,ether1 vlan-ids=99

```

将 "frame-types "设置为 "admit-all "或 "admit-only-untagged-and-priority-tagged "的网桥端口将被自动添加为 "pvid "VLAN的untagged端口。

同样地，需要为SwitchB设置一个桥接VLAN表。在 **SwitchB** 上使用这些命令。

```shell
/interface bridge vlan
add bridge=bridge tagged=bond_1-2 vlan-ids=10
add bridge=bridge tagged=bond_1-2 vlan-ids=20
add bridge=bridge tagged=bond_1-2 vlan-ids=30
add bridge=bridge tagged=bridge,bond_1-2,ether1 vlan-ids=99

```

当一切配置完毕后，启用VLAN过滤。在 **SwitchA**、**SwitchB、** 和 **SwitchC** 上使用这些命令。

```shell
/interface bridge
set bridge vlan-filtering=yes

```

仔细检查是否正确设置了基于端口的VLAN。如果犯了错误，你可能会丢失对交换机的访问，只有通过重置配置或使用串行控制台才能重新获取。

VLAN过滤在 [Bridge VLAN Filtering](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-BridgeVLANFiltering) 部分有更多描述。

## VLAN间路由

要创建VLAN间路由，必须在路由器上为每个客户VLAN ID创建VLAN接口，并且必须为其分配一个IP地址。该VLAN接口必须在之前创建的绑定接口上创建。

在 **路由器** 上使用这些命令。

```shell
/interface vlan
add interface=bond_1-2-3-4 name=VLAN10 vlan-id=10
add interface=bond_1-2-3-4 name=VLAN20 vlan-id=20
add interface=bond_1-2-3-4 name=VLAN30 vlan-id=30
/ip address
add address=192.168.10.1/24 interface=VLAN10
add address=192.168.20.1/24 interface=VLAN20
add address=192.168.30.1/24 interface=VLAN30

```

这些命令对DHCP服务器来说是必需的。如果不需要VLAN间的路由，但需要在一台路由器上设置DHCP服务器，那么可以使用 [Firewall Filter](https://help.mikrotik.com/docs/display/ROS/Filter) 来阻止不同子网间的访问。

从RouterOS v7开始，可以使用某些设备上的L3硬件卸载来路由流量。请看更多关于 [L3硬件卸载](https://help.mikrotik.com/docs/display/ROS/L3+Hardware+Offloading) 的细节。

## DHCP服务器

为了使每个VLAN ID的DHCP服务器工作，必须在先前创建的VLAN接口上设置服务器（每个VLAN ID一个服务器）。最好是每个VLAN ID都有自己的子网和自己的IP池。DNS服务器可以被指定为特定VLAN ID的路由器IP地址，也可以使用一个全局的DNS服务器，但这个地址必须是可达的。

要设置DHCP服务器，请在 **路由器** 上使用这些命令。

```shell
/ip pool
add name=VLAN10_POOL ranges=192.168.10.100-192.168.10.200
add name=VLAN20_POOL ranges=192.168.20.100-192.168.20.200
add name=VLAN30_POOL ranges=192.168.30.100-192.168.30.200
/ip dhcp-server
add address-pool=VLAN10_POOL disabled=no interface=VLAN10 name=VLAN10_DHCP
add address-pool=VLAN20_POOL disabled=no interface=VLAN20 name=VLAN20_DHCP
add address-pool=VLAN30_POOL disabled=no interface=VLAN30 name=VLAN30_DHCP
/ip dhcp-server network
add address=192.168.10.0/24 dns-server=192.168.10.1 gateway=192.168.10.1
add address=192.168.20.0/24 dns-server=192.168.20.1 gateway=192.168.20.1
add address=192.168.30.0/24 dns-server=192.168.30.1 gateway=192.168.30.1

```

如果使用的是路由器的DNS服务器，切记要允许远程请求，并确保在路由器上配置了DNS服务器。在 **路由器** 上使用这些命令。

```shell
/ip dns
set allow-remote-requests=yes servers=8.8.8.8

```

当 "允许远程请求 "设置为 "是 "时，确保从外部用防火墙保护你的本地DNS服务器，因为如果你的DNS服务器可以被任何人从互联网上访问，它就可以被用来进行DDoS攻击。

不要忘记创建NAT，假设sfp-sfpplus8被用作WAN端口，在 **路由器** 上使用这些命令。

```shell
/ip firewall nat
add action=masquerade chain=srcnat out-interface=sfp-sfpplus8

```

## 巨型帧

在该设置中，可以通过启用巨型帧来增加总吞吐量。这通过增加最大传输单元（MTU）来减少数据包的开销。如果你网络中的一个设备不支持巨型帧，那它将不会从更大的MTU中受益。通常情况下，整个网络不支持巨型帧，但在支持巨型帧的设备之间发送数据时，包括路径中的所有交换机，仍然可从中受益。

在这种情况下，如果SwitchA后面的客户和SwitchC后面的客户支持巨型帧，那么启用巨型帧将是有益的。在启用巨型帧之前，请使用此命令确定MAX-L2MTU。

```shell
[admin@SwitchA] > interface print
Flags: R - RUNNING
Columns: NAME, TYPE, ACTUAL-MTU, L2MTU, MAX-L2MTU, MAC-ADDRESS
 #   NAME           TYPE   ACTUAL-MTU  L2MTU  MAX-L2MTU  MAC-ADDRESS     
 1 R sfp-sfpplus1   ether        1500   1584      10218  64:D1:54:FF:E3:7F

```

更多信息可以在 [MTU手册](https://help.mikrotik.com/docs/display/ROS/MTU+in+RouterOS) 页面找到。

当MAX-L2MTU确定后，根据网络上的流量选择MTU大小，在 **SwitchA**、**SwitchB** 和 **SwitchC** 使用此命令。

```shell
/interface ethernet
set [ find ] l2mtu=10218 mtu=10218

```

切记在客户设备上也要更改MTU，否则，上述设置将没有任何效果。
