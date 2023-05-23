# 概述

**Sub-menu:** `/interface ipip   **Standards:** [RFC2003](https://tools.ietf.org/html/rfc2003)`

在microtik RouterOS上实现的IPIP隧道符合RFC 2003标准。IPIP隧道是一种简单的协议，它将IP报文封装在IP中，在两台路由器之间形成一条隧道。IPIP隧道接口显示为接口列表下的接口。包括Cisco和Linux在内的许多路由器都支持该协议。该协议使多种网络方案成为可能。

IP隧道协议为网络设置增加了以下可能性:

- 通过Internet对内部网进行隧道

- 使用它代替源路由

# 属性

| 属性                                                                       | 说明                                                                                                                                                                                                                                                                          |
| -------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **clamp-tcp-mss** (_yes \| no_; Default: **yes**)                          | 控制是否修改接收到的TCP SYN报文的MSS大小。启用后，如果当前MSS大小超过tunnel接口MTU(考虑TCP/IP开销)，路由器将改变接收到的TCP SYN报文的MSS大小。接收到的封装报文仍然包含原始的MSS，只有在解封装之后，MSS才会改变。                                                              |
| **not -fragment** (_inherit \| no_;Default:**no**)                         |                                                                                                                                                                                                                                                                               |
| **dscp** (_inherit \| integer [0-63]_;Default:)                            | 设置IPIP报头中的dscp值为固定值或继承隧道流量中的dscp值                                                                                                                                                                                                                        |
| **ipsec-secret** (_string_;Default:)                                       | 当指定secret时，路由器使用默认值的预共享密钥和策略为remote-address添加动态ipsec peer (phase2默认使用sha1/aes128cbc)。                                                                                                                                                         |
| **local-address** (_IP_; Default: )                                        | 路由器上被IPIP隧道使用的IP地址                                                                                                                                                                                                                                                |
| **mtu** (_integer_;Default:**1500**)                                       | Layer3最大传输单元                                                                                                                                                                                                                                                            |
| **keepalive** (_integer[/time]，integer 0..4294967295_;Default:**10s,10**) | 隧道保持存活参数设置即使隧道对端发生故障，隧道运行标志保持的时间间隔。如果配置时间，重试失败，则取消接口运行标志。参数的格式如下:' KeepaliveInterval,KeepaliveRetries '，其中KeepaliveInterval是时间间隔，KeepaliveRetries是重试次数。缺省情况下，keepalive为10秒，重试10次。 |
| **name** (_string_;Default:)                                               | 接口名称                                                                                                                                                                                                                                                                      |
| **remote-address** (_IP_;Default:)                                         | IPIP隧道对端IP地址                                                                                                                                                                                                                                                            |

此接口没有身份验证或“状态”。可以使用接口菜单中的监视器功能监视接口的带宽使用情况。

# 例子

假设想在路由器R1和R2之间添加一条IPIP隧道:

![](https://help.mikrotik.com/docs/download/attachments/47579173/Ipip-sample.jpg?version=1&modificationDate=1612793622487&api=v2)

首先需要配置IPIP接口，然后为其添加IP地址。

路由器 **R1** 的配置如下:

```shell
[admin@MikroTik] interface ipip> add
local-address: 10.0.0.1
remote-address: 22.63.11.6
[admin@MikroTik] interface ipip> print
Flags: X - disabled, R - running
# NAME MTU LOCAL-ADDRESS REMOTE-ADDRESS
0 X ipip1 1480 10.0.0.1 22.63.11.6
 
[admin@MikroTik] interface ipip> en 0
[admin@MikroTik] interface ipip> /ip address add address=1.1.1.1/24 interface=ipip1
```

**R2** 的配置:

```shell
[admin@MikroTik] interface ipip> add local-address=22.63.11.6 remote-address=10.
0.0.1
[admin@MikroTik] interface ipip> print
Flags: X - disabled, R - running
# NAME MTU LOCAL-ADDRESS REMOTE-ADDRESS
0 X ipip1 1480 22.63.11.6 10.0.0.1
 
[admin@MikroTik] interface ipip> enable 0
[admin@MikroTik] interface ipip> /ip address add address=1.1.1.2/24 interface=ipip1
```

现在两个路由器可以相互ping通了: 

```shell
[admin@MikroTik] interface ipip> /ping 1.1.1.2
1.1.1.2 64 byte ping: ttl=64 time=24 ms
1.1.1.2 64 byte ping: ttl=64 time=19 ms
1.1.1.2 64 byte ping: ttl=64 time=20 ms
3 packets transmitted, 3 packets received, 0% packet loss
round-trip min/avg/max = 19/21.0/24 ms
[admin@MikroTik] interface ipip>
```