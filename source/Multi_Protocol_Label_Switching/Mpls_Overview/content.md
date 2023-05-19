# 概述

MPLS即多协议标签交换。它在某种程度上取代了IP路由——数据包转发决策(出接口和下一跳路由器)不再基于IP报头(通常是目的地址)和路由表中的字段，而是基于附加在数据包上的标签。这种方法加快了转发过程，因为与路由查找(查找最长匹配前缀)相比，下一跳查找变得非常简单。

转发过程的效率是MPLS的主要优点，但必须考虑到MPLS转发不允许对网络层(如IP)报头进行处理，因此不能对MPLS转发的报文进行NAT、过滤等基于网络层的操作。任何基于网络层的操作都应该在MPLS云的入口或出口上进行，首选的方式是入口——这样，例如，无论如何都要被丢弃的流量不会通过MPLS骨干网传输。

在最简单的形式中，MPLS可以被认为是改进的路由-标签通过LDP协议分发给活动路由，并且标记的数据包采用与未标记时相同的路径。如果路由器使用从下一跳接收到标签的路由来路由未标记的数据包，在数据包上加上标签，并将其发送到下一跳，则会使MPLS沿着其路径进一步交换。当路由器收到带有标签的数据包时，将其与从特定路由的下一跳收到的标签进行更改，并将数据包发送到下一跳。标签交换路径可确保数据传输到MPLS云出口点。MPLS的应用就是基于标签交换路径这一MPLS基本概念。

另一种建立标签交换路径的方法是通过RSVP-TE协议建立流量工程隧道(traffic engineering tunnel)。流量工程隧道允许显式路由lsp和基于约束的路径选择(其中约束是接口属性和可用带宽)。

考虑到MPLS的复杂性、引入的新协议和应用，以及MPLS在路由/桥接网络中增加的概念差异，建议在生产网络中实现MPLS之前，先深入了解MPLS的概念。一些建议的阅读材料:

- 多协议标签交换 [http://en.wikipedia.org/wiki/Multiprotocol_Label_Switching](http://en.wikipedia.org/wiki/Multiprotocol_Label_Switching)
- RFC3031多协议标签交换架构 [http://www.ietf.org/rfc/rfc3031.txt](http://www.ietf.org/rfc/rfc3031.txt)
- Luc De Ghein的MPLS基础知识 [http://www.amazon.com/MPLS-Fundamentals-Luc-Ghein/dp/1587051974](http://www.amazon.com/MPLS-Fundamentals-Luc-Ghein/dp/1587051974)

SMIPS设备(hAP lite、hAP lite TC和hAP mini)不支持该特性。

# 支持的功能

目前，Routeros支持以下MPLS相关功能：

- MPLS随着倒数第二个跳跃的支持而切换
  -  IPv4和IPv6的静态本地标签绑定
  -  IPv4和IPv6的静态远程标签绑定
- IPv4和IPv6的标签分销协议（RFC 3036，RFC 5036和RFC 7552）
    - 下游未经请求的标签广告
    - 独立标签分布控制
    - 自由标签保留
    - 有针对性的会议建立
    - 可选循环检测
    - ECMP支持
 - 虚拟私人LAN服务
    - VPLS LDP信号（RFC 4762）
    - Cisco样式静态VPLS pseudowires（RFC 4447 FEC类型0x80）
    - VPLS伪片碎片和重新组装（RFC 4623）
    - 基于VPLS MP-BGP的自动发现和信号传导（RFC 4761）
    - Cisco VPLS基于BGP的自动发现（Draft-iETF-L2VPN-SIGNALING-08）
    - 支持基于BGP的VPLS多个进口/出口路线目标扩展社区（均为RFC 4761和DRAFT-EITF-L2VPN-SIGNALING-08）
 -  RSVP-TE隧道
    - 隧道头
    - 显式路径
    -  TE隧道的OSPF扩展
    - CSPF路径选择
    -  te隧道上VPL和MPLS IP VPN流量的转发
    - 入口TE隧道速率限制和自动保留带宽调整，[TE隧道带宽控制]（https://wiki.mikrotik.com/wiki/wiki/wiki/te_tunnel_auto_auto_bandwidth“ te Tunnel auto auto auto bando bando bando bando bando bando bando bandwidth”）
    - 所有隧道带宽设置均已指定并以每秒位显示
 - 基于MP-BGP的MPLS IP VPN
 - 基于MP-BGP的MPLS VPN
 - MPLS TE的OSPF扩展
 - 支持OSPF作为CE-PE协议
 - 指定VRF的ping和traceroute
 - 控制MPL中的网络层TTL传播
 - RIP作为CE-PE协议
 - VRF BGP实例重新分布设置

**routeros还没有的MPLS功能：**

- LDP功能：
      - 按需标签广告
      - 订购的标签分布控制
      - 保守标签保留率
- TE功能
      - 快速路线
      - 链接/节点保护
- 支持BGP作为标签分布协议