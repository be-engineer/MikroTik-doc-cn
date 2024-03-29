# CRS1xx/2xx系列交换机实例

___

Cloud Router Switch功能的基本使用案例和配置实例。

本文适用于CRS1xx和CRS2xx系列交换机，不适用于CRS3xx系列交换机。对于CRS3xx系列设备，请阅读 [CRS3xx、CRS5xx系列交换机和CCR2116、CCR2216](https://help.mikrotik.com/docs/display/ROS/CRS3xx%2C+CRS5xx%2C+CCR2116%2C+CCR2216+switch+chip+features) 手册。

## 端口交换

___

为了在CRS1xx/2xx系列交换机上设置端口交换，请查看 [网桥硬件卸载](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-BridgeHardwareOffloading) 页面。

可以通过使用启用了硬件卸载的多个网桥来创建多个孤立的交换机组，这只在CRS1xx/2xx系列交换机上可以实现。对于更复杂的设置（例如，VLAN过滤），你应该使用端口隔离功能来代替。

## 管理访问配置

___

一般来说，交换机只应该使用内置的交换芯片来转发数据包，但出于安全考虑，不允许对设备本身进行访问。使用设备的串口进行管理访问是可以的，在大多数情况下，不希望使用这样的访问方式，使用IP地址访问更合适。在这种情况下，需要配置管理访问。

在所有类型的管理访问中，都假定端口必须被交换到一起，使用下面的命令将所需的端口交换到一起。

```shell
/interface bridge
add name=bridge1
/interface bridge port
add bridge=bridge1 interface=ether2 hw=yes
add bridge=bridge1 interface=ether3 hw=yes
add bridge=bridge1 interface=ether4 hw=yes
add bridge=bridge1 interface=ether5 hw=yes

```

还应该给网桥接口分配一个 IP 地址，这样设备就可以用 IP 地址访问了（设备也可以用 MAC 地址访问）。

```shell
/ip address
add address=192.168.88.1/24 interface=bridge1

```

## 未标记的

如果未启用无效VLAN过滤，则允许从任何端口使用有标记或无标记（**VLAN 0**）流量对设备进行管理访问，但这不是一个好的做法，可能导致安全问题，并在某些情况下导致设备的CPU过载（最常见的是广播类型的流量）。

如果打算使用无效的VLAN过滤（应该这样做），那么要访问的交换机端口必须添加到VLAN表中，以获得未标记的（**VLAN 0**）流量，例如如果想从 **ether2** 访问交换机。

```shell
/interface ethernet switch vlan
add vlan-id=0 ports=ether2,switch1-cpu

```

## 标签

只允许被标记的流量通过特定的端口对设备进行管理访问是一个更好的做法。例如，如果只允许 **VLAN99** 通过 **ether2** 访问设备，应该首先在VLAN表中添加一个项，允许选定的端口和CPU端口（**switch1-cpu**）转发选定的VLAN ID，由此启用管理访问。

```shell
/interface ethernet switch vlan
add ports=ether2,switch1-cpu vlan-id=99

```

从CPU发出的数据包，例如，PING回复将没有VLAN标签，为了解决这个问题，需要指定哪些端口应该总是为特定的VLAN ID发出带有VLAN标签的数据包。

```shell
/interface ethernet switch egress-vlan-tag
add tagged-ports=ether2,switch1-cpu vlan-id=99

```

在设置了有效的VLAN99配置后，可以启用未知/无效VLAN过滤，这将禁止通过与VLAN表中指定的不同端口进行管理访问。

```shell
/interface ethernet switch
set drop-if-invalid-or-src-port-not-member-of-vlan-on-ports=ether2,ether3,ether4,ether5

```

在这个例子中，VLAN99 将被用来访问设备，必须在网桥上创建一个 VLAN 接口，并为其分配一个 IP 地址。

```shell
/interface vlan
add interface=bridge1 name=MGMT vlan-id=99
/ip address
add address=192.168.99.1/24 interface=MGMT

```

## VLAN

___

建议在配置VLAN前接上串行控制台电缆并进行测试，因为可能会失去CPU和连接端口的通信。

由于学习了MAC地址，有些更改可能需要一些时间才能生效。在这种情况下，刷新单播转发数据库会有帮助。 `/interface ethernet switch unicast-fdb flush`.

多个硬件卸载网桥配置被设计为快速和简单的端口隔离解决方案，但它限制了CRS交换机芯片所支持的部分VLAN功能。对于高级配置，在CRS交换机芯片内为所有端口使用一个网桥，配置VLAN，用端口隔离配置文件配置隔离端口组。

## 基于端口的VLAN

对于CRS3xx系列设备，必须使用桥接VLAN过滤，可以在 [桥接VLAN过滤](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-BridgeVLANFiltering) 部分阅读更多信息。

### 示例 1 (主干和接入端口)

![](https://help.mikrotik.com/docs/download/attachments/103841836/access_ports.png?version=1&modificationDate=1642165965260&api=v2)

将所需的端口交换到一起。

```shell
/interface bridge
add name=bridge1
/interface bridge port
add bridge=bridge1 interface=ether2 hw=yes
add bridge=bridge1 interface=ether6 hw=yes
add bridge=bridge1 interface=ether7 hw=yes
add bridge=bridge1 interface=ether8 hw=yes

```

指定交换机必须对每个接入端口的未标记（VLAN0）流量设置的VLAN ID。

```shell
/interface ethernet switch ingress-vlan-translation
add ports=ether6 customer-vid=0 new-customer-vid=200
add ports=ether7 customer-vid=0 new-customer-vid=300
add ports=ether8 customer-vid=0 new-customer-vid=400

```

当在 `/interface ethernet switch ingress-vlan-translation` 下创建项目时，交换芯片将在指定端口的入站帧上添加一个VLAN标签。要在同一端口上为出站帧移除VLAN标签，应该在指定有标签的端口上为同一VLAN ID创建 `/interface ethernet switch egress-vlan-tag` 项。如果一个特定的VLAN只在接入端口之间转发，`/interface ethernet switch egress-vlan-tag` 项仍应该在没有任何标记的端口下创建。另一个选择是在 `/interface ethernet switch egress-vlan-translation` 菜单下创建额外的项，以设置未标记的（VLAN0）流量。

你还必须指定哪些VLAN应该被发送到带VLAN标签的主干端口。使用tagged-ports属性来设置一个聚合端口。

```shell
/interface ethernet switch egress-vlan-tag
add tagged-ports=ether2 vlan-id=200
add tagged-ports=ether2 vlan-id=300
add tagged-ports=ether2 vlan-id=400

```

向VLAN表添加项，为每个端口和每个VLAN ID指定VLAN成员。

```shell
/interface ethernet switch vlan
add ports=ether2,ether6 vlan-id=200
add ports=ether2,ether7 vlan-id=300
add ports=ether2,ether8 vlan-id=400

```

在设置了有效的VLAN配置后，可以启用未知/无效VLAN过滤。

```shell
/interface ethernet switch
set drop-if-invalid-or-src-port-not-member-of-vlan-on-ports=ether2,ether6,ether7,ether8

```

可以同时使用内置的交换芯片和CPU来创建一个交换机-路由器设置，即一个设备同时作为交换机和路由器。可以在 [CRS-Router](https://wiki.mikrotik.com/wiki/Manual:CRS_Router "Manual:CRS Router") 指南中找到配置实例。

### 示例 2 (聚合和混合端口)

![](https://help.mikrotik.com/docs/download/attachments/103841836/hybrid_ports.png?version=1&modificationDate=1642166287658&api=v2)

将所需的端口交换到一起。

```shell
/interface bridge
add name=bridge1
/interface bridge port
add bridge=bridge1 interface=ether2 hw=yes
add bridge=bridge1 interface=ether6 hw=yes
add bridge=bridge1 interface=ether7 hw=yes
add bridge=bridge1 interface=ether8 hw=yes

```

指定交换机必须对每个接入端口的未标记（VLAN0）流量设置VLAN ID。

```shell
/interface ethernet switch ingress-vlan-translation
add ports=ether6 customer-vid=0 new-customer-vid=200
add ports=ether7 customer-vid=0 new-customer-vid=300
add ports=ether8 customer-vid=0 new-customer-vid=400

```

通过指定端口为标签端口，交换机将始终以相应的VLAN ID作为标签数据包发送出去。根据上图添加适当的项。

```shell
/interface ethernet switch egress-vlan-tag
add tagged-ports=ether2,ether7,ether8 vlan-id=200
add tagged-ports=ether2,ether6,ether8 vlan-id=300
add tagged-ports=ether2,ether6,ether7 vlan-id=400

```

向VLAN表添加项，为每个端口和每个VLAN ID指定VLAN成员。

```shell
/interface ethernet switch vlan
add ports=ether2,ether6,ether7,ether8 vlan-id=200 learn=yes
add ports=ether2,ether6,ether7,ether8 vlan-id=300 learn=yes
add ports=ether2,ether6,ether7,ether8 vlan-id=400 learn=yes

```

在设置了有效的VLAN配置后，可以启用未知/无效VLAN过滤。

```shell
/interface ethernet switch
set drop-if-invalid-or-src-port-not-member-of-vlan-on-ports=ether2,ether6,ether7,ether8

```

## 基于协议的VLAN

![](https://help.mikrotik.com/docs/download/attachments/103841836/Protocol-Based.jpg?version=1&modificationDate=1653991328706&api=v2)

将所需的端口交换到一起。

```shell
/interface bridge
add name=bridge1
/interface bridge port
add bridge=bridge1 interface=ether2 hw=yes
add bridge=bridge1 interface=ether6 hw=yes
add bridge=bridge1 interface=ether7 hw=yes
add bridge=bridge1 interface=ether8 hw=yes

```

为IP和ARP协议设置VLAN。

```shell
/interface ethernet switch protocol-based-vlan
add port=ether2 protocol=arp set-customer-vid-for=all new-customer-vid=0
add port=ether6 protocol=arp set-customer-vid-for=all new-customer-vid=200
add port=ether2 protocol=ip set-customer-vid-for=all new-customer-vid=0
add port=ether6 protocol=ip set-customer-vid-for=all new-customer-vid=200

```

为IPX协议设置VLAN。

```shell
/interface ethernet switch protocol-based-vlan
add port=ether2 protocol=ipx set-customer-vid-for=all new-customer-vid=0
add port=ether7 protocol=ipx set-customer-vid-for=all new-customer-vid=300

```

为AppleTalk AARP和AppleTalk DDP协议设置VLAN。

```shell
/interface ethernet switch protocol-based-vlan
add port=ether2 protocol=0x80F3 set-customer-vid-for=all new-customer-vid=0
add port=ether8 protocol=0x80F3 set-customer-vid-for=all new-customer-vid=400
add port=ether2 protocol=0x809B set-customer-vid-for=all new-customer-vid=0
add port=ether8 protocol=0x809B set-customer-vid-for=all new-customer-vid=400

```

## 基于MAC的VLAN

内部基于MAC的VLAN中的所有MAC地址都是哈希值，某些MAC地址可能有相同的哈希值，如果哈希值和已经加载的MAC地址的哈希值相匹配，这会阻止MAC地址被加载到交换芯片中，因此，建议将端口基础VLAN与基于MAC的VLAN结合使用。这是一个硬件限制。

![](https://help.mikrotik.com/docs/download/attachments/103841836/MAC-Based.jpg?version=1&modificationDate=1653991417317&api=v2)

将所需的端口交换到一起。

```shell
/interface bridge
add name=bridge1
/interface bridge port
add bridge=bridge1 interface=ether2 hw=yes
add bridge=bridge1 interface=ether7 hw=yes

```

在接入端口启用基于MAC的VLAN转换。

```shell
/interface ethernet switch port
set ether7 allow-fdb-based-vlan-translate=yes

```

在基于MAC的VLAN表中添加MAC到VLAN的映射项。

```shell
/interface ethernet switch mac-based-vlan
add src-mac=A4:12:6D:77:94:43 new-customer-vid=200
add src-mac=84:37:62:DF:04:20 new-customer-vid=300
add src-mac=E7:16:34:A1:CD:18 new-customer-vid=400

```

在ether2端口上添加VLAN200、VLAN300和VLAN400标记，将其创建为一个VLAN聚合端口。

```shell
/interface ethernet switch egress-vlan-tag
add tagged-ports=ether2 vlan-id=200
add tagged-ports=ether2 vlan-id=300
add tagged-ports=ether2 vlan-id=400

```

此外，在 VLAN 表中添加项，为每个端口指定 VLAN 成员，并启用未知/无效 VLAN 过滤，见下面的例子。这对于在网桥上添加更多接口的网络设置是必需的，因为它允许定义 VLAN 的边界。

## VLAN间路由

![](https://help.mikrotik.com/docs/download/attachments/103841836/vlan_routing.png?version=1&modificationDate=1642167118612&api=v2)

VLAN间路由配置包括两个主要部分--交换芯片的VLAN标记和RouterOS的路由。这种配置可以通过与DHCP服务器、Hotspot、PPP和其他功能相结合，在许多应用中用于每个VLAN。

将所需的端口交换在一起。

```shell
/interface bridge
add name=bridge1
/interface bridge port
add bridge=bridge1 interface=ether6 hw=yes
add bridge=bridge1 interface=ether7 hw=yes
add bridge=bridge1 interface=ether8 hw=yes

```

在CPU端口上为所有VLAN设置VLAN标签，使数据包在被路由之前被标记。

```shell
/interface ethernet switch egress-vlan-tag
add tagged-ports=switch1-cpu vlan-id=200
add tagged-ports=switch1-cpu vlan-id=300
add tagged-ports=switch1-cpu vlan-id=400

```

添加入口VLAN转换规则以确保在接入端口上进行正确的VLAN ID分配。

```shell
/interface ethernet switch ingress-vlan-translation
add ports=ether6 customer-vid=0 new-customer-vid=200
add ports=ether7 customer-vid=0 new-customer-vid=300
add ports=ether8 customer-vid=0 new-customer-vid=400

```

在网桥接口上创建VLAN接口。

```shell
/interface vlan
add name=VLAN200 interface=bridge1 vlan-id=200
add name=VLAN300 interface=bridge1 vlan-id=300
add name=VLAN400 interface=bridge1 vlan-id=400

```

请确保 VLAN 接口是在网桥接口之上而不是在任何物理接口之上创建的。如果 VLAN 接口是在从属接口上创建的， 那么数据包可能无法被正确接收， 路由可能会失败。更详细的信息可以在 [VLAN interface on a slave interface](https://help.mikrotik.com/docs/display/ROS/Layer2+misconfiguration#Layer2misconfiguration-VLANinterfaceonaslaveinterface) 手册页上找到。

在创建的VLAN接口上添加IP地址。这个例子中，三个192.168.x.1地址被添加到VLAN200、VLAN300和VLAN400接口。

```shell
/ip address
add address=192.168.20.1/24 interface=VLAN200
add address=192.168.30.1/24 interface=VLAN300
add address=192.168.40.1/24 interface=VLAN400

```

## 未知/无效的VLAN过滤

VLAN成员资格是在VLAN表中定义的。添加带有VLAN ID和端口的项使该VLAN流量在这些端口上有效。在设置了有效的VLAN配置后，可以启用未知/无效的VLAN过滤。这个VLAN过滤配置例子适用于VLAN间路由设置。

```shell
/interface ethernet switch vlan
add ports=switch1-cpu,ether6 vlan-id=200
add ports=switch1-cpu,ether7 vlan-id=300
add ports=switch1-cpu,ether8 vlan-id=400

```

- 选项1：禁用特定端口上的无效VLAN转发（更常见）。
  
```shell
/interface ethernet switch
set drop-if-invalid-or-src-port-not-member-of-vlan-on-ports=ether2,ether6,ether7,ether8

```

- 选项2：禁用所有端口上的无效VLAN转发。

```shell
/interface ethernet switch
set forward-unknown-vlan=no

```

在单个交换芯片上使用多个网桥，并启用未知/无效的 VLAN 过滤，可能会导致意外的行为。在使用VLAN过滤时，应该始终使用单网桥配置。如果需要端口隔离，则应使用端口隔离功能，而不是使用多个网桥。

## VLAN隧道(Q-in-Q)

这个例子涵盖了一个典型的VLAN隧道使用情况，即服务提供商的设备添加另一个VLAN标签进行独立转发，同时允许客户使用自己的VLAN。

这个例子只包含服务VLAN标记部分。建议在端口上额外设置未知/无效VLAN过滤。

![](https://help.mikrotik.com/docs/download/attachments/103841836/Qinq.jpg?version=1&modificationDate=1653991582909&api=v2)

**CRS-1**。服务提供商网络边缘的第一台交换机必须正确识别端口上来自客户VLAN id的流量，并用入口VLAN转换规则分配新的服务VLAN id。服务提供商VLAN标签的VLAN聚合端口配置在同一个 _egress-vlan-tag_ 表中。和基于端口的基本VLAN配置的主要区别是，CRS交换机芯片必须设置为根据服务（_outer_）VLAN id而不是客户（_inner_）VLAN id进行转发。

```shell
/interface bridge
add name=bridge1
/interface bridge port
add bridge=bridge1 interface=ether1 hw=yes
add bridge=bridge1 interface=ether2 hw=yes
add bridge=bridge1 interface=ether9 hw=yes
 
/interface ethernet switch ingress-vlan-translation
add customer-vid=200 new-service-vid=400 ports=ether1
add customer-vid=300 new-service-vid=500 ports=ether2
 
/interface ethernet switch egress-vlan-tag
add tagged-ports=ether9 vlan-id=400
add tagged-ports=ether9 vlan-id=500
 
/interface ethernet switch
set bridge-type=service-vid-used-as-lookup-vid

```

**CRS-2**。服务提供商网络中的第二台交换机只要求交换的端口按照服务（_outer_）VLAN id而不是客户（_inner_）VLAN id进行转发。

```shell
/interface bridge
add name=bridge1
/interface bridge port
add bridge=bridge1 interface=ether9 hw=yes
add bridge=bridge1 interface=ether10 hw=yes
 
/interface ethernet switch
set bridge-type=service-vid-used-as-lookup-vid

```

**CRS-3**。第三台交换机的配置与CRS-1类似。

- 使用网桥的交换机组中的端口。
- 入站VLAN转换规则，在端口上定义新的服务VLAN分配。
- 用于服务提供商VLAN聚合的标记端口。
- CRS交换机芯片设置为在交换查找中使用服务VLAN ID。

```shell
/interface bridge
add name=bridge1
/interface bridge port
add bridge=bridge1 interface=ether3 hw=yes
add bridge=bridge1 interface=ether4 hw=yes
add bridge=bridge1 interface=ether10 hw=yes
 
/interface ethernet switch ingress-vlan-translation
add customer-vid=200 new-service-vid=400 ports=ether3
add customer-vid=300 new-service-vid=500 ports=ether4
 
/interface ethernet switch egress-vlan-tag
add tagged-ports=ether10 vlan-id=400
add tagged-ports=ether10 vlan-id=500
 
/interface ethernet switch
set bridge-type=service-vid-used-as-lookup-vid

```

## CVID堆叠

可以使用CRS1xx/CRS2xx系列交换机进行CVID堆叠设置。CRS1xx/CRS2xx系列交换机能够根据有两个CVID标签（双CVID标签）的标记数据包的外部标签进行VLAN过滤，这些交换机还能够在现有的CVID标签之上添加另一个CVID标签（CVID堆叠）。例如，在一个设置中，**ether1** 正在接收带有CVID 10的标签数据包，但要求 **ether2** 用另一个标签CVID 20（VLAN10 in VLAN20）发送这些数据包，同时过滤掉任何其他VLAN，配置如下。

将 **ether1** 和 **ether2** 交换到一起。

```shell
/interface bridge
add name=bridge1
/interface bridge port
add bridge=bridge1 interface=ether1 hw=yes
add bridge=bridge1 interface=ether2 hw=yes

```

设置交换机根据服务标签（0x88a8）来过滤VLAN。

```shell
/interface ethernet switch
set bridge-type=service-vid-used-as-lookup-vid

```

为在 **ether1** 上有CVID 10标签的数据包添加一个服务标签SVID 20。

```shell
/interface ethernet switch ingress-vlan-translation
add customer-vid=10 new-service-vid=20 ports=ether1

```

指定 **ether2** 作为SVID 20的标记/聚合端口。

```shell
/interface ethernet switch egress-vlan-tag
add tagged-ports=ether2 vlan-id=20

```

允许 **ether1** 和 **ether2** 转发SVID 20。

```shell
/interface ethernet switch vlan
add ports=ether1,ether2 vlan-id=20

```

在 **ether2** 上将SVID EtherType（0x88a8）覆盖为CVID EtherType（0x8100）。

```shell
/interface ethernet switch port
set ether2 egress-service-tpid-override=0x8100 ingress-service-tpid-override=0x8100

```

启用未知/无效的VLAN过滤。

```shell
/interface ethernet switch
set drop-if-invalid-or-src-port-not-member-of-vlan-on-ports=ether1,ether2

```

由于交换机被设置为根据服务标签查找VLAN ID，而服务标签被不同的EtherType所覆盖，那么VLAN过滤只在数据包的外部标签上进行，内部标签不被检查。

## 镜像

___

![](https://help.mikrotik.com/docs/download/attachments/103841836/Mirroring.jpg?version=1&modificationDate=1653991663872&api=v2)

Cloud Router Switches支持三种类型的镜像。基于端口的镜像可以应用于任何交换机芯片端口，基于VLAN的镜像适用于所有指定的VLAN，与交换芯片端口无关，而基于MAC的镜像则复制从单播转发数据库中配置的端口可到达的特定设备发送或接收的流量。

### 基于端口的镜像

第一个配置将ether5端口设置为镜像0分析端口，用于入站和出站镜像，镜像的流量将被发送到这个端口。基于端口的入站和出站镜像在ether6端口启用。

```shell
/interface ethernet switch
set ingress-mirror0=ether5 egress-mirror0=ether5
 
/interface ethernet switch port
set ether6 ingress-mirror-to=mirror0 egress-mirror-to=mirror0

```

### 基于VLAN的镜像

第二个例子要求端口在一个组中进行交换。镜像配置将ether5端口设置为镜像0分析端口，并将镜像0端口设置为在发生从VLAN镜像时使用。VLAN表项仅对ether2和ether7端口之间的VLAN 300流量启用镜像。

```shell
/interface bridge
add name=bridge1
/interface bridge port
add bridge=bridge1 interface=ether2 hw=yes
add bridge=bridge1 interface=ether7 hw=yes
 
/interface ethernet switch
set ingress-mirror0=ether5 vlan-uses=mirror0
 
/interface ethernet switch vlan
add ports=ether2,ether7 vlan-id=300 learn=yes ingress-mirror=yes

```

### 基于MAC的镜像

第三种配置也需要端口在一个组中进行交换。镜像配置将ether5端口设置为镜像0分析端口，并将镜像0端口设置为发生单播转发数据库的镜像时使用。来自单播转发数据库的项目使来自ether8端口的具有源或目的MAC地址E7:16:34:A1:CD:18的数据包能够被镜像。

```shell
/interface bridge
add name=bridge1
/interface bridge port
add bridge=bridge1 interface=ether2 hw=yes
add bridge=bridge1 interface=ether8 hw=yes
 
/interface ethernet switch
set ingress-mirror0=ether5 fdb-uses=mirror0
 
/interface ethernet switch unicast-fdb
add port=ether8 mirror=yes svl=yes mac-address=E7:16:34:A1:CD:18

```

## 聚合

___

![](https://help.mikrotik.com/docs/download/attachments/103841836/Trunking3.jpg?version=1&modificationDate=1653991953731&api=v2)

Cloud Router Switches中的聚合提供静态链路聚合组，具有硬件自动故障切换和负载均衡功能。目前还不支持IEEE802.3ad和IEEE802.1ax兼容的链路聚合控制协议。最多支持8个聚合组，每个聚合组最多支持8个聚合成员端口。

配置需要一组交换的端口和聚合表中的项目。

```shell
/interface bridge
add name=bridge1 protocol-mode=none
/interface bridge port
add bridge=bridge1 interface=ether2 hw=yes
add bridge=bridge1 interface=ether6 hw=yes
add bridge=bridge1 interface=ether7 hw=yes
add bridge=bridge1 interface=ether8 hw=yes
 
/interface ethernet switch trunk
add name=trunk1 member-ports=ether6,ether7,ether8

```

这个例子还显示了另一端在RouterOS中的正确绑定配置。

```shell
/interface bonding
add name=bonding1 slaves=ether2,ether3,ether4 mode=balance-xor transmit-hash-policy=layer-2-and-3

```

可以在 [CRS VLANs with Trunks](https://wiki.mikrotik.com/wiki/Manual:CRS_VLANs_with_Trunks "Manual:CRS VLANs with Trunks") 页面找到聚合和基于端口的VLAN的工作实例。

网桥(R)STP不知道底层交换机的聚合配置，一些聚合端口可以移动到丢弃或阻塞状态。当聚合成员端口连接到其他网桥时，应该禁用(R)STP或过滤掉集群设备之间的任何BPDU（例如，用ACL规则）。

## 每个端口有限的 MAC 访问

___

禁用MAC学习和配置静态MAC地址，可以控制哪些确切的设备可以与CRS1xx/2xx交换机通信并通过它们通信。

配置需要交换的一组端口，在这些端口上禁用MAC学习，以及静态UFDB项。

```shell
/interface bridge
add name=bridge1
/interface bridge port
add bridge=bridge1 interface=ether2 hw=yes
add bridge=bridge1 interface=ether6 hw=yes learn=no unknown-unicast-flood=no
add bridge=bridge1 interface=ether7 hw=yes learn=no unknown-unicast-flood=no
 
/interface ethernet switch unicast-fdb
add mac-address=4C:5E:0C:00:00:01 port=ether6 svl=yes
add mac-address=D4:CA:6D:00:00:02 port=ether7 svl=yes
 
/interface ethernet switch acl
add action=drop src-mac-addr-state=sa-not-found src-ports=ether6,ether7 table=egress
add action=drop src-mac-addr-state=static-station-move src-ports=ether6,ether7 table=egress

```

CRS1xx/2xx交换机还允许每个端口学习一个动态MAC，以确保只有一个终端用户设备被连接，无论其MAC地址如何。

```shell
/interface ethernet switch port
set ether6 learn-limit=1
set ether7 learn-limit=1

```

## 隔离

___

### 端口级隔离

![](https://help.mikrotik.com/docs/download/attachments/103841836/Port-level-Isolation.jpg?version=1&modificationDate=1653992020849&api=v2)

端口级隔离通常用于私有VLAN。

- 一个或多个上行链路端口在所有用户中共享，用于访问网关或路由器。
- 端口组的隔离端口是为访客准备的。通信只通过上行链路端口。
- 端口组Community 0适用于A部门，允许组内成员之间通过上行链路端口进行通信。
- 端口组Community X是为X部门服务的，允许组内成员之间以及通过上行链路端口进行通信。

Cloud Router Switches使用端口级隔离配置文件来实现私有VLAN。

- 上行链路端口 - 端口级隔离配置文件0
- 隔离的端口--端口级隔离配置文件1
- Community 0端口--端口级隔离配置文件2
- Community X（X<=30）端口--端口级隔离配置文件X

**本例需要一组交换的端口。假设本例中使用的所有端口都在一个交换组中**。

```shell
/interface bridge
add name=bridge1
/interface bridge port
add bridge=bridge1 interface=ether2 hw=yes
add bridge=bridge1 interface=ether6 hw=yes
add bridge=bridge1 interface=ether7 hw=yes
add bridge=bridge1 interface=ether8 hw=yes
add bridge=bridge1 interface=ether9 hw=yes
add bridge=bridge1 interface=ether10 hw=yes

```

端口隔离配置的第一部分是设置上行链路端口 - 为ether2设置一个端口配置文件为0。

```shell
/interface ethernet switch port
set ether2 isolation-leakage-profile-override=0

```

然后继续为所有被隔离的端口设置隔离配置1，并为端口隔离配置1添加通信端口。

```shell
/interface ethernet switch port
set ether5 isolation-leakage-profile-override=1
set ether6 isolation-leakage-profile-override=1
 
/interface ethernet switch port-isolation
add port-profile=1 ports=ether2 type=dst

```

Community 2 和Community 3端口的配置是类似的。

```shell
/interface ethernet switch port
set ether7 isolation-leakage-profile-override=2
set ether8 isolation-leakage-profile-override=2
 
/interface ethernet switch port-isolation
add port-profile=2 ports=ether2,ether7,ether8 type=dst
 
/interface ethernet switch port
set ether9 isolation-leakage-profile-override=3
set ether10 isolation-leakage-profile-override=3
 
/interface ethernet switch port-isolation
add port-profile=3 ports=ether2,ether9,ether10 type=dst

```

### 协议级隔离

![](https://help.mikrotik.com/docs/download/attachments/103841836/Protocol-level-Isolation.jpg?version=1&modificationDate=1653992078245&api=v2)  

CRS交换机上的协议级隔离可以用来增强网络安全。例如，限制用户之间的DHCP流量，只允许它进入受信任的DHCP服务器端口，可以防止DHCP欺骗攻击等安全风险。下面的例子说明了如何在CRS上进行配置。

将所需的端口交换到一起。

```shell
/interface bridge
add name=bridge1
/interface bridge port
add bridge=bridge1 interface=ether1 hw=yes
add bridge=bridge1 interface=ether2 hw=yes
add bridge=bridge1 interface=ether3 hw=yes
add bridge=bridge1 interface=ether4 hw=yes
add bridge=bridge1 interface=ether5 hw=yes

```

为所有 DHCP 客户端端口设置相同的 Community 端口配置文件。Community端口配置文件编号从2到30。

```shell
/interface ethernet switch port
set ether2 isolation-leakage-profile-override=2
set ether3 isolation-leakage-profile-override=2
set ether4 isolation-leakage-profile-override=2
set ether5 isolation-leakage-profile-override=2

```

为选定的Community（2）配置端口隔离/泄漏配置文件，以允许DHCP流量只流向受信任的DHCP服务器所在的端口，注册状态和流量类型属性必须设置为空，以便只对DHCP协议应用限制。

```shell
/interface ethernet switch port-isolation
add port-profile=2 protocol-type=dhcpv4 type=dst forwarding-type=bridged ports=ether1 registration-status="" traffic-type=""

```

## 服务质量 (QoS)

___

**QoS配置方案**

基于MAC的流量调度和整形: [MAC address in UFDB] -> [QoS Group] -> [Priority] -> [Queue] -> [Shaper]

基于VLAN的流量调度和整形: [VLAN id in VLAN table] -> [QoS Group] -> [Priority] -> [Queue] -> [Shaper]

基于协议的流量调度和整形: [Protocol in Protocol VLAN table] -> [QoS Group] -> [Priority] -> [Queue] -> [Shaper]

基于PCP/DEI的流量调度和整形: [Switch port PCP/DEI mapping] -> [Priority] -> [Queue] -> [Shaper]

基于DSCP的流量调度和整形: [QoS DSCP mapping] -> [Priority] -> [Queue] -> [Shaper]

### 基于MAC的流量调度使用内部优先级

在严格的优先级调度模式下，最高优先级的队列首先被服务。队列号代表优先级，队列号最高的队列具有最高优先级。流量从最高优先级的队列传输，直到该队列为空，然后转移到下一个最高优先级的队列，以此类推。如果出站端口没有出现拥堵，数据包一收到就被传送。如果在高优先级流量不断到来的端口发生拥堵，低优先级队列就会饿死。

在所有的CRS交换机上，基于MAC的出站流量调度是根据内部优先级进行的，其方案如下。[MAC address] -> [QoS Group] -> [Priority] -> [Queue]。

在这个例子中，主机1（E7:16:34:00:00:01）和主机2（E7:16:34:00:00:02）将拥有较高的优先级1，其余的主机将拥有较低的优先级0，用于在 ether7端口传输流量。请注意，CRS每个端口最多有8个队列。

```shell
/interface bridge
add name=bridge1
/interface bridge port
add bridge=bridge1 interface=ether6 hw=yes
add bridge=bridge1 interface=ether7 hw=yes
add bridge=bridge1 interface=ether8 hw=yes

```

创建供UFDB使用的QoS组。

```shell
/interface ethernet switch qos-group
add name=group1 priority=1

```

添加UFDB条目以匹配ether7上的特定MAC，并应用QoS组1。

```shell
/interface ethernet switch unicast-fdb
add mac-address=E7:16:34:00:00:01 port=ether7 qos-group=group1 svl=yes
add mac-address=E7:16:34:00:00:02 port=ether7 qos-group=group1 svl=yes

```

配置ether7端口队列，使其只对目标地址按照严格的优先级和QoS方案工作。

```shell
/interface ethernet switch port
set ether7 per-queue-scheduling="strict-priority:0,strict-priority:0,strict-priority:0,strict-priority:0,strict-priority:0,strict-priority:0,strict-priority:0,strict-priority:0" priority-to-queue=0:0,1:1 qos-scheme-precedence=da-based

```

### 基于MAC的流量整形使用内部优先级

基于MAC的流量整形是根据内部优先级来完成的，方案如下。[MAC address] -> [QoS Group] -> [Priority] -> [Queue] -> [Shaper]。 

在这个例子中，无限流量的优先级是0，有限流量的优先级是1，带宽限制是10Mbit。请注意，CRS每个端口最多有8个队列。

创建一个交换端口组。

```shell
/interface bridge
add name=bridge1
/interface bridge port
add bridge=bridge1 interface=ether6 hw=yes
add bridge=bridge1 interface=ether7 hw=yes
add bridge=bridge1 interface=ether8 hw=yes

```

创建一个供UFDB使用的QoS组。

```shell
/interface ethernet switch qos-group
add name=group1 priority=1

```

添加UFDB条目以匹配ether8上的特定MAC并应用QoS组1。

```shell
/interface ethernet switch unicast-fdb
add mac-address=E7:16:34:A1:CD:18 port=ether8 qos-group=group1 svl=yes

```

配置ether8端口队列，使其根据严格的优先级和QoS方案工作，只针对目标地址。

```shell
/interface ethernet switch port
set ether8 per-queue-scheduling="strict-priority:0,strict-priority:0,strict-priority:0,strict-priority:0,strict-priority:0,strict-priority:0,strict-priority:0,strict-priority:0" priority-to-queue=0:0,1:1 qos-scheme-precedence=da-based

```

在ether8上为queue1应用带宽限制。

```shell
/interface ethernet switch shaper
add port=ether8 rate=10M target=queue1

```

如果CRS交换机支持访问控制列表，这种配置就比较简单。

```shell
/interface ethernet switch acl policer
add name=policer1 yellow-burst=100k yellow-rate=10M
 
/interface ethernet switch acl
add mac-dst-address=E7:16:34:A1:CD:18 policer=policer1

```

### 基于VLAN的流量调度+使用内部优先级的整形

最好的做法是为被整形器限制的流量分配较低的内部QoS优先级，使其在严格的优先级调度器中也不那么重要。(更高的优先级应该是更重要的和无限的）。

在这个例子中。交换机端口ether6正在使用一个整形器来限制来自ether7和ether8的流量。当链接达到其容量时，具有最高优先级的流量将被首先发送出去。

VLAN10 -> QoS group0 = lowest priority  
VLAN20 -> QoS group1 = normal priority  
VLAN30 -> QoS group2 = highest priority

```shell
/interface bridge
add name=bridge1
/interface bridge port
add bridge=bridge1 interface=ether6 hw=yes
add bridge=bridge1 interface=ether7 hw=yes
add bridge=bridge1 interface=ether8 hw=yes

```

创建QoS组，在VLAN表中使用。

```shell
/interface ethernet switch qos-group
add name=group0 priority=0
add name=group1 priority=1
add name=group2 priority=2

```

添加VLAN条目，对某些VLAN应用QoS组。

```shell
/interface ethernet switch vlan
add ports=ether6,ether7,ether8 qos-group=group0 vlan-id=10
add ports=ether6,ether7,ether8 qos-group=group1 vlan-id=20
add ports=ether6,ether7,ether8 qos-group=group2 vlan-id=30

```

配置ether6、ether7和ether8端口队列，使其仅根据严格的优先级和QoS方案工作，用于基于VLAN的QoS。

```shell
/interface ethernet switch port
set ether6 per-queue-scheduling="strict-priority:0,strict-priority:0,strict-priority:0,strict-priority:0,strict-priority:0,strict-priority:0,strict-priority:0,strict-priority:0" priority-to-queue=0:0,1:1,2:2 qos-scheme-precedence=vlan-based
set ether7 per-queue-scheduling="strict-priority:0,strict-priority:0,strict-priority:0,strict-priority:0,strict-priority:0,strict-priority:0,strict-priority:0,strict-priority:0" priority-to-queue=0:0,1:1,2:2 qos-scheme-precedence=vlan-based
set ether8 per-queue-scheduling="strict-priority:0,strict-priority:0,strict-priority:0,strict-priority:0,strict-priority:0,strict-priority:0,strict-priority:0,strict-priority:0" priority-to-queue=0:0,1:1,2:2 qos-scheme-precedence=vlan-based

```

在ether6上应用带宽限制。

```shell
/interface ethernet switch shaper
add port=ether6 rate=10M

```

### 基于PCP的流量调度

默认情况下，CRS1xx/CRS2xx系列设备将忽略PCP/CoS/802.1p值，并基于FIFO（先进先出）方式转发数据包。当设备的内部队列未满时，则以先进先出的方式发送数据包，一旦队列满了，则更高优先级的流量就可以先发送出去。考虑一个场景，当 **ether1** 和 **ether2** 向 **ether3** 转发数据，而且 **ether3** 拥堵时，那么数据包就要被安排好，我们可以配置交换机来保留最低优先级的数据包，直到所有高优先级的数据包被发送出去，这是VoIP类型设置中非常常见的场景，有些流量需要优先处理。

为了实现这样的行为，将 **ether1、ether2、** 和 **ether3** 端口交换到一起。

```shell
/interface bridge
add name=bridge1
/interface bridge port
add bridge=bridge1 interface=ether1 hw=yes
add bridge=bridge1 interface=ether2 hw=yes
add bridge=bridge1 interface=ether3 hw=yes

```

为每个端口上的每个内部队列启用 **严格策略**。

```shell
/interface ethernet switch port
set ether1,ether2,ether3 per-queue-scheduling="strict-priority:0,strict-priority:0,strict-priority:0,strict-priority:0,strict-priority:0,strict-priority:0,strict-priority:0,strict-priority:0"

```

将每个PCP值映射到一个内部优先级值，为方便起见，只需将PCP映射到一个内部优先级1-1。

```shell
/interface ethernet switch port
set ether1,ether2,ether3 pcp-based-qos-priority-mapping=0:0,1:1,2:2,3:3,4:4,5:5,6:6,7:7

```

交换机会先清空最大的队列，而最高的优先级先得到服务，那么可以把这个内部优先级分配给队列1-1。

```shell
/interface ethernet switch port
set ether1,ether2,ether3 priority-to-queue=0:0,1:1,2:2,3:3,4:4,5:5,6:6,7:7

```

最后，将每个交换机端口设置为根据PCP值来安排数据包。

```shell
/interface ethernet switch port
set ether1,ether2,ether3 qos-scheme-precedence=pcp-based

```

## 带宽限制

___

入站端口监控器和整形器都为CRS交换机提供带宽限制功能。

- 入站端口监控器在端口上设置RX限制。

```shell
/interface ethernet switch ingress-port-policer
add port=ether5 meter-unit=bit rate=10M

```

- 整形器在端口上设置TX限制。

```shell
/interface ethernet switch shaper
add port=ether5 meter-unit=bit rate=10M

```

## 流量风暴控制

___

同样的入站端口监控器也可用于流量风暴控制，以防止二层端口因广播、组播或单播流量风暴而造成中断。

- 下面是ether5端口的广播风暴控制实例，每秒限制500个数据包。

```shell
/interface ethernet switch ingress-port-policer
add port=ether5 rate=500 meter-unit=packet packet-types=broadcast

```

- 有多种数据包类型的例子，其中包括ARP和ND协议以及未注册的组播流量。未注册的组播是未在组播转发数据库中定义的流量。

```shell
/interface ethernet switch ingress-port-policer
add port=ether5 rate=5k meter-unit=packet packet-types=broadcast,arp-or-nd,unregistered-multicast

```

## 参考文档

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
- [Layer2 misconfiguration](https://help.mikrotik.com/docs/display/ROS/Layer2+misconfiguration)
