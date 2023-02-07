# 控制网桥和端口扩展器

___

控制网桥（CB）和端口扩展器（PE）是CRS3xx系列交换机在RouterOS中的一个IEEE 802.1BR标准实现。它允许用PE设备虚拟扩展CB端口，并从一个控制设备管理这些扩展接口。这种配置提供了一个简化的网络拓扑结构、灵活性、增加端口密度并易于管理。下面是一个控制网桥和端口扩展器拓扑结构的例子。

![](https://help.mikrotik.com/docs/download/attachments/37224456/CB_summary.png?version=1&modificationDate=1598966520696&api=v2)

控制网桥通过 **级联** 端口与端口扩展器通信。同样，端口扩展器只通过一个 **上行端口** 与控制网桥通信。在PE设备上，必须配置控制端口，只有一个端口（最靠近CB）作为上行端口，其他控制端口可以作为上行端口的备份，也可以作为串联的交换机的级联端口（如上图中的端口扩展器2和3）。级联端口和上行端口用于传输和接收控制和网络流量。 **扩展端口** 是由CB设备控制的接口，它们通常连接到终端主机。扩展端口只传输和接收网络流量。

请看下面每个交换机型号的支持功能。

| **型号**                           | **控制器网桥** | 端口扩展器 |
| ---------------------------------- | -------------- | ---------- |
| netPower 15FR (CRS318-1Fi-15Fr-2S) | **-**          | **+**      |
| netPower 16P (CRS318-16P-2S+)      | **-**          | **+**      |
| CRS310-1G-5S-4S+ (netFiber 9/IN)   | **-**          | **+**      |
| CRS326-24G-2S+ (RM/IN)             | **-**          | **+**      |
| CRS328-24P-4S+                     | **-**          | **+**      |
| CRS328-4C-20S-4S+                  | **-**          | **+**      |
| CRS305-1G-4S+                      | **-**          | **+**      |
| CRS309-1G-8S+                      | **+**          | **+**      |
| CRS317-1G-16S+                     | **+**          | **+**      |
| CRS312-4C+8XG                      | **+**          | **+**      |
| CRS326-24S+2Q+                     | **+**          | **+**      |
| CRS354-48G-4S+2Q+                  | **+**          | **+**      |
| CRS354-48P-4S+2Q+                  | **+**          | **+**      |

## 限制

尽管控制器允许配置端口扩展器接口，但一些网桥和交换功能不能使用或不能正常工作。下面是最常见的控制器和扩展器的限制。在即将发布的RouterOS版本中，这个列表可能会发生变化。

| 特性                 | 支持 |
| -------------------- | ---- |
| 级联和上行端口绑定   |      |
| 桥接 VLAN 过滤       |      |
| 绑定扩展端口         | -    |
| Dot1x 认证（服务器） | -    |
| 入站和出站速率       | -    |
| 镜像                 | -    |
| 入站端口 VLAN 过滤   | -    |
| 端口隔离             | -    |
| 风暴控制             | -    |
| 交换规则（ACL）      | -    |
| L3 HW 卸载           | -    |
| MLAG                 | -    |

## 快速设置

___

这个例子将创建一个控制网桥（如CRS317-1G-16S+交换机），通过SFP+1接口连接到一个端口扩展器（如CRS326-24G-2S+交换机）。

首先，在CB设备上配置一个启用VLAN过滤的网桥。

```shell
/interface bridge
add name=bridge1 vlan-filtering=yes

```

在同一设备上，配置一个连接到PE设备的端口，作为级联端口。

```shell
/interface bridge port-controller
set bridge=bridge1 cascade-ports=sfp-sfpplus1 switch=switch1

```

最后，在PE设备上，只需配置一个控制端口，它将被选为上游端口。

```shell
/interface bridge port-extender
set control-ports=sfp-sfpplus1 switch=switch1

```

一旦PE和CB设备连接起来，所有在同一个交换机组上的接口（除了控制端口）将被扩展，并可以在CB设备上进一步配置。CB设备上将应用自动网桥端口配置，将所有扩展的端口添加到一个单一的网桥中，该配置可以以后修改。

为了排除某些端口被扩展（例如，用于带外管理），需另外配置 "排除的端口 "属性。
  
请确保不在任何路由或网桥配置中包括级联端口和控制端口。这些端口只推荐给CB和PE使用。

## 发现和控制协议

___

在扩展端口的帧转发之前，控制网桥和端口扩展器必须发现对方并交换基本信息。

支持CB和PE的设备使用邻居发现协议LLDP和特定的端口扩展TLV。允许CB和PE设备在级联和控制端口上广告它们支持的功能。

CB和PE配置可以覆盖邻居发现设置，例如，如果一个级联端口不包括在邻居发现接口列表中，LLDP消息仍将被发送。

一旦CB和PE之间交换了LLDP信息，就会通过一个边缘控制协议（ECP）启动控制和状态协议（CSP）。CSP在CB和PE之间用于主张控制和接收来自相关PE的状态信息--它为扩展端口分配唯一的ID，控制数据路径设置（如端口VLAN成员）并发送端口状态信息（如接口统计，PoE-out监控）。ECP提供可靠和有顺序的帧交付（用EtherType 0x8940编码）。

目前的CB实现不支持任何故障转移技术。一旦CB设备变得不可用，PE设备将失去所有的控制和数据转发规则。

## 数据包流量

___

为了更好地理解控制网桥和端口扩展器的基本原理，下面提供一个数据包演练。

1. 在扩展端口上收到一个L2数据包。
2. 端口扩展器用E-TAG头（EtherType 0x893F）封装该数据包，并通过上行端口转发到控制网桥。E-TAG数据包包含有关PE源端口ID的信息。PE设备不做任何本地交换决定。
3. 控制网桥收到E-TAG数据包，并确切知道哪个扩展接口收到了它。然后控制网桥在内部对数据包进行解封装，并通过常规的交换决策（主机学习、目标地址查询、VLAN过滤等）进行处理。
4. 一旦做出交换决定，CB将再次用E-TAG封装原始数据包，并通过级联端口，向端口扩展器发送。
   1. 对于单目标数据包（单播），CB将在E-TAG中包括PE目的端口ID，并通过一个正确的级联端口发送。
   2. 对于多目标数据包（广播、多播或未知单播），CB将在E-TAG中包括一个目标组标记和源端口ID，并在每个级联端口发送一个数据包副本。
5. 一旦PE设备在上行端口收到E-TAG数据包，PE将其解封装并通过扩展端口发送原始L2数据包。
   1. 对于单目标数据包（单播），PE将只把数据包发送到正确的扩展端口。
   2. 对于多目标数据包（广播、多播或未知的单播），PE将在每个扩展端口发送一个数据包副本（除了接收数据包的源端口）。

![](https://help.mikrotik.com/docs/download/attachments/37224456/CB_unicast3.png?version=3&modificationDate=1599825162444&api=v2)

![](https://help.mikrotik.com/docs/download/attachments/37224456/CB_broadcast2.png?version=1&modificationDate=1599824973103&api=v2)

## 控制网桥的设置和监控选项

___

本节介绍控制网桥的设置和监控选项。

**Sub-menu:** `/interface bridge port-controller`

| 属性                                                | 说明                                                                                                          |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| **bridge** (_name;_ Default: **none**)              | 桥接接口，端口将被扩展。只有在指定了`bridge`和`switch`属性时，CB才会启用，否则，它将处于禁用状态。            |
| **cascade-ports** (_interfaces;_ Default: **none**) | 将充当级联端口的接口。也支持802.3ad或balance-xor`mode`的绑定接口。                                            |
| **switch** (_name;_ Default: **none**)              | 作为CB的交换，确保控制和网络流量。 只有在指定了`bridge`和`switch`属性时，CB才会启用，否则，它将处于禁用状态。 |

在CB和PE设备配置和连接后，每个PE设备将自动在设备菜单上可见，使用 `print` 和 `monitor` 命令查看更多细节。

```shell
[admin@Controller] > interface bridge port-controller device print
Flags: I - inactive
 0   name="pe1" pe-mac=64:D1:54:EB:AE:BC descr="MikroTik RouterOS 6.48beta35 (testing) CRS328-24P-4S+" control-ports=pe1-sfpplus1,pe1-sfpplus2
 
 1   name="pe2" pe-mac=64:D1:54:C7:3A:58 descr="MikroTik RouterOS 6.48beta35 (testing) CRS326-24G-2S+" control-ports=pe2-sfpplus1
[admin@Controller] > interface bridge port-controller device monitor pe2
                 name: pe2
               status: active
  connected-via-ports: sfp-sfpplus1==pe1-sfpplus1,pe1-sfpplus2==pe2-sfpplus1
   connected-via-devs: controller,pe1

```

**Sub-menu:** `/interface bridge port-controller device`

| 属性                                           | 说明                           |
| ---------------------------------------------- | ------------------------------ |
| **connected-via-devs** (_name_)                | 显示从PE到CB路径中的连接设备。 |
| **connected-via-ports** (_name_)               | 显示从PE到CB的连接路径。       |
| **control-ports** (_interfaces_)               | PE设备控制端口。               |
| **descr** (_name_)                             | 简短PE设备说明。               |
| **name** (_name_)                              | 自动分配的PE设备名称。         |
| **pe-mac** (_MAC address_)                     | PE设备MAC地址。                |
| **status** (_active              \| inactive_) | PE设备状态。                   |

此外，每个PE设备接口都可以在端口菜单上进行监控，使用 `print` 和 `monitor` 命令查看更多细节。

```shell

[admin@Controller] > interface bridge port-controller port print where !disabled
Flags: I - inactive, X - disabled, R - running, U - upstream-port, C - cascade-port
 #    NAME                                   DEVICE
 0 I  pe1-ether1                             pe1
 1 R  pe1-ether2                             pe1
 2 R  pe1-ether3                             pe1
 3 R  pe1-ether4                             pe1
 4 U pe1-sfpplus1                           pe1
 5 RC pe1-sfpplus2                           pe1
 6 I  pe2-ether1                             pe2
 7 R  pe2-ether2                             pe2
 8 R  pe2-ether3                             pe2
 9 R  pe2-ether4                             pe2
10  U pe2-sfpplus1                           pe2
[admin@Controller] > interface bridge port-controller port monitor [find where !disabled]
           name: pe1-ether1 pe1-ether2 pe1-ether3 pe1-ether4 pe1-sfpplus1 pe1-sfpplus2 pe2-ether1 pe2-ether2 pe2-ether3 pe2-ether4 pe2-sfpplus1
         status: unknown    link-ok    link-ok    link-ok    no-link      link-ok      unknown    link-ok    link-ok    link-ok    no-link
           rate:            1Gbps      1Gbps      1Gbps      10Gbps       10Gbps                  1Gbps      1Gbps      1Gbps      10Gbps
    port-status: not-added  ok         ok         ok         ok           ok           not-added  ok         ok         ok         ok
           pcid:            457        458        459        480          481                     509        510        511        532

```

**Sub-menu:** `/interface bridge port-controller port`

| 属性                                                                                           | 说明                   |
| ---------------------------------------------------------------------------------------------- | ---------------------- |
| **device** (_name_)                                                                            | 自动分配的PE设备名称。 |
| **name** (_name_)                                                                              | 自动分配的PE端口名称。 |
| **pcid** (_integer_)                                                                           | 自动分配的端口标识符。 |
| **port-status** (_dev-inactive \| not-added                               \| ok_)              | PE端口状态。           |
| **rate** (_bps_)                                                                               | 连接的数据速率。       |
| **status** (_link-ok           \| no-link                                         \| unknown_) | PE端口连接状态。       |

控制网桥可以从端口扩展器的端口poe菜单上监控PoE-out相关信息，使用 `print` 和 `monitor` 命令查看更多细节。有关PoE-out的更多信息，请访问 [PoE-out手册](https://help.mikrotik.com/docs/display/ROS/PoE-Out)。

```shell
[admin@Controller] > interface bridge port-controller port poe print
 # NAME                                    DEVICE
 0 pe1-ether1                              pe1
 1 pe1-ether2                              pe1
 2 pe1-ether3                              pe1
 3 pe1-ether4                              pe1
 4 pe1-ether5                              pe1
 5 pe1-ether6                              pe1
 6 pe1-ether7                              pe1

...
```

```shell
[admin@Controller] > interface bridge port-controller port poe monitor pe1-ether2,pe1-ether3
               name: pe1-ether2 pe1-ether3
     poe-out-status: powered-on powered-on
    poe-out-voltage: 52.8V      52.9V
    poe-out-current: 123mA      95mA
      poe-out-power: 6.4W       5W
```

## 端口扩展器设置

___

本节介绍端口扩展器的设置。

**Sub-menu:** `/interface bridge port-extender`

| 属性                                                 | 说明                                                                                                         |
| ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| **control-ports** (_interfaces;_ Default: **none**)  | 将连接到CB（上游端口）或串联其他PE设备（级联端口）的接口。也支持带有802.3ad或balance-xor `mode` 的绑定接口。 |
| **excluded-ports** (_interfaces;_ Default: **none**) | 不会被扩展的接口。                                                                                           |
| **switch** (_name;_ Default: **none**)               | 将作为扩展器并确保控制和网络流量的交换机。 只有指定该属性时，PE才会启用，否则，将处于禁用状态。              |

## 配置实例

___

下面介绍了最常见的配置例子。为了使 CB 和 PE 配置正常工作，需要启用网桥 VLAN 过滤，所以一定要先了解过滤原理 - [bridge VLAN filtering](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-BridgeVLANFiltering), [bridge VLAN table](https://help.mikrotik.com/docs/display/ROS/Bridge+VLAN+Table)。

## CB和PE的基本配置

在这个例子中，CRS317-1G-16S+设备作为控制网桥，CRS328-24P-4S+作为端口扩展器，见下面的连接方案。

![](https://help.mikrotik.com/docs/download/attachments/37224456/Basic_CB_PE_config.png?version=2&modificationDate=1605179681488&api=v2)

首先，配置CB设备。可以添加一个启用了VLAN过滤的网桥接口来完成。此外，将任何本地接口添加到同一个网桥，它允许在任何本地接口和扩展接口之间转发流量。在这个例子中，添加了一个 sfp-sfpplus2 接口。

```shell
/interface bridge
add name=bridge1 vlan-filtering=yes
/interface bridge port
add bridge=bridge1 interface=sfp-sfpplus2

```

要启用 CB，需要指定网桥、交换机和至少一个级联端口。请确保级联端口不包括在网桥或路由配置中。这些端口只推荐用于 CB 和 PE 的使用。

```shell
/interface bridge port-controller
set bridge=bridge1 cascade-ports=sfp-sfpplus1 switch=switch1

```

为了启用PE，配置控制端口和交换机。另外，配置一个或多个不应该被扩展的接口，用 "excluded-ports "属性（例如带外管理目的）。在这个例子中，所有的交换机端口将被扩展。

```shell
/interface bridge port-extender
set control-ports=sfp-sfpplus4 switch=switch1

```

一旦PE和CB设备完成发现并开始控制和状态协议（CSP），RouterOS将永久地创建新的接口并将它们添加到CB设备的网桥中。接口自动分配PE设备名称，加上默认的接口名称，这些接口名称可以在之后修改。请注意，控制端口和排除端口也会被显示在接口列表中，但它们不会被纳入网桥。

```
[admin@Controller_Bridge] > /interface print where name~ "pe"

Flags: D - dynamic, X - disabled, R - running, S - slave 

 #     NAME                                TYPE       ACTUAL-MTU L2MTU  MAX-L2MTU
 0  RS pe1-ether1                          extport          1500  1584
 1  RS pe1-ether2                          extport          1500  1584
 2  RS pe1-ether3                          extport          1500  1584
 3   S pe1-ether4                          extport          1500  1584
 4   S pe1-ether5                          extport          1500  1584
 5   S pe1-ether6                          extport          1500  1584
 6   S pe1-ether7                          extport          1500  1584
 7   S pe1-ether8                          extport          1500  1584
 8   S pe1-ether9                          extport          1500  1584
 9   S pe1-ether10                         extport          1500  1584
10   S pe1-ether11                         extport          1500  1584
11   S pe1-ether12                         extport          1500  1584
12   S pe1-ether13                         extport          1500  1584
13   S pe1-ether14                         extport          1500  1584
14   S pe1-ether15                         extport          1500  1584
15   S pe1-ether16                         extport          1500  1584
16   S pe1-ether17                         extport          1500  1584
17   S pe1-ether18                         extport          1500  1584
18   S pe1-ether19                         extport          1500  1584
19   S pe1-ether20                         extport          1500  1584
20   S pe1-ether21                         extport          1500  1584
21   S pe1-ether22                         extport          1500  1584
22   S pe1-ether23                         extport          1500  1584
23   S pe1-ether24                         extport          1500  1584
24  RS pe1-sfpplus1                        extport          1500  1584
25  RS pe1-sfpplus2                        extport          1500  1584
26  RS pe1-sfpplus3                        extport          1500  1584
27     pe1-sfpplus4                        extport          1500  1584
[admin@Controller_Bridge] > interface bridge port print 
Flags: X - disabled, I - inactive, D - dynamic, H - hw-offload 

 #     INTERFACE              BRIDGE             HW  PVID PRIORITY  PATH-COST INTERNAL-PATH-COST    HORIZON

 0   H sfp-sfpplus2           bridge1            yes    1     0x80         10                 10       none
 1   H pe1-ether1             bridge1            yes    1     0x80         10                 10       none
 2   H pe1-ether2             bridge1            yes    1     0x80         10                 10       none
 3   H pe1-ether3             bridge1            yes    1     0x80         10                 10       none
 4 I H pe1-ether4             bridge1            yes    1     0x80         10                 10       none
 5 I H pe1-ether5             bridge1            yes    1     0x80         10                 10       none
 6 I H pe1-ether6             bridge1            yes    1     0x80         10                 10       none
 7 I H pe1-ether7             bridge1            yes    1     0x80         10                 10       none
 8 I H pe1-ether8             bridge1            yes    1     0x80         10                 10       none
 9 I H pe1-ether9             bridge1            yes    1     0x80         10                 10       none
10 I H pe1-ether10            bridge1            yes    1     0x80         10                 10       none
11 I H pe1-ether11            bridge1            yes    1     0x80         10                 10       none
12 I H pe1-ether12            bridge1            yes    1     0x80         10                 10       none
13 I H pe1-ether13            bridge1            yes    1     0x80         10                 10       none
14 I H pe1-ether14            bridge1            yes    1     0x80         10                 10       none
15 I H pe1-ether15            bridge1            yes    1     0x80         10                 10       none
16 I H pe1-ether16            bridge1            yes    1     0x80         10                 10       none
17 I H pe1-ether17            bridge1            yes    1     0x80         10                 10       none
18 I H pe1-ether18            bridge1            yes    1     0x80         10                 10       none
19 I H pe1-ether19            bridge1            yes    1     0x80         10                 10       none
20 I H pe1-ether20            bridge1            yes    1     0x80         10                 10       none
21 I H pe1-ether21            bridge1            yes    1     0x80         10                 10       none
22 I H pe1-ether22            bridge1            yes    1     0x80         10                 10       none
23 I H pe1-ether23            bridge1            yes    1     0x80         10                 10       none
24 I H pe1-ether24            bridge1            yes    1     0x80         10                 10       none
25   H pe1-sfpplus1           bridge1            yes    1     0x80         10                 10       none
26   H pe1-sfpplus2           bridge1            yes    1     0x80         10                 10       none
27   H pe1-sfpplus3           bridge1            yes    1     0x80         10                 10       none
```

现在，CRS317-1G-16S+设备使用CRS328-24P-4S+设备扩展了其端口，数据包转发可以在所有桥接的端口之间进行。

## 聚合和接入端口

在这个例子中，将在控制器桥接设备上创建无标记（接入）和有标记（聚合）的端口配置，见下图。

![](https://help.mikrotik.com/docs/download/attachments/37224456/CB_PE_VLANs.png?version=3&modificationDate=1605189595256&api=v2)First, configure the CB and PE devices, the configuration is identical to the previous example. Use this configuration for CB device.

```shell
/interface bridge
add name=bridge1 vlan-filtering=yes
/interface bridge port
add bridge=bridge1 interface=sfp-sfpplus2
/interface bridge port-controller
set bridge=bridge1 cascade-ports=sfp-sfpplus1 switch=switch1

```

对PE设备使用此配置。

```shell
/interface bridge port-extender
set control-ports=sfp-sfpplus4 switch=switch1

```

在CB设备上成功创建扩展端口并添加到网桥后，可以开始配置VLAN相关属性。首先，使用 `pvid` 属性将访问端口配置为各自的 VLAN ID。在 `/interface bridge port` 菜单中使用 `print` 命令，以找出准确的接口名称。

```shell
/interface bridge port
set [find interface=pe1-ether1] pvid=10
set [find interface=pe1-ether2] pvid=20
set [find interface=pe1-ether3] pvid=30

```

然后添加网桥VLAN条目，并指定有标签、无标签的端口。注意，有两个标记的端口 - 本地端口名为 sfp-sfpplus2，扩展端口名为 pe1-sfpplus1。

```shell
/interface bridge vlan
add bridge=bridge1 tagged=pe1-sfpplus1,sfp-sfpplus2 untagged=pe1-ether1 vlan-ids=10
add bridge=bridge1 tagged=pe1-sfpplus1,sfp-sfpplus2 untagged=pe1-ether2 vlan-ids=20
add bridge=bridge1 tagged=pe1-sfpplus1,sfp-sfpplus2 untagged=pe1-ether3 vlan-ids=30

```

这样，VLAN就配置好了，设备应该能通过端口通信。然而，我们建议再进一步，应用一些额外的过滤选项。在本地网桥端口上启用端口 "ingress-filtering"，并根据数据包类型使用 "frame-types "设置进行帧过滤。

```shell
/interface bridge port
set [find interface=pe1-ether1] frame-types=admit-only-untagged-and-priority-tagged
set [find interface=pe1-ether2] frame-types=admit-only-untagged-and-priority-tagged
set [find interface=pe1-ether3] frame-types=admit-only-untagged-and-priority-tagged
set [find interface=pe1-sfpplus1] frame-types=admit-only-vlan-tagged
set [find interface=sfp-sfpplus2] frame-types=admit-only-vlan-tagged ingress-filtering=yes

```

端口入站VLAN过滤在扩展端口上不支持。

## 级联多个端口扩展器并使用绑定接口

在这个例子中，两个PE设备（CRS328-24P-4S+和CRS326-24G-2S+）将被添加到CB（CRS317-1G-16S+）。为了增加上行和级联端口的吞吐量，将创建 [绑定接口](https://help.mikrotik.com/docs/display/ROS/Bonding)。见下图。

![](https://help.mikrotik.com/docs/download/attachments/37224456/bonding_cascade.png?version=2&modificationDate=1606810698758&api=v2)

CB和PE的配置与第一个例子类似，主要区别在于绑定接口的使用。首先，配置CB设备--为级联端口创建一个绑定接口，创建一个网桥并添加任何需要的本地网桥端口，最后启用CB。使用下面的命令。

```shell
/interface bonding
add mode=802.3ad name=bond1 slaves=sfp-sfpplus1,sfp-sfpplus2
/interface bridge
add name=bridge1 vlan-filtering=yes
/interface bridge port
add bridge=bridge1 interface=sfp-sfpplus3
/interface bridge port-controller
set bridge=bridge1 cascade-ports=bond1 switch=switch1

```

然后配置端口扩展器1设备。这个设备需要两个绑定接口--第一个将作为上行端口，第二个将作为端口扩展器2设备的级联端口。另外，配置一个或多个不该扩展的接口，用 "excluded-ports "属性（例如带外管理目的）。在这个例子中，所有交换机端口都将被扩展。

```shell
/interface bonding
add mode=802.3ad name=bond1 slaves=sfp-sfpplus1,sfp-sfpplus2
add mode=802.3ad name=bond2 slaves=sfp-sfpplus3,sfp-sfpplus4
/interface bridge port-extender
set control-ports=bond1,bond2 switch=switch1

```

最后，配置端口扩展器2设备 - 创建一个绑定接口并启用PE。此外，如果有必要，配置一个或多个 "排除端口"。在这个例子中，所有的交换机端口都将被扩展。

```shell
/interface bonding
add mode=802.3ad name=bond1 slaves=sfp-sfpplus1,sfp-sfpplus2
/interface bridge port-extender
set control-ports=bond1 switch=switch1

```

现在，CRS317-1G-16S+设备已经用额外的48个千兆以太网端口扩展了它的端口，在所有桥接的端口之间可以实现数据包转发。

使用设备菜单中的 `monitor` 命令来查看PE设备的连接路径。另外，使用端口菜单中的 `print` 命令，可以看到哪些PE接口被用作上行和级联端口。

```shell
[admin@Controller_Bridge] > interface bridge port-controller device monitor [find]
                   name: pe1                    pe2
                 status: active                 active
    connected-via-ports: bond1==pe1-cntrl-bond1 bond1==pe1-cntrl-bond1
                                                pe1-cntrl-bond2==pe2-cntrl-bond1
     connected-via-devs: controller             controller
                                                pe1
[admin@Controller_Bridge] > interface bridge port-controller port print where running or upstream-port
Flags: I - inactive, X - disabled, R - running, U - upstream-port, C - cascade-port 
 #    NAME                                                  DEVICE                                                 
 0 R  pe1-ether2                                            pe1                                                    
 1 R  pe1-ether3                                            pe1                                                    
 2 R  pe1-ether4                                            pe1                                                    
 3 U pe1-sfpplus1                                          pe1                                                    
 4 U pe1-sfpplus2                                          pe1                                                    
 5 RC pe1-sfpplus3                                          pe1                                                    
 6 RC pe1-sfpplus4                                          pe1                                                    
 7 R  pe2-ether1                                            pe2                                                    
 8 R  pe2-ether2                                            pe2                                                    
 9 R  pe2-ether3                                            pe2                                                    
10 R  pe2-ether4                                            pe2                                                    
11 U pe2-sfpplus1                                          pe2                                                    
12 U pe2-sfpplus2                                          pe2     

```

## 修改和删除配置

在某些情况下，CB和PE设备的配置需要调整（例如，PE设备需要新的控制端口）或删除。要修改PE设备的配置，应先从CB设备上删除所有相关的PE设备配置。只有这样，新的配置才会被应用。

首先，要从CB中删除PE配置，使用以下命令禁用PE。

```shell
/interface bridge port-extender set switch=none control-ports="" excluded-ports=""

```

然后，在 CB 设备上，删除相关的桥接和其他使用 PE 接口的 RouterOS 配置 (例如，参见 "/interface bridge port" 和 "/interface bridge vlan" 菜单中的导出)。例如，要从一个特定的 PE 设备上删除所有桥接端口，请使用下面的命令。

```shell
/interface bridge port remove [find interface~"pe1"]

```

一旦配置被删除，PE就可以从CB设备列表中删除。此命令也将自动从CB接口列表中删除所有的PE设备接口。如果一些PE接口配置仍然应用在CB上，它将不再有效。使用`print`命令来找出PE设备的名称。

```shell
/interface bridge port-controller device remove [find name=pe1]

```
