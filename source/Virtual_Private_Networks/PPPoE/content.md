# 概述


PPPoE (Point to Point over Ethernet)是一种简单的将PPP报文封装到以太网帧中的方法。PPPoE是对标准的PPP (Point to Point Protocol)协议的扩展，是PPPoE的继承者。PPPoE标准在 [RFC 2516](https://tools.ietf.org/html/rfc2516) 中定义。PPPoE client和server工作在路由器的任何二层以太网接口上，例如Wireless、Ethernet、EoIP等。一般来说，PPPoE用于根据用户名(如果需要，也可以根据工作站)的身份验证向客户端分发IP地址，而不是仅使用静态IP地址或DHCP的工作站身份验证。出于安全考虑，建议不要在与PPPoE相同的接口上使用静态IP地址或DHCP。

# 介绍

PPPoE提供了通过简单的桥接接入设备将主机网络连接到远程接入集中器的能力。

支持连接:

- MikroTik RouterOS PPPoE client到任意PPPoE server;
- MikroTik RouterOS服务器(接入集中器)到多个PPPoE客户端(客户端可用于几乎所有操作系统和大多数路由器);

# PPPoE操作

PPPoE有两个不同的阶段:

1.  发现阶段;
2.  会话阶段;

## 发现阶段

探索阶段有四个步骤。当它完成时，两个对等体都知道PPPoE 
 SESSION_ID 和对等体的以太网地址，它们一起唯一地定义了PPPoE会话:

1. **PPPoE Active Discovery Initialization (PADI)** PPPoE client向广播地址发送一个_padi报文。如果在PPPoE client的拨号网络属性中已经输入了服务名称，该报文也可以填充service-name字段。如果没有输入服务名称，则不填充此字段
2.  **PPPoE Active Discovery Offer (PADO)** 如果Access Concentrator能够服务PADI包中列出的“service-name”字段，PPPoE server或Access Concentrator应该用PADO响应PADI。如果没有列出“service-name”字段，则访问集中器将使用一个_PADO_包进行响应，该包具有“service-name”字段，其中填充了访问集中器可以服务的服务名称。PADO报文发送到PPPoE client的单播地址
3. **PPPoE Active Discovery Request (PADR)** 当PPPoE client收到PADO报文时，将返回一个PADR报文。该报文被发送到接入集中器的单播地址。客户端可以接收多个PADO包，但是客户端会响应接收到的第一个有效的PADO包。如果初始的PADR包有一个空白的“service-name”字段，客户机将使用PADR包中返回的第一个服务名称填充PADR包的“service-name”字段。
4.  **PPPoE Active Discovery Session Confirmation (PADS)** 当接收到PADR时，Access Concentrator会生成一个唯一的PPP会话ID (Session identification)，并在PADR报文中返回给PPPoE client。该报文被发送到客户端的单播地址。
    

PPPoE会话终止:

- **PPPoE Active Discovery Terminate (PADT)** 可以在PPPoE会话建立后的任何时间发送，表示PPPoE会话的结束。它可以由服务器或客户端发送。

## 会话阶段

当发现阶段完成后，两个对等体都知道_PPPoE Session id和其他对等体的以太网(MAC)地址，它们共同定义了PPPoE会话。PPP帧封装在PPPoE会话帧中，以太网帧类型为 **0x8864** 。
当服务器发送确认信息，客户端接收到确认信息后，PPP会话开始，该会话包括以下几个阶段:

1. **LCP谈判** 阶段
2. **认证(CHAP/PAP)** 阶段
3. IPCP协商阶段——为客户端分配IP地址。

如果有进程失败，则重新启动LCP协商建立阶段。

  
PPPoE服务器向客户端发送_Echo-Request_报文来确定会话的状态，否则，如果客户端没有发送Terminate-Request报文而终止会话，服务器将无法确定会话是否已经结束。

# MTU

通常情况下，可以传输的无分片的最大以太网帧是1500字节。PPPoE增加了6个字节的开销，PPP字段增加了2个字节，为IP数据报留下了1492个字节。因此，PPPoE最大MRU值和MTU值不能大于1492。

TCP栈试图避免碎片，因此它们使用MSS(最大段大小)。缺省情况下，选择MSS作为出接口的MTU减去TCP和IP报头的通常大小(40字节)，即以太网接口的MTU为1460字节。不幸的是，可能存在MTU较低的中间链路，这会导致分片。在这种情况下，TCP栈执行路径MTU发现。如果路由器不能在没有分片的情况下转发数据报，则应该丢弃数据包并发送_icmp - fragment - required_到原始主机。当主机收到这样的ICMP报文时，它会尝试降低MTU。这在理想情况下应该可以工作，但是在现实世界中，许多路由器不生成分段所需的数据报，而且许多防火墙会丢弃所有ICMP数据报。

这个问题的解决办法是 [调整MSS](https://help.mikrotik.com/docs/display/ROS/Mangle#Mangle-ChangeMSS) ，如果它太大。

# PPPoE客户端

**Properties**

| 属性                                                                                 | 说明                                                                                                                          |
| ------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------- |
| **ac-name** (_string_;Default:**""**)                                                | 访问集中器名称，该值可以为空，客户端将连接到广播域中的任何访问集中器                                                          |
| **add-default-route** (_yes \| no_;Default:**no**)                                   | Enable/Disable是否自动添加默认路由                                                                                            |
| **allow** (_mschap2 \| mschap1\| chap\| pap_; Default: **mschap2,mschap1,chap,pap**) | 允许的认证方法，默认情况下允许所有方法                                                                                        |
| **default-route-distance** (_byte [0..255]_;Default:**1**)                           | 设置应用于自动创建的默认路由的距离值，如果add-default-route也被选中                                                           |
| **dial-on-demand** (_yes\| no_;Default:**no**)                                       | 仅在产生出站流量时连接AC。如果选择，则在未建立连接的情况下，将添加网关地址为10.112.112.0/24网络的路由。                       |
| **interface** (_string_;Default:)                                                    | 客户端将运行的接口名                                                                                                          |
| **keepalive-timeout** (_integer_;Default:**60**)                                     | 设置以秒为单位的keepalive超时时间。                                                                                           |
| **max-mru** (_integer_; Default: **1460**)                                           | 最大接收单元                                                                                                                  |
| **max-mtu** (_integer_;Default:**1460**)                                             | 最大传输单元                                                                                                                  |
| **mrru** (_integer: 512..)65535 \| disabled_;Default:**disabled**)                   | 该链路可接收的最大数据包大小。如果报文的大小大于隧道的MTU，则会将其分割成多个报文，允许通过隧道发送完整大小的IP或以太网报文。 |
| **name** (_string_;Default:**PPPoE -out[i]**)                                        | PPPoE接口名称，如果不指定，则由RouterOS生成                                                                                   |
| **password** (_string_;Default:)                                                     | 认证密码                                                                                                                      |
| **profile** (_string_;Default:**Default**)                                           | 建立隧道时使用哪一种PPP配置文件。                                                                                             |
| **service-name** (_string_;Default:**""**)                                           | 接入集中器上设置的服务名称，可以不设置，表示连接到任意一个PPPoE服务器                                                         |
| **use-peer-dns** (_yes\| no_; Default: **no**)                                       | 启用/禁用从对端获取DNS设置                                                                                                    |
| **user** (_string_;Default:**""**)                                                   | 用于认证的用户名                                                                                                              |

## 状态

命令 `/interface PPPoE -client monitor` 将显示当前PPPoE的状态。

可用的只读属性:

| 属性                                | 说明                                                  |
| ----------------------------------- | ----------------------------------------------------- |
| **ac-mac** (_MAC address_)          | 客户端连接的AC (access concentrator) MAC地址          |
| **ac-name** (_string_)              | 访问集中器的名称                                      |
| **active-links** (_integer_)        | 绑定的MLPPP连接数，如果不使用MLPPP，则为“1”           |
| **encoding** (_string_)             | 在此连接中使用的加密和编码(如果是非对称的，用'/'分隔) |
| **local-address** (_IP Address_)    | 分配给客户端的IP地址                                  |
| **Remote - Address** (_IP Address_) | 分配给服务器的远端IP地址(即网关地址)                  |
| **mru** (_integer_)                 | 链路的有效mru值                                       |
| **mtu** (_integer_)                 | 链路的有效mtu值                                       |
| **service-name** (_string_)         | 使用的服务名称                                        |
| **status** (_string_)               | 当前链接状态。取值包括:                               | <br>-   dialing,<br>-   verifying password...,<br>-   connected,<br>-   disconnected. |
| **uptime** (_time_)                 | 以天、小时、分、秒为单位显示的连接时间                |

## 扫描仪

“PPPoE Scanner”功能可以扫描二层广播域中所有活跃的PPPoE服务器。运行扫描器的命令如下:

`/interface pppoe-client scan [interface]`

可用的只读属性:

| 属性                     | 说明                   |
| ------------------------ | ---------------------- |
| **service** (_string_)   | 服务器上配置的服务名称 |
| **Mac -address** (_MAC_) | 检测到的服务器Mac地址  |
| **ac-name** (_string_)   | 访问集中器的名称       |

对于Windows，某些连接指令可能会使用指定“电话号码”(例如“MikroTik_AC\mt1”)的形式，以表明“MikroTik_AC”是访问集中器名称，“mt1”是服务名称。

指定MRRU表示在单个链路上启用MP (Multilink PPP)功能。该协议用于将大数据包分成较小的数据包。在Windows下，它可以在网络选项卡，设置按钮，“为单链路连接协商多链路”中启用。在Windows上，MRRU硬编码为1614。此设置有助于克服PathMTU发现失败。对等体两端都应使能MP设置。

# PPPoE Server

PPPoE server配置的接口(隧道)项分为静态用户和动态连接两种。为每一条与给定服务器建立的隧道创建一个接口。如果需要引用为特定用户创建的特定接口名称(在防火墙规则或其他地方)，则可以通过管理方式添加静态接口。动态接口将自动添加到此列表中，只要用户连接并且其用户名与任何现有的静态表项不匹配(或者如果表项已经激活，因为不能有两个单独的隧道接口被相同的名称引用-如果这是一个问题，请设置one-session-per-host)。动态接口在用户连接时出现，一旦用户断开连接就消失，因此不可能在路由器配置(例如防火墙)中引用为该用途创建的隧道，因此如果您需要为该用户创建持久规则，请为他/她创建静态条目。否则，使用动态配置是安全的。

在这两种情况下，都必须正确配置PPP用户，静态表项不能替代PPP配置。

## 访问集中器

`/interface pppoe-server server`

**属性**

| 属性                                                                                             | 说明                                                                                                                                                            |
| ------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **authentication** ( _mschap2\| mschap1\| chap\| pap_; Default: **mschap2, mschap1, chap, pap**) | 认证算法                                                                                                                                                        |
| **default-profile** (_string_;Default:**Default**)                                               |                                                                                                                                                                 |  |
| **interface** (_string_;Default:**""**)                                                          | 客户端所连接的接口                                                                                                                                              |
| **keepalive-timeout** (_time_;Default:**"10"**)                                                  | 定义路由器每秒开始发送keepalive报文的时间间隔(单位为秒)。如果在这段时间内(即2 * keepalive-timeout)没有流量和keepalive响应到达，则宣布未响应的客户端已断开连接。 |
| **max-mru** (_integer_;Default:**1480**)                                                         | 最大接收单元。最优值是tunnel工作所在接口的MTU减小20(因此，对于1500字节的以太网链路，将MTU设置为1480，以避免报文分片)                                            |
| **max-mtu** (_integer_;Default:**1480**)                                                         | 最大传输单元。最优值是tunnel工作所在接口的MTU减小20(因此，对于1500字节的以太网链路，将MTU设置为1480，以避免报文分片)。                                          |
| **max-sessions** (_integer_; Default: **0**)                                                     | AC可服务的最大客户端数。'0' =没有限制。                                                                                                                         |
| **mrru** (_integer: 512..65535 \| disabled_;Default:**disabled**)                                | 链路上可接收的最大数据包大小。如果报文的大小大于隧道的MTU，则会将其分割成多个报文，允许通过隧道发送完整大小的IP或以太网报文。                                   |
| **1 -session per-host** (_yes \| no_;Default:**no**)                                             | 每台主机只允许一个会话(由MAC地址决定)。如果主机试图建立一个新的会话，旧的会话将被关闭。                                                                         |
| **service-name** (_string_;Default:**""**)                                                       | PPPoE服务名称。服务器将接受发送具有与此设置匹配的服务名称的PADI消息的客户端，或者PADI消息中的服务名称字段未设置。                                               |

PPPoE服务器(接入集中器)支持为每个接口配置多个服务器，使用不同的服务名称。接入集中器名称和PPPoE服务名称用于客户端识别要注册的接入集中器。访问集中器名称与命令提示符前显示的路由器的标识相同。标识可以在/system identity子菜单中设置。

不要为将要接收PPPoE请求的接口分配IP地址。

指定MRRU表示在单个链路上启用MP (Multilink PPP)功能。该协议用于将大数据包分成较小的数据包。他们的MRRU被硬编码为1614。此设置有助于克服PathMTU发现失败。对等体两端都应使能MP设置。

默认的_keepalive-timeout_值10秒在大多数情况下是可以的。如果将其设置为0，则在客户端显式注销或重启路由器之前，路由器不会断开连接。要解决这个问题，可以使用one-session-per-host属性。

#快速示例

![](https://help.mikrotik.com/docs/download/attachments/2031625/Untitled%20Diagram.jpg?version=1&modificationDate=1571812332084&api=v2)

## PPPoE Client

若要将microtik RouterOS配置为PPPoE客户端，只需按以下参数配置PPPoE客户端，配置示例如下:

```shell
[admin@MikroTik] > interface pppoe-client add interface=ether2 password=StrongPass service-name=pppoeservice name=PPPoE-Out disabled=no user=MT-User
[admin@MikroTik] > interface pppoe-client print
Flags: X - disabled, I - invalid, R - running
 0  R name="PPPoE-Out" max-mtu=auto max-mru=auto mrru=disabled interface=ether2 user="MT-User"
      password="StrongPass" profile=default keepalive-timeout=10 service-name="pppoeservice" ac-name=""
      add-default-route=no dial-on-demand=no use-peer-dns=no allow=pap,chap,mschap1,mschap2
```

## PPPoE Server

将microtik RouterOS配置为接入集中器(PPPoE Server)。

- 为10.0.0.2 ~ 10.0.0.5的客户端添加IP地址池;
- 添加PPP配置文件;
- 添加PPP秘钥(用户名/密码);
- 添加PPPoE服务器本身;

```shell
[admin@MikroTik] > /ip pool
add name=pppoe-pool ranges=10.0.0.2-10.0.0.5
[admin@MikroTik] > /ppp profile
add local-address=10.0.0.1 name=for-pppoe remote-address=pppoe-pool
[admin@MikroTik] > /ppp secret
add name=MT-User password=StrongPass profile=for-pppoe service=pppoe
[admin@MikroTik] > /interface pppoe-server server
add default-profile=for-pppoe disabled=no interface=ether3 service-name=pppoeservice
```