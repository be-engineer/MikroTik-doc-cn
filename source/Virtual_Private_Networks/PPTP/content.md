# 概述

PPTP有许多已知的安全问题，我们不建议使用它。然而，该协议被集成到常见的操作系统中，并且易于设置。PPTP在不考虑安全问题的网络中很有用。

PPTP流量使用TCP端口1723,IP协议GRE (Generic Routing Encapsulation, IP协议ID 47)，由IANA (Internet assigned Numbers Authority)分配。PPTP可以与大多数防火墙和路由器一起使用，它允许发送到TCP端口1723和协议47的流量通过防火墙或路由器。PPTP包括PPP认证和对每个PPTP连接的记帐。每个连接的完整身份验证和记帐可以通过RADIUS客户端或本地完成。

# PPTP Client

**属性**

| 属性                                                                                    | 说明                                                                                                                            |
| --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| **add-default-route** (_yes\| no_; Default: **no**)                                     | 是否添加PPTP对端地址作为缺省路由。                                                                                              |
| **allow** (_mschap2 \| mschap1 \| chap \| pap_;Default:**mschap2, mschap1, chap, pap**) | 允许的认证方式。                                                                                                                |
| **connect-to** (_IP_;  Default: )                                                       | PPTP服务器的远程地址                                                                                                            |
| **default-route-distance** (_byte [0..255]_;Default:**1**)                              | 设置应用于自动创建的默认路由的距离值，如果add-default-route也被选中                                                             |
| **dial-on-demand** (_yes \| no_;Default:**no**)                                         | 仅在产生出站流量时连接PPTP服务器。如果选择，则在未建立连接的情况下，将添加网关地址为10.112.112.0/24网络的路由。                 |
| **disabled** (_yes \| no_;Default:**yes**)                                              | 接口是否被禁用。缺省情况下是关闭的                                                                                              |
| **keepalive-timeout** (_integer_; Default: **60**)                                      | 以秒为单位设置keepalive超时。                                                                                                   |
| **max-mru** (_integer_;Default:**1460**)                                                | 最大接收单元。PPTP接口在不出现数据包碎片的情况下能够接收的最大数据包大小。                                                      |
| **max-mtu** (_integer_;Default:**1460**)                                                | 最大传输单元。PPTP接口在不发送数据包碎片的情况下能够发送的最大数据包大小。                                                      |
| **mrru** (_disabled \| integer_;Default:**disabled**)                                   | 链路上可以接收的最大数据包大小。如果报文的大小大于隧道的MTU，则会将其分割成多个报文，允许通过隧道发送完整大小的IP或以太网报文。 |
| **name** (_string_;Default:)                                                            | 接口的描述性名称。                                                                                                              |
| **password** (_string_;Default:**""**)                                                  | 鉴权密码。                                                                                                                      |
| **profile** (_name;Default:**Default -encryption**)                                     |                                                                                                                                 |
| **user** (_string_;Default:)                                                            | 用于鉴权的用户名。                                                                                                              |

# PPTP Server

`/interface pptp-server`

为每一条与给定服务器建立的隧道创建一个接口。在PPTP服务器的配置中有两种类型的接口:

- 如果需要引用为特定用户创建的特定接口名称(在防火墙规则或其他地方)，则在管理上添加静态接口;
- 动态接口将自动添加到此列表中，每当用户连接，其用户名不匹配任何现有的静态表项(或者如果表项已经激活，因为不能有两个单独的隧道接口引用相同的名称);

动态接口在用户连接时出现，一旦用户断开连接就消失，因此不可能在路由器配置(例如防火墙)中引用为该用途创建的隧道，因此如果您需要为该用户创建持久规则，请为他/她创建静态条目。否则，使用动态配置是安全的。

在这两种情况下，都必须正确配置PPP用户，静态表项不能替代PPP配置。

**属性**

| 属性                                                                                 | 说明                                                                                                                                                                         |
| ------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **authentication** (_pap\| chap \| mschap1\| mschap2_; Default: **mschap1,mschap2**) | 服务器将接受的身份验证方法。                                                                                                                                                 |
| **default-profile** (_name_;Default:**Default -encryption**)                         |                                                                                                                                                                              |
| **enabled** (_yes\| no_;Default:**no**)                                              | 定义PPTP服务器是否启用。                                                                                                                                                     |
| **keepalive-timeout** (_time_;Default:**30**)                                        | 如果在保持连接时间内服务器没有收到任何报文，则每秒发送5次保持连接报文。如果服务器没有收到客户端的响应，则在5秒后断开连接。日志将显示5次“LCP错过回声回复”消息，然后断开连接。 |
| **max-mru** (_integer_;Default:**1460**)                                             | 最大接收单元。PPTP接口在不出现数据包碎片的情况下能够接收的最大数据包大小。                                                                                                   |
| **max-mtu** (_integer_;Default:**1460**)                                             | 最大传输单元。PPTP接口在不发送数据包碎片的情况下能够发送的最大数据包大小。                                                                                                   |
| **mrru** (_disabled \| integer_; Default: **disabled**)                              | 链路上可以接收的最大数据包大小。如果报文的大小大于隧道的MTU，则会将其分割成多个报文，允许通过隧道发送完整大小的IP或以太网报文。                                              |

# 例子

![](https://help.mikrotik.com/docs/download/attachments/2031638/pptp-setup.jpg?version=1&modificationDate=1571822551430&api=v2)

## PPTP客户端

下面的例子演示了如何使用用户名“MT-User”，密码“StrongPass”和服务器192.168.62.2建立一个PPTP客户端:

```shell
[admin@MikroTik] > interface pptp-client add connect-to=192.168.62.2 disabled=no name=pptp-out1 password=StrongPass user=MT-User
[admin@MikroTik] > interface pptp-client print
Flags: X - disabled; R - running
 0  R name="pptp-out1" max-mtu=1450 max-mru=1450 mrru=disabled connect-to=192.168.62.2 user="MT-User"
      password="StrongPass" profile=default-encryption keepalive-timeout=60 add-default-route=no
      dial-on-demand=no allow=pap,chap,mschap1,mschap2
```

## PPTP服务器

另一方面，只需启用PPTP服务器并为特定用户创建一个PPP密码:

```shell
[admin@MikroTik] >  interface pptp-server server set enabled=yes
[admin@MikroTik] >  ppp secret add local-address=10.0.0.1 name=MT-User password=StrongPass profile=default-encryption remote-address=10.0.0.5 service=pptp
[admin@MikroTik] >  interface pptp-server print
Flags: D - dynamic; R - running
Columns: NAME, USER, MTU, CLIENT-ADDRESS, UPTIME, ENCODING
#      NAME            USER     MTU  CLIENT-ADDRESS  UPTIM  ENCODING        
0  DR  <pptp-MT-User>  MT-User  1450  192.168.51.3   44m8s  MPPE128 stateless
```