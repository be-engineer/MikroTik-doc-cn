# 概述

`/interface mesh`

HWMP+是microtik专用于无线网状网络的第二层路由协议。它基于IEEE 802.11s草案标准中的混合无线Mesh协议(HWMP)。它可以用来代替(快速)生成树协议在网格设置，以确保无环路的最优路由。

但是，HWMP+协议不兼容IEEE 802.11s标准草案中的HWMP协议。

请注意，用于网络的分配系统不一定是无线分配系统(WDS)。HWMP+ mesh路由不仅支持WDS接口，还支持mesh内的以太网接口。因此，您可以使用简单的基于以太网的分发系统，或者您可以将WDS和以太网链路结合起来!

本文的先决条件是:您了解WDS是什么以及为什么要使用它!

## 属性

**Mesh**

| 属性                                                                        | 说明                                                                                                                                                        |
| --------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **admin-mac** (_MAC address_; **Default: 00:00:00:00:00:00)**               | 管理分配的MAC地址，当auto-mac设置被禁用时使用                                                                                                               |
| **arp** (_disabled \| enabled \| proxy-arp \| reply-only_;Default:**启用**) | 地址解析协议设置                                                                                                                                            |
| **auto-mac** (_boolean_;Default:**no**)                                     | 如果禁用，则使用admin-mac中的值作为mesh接口的MAC地址;如果端口存在，则使用其他端口的地址                                                                     |
| **hwmp-default-hopllimit** (_integer: 1..255_;Default:)                     | 生成路由协议数据包的最大跳数;HWMP+报文经过“hopllimit”次转发后被丢弃                                                                                         |
| **hwmp-prep-lifetime** (_time_;Default:**5m**)                              | 从接收到的PREP或PREQ消息创建路由的生存时间                                                                                                                  |
| **hwmp-preq-destination-only** (_boolean_; Default: **yes**)                | 是否只有目的端可以响应HWMP+ PREQ消息                                                                                                                        |
| **hwmp-preq-reply- forward** (_boolean_;Default:**yes**)                    | 中间节点响应后是否转发HWMP+ PREQ消息。仅当禁用 **hwmp-preq-destination-only** 时有效                                                                        |
| **hwmp-preq-retries** (_integer_;Default:**2**)                             | 在指定MAC地址被认为不可达之前，需要重试路由发现的次数                                                                                                       |
| **hwmp-preq-wait-time** (_time_;Default:**4s**)                             | 等待对第一个PREQ消息的响应的时间。注意，对于后续的preq，等待时间呈指数增长                                                                                  |
| **hwmp-run-interval** (_time_;Default:**10s**)                              | 发送HWMP+ RANN消息的频率                                                                                                                                    |
| **hwmp-rann-lifetime** (_time_; Default: **1s**)                            | 从接收到的RANN消息创建路由的生存期                                                                                                                          |
| **hwmp-run-propagation-delay** (_number_;Default:**0.5**)                   | 在传播RANN消息之前等待多长时间。秒值                                                                                                                        |
| **mesh-portal** (_boolean_;Default:**no**)                                  | 该接口是否为mesh网络中的portal                                                                                                                              |
| **mtu** (_number_;Default:**1500**)                                         | 最大传输单元大小                                                                                                                                            |
| **name** (_string_;Default:)                                                | 接口名称                                                                                                                                                    |
| **reoptimize-paths** (_boolean_; Default: **no**)                           | 是否定期发送PREQ消息请求已知的MAC地址。如果网络拓扑结构经常变化，则打开此设置非常有用。注意，如果没有收到对重新优化PREQ的回复，则保留现有路径(直到它超时)。 |

## 端口

| 属性                                                           | 说明                                                                                                                                                                                                                                                                 |
| -------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **active-port-type** (_read-only: wireless                     | WDS                                                                                                                                                                                                                                                                  | ethernet-mesh | ethernet-bridge | ethernet-mixed_; Default: ) | 实际使用的端口类型和状态 |
| **hello-interval** (_time_;Default:**10s**)                    | 发送HWMP+ Hello报文的最大时间间隔。仅用于以太网类型端口                                                                                                                                                                                                              |
| **interface** (_interface name_;Default:)                      | 接口名称，它将包含在一个网格                                                                                                                                                                                                                                         |
| **mesh** (_interface name;Default:)                            | 该端口所属的mesh接口                                                                                                                                                                                                                                                 |
| **path-cost** (_integer: 0..65535_;Default:**10**)             | 到接口的路径开销，由路由协议用来确定“最佳”路径                                                                                                                                                                                                                       |
| **port-type** (_WDS \| auto \| ethernet \| wireless_;Default:) | 使用的端口类型<br>- 自动端口类型是根据底层接口的类型自动确定的<br>- WDS -无线分配系统接口。远程MAC地址从无线连接数据中学习<br>- ethernet -从HWMP+ Hello报文中学习远端MAC地址，也可以从接收或转发的流量中学习源MAC地址<br>- wireless -从无线连接数据中学习远端MAC地址 |

## FDB状态

| 属性                                                                                 | 说明                                                                                                                                                                                                                                                                                                                                                                                     |
| ------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **mac-address** (_MAC address_)                                                      | 这个FDB表项对应的MAC地址                                                                                                                                                                                                                                                                                                                                                                 |
| **seq-number** (_integer_)                                                           | 路由协议中使用的序列号以避免环路                                                                                                                                                                                                                                                                                                                                                         |
| **type** (_integer_)                                                                 | 路由协议中使用的序列号，以避免环路                                                                                                                                                                                                                                                                                                                                                       |
| **interface** (_local\| outsider\| direct \| mesh \| neighbor \| larval \| unknown_) | FDB条目的类型<br>- local——MAC地址属于本地路由器本身<br>- outsider ——MAC地址属于网状网络外部的设备<br>- direct——MAC地址属于mesh网络接口上的无线客户端<br>- mesh——MAC地址属于可通过mesh网络访问的设备;它可以是网状网络的内部或外部<br>- neighbor——MAC地址属于与该路由器直接相邻的mesh路由器<br>- larval——MAC地址属于一个未知的设备，可以通过网状网络访问<br>- unknown——MAC地址属于未知设备 |
| **mesh** (_interface name_)                                                          | 该FDB表项所属的网格接口                                                                                                                                                                                                                                                                                                                                                                  |
| **on-interface** (_interface name_)                                                  | 用于流量转发的mesh端口，类似于下一跳值                                                                                                                                                                                                                                                                                                                                                   |
| **lifetime** (_time_)                                                                | 如果此表项不用于流量转发，则剩余存活时间                                                                                                                                                                                                                                                                                                                                                 |
| **age** (_time_)                                                                     | FDB表项的年龄                                                                                                                                                                                                                                                                                                                                                                            |
| **metric** (_integer_)                                                               | 路由协议用来确定“最佳”路径的度量值                                                                                                                                                                                                                                                                                                                                                       |

**例子**

![](https://help.mikrotik.com/docs/download/attachments/8978441/Mesh_ex1.jpg?version=2&modificationDate=1612788541366&api=v2)

这个例子使用静态WDS链接，当它们变得活跃时，动态地将其添加为网格端口。使用两个不同的频率:一个用于AP互连，一个用于客户端与AP连接，因此AP必须至少有两个无线接口。当然，所有连接也可以使用相同的频率，但由于潜在的干扰问题，可能效果不佳。

在所有ap上重复此配置:

```shell
/interface mesh add disabled=no
/interface mesh port add interface=wlan1 mesh=mesh1
/interface mesh port add interface=wlan2 mesh=mesh1
 
 # interface used for AP interconnections
/interface wireless set wlan1 disabled=no ssid=mesh frequency=2437 band=2.4ghz-b/g/n mode=ap-bridge \
 wds-mode=static-mesh wds-default-bridge=mesh1
 
# interface used for client connections
 /interface wireless set wlan2 disabled=no ssid=mesh-clients frequency=5180 band=5ghz-a/n/ac mode=ap-bridge
 
# a static WDS interface for each AP you want to connect to
/interface wireless wds add disabled=no master-interface=wlan1 name=<;descriptive name of remote end> \
 wds-address=<;MAC address of remote end>
```

这里的WDS接口是手动添加的，因为使用的是静态WDS模式。如果你使用的是 ** WDS -mode**\=**dynamic-mesh**，所有的WDS接口都会自动创建。这里指定频率和频带参数只是为了产生有效的示例配置;Mesh协议操作绝不限于或优化这些特定的值。

您可能需要增加disconnect-timeout无线接口选项，以使协议更稳定。

在实际设置中，您还应该注意保护无线连接，使用/interface wireless security-profile。为简单起见，这里没有显示该配置。

路由器A上的结果(有一个客户端连接到wlan2):

```shell
[admin@A] > /interface mesh print
Flags: X - disabled, R - running
0 R name="mesh1" mtu=1500 arp=enabled mac-address=00:0C:42:0C:B5:A4 auto-mac=yes
admin-mac=00:00:00:00:00:00 mesh-portal=no hwmp-default-hoplimit=32
hwmp-preq-waiting-time=4s hwmp-preq-retries=2 hwmp-preq-destination-only=yes
hwmp-preq-reply-and-forward=yes hwmp-prep-lifetime=5m hwmp-rann-interval=10s
hwmp-rann-propagation-delay=1s hwmp-rann-lifetime=22s
 
[admin@A] > /interface mesh port print detail
Flags: X - disabled, I - inactive, D - dynamic
0 interface=wlan1 mesh=mesh1 path-cost=10 hello-interval=10s port-type=auto port-type-used=wireless
1 interface=wlan2 mesh=mesh1 path-cost=10 hello-interval=10s port-type=auto port-type-used=wireless
2 D interface=router_B mesh=mesh1 path-cost=105 hello-interval=10s port-type=auto port-type-used=WDS
3 D interface=router_D mesh=mesh1 path-cost=76 hello-interval=10s port-type=auto port-type-used=WDS
```

FDB (Forwarding Database)目前只包含本地MAC地址、通过本地接口可达的非mesh节点和直接mesh邻居的信息。

```shell
[admin@A] /interface mesh fdb print
Flags: A - active, R - root
MESH TYPE MAC-ADDRESS ON-INTERFACE LIFETIME AGE
A mesh1 local 00:0C:42:00:00:AA 3m17s
A mesh1 neighbor 00:0C:42:00:00:BB router_B 1m2s
A mesh1 neighbor 00:0C:42:00:00:DD router_D 3m16s
A mesh1 direct 00:0C:42:0C:7A:2B wlan2 2m56s
A mesh1 local 00:0C:42:0C:B5:A4 2m56s
 
[admin@A] /interface mesh fdb print detail
Flags: A - active, R - root
A mac-address=00:0C:42:00:00:AA type=local age=3m21s mesh=mesh1 metric=0 seqnum=4294967196
A mac-address=00:0C:42:00:00:BB type=neighbor on-interface=router_B age=1m6s mesh=mesh1 metric=132 seqnum=4294967196
A mac-address=00:0C:42:00:00:DD type=neighbor on-interface=router_D age=3m20s mesh=mesh1 metric=79 seqnum=4294967196
A mac-address=00:0C:42:0C:7A:2B type=direct on-interface=wlan2 age=3m mesh=mesh1 metric=10 seqnum=0
A mac-address=00:0C:42:0C:B5:A4 type=local age=3m mesh=mesh1 metric=0 seqnum=0
```

测试ping是否有效:

```shell
[admin@A] > /ping 00:0C:42:00:00:CC
00:0C:42:00:00:CC 64 byte ping time=108 ms
00:0C:42:00:00:CC 64 byte ping time=51 ms
00:0C:42:00:00:CC 64 byte ping time=39 ms
00:0C:42:00:00:CC 64 byte ping time=43 ms
4 packets transmitted, 4 packets received, 0% packet loss
round-trip min/avg/max = 39/60.2/108 ms
```

路由器A必须先发现到路由器C的路径，因此第一次ping的时间略长。现在，FDB还包含一个00:01 c:42:00:00:CC的条目，类型为“mesh”。

此外，测试ARP解析工作，所以IP级别ping:

```shell
[admin@A] > /ping 10.4.0.3
10.4.0.3 64 byte ping: ttl=64 time=163 ms
10.4.0.3 64 byte ping: ttl=64 time=46 ms
10.4.0.3 64 byte ping: ttl=64 time=48 ms
3 packets transmitted, 3 packets received, 0% packet loss
round-trip min/avg/max = 46/85.6/163 ms
```

### Mesh traceroute

还有一个mesh traceroute命令，它可以帮助确定用于路由的路径。

例如，对于这个网络:

```shell
[admin@1] /interface mesh fdb print
Flags: A - active, R - root
MESH TYPE MAC-ADDRESS ON-INTERFACE LIFETIME AGE
A mesh1 local 00:0C:42:00:00:01 7m1s
A mesh1 mesh 00:0C:42:00:00:02 wds4 17s 4s
A mesh1 mesh 00:0C:42:00:00:12 wds4 4m58s 1s
A mesh1 mesh 00:0C:42:00:00:13 wds4 19s 2s
A mesh1 neighbor 00:0C:42:00:00:16 wds4 7m1s
A mesh1 mesh 00:0C:42:00:00:24 wds4 18s 3s
```

Traceroute to 00:c:42:00:00:12显示:

```shell
[admin@1] /interface mesh traceroute mesh1 00:0C:42:00:00:12
ADDRESS TIME STATUS
00:0C:42:00:00:16 1ms ttl-exceeded
00:0C:42:00:00:02 2ms ttl-exceeded
00:0C:42:00:00:24 4ms ttl-exceeded
00:0C:42:00:00:13 6ms ttl-exceeded
00:0C:42:00:00:12 6ms success
```

# 协议说明

## 反应模式

![](https://help.mikrotik.com/docs/download/attachments/8978441/520px-Hwmp_reactive_a.jpg?version=1&modificationDate=1612788675602&api=v2)  
Router A wants to discover a path to C

  
![](https://help.mikrotik.com/docs/download/attachments/8978441/520px-Hwmp_reactive_b.jpg?version=1&modificationDate=1612788683515&api=v2)

路由器C向a发送一个单播响应

在响应模式下，HWMP+非常像AODV (Ad-hoc On-demand Distance Vector)。所有路径都是按需发现的，通过在网络中传播路径请求(PREQ)消息。目的地节点或某些具有到达目的地路径的路由器将使用路径响应(PREP)进行应答。请注意，如果目的地址属于某个客户端，则该客户端所连接的AP将作为其代理(即代表其回复preq)。

这种模式最适合于移动网络和/或当大多数通信发生在网格内节点之间时。

## 主动模式

![](https://help.mikrotik.com/docs/download/attachments/8978441/Hwmp_proactive_a.jpg?version=1&modificationDate=1612788716474&api=v2)  
The root announces itself by flooding RANN

  

![](https://help.mikrotik.com/docs/download/attachments/8978441/Hwmp_proactive_b.jpg?version=1&modificationDate=1612788725360&api=v2)  
Internal nodes respond with PREGs

在主动模式下，有一些路由器被配置为门户。一般来说，作为一个门户意味着路由器有通往其他网络的接口，也就是说，它是网状网络的入口/出口点。

门户将通过在网络中大量发布根公告(RANN)消息来宣布它们的存在。内部节点将使用路径注册(PREG)消息进行应答。这个过程的结果将是路由在门户中有根的树。

到门户的路由将作为一种默认路由。如果内部路由器不知道通往特定目的地的路径，它将把所有数据转发到最近的门户。然后，门户将在需要时代表路由器发现路径。之后的数据将通过传送门传送。这可能导致次优路由，除非将数据寻址到门户本身或门户具有接口的某些外部网络。

当大多数流量在内部网格节点和几个门户节点之间传输时，主动模式最适合。

## 拓扑变更检测

![](https://help.mikrotik.com/docs/download/attachments/8978441/Hwmp_error_a.jpg?version=1&modificationDate=1612788766081&api=v2)  
Data flow path

![](https://help.mikrotik.com/docs/download/attachments/8978441/Hwmp_error_b.jpg?version=1&modificationDate=1612788772566&api=v2)  
After the link disappears, an error is propagated upstream

HWMP+使用PERR (Path Error)消息来通知链路已经消失。消息被传播到所有上游节点直至数据源。接收到PERR的源重启路径发现过程。

# 问题解答

**问，这比RSTP有什么好?**

答:它为你提供最佳路线。RSTP仅用于防止环路。

**问，路线选择是如何完成的?**

A.具有最佳度量的路由总是在发现过程之后被选择。还有一个配置选项可以定期重新优化已知的路由。

路由度量是计算各个链路度量的总和。

链路度量的计算方法与(R)STP协议相同:

- 对于以太网链路，度量值是静态配置的(例如OSPF)。
- 对于WDS链路，度量根据实际链路带宽动态更新，而实际链路带宽又受无线信号强度和所选数据传输速率的影响。

目前，该协议没有考虑链路上使用的带宽量，但将来可能也会考虑到这一点。

**问，总的来说，这比OSPF/RIP/三层路由好在哪里?**

答:WDS网络通常是桥接的，而不是路由的。自配置能力对于网状网络很重要，路由通常比桥接需要更多的配置。当然，您总是可以在桥接网络上运行任何L3路由协议，但对于网状网络，这通常没有什么意义。

由于mesh协议中不包括优化的第二层组播转发，因此最好避免在mesh网络上转发任何组播流量(包括OSPF)。如果需要使用OSPF协议，则需要配置使用单播模式的 [OSPF NBMA](https://wiki.mikrotik.com/wiki/OSPF-reference#NBMA_Neighbor) 邻居。

**问，性能/CPU需求如何?**

A.协议本身，如果配置得当，将比OSPF(例如)占用更少的资源。单个路由器上的数据转发性能应该接近桥接的性能。

**问，它如何与使用RSTP的现有网格设置一起工作?**

A. RSTP网络的内部结构对mesh协议是透明的(因为mesh hello报文在RSTP网络内部转发)。mesh将把RSTP网络中两个入口点之间的路径视为单个段。另一方面，mesh网络对RSTP不透明，因为RSTP hello报文不会在mesh网络内部转发。_(这是v3.26以来的行为)_


如果网状网络在两个或更多的点上连接到RSTP网络，则路由环路是可能的!


注意，如果在两个接入点之间有一个WDS链接，那么两端必须具有相同的配置(要么作为两端mesh中的端口，要么作为两端网桥接口中的端口)。

您还可以将网桥接口作为网状端口(例如，为了能够使用网桥防火墙)。

**问，我可以有多个网络入口/出口点吗?**

A.如果入口/出口点被配置为门户(即使用主动模式)，网状网络中的每个路由器将选择其最近的门户并将所有数据转发给它。然后，如果需要，门户将代表路由器发现一条路径。

**问，如何控制或过滤网格流量?**

答:目前唯一的办法是使用桥接防火墙。创建一个桥接接口，将WDS接口和/或以太网放在桥接中，并将桥接放在网状接口中。然后配置网桥防火墙规则。

匹配mesh流量封装时使用的MAC协议号为0x9AAA，匹配mesh路由流量时使用的MAC协议号为0x9AAB。例子:

```shell
interface bridge settings set use-ip-firewall=yes
interface bridge filter add chain=input action=log mac-protocol=0x9aaa
interface bridge filter add chain=input action=log mac-protocol=0x9aab
```

这是完全有可能创建混合网格/桥的设置，将不工作(例如_有问题的例子1_与桥而不是开关)。推荐的始终有效的故障安全方法是为每个物理接口创建一个单独的桥接接口;然后将所有这些网桥接口添加为网格端口。

# 高级主题

我们都知道，二层桥接或路由设置很容易出现问题，而且很难调试它们。(与三层路由设置相比。)因此，这里有一些可能给您带来问题的糟糕配置示例。避免他们!

## 问题示例1:以太网交换机在一个网格内

![](https://help.mikrotik.com/docs/download/attachments/8978441/Mesh_bad_ex1.jpg?version=2&modificationDate=1612788797211&api=v2)

Router A在网格外，其余的路由器都在网格内。对于路由器B、C、D，所有接口都添加为mesh端口

路由器A将无法与路由器c进行可靠的通信。当D被指定为以太网路由器时，问题就会显现出来;如果B担任这个角色，一切都没问题。导致该问题的主要原因是以太网交换机的MAC地址学习。

考虑一下当路由器A想要向c发送一些东西时会发生什么。我们假设路由器A知道或将数据发送到所有接口。无论哪种方式，数据都会到达交换机。交换机不知道目的地的MAC地址，将数据转发给B和D。

现在发生了什么:

1.  B在mesh接口上接收报文。由于MAC地址不是B的本地地址，并且B知道他不是以太网网络的指定路由器，因此他直接忽略了该数据包。
2.  D在mesh接口上接收报文。由于B的MAC地址不是本地的，而D是以太网的指定路由器，所以他向C发起了路径发现过程。

路径发现完成后，D得到了通过b可以到达C的信息，此时D将数据包封装并转发回以太网。封装后的数据包由交换机转发，由B接收转发，由c接收。目前一切正常。

现在C可能会响应这个数据包。因为B已经知道A在哪里，所以他将解封装并转发回复报文。但是现在交换机会知道C的MAC地址可以通过B到达!这意味着，下次当某件事从A到达C地址时，交换机将只把数据转发给B(当然，B会默默地忽略这个数据包)!

相反，如果B充当指定路由器的角色，一切都没问题，因为流量不必经过两次以太网交换机。

**故障排除** :避免这种设置或禁用交换机上的MAC地址学习。请注意，在许多交换机上，这是不可能的。

还请注意，如果有以下任何一种情况，都不会有问题:

- 路由器A支持并配置为使用HWMP+;
- 或将以太网交换机更换为支持HWMP+的路由器，并添加以太网接口作为mesh端口。

## 问题示例2:无线模式

考虑这个(无效的)设置例子:

![](https://help.mikrotik.com/docs/download/attachments/8978441/Mesh_bad_ex2.jpg?version=2&modificationDate=1612788828215&api=v2)

路由器A和B在网内，路由器C在网外。对于路由器A和路由器B，所有接口都添加为mesh端口。

现在不可能在路由器B上桥接wlan1和wlan2。如果你了解白龙会是如何工作的，原因就很明显了。对于WDS通信，使用四个地址帧。这是因为对于无线多跳转发，您需要知道中间跳的地址，以及原始发送方和最终接收方的地址。相比之下，非wds 802.11通信在一个帧中只包含三个MAC地址。这就是为什么在站模式下不能进行多跳转发的原因。

**故障排除** :取决于想要达到的效果:

1.  如果您希望路由器C充当无线或以太网流量的中继器，请在路由器B和路由器C之间配置WDS链路，并在所有节点上运行mesh路由协议。
2.  在其他情况下，在路由器B上配置AP模式的wlan2，在路由器C上配置站模式的WLAN。