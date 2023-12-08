# 介绍

**Sub-menu:** `/interface gre`  
**Standards:** [RFC1701](https://tools.ietf.org/html/rfc1701)

GRE (Generic Routing Encapsulation)是一种隧道协议，最初由Cisco公司开发。它可以封装各种各样的协议，创建虚拟的点对点链路。

GRE和IPIP、EoIP一样，最初都是作为无状态隧道发展起来的。这意味着，如果隧道的远端出现故障，所有通过隧道路由的流量都将陷入黑洞。为了解决这个问题，RouterOS为GRE隧道增加了keepalive功能。

GRE隧道增加了24字节的开销(4字节的GRE头+ 20字节的IP头)。GRE隧道只能转发IP和IPv6报文(以太网类型为800和86dd)。当GRE隧道作为路由网关时，不建议使用“检查网关”选项“arp”。

# 属性

| 属性                                                                       | 说明                                                                                                                                                                                                                                                                          |
| -------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **allow-fast-path** (_yes \| no_; Default: **yes**)                        | 是否允许FastPath处理。使用IPsec隧道时必须关闭。                                                                                                                                                                                                                               |
| **clamp-tcp-mss**(_yes \| no_;Default:**yes**)                             | 控制是否更改接收到的TCP SYN报文的MSS大小。启用后，如果当前MSS大小超过tunnel接口MTU(考虑TCP/IP开销)，路由器将改变接收到的TCP SYN报文的MSS大小。接收到的封装报文仍然包含原始的MSS，只有在解封装之后，MSS才会改变。                                                              |
| **comment** (_string_;Default:)                                            | 隧道的简短描述。                                                                                                                                                                                                                                                              |
| **disabled** (_yes \| no_;Default:**no**)                                  | 开启/关闭隧道。                                                                                                                                                                                                                                                               |
| **dont-fragment** (_inherit \| no_; Default: **no**)                       | 相关报文中是否包含DF位:<br>_no_ - fragment如果需要，_inherit_ -使用原始数据包的不分段标志。<br>(不带don Fragment: inherit - packet可能被分片)。                                                                                                                               |
| **dscp** (_inherit \| integer [0-63]_; Default: )                          | 设置Gre报头中的dscp值为固定值或继承隧道流量中的dscp值                                                                                                                                                                                                                         |
| **ipsec-secret** (_string_;Default:)                                       | 当指定secret时，路由器使用预共享密钥和策略为remote-address添加动态IPsec peer (phase2默认使用sha1/aes128cbc)。                                                                                                                                                                 |
| **keepalive** (_integer[/time]，integer 0..4294967295_;Default:**10s,10**) | 隧道保持存活参数设置即使隧道对端发生故障，隧道运行标志保持的时间间隔。如果配置时间，重试失败，则取消接口运行标志。参数的格式如下:' KeepaliveInterval,KeepaliveRetries '，其中KeepaliveInterval是时间间隔，KeepaliveRetries是重试次数。缺省情况下，keepalive为10秒，重试10次。 |
| **l2mtu** (_integer [0..65536]_;Default:**65535**)                         | Layer2最大传输单元。                                                                                                                                                                                                                                                          |
| **local-address** (_IP_;Default:**0.0.0.0**)                               | 隧道本端使用的IP地址。如果设置为0.0.0.0，则使用出接口的IP地址。                                                                                                                                                                                                               |
| **mtu** (_integer [0..65536]_;Default:**1476**)                            | Layer3最大传输单元。                                                                                                                                                                                                                                                          |
| **name** (_string_;Default:)                                               | 隧道名称。                                                                                                                                                                                                                                                                    |
| **remote-address** (_IP_;Default:)                                         | 隧道远端IP地址。                                                                                                                                                                                                                                                              |

# 设置示例

这个示例的目标是通过internet在两个远程站点之间获得第3层连接

![](https://help.mikrotik.com/docs/download/attachments/24805531/Site-to-site-gre-example.jpg?version=1&modificationDate=1612794055516&api=v2)

有两个站点，**Site1** ，本地网络范围为10.1.101.0/24，**Site2** ，本地网络范围为10.1.202.0/24。

第一步是创建GRE隧道。站点1的路由器:

`/interface gre add name=myGre remote-address=192.168.90.1 local-address=192.168.80.1`

site2的路由器:

`/interface gre add name=myGre remote-address=192.168.80.1 local-address=192.168.90.1`

正如您所看到的，隧道配置非常简单。

在本例中，由于没有配置keepalive，所以即使远端隧道不可达，tunnel接口也会有一个 **running** 标志

现在只需要设置隧道地址和正确的路由。站点1的路由器:

```shell
/ip address add address=172.16.1.1/30 interface=myGre
/ip route add dst-address=10.1.202.0/24 gateway=172.16.1.2
```

site2的路由器:

```shell
/ip address add address=172.16.1.2/30 interface=myGre
/ip route add dst-address=10.1.101.0/24 gateway=172.16.1.1
```

此时，两个站点都通过GRE隧道实现了三层连接。