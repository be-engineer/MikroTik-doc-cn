# 介绍

**Sub-menu:** `/interface eoip`

EoIP (Ethernet over IP)隧道是一种基于 [GRE RFC 1701](https://tools.ietf.org/html/rfc1701) 的microtik RouterOS协议，它在IP连接的基础上在两台路由器之间创建以太网隧道。EoIP隧道可以在IPIP隧道、PPTP隧道或任何其他能够传输IP的连接上运行。
当路由器的桥接功能开启时，所有以太网流量(所有以太网协议)将被桥接，就像两台路由器之间有物理以太网接口和电缆一样(桥接功能开启)。该协议使多种网络方案成为可能。

带有EoIP接口的网络设置:

- 通过互联网桥接局域网的可能性
- 通过加密隧道桥接局域网的可能性
- 通过802.11b“特设”无线网络桥接局域网的可能性

EoIP协议将以太网帧封装在GRE (IP协议号47)报文中(就像PPTP一样)，并将其发送到EoIP隧道的远端。

# 属性说明

| 属性                                                                           | 说明                                                                                                                                                                                                                                                                                                 |
| ------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **allow-fast-path** (_yes \| no_; Default: **yes**)                            | 是否允许FastPath处理。使用IPsec隧道时必须关闭。                                                                                                                                                                                                                                                      |
| **arp (**_disabled \| enabled\| proxy-arp\| reply-only_; Default: **enabled)** | 地址解析协议模式。<br>- disabled表示接口不使用ARP<br>- enabled接口使用ARP<br>- proxy- ARP指定接口使用ARP代理特性<br>- reply-only表示接口只响应在/ IP arp表中以静态表项形式输入的匹配的IP /MAC地址组合发起的请求。“/ip arp”表中不会自动存储动态表项。因此，要使通信成功，必须已经存在有效的静态条目。 |
| **arp-timeout** (_integer[/time]_; Default: **auto**)                          | ARP表项超时的时间间隔。                                                                                                                                                                                                                                                                              |
| **clamp-tcp-mss** (_yes\| no_;Default:**yes**)                                 | 控制是否更改接收到的TCP SYN报文的MSS大小。启用后，如果当前MSS大小超过tunnel接口MTU(考虑TCP/IP开销)，路由器将改变接收到的TCP SYN报文的MSS大小。接收到的封装报文仍然包含原始的MSS，只有在解封装之后，MSS才会改变。                                                                                     |
| **comment** (_string_;Default:)                                                | 接口的简短描述。                                                                                                                                                                                                                                                                                     |
| **disabled** (_yes\| no_;Default:**no**)                                       | 是否禁用某项。                                                                                                                                                                                                                                                                                       |
| **not-fragment** (_inherit\| no_;Default:**no**)                               | 是否在相关报文中包含DF位。                                                                                                                                                                                                                                                                           |
| **dscp** (_integer: 0-63_;Default:**inherited**)                               | 报文的DSCP值。“Inherited”选项表示从将要封装的数据包继承dscp值。                                                                                                                                                                                                                                      |
| **ipsec-secret** (_string_;Default:)                                           | 当指定secret时，路由器使用预共享密钥和策略为remote-address添加动态IPsec peer (phase2默认使用sha1/aes128cbc)。                                                                                                                                                                                        |
| **keepalive** (_integer[/time],integer 0..4294967295_; Default: **10s,10**)    | Tunnel keepalive参数设置隧道对端发生故障时，隧道运行标志保持的时间间隔。如果配置时间，重试失败，则取消接口运行标志。参数以以下格式写入: KeepaliveInterval,KeepaliveRetries 其中KeepaliveInterval是时间间隔，KeepaliveRetries是重试尝试的次数。缺省情况下，keepalive为10秒，重试10次。                |
| **l2mtu** (_integer;read-only_)                                                | Layer2最大传输单元。不能配置为EoIP。[RouterOS中的MTU](https://help.mikrotik.com/docs/display/ROS/MTU+in+RouterOS)                                                                                                                                                                                    |
| **local-address** (_IP_;Default:)                                              | 隧道报文的源地址，路由器上的local。                                                                                                                                                                                                                                                                  |
| **loop-protect**                                                               |                                                                                                                                                                                                                                                                                                      |
| **loop-protect-disable-time**                                                  |                                                                                                                                                                                                                                                                                                      |
| **loop-protect-send-interval**                                                 |                                                                                                                                                                                                                                                                                                      |
| **mac-address** (_MAC_; Default: )                                             | 接口的媒体访问控制号。地址编号机构IANA允许使用**00:00:5E:80:00:00 - 00:00:5E:FF:FF:FF** free                                                                                                                                                                                                         | 范围内的MAC地址 |
| **mtu** (_integer_;Default:**auto**)                                           | Layer3最大传输单元                                                                                                                                                                                                                                                                                   |
| **name** (_string_;Default:)                                                   | 接口名称                                                                                                                                                                                                                                                                                             |
| **remote-address** (_IP_;Default:)                                             | EoIP隧道对端IP地址                                                                                                                                                                                                                                                                                   |
| **tunnel-id** (_integer: 65536_;Default:)                                      | 唯一的隧道标识符，必须与隧道的另一端匹配                                                                                                                                                                                                                                                             |

# 配置举例

参数tunnel-id是隧道的标识方法。对于每个EoIP隧道，必须是唯一的。

EoIP隧道至少增加42字节的开销(8字节GRE + 14字节以太网+ 20字节IP)。MTU应该设置为1500，以消除隧道内的数据包碎片(这允许类似以太网的网络透明桥接，以便有可能在隧道上传输全尺寸的以太网帧)。

在桥接EoIP隧道时，建议为每条隧道配置唯一的MAC地址，以保证桥接算法正常工作。 对于EoIP接口，可以使用的MAC地址范围为 
 **00:00:5E:80:00:00 ~ 00:00:5E:FF:FF:FF**，这是IANA为这种情况预留的。或者可以设置第一个字节的第二位，将自动分配的地址修改为由网络管理员分配的“本地管理地址”，从而使用任何MAC地址，只需要确保它们在连接到一个网桥的主机之间是唯一的。

**例子**

假设我们想要桥接两个网络:“Station”和“AP”。通过使用EoIP设置，可以使站和AP局域网处于同一第二层广播域中。

考虑以下设置:

![](https://help.mikrotik.com/docs/download/attachments/24805521/Eoip-example.jpg?version=1&modificationDate=1612793527009&api=v2)

正如您所知，无线站不能桥接，为了克服这个限制(不涉及WDS)，我们将在无线链路上创建EoIP隧道，并将其与连接到本地网络的接口桥接。

在本例中我们将不讨论无线配置，让我们假设无线链路已经建立。

首先在AP上创建一个EoIP隧道:

`/interface eoip add name="eoip-remote" tunnel-id=0 remote-address=10.0.0.2 disabled=no`

验证接口已创建:

```shell
[admin@AP] > /interface eoip print
Flags: X - disabled; R - running
 0  R name="eoip-remote" mtu=auto actual-mtu=1458 l2mtu=65535 mac-address=FE:A5:6C:3F:26:C5 arp=enabled
      arp-timeout=auto loop-protect=default loop-protect-status=off loop-protect-send-interval=5s
      loop-protect-disable-time=5m local-address=0.0.0.0 remote-address=10.0.0.2 tunnel-id=0
      keepalive=10s,10 dscp=inherit clamp-tcp-mss=yes dont-fragment=no allow-fast-path=yes
```

站路由器:

`/interface eoip add name="eoip-main" tunnel-id=0 remote-address=10.0.0.1 disabled=no`

验证接口已创建:

```shell
[admin@Station] >  /interface eoip print
Flags: X - disabled; R - running
 0  R name="eoip-main" mtu=auto actual-mtu=1458 l2mtu=65535 mac-address=FE:4B:71:05:EA:8B arp=enabled
      arp-timeout=auto loop-protect=default loop-protect-status=off loop-protect-send-interval=5s
      loop-protect-disable-time=5m local-address=0.0.0.0 remote-address=10.0.0.1 tunnel-id=0
      keepalive=10s,10 dscp=inherit clamp-tcp-mss=yes dont-fragment=no allow-fast-path=yes
```

接下来将在AP上用EoIP隧道桥接本地接口。如果已经有了本地桥接接口，只需添加EoIP接口即可:

`/interface bridge port add bridge=bridge1 interface=eoip-remote`

网桥端口列表应列出所有本地局域网接口和EoIP接口:

```shell
[admin@AP] > /interface bridge port print
Flags: I - INACTIVE; H - HW-OFFLOAD
Columns: INTERFACE, BRIDGE, HW, PVID, PRIORITY, PATH-COST, INTERNAL-PATH-COST, HORIZON
#    INTERFACE       BRIDGE   HW   PVID  PRIORITY  PATH-COST  INTERNAL-PATH-COST  HORIZON
0  H ether2          bridge1  yes     1  0x80             10                  10  none  
1  H ether3          bridge1  yes     1  0x80             10                  10  none   
2    eoip-remote     bridge1  yes     1  0x80             10                  10  none
```

在站点路由器上，如果没有本地网桥接口，创建一个新的网桥，并将EoIP和本地LAN接口添加到其中:

```shell

/interface bridge add name=bridge1
/interface bridge port add bridge=bridge1 interface=ether2
/interface bridge port add bridge=bridge1 interface=eoip-main
```

验证桥接端口部分:

```shell
[admin@Station] > /interface bridge port print
Flags: I - INACTIVE; H - HW-OFFLOAD
Columns: INTERFACE, BRIDGE, HW, PVID, PRIORITY, PATH-COST, INTERNAL-PATH-COST, HORIZON
#    INTERFACE     BRIDGE   HW   PVID  PRIORITY  PATH-COST  INTERNAL-PATH-COST  HORIZON
0  H ether2        bridge1  yes     1  0x80             10                  10  none   
2    eoip-main     bridge1  yes     1  0x80             10                  10  none
```

现在两个站点都在同一个二层广播域中。可以在两个站点上设置来自同一网络的IP地址。