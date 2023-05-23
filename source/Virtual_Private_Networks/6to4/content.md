# 概述

**Sub-menu:** `/interface 6to4`

6to4是一种特殊的机制，允许IPv6数据包在IPv4网络上传输，而不需要显式配置隧道接口。它对于通过不支持IPv6的网络连接两个或多个IPv6网络特别有用。6to4机制有两种不同的方式。如果未配置remote-address，则如果前16位是_2002_，路由器将封装并直接通过IPv4发送IPv6报文，并使用后32位作为目的地址(IPv4地址转换为十六进制)。否则，IPv6报文将直接发送到IPv4地址remote-address。

# 属性说明

| 属性                                                                    | 说明                                                                                                                                                                                                                                                                                    |
| ----------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **clamp-tcp-mss** (_yes \| no_; Default: **yes**)                       | 控制是否修改接收到的TCP SYN报文的MSS大小。启用后，如果当前MSS大小超过tunnel接口MTU(考虑TCP/IP开销)，路由器将改变接收到的TCP SYN报文的MSS大小。接收到的封装报文仍然包含原始的MSS，只有在解封装之后，MSS才会改变。                                                                        |
| **comment** (_string_;Default:)                                         | 接口的简短描述                                                                                                                                                                                                                                                                          |
| **disabled** (_yes\| no_;Default:**no**)                                | 是否禁用                                                                                                                                                                                                                                                                                |
| **not -fragment** (_inherit\| no_;Default:**no**)                       | 是否在相关报文中包含DF位                                                                                                                                                                                                                                                                |
| **dscp** (_integer: 0-63_;Default:**inherited**)                        | 报文的DSCP值。“Inherited”选项表示从将要封装的报文继承DSCP值                                                                                                                                                                                                                             |
| **ipsec-secret** (_string_;Default:)                                    | 指定secret时，路由器使用预共享密钥和策略为remote-address添加动态IPsec peer (phase2默认使用sha1/aes128cbc)                                                                                                                                                                               |
| **keepalive** (_integer[/time]，integer 0..4294967295_;Default:**0,0**) | 隧道保持存活参数设置隧道对端宕机时，隧道运行标志保持的时间间隔。如果配置时间，重试失败，则取消接口运行标志。参数以以下格式写入:' KeepaliveInterval,KeepaliveRetries '其中' KeepaliveInterval '是时间间隔，' KeepaliveRetries '是重试尝试的次数。缺省情况下，keepalive为10秒，重试10次。 |
| **local-address** (_IP_;Default:)                                       | 路由器本地报文的源地址                                                                                                                                                                                                                                                                  |
| **mtu** (_integer_;Default:**auto**)                                    | Layer3最大传输单元。                                                                                                                                                                                                                                                                    |
| **name** (_string_;Default:)                                            | 接口名称                                                                                                                                                                                                                                                                                |
| **remote-address** (_IP_;Default:)                                      | 6to4隧道对端IP地址。如果不指定，将派生2002::/16网关地址中的IPv4地址。                                                                                                                                                                                                                   |

# 配置举例

## 简单的6to4隧道封装(目前不工作)

! [] (https://help.mikrotik.com/docs/download/attachments/135004174/6to4-tunnel.jpg?version=1&modificationDate=1656683221465&api=v2)

通过利用2002::/16分配的地址空间，可以简单地在IPv4网络上路由IPv6数据包。所有6to4节点都必须具有可访问的IPv4地址——如果您在Internet上运行此设置，则所有IPv4地址都必须是公共地址。

**R1配置:**

创建6to4 tunnel接口。

`/interface 6to4
add name=6to4-tunnel1`

指定一个IPv6地址，前16位为'2002'，后32位为十六进制格式的IPv4。例如，路由器的IP地址为10.0.1.1，则IPv6地址为2002:A00:101::

`/ipv6 address
add address=2002:a00:101::/128 advertise=no interface=6to4-tunnel1`

在6to4-tunnel接口上添加专门分配的6to4隧道范围的路由。

`/ipv6 route
add dst-address=2002::/16 gateway=6to4-tunnel1`

**R2配置:**

创建6to4 tunnel接口。

`/interface 6to4
add name=6to4-tunnel1`

分配一个与R1相同原理生成的IPv6地址。在本例中，10.0.2.1转换为2002:A00:201::

`/ipv6 address
add address=2002:a00:201::/128 advertise=no interface=6to4-tunnel1`

这边也必须走6to4路由。

`/ipv6 route
add dst-address=2002::/16 gateway=6to4-tunnel1`

**测试:**

配置完两个设备后，如果正确生成IPv6地址，应该可以ping通IPv6地址。

从R1:

`/ping 2002:a00:201::`

## Hurricane Electric隧道代理例子

下面以RouterOS设备为例，介绍如何通过IPv4网络通过6to4隧道实现IPv6连通性。

为了能够创建隧道，必须有一个公共IPv4地址，并启用隧道代理IPv4服务器的ping功能。

当使用 [Hurricane Electric隧道代理](https://tunnelbroker.net) 创建隧道时，将获得路由/64 IPv6前缀和设置隧道所需的其他信息。

_![](https://help.mikrotik.com/docs/download/attachments/135004174/TunnelBrokerIPv6.png?version=1&modificationDate=1656679624575&api=v2)_

这个例子假设公共IPv4地址是194.105.56.170

Hurricane Electric在“配置示例”一节中提供了用于RouterOS的命令:

```shell
/interface 6to4
add comment="Hurricane Electric IPv6 Tunnel Broker" disabled=no local-address=194.105.56.170 mtu=1280 name=sit1 remote-address=216.66.80.90
/ipv6 route
add comment="" disabled=no distance=1 dst-address=2000::/3 gateway=2001:470:27:37e::1 scope=30 target-scope=10
/ipv6 address
add address=2001:470:27:37e::2/64 advertise=no disabled=no eui-64=no interface=sit1
```

这些命令将设置隧道本身-路由器连接到IPv6主机，但最终用户设备(计算机，平板电脑，手机)还没有IPv6连接。

为了能够分配IPv6地址给客户端，必须添加路由IPv6前缀到内部接口(默认情况下桥本地)。

`/ipv6 address add address=2001:470:28:37e:: interface=bridge-local advertise=yes`

启用通过网络发现方式发布DNS服务器

`/ipv6 nd set [ find default=yes ] advertise-dns=yes`

最后添加IPv6 DNS服务器(这些是Google公共DNS服务器，也可以使用Hurricane Electric提供的服务器- 2001:470:20::2)。

`/ip dns set allow-remote-requests=yes servers=2001:4860:4860::8888,2001:4860:4860::8844`

然后在设备上启用IPv6，应该有IPv6连接。[http://ipv6-test.com](http://ipv6-test.com) 可以用来测试IPv6的连通性。