# 基本概念介绍

![](https://help.mikrotik.com/docs/download/attachments/328229/firewall-fundamental.jpg?version=2&modificationDate=1572439380369&api=v2)

防火墙实现了有状态（通过利用连接跟踪）和无状态数据包过滤，从而提供了安全功能，用于管理进出路由器的数据流。与网络地址转换（NAT）一起，可以防止未经授权访问直接连接的网络和路由器本身的工具，也是出站流量的一个过滤器。

网络防火墙使外部威胁远离网络内部的敏感数据。每当不同的网络连接在一起时，总是有一种威胁，即来自网络之外的人闯入你的局域网。这种闯入可能导致私人数据被盗和传播，有价值的数据被改变或破坏，或整个硬盘被删除。防火墙用作防止或尽量减少连接到其他网络的固有安全风险的手段。正确配置的防火墙在高效和安全的网络基础设施部署中发挥着关键作用。

MikroTik RouterOS有一个非常强大的防火墙，功能包括。

- 状态包检查
- 点对点协议过滤
- 通过以下方式进行流量分类
  - 源MAC地址
  - IP地址（网络或列表）和地址类型（广播、本地、多播、单播）
  - 端口或端口范围
  - IP协议
  - 协议选项（ICMP类型和代码域、TCP标志、IP选项和MSS）
  - 数据包到达或离开的接口
  - 内部流量和连接标记
  - DSCP字节
  - 数据包内容
  - 数据包到达的速率和序列号
  - 数据包大小
  - 数据包到达时间

还有很多!

## 防火墙如何工作

防火墙通过防火墙规则运行。每个规则由两部分组成 **匹配器**，根据给定的条件匹配流量， **动作** 定义如何处理匹配的数据包。

RouterOS利用防火墙的5个子功能：

- Connection tracking
- Filters
- NAT
- Mangle
- RAW

### 连接状态

要完全理解防火墙规则，首先必须了解可能适用于特定网络数据包的各种状态。在RouterOS中，有五种连接状态。

- **NEW** - 新状态告诉我们，该数据包是看到的第一个数据包。意味着conntrack模块看到的第一个数据包，在一个特定的连接中被匹配。例如，如果一个SYN数据包是一个连接中的第一个数据包，它将被匹配。
- **ESTABLISHED -** _ESTABLISHED_ 状态在两个方向都看到了流量，然后会持续匹配这些数据包。_ESTABLISHED_ 连接是相当容易理解的。进入 _ESTABLISHED_ 状态的唯一要求是一台主机发送了一个数据包，随后它从另一台主机得到了一个回复。在收到回复数据包后，_NEW_ 状态将改变为 _ESTABLISHED_ 状态，或通过防火墙。
- **RELATED** - 连接被认为是 _RELATED_ ，当它与另一个已经 _ESTABLISHED_ 的连接有关。为了使一个连接被认为是 _RELATED_，必须首先有一个被认为是 _ESTABLISHED_ 的连接，然后 _ESTABLISHED_ 连接将在主连接之外产生一个连接。然后新产生的连接将被认为是 _RELATED_ ，例如，一个开始FTP数据连接的数据包。
- **INVALID**- _INVALID_ 状态意味着数据包无法被识别，或者没有任何状态。 建议丢弃这种状态下的所有流量。
- **UNTRACKED** - 数据包设置为绕过防火墙RAW表中的连接跟踪。  

### 配置实例

看一下保护路由器的基本防火墙设置。默认RouterOS防火墙接受一切，阻断是通过在所有规则的末尾添加一个过滤规则来丢弃一切。如果路由器只想允许ICMP、ssh和Winbox，而丢弃其他的，可按下面设置：

```shell
/ip firewall filter
add chain=input connection-state=invalid action=drop comment="Drop Invalid connections"
add chain=input connection-state=established,related,untracked action=accept comment="Allow Established/Related/Untracked connections"
add chain=input protocol=icmp action=accept ;comment="Allow ICMP"
add chain=input protocol=tcp ports=8291,22 action=accept comment="Allow Winbox and SSH"
add chain=input action=drop comment="Drop everything else"
```

RouterOS还允许在连接跟踪前过滤数据包，并有选择只发送特定的流量到连接跟踪。这可以大大减少CPU的负荷，减少DOS/DDoS攻击。这种规则配置是在RAW过滤表中完成的。

额外的 _/ip firewall filter_ 配置例子可在 [建立第一个防火墙](https://help.mikrotik.com/docs/display/ROS/Building+Your+First+Firewall) 部分找到。

## 连接跟踪

连接跟踪允许内核跟踪所有的逻辑网络连接或会话，从而将可能构成该连接的所有数据包联系起来。NAT依靠这一信息，以同样的方式翻译所有相关的数据包。连接跟踪可以使用有状态防火墙功能，也可以是无状态协议，如UDP。

跟踪的连接列表可以在ipv4的 _/ip firewall connection_ 和IPv6的 _/ipv6 firewall connection_ 中看到。

```shell
[admin@MirkoTik] /ip firewall connection> print
Flags: S - seen-reply, A - assured
# PR.. SRC-ADDRESS DST-ADDRESS TCP-STATE TIMEOUT
0 udp 10.5.8.176:5678 255.255.255.255:5678 0s
1 udp 10.5.101.3:646 224.0.0.2:646 5s
2 ospf 10.5.101.161 224.0.0.5 9m58s
3 udp 10.5.8.140:5678 255.255.255.255:5678 8s
4 SA tcp 10.5.101.147:48984 10.5.101.1:8291 established 4m59s
```
  
根据连接表的内容，到达的数据包可以分配到其中一个连接状态。**新的，无效的，已建立的，相关的** 或 **未跟踪的**。

当数据包是 **新** 的时候，有两种不同的方法。第一种是在无状态连接（如UDP）的情况下，当连接表中没有连接条目时。另一种是在有状态协议（TCP）的情况下。在这种情况下，一个开始新连接的新数据包总是一个带有 _SYN_ 标志的TCP数据包。

如果数据包不是新的，可以属于 _已建立_ 或 _相关_ 连接，或者不属于任何连接，使其 _无效_ 。有 _稳定_ 状态的数据包，正如大多数人猜到的，属于连接跟踪表中的一个现有连接。和 _相关_ 状态类似，除了该数据包属于一个与现有连接相关的连接。例如，ICMP错误数据包或FTP数据连接数据包。

连接状态 **未跟踪** 是一种特殊情况，当使用RAW防火墙规则将连接排除在连接跟踪之外。这一个规则将使所有转发的流量绕过连接跟踪引擎，加速通过设备的数据包处理。

任何其他数据包都被认为是 _无效_ 的，在大多数情况下应该丢弃。

基于这些信息，我们可以设置一套基本的过滤规则，通过接受_已建立的/相关的_数据包，丢弃 _无效_ 数据包，只对 _新_ 数据包进行更详细的过滤，从而加快数据包的过滤速度，减少CPU的负荷。

```shell
ip firewall filter
add chain=input connection-state=invalid action=drop comment="Drop Invalid connections"
add chain=input connection-state=established,related,untracked action=accept comment="Allow Established/Related/Untracked connections
```

这样的规则集不要用于具有非对称路由的路由器，因为非对称路由的数据包可能被认为是无效的被丢弃。

## 快速跟踪

IPv4快速跟踪处理程序被自动用于标记的连接。使用防火墙动作 "fasttrack-connection "来标记快速跟踪的连接。目前，只有TCP和UDP连接可以被实际快速跟踪（尽管任何连接都可以被标记为快速跟踪）。IPv4快速跟踪处理程序支持NAT（SNAT、DNAT，或两者）。

请注意，一个连接中并非所有的数据包都可以被快速跟踪，因此，即使连接被标记为快速跟踪，也可能会看到一些数据包通过慢速路径。这就是为什么fasttrack-connection后面通常有一个相同的"_action=accept_"规则的原因。快速跟踪数据包会绕过防火墙、连接跟踪、简单队列、带有 _parent=global_ 的队列树、IP审计、IPSec、热点通用客户端、VRF分配，因此，管理员要确保快速跟踪不干扰其他配置。

### 要求

如果满足以下条件，IPv4快速跟踪将被激活。

- 没有Mesh、metarouter接口配置。
- 嗅探器、火炬或流量发生器没有运行。
- _/tool mac-scan_ 未被积极使用。
- _/tool ip-scan_ 未被主动使用。
- 在 _IP/Settings_ 下启用了FastPath和路由缓存。

### 示例

对于有出厂默认配置的SOHO路由器，可以通过放在防火墙过滤器顶部的这一规则来快速跟踪所有的LAN流量。需要同样的配置接受规则。

```shell
/ip firewall filter add chain=forward action=fasttrack-connection connection-state=established,related
/ip firewall filter add chain=forward action=accept connection-state=established,related
```

- 连接被快速跟踪，直到连接被关闭、超时或路由器被重启。
- 只有在FastTrack防火墙规则被删除、停用和路由器重启后，假规则才会消失。
- 当设备上的FastPath和FastTrack都启用时，一次只能激活一个。

队列（除非队列树被赋予接口）、防火墙过滤器和混杂规则不会应用于快速跟踪的流量。

## 服务

本节列出了各种MikroTik RouterOS服务所使用的协议和端口。可以帮助确定为什么MikroTik路由器要监听某些端口，以及在想阻止或允许访问某些服务时，需要阻止/允许什么。 

默认的服务是：

| Property    | Description                                                   |
| ----------- | ------------------------------------------------------------- |
| **telnet**  | Telnet service                                                |
| **ftp**     | FTP service                                                   |
| **www**     | Webfig http service                                           |
| **ssh**     | SSH service                                                   |
| **www-ssl** | Webfig HTTPS service                                          |
| **api**     | API service                                                   |
| **winbox**  | 负责Winbox工具的访问，以及Tik-App智能手机应用程序和Dude探测器 |
| **api-ssl** | API over SSL service                                          |

## 属性

注意，不能添加新的服务，只允许对现有的服务进行修改。

| Property                                                                | Description                                                            |
| ----------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| **address** (_IP address/netmask            \| IPv6/0..128_; Default: ) | 可访问服务的IP/IPv6前缀列表。                                          |
| **certificate** (_name_; default: **none**)                             | 特定服务使用的证书名称。仅适用于依赖证书的服务（_www-ssl, api-ssl_）。 |
| **name** (_name_; default: **none**)                                    | 服务名称                                                               |
| **port** (_integer: 1...65535_; Default: )                              | 特定服务监听的端口。                                                   |

为了限制Winbox服务只从 **192.168.88.0/24** 子网访问设备，必须配置如下：

```shell
[admin@MikroTik] > ip service set [find name~"winbox"] address=192.168.88.0/24
[admin@MikroTik] > ip service print
Flags: X - disabled, I - invalid
# NAME PORT ADDRESS CERTIFICATE
0 telnet 23
1 XI ftp 21
2 XI www 80
3 ssh 22
4 XI www-ssl 443 none
5 XI api 8728
6 winbox 8291 192.168.88.0/24
7 XI api-ssl 8729 none
```

建议禁用未使用的服务。

## 地址列表

防火墙地址列表允许用户创建IP地址列表，这些地址在一个共同的名称下组合在一起。然后，防火墙过滤器、Mangle和NAT可以使用这些地址列表对数据包进行匹配。地址列表记录也可以通过NAT、Mangle和过滤器中的 _action=add-src-to-address-list_ 或 _action=add-dst-to-address-list_ 项目动态更新。 
带有 _add-src-to-address-list_ 或 _add-dst-to-address-list_ 动作的防火墙规则在穿透模式下工作，这意味着匹配的数据包将被传递到下一个防火墙规则。一个动态创建地址列表的基本例子:

```shell
[admin@MirkoTik] > ip firewall address-list add address=www.mikrotik.com list=MikroTik
[admin@MirkoTik] > ip firewall address-list print
Flags: X - disabled, D - dynamic
# LIST ADDRESS CREATION-TIME TIMEOUT
0 MikroTik www.mikrotik.com oct/09/2019 14:53:14
1 D ;;; www.mikrotik.com
MikroTik 159.148.147.196 oct/09/2019 14:53:14
```

## Layer7-protocol

Layer7-protocol是一种在ICMP/TCP/UDP数据流中搜索模式的方法。它收集一个连接的前10个数据包或一个连接的前2KB，并在收集的数据中搜索模式。如果在收集的数据中没有找到该模式，匹配器就停止进一步检查。所分配的内存被释放，协议被认为是未知的。要考虑到大量的连接将大大增加内存和CPU的使用。为了避免这种情况，添加定期的防火墙匹配，以减少重复传递给第七层过滤器的数据量。

一个额外的要求是，第七层匹配器必须看到两个方向的流量（入站和出站）。为了满足这一要求，应在转发链中设置l7规则。如果在input/prerouting链中设置了规则，那么在output/postrouting链中也必须设置同样的规则，否则，收集的数据可能不完整，导致错误的匹配模式。

在这个例子中用一个模式来匹配RDP数据包。

`/ip firewall layer7-protocol add name=rdp regexp="rdpdr.*cliprdr.*rdpsnd"`

如果Layer7匹配器识别了这个连接，那这个规则就会把这个连接标记为 "自己的"，其他规则就不会再看这个连接，即使两个带有Layer7匹配器的防火墙规则是相同的也如此。

当用户使用HTTPS时，Layer7规则将无法匹配这个流量。**只有未加密的HTTP可以匹配**。
