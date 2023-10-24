# 网络模型

计算机网络由许多不同的组件和协议共同组成。为了理解节点间通信是如何发生的概念，让我们先熟悉一下OSI模型和TCP/IP模型。这两个模型都有助于可视化节点之间的通信是如何发生的。

## OSI模型

开放系统互连(OSI)模型是一个7层模型，目前被用作教学工具。OSI模型最初被设想为构建网络系统的标准体系结构，但在现实世界中，网络的定义比OSI模型所建议的要少得多。

- **第七层(应用层)** -定义服务器端与客户端通信的协议，如HTTP协议。如果web浏览器想要下载图像，协议将组织并执行请求;
- **第6层(表示)** -确保以可用的格式接收数据。加密在这里完成(但实际上可能不是这样，例如IPSec);
- **第5层(会话)** -负责在客户端和服务器之间建立、管理和关闭会话;
- **第4层(传输)** -传输层主要负责组装和重组，数据流被分成块(段)，分配序列号并封装成协议头(TCP, UDP等);
- **第3层(网络)** -负责逻辑设备寻址，数据被封装在IP头中，现在称为“包”;
- **第2层(数据链路)** -数据封装在自定义报头中，802.3(以太网)或802.11(无线)，称为“帧”，处理流量控制;
- **第1层(物理)** -通信介质，负责发送和接收比特、电信号和硬件接口;

## TCP/IP模型

该模型与OSI模型具有相同的目的，但更适合现代网络故障排除。与OSI模型相比，TCP/IP是一个四层模型:

- **应用层(4)** -包括OSI模型的应用层、表示层和会话层，大大简化了网络故障排除;
- **传输层(3)** -与OSI模型(TCP, UDP协议)中的传输层相同;
- **Internet层(2)** -与OSI模型中的网络层相同(包括ARP, IP协议);
- **链路层(1)** -也称为网络接入层。包括OSI模型的第1层和第2层，因此它主要关注网络节点之间的物理数据交换;

| TCP/IP             | OSI模型                         | 协议                          |
| ------------------ | ------------------------------- | ----------------------------- |
| Application Layer  | Application Layer               | DNS, DHCP,HTTP,SSH etc.       |
| Presentation Layer | JPEG,MPEG,PICT etc.             |
| Session Layer      | PAP, SCP, ZIP etc.              |
| Transport Layer    | Transport Layer                 | TCP, UDP                      |
| Internet Layer     | Network Layer                   | ICMP, IGMP, IPv4, IPv6, IPSec |
| Link Layer         | Data Link Layer                 | ARP, CDP, MPLS, PPP etc.      |
| Physical Layer     | Bluetooth, Ethernet, Wi-Fi etc. |

# 以太网

计算机网络中最常用的链路层协议(OSI layer 2)是以太网协议。为了通信，每个节点都有一个唯一的分配地址，称为MAC(媒体访问控制地址)，有时也称为以太网地址。

长度为48位，通常由制造商固定(不能更改)，但近年来自定义MAC地址被广泛使用，RouterOS也允许设置自定义MAC地址。

最常用的MAC格式是用冒号分隔的6个十六进制数(D4:CA:6D:01:22:96)

RouterOS在所有类以太网接口(无线、60G、VPLS等)的配置中显示MAC地址。


```shell
[admin@rack1_b32_CCR1036] /interface ethernet> print
Flags: X - disabled, R - running, S - slave
 #    NAME                  MTU MAC-ADDRESS       ARP             SWITCH              
 0 R  ether1               1500 D4:CA:6D:01:22:96 enabled       
 1 R  ether2               1500 D4:CA:6D:01:22:97 enabled       
 2 R  ether3               1500 D4:CA:6D:01:22:98 enabled       
 3    ether4               1500 D4:CA:6D:01:22:99 enabled       
 4    ether5               1500 D4:CA:6D:01:22:9A enabled       
 5    ether6               1500 D4:CA:6D:01:22:9B enabled       
 6    ether7               1500 D4:CA:6D:01:22:9C enabled       
 7 R  ether8               1500 D4:CA:6D:01:22:9D enabled       
 8    sfp-sfpplus1         1500 D4:CA:6D:01:22:94 enabled       
 9    sfp-sfpplus2         1500 D4:CA:6D:01:22:95 enabled
```

有三类地址:

![](https://help.mikrotik.com/docs/download/attachments/119144661/ucast_bcast_mcast_diff_eth.png?version=1&modificationDate=1653919107792&api=v2)

- **单播** 地址发送到碰撞域内的所有节点，通常是两个节点之间的以太网电缆，或者在无线情况下可以检测到无线信号的所有接收器。只有具有匹配MAC地址的远程节点才会接受帧(除非启用了混杂模式)。

- 其中一个特殊地址是广播地址(FF:FF:FF:FF:FF:FF:FF)，广播帧在二层网络中被所有节点接受并转发

- 另一个特殊地址是 **multicast**。具有组播地址的帧被配置为接收具有此地址的帧的所有节点接收。

# IP组网

以太网协议足以在以太网网络上的两个节点之间获取数据，但它不能单独使用。对于Internet/网络层(OSI第三层)，使用IP (Internet Protocol)来标识具有唯一逻辑地址的主机。

目前大多数网络使用IPv4地址，它是用点分十进制表示的32位地址(' 192.168.88.1 ')。

可以有多个逻辑网络，为了确定哪个网络的IP地址属于哪个网络，使用netmask。网络掩码通常被指定为用于标识逻辑网络的位数。格式也可以是十进制，例如，24位的网络掩码可以写成 255.255.255.0 。

仔细看看192.168.3.24/24:

```shell
11000000 10101000 00000011 00011000 => 192.168.3.24
11111111 11111111 11111111 00000000 => /24 or 255.255.255.0
```

从上面的插图中可以看出，高24位被屏蔽，留给我们的范围是0-255。

在这个范围内，第一个地址用于标识网络(在我们的示例中，网络地址为192.168.3.0)，最后一个地址用于网络广播(192.168.3.255)。这就给我们留下了一个范围从1到254的主机标识，称为单播地址。

与以太网协议一样，也可以有特殊地址:

- **broadcast** -地址发送数据到所有可能的目的地(“all-hosts broadcast”)，这允许发送者只发送一次数据，所有接收者都收到它的副本。在IPv4协议中，本地广播使用地址255.255.255.255。另外，可以对网络广播地址进行定向(有限)广播;
- **multicast** -与一组感兴趣的接收者相关联的地址。在IPv4中，地址224.0.0.0 到 239.255.255.255 被指定为组播地址。发送方将单个数据报从其单播地址发送到多播组地址，中间路由器负责制作副本并将其发送给已加入相应多播组的所有接收方;

在逻辑IP网络的情况下，单播、广播和多播可视化看起来有点不同

![](https://help.mikrotik.com/docs/download/attachments/119144661/ucast_bcast_mcast_diff.png?version=1&modificationDate=1653919107833&api=v2)

也有为特殊目的保留的地址范围，例如，[私人地址范围](https://tools.ietf.org/html/rfc1918)，应该只在本地网络中使用，并且通常在转发到internet时丢弃:

- 10.0.0.0/8 - start: 10.0.0.0; end: 10.255.255.255
- 172.16.0.0/12 - start: 172.16.0.0; end:172.31.255.255
- 192.168.0.0/16 - start: 192.168.0.0; end: 192.168.255.255

# ARP and Tying It All Together

尽管IP数据包是使用IP地址寻址的，但必须使用硬件地址来实际地将数据从一台主机传输到另一台主机。

这就引出了地址解析协议(ARP)，它用于将主机的IP地址映射到硬件地址(MAC)。ARP协议在 [RFC 826](https://tools.ietf.org/html/rfc826) 中被引用。

每个网络设备都有一个当前使用的ARP表项。通常表是动态构建的，但为了提高网络安全性，可以通过添加静态表项来部分或完全静态构建表。

地址解析协议是过去的事情。IPv6完全消除了ARP的使用。

局域网中的一台主机向另一台主机发送IP报文时，必须在自己的ARP缓存中查找目的主机的以太网MAC地址。如果目的主机的MAC地址不在ARP表中，则发送ARP请求，查找具有相应IP地址的设备。ARP向局域网内的所有设备发送广播请求消息，要求指定IP地址的设备回复自己的MAC地址。识别IP地址为自己的设备返回带有自己MAC地址的ARP响应:

![](https://help.mikrotik.com/docs/download/attachments/119144661/arp.jpg?version=1&modificationDate=1653919107855&api=v2)

做一个简单的配置，并仔细查看主机a试图ping主机C时的进程。

首先，在主机A上添加IP地址:

```shell
/ip address add address=10.155.101.225 interface=ether1
```

主机B:

```shell
/ip address add address=10.155.101.221 interface=ether1
```

主机C:

```shell
/ip address add address=10.155.101.217 interface=ether1
```

现在，运行一个数据包嗅探器，将数据包转储保存到文件中，并在主机a上运行ping命令:

```shell
/tool sniffer
  set file-name=arp.pcap filter-interface=ether1
  start
/ping 10.155.101.217 count=1
  stop
```

现在可以从路由器下载 arp.pcap 文件，然后在 Wireshark 打开它进行分析:

![](https://help.mikrotik.com/docs/download/attachments/119144661/arp_wireshark.png?version=1&modificationDate=1653919107874&api=v2)

- 主机 A 发送 ARP 消息询问谁拥有“10.155.101.217”
- 主机 C 回应说10.155.101.217可以在08:00:27:3 C: 79:3访问一个 MAC 地址
- 主机 A 和主机 C 现在都已经更新了它们的 ARP 表，现在可以发送 ICMP (ping)数据包

如果查看两个主机的 ARP 表，可以看到相关的条目，在 RouterOS ARP 表可以通过运行命令: `/ip ARP print` 来查看

```shell
[admin@host_a] /ip arp> print
Flags: X - disabled, I - invalid, H - DHCP, D - dynamic, P - published,
C - complete
 #    ADDRESS         MAC-ADDRESS       INTERFACE                         
 0 DC 10.155.101.217  08:00:27:3C:79:3A ether1 
 
 [admin@host_b] /ip arp> print
Flags: X - disabled, I - invalid, H - DHCP, D - dynamic, P - published,
C - complete
 #    ADDRESS         MAC-ADDRESS       INTERFACE                    
 0 DC 10.155.101.225  08:00:27:85:69:B5 ether1
```

## ARP模式

现在，上面的示例演示了默认行为，其中在接口上启用了ARP，但可能存在需要不同ARP行为的场景。对于支持ARP的接口，RouterOS支持配置不同的ARP模式。

### 启用

ARP将被自动发现，新的动态表项将被添加到ARP表中。这是RouterOS中接口的默认模式，如上例所示。

### 禁用

如果在接口上关闭ARP功能，即使用 _arp=disabled_ ，则来自客户端的ARP请求不会得到路由器的响应。因此，客户端也需要添加静态ARP表项。例如，添加路由器的IP地址和MAC地址:

```shell
[admin@host_a] > /ip arp add mac-address=08:00:27:3C:79:3A address=10.155.101.217 interface=ether1
```

### reply-only

如果接口的ARP属性设置为 _reply-only_ ，表示只响应ARP请求。邻居MAC地址将使用 _/ip arp_ 静态解析，但是在ARP被禁用的情况下，不需要将路由器的MAC地址添加到其他主机的ARP表中。

### ARP代理

正确配置ARP代理特性的路由器在直连网络之间充当透明的ARP代理。这种行为可能是有用的，例如，如果要分配拨号(PPP, PPPoE, PPTP)客户端IP地址从相同的地址空间用于连接的局域网。

![](https://help.mikrotik.com/docs/download/attachments/119144661/Proxy-ARP.jpg?version=1&modificationDate=1653919107889&api=v2)

看上面图片中的示例设置。子网A上的主机A(172.16.1.2)想要向子网B上的主机D(172.16.2.3)发送报文。主机A的子网掩码为/16，这意味着主机A认为自己与所有172.16.0.0/16网络(同一局域网)都是直连的。由于主机A认为是直连的，因此向目的地址发送ARP请求，以澄清主机D的MAC地址(当主机A发现目的地址不在同一子网时，向默认网关发送数据包)。主机A向子网A广播ARP请求。

来自数据包分析软件的信息:


```shell

No.     Time   Source             Destination       Protocol  Info
 
 12   5.133205  00:1b:38:24:fc:13  ff:ff:ff:ff:ff:ff  ARP      Who has 173.16.2.3?  Tell 173.16.1.2
 
 
Packet details:
 
Ethernet II, Src: (00:1b:38:24:fc:13), Dst: (ff:ff:ff:ff:ff:ff)
    Destination: Broadcast (ff:ff:ff:ff:ff:ff)
    Source: (00:1b:38:24:fc:13)
    Type: ARP (0x0806)
Address Resolution Protocol (request)
    Hardware type: Ethernet (0x0001)
    Protocol type: IP (0x0800)
    Hardware size: 6
    Protocol size: 4
    Opcode: request (0x0001)
    [Is gratuitous: False]
    Sender MAC address: 00:1b:38:24:fc:13
    Sender IP address: 173.16.1.2
    Target MAC address: 00:00:00:00:00:00
    Target IP address: 173.16.2.3
```

通过这个ARP请求，主机A(172.16.1.2)请求主机D(172.16.2.3)发送自己的MAC地址。然后以主机A的MAC地址作为源地址，广播(FF:FF:FF:FF:FF)作为目的地址，将ARP请求报文封装在以太网帧中。第二层广播是指帧将被发送到包括路由器的ether0接口在内的同一第二层广播域中的所有主机，但不会到达主机D，因为路由器默认不转发第二层广播。

因为路由器知道目标地址(172.16.2.3)在另一个子网上，但它可以到达主机D，所以它用自己的MAC地址回复主机A。

```shell
No.     Time   Source            Destination         Protocol   Info
 
13   5.133378  00:0c:42:52:2e:cf  00:1b:38:24:fc:13   ARP        172.16.2.3 is at 00:0c:42:52:2e:cf
 
Packet details:
 
Ethernet II, Src: 00:0c:42:52:2e:cf, Dst: 00:1b:38:24:fc:13
   Destination: 00:1b:38:24:fc:13
   Source: 00:0c:42:52:2e:cf
   Type: ARP (0x0806)
Address Resolution Protocol (reply)
   Hardware type: Ethernet (0x0001)
   Protocol type: IP (0x0800)
   Hardware size: 6
   Protocol size: 4
   Opcode: reply (0x0002)
   [Is gratuitous: False]
   Sender MAC address: 00:0c:42:52:2e:cf
   Sender IP address: 172.16.1.254
   Target MAC address: 00:1b:38:24:fc:13
   Target IP address: 172.16.1.2
```

这是路由器发送给主机A的代理ARP应答。路由器发送回单播代理ARP应答，将自己的MAC地址作为源地址，将主机A的MAC地址作为目的地址，表示“将这些数据包发送给我，我将把它送到需要的地方”。

当主机A收到ARP响应时，它更新自己的ARP表，如下所示:

```shell
C:\Users\And>arp -a
Interface: 173.16.2.1 --- 0x8
  Internet Address      Physical Address      Type
  173.16.1.254          00-0c-42-52-2e-cf    dynamic
  173.16.2.3            00-0c-42-52-2e-cf    dynamic
  173.16.2.2            00-0c-42-52-2e-cf    dynamic
```

MAC表更新后，主机A将发往主机D(172.16.2.3)的报文直接转发到路由器接口ether0 (00:01 c:42:52:2e:cf)，由路由器转发给主机D。在子网A主机的ARP缓存中填充了子网B所有主机的MAC地址，因此所有发往子网B的报文都发往路由器。路由器将这些数据包转发到子网B中的主机。

使用代理ARP时，主机的多个IP地址映射到一个MAC地址(即本路由器的MAC地址)。

通过命令 _arp= Proxy -arp_ ，可以在每个接口上单独启用代理ARP:

```shell
[admin@MikroTik] /interface ethernet> set 1 arp=proxy-arp
[admin@MikroTik] /interface ethernet> print
Flags: X - disabled, R - running
  #    NAME                 MTU   MAC-ADDRESS         ARP
  0  R ether1              1500  00:30:4F:0B:7B:C1 enabled
  1  R ether2              1500  00:30:4F:06:62:12 proxy-arp
[admin@MikroTik] interface ethernet>
```

#### 本地代理ARP

如果在接口上配置了 _local-proxy-arp_ 属性，则路由器只对该接口执行代理arp。例如，对于进出同一接口的流量。在一个普通的局域网中，默认的行为是两个网络主机直接相互通信，而不涉及路由器。

这样做是为了支持(以太网)交换机功能，如 [RFC 3069](https://tools.ietf.org/html/rfc3069)，其中单个端口不允许彼此通信，但允许与上游路由器通信。如 [RFC 3069](https://tools.ietf.org/html/rfc3069) 所述，允许这些主机通过代理arp'ing通过上游路由器进行通信是可能的。不需要与proxy_arp一起使用。这项技术有不同的名称:

- 在RFC 3069中称为VLAN聚合;
- 思科和联合电信称之为私有VLAN;
- 惠普称之为源端口过滤或端口隔离;
- 爱立信称之为mac强制转发(RFC Draft)。

# TCP/IP

## TCP会话建立和终止

TCP是一个面向连接的协议。面向连接协议和无连接协议的区别在于，在建立正确的连接之前，面向连接协议不发送任何数据。

每当传输设备试图建立到远程节点的连接时，TCP使用三次握手。因此，创建了端到端的虚拟(逻辑)电路，其中使用了可靠交付的流控制和确认。TCP在连接建立和终止过程中有几种消息类型。

### 连接建立过程

![](https://help.mikrotik.com/docs/download/attachments/119144661/tcp-connection-establishment.jpg?version=1&modificationDate=1653919107907&api=v2)

1. 需要初始化连接的主机A向目的地“主机B”发送带有建议初始序列号的 **SYN** (同步)数据包;
2. 当主机B接收到一个 **SYN** 消息时，它返回一个在TCP头(SYN-ACK)中设置了 **SYN** 和 **ACK** 标志的数据包;
3.当主机A接收到SYN-ACK时，发送回 **ACK** (确认)包;
4. 主机B收到 **ACK** ，此时连接为 **ESTABLISHED;**

面向连接的协议服务通常在成功交付后发送确认(ack)。发送方在发送数据包后，等待接收方的确认。如果超时且发送方未收到ACK，则重传数据包。

连接终止

![](https://help.mikrotik.com/docs/download/attachments/119144661/tcp-connection-termination.jpg?version=1&modificationDate=1653919107922&api=v2)

当数据传输完成，主机想要终止连接时，终止过程启动。与TCP连接建立使用三向握手不同，连接终止使用四向按摩。当双方通过发送FIN(结束)和接收ACK(确认)完成关闭过程时，连接终止。

1. 需要终止连接的主机A发送带有 **FIN** 标志的特殊消息，表示数据发送完成;
2. 接收到 **FIN** 段的主机B不会终止连接，而是进入“被动关闭”(CLOSE_WAIT)状态，并将 **FIN** 的 **ACK** 发送回主机a。如果主机B没有任何数据可以传输给主机a，它也会发送 **FIN** 消息。现在主机B进入LAST_ACK状态。此时，主机B将不再接受来自主机A的数据，但可以继续向主机A传输数据。
3. 当主机A从主机B接收到最后一个 **FIN** 时，进入(TIME_WAIT)状态，并向主机B发送一个 **ACK** ;
4. 主机B从主机A处获得 **ACK** ，连接终止;

## TCP段传输(窗口)

现在知道了TCP连接是如何建立的，需要了解数据传输是如何管理和维护的。在TCP/IP网络中，主机之间的传输由TCP协议处理。

考虑当data-grams发送的速度超过接收设备的处理速度时会发生什么。接收器将它们存储在称为缓冲区的内存中。但是由于缓冲区空间不是无限的，当超过它的容量时，接收方开始丢弃帧。所有丢失的帧必须重新传输，这是低传输性能的原因。

为了解决这个问题，TCP使用了一个流控制协议。窗口机制用于控制数据流。当连接建立时，接收方指定每个TCP帧中的窗口字段。窗口大小表示接收方愿意存储在缓冲区中的接收数据量。窗口大小(以字节为单位)与确认一起发送给发送方。因此，窗口的大小控制着有多少信息可以在不收到确认的情况下从一个主机传输到另一个主机。发送方将只发送在窗口大小中指定的字节数，然后等待更新窗口大小的确认。

如果接收应用程序可以在数据到达发送方时快速处理数据，那么接收方将在每次确认时发送一个积极的窗口广告(增加窗口的大小)。它会一直工作，直到发送方的速度比接收方快，并且传入的数据最终会填满接收方的缓冲区，导致接收方用一个零窗口发布确认。接收到零窗口广告的发送方必须停止发送，直到它接收到一个正窗口。看看图示的开窗过程:

![](https://help.mikrotik.com/docs/download/attachments/119144661/tcp-flow-control-using-windowing.jpg?version=1&modificationDate=1653919107937&api=v2)
  
1. “主机A”开始传输，窗口大小为1000，传输1个1000字节帧;
2. 接收端“主机B”返回ACK，窗口大小增加到2000;
3. 主机A接收ACK，发送两帧(每帧1000字节);
4. 之后，接收方将初始窗口大小发布为3000。发送方发送三帧，等待确认;
5. 前三个段填满接收方缓冲区的速度比接收应用程序处理数据的速度要快，因此公告的窗口大小达到零，表明在进一步传输之前有必要等待;
6. 窗口的大小以及增加或减少窗口大小的速度在各种TCP拥塞避免算法(如Reno, Vegas, Tahoe等)中可用;
