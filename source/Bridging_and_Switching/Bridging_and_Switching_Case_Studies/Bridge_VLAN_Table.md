# 网桥VLAN表

___

从RouterOS v6.41开始，可以使用网桥来过滤网络中的VLAN。为了达到这个目的，应该使用 [网桥VLAN过滤](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-BridgeVLANFiltering) 功能。这个功能应该用来代替许多已知的VLAN错误配置，这些错误配置很可能导致你的性能问题或连接问题，可以在 [VLAN in a bridge with a physical interface](https://help.mikrotik.com/docs/display/ROS/Layer2+misconfiguration#Layer2misconfiguration-VLANinabridgewithaphysicalinterface) 部分阅读最受欢迎的错误配置之一。网桥 VLAN 过滤功能最重要的部分是网桥 VLAN 表，它规定了每个端口允许哪些 VLAN，但如果想进行更高级的设置，配置它可能会变得相当复杂，对于一般的设置，可以使用 [聚合和访问端口](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-VLANExample-TrunkandAccessPorts) 的例子，但本指南的目的是深入解释并指出使用网桥VLAN过滤时的一些行为特征。

## 背景

___

在深入解释桥接VLAN过滤之前， 应该了解桥接VLAN过滤所涉及的几个基本概念。

- **Tagged/Untagged** 在"/interface bridge vlan "菜单下，可以指定一个包含有标签和无标签端口的项。一般来说，有标签的端口应该是聚合端口，无标签的端口应该是接入端口。通过指定一个有标签的端口，网桥将始终为通过该端口发送的数据包设置一个 VLAN 标签 (出站)。如果指定了一个未标记的端口， 网桥将总是从出站数据包中去除 VLAN 标记。
- **VLAN-ids** - 在"/interface bridge vlan "菜单下，你可以指定一项，其中允许在特定的端口上使用某些VLAN。VLAN ID在出站端口上被检查。如果数据包中的 VLAN ID 不存在于出站端口的桥接 VLAN 表中，那么数据包在发送之前就会被丢弃。
- **PVID** - 端口VLAN ID用于接入端口，用一个特定的VLAN ID来标记所有入站流量。每使用一个PVID，就会在网桥VLAN表中添加一个动态条目，该端口会被自动添加为未标记的端口。
- **Ingress filtering/** - 默认情况下，在桥接VLAN表中不存在的VLAN会在发送前被丢弃（出站），但这个属性允许在接收数据包时丢弃（入站）。
- **管理访问** - 网桥应该只是在网桥端口之间转发数据包，在其他设备看来，它们之间只是有一条线。通过网桥VLAN过滤，可以限制哪些数据包被允许访问配置了网桥的设备，最常见的做法是只允许使用一个非常具体的VLAN ID来访问设备，但也有其他方法可以授予设备访问权。在通过网桥端口访问设备时，管理访问是增加另一层安全性的好方法，这种访问方式有时被称为管理端口。对于支持 [带有硬件卸载的VLAN过滤](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-BridgeHardwareOffloading) 的设备，它也与网桥的CPU端口有关。
- **CPU端口** - 每个带有交换芯片的设备都有一个特殊用途的端口，称为CPU端口，它用于与设备的CPU通信。对于支持硬件卸载的VLAN过滤的设备，这个端口就是网桥接口本身。这个端口主要用于创建管理访问，但也可用于其他目的，例如，在VLAN之间路由流量，标记数据包和应用队列。
- **frame-type** - 可以过滤掉数据包，无论它们是否有VLAN标签，这对桥接端口增加一层安全保障很有用。
- **EtherType** - 默认情况下，VLAN感知网桥会通过检查C-TAG（0x8100）来过滤VLAN，所有其他的VLAN标签都被认为是无标签的数据包（没有VLAN标签）。所选的 EtherType 将被用于 VLAN 过滤和 VLAN 标记/未标记。
- 如果数据包的 EtherType 与网桥配置的 EtherType 不匹配，那么入站数据包就会被视为无标记数据包，这种行为为将 VLAN 封装到另一个不同的 VLAN 提供了可能性。这也为通过网络中的不同设备来分流特定的流量提供了可能。
- 如果一个数据包有一个与EtherType相匹配的VLAN标签，那么这个数据包就会被认为是一个有标签的数据包，但是你可以强迫另一个VLAN标签，而不管数据包的内容。通过在网桥端口上设置 `tag-stacking=yes`，将在所有入站数据包的任何其他标签之上添加另一个具有 PVID 值的 VLAN 标签。

## 聚合/接入端口设置

___

下面可以看到一个很常见的图，是由一个聚合端口和多个接入端口组成的非常典型的设置类型。

![](https://help.mikrotik.com/docs/download/attachments/28606465/Trunk_access_setup.png?version=2&modificationDate=1618317157478&api=v2)

这种设置非常普遍，它提供了把网络划分为多个网段的可能性，同时使用一个交换机和一个路由器，这样的要求对于想要分离多个部门的公司非常普遍。有了VLAN，可以使用不同的DHCP服务器，它可以根据VLAN ID从不同的子网发出一个IP地址，这使得创建防火墙规则和QoS更加容易。

在这样的设置中，会把一些通用设备如台式电脑连接到  **ether2**  和  **ether3** ，这些设备可以被认为是工作站，它们一般只使用无标签的流量（有可能对所有发送出通用工作站的流量强制使用VLAN标签，尽管这不是很常见）。为了将一些工作站与其他工作站隔离开来，必须给所有进入  **ether2**  或  **ether3**  的数据包添加一个VLAN标签，但要决定数据包应该得到什么VLAN ID，就要用一个叫做**基于端口的VLAN**概念。在这个概念中，数据包得到一个VLAN标签，其VLAN ID基于设备所连接的桥接端口。例如，在这个设置中， **ether2**  的设备将得到一个带有  **VLAN20**  的VLAN标签，而  **ether3**  的设备将得到一个带有**VLAN30**的VLAN标签，只要有足够的桥接端口，这个概念是非常可扩展的。这应该让你明白网桥和 **ether2/ether3** 后面的设备之间的通信是没有标签的（因为没有VLAN标签，所以叫这个名字）。

当我们确定了我们的非标记端口后，我们现在可以确定我们的标记端口。标签端口将是聚合端口（携带多个VLAN的端口），通常这个端口连接到路由器或另一个交换机/网桥，也可以有多个聚合端口。标签端口总是携带带有VLAN标签的数据包（因此而得名），必须 **总是** 为希望这个端口转发的每个VLAN ID指定标签端口。有可能一个端口是一个VLAN ID的标记端口，而同一个端口是一个不同VLAN ID的非标记端口，但这是针对不同类型的设置（混合端口设置）。

必须为PVID属性添加特别说明。这个属性应该用于接入端口，但它也可以用于聚合端口（在混合端口设置中）。通过使用 PVID 属性，将为该特定网桥端口上收到的所有 **UNTAGGED** 数据包添加一个新的 VLAN 标签，其 VLAN ID 在 PVID 中指定。PVID 对有标签的数据包没有任何影响，这意味着，例如，如果在  **ether2**  上收到一个 VLAN 标签为 **VLAN40** 的数据包，而这个数据包有 `PVID=20`，那么 VLAN 标签就不会被改变，转发将取决于网桥 VLAN 表中的条目。

要配置聚合/接入端口设置，首先需要创建一个网桥。

```shell
/interface bridge
add name=bridge1

```

先不要启用VLAN过滤，因为可能会因为没有管理权限而被锁定在设备之外，管理权限是在最后配置的。

添加桥接端口，为每个接入端口指定PVID。

```shell
/interface bridge port
add bridge=bridge1 interface=ether1
add bridge=bridge1 interface=ether2 pvid=20
add bridge=bridge1 interface=ether3 pvid=30

```

PVID 在启用 VLAN 过滤之前没有任何作用。

在网桥 VLAN 表中添加适当的条目。

```shell
/interface bridge vlan
add bridge=bridge1 tagged=ether1 untagged=ether2 vlan-ids=20
add bridge=bridge1 tagged=ether1 untagged=ether3 vlan-ids=30

```

可能想用一个项来简化，类似于这样。

````shell
/interface bridge vlan
add bridge=bridge1 tagged=ether1 untagged=ether2,ether3 vlan-ids=20,30

````

不要在接入端口上使用多个VLAN ID。这将无意中在两个接入端口上同时允许  **VLAN20**  和 **VLAN30**。在上面的例子中， **ether3**  应该为所有进入的数据包设置VLAN标签，使用 **VLAN30** (因为`PVID=30`)，但当VLAN通过这个端口发送出去时，没有限制这个端口上允许的VLAN。网桥 VLAN 表负责决定是否允许某个 VLAN 通过特定端口发送。上面的条目指定了  **VLAN20**  和 **VLAN30** 都允许通过  **ether2**  和  **ether3**  发送出去，在此基础上，该项还指定了数据包应该在没有VLAN标签的情况下发送出去（数据包作为无标签的数据包发送）。因此，你可能会从VLAN向不应该接收这种流量的端口泄漏数据包，请看下面的图片。

![](https://help.mikrotik.com/docs/download/attachments/28606465/Trunk_access_setup_bad.png?version=2&modificationDate=1618317557770&api=v2)

错误配置的 VLAN 表允许 VLAN20 通过 ether3 发送，它也会允许 VLAN30 通过 ether2。

不要为接入端口使用一个以上的桥接VLAN表项中指定的VLAN ID， 只应该为聚合端口指定多个VLAN ID。

没有必要把桥接端口作为无标记端口添加，因为每个桥接端口都是作为无标记端口动态添加的，其 VLAN ID 是在 PVID 属性中指定的。这是因为有一个功能可以自动在网桥 VLAN 表中添加一个适当的条目， 以方便和提高性能， 但这个功能也有一些注意事项， 你必须加以注意。所有具有相同PVID的端口都会被添加到一个适当的VLAN ID条目中，作为无标记的端口，但请注意 **网桥接口** 也有一个VLAN ID。

出于测试目的，我们将启用 VLAN 过滤，但请注意，这可能会失去对设备的访问，因为它还没有配置管理权限（我们将在后面配置）。建议在使用串行控制台时配置VLAN过滤，尽管你也可以通过一个没有加入网桥的端口来配置设备。确保你使用的是串行控制台或通过不同的端口（不在网桥中）连接，并启用VLAN过滤功能。

```shell
/interface bridge set bridge1 vlan-filtering=yes

```
  
可能不会在启用VLAN过滤后就失去对设备的访问，但可能会被断开连接，因为网桥必须自我重置才能使VLAN过滤生效，这迫使你重新连接（这主要与使用MAC-telnet时有关）。有可能使用无标记的流量来访问设备，这种情况将在下面描述。

如果你现在启用了VLAN过滤，并打印出当前的VLAN表，看到这样一张表。

```shell
[admin@MikroTik] > /interface bridge vlan print
Flags: X - disabled, D - dynamic
 #   BRIDGE                     VLAN-IDS  CURRENT-TAGGED       CURRENT-UNTAGGED
 0   bridge1                    20        ether1               ether2
 1   bridge1                    30        ether1               ether3
 2 D bridge1                    1                              bridge1
                                                               ether1

```

由于所有桥接端口（包括聚合端口， **ether1** ）都默认设置了 "PVID=1"，所以 **VLAN1** 有一个动态添加的项，但也应该注意到， **bridge1**  接口（CPU端口）也被动态添加。应该注意到， **bridge1**  也是一个网桥端口，因此可能会被动态添加到网桥VLAN表中。有可能因为这个功能而无意中允许对设备的访问。例如，如果按照本指南的要求，为聚合端口（ **ether1** ）设置了 **PVID=1**，而没有同时改变CPU端口（ **bridge1** ）的PVID，那么通过  **ether1**  使用无标记流量访问设备是允许的，这在打印出网桥VLAN表时也可以看到。这种情况在下面的图片中有所说明。

![](https://help.mikrotik.com/docs/download/attachments/28606465/Trunk_access_setup_unintentional_mgmt.png?version=2&modificationDate=1618317673875&api=v2)

无意中允许通过聚合端口使用未标记的流量进行管理访问

经常检查网桥VLAN表，是否无意中允许某些VLAN或无标记流量进入特定端口，特别是CPU端口（网桥）。

有一个简单的方法可以防止网桥（CPU端口）被添加为无标记端口，可以简单地将聚合端口的PVID设置为与网桥的PVID不同（或改变网桥的PVID），但还有一个选择更直观，也更值得推荐。既然期望聚合端口只应该接收有标记的流量（在这个例子中，它应该只接收 **VLAN20/VLAN30**），而不接收无标记的流量，那么可以使用ingress-filtering和frame-type来过滤掉不需要的数据包，为了充分理解ingress filtering的行为，我们必须首先了解管理访问的细节。

管理访问是用来创建一种通过启用了 VLAN 过滤的网桥访问设备的方式。可以简单地允许无标记的访问，要做到这一点相当简单。假设你想让  **ether3**  后面的工作站能够访问设备，我们之前假设工作站是一台普通的计算机，不会使用有标签的数据包，因此只会发送无标签的数据包，这意味着我们应该把CPU端口（ **bridge1** ）作为一个无标签的接口添加到网桥的VLAN表中，要做到这一点，只需对  **bridge1**  和  **ether3**  端口使用相同的PVID值，把两个端口设置为VLAN ID无标签的成员。 在本例中，将从  **ether3**  连接，它有 `PVID=30`，所以要相应地改变配置。

```shell
/interface bridge set [find name=bridge1] pvid=30
/interface bridge vlan set [find vlan-ids=30] untagged=bridge1,ether3

```

可以使用动态添加具有相同PVID值的无标记端口的功能，可以简单地改变PVID以匹配  **ether3**  和  **bridge1** 。

允许使用无标记流量访问设备并不是一个好的安全做法，一个更好的方法是允许使用一个非常具体的VLAN（有时称为管理VLAN）来访问设备，在我们的案例中，这将是  **VLAN99** 。这增加了一个重要的安全层，因为攻击者必须猜测用于管理的VLAN ID，然后猜测登录凭证，在此基础上，甚至可以通过只允许使用某些IP地址访问设备来增加另一个安全层。本指南的目的是提供一个深入的解释，为此，我们在设置中增加了一个复杂程度，以了解一些必须考虑到的可能的注意事项。我们将允许从一个访问端口使用标记流量进行访问（如下图所示）。为了允许使用  **VLAN99**  从  **ether3**  访问设备，我们必须在网桥VLAN表中添加一个适当的条目。此外，连接到ether3的网络设备必须支持VLAN标记。

```shell
/interface bridge vlan
add bridge=bridge1 tagged=bridge1,ether3 vlan-ids=99

```
  
![](https://help.mikrotik.com/docs/download/attachments/28606465/Trunk_access_setup_mgmt_access.png?version=2&modificationDate=1618317611046&api=v2)

通过一个接入端口使用带标签的流量进行管理访问(这使得它成为一个混合端口)

如果 ether1 和 bridge1 的 PVID 匹配（默认情况下，确实与 1 匹配），那么允许使用来自 ether1 的无标记流量访问设备，因为有动态添加无标记端口到网桥 VLAN 表的功能。

但你可能会注意到，使用  **VLAN99**  的访问在这里不起作用，这是因为需要一个监听标记流量的VLAN接口，可以简单地为适当的VLAN ID创建这个接口，也可以为这个接口设置一个IP地址。

```shell
/interface vlan
add interface=bridge1 name=VLAN99 vlan-id=99
/ip address
add address=192.168.99.2/24 interface=VLAN99

```

我们的接入端口（ **ether3** ）在这一点上希望同时获得有标签和无标签的流量，这样的端口被称为 **混合端口**。

在这一点上，可以从使用ingress-filtering和frame-type中获益。首先，要关注帧类型，它限制了允许的数据包类型（有标记的、无标记的、两者都有），但为了使帧类型正常工作，必须启用ingress-filtering，否则它不会有任何效果。在这个例子中想允许从  **ether3**  使用标记流量（ **VLAN99** ）访问，同时允许一个普通工作站访问网络，我们可以得出结论，这个端口需要允许标记和非标记的数据包，但  **ether1**  和  **ether2**  应该只接收特定类型的数据包，出于这个原因，我们可以加强我们网络的安全性。由于  **ether1**  是聚合端口，它应该只携带有标记的数据包，但  **ether2**  是接入端口，所以它不应该携带任何有标记的数据包，基于这些结论，可以丢弃无效的数据包。

```shell
/interface bridge port
set [find where interface=ether1] ingress-filtering=yes frame-types=admit-only-vlan-tagged
set [find where interface=ether2] ingress-filtering=yes frame-types=admit-only-untagged-and-priority-tagged

```

假设忘了启用ingress-filtering和改变 **ether1** 的frame-type属性，这将无意中通过 **ether1** 增加对设备的访问，因为 **bridge1** 和 **ether1** 的PVID是匹配的，但你希望只有标签流量能够访问设备。可以放弃所有以 **CPU** 端口为目的地的无标记数据包。

```shell
/interface bridge
set bridge1 frame-types=admit-only-vlan-tagged ingress-filtering=yes

```

这不仅会丢弃无标记的数据包， 而且会禁用动态添加无标记端口到网桥 VLAN 表的功能。如果打印出当前的网桥 VLAN 表， 就会发现  **bridge1**  没有被动态地添加为无标记端口。

```shell
[admin@MikroTik] > /interface bridge vlan print
Flags: X - disabled, D - dynamic
 #   BRIDGE       VLAN-IDS  CURRENT-TAGGED        CURRENT-UNTAGGED
 0   bridge1      20        ether1
 1   bridge1      30        ether1                ether3
 2 D bridge1      1                               ether1
 3   bridge1      99        bridge1
                            ether3

```

当在端口上使用 "frame-type=admit-only-vlan-tagged "时，该端口不会被动态地添加为PVID的非标记端口。

帧类型可以用来丢弃某种类型的数据包，而入站过滤可以用来在数据包被送出之前过滤掉它们。为了充分理解进站过滤的必要性，请考虑以下情况。 在 **ether3** 和 **bridge1** 上允许 **VLAN99** ，但仍然可以从 **ether1** 向 **ether3** 发送 **VLAN99** 流量，这是因为网桥VLAN表只在出站端口检查一个端口是否允许携带某个VLAN。在我们的例子中， **ether3** 被允许携带 **VLAN99** ，为此，它被转发。为了防止这种情况，必须使用入站过滤。在这个例子中，网桥VLAN表不包含 **VLAN99** 在 **ether1** 上被允许的条目，因此将被立即丢弃。当然，在我们的方案中，如果没有入口过滤，连接就无法建立，因为 **VLAN99** 只能从 **ether1** 转发到 **ether3** ，而不能从 **ether3** 转发到 **ether1** ，尽管仍有可能在这种错误配置中使用攻击（例如，ARP中毒）。丢包行为在下面的图片中得到说明。

![](https://help.mikrotik.com/docs/download/attachments/28606465/Trunk_access_setup_ingress.png?version=2&modificationDate=1618317931543&api=v2)

有和没有入站过滤的聚合/接入端口设置。入站过滤可以防止不需要的流量被转发。注意，ether1在网桥VLAN表中不允许携带VLAN99。

只要有可能，一定要尝试使用入站过滤，它可以增加一个重要的安全层。

ingress-filtering 也可以用在 **CPU 端口**（网桥）上，这可以用来防止一些可能的攻击载体，并限制允许访问 CPU 的 VLANs。最好是在入站端口丢弃数据包，而不是在出站端口丢弃，这样可以减少CPU负载，当你使用硬件卸载和网桥VLAN过滤时，这一点非常关键。

ingress-filtering属性只对入站流量有影响，但frame-type对出站和入站流量都有影响。

即使可以限制端口上允许的VLAN和数据包类型，但允许通过访问端口访问设备绝不是一个好的安全做法，因为攻击者可以嗅探数据包并提取管理VLAN的ID，应该只允许从聚合端口（ **ether1** ）访问设备，因为聚合端口通常有更好的物理安全性，应该删除之前的项，允许通过连接到路由器的端口访问设备（如下图所示）。

```shell
/interface bridge vlan
add bridge=bridge1 tagged=bridge1,ether1 vlan-ids=99

```

![](https://help.mikrotik.com/docs/download/attachments/28606465/Basic_vlan_switching.png?version=3&modificationDate=1618318076269&api=v2)

## VLAN 隧道设置

___

在某些情况下可能想通过某些交换机转发已经打过标签的流量。这是骨干网基础设施的一个很常见的设置，因为它提供了一种可能性，例如，从边缘路由器封装流量，并通过骨干网无缝转发到另一个边缘路由器。下面可以找到一个VLAN隧道拓扑结构的例子。

![](https://help.mikrotik.com/docs/download/attachments/28606465/Provider_bridge.png?version=2&modificationDate=1618318153472&api=v2)

提供者网桥拓扑结构

为了充分了解如何正确配置VLAN隧道，应该先阅读聚合/接入端口设置，然后再继续。

从RouterOS v6.43开始，有两种可能的方式来实现，一种是标准化的IEEE 802.1ad方式，另一种是使用 **标签堆叠**，先来看看标准化的方式，因为两种方式的原理是一样的，只有几个参数改变才能使用另一种方式。VLAN隧道的工作方式是，网桥检查外部VLAN标签是否使用了指定为ether-type的相同VLAN标签。如果VLAN标签匹配，数据包就被认为是有标签的数据包，否则就被认为是无标签的数据包。

网桥只检查外层标签 (最接近 MAC 地址的标签)， 任何其他标签都会在网桥配置的任何地方被忽略。网桥不知道数据包的内容，即使可能还有其他 VLAN 标签，也只检查第一个 VLAN 标签。

ether-type 属性允许为 VLAN 标签选择以下 EtherTypes。

- 0x88a8 - SVID, IEEE 802.1ad, 服务VLAN
- 0x8100 - CVID, IEEE 802.1Q, 客户 VLAN
- 0x9100 - 双重标签（不是很常见）。

为了正确配置网桥的 VLAN 过滤， 必须了解网桥是如何区分有标签和无标签的数据包的。如前所述， 网桥会检查 EtherType 是否与包中的外层 VLAN 标签相匹配。例如， 考虑下面这个数据包。

```shell
FFFFFFFFFFFF 6C3B6B7C413E 8100 6063 9999
----------------------------------------
DST-MAC = FFFFFFFFFFFF
SRC-MAC = 6C3B6B7C413E
Outer EtherType = 8100 (IEEE 802.1Q VLAN tag)
VLAN priority = 6
VLAN ID = 99 (HEX = 63)
Inner EtherType = 9999

```

假设我们设置了 `ether-type=0x88a8`， 在这种情况下， 上面的数据包将被视为无标记， 因为网桥正在寻找不同的 VLAN 标记。现在考虑下面的数据包。

```shell
FFFFFFFFFFFF 6C3B6B7C413E 88A8 6063 8100 5062 9999
----------------------------------------
DST-MAC = FFFFFFFFFFFF
SRC-MAC = 6C3B6B7C413E
Outer EtherType = 88A8 (IEEE 802.1ad VLAN tag)
VLAN priority = 6
VLAN ID = 99 (HEX = 63)
Inner EtherType 1 = 8100 (IEEE 802.1Q VLAN tag)
VLAN priority = 5
VLAN ID = 98 (HEX = 62)
Innter EtherType 2 = 9999

```

这次假设设置了 `ether-type=0x8100`，在这种情况下，上面的数据包也被认为是没有标签的，因为外部标签使用的是IEEE 802.1ad VLAN标签。同样的原则也适用于其他与VLAN相关的功能，例如，PVID属性会在接入端口上添加一个新的VLAN标签，VLAN标签将使用ether-type中指定的EtherType。

 **SW1** 和 **SW2** 都在使用相同的配置。

```shell
/interface bridge
add name=bridge1 vlan-filtering=yes ether-type=0x88a8
/interface bridge port
add interface=ether1 bridge=bridge1 pvid=200
add interface=ether2 bridge=bridge1 pvid=300
add interface=ether3 bridge=bridge1
/interface bridge vlan
add bridge=bridge1 tagged=ether3 untagged=ether1 vlan-ids=200
add bridge=bridge1 tagged=ether3 untagged=ether2 vlan-ids=300

```

在这个例子中，我们假设所有路由器传递的流量都使用CVID VLAN标签（内部VLAN标签）。根据上述原则，交换机上的这种流量将被视为无标签的流量。交换机将使用SVID VLAN标签（外侧VLAN标签）对这些流量进行封装， **SW1** 和 **SW2** 之间的流量将被视为有标签的流量。在流量到达目的地之前，交换机将解封外部标签，并将原始的CVID VLAN标签帧转发给路由器。请看下面的一个数据包例子。

![](https://help.mikrotik.com/docs/download/attachments/28606465/Service_VLAN_8021ad.png?version=3&modificationDate=1590411291205&api=v2)A packet example before and after SVID VLAN encapsulation 

所有适用于使用IEEE 802.1Q的普通聚合/接入端口设置的原则也适用于VLAN隧道设置，确保使用网桥VLAN表和入站过滤来正确限制VLAN和数据包类型。

如果想从 **ether3** 到设备建立管理访问，并想使用 **VLAN99** ，那么将使用这样的命令。

```shell
/interface bridge vlan
add bridge=bridge1 tagged=bridge1,ether3 vlan-ids=99
/interface vlan
add interface=bridge1 name=VLAN99 use-service-tag=yes vlan-id=99
/ip address
add address=192.168.99.2/24 interface=VLAN99

```

你可能注意到，唯一的区别是VLAN接口使用了 `us-service-tag=yes`，这将VLAN接口设置为监听SVID（IEEE 802.1ad）VLAN标签。这要求使用IEEE 802.1ad VLAN标签，使用管理VLAN访问设备。这意味着，在使用网桥VLAN过滤时，将无法使用CVID VLAN标签连接到设备，ether-type是全局设置的，对所有网桥VLAN过滤功能都有影响。

带有交换芯片Marvell-98DX3257的设备（如CRS354系列）不支持其他VLAN类型（`0x88a8` 和 `0x9100`）的1Gbps以太网接口的VLAN过滤。

## 标签堆叠

在 VLAN 隧道设置中，我们是在添加一个新的 VLAN 标签，这个标签与 VLAN 标签不同，但也可以添加一个新的 VLAN 标签，而不考虑数据包的内容。普通的VLAN隧道设置的区别在于，网桥不检查数据包是有标签还是无标签，它假定在特定端口上收到的所有数据包都是无标签的数据包，并且不管是否有VLAN标签，都会添加一个新的VLAN标签，这被称为**标签堆叠，因为它把VLAN标签 "堆叠 "在之前的标签之上，而不管VLAN标签的类型。对于不支持IEEE 802.1ad标准，但仍想将VLAN流量封装到一个新的VLAN中的网络来说，这是一个非常常见的设置。

将要添加的 VLAN 标签取决于 ether-type 和 PVID。例如，如果在一个端口上有 `ether-type=0x8100` 和  `PVID=200`，那么网桥就会在任何其他标签(如果有的话)之上添加一个新的 IEEE 802.1Q VLAN 标签。同样的VLAN过滤原则仍然适用，必须确定哪些端口将成为主干端口，并把它们标记为有标签的端口，确定接入端口，并把它们添加为无标签的端口。

为了解释VLAN标记和取消标记如何与标记堆叠一起工作，让我们使用与之前相同的网络拓扑结构。

![](https://help.mikrotik.com/docs/download/attachments/28606465/Basic_vlan_switching2.png?version=1&modificationDate=1618318089836&api=v2)

我们想实现的是无论在  **ether2**  和 **ether3** 上收到什么，都会添加一个新的VLAN标签来封装来自这些端口的流量。标签堆叠的作用是强迫添加一个新的VLAN标签，所以可以使用这个属性来实现所期望的设置。我们将使用与聚合/接入端口设置相同的配置，但在接入端口上启用标签堆叠。

```shell
/interface bridge
add name=bridge1 vlan-filtering=yes ether-type=0x8100
/interface bridge port
add bridge=bridge1 interface=ether1
add bridge=bridge1 interface=ether2 tag-stacking=yes pvid=20
add bridge=bridge1 interface=ether3 tag-stacking=yes pvid=30
/interface bridge vlan
add bridge=bridge1 tagged=ether1 untagged=ether2 vlan-ids=20
add bridge=bridge1 tagged=ether1 untagged=ether3 vlan-ids=30

```

添加的VLAN标签将使用指定的以太网类型。所选的EtherType也将被用于VLAN过滤。只有外部标签被检查，但在标签堆叠的情况下，标签检查被跳过，并假定必须以任何方式添加新标签。

让我们假设  **ether2**  和 **ether3** 后面的设备正在发送标记的 **VLAN40** 流量。在这种配置下，**所有** 的数据包都会被封装上一个新的VLAN标签，但必须确保已经把外部标签的VLAN ID添加到网桥VLAN表中。因为 **VLAN40** 是内部标签，所以没有被添加到网桥VLAN表中，我们只关心外部标签，根据端口的不同，外部标签是  **VLAN20**  或 **VLAN30**。

与其他设置类似，网桥的 VLAN 表将被用来确定是否需要去除 VLAN 标签。例如， **ether1** 收到带标签的 **VLAN20** 数据包，网桥检查 **ether2** 是否允许携带 **VLAN20** ，所以它要通过 **ether2** 发送出去，但它也会检查网桥VLAN表是否要去除VLAN标签，由于 **ether2** 被标记为无标签端口，那么网桥将把这些数据包从 **ether1** 转发到 **ether2** ，而不带有 **VLAN20** VLAN标签。

从接入端口的角度来看，与聚合/接入端口设置中的原则相同。所有在 **ether2** 上收到的数据包都将获得一个新的VLAN标签，其VLAN ID是在PVID中指定的，在这种情况下，一个新的VLAN标签将被添加为 **VLAN20** ，这个VLAN将被进行VLAN过滤。请看下面的一个数据包例子。

![](https://help.mikrotik.com/docs/download/attachments/28606465/Tag_stacking.png?version=2&modificationDate=1590414931104&api=v2)

<center>标签堆叠前后的数据包实例</center>
