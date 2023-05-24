# 概述

**Standards:** `RFC 1990`

多链路点对点协议(Multi-Link Point to Point Protocol, MP, Multi-Link PPP, MultiPPP或MLPPP)是一种跨多个逻辑数据链路拆分、重组和排序数据的方法。

在一对设备上有多个DSL链路的情况下，使用多链路PPP可以通过“拓宽两个设备之间的管道”来提高性能，而无需采用更新、更昂贵的技术。

大的数据包实际上被分割成比特，并在所有逻辑数据链路上均匀发送。这是在没有带宽损失的情况下立即完成的。重要的是要理解链接的另一端需要使用相同的协议来重新组合数据。

Multilink基于 [LCP](https://wiki.mikrotik.com/index.php?title=LCP&action=edit&redlink=1 "LCP(page does not exist)") 选项协商，允许向其对等方表明它能够组合多个物理链路。

# MLPPP单链路

通常，由于开销的原因，PPP链路上发送的数据包大小会减小。MP可用于在单个ppp链路上发送和接收全帧。为了使它工作，多链路协议使用额外的LCP配置选项 **多链路最大接收重构单元(MRRU)**

为了在单链路上启用多链路PPP，必须指定MRRU(最大接收重构单元)选项。如果双方都支持此功能，则不需要调整MSS(在防火墙管理中)。研究表明，MRRU对CPU的消耗比每个客户端2条规则要少。MRRU允许将数据包分成多个通道，从而增加可能的MTU和MRU(最多65535字节)。

在Windows下，它可以在网络标签，设置按钮，“协商多链路为单链路连接”中启用。他们的MRRU编码是1614。

当启用MPPE加密时，MTU将减少4个字节才能正常工作

## 配置示例

配置与Windows客户端兼容的pppoe server，并使能MRRU。

```shell
[admin@RB800] /interface pppoe-server server> add service-name=myPPP interface=ether1 mrru=1614
[admin@RB800] /interface pppoe-server server> print
Flags: X - disabled
 0   service-name="myPPP" interface=ether1 max-mtu=1480 max-mru=1480 mrru=1614
     authentication=pap,chap,mschap1,mschap2 keepalive-timeout=10 one-session-per-host=no
     max-sessions=0 default-profile=default
```

简而言之，标准PPP链路-只需在两端指定MRRU即可。

# MLPPP多链路

MLPPP over multiple links允许在多个物理连接上创建一条PPP链路。所有PPP链路必须来自同一服务器(服务器必须支持MLPPP over多链路)，所有PPP链路必须具有相同的用户名和密码。

要启用MLPPP，您只需要创建PPP客户端并指定多个接口而不是单个接口。RouterOS只支持MLPPP客户端。目前没有可用的MLPPP服务器支持。

## 配置示例

![](https://help.mikrotik.com/docs/download/attachments/132350045/Mlppp.jpg?version=1&modificationDate=1657264990603&api=v2)

ISP给它的客户提供两条物理链路(DSL线)，每条1Mbps。为了获得2Mbps的聚合管道，我们必须设置MLPPP。考虑ISP路由器被预配置为支持MLPPP。

路由器R1上的配置如下:

```shell
/interface pppoe-client
   add service-name=ISP interface=ether1,ether2 user=xxx password=yyy disabled=no \
   add-default-route=yes use-peer-dns=yes
```

```shell
[admin@RB800] /interface pppoe-client> print
Flags: X - disabled, R - running
 0    name="pppoe-out1" max-mtu=1480 max-mru=1480 mrru=disabled interface=ether1,ether2
      user="xxx" password="yyy" profile=default service-name="ISP" ac-name="" add-default-route=yes
      dial-on-demand=no use-peer-dns=yes allow=pap,chap,mschap1,mschap2
```

现在，当PPPoE客户端连接时，可以设置其余的配置，本地网络地址，启用DNS请求，设置伪装和防火墙

```shell
/ip address add address=192.168.88.1/24 interface=local
 
/ip dns set allow-remote-request=yes
 
/ip firewall nat
add chain=src-nat action=masquerade out-interface=pppoe-out1
 
/ip firewall filter
add chain=input connection-state=invalid action=drop \
    comment="Drop Invalid connections" 
add chain=input connection-state=established action=accept \
    comment="Allow Established connections" 
add chain=input protocol=icmp action=accept \
    comment="Allow ICMP"
add chain=input src-address=192.168.88.0/24 action=accept \
    in-interface=!pppoe-out1
add chain=input action=drop comment="Drop everything else"
```

有关更高级的路由器和客户保护，请查看 [防火墙示例](https://help.mikrotik.com/docs/display/ROS/Filter) 。