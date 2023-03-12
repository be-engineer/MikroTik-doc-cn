## 介绍

配置最大传输单元（MTU）是管理员的唯一责任，这样才能在网络中成功实现预期的服务和应用。也就是管理员必须确保MTU的配置方式不会使数据包大小超过网络设备的能力。

最初，MTU的引入是因为通信的高错误率和低速度。数据流的碎片化使人们只能通过重新发送损坏的碎片来纠正损坏的错误，而不是整个数据流。此外，低速连接如调制解调器，发送一个大的片段需要很多的时间，在这种情况下，只有用较小的片段才能进行通信。

但在今天，我们有更低的错误率和更高的通信速度，这为增加MTU的值提供了可能性。通过增加MTU的值减少协议开销，主要由于中断减少而减少CPU的占用率。这样一来，一些非标准帧开始出现。

- **Giant** 或 **Jumbo** 帧 - 比标准（IEEE）以太网MTU更大的帧。
- **Baby Giant** 或 **Baby Jumbo** 帧--比标准（IEEE）以太网MTU稍大的帧。

现在，以太网接口支持高于标准的物理MTU是很常见的，但这不能被视为理所当然。其他网络设备的能力也必须考虑在内-例如，如果2台具有支持物理MTU 1526的以太网接口的路由器通过以太网交换机连接，为了成功实现一些会产生这些大以太网帧的应用，交换机也必须支持转发这种帧。

## 最大传输单元

<table><colgroup><col><col></colgroup><tbody><tr><td><p><span><img draggable="false" src="https://help.mikrotik.com/docs/download/attachments/21725296/MTU_general_explanation.jpg?version=1&amp;modificationDate=1657267706011&amp;api=v2" data-image-src="/docs/download/attachments/21725296/MTU_general_explanation.jpg?version=1&amp;modificationDate=1657267706011&amp;api=v2" data-unresolved-comment-count="0" data-linked-resource-id="135856347" data-linked-resource-version="1" data-linked-resource-type="attachment" data-linked-resource-default-alias="MTU_general_explanation.jpg" data-base-url="https://help.mikrotik.com/docs" data-linked-resource-content-type="image/jpeg" data-linked-resource-container-id="21725296" data-linked-resource-container-version="13" alt=""></span></p></td>
<td><p>Mikrotik RouterOS recognizes several types of MTU:</p><ul><li>IP/Layer-3/L3 MTU</li><li>MPLS/Layer-2.5/L2.5 MTU</li><li>MAC/Layer-2/L2 MTU</li><li>Full frame MTU</li></ul></td></tr></tbody></table>

## 全帧MTU

全帧MTU表示由一个特定接口发送帧的实际大小。不包括校验和，因为它一到达目的地就会被以太网驱动程序删除。

## MAC/Layer-2/L2 MTU

L2MTU表示这个接口可以发送的没有MAC头的帧的最大尺寸。

在RouterOS中，L2MTU值可以在"/interface "菜单中看到。L2MTU支持添加到所有与Routerboard相关的以太网接口、VLAN、网桥、VPLS和无线接口。其中一些支持L2MTU值的配置。所有其他的以太网接口只有在芯片组与Routerboard Ethernets相同时才能显示L2MTU。

这使用户可以检查所需的设置是否可行。用户将可以利用额外的字节用于VLAN和MPLS标签，或者简单地增加接口MTU以摆脱一些不必要的碎片。

这个表格显示了Mikrotik RouterBoards所支持的 _max-l2mtu_（可在"/interface print "菜单中作为只读 "max-l2mtu "选项的值）。

<table style="border: 1px solid #000000"><colgroup><col><col></colgroup>
<tbody><tr><td style="border: 1px solid #000000"><strong>Model name</strong></td><td style="border: 1px solid #000000"><strong>MTU description</strong></td></tr><tr><td style="border: 1px solid #000000"><strong>RB SXT series, RB LHG, RB LDF, PL6411-2nD, PL7411-2nD, RB711 series, wAP R-2nD, RB912R-2nD-LTm (LtAP mini), RB Metal series, RB SXT Lite series, RB Groove series, Cube Lite60, LHG Lite60</strong></td><td style="border: 1px solid #000000">ether1:2028</td></tr><tr><td style="border: 1px solid #000000"><strong>RB SXT G series, RB DynaDish, wAP ac, RB QRT series, RB711G series, RB911G, RB912UAG</strong></td><td style="border: 1px solid #000000">ether1:4076</td></tr><tr><td style="border: 1px solid #000000"><strong>RB OmniTik series, RB750, RB750UP, RB751U-2HnD, RB951-2n</strong></td><td style="border: 1px solid #000000"><p>ether1:4076; ether2-ether5:2028</p></td></tr><tr><td style="border: 1px solid #000000"><strong>RB OmniTik ac series, RB750GL, RB750Gr2</strong></td><td style="border: 1px solid #000000">ether1-ether5:4074</td></tr><tr><td style="border: 1px solid #000000"><strong>RB mAP, RB mAP lite, RB cAP, RB wAP</strong></td><td style="border: 1px solid #000000">ether1-ether2:2028</td></tr><tr><td style="border: 1px solid #000000"><strong>RB750r2, RB750P-PBr2, RB750UPr2, RB941-2nD, RB951Ui/RB952Ui series</strong></td><td style="border: 1px solid #000000">ether1-ether5:2028</td></tr><tr><td style="border: 1px solid #000000"><strong>RB750Gr3</strong></td><td style="border: 1px solid #000000">ether1-ether5:2026</td></tr>
<tr><td style="border: 1px solid #000000"><strong>RB751G-2HnD, RB951G-2HnD</strong></td><td style="border: 1px solid #000000">ether1-ether5:4074</td></tr><tr><td style="border: 1px solid #000000"><strong>RB962UiGS, RB960PGS</strong></td><td style="border: 1px solid #000000">ether1-ether5:4074; sfp1:4076</td></tr><tr><td style="border: 1px solid #000000"><strong>RB LHGG series</strong></td><td style="border: 1px solid #000000">ether1:9214</td></tr><tr><td style="border: 1px solid #000000"><strong>LHG XL 52 ac</strong></td><td style="border: 1px solid #000000">ether1:9214; sfp1:9214</td></tr><tr><td style="border: 1px solid #000000"><strong>RB1100Hx2, RB1100AHx2</strong></td><td style="border: 1px solid #000000">ether1-ether10:9498; ether11:9500; ether12-ether13:9116</td></tr><tr><td style="border: 1px solid #000000"><strong>RB4011iGS+ series</strong></td><td style="border: 1px solid #000000">ether1-ether10:9578; sfp-sfpplus1:9982</td></tr><tr><td style="border: 1px solid #000000"><strong>CCR1009 series</strong></td><td style="border: 1px solid #000000">ether1-ether4:10224; ether5-ether8:10226; sfp1:10226; sfp-sfpplus1:10226</td></tr><tr><td style="border: 1px solid #000000"><strong>CCR1016 series</strong></td><td style="border: 1px solid #000000">ether1-ether12:10226; sfp1-sfp12:10226; sfp-sfpplus1:10226</td></tr><tr><td style="border: 1px solid #000000"><strong>CCR1036 series</strong></td><td style="border: 1px solid #000000">ether1-ether12:10226; sfp1-sfp4:10226; sfp-sfpplus1-sfp-sfpplus2:10226</td></tr><tr><td style="border: 1px solid #000000"><strong>CCR1072 series</strong></td><td style="border: 1px solid #000000">ether1:9116; sfp-sfpplus1-sfp-sfpplus8:10226</td></tr>
<tr><td style="border: 1px solid #000000"><strong>CRS109-8G-1S</strong></td><td style="border: 1px solid #000000">ether1-ether8:4064; sfp1:4064</td></tr><tr><td style="border: 1px solid #000000"><strong>CRS125-24G-1S</strong></td><td style="border: 1px solid #000000">ether1-ether24:4064; sfp1:4064</td></tr><tr><td style="border: 1px solid #000000"><strong>CRS112-8G-4S, CRS112-8P-4S</strong></td><td style="border: 1px solid #000000">ether1-ether8:9204; sfp9-sfp12:9204</td></tr><tr><td style="border: 1px solid #000000"><strong>CRS106-1C-5S</strong></td><td style="border: 1px solid #000000">sfp1-sfp5:9204; combo1:9204</td></tr><tr><td style="border: 1px solid #000000"><strong>CRS210-8G-2S+</strong></td><td style="border: 1px solid #000000">ether1-ether8:9204; sfp-sfpplus1:9204; sfpplus2:9204</td></tr><tr><td style="border: 1px solid #000000"><strong>CRS212-1G-10S-1S+</strong></td><td style="border: 1px solid #000000">ether1:9204; sfp1-sfp10:9204; sfpplus1:9204</td></tr><tr><td style="border: 1px solid #000000"><strong>CRS226-24G-2S+</strong></td><td style="border: 1px solid #000000">ether1-ether24:9204; sfp-sfpplus1:9204; sfpplus2:9204</td></tr><tr><td style="border: 1px solid #000000"><strong>CRS326-24G-2S+, CSS326-24G-2S+</strong></td><td style="border: 1px solid #000000">ether1-ether24:10218; sfp-sfpplus1:10218; sfpplus2:10218</td></tr><tr><td style="border: 1px solid #000000"><strong>CRS317-1G-16S+</strong></td><td style="border: 1px solid #000000">ether1:10218; sfp-sfpplus1-sfp-sfpplus16:10218</td></tr><tr><td style="border: 1px solid #000000"><strong>CRS328-24P-4S+</strong></td><td style="border: 1px solid #000000">ether1-ether24:10218; sfp-sfpplus1-sfp-sfpplus4:10218</td></tr>
<tr><td style="border: 1px solid #000000"><strong>CRS328-4C-20S-4S+</strong></td><td style="border: 1px solid #000000">combo1-combo4:10218; sfp1-sfp20:10218; sfp-sfpplus1-sfp-sfpplus4:10218</td></tr><tr><td style="border: 1px solid #000000"><strong>CRS305-1G-4S+, CRS309-1G-8S+</strong></td><td style="border: 1px solid #000000">ether1:10218; sfp-sfpplus1-sfp-sfpplus4:10218</td></tr><tr><td style="border: 1px solid #000000"><strong>CRS312-4C+8XG</strong></td><td style="border: 1px solid #000000">combo1-combo4:10218; ether1-ether8:10218; ether9:2028</td></tr><tr><td style="border: 1px solid #000000"><strong>CRS326-24S+2Q+</strong></td><td style="border: 1px solid #000000">sfp-sfpplus1-sfp-sfpplus24:10218; qsfpplus1-1-qsfpplus2-4:10218; ether1:2028</td></tr><tr><td style="border: 1px solid #000000"><strong>CRS354-48G-4S+2Q+, CRS354-48P-4S+2Q+</strong></td><td style="border: 1px solid #000000">sfp-sfpplus1-sfp-sfpplus4:10218; qsfpplus1-1-qsfpplus2-4:10218; ether1-ether48:10218; ether49:2028</td></tr><tr><td style="border: 1px solid #000000"><strong>D52G-5HacD2HnD (hAP ac²)</strong></td><td style="border: 1px solid #000000">ether1-ether5:9124</td></tr><tr><td style="border: 1px solid #000000"><strong>cAP ac</strong></td><td style="border: 1px solid #000000">ether1-ether2:9124</td></tr><tr><td style="border: 1px solid #000000"><strong>GPEN21</strong></td><td style="border: 1px solid #000000">ether1-ether2:10222; sfp1: 10222</td></tr><tr><td style="border: 1px solid #000000"><strong>wAP60G,&nbsp;LHG60G</strong></td><td style="border: 1px solid #000000">ether1:9124</td></tr><tr><td style="border: 1px solid #000000"><strong>RB260GS series, CSS106-5G-1S, CSS106-1G-4P-1S</strong></td><td style="border: 1px solid #000000">ether1-ether5:9198; sfp1:9198</td></tr><tr><td style="border: 1px solid #000000"><strong>RBFTC11</strong></td><td style="border: 1px solid #000000">ether1:4046; sfp1:4046</td></tr><tr><td style="border: 1px solid #000000"><strong>RBM33G</strong></td><td style="border: 1px solid #000000">ether1-ether3:2026</td></tr><tr><td style="border: 1px solid #000000"><strong>RBM11G</strong></td><td style="border: 1px solid #000000">ether1:2026</td></tr><tr><td style="border: 1px solid #000000"><strong>RB760iGS</strong></td><td style="border: 1px solid #000000">ether1-ether5:2026; sfp1:2026</td></tr><tr><td style="border: 1px solid #000000"><strong>RB411 series</strong></td><td style="border: 1px solid #000000">ether1:1526</td></tr><tr><td style="border: 1px solid #000000"><strong>RB433 series, RB450, RB493 series</strong></td><td style="border: 1px solid #000000">ether1:1526; ether2-ether3:1522</td></tr>
<tr><td style="border: 1px solid #000000"><strong>RB450Gx4</strong></td><td style="border: 1px solid #000000">ether1-ether5:9214</td></tr><tr><td style="border: 1px solid #000000"><strong>RB411GL</strong></td><td style="border: 1px solid #000000">ether1:1520</td></tr><tr><td style="border: 1px solid #000000"><strong>RB433GL, RB435G , RB450G, RB493G</strong></td><td style="border: 1px solid #000000">ether1-ether3:1520</td></tr><tr><td style="border: 1px solid #000000"><strong>RB800</strong></td><td style="border: 1px solid #000000">ether1-ether2:9500; ether3:9116</td></tr><tr><td style="border: 1px solid #000000"><strong>RB850Gx2</strong></td><td style="border: 1px solid #000000">ether1-ether5:1580</td></tr><tr><td style="border: 1px solid #000000"><strong>RB921UAGS, RB922UAGS</strong></td><td style="border: 1px solid #000000">ether1:4076; sfp1:4076</td></tr><tr><td style="border: 1px solid #000000"><strong>D23UGS-5HPacD2HnD (NetMetal ac²)</strong></td><td style="border: 1px solid #000000">ether1:9214&nbsp;; sfp1:9214</td></tr><tr><td style="border: 1px solid #000000"><strong>RB953GS</strong></td><td style="border: 1px solid #000000">ether1-ether2:4074; sfp1:4074; sfp2:4076</td></tr><tr><td style="border: 1px solid #000000"><strong>RB2011 series</strong></td><td style="border: 1px solid #000000">ether1-ether5:4074; ether6-ether10:2028; sfp1:4074</td></tr><tr><td style="border: 1px solid #000000"><strong>RB3011 series</strong></td><td style="border: 1px solid #000000">ether1-ether5:8156; ether6-ether10:8156; sfp1:8158</td></tr><tr><td style="border: 1px solid #000000"><strong>RB5009&nbsp;</strong></td><td style="border: 1px solid #000000">ether1-ether8: 9796; sfp-sfpplus1: 9796</td></tr><tr><td style="border: 1px solid #000000"><strong>RB44Ge</strong></td><td style="border: 1px solid #000000">ether1-ether4:9116</td></tr></tbody></table>

RouterOS（包括Nstreme2）中的所有无线接口都支持2290字节的L2MTU。

L2MTU配置的改变会引起所有接口重新加载（链接下降/链接上升），这是由于必要的内部过程。 
建议谨慎配置L2MTU，牢记它可能会导致连接设备的短暂中断。

## MPLS/Layer-2.5/L2.5 MTU

在"/mpls interface "菜单中配置，指定数据包的最大尺寸，包括MPLS标签，指定特定接口发送（默认是1508）。

确保MPLS MTU小于或等于L2MTU。MPLS MTU对数据包的影响取决于MPLS路由器正在执行的动作。建议在组成MPLS云的所有路由器上将MPLS MTU配置成相同的值，因为MPLS MTU对MPLS交换的数据包有影响。这一要求意味着所有参与MPLS云的接口必须配置为参与接口中最小的MPLS MTU值，因此必须注意正确选择要使用的硬件。

### MPLS交换

如果包含标签的数据包大于MPLS的MTU，MPLS会尝试猜测MPLS帧内携带的协议。

- 如果是一个IP数据包，MPLS会产生一个ICMP需要碎片的错误。这种行为模仿了IP协议的行为。注意，这个ICMP错误不会被路由回数据包的发起者，而是被切换到LSP的末端，以便出站路由器可以将其路由回去。
- 如果不是一个IP数据包，MPLS会简单地丢弃，因为它不知道如何解释数据包的内容。在使用MPLS应用的情况下，如VPLS，这个功能非常重要（MPLS标记的帧不是IP包，而是封装的以太网帧，如VPLS的情况）-如果在LSP的某个地方，MPLS的MTU小于入站路由器准备的包的大小，帧将被简单地丢弃。

### IP入站

当路由器第一次在IP数据包上引入一个（或多个）标签，并且产生的数据包大小包括MPLS标签超过MPLS MTU时，路由器的行为就像接口MTU被超过一样--要么将数据包分割成不超过MPLS MTU的片段，当标签被附加时（如果没有设置IP Don't Fragment），要么产生ICMP Need Fragmentation错误被送回给发起者。

### VPLS入站

当路由器封装以太网帧以便在VPLS伪线上转发时，它检查数据包的大小与VPLS控制字（4字节）和任何必要的标签（通常是2个标签-8字节）是否超过了出站接口的MPLS MTU。如果是这样，VPLS会对数据包进行碎片化处理，使其符合出站接口的MPLS MTU。数据包在VPLS伪线的出口处被分解。

## 设置实例

在这些例子中，看看通过以太网接口进入和离开路由器的帧。

## 简单路由

该图显示了简单路由的数据包MTU大小，数据包大小没有修改。

![](https://help.mikrotik.com/docs/download/attachments/21725296/MTUSimpleRouting.jpg?version=1&modificationDate=1657268976520&api=v2)

## Routing with VLAN Encap

Each VLAN tag is 4 bytes long, the VLAN tag is added by a router. L2-MTU is increased by 4 bytes.

![](https://help.mikrotik.com/docs/download/attachments/21725296/MTUVLANENCAP.jpg?version=1&modificationDate=1657269006433&api=v2)  

当MPLS被用作IP路由的简单替代物时，每个数据包只附加一个标签，因此数据包的大小增加了4个字节，我们有两个MPLS标签的情况。为了能够转发标准大小（1500字节）的IP数据包而不产生碎片，MPLS的MTU必须被设置为两个MPLS标签的至少1508。

![](https://help.mikrotik.com/docs/download/attachments/21725296/MTUMPLS2Tags.jpg?version=1&modificationDate=1657269041226&api=v2)

## VPLS隧道

当一个远程端点没有直接连接时，会有两个MPLS标签。一个MPLS标签用于到达远程端点，第二个标签用于识别VPLS隧道。

![](https://help.mikrotik.com/docs/download/attachments/21725296/MTUVPLS.jpg?version=1&modificationDate=1657269060304&api=v2)

## 高级设置实例

这个例子仔细研究所有类似以太网接口所需的L2MTU，包括网桥、VLAN和VPLS接口。

在这个设置中，有3个路由器：

- Q-in-Q路由器 - 路由器接收一个标准的1500字节的以太网帧，并将两个VLAN标签添加到数据包中。然后，数据包通过一个以太网发送到第二个路由器。

- VPLS路由器 - 路由器删除外部VLAN标签，并将数据包与剩余的VLAN标签通过VPLS隧道桥接。VPLS隧道把数据包通过MPLS网络带到第三个路由器。

- MPLS边缘路由器 - 删除VPLS和VLAN标签，并将数据包桥接到客户的以太网网络。

![](https://help.mikrotik.com/docs/download/attachments/21725296/L2MTU_example.jpg?version=1&modificationDate=1657269085761&api=v2)
