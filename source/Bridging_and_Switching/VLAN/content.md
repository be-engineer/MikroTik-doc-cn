# 概述

**标准:** `IEEE 802.1Q, IEEE 802.1ad`

虚拟局域网（VLAN）是一种第2层的方法，它允许在一个物理接口（以太网、无线等）上有多个虚拟局域网，可以有效隔离局域网的能力。

你可以使用MikroTik RouterOS（以及Cisco IOS、Linux和其他路由器系统）来标记这些数据包，以及接受和路由标记的数据包。

由于VLAN在OSI第二层工作，它可以像任何其他网络接口一样使用，没有任何限制。VLAN成功地通过普通的以太网桥。

你也可以通过无线链路传输VLAN，把多个VLAN接口放在一个无线接口上。请注意，由于VLAN不是一个完整的隧道协议（即它没有额外的字段来传输发送方和接收方的MAC地址），在VLAN上桥接和在普通无线接口上桥接的限制相同。换句话说，虽然无线客户端可以参与放在无线接口上的VLAN，但不可能让VLAN放在与任何其他接口桥接的站点模式的无线接口上。

## 802.1Q

虚拟局域网（VLAN）最常用的协议是IEEE 802.1Q。它是一个标准化的封装协议，定义了如何在以太网头中插入一个四字节的VLAN标识。

每个VLAN被视为一个独立的子网。这意味着在默认情况下，一个特定VLAN中的主机不能与另一个VLAN成员的主机通信，尽管它们连接在同一个交换机中。因此，如果你想进行VLAN间的通信，你需要一个路由器。RouterOS支持多达4095个VLAN接口，每个接口都有一个独特的VLAN ID。VLAN的优先级也可以被使用和操作。

当VLAN延伸到一个以上的交换机上时，交换机之间的链接必须成为 "聚合"，数据包被标记以表明它们属于哪个VLAN。聚合承载多个VLAN的流量；它就像一条点对点的链路，在交换机之间或在交换机和路由器之间承载标记的数据包。

IEEE 802.1Q标准保留了有特殊用途的VLAN ID，以下VLAN ID不应该用于通用VLAN设置。0, 1, 4095

## Q-in-Q

原始的802.1Q只允许一个VLAN头，Q-in-Q允许两个或更多的VLAN头。在RouterOS中，Q-in-Q可以通过在另一个VLAN接口上添加一个VLAN接口来进行配置。例子。

```shell
/interface vlan
add name=vlan1 vlan-id=11 interface=ether1
add name=vlan2 vlan-id=12 interface=vlan1

```
  
如果任何数据包通过'vlan2'接口发送，两个VLAN标签将被添加到以太网头中 - '11'和'12'。

## 属性

| 属性                                                                                                | 说明                                                                                                                                                                                                                                                                                                                                                                                                                           |
| --------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **arp** (_disabled \| enabled \| local-proxy-arp \| proxy-arp \| reply-only_; Default: **enabled**) | 地址解析协议设置<br>- `disabled`- 接口将不使用ARP<br>-  `enabled` - 该接口将使用ARP<br>- `local-proxy-arp`- 路由器在接口上执行代理ARP，并向同一接口发送回复。<br>- `proxy-arp`- 路由器在该接口上执行代理ARP，并向其他接口发送回复。<br>- `reply-only `- 接口将只回复来自匹配的IP地址/MAC地址组合的请求，这些组合在IP/ARP表中被输入为静态项。动态项不会自动存储在IP/ARP表中。因此，要使通信成功，必须已经存在一个有效的静态项。 |
| **arp-timeout** (_auto \| integer_; Default: **auto**)                                              | 在没有收到IP的数据包时，ARP记录在ARP表中保留多长时间。值 `auto` 等于IP/Settings中 `arp-timeout` 的值，默认为30s。                                                                                                                                                                                                                                                                                                              |
| **disabled** (_yes \| no_; Default: **no**)                                                         | 改变网桥是否被禁用。                                                                                                                                                                                                                                                                                                                                                                                                           |
| **interface** (_name_; Default: )                                                                   | 接口名称，VLAN将在该接口上工作。                                                                                                                                                                                                                                                                                                                                                                                               |
| **mtu** (_integer_; Default: **1500**)                                                              | 第三层 最大传输单位                                                                                                                                                                                                                                                                                                                                                                                                            |
| **name** (_string_; Default: )                                                                      | 接口名称                                                                                                                                                                                                                                                                                                                                                                                                                       |
| **use-service-tag** (_yes \| no_; Default: )                                                        | 兼容IEEE 802.1ad的服务标签                                                                                                                                                                                                                                                                                                                                                                                                     |
| **vlan-id** (_integer: 4095_; Default: **1**)                                                       | 用于区分VLAN的虚拟LAN标识符或标签。对于属于同一VLAN的所有计算机必须是相同的。                                                                                                                                                                                                                                                                                                                                                  |

MTU应该设置为1500字节，与以太网接口一样。但是，这可能不适合某些以太网卡，它们不支持接收/发送添加了VLAN头的全尺寸以太网数据包（1500字节数据+4字节VLAN头+14字节以太网头）。在这种情况下，可以使用MTU 1496，但要注意，如果要在接口上发送较大的数据包，这将导致数据包碎片化。同时要记住，如果源和目的地之间的路径MTU发现工作不正常，MTU 1496可能会引起问题。

## 设置实例

### 第二层VLAN实例

可以使用多种可能的配置，但每种配置类型都是为一组特殊的设备设计的，因为有些配置方法会让你获得内置交换芯片的好处，获得更大的吞吐量。请查看 [Basic VLAN switching](https://help.mikrotik.com/docs/display/ROS/Basic+VLAN+switching)指南，看看每种类型的设备应该使用哪种配置，以获得最大可能的吞吐量和兼容性，该指南显示了如何设置一个非常基本的VLAN中继/接入端口配置。

还有一些其他的方法来设置VLAN标记或VLAN交换，但推荐的方法是使用 [Bridge VLAN Filtering](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-BridgeVLANFiltering)。确保你没有使用任何 [已知的第二层错误配置](https://help.mikrotik.com/docs/display/ROS/Layer2+misconfiguration)。

### 第三层VLAN实例

#### 简单的VLAN路由

假设我们有几个MikroTik路由器连接到一个集线器。集线器是一个OSI物理层的设备（如果在路由器之间有一个集线器，那么从L3的角度来看，它与路由器之间的以太网电缆连接是一样的）。为简化起见，假设所有的路由器都使用ether1接口与集线器连接，并分配了IP地址，如下图所示。然后在每个路由器上创建VLAN接口。

R2和R4的配置如下所示。

R2:

```shell
[admin@MikroTik] /interface vlan> add name=VLAN2 vlan-id=2 interface=ether1 disabled=no
 
[admin@MikroTik] /interface vlan> print
Flags: X - disabled, R - running, S - slave
 #    NAME                  MTU   ARP        VLAN-ID INTERFACE               
0 R  VLAN2                 1500  enabled    2       ether1

```

R4:

```shell
[admin@MikroTik] /interface vlan> add name=VLAN2 vlan-id=2 interface=ether1 disabled=no
 
[admin@MikroTik] /interface vlan> print
Flags: X - disabled, R - running, S - slave
 #    NAME                  MTU   ARP        VLAN-ID INTERFACE               
0 R  VLAN2                 1500  enabled    2       ether1

```

下一步是为VLAN接口分配IP地址。

R2:

```shell
[admin@MikroTik] ip address> add address=10.10.10.3/24 interface=VLAN2
[admin@MikroTik] ip address> print
Flags: X - disabled, I - invalid, D - dynamic
  #   ADDRESS            NETWORK         BROADCAST       INTERFACE
  0   10.0.1.4/24        10.0.1.0        10.0.1.255      ether1
  1   10.20.0.1/24       10.20.0.0       10.20.0.255     pc1
  2   10.10.10.3/24      10.10.10.0      10.10.10.255    vlan2
 
[admin@MikroTik] ip address>

```

R4:

```shell
[admin@MikroTik] ip address> add address=10.10.10.5/24 interface=VLAN2
 [admin@MikroTik] ip address> print
 Flags: X - disabled, I - invalid, D - dynamic
   #   ADDRESS            NETWORK         BROADCAST       INTERFACE
   0   10.0.1.5/24        10.0.1.0        10.0.1.255      ether1
   1   10.30.0.1/24       10.30.0.0       10.30.0.255     pc2
   2   10.10.10.5/24      10.10.10.0      10.10.10.255    vlan2
 
[admin@MikroTik] ip address>

```

这样应该可以从R2路由器ping到R4路由器，反之亦然。

```shell
"Ping from R2 to R4:"
 
[admin@MikroTik] ip address> /ping 10.10.10.5
 
10.10.10.5 64 byte ping: ttl=255 time=4 ms
 
10.10.10.5 64 byte ping: ttl=255 time=1 ms
 
2 packets transmitted, 2 packets received, 0% packet loss
 
round-trip min/avg/max = 1/2.5/4 ms
 
 
"From R4 to R2:"
 
[admin@MikroTik] ip address> /ping 10.10.10.3
10.10.10.3 64 byte ping: ttl=255 time=6 ms
10.10.10.3 64 byte ping: ttl=255 time=1 ms
2 packets transmitted, 2 packets received, 0% packet loss
round-trip min/avg/max = 1/3.5/6 ms

```
  
为了确定VLAN设置是否正常工作，尝试从R2 ping R1。如果ping是超时的，那么VLAN就成功隔离了。

```shell
"From R2 to R1:"
 
[admin@MikroTik] ip address> /ping 10.10.10.2
10.10.10.2 ping timeout
10.10.10.2 ping timeout
3 packets transmitted, 0 packets received, 100% packet loss

```

#### VLAN间的路由

如果在交换机上实现了独立的VLAN，那么就需要一个路由器来提供VLAN之间的通信。交换机工作在OSI第二层，所以它只使用以太网头进行转发，不检查IP头。由于这个原因，我们必须使用作为每个VLAN的网关的路由器。没有路由器，主机就无法在自己的VLAN之外进行通信。上述VLAN之间的路由过程被称为VLAN间通信。

为了说明VLAN间的通信，我们将创建一个聚合，在Mikrotik路由器和支持VLAN聚合的可管理交换机之间的一条链路上传输来自三个VLAN（VLAN2和VLAN3、VLAN4）的流量。

如上图所示，每个VLAN都有自己独立的子网（广播域）。

- VLAN 2 – 10.10.20.0/24;
- VLAN 3 – 10.10.30.0/24;
- VLAN 4 – 10.10.40.0./24.

大多数交换机上的VLAN配置很简单，我们需要定义哪些端口是VLAN的成员，并定义一个 "聚合 "端口，该端口可以在交换机和路由器之间传输标记帧。

创建VLAN接口。

```shell
/interface vlan
add name=VLAN2 vlan-id=2 interface=ether1 disabled=no
add name=VLAN3 vlan-id=3 interface=ether1 disabled=no
add name=VLAN4 vlan-id=4 interface=ether1 disabled=no

```
  
添加IP地址到VLAN:

```shell
/ip address
add address=10.10.20.1/24 interface=VLAN2
add address=10.10.30.1/24 interface=VLAN3
add address=10.10.40.1/24 interface=VLAN4

```

#### RouterOS /32和IP非数字地址

在RouterOS中，要用地址创建一个点对点的隧道，必须使用带有网络掩码'/32'的地址，这实际上带来了与一些供应商的无编号IP地址一样的功能。

有2个路由器RouterA和RouterB，其中每个都是网络10.22.0.0/24和10.23.0.0/24的一部分，要使用VLAN作为载体连接这些路由器，配置如下。

RouterA:

```shell
/ip address add address=10.22.0.1/24 interface=ether1
/interface vlan add interface=ether2 vlan-id=1 name=vlan1
/ip address add address=10.22.0.1/32 interface=vlan1 network=10.23.0.1
/ip route add gateway=10.23.0.1 dst-address=10.23.0.0/24

```

RouterB:

```shell
/ip address add address=10.23.0.1/24 interface=ether1
/interface vlan add interface=ether2 vlan-id=1 name=vlan1
/ip address add address=10.23.0.1/32 interface=vlan1 network=10.22.0.1
/ip route add gateway=10.22.0.1 dst-address=10.22.0.0/24

```
