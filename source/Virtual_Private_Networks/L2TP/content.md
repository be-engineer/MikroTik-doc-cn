# 概述

L2TP (Layer Two Tunneling Protocol)是对PPP模型的扩展，它允许L2和PPP端点驻留在由分组交换网络连接的不同设备上。L2TP包括PPP认证和对每个L2TP连接的计费。每个连接的完整身份验证和记帐可以通过RADIUS客户端或本地完成。L2TP流量的控制报文和数据报文都使用UDP协议。UDP端口1701仅用于链路建立，后续流量使用任何可用的UDP端口(可能是也可能不是1701)。这意味着L2TP可以与大多数防火墙和路由器(甚至NAT)一起使用，允许UDP流量通过防火墙或路由器路由。L2TP标准在[RFC 2661](https://tools.ietf.org/html/rfc2661)中定义。

# 介绍

使用L2TP就像使用任何其他带或不带加密的隧道协议一样有用。L2TP标准指出，最安全的数据加密方式是使用L2TP over IPsec(注意，这是Microsoft L2TP客户端的默认模式)，因为特定隧道的所有L2TP控制和数据包对IPsec系统来说都是同质的UDP/IP数据包。

支持多链路PPP (MP)是为了提供MRRU(传输全尺寸1500或更大数据包的能力)和PPP链路桥接(使用桥接控制协议(BCP)，允许在PPP链路上发送原始以太网帧)。这样就可以在没有EoIP的情况下设置桥接。由于PPP链路没有MAC地址，网桥应该有一个管理设置的MAC地址，或者其中有一个类似以太网的接口。

L2TP对隧道流量不提供加密机制。IPsec可以用于附加的安全层。

# L2TP Client

## 属性

| 属性                                                              | 说明                                                                                                                                         |
| ----------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **add-default-route** (_yes                                       | no_; Default: **no**)                                                                                                                        | 是否添加L2TP对端地址作为缺省路由。 |
| **allow** (_mschap2                                               | mschap1                                                                                                                                      | chap                               | pap_;Default:**mschap2, mschap1, chap, pap**) | 允许的认证方式。 |
| **连接到** (_IP_;Default:)                                        | L2TP服务器对端地址(如果在VRF表中，则需要指定VRF)<br>/interface l2tp-client Add connect-to=192.168.88.1@vrf1;name=l2tp-out1;user=l2tp-client) |
| **comment** (_string_;Default:)                                   | 隧道的简短描述。                                                                                                                             |
| **default-route-distance** (_byte_;  Default: )                   | 自v6.2起，设置应用于自动创建的默认路由的距离值，如果add-default-route也被选中                                                                |
| **dial-on-demand** (_yes \| no_;Default:**no**)                   | 仅在产生出站流量时连接。如果选择，则在未建立连接的情况下，将添加网关地址为10.112.112.0/24网络的路由。                                        |
| **disabled** (_yes \| no_;Default:**yes**)                        | 开启/关闭隧道。                                                                                                                              |
| **keepalive-timeout** (_integer [1..4294967295]_;Default:**60s**) | 从v6.0rc13开始，隧道保持连接超时以秒为单位。                                                                                                 |
| **max-mru** (_integer_; Default: **1460**)                        | 最大接收单元。L2TP接口在不发生报文分片的情况下能够接收的最大报文大小。                                                                       |
| **max-mtu** (_integer_;Default:**1460**)                          | 最大传输单元。L2TP接口在不发生报文分片的情况下能够发送的最大报文大小。                                                                       |
| **mrru** (_disabled \| integer_;Default:**disabled**)             | 链路上可以接收的最大数据包大小。如果报文的大小大于隧道的MTU，则会将其分割成多个报文，允许通过隧道发送完整大小的IP或以太网报文。              |
| **name** (_string_;Default:)                                      | 接口的描述性名称。                                                                                                                           |
| **password** (_string_;Default:**""**)                            | 鉴权密码。                                                                                                                                   |
| **profile** (_name_;Default:**Default -encryption**)              | 建立隧道时使用哪一种PPP配置文件。                                                                                                            |
| **user** (_string_;Default:)                                      | 用于鉴权的用户名。                                                                                                                           |
| **use-ipsec** (_yes \| no_;Default:**no**)                        | 启用后，会添加动态IPSec对等体配置和策略，将L2TP连接封装到IPSec隧道中。                                                                       |
| **ipsec-secret** (_string_;Default:)                              | 启用use-ipsec时使用的预共享密钥。                                                                                                            |

# L2TP服务器

为每一条与给定服务器建立的隧道创建一个接口。L2TP服务器的配置中有两种类型的接口

如果需要引用为特定用户创建的特定接口名称(在防火墙规则或其他地方)，则在管理上添加静态接口;
-动态接口将自动添加到此列表中，每当用户连接，其用户名不匹配任何现有的静态表项(或者如果表项已经激活，因为不能有两个单独的隧道接口引用相同的名称);

动态接口在用户连接时出现，一旦用户断开连接就消失，因此不可能在路由器配置(例如防火墙)中引用为该用途创建的隧道，因此如果您需要为该用户创建持久规则，请为他/她创建静态条目。否则，使用动态配置是安全的。

这两种情况下都需要正确配置PPP用户，静态表项不能替代PPP配置。

## 属性

| 属性                                                                                 | 说明                                                                                                                                                                                                   |
| ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **authentication** (_pap\| chap \| mschap1\| mschap2_; Default: **mschap1,mschap2**) | 服务器将接受的身份验证方法。                                                                                                                                                                           |
| **default-profile** (_name;Default:** Default -encryption**)                         | 默认配置文件使用                                                                                                                                                                                       |
| **enabled** (_yes                                                                    | no_;Default:**no**)                                                                                                                                                                                    | 设置L2TP服务器是否开启。 |
| **max-mru** (_integer_;Default:**1450**)                                             | 最大接收单元。L2TP接口在不发生报文分片的情况下能够接收的最大报文大小。                                                                                                                                 |
| **keepalive-timeout** (_integer_;Default:**30**)                                     | 如果在keepalive超时时间内服务器未收到任何报文，则每秒发送keepalive报文，共5次。如果服务器仍然没有收到客户端的任何响应，那么客户端将在5秒后断开连接。日志将显示5次“LCP错过回声回复”消息，然后断开连接。 |
| **max-mtu** (_integer_;Default:**1450**)                                             | 最大传输单元。L2TP接口在不发生报文分片的情况下能够发送的最大报文大小。                                                                                                                                 |
| **use-ipsec** (_no \| yes\| require_; Default: **no**)                               | 启用此选项后，将添加动态IPSec对等体配置，以适应大多数L2TP道路战士的设置。当选择“要求”时，服务器将只接受那些封装在IPSec隧道中的L2TP连接尝试。                                                           |
| **ipsec-secret** (_string_;Default:)                                                 | 启用use-ipsec时使用的预共享密钥                                                                                                                                                                        |
| **mrru** (_disabled \| integer_;Default:**disabled**)                                | 链路上可以接收的最大数据包大小。如果报文的大小大于隧道的MTU，则会将其分割成多个报文，允许通过隧道发送完整大小的IP或以太网报文。                                                                        |

# 快速例子

![](https://help.mikrotik.com/docs/download/attachments/2031631/Simple-l2tp-setup.jpg?version=2&modificationDate=1571748876898&api=v2)

## L2TP服务器

在服务器端，我们将启用L2TP-server并为特定用户创建PPP配置文件:

```shell
[admin@MikroTik] > /interface l2tp-server server set enabled=yes
[admin@MikroTik] > /ppp secret add local-address=10.0.0.2 name=MT-User password=StrongPass profile=default-encryption remote-address=10.0.0.1 service=l2tp
```

## L2TP Client

在RouterOS中建立L2TP客户端非常简单。在下面的示例中，我们已经有了一个预配置的3单元设置。我们将更详细地了解如何使用用户名“MT-User”，密码“StrongPass”和服务器192.168.51.3设置L2TP客户端:

```shell
[admin@MikroTik] > /interface l2tp-client \
add connect-to=192.168.51.3 disabled=no name=MT-User password=StrongPass user=MT-User
[admin@MikroTik] > /interface l2tp-client print
Flags: X - disabled, R - running
0 R name="MT-User" max-mtu=1450 max-mru=1450 mrru=disabled connect-to=192.168.51.3 user="MT-User"
password="StrongPass" profile=default-encryption keepalive-timeout=60 use-ipsec=no ipsec-secret=""
allow-fast-path=no add-default-route=no dial-on-demand=no allow=pap,chap,mschap1,mschap2
```