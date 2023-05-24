# 介绍

[ZeroTier](https://www.zerotier.com/manual/) 网络管理程序是一个自包含的网络虚拟化引擎，它实现了一个类似于 [VXLAN](https://en.wikipedia.org/wiki/Virtual_Extensible_LAN) 的以太网虚拟化层，构建在加密安全的全局点对点网络之上。它提供了与企业SDN交换机相当的高级网络虚拟化和管理功能，但跨越局域网和广域网，并连接几乎任何类型的应用程序或设备。

microtik已经将ZeroTier作为一个单独的包添加到RouterOS v7.1rc2中，用于 **ARM/ARM64** 架构。

等等，那我能用它做什么?

- 在家里托管一个游戏服务器(对局域网游戏很有用)，或者和你的朋友一起创建一个局域网派对;
- 直接访问NAT后的局域网设备;
- 通过SSH访问局域网设备，而不打开连接互联网的端口;
- 使用本地Pi-Hole设置从任何地方通过互联网;

## 视频教程

-   [ZeroTier](https://youtu.be/60uIlyF8Z5s)

# 必要的网络配置

ZeroTier使用哪些端口?

它监听三个3 UDP端口:

- 9993—默认值
- 从您的零层地址中派生的随机高编号端口
- 一个随机的高编号端口，用于UPnP/NAT-PMP映射

这意味着你的对等体可以在任何端口上监听。要直接与它们对话，您需要能够将它们发送到任何端口。

推荐配置本地网络和外网网关

这些ZeroTier推荐的指南与绝大多数使用商品网关和接入点的典型部署一致:

- 不限制UDP出方向流量。
—在您的网络中支持UPnP或NAT- pmp可以通过允许ZeroTier端点映射外部端口并完全避免NAT穿越来极大地提高性能。
- 建议使用IPv6协议，如果直连链路两端都支持IPv6协议，可以大大提高直连链路的可靠性。如果存在，它应该在没有NAT的情况下实现(NAT对于IPv6来说是完全不必要的，只会增加复杂性)，并使用允许双向UDP会话的有状态防火墙。
- 不要使用“对称”NAT。使用“全锥”或“端口限制锥”NAT。对称NAT对点对点流量非常不利，并且会降低VoIP，视频聊天，游戏，WebRTC和许多其他协议以及ZeroTier。
- 零层端点与Internet之间的NAT不能超过一层。多层NAT由于不同层间状态和行为的混乱交互，导致连接不稳定。**禁止双重NAT**
- nat的端口映射或连接超时时间不小于60秒。
- 每个nat管理的外部IP地址后面的设备数量不超过16000台，以保证每个设备映射的端口数量充足。
- 交换机和无线接入点应允许本地设备之间的直接本地通信。关闭任何“本地隔离”功能。有些交换机可能允许更细粒度的控制，在这些交换机上，允许本地UDP流量进出9993(或一般情况下)就足够了。

# 配置示例

![](https://help.mikrotik.com/docs/download/attachments/83755083/ZeroTier_ilustracija.png?version=1&modificationDate=1640071414044&api=v2)

缺省情况下，ZeroTier被设计为零配置。用户无需编写配置文件或提供其他节点的IP地址即可启动新的ZeroTier节点。它的设计也是为了快速。世界上任何两台设备都应该能够相互定位并几乎立即通信，所以下面的例子将在RouterOS设备上启用ZeroTier，并使用ZeroTier应用程序连接一台手机。


1.  注册 [my.zerotier.com](https://my.zerotier.com/) 并创建网络，获取Network ID，本例中为:_1d71939404912b40_;

![](https://help.mikrotik.com/docs/download/attachments/83755083/network.jpg.png?version=1&modificationDate=1640071063702&api=v2)
2.  [下载](https://mikrotik.com/download) 并在RouterOS中安装ZeroTier NPK包，您可以在“Extra packages”下找到，将包上传到设备并重启设备;
3. 启用默认的(官方的)ZeroTier实例:
    
`[admin@mikrotik] > zerotier/enable zt1`
    
4.  添加一个新网络，指定你在ZeroTier云控制台中创建的网络ID:
    
`[admin@mikrotik] zerotier/interface/add network=1d71939404912b40 instance=zt1`
    
5.  验证ZeroTier配置:
    
```shell
[admin@MikroTik] > zerotier/interface/print
Flags: R - RUNNING
Columns: NAME, MAC-ADDRESS, NETWORK, NETWORK-NAME, STATUS
#   NAME       MAC-ADDRESS        NETWORK           NETWORK-NAME     STATUS
0 R zerotier1  42:AC:0D:0F:C6:F6  1d71939404912b40  modest_metcalfe  OK
```
    
6.  现在需要允许从ZeroTier接口连接到路由器，以及可选连接到其他局域网接口:
    
```shell
/ip firewall filter add action=accept chain=forward in-interface=zerotier1 place-before=0
/ip firewall filter add action=accept chain=input in-interface=zerotier1 place-before=0
```
    
7.  在您的智能手机或计算机上安装ZeroTier客户端，按照ZeroTier手册了解如何从那里连接到相同的网络。
8.  当Access Control设置为Private时，需要对节点进行授权才能成为成员:
    ![](https://help.mikrotik.com/docs/download/attachments/83755083/Screenshot_2.png?version=1&modificationDate=1640071629089&api=v2)
9.  
```shell
[admin@MikroTik] > ip/address/print where interface~"zero"
Flags: D - DYNAMIC
Columns: ADDRESS, NETWORK, INTERFACE
#   ADDRESS             NETWORK        INTERFACE
3 D 192.168.192.105/24  192.168.192.0  zerotier1
 
[admin@MikroTik] > ping 192.168.192.252 count=3
SEQ HOST                                     SIZE TTL TIME       STATUS                                                                                                                                          
0 192.168.192.252                            56  64 407us    
1 192.168.192.252                            56  64 452us    
2 192.168.192.252                            56  64 451us    
sent=3 received=3 packet-loss=0% min-rtt=407us avg-rtt=436us max-rtt=452us
   ```
    

您应该在 [ZeroTier云控制台](https://my.zerotier.com/) 中指定到特定内部子网的路由，以确保从其他设备连接时可以访问这些网络。

### 对等体

`zerotier/peer/`

ZeroTier的peer是一个信息部分，其中包含您的节点所知道的节点列表。节点之间不能相互通信，除非它们在同一网络上加入并获得授权。

```shell
[admin@Home] > zerotier/peer/print
Columns: INSTANCE, ZT-ADDRESS, LATENCY, ROLE, PATH
# INSTANCE  ZT-ADDRESS  LATENCY  ROLE    PATH                                                           
0 zt1       61d294b9cb  186ms    PLANET  active,preferred,50.7.73.34/9993,recvd:4s526ms                 
1 zt1       62f865ae71  270ms    PLANET  active,preferred,50.7.252.138/9993,recvd:4s440ms,sent:9s766ms  
2 zt1       778cde7190  132ms    PLANET  active,preferred,103.195.103.66/9993,recvd:4s579ms,sent:9s766ms
3 zt1       992fcf1db7  34ms     PLANET  active,preferred,195.181.173.159/9993,recvd:4s675ms,sent:4s712ms
4 zt1       159924d630  130ms    LEAF    active,preferred,34.121.192.xx/21002,recvd:3s990ms,sent:3s990ms
```

# 参数

`[admin@MikroTik] > zerotier/`

| 属性                                      | 说明                                          |
| ----------------------------------------- | --------------------------------------------- |
| **name** (s_tring_;default:**zt1**)       | 实例名。                                      |
| **port** (_number;_ default: **9993**)    | 实例监听的端口号。                            |
| **identity** (_string_;default)           | 实例40位唯一地址。                            |
| **interface** (string;default: **all)**   | 使用ARP和IP类型连接发现零层对等体的接口列表。 |
| **route-distance** (number;default:**1**) | 从行星/月球服务器获得的路由距离。             |

`[admin@MikroTik] > zerotier/interface/`

| 属性                                           | 说明                                    |
| ---------------------------------------------- | --------------------------------------- |
| **allow-default** (_string;yes \| no)_         | 网络可以覆盖系统默认路由(强制VPN模式)。 |
| **allow-global** (_string;yes \| no)_          | ZeroTier IP地址和路由可以重叠。         |
| **allow-managed** (_string;yes \| no)_         | ZeroTier管理IP地址和路由分配。          |
| **arp-timeout** (_number_;default: **auto**)   | ARP超时值。                             |
| **comment** (_string_;Default:)                | 接口的描述性注释。                      |
| **copy-from**                                  | 允许复制现有接口配置。                  |
| **disable-running-check** (_string;yes \| no)_ | 强制界面处于“running”状态。             |
| **instance** (_string_;Default:**zt1**)        | ZeroTier实例名。                        |
| **name** (s_tring_;default: **zerotier1**)     | 短名称。                                |
| **network** (_string_;Default)                 | 16位网络ID。                            |

# 控制器



RouterOS以节点的角色实现了ZeroTier功能，其中大多数网络配置必须在ZeroTier网页仪表板上完成。然而，在你希望在自己的设备上完成所有配置的情况下，RouterOS可以为你提供自己的控制器

一个常见的误解是将网络控制器与根服务器(行星和卫星)混为一谈。根服务器是在 [VL1级别](https://docs.zerotier.com/zerotier/manual/#2networkhypervisoroverviewaname2a) 运行的连接促进器。网络控制器是属于 [VL2级别](https://docs.zerotier.com/zerotier/manual/#22vl2theethernetvirtualizationlayeraname2_2a) 的配置管理器和证书颁发机构。一般来说，根服务器不加入或控制虚拟网络，网络控制器也不是根服务器，尽管节点可以同时执行这两项任务。

`/zerotier/controller/`

每个ZeroTier实例都有一个可用于托管虚拟网络的自托管网络控制器。控制器负责允许成员进入网络，并发布包括证书在内的默认配置信息。理论上，控制器可以承载多达2^24个网络，并为数百万(或更多)设备提供服务，但出于负载平衡和容错的原因，我们建议将大量网络分布在许多控制器上。

## 参数

| 属性                                             | 说明                                                                                                                                                                                                                  |
| ------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **broadcast**  _( yes\| no; Default: **yes**)_   | 允许接收广播(_FF:FF:FF:FF:FF:FF_)报文。                                                                                                                                                                               |
| **comment** (_string_;Default:)                  | 控制器的描述性注释。                                                                                                                                                                                                  |
| **copy-from** (_string_;Default:)                | 复制现有项。它从另一个项目中获取新项目属性的默认值。如果不想进行精确的复制，可以为某些属性指定新值。当复制有名称的项时，通常需要为副本指定一个新名称。                                                                |
| **instance** (_string_;Default:**zt1**)          | ZeroTier实例名。                                                                                                                                                                                                      |
| **ip-range** (_ip_;Default:)                     | IP范围，_例如，172.16.16.1-172.16.16.254。_                                                                                                                                                                           |
| **ip6-6plane** _(yes \| no;Default:**no**)_      | 一个选项为/40网络中的每个成员提供/80，但使用NDP仿真将_all_ ip路由到该/80下的所有者。“6plane”模式对于像Docker这样的用例来说是非常好的，因为它允许每个成员在其/80范围内分配IPv6地址，这些地址在网络上即时和全局地工作。 |
| **ip6-rfc4193** _(yes \| no;Default:**no**)_     | _rfc4193_模式在/88网络上为每个成员提供/128。                                                                                                                                                                          |
| **ip6-range** (_IPv6_ ;Default:)                 | IPv6范围，_for example fd00:feed:feed:beef::-fd00:feed:feed:beef:ffff:ffff:ffff:ffff:ffff。_                                                                                                                          |
| **mtu** _(integer;_ Default:**2800**)            | 网络mtu。                                                                                                                                                                                                             |
| **multicast-limit** (_integer_: Default: **32**) | 组播报文的最大接收方。                                                                                                                                                                                                |
| **name** (_string_;Default:)                     | 该控制器的短名称。                                                                                                                                                                                                    |
| **network** (_string_;Default)                   | 16位网络ID。                                                                                                                                                                                                          |
| **private** _(yes \| no;Default:**yes**)_        | 启用访问控制。                                                                                                                                                                                                        |
| **routes** (_IP@GW_; Default: )                  | 按以下格式推送路由:<br>_Routes ::= Route[,Routes]_  <br>  _Route ::= Dst[@Gw]_                                                                                                                                        |

## 配置示例

在下面的示例中，将使用RouterOS内置的ZeroTier控制器向新网络主机发送适当的证书、凭据和配置信息。控制器将从“RouterOS Home”设备操作，我们将加入我们的网络3个单元:手机，笔记本电脑，RouterOS Office设备，理论上可以在一个网络中加入多达100个设备。

![](https://help.mikrotik.com/docs/download/attachments/83755083/ZeroTier_ilustracija_2.png?version=1&modificationDate=1649918837632&api=v2)

### RouterOS Home

首先，我们启用在 **VL1** 级别运行的默认实例:

```shell
[admin@Home] /zerotier> print
Columns: NAME, PORT, IDENTITY.PUBLIC
# NAME  PORT  IDENTITY.PUBLIC                                                                                                                             
;;; ZeroTier Central controller - https://my.zerotier.com/
0 zt1   9993  879c0b5265:0:d5fd2d17805e011d9b93ce8779385e427c8f405e520eea9284809d8444de0335a817xxb21aa4ba153bfbc229ca34d94e08de96d925a4aaa19b252da546693a28
```


现在我们通过控制器部分创建一个新的网络，该网络将在 **VL2** 级别上运行。每个网络都有自己的控制器，每个网络ID由控制器地址和控制器ID组合生成。

注意，我们使用 **_private=yes_** 选项来获得更安全的网络:

```shell
[admin@Home] /zerotier> controller/add name=ZT-private instance=zt1 ip-range=172.27.27.10-172.27.27.20 private=yes routes=172.27.27.0/24
[admin@Home] /zerotier> controller/print
Columns: INSTANCE, NAME, NETWORK, PRIVATE
# INSTANCE  NAME        NETWORK           PRIVATE
0 zt1       ZT-private  879c0b5265a99e4b  yes
```

在接口部分下添加新网络:

```shell
[admin@Home] /zerotier> interface/add network=879c0b5265a99e4b name=myZeroTier instance=zt1
[admin@Home] /zerotier> interface/print interval=1
Columns: NAME, MAC-ADDRESS, NETWORK, STATUS
# NAME        MAC-ADDRESS        NETWORK           STATUS      
0 myZeroTier  4A:19:35:6E:00:6E  879c0b5265a99e4b  ACCESS_DENIED
```

每个新的对等体都要求一个控制器加入网络，在这种情况下，我们有ACCESS_DENIED状态，我们必须授权一个新的对等体，这是因为我们使用了 **private=yes** 选项。

授权后，网络中的每个成员从控制器接收到新的对等体的信息，并批准他们可以与它们交换数据包:

```shell
[admin@Home] /zerotier> controller/member/print
Columns: NETWORK, ZT-ADDRESS
#  NETWORK     ZT-ADDRESS
0  ZT-private  879a0b5265
[admin@Home] /zerotier> controller/member/set 0 authorized=yes
```

验证新配置的IP地址和路由:

```shell
[admin@Home] /zerotier> /ip/address/print where interface~"Zero"
Flags: D - DYNAMIC
Columns: ADDRESS, NETWORK, INTERFACE
#   ADDRESS          NETWORK      INTERFACE
4 D 172.27.27.15/24  172.27.27.0  myZeroTier
 
[admin@Home] /zerotier> /ip/route/pr where gateway~"Zero"
Flags: D - DYNAMIC; A - ACTIVE; c, y - COPY
Columns: DST-ADDRESS, GATEWAY, DISTANCE
    DST-ADDRESS     GATEWAY     DISTANCE
DAc 172.27.27.0/24  myZeroTier         0
```

### RouterOS Office

Office设备侧配置。我们将启用默认实例，并请求控制器加入879c0b5265a99e4b网络:

```shell
[admin@office] /zerotier> interface/add network=879c0b5265a99e4b instance=zt1 name=ZT-interface
[admin@office] /zerotier> interface/print interval=1
Columns: NAME, MAC-ADDRESS, NETWORK, STATUS
# NAME          MAC-ADDRESS        NETWORK           STATUS      
0 ZT-interface  4A:40:1C:38:97:BA  879c0b5265a99e4b  ACCESS_DENIED
```

和前面一样，因为网络是私有的，必须通过“RouterOS主设备”来授权一个新的对等体。然后验证从控制器接收到的IP地址和路由:

```shell
[admin@Home] /zerotier> controller/member/print
Flags: A - AUTHORIZED
Columns: NETWORK, ZT-ADDRESS, IP-ADDRESS, LAST-SEEN
#    NETWORK     ZT-ADDRESS  IP-ADDRESS    LAST-SEEN
0 A  ZT-private  879a0b5265  172.27.27.15          
1 A  ZT-private  554a914c7f  172.27.27.17          
2 A  ZT-private  a83ac6032a  172.27.27.10          
3    ZT-private  deba5dc5b1  172.27.27.13  3s348ms 
[admin@Home] /zerotier> controller/member/set 3 authorized=yes
[admin@Home] /zerotier> controller/member/print              
Flags: A - AUTHORIZED
Columns: NETWORK, ZT-ADDRESS, IP-ADDRESS, LAST-SEEN
#    NETWORK     ZT-ADDRESS  IP-ADDRESS    LAST-SEEN
0 A  ZT-private  879a0b5265  172.27.27.15          
1 A  ZT-private  554a914c7f  172.27.27.17          
2 A  ZT-private  a83ac6032a  172.27.27.10          
3 A  ZT-private  deba5dc5b1  172.27.27.13  4s55ms
```

通过ZeroTier验证获得的IP地址和路由:

```shell
[admin@office] /zerotier> /ip/address/print where interface~"ZT"
Flags: D - DYNAMIC
Columns: ADDRESS, NETWORK, INTERFACE
#   ADDRESS          NETWORK      INTERFACE  
0 D 172.27.27.13/24  172.27.27.0  ZT-interface
 
[admin@office] /zerotier> /ip/route/print where gateway~"ZT"
Flags: D - DYNAMIC; A - ACTIVE; c, y - COPY
Columns: DST-ADDRESS, GATEWAY, DISTANCE
    DST-ADDRESS     GATEWAY       DISTANCE
DAc 172.27.27.0/24  ZT-interface         0
```

### 其他设备


为您的手机或电脑 [下载ZeroTier应用程序](https://www.zerotier.com/download/) ，并加入新创建的网络:

1) 通过我们的Laptop ZeroTier应用程序，我们加入了879c0b5265a99e4b网络;

2) 用户Zerotier手机app加入879c0b5265a99e4b网络;

此外，必须在 _/zerotier/controller/member/_ 下授权所有其他新主机。

![](https://help.mikrotik.com/docs/download/attachments/83755083/Screenshot_7.png?version=1&modificationDate=1649918837933&api=v2)

![](https://help.mikrotik.com/docs/download/attachments/83755083/ztAPP%20%282%29.png?version=1&modificationDate=1650365184697&api=v2)