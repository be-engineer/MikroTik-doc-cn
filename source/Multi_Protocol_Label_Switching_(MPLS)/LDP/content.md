# 概述

MikroTik RouterOS针对IPv4和IPv6地址族实现了标签分发协议(RFC 3036、RFC 5036和RFC 7552)。LDP是lsr (Label Switched Routers)通过网络将网络层路由信息直接映射到数据链路层交换路径上，从而建立lsp的一组过程和交换消息的协议。

# MPLS的先决条件

“回环”IP地址

虽然没有严格的要求，但建议在参与MPLS网络的路由器上配置“回环”IP地址(不附加在任何真实的网络接口上)，供LDP建立会话使用。
这有两个目的:

- 由于任意两台路由器之间只有一个LDP会话，因此无论连接它们的链路有多少，回环 IP地址都可以确保LDP会话不受接口状态或地址变化的影响
- 使用回环地址作为LDP传输地址，可以保证在报文附加多个标签(如VPLS)时正确的倒数第二跳弹出行为

在RouterOS中，“回环”IP地址可以通过创建一个没有任何端口的虚拟网桥接口来配置，并将该地址添加到该接口中。例如:

```shell
/interface bridge add name=lo
/ip address add address=255.255.255.1/32 interface=lo
```


## IP连接

由于LDP为活动路由分配标签，因此基本要求是正确配置IP路由。缺省情况下，LDP对活动的IGP路由(即非连接路由、静态路由和路由协议学习路由，BGP除外)分发标签。

有关如何正确设置IGP的说明，请参阅相应的文档部分:

- [OSPF](https://help.mikrotik.com/docs/display/ROS/OSPF)
- [静态路由](https://help.mikrotik.com/docs/display/ROS/IP+Routing)


LDP支持ECMP路由。

在继续进行LDP配置之前，您应该能够从网络的任何位置访问任何环回地址。可以使用从loopback地址到loopback地址的ping工具来验证连通性。

# 示例设置

考虑已经设置了四个路由器，具有工作IP连接。

```shell
   (lo:111.111.111.1)       (lo:111.111.111.2)          (lo:111.111.111.3)         (lo:111.111.111.4)
|---------R1-----(111.11.0.0/24)-----R2-----(111.12.0.0/24)-----R3-----(111.13.0.0/24)-----R4---------|
```

  

### Ip可达性

不深入路由设置，导出这是IP和OSPF配置:

```shell
#R1
/interface bridge
add name=loopback
/ip address
add address=111.11.0.1/24 interface=ether2
add address=111.111.111.1 interface=loopback
 
/routing ospf instance
add name=default_ip4 router-id=111.111.111.1
/routing ospf area
add instance=default_ip4 name=backbone_ip4
/routing ospf interface-template
add area=backbone_ip4 dead-interval=10s hello-interval=1s networks=111.111.111.1
add area=backbone_ip4 dead-interval=10s hello-interval=1s networks=111.11.0.0/24
 
 
#R2
/interface bridge
add name=loopback
/ip address
add address=111.11.0.2/24 interface=ether2
add address=111.12.0.1/24 interface=ether3
add address=111.111.111.2 interface=loopback
 
/routing ospf instance
add name=default_ip4 router-id=111.111.111.2
/routing ospf area
add instance=default_ip4 name=backbone_ip4
/routing ospf interface-template
add area=backbone_ip4 dead-interval=10s hello-interval=1s networks=111.111.111.2
add area=backbone_ip4 dead-interval=10s hello-interval=1s networks=111.11.0.0/24
add area=backbone_ip4 dead-interval=10s hello-interval=1s networks=111.12.0.0/24
 
 
#R3
/interface bridge
add name=loopback
 
/ip address
add address=111.12.0.2/24 interface=ether2
add address=111.13.0.1/24 interface=ether3
add address=111.111.111.3 interface=loopback
 
/routing ospf instance
add name=default_ip4 router-id=111.111.111.3
/routing ospf area
add instance=default_ip4 name=backbone_ip4
/routing ospf interface-template
add area=backbone_ip4 dead-interval=10s hello-interval=1s networks=111.111.111.3
add area=backbone_ip4 dead-interval=10s hello-interval=1s networks=111.12.0.0/24
add area=backbone_ip4 dead-interval=10s hello-interval=1s networks=111.13.0.0/24
 
 
#R4
/interface bridge
add name=loopback
/ip address
add address=111.13.0.2/24 interface=ether2
add address=111.111.111.4 interface=loopback
 
/routing ospf instance
add name=default_ip4 router-id=111.111.111.4
/routing ospf area
add instance=default_ip4 name=backbone_ip4
/routing ospf interface-template
add area=backbone_ip4 dead-interval=10s hello-interval=1s networks=111.111.111.4
add area=backbone_ip4 dead-interval=10s hello-interval=1s networks=111.13.0.0/24
Verify that IP connectivity and routing are working properly

[admin@R4] /ip/address> /tool traceroute 111.111.111.1 src-address=111.111.111.4
Columns: ADDRESS, LOSS, SENT, LAST, AVG, BEST, WORST, STD-DEV
#  ADDRESS        LOSS  SENT  LAST   AVG  BEST  WORST  STD-DEV
1  111.13.0.1     0%       4  0.6ms  0.6  0.6   0.6    0     
2  111.12.0.1     0%       4  0.5ms  0.6  0.5   0.6    0.1   
3  111.111.111.1  0%       4  0.6ms  0.6  0.6   0.6    0     
```

  

## LDP设置

为了分发标签，需要在连接其他LDP路由器的接口上使能LDP，而在连接客户网络的接口上不使能LDP。

在R1上是这样的:

```shell
/mpls ldp
add afi=ip lsr-id=111.111.111.1 transport-addresses=111.111.111.1
/mpls ldp interface
add interface=ether2    
```

注意，传输地址设置为111.111.111.1。路由器使用此地址发起LDP会话连接，并将此地址作为传输地址通告给LDP邻居。



其他路由器的设置也类似。

R2:

```shell
/mpls ldp
add afi=ip lsr-id=111.111.111.2 transport-addresses=111.111.111.2
/mpls ldp interface
add interface=ether2  
add interface=ether3  
```

R3:

```shell
/mpls ldp
add afi=ip lsr-id=111.111.111.3 transport-addresses=111.111.111.3
/mpls ldp interface
add interface=ether2  
add interface=ether3 
```

R4:

```shell
/mpls ldp
add afi=ip lsr-id=111.111.111.4 transport-addresses=111.111.111.4
/mpls ldp interface
add interface=ether2  
```

LDP会话建立后，R2应该有两个LDP邻居:

```shell
[admin@R2] /mpls/ldp/neighbor> print
Flags: D, I - INACTIVE; O, T - THROTTLED; p - PASSIVE
Columns: TRANSPORT, LOCAL-TRANSPORT, PEER, ADDRESSES
#     TRANSPORT      LOCAL-TRANSPORT  PEER             ADDRESSES   
0 DO  111.111.111.1  111.111.111.2    111.111.111.1:0  111.11.0.1  
                                                       111.111.111.1
1 DOp 111.111.111.3  111.111.111.2    111.111.111.3:0  111.12.0.2  
                                                       111.13.0.1  
                                                       111.111.111.3
```
 

本地映射表显示了路由器将标签分配给了哪些路由和对等体。

```shell
[admin@R2] /mpls/ldp/local-mapping> print
Flags: I - INACTIVE; D - DYNAMIC; E - EGRESS; G - GATEWAY; L - LOCAL
Columns: VRF, DST-ADDRESS, LABEL, PEERS
#       VRF   DST-ADDRESS      LABEL      PEERS         
0  D G  main  10.0.0.0/8       16         111.111.111.1:0
                                          111.111.111.3:0
1 IDE L main  10.155.130.0/25  impl-null  111.111.111.1:0
                                          111.111.111.3:0
2 IDE L main  111.11.0.0/24    impl-null  111.111.111.1:0
                                          111.111.111.3:0
3 IDE L main  111.12.0.0/24    impl-null  111.111.111.1:0
                                          111.111.111.3:0
4 IDE L main  111.111.111.2    impl-null  111.111.111.1:0
                                          111.111.111.3:0
5  D G  main  111.111.111.1    17         111.111.111.1:0
                                          111.111.111.3:0
6  D G  main  111.111.111.3    18         111.111.111.1:0
                                          111.111.111.3:0
7  D G  main  111.111.111.4    19         111.111.111.1:0
                                          111.111.111.3:0
8  D G  main  111.13.0.0/24    20         111.111.111.1:0
                                          111.111.111.3:0
```
  

另一方面，远程映射表显示邻居LDP路由器为路由分配的标签，并向本路由器发布。

```shell
[admin@R2] /mpls/ldp/remote-mapping> print
Flags: I - INACTIVE; D - DYNAMIC
Columns: VRF, DST-ADDRESS, NEXTHOP, LABEL, PEER
 #    VRF   DST-ADDRESS      NEXTHOP     LABEL      PEER          
 0 ID main  10.0.0.0/8                   16         111.111.111.1:0
 1 ID main  10.155.130.0/25              impl-null  111.111.111.1:0
 2 ID main  111.11.0.0/24                impl-null  111.111.111.1:0
 3 ID main  111.12.0.0/24                17         111.111.111.1:0
 4  D main  111.111.111.1    111.11.0.1  impl-null  111.111.111.1:0
 5 ID main  111.111.111.2                19         111.111.111.1:0
 6 ID main  111.111.111.3                20         111.111.111.1:0
 7 ID main  111.111.111.4                21         111.111.111.1:0
 8 ID main  111.13.0.0/24                18         111.111.111.1:0
 9 ID main  0.0.0.0/0                    impl-null  111.111.111.3:0
10 ID main  111.111.111.2                16         111.111.111.3:0
11 ID main  111.111.111.1                18         111.111.111.3:0
12  D main  111.111.111.3    111.12.0.2  impl-null  111.111.111.3:0
13  D main  111.111.111.4    111.12.0.2  19         111.111.111.3:0
14 ID main  10.155.130.0/25              impl-null  111.111.111.3:0
15 ID main  111.11.0.0/24                17         111.111.111.3:0
16 ID main  111.12.0.0/24                impl-null  111.111.111.3:0
17  D main  111.13.0.0/24    111.12.0.2  impl-null  111.111.111.3:0
```

  

可以观察到路由器已经从它的邻居R1和R3接收到所有路由的标签绑定。

远程映射表将仅对具有直接下一跳的目的地具有活动映射，例如，仔细查看111.111.111.4映射。由路由表可知，网络111.111.111.4可以通过111.12.0.2 (R3)到达:

```shell
[admin@R2] /ip/route> print where dst-address=111.111.111.4
Flags: D - DYNAMIC; A - ACTIVE; o, y - COPY
Columns: DST-ADDRESS, GATEWAY, DISTANCE
    DST-ADDRESS       GATEWAY            DISTANCE
DAo 111.111.111.4/32  111.12.0.2%ether3       110
```

如果再看一下远程映射表，唯一的活动映射是从R3接收到的标签为19的映射。这意味着当R2将流量路由到此网络时，将强加19号标签。

`17  D main  111.111.111.4    111.12.0.2  19         111.111.111.3:0`

  

在转发表中可以看到标签交换规则:

```shell
[admin@R2] /mpls/forwarding-table> print
Flags: L, V - VPLS
Columns: LABEL, VRF, PREFIX, NEXTHOPS
#   LABEL  VRF   PREFIX         NEXTHOPS                                           
0 L    16  main  10.0.0.0/8     { nh=10.155.130.1; interface=ether1 }              
1 L    18  main  111.111.111.3  { label=impl-null; nh=111.12.0.2; interface=ether3 }
2 L    19  main  111.111.111.4  { label=19; nh=111.12.0.2; interface=ether3 }      
3 L    20  main  111.13.0.0/24  { label=impl-null; nh=111.12.0.2; interface=ether3 }
4 L    17  main  111.111.111.1  { label=impl-null; nh=111.11.0.1; interface=ether2 }
```

如果看一下规则2，规则说，当R2收到标签为19的数据包时，它将把标签更改为新标签19(由R3分配)。

从这个例子中可以看到，路径上的标签并不一定是唯一的。



现在看一下R3的转发表:

```shell
[admin@R3] /mpls/forwarding-table> print
Flags: L, V - VPLS
Columns: LABEL, VRF, PREFIX, NEXTHOPS
#   LA  VRF   PREFIX         NEXTHOPS                                           
0 L 19  main  111.111.111.4  { label=impl-null; nh=111.13.0.2; interface=ether3 }
1 L 17  main  111.11.0.0/24  { label=impl-null; nh=111.12.0.1; interface=ether2 }
2 L 16  main  111.111.111.2  { label=impl-null; nh=111.12.0.1; interface=ether2 }
3 L 18  main  111.111.111.1  { label=17; nh=111.12.0.1; interface=ether2 }
```

规则0表示输出标签为 **impl-null**。这样做的原因是R3是111.111.111.4之前的最后一跳，不需要交换到任何真实的标签。已知R4是111.111.111.4网络的出口点(路由器是直连网络的出口点，因为流量的下一跳不是MPLS路由器)，因此它为该路由发布“隐式null”标签。这告诉R3将目的地111.111.111.4/32的流量转发到未标记的R4，这正是R3转发表项所告诉的。

当标签没有交换到任何实际标签时，称为倒数第二跳弹出，确保路由器在事先知道路由器必须路由数据包时不必进行不必要的标签查找。

  

# 在MPLS网络中使用traceroute

RFC4950为MPLS引入了对ICMP协议的扩展。基本思想是，一些ICMP消息可能携带MPLS“标签堆栈对象”(当它引起特定ICMP消息时，包上的标签列表)。MPLS关心的ICMP消息是超时和需要分片。

MPLS标签不仅包含标签值，还包含TTL字段。在IP报文上添加标签时，将MPLS TTL设置为IP报头中的值，当IP报文的最后一个标签被移除时，将IP TTL设置为MPLS TTL中的值。因此，可以使用支持MPLS扩展的traceroute工具对MPLS交换网络进行诊断。

例如，从R4到R1的跟踪路由是这样的:

```shell
[admin@R1] /mpls/ldp/neighbor> /tool traceroute 111.111.111.4 src-address=111.111.111.1
Columns: ADDRESS, LOSS, SENT, LAST, AVG, BEST, WORST, STD-DEV, STATUS
#  ADDRESS        LOSS  SENT  LAST   AVG  BEST  WORST  STD-DEV  STATUS        
1  111.11.0.2     0%       2  0.7ms  0.7  0.7   0.7          0  <MPLS:L=19,E=0>
2  111.12.0.2     0%       2  0.4ms  0.4  0.4   0.4          0  <MPLS:L=19,E=0>
3  111.111.111.4  0%       2  0.5ms  0.5  0.5   0.5          0
```

  

Traceroute结果显示产生ICMP超时报文上的MPLS标签。上面的意思是:当R3接收到一个MPLS TTL为1的数据包时，它的标签为18。这场比赛由R3为111.111.111.4广告标签。以同样的方式，R2在下一个traceroute迭代中观察到数据包上的标签17 - R3将标签17切换到标签17，如上所述。R1收到没有标签的数据包- R2像上面解释的那样做倒数第二跳弹出。



在MPLS网络中使用traceroute的缺点

标签交换ICMP错误

在MPLS网络中使用traceroute的缺点之一是MPLS处理产生的ICMP错误的方式。在IP网络中，ICMP错误被简单地路由回引起错误的数据包的源。在MPLS网络中，产生错误消息的路由器甚至可能没有到IP数据包源的路由(例如在非对称标签交换路径或某种MPLS隧道的情况下，例如传输MPLS VPN流量)。

由于产生的ICMP错误不会路由到引起错误的数据包的源，而是沿着标签交换路径进一步交换，假设当标签交换路径端点接收到ICMP错误时，它将知道如何正确地将其路由回源。

这导致在MPLS网络中不能像在IP网络中那样使用traceroute来确定网络中的故障点。如果标签交换路径在中间的任何地方中断，则不会返回ICMP应答，因为它们不会到达标签交换路径的远端点。

倒数第二跳弹出和traceroute源地址

彻底了解倒数第二跳的行为和路由是理解和避免倒数第二跳弹出导致traceroute问题的必要条件。

在示例设置中，从R5到R1的常规跟踪路由将产生以下结果:

```shell
[admin@R5] > /tool traceroute 9.9.9.1
     ADDRESS                                    STATUS
   1         0.0.0.0 timeout timeout timeout
   2         2.2.2.2 37ms 4ms 4ms
                      mpls-label=17
   3         9.9.9.1 4ms 2ms 11ms

```

比较:

```shell
[admin@R5] > /tool traceroute 9.9.9.1 src-address=9.9.9.5
     ADDRESS                                    STATUS
   1         4.4.4.3 15ms 5ms 5ms
                      mpls-label=17
   2         2.2.2.2 5ms 3ms 6ms
                      mpls-label=17
   3         9.9.9.1 6ms 3ms 3ms

```

第一个traceroute没有得到R3的响应的原因是，默认情况下，R5上的traceroute使用源地址4.4.4.5作为其探测，因为它是路由的首选源，下一跳可以到达9.9.9.1/32。

```shell
[admin@R5] > /ip route print
Flags: X - disabled, A - active, D - dynamic,
C - connect, S - static, r - rip, b - bgp, o - ospf, m - mme,
B - blackhole, U - unreachable, P - prohibit
 #      DST-ADDRESS        PREF-SRC        G GATEWAY         DISTANCE             INTERFACE
 ...
 3 ADC  4.4.4.0/24         4.4.4.5                           0                    ether1
 ...
 5 ADo  9.9.9.1/32                         r 4.4.4.3         110                  ether1
 ...

```

当发送第一个traceroute探测(源:4.4.4.5，目的9.9.9.1)时，R3丢弃它并产生一个ICMP错误消息(源4.4.4.3，目的4.4.4.5)，该消息一路切换到R1。然后R1发送回ICMP错误——它沿着标签交换路径切换到4.4.4.5。

R2是网络4.4.4.0/24的倒数第二个跳跳路由器，因为4.4.4.0/24直接连接到R3。因此，R2删除最后一个标签，并发送ICMP错误给无标签的R3:

```shell
[admin@R2] > /mpls forwarding-table print
 # IN-LABEL             OUT-LABELS           DESTINATION        INTERFACE            NEXTHOP
 ...
 3 19                                        4.4.4.0/24         ether2               2.2.2.3
 ...

```

R3会丢弃接收到的IP数据包，因为它收到了一个以自己的地址作为源地址的数据包。以下探测产生的ICMP错误会正确返回，因为R3接收到源地址为2.2.2.2和9.9.9.1的未标记数据包，这是路由可以接受的。

命令:

```shell
[admin@R5] > /tool traceroute 9.9.9.1 src-address=9.9.9.5
 ...

```

产生预期的结果，因为traceroute探测的源地址是9.9.9.5。当ICMP错误从R1返回到R5时，9.9.9.5/32网络的倒数第二跳发生在R3，因此它永远不会用自己的地址作为源地址路由数据包。

# 优化标签分配

标签绑定过滤

在实现给定示例设置期间，很明显并非所有标签绑定都是必需的。例如，不需要在R1和R3或R2和R4之间交换IP路由标签绑定，因为它们永远不会被使用。此外，如果给定的网络核心仅为所提到的客户以太网段提供连接，则没有必要为它们之间连接路由器的网络分发标签，唯一重要的路由是到端点或附加客户网络的/32路由。

通过标签绑定过滤，可以只分发指定的标签集，以减少资源使用和网络负载。

有两种类型的标签绑定过滤器:

-在“/mpls LDP advertise-filter”菜单中配置向LDP邻居通告哪些标签绑定
-从LDP邻居接收哪些标签绑定，在/mpls LDP accept-filter菜单中配置

过滤器在有序列表中组织，指定的前缀必须包含针对过滤器和邻居(或通配符)进行测试的前缀。

在给定的示例设置中，可以配置所有路由器，以便它们仅为允许到达隧道端点的路由发布标签。为此，需要在所有路由器上配置2个通告过滤器:

```shell
/mpls ldp advertise-filter add prefix=111.111.111.0/24 advertise=yes
/mpls ldp advertise-filter add prefix=0.0.0.0/0 advertise=no
```


该过滤器使路由器只发布包含111.111.111.0/24前缀的路由绑定，该前缀包括环回(111.111.111.1/32、111.111.111.2/32等)。第二条规则是必要的，因为当没有规则匹配时，默认过滤器将允许所讨论的操作。

在给定的设置中，不需要设置接受过滤器，因为根据上述2条规则引入的约定，没有LDP路由器会分发不必要的绑定。

注意，过滤器的更改不会影响现有的映射，因此要使过滤器生效，需要重置邻居之间的连接。可以从LDP邻居表中删除邻居，也可以重启LDP实例。

例如，在R2上得到:

```shell
[admin@R2] /mpls/ldp/remote-mapping> print
Flags: I - INACTIVE; D - DYNAMIC
Columns: VRF, DST-ADDRESS, NEXTHOP, LABEL, PEER
#    VRF   DST-ADDRESS    NEXTHOP     LABEL      PEER          
0 ID main  111.111.111.2              17         111.111.111.3:0
1 ID main  111.111.111.1              16         111.111.111.3:0
2  D main  111.111.111.3  111.12.0.2  impl-null  111.111.111.3:0
3  D main  111.111.111.4  111.12.0.2  18         111.111.111.3:0
4 ID main  111.111.111.2              16         111.111.111.1:0
5  D main  111.111.111.1  111.11.0.1  impl-null  111.111.111.1:0
6 ID main  111.111.111.3              17         111.111.111.1:0
7 ID main  111.111.111.4              18         111.111.111.1:0
```

  

# LDP on Ipv6和Dual-Stack链路

RouterOS采用RFC 7552实现了在双栈链路上支持LDP。

支持的afi可以根据LDP实例选择，也可以根据每个LDP接口显式配置。

```shell
/mpls ldp
add afi=ip,ipv6 lsr-id=111.111.111.1 preferred-afi=ipv6
/mpls ldp interface
add interface=ether2 afi=ip
add interface=ether3 afi=ipv6
```

上面的示例使能LDP实例使用IPv4和IPv6地址族，并通过参数preferred-afi设置优先级为IPv6。另一方面，LDP接口配置显式设置 **ether2** 只支持IPv4， **ether3** 只支持IPv6。



主要的问题是，当有不同的AFI混合时，如何选择AFI，以及如果支持的AFI之一发生皮瓣移位怎么办。

发送hello背后的逻辑如下:

- 如果一个接口只有一个AFI:- 不发送双栈元素
  - 仅当接口上存在对应AFI的IP地址时才发送hello。
- 如果一个接口有两个afi:
  - 总是发送双栈元素，并且包含来自preferred-afi的值
  - 如果接口上有对应的地址，则对每个AFI发送hello。

  

从所有收到的hello中，对等体决定使用哪个AFI进行连接，以及为哪个AFI绑定和发送标签。为了使LDP能够使用特定的AFI，接收特定AFI的hello是强制性的。Hello报文中包含LDP正常运行所必需的传输地址。通过比较收到的AFI地址，确定主动/被动角色。

接收和处理hello的逻辑如下:

- 如果LDP实例只有一个AFI(这意味着所有接口只能有特定的AFI操作):
  - 从不支持的AFI中删除hello
  - 忽略/忘记hello报文的双栈元素
  - 这个角色只针对一个特定的AFI
  - 标签只发送给这一个特定的AFI
- 如果LDP实例有两个afi(接口可以有不同的afi支持组合):
  - 删除接口不支持的来自AFI的hello。
  - 如果一个接口只支持一种AFI，忽略/忘记hello报文的双栈元素(不考虑优先级)。
  - 如果收到的优先级与配置的'preferred-afi'不匹配，则丢弃hello。

  

如果Hello数据包发生更改，则仅在更改标签使用的地址系列的情况下，现有会话才会终止，否则将保留会话。

仅当确定接口兼容界面时，Hello数据包中的双堆栈元素才设置。

 - 通常，这样的界面应该能够从两个AFI中接收Hellos，
      - 在继续前进之前，应等待首选AFI的您好。
      - 如果仅从一个AFI收到Hello：
          - 如果未收到首选AFI的Hello，则将其视为错误。
          - 否则，请等待缺少X秒的Hello（x = 3 \* Hello-Interval）
              - 如果缺少Hello出现在时间间隔内
              - 如果缺少Hello
              - 如果缺少Hello在时间间隔之后出现，请重新启动会话。
 - 双堆栈元素表明LDP想要为两个AFIS分发标签。

综上所述，假设preferred-afi=ipv6，以下afi和双栈元素(ds6)的组合是可能的:

1.  ipv4 -等待X秒，如果没有变化，则使用ipv4 LDP会话并分发ipv4标签
2.  ipv4+ds6 - wait for IPv6 hello，双栈元素表示应该有IPv6
3.ipv6 -等待X秒，如果没有变化，则使用ipv6 LDP会话并分发ipv6标签
4.  ipv6+ds6 -使用ipv6 LDP会话，分发ipv6标签
5.  ipv4、ipv6 -使用ipv6 LDP会话，分配ipv4和ipv6标签
6.  ipv4、ipv6+ds6 -使用ipv6 LDP会话，分配ipv4和ipv6标签

# 属性参考

## LDP实例


**Sub-menu:** `/mpls`

**属性**

| 属性                                                | 描述                                                                                               |
| --------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| **afi** (_ip\| ipv6_;Default:)                      | 由实例确定支持的地址族。                                                                           |
| **comments** (_string_;Default:)                    | 条目的简短描述                                                                                     |
| **disabled** (_yes \| no_;Default:**no**)           |                                                                                                    |  |
| **distribute-for-default** (_yes\| no_;Default: no) | 定义是否为默认路由映射标签。                                                                       |
| **hop-limit** (_integer[0..255]_;Default:)          | 用于环路检测的最大跳数限制。与 **loop-detect** 属性结合使用。                                      |
| **loop-detect** (_yes\| no_; Default: )             | 定义是否进行LSP环路检测。如果没有在所有lsr上启用，将无法正常工作。应该只在非ttl网络(如atm)上使用。 |
| **lsr-id** (_IP_;Default:)                          | 唯一标签交换路由器的ID。                                                                           |
| **path-vector-limit** (_IP_;Default:)               | 用于循环检测的最大路径矢量限制。与 **loop-detect** 属性结合使用。                                  |
| **preferred-afi** (ip\| ipv6; Default: **ipv6**)    | 确定首选哪个地址族连接。Value也可以在双栈元素中设置(如果使用的话)。                                |
| **transport-addresses** (_IP_;Default:)             | 指定LDP会话连接的起始地址，并将这些地址作为传输地址发布给LDP邻居。                                 |
| **use-explicit-null** (_yes\| no_;Default:no)       | 是否分发显式空标签绑定。                                                                           |
| **vrf** (_name;Default:**main**)                    | 该实例将操作的VRF表名。                                                                            |

## 接口

**Sub-menu:** `/mpls ldp interface`

  

| 属性                                               | 说明                                                                                                              |
| -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| **afi (**_ip\| ipv6_**;**Default:**)**             | 确定接口地址族。只有配置为实例支持的afi才会被考虑在内。如果没有显式指定该值，则认为它等于实例支持的afi。          |
| **accept-dynamic-neighbors** (_yes\| no_;Default:) | 定义是动态发现邻居，还是只使用 [LDP neighbors menu](https://help.mikrotik.com/docs/display/ROS/LDP#LDP-Neighbors) | 中静态配置的邻居 |
| **comments** (_string_;Default:)                   | 条目的简短描述                                                                                                    |
| **disabled** (_yes \| no_;Default:**no**)          |                                                                                                                   |
| **hello-interval** (_string_;Default:)             | 路由器在指定接口上发送hello报文的时间间隔。缺省值是5s。                                                           |
| **hold-time** (_string_;Default:)                  | 指定在接口上发现邻居后宣布为不可达的时间间隔。缺省值是15秒。                                                      |
| **interface** (_string_;Default:)                  | LDP监听的接口名或接口列表名。                                                                                     |
| **transport-addresses** (List of _IPs_;Default:)   | 使用的传输地址与LDP实例设置不同。                                                                                 |

  

## 邻居

**Sub-menu:** `/mpls ldp neighbor`

发现和静态配置的LDP邻居列表。

**属性**

| 属性                                      | 说明                                             |
| ----------------------------------------- | ------------------------------------------------ |
| **comments** (_string_;Default:)          | 条目的简短描述                                   |
| **disabled** (_yes \| no_;Default:**no**) |
|                                           |
| **send-target** (_yes \| no_;Default:)    | 是否尝试发送目标hello，用于目标(非直连)LDP会话。 |
| **transport** (_IP_;Default:)             | 远程传输地址。                                   |

  

**只读属性**

| 属性                                   | 说明                                       |
| -------------------------------------- | ------------------------------------------ |
| **active-connect** (_yes\| no_)        |                                            |
| **addresses** (_list of IPs_)          | 发现的邻居地址列表                         |
| **inactive** (_yes\| no_)              | 绑定是否激活，是否可以选择作为转发的候选。 |
| **dynamic** (_yes\| no_)               | 条目是否被动态添加                         |
| **local-transport** (_IP_)             | 选择的本地传输地址。                       |
| **on-demand** (_yes\| no_)             |                                            |
| **operational** (_yes\| no_)           | 对端是否可操作。                           |
| **passive** (_yes\| no_)               | 对端是否处于被动状态。                     |
| **passive-wait** (_yes\| no_)          |                                            |
| **path-vector-limit** (_integer_)      |                                            |
| **peer** (_IP:integer_)                | 邻居的LSR-ID和标签空间                     |
| **sending-targeted-hello**(_yes\| no_) | 是否向邻居发送目标hello。                  |
| **throtted** (_yes\| no_)              |                                            |
| **Used - AFI** (_yes\| no_)            | 用于传输的AFI                              |
| **vpls** (_yes\| no_)                  | 邻居是否被vpls隧道使用                     |

## 接受滤波器

**Sub-menu:** `/mpls ldp accept-filter`

LDP邻居应该接受的标签绑定列表。

| 属性                                     | 说明                               |
| ---------------------------------------- | ---------------------------------- |
| **accept** (_yes\| no_;Default:)         | 是否接受邻居对指定前缀的标签绑定。 |
| **comments** (_string_;Default:)         | 条目的简短描述                     |
| **disabled** (_yes\| no_;Default:**no**) |                                    |
| **neighbor** (_string_;Default:)         | 该过滤器应用的邻居。               |
| **prefix** (_IP/mask_;Default:)          | 匹配的前缀。                       |
| **vrf** (name; Default: )                |                                    |  |

  

## 广告过滤器

**Sub-menu:** `/mpls ldp advertise-filter`

应该通告给LDP邻居的标签绑定列表。

| 属性                                      | 说明                               |
| ----------------------------------------- | ---------------------------------- |
| **advertise** (_yes\| no_;Default:)       | 是否向指定前缀的邻居通告标签绑定。 |
| **comments** (_string_;Default:)          | 条目的简短描述                     |
| **disabled** (_yes \| no_;Default:**no**) |                                    |
| **neighbor**(_string_;Default:)           | 该过滤器应用的邻居。               |
| **prefix** (_IP/mask_;Default:)           | 匹配的前缀。                       |
| **vrf** (name; Default: )                 |                                    |  |

## 本地映射

**Sub-menu:** `/mpls local-mapping`

该子菜单显示与路由器本地路由绑定的标签。在这个菜单中，如果不打算动态使用LDP，也可以配置静态映射。


**属性**

| 属性                                                                                                      | 说明                     |
| --------------------------------------------------------------------------------------------------------- | ------------------------ |
| **comments** (_string_;Default:)                                                                          | 条目的简短描述           |
| **disabled** (_yes\| no_;Default:**no**)                                                                  |                          |
| **dst-address** (_IP/Mask_;Default:)                                                                      | 指定标签的目的前缀。     |
| **label** (_integer[0..][1048576]\| alert\| expli -null \| expli -null6 \| impli -null \| none_;Default:) | 分配给目的地的标签编号。 |
| **vrf** (_name_;Default:main)                                                                             | 该映射所属的VRF表名。    |

  
**只读属性**

| 属性                         | 说明                                       |
| ---------------------------- | ------------------------------------------ |
| **adv-path** ()              |                                            |
| **inactive** (_yes\| no_)    | 绑定是否激活，是否可以选择作为转发的候选。 |
| **dynamic** (_yes\| no_)     | 条目是否被动态添加                         |
| **egress** (_yes\| no_)      |
| **gateway** (_yes\| no_)     | 是否可通过网关到达目的地。                 |
| **local** (_yes\| no_)       | 目的地在路由器上是否可达                   |
| **peers** (_IP:label space_) | 被发布到的对等体的IP地址和标签空间。       |

## 远程映射

**Sub-menu:** `/mpls remote-mapping`

子菜单显示从其他路由器接收的路由的标签绑定。如果不打算动态使用LDP，可以配置静态映射。该表用于建立 [转发表](https://help.mikrotik.com/docs/display/ROS/Mpls+Overview#MplsOverview-ForwardingTable)

**属性**

| 属性                                                                                                        | 说明                     |
| ----------------------------------------------------------------------------------------------------------- | ------------------------ |
| **comments** (_string_;Default:)                                                                            | 条目的简短描述           |
| **disabled** (_yes\| no_;Default:**no**)                                                                    |                          |  |
| **dst-address** (_IP/Mask_;Default:)                                                                        | 指定标签的目的前缀。     |
| **label** (_integer[0..][1048576] \| alert \| expli -null \| expli -null6 \| impli -null \| none_;Default:) | 分配给目的地的标签编号。 |
| **nexthop** (_IP_;Default:)                                                                                 |                          |
| **vrf** (_name_;Default:main)                                                                               | 该映射所属的VRF表名。    |

  

**只读属性**

| 属性                       | 说明                                       |
| -------------------------- | ------------------------------------------ |
| **inactive** (_yes \| no_) | 绑定是否激活，是否可以选择作为转发的候选。 |
| **dynamic** (_yes \| no_)  | 条目是否被动态添加                         |
| **path** (_string_)        |                                            |