# 概述


本页面列出了各种microtik RouterOS服务使用的协议和端口。它可以帮助您确定为什么MikroTik路由器侦听某些端口，以及如果想要阻止或授予对某些服务的访问权限，需要阻止允许什么。请参阅手册的相关章节了解更多说明。

默认的服务是:

| 属性        | 说明                                                  |
| ----------- | ----------------------------------------------------- |
| **telnet**  | Telnet service                                        |
| **ftp**     | FTP service                                           |
| **www**     | Webfig HTTP service                                   |
| **ssh**     | SSH service                                           |
| **www-ssl** | Webfig HTTPS service                                  |
| **api**     | API service                                           |
| **winbox**  | 负责Winbox工具访问，以及Tik-App智能手机程序和Dude探针 |
| **api-ssl** | API over SSL service                                  |

# 属性


注意，不能添加新服务，只允许修改现有服务。

**Sub-menu:** `/ip service`

| 属性                                                    | 描述                                                                  |
| ------------------------------------------------------- | --------------------------------------------------------------------- |
| **address** (_IP地址/netmask\| IPv6/0..128_;Default:)   | 可访问服务的IP/IPv6前缀列表                                           |
| **certificate** (_name_;Default:**none**)               | 特定服务使用的证书名称。仅适用于依赖于证书(_www-ssl, api-ssl_) 的服务 |
| **name** (_name_;Default:**none**)                      | 服务名称                                                              |
| **port** (_integer_: 1..65535_;Default:)                | 端口特定服务监听                                                      |
| **_tls-version_** (_any_ \| _only-1.2_;Default:**any**) | 指定特定服务允许的TLS版本                                             |
| **vrf** (_name_;Default:**main**)                       | 指定特定服务使用哪个VRF实例                                           |

## 例子

例如，只允许来自特定IP/IPv6地址范围的API

```shell
[admin@dzeltenais_burkaans] /ip service> set api address=10.5.101.0/24,2001:db8:fade::/64
[admin@dzeltenais_burkaans] /ip service> print
Flags: X - disabled, I - invalid
 #   NAME     PORT  ADDRESS                                       CERTIFICATE 
 0   telnet   23  
 1   ftp      21  
 2   www      80  
 3   ssh      22  
 4 X www-ssl  443                                                 none        
 5   api      8728  10.5.101.0/24                               
                    2001:db8:fade::/64                          
 6   winbox   8291
```

# 服务端口


启用nat的路由器后面的主机没有真正的端到端连接。因此，一些互联网协议可能无法在NAT场景下工作。

为了克服这些限制，RouterOS包含了许多 [NAT](https://help.mikrotik.com/docs/display/ROS/NAT) 帮助器，可以对各种协议进行NAT遍历。

如果连接跟踪未启用，则防火墙服务端口将显示为非活动状态

**Sub-menu:** `/ip firewall service-port`

| 助手        | 说明                                                                                                                                                                                           |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **FTP**     | FTP助手                                                                                                                                                                                        |
| **H323**    | H323助手                                                                                                                                                                                       |
| **IRC**     | IRC助手                                                                                                                                                                                        |
| **PPTP**    | PPTP隧道助手                                                                                                                                                                                   |
| **UDPLITE** | UDP-Lite助手                                                                                                                                                                                   |
| **DCCP**    | DCCP助手                                                                                                                                                                                       |
| **SCTP**    | SCTP助手                                                                                                                                                                                       |
| **SIP**     | SIP助手。其他选项:<br>**sip-direct-media**允许重定向RTP媒体流直接从调用方到被调用方。默认值为“yes”。<br>- **SIP -timeout**允许调整SIP UDP连接的TTL。默认值:1小时。在某些设置中，你必须减少它。 |
| **TFTP**    | TFTP助手                                                                                                                                                                                       |
| **RSTP**    | RTSP助手                                                                                                                                                                                       |

**udplite** 、**dccp** 和 **sctp** 是内置的连接跟踪服务。由于这些不是单独加载的模块，所以它们不能单独禁用，它们会与连接跟踪一起被禁用。

  

# 协议和端口


RouterOS使用的协议和端口列表如下表所示。

| 原型/端口              | 说明                                                                                                         |
| ---------------------- | ------------------------------------------------------------------------------------------------------------ |
| **20/tcp**             | FTP数据连接                                                                                                  |
| **21/tcp**             | FTP控制连接                                                                                                  |
| **22/tcp**             | SSH远程登录协议                                                                                              |
| **23/tcp**             | Telnet协议                                                                                                   |
| **53/tcp \|53/udp**    | DNS                                                                                                          |
| **67/udp**             | 引导协议或 [DHCP Server](https://help.mikrotik.com/docs/display/ROS/DHCP#DHCP-DHCPServer)                    |
| **68/udp**             | 引导协议或 [DHCP Client](https://help.mikrotik.com/docs/display/ROS/DHCP#DHCP-DHCPClient)                    |
| **80/tcp**             | 万维网HTTP                                                                                                   |
| **123/udp**            | 网络时间协议 [NTP](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=40992869)                     |
| **161/udp**            | 简单网络管理协议 [SNMP](https://help.mikrotik.com/docs/display/ROS/SNMP)                                     |
| **179/tcp**            | 边界网关协议 [BGP](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328220)                       |
| **443/tcp**            | SSL加密HTTP                                                                                                  |
| **500/udp**            | IKE (Internet Key Exchange)协议                                                                              |
| **520/udp \| 521/udp** | [RIP](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328211) 路由协议                           |
| **546/udp**            | [DHCPv6 Client](https://help.mikrotik.com/docs/display/ROS/DHCP-client) 消息                                 |
| **547/udp**            | [DHCPv6服务器](https://help.mikrotik.com/docs/display/ROS/DHCP+Server) 消息                                  |
| **646/tcp**            | [LDP](https://wiki.mikrotik.com/wiki/Manual:MPLS/LDP "Manual:MPLS/LDP") 传输会话                             |
| **646/udp**            | [LDP](https://wiki.mikrotik.com/wiki/Manual:MPLS/LDP "Manual:MPLS/LDP") hello协议                            |
| **1080/tcp**           | [SOCKS](https://help.mikrotik.com/docs/display/ROS/SOCKS) 代理协议                                           |
| **1698/udp 1699/udp**  | RSVP TE隧道                                                                                                  |
| **1701/udp**           | 第二层隧道协议 [L2TP](https://help.mikrotik.com/docs/display/ROS/L2TP)                                       |
| **1723/tcp**           | 点对点隧道协议 [PPTP](https://help.mikrotik.com/docs/display/ROS/PPTP)                                       |
| **1900/udp\|2828/tcp** | 通用即插即用 [uPnP](https://help.mikrotik.com/docs/display/ROS/UPnP)                                         |
| **1966/udp**           | MME发起者消息流量                                                                                            |
| **1966/tcp**           | MME网关协议                                                                                                  |
| **2000/tcp**           | 带宽测试服务器                                                                                               |
| **5246,5247/udp**      | [CAPsMAN](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=1409149)                               |
| **5678/udp**           | Mikrotik邻居发现协议                                                                                         |
| **6343/tcp**           | 默认OpenFlow端口                                                                                             |
| **8080/tcp**           | HTTP Web 代理                                                                                                |
| **8291/tcp**           | [Winbox](https://help.mikrotik.com/docs/display/ROS/Winbox)                                                  |
| **8728/tcp**           | [API](https://help.mikrotik.com/docs/display/ROS/API)                                                        |
| **8729/tcp**           | API-SSL                                                                                                      |
| **20561/udp**          | MAC winbox                                                                                                   |
| **/1**                 | ICMP                                                                                                         |
| **/2**                 | [Multicast&IGMP](https://wiki.mikrotik.com/wiki/Manual:Routing "Manual:Routing")                             |
| **/4**                 | [IPIP](https://help.mikrotik.com/docs/display/ROS/IPIP) encapsulation                                        |
| **/41**                | IPv6 (encapsulation)                                                                                         |
| **/46**                | RSVP TE隧道                                                                                                  |
| **/47**                | GRE (General Routing Encapsulation)——用于PPTP和 [EoIP](https://help.mikrotik.com/docs/display/ROS/EoIP) 隧道 |
| **/50**                | 封装IPv4安全负载(ESP)                                                                                        |
| **/51**                | IPv4 (AH)的认证头                                                                                            |
| **/89**                | [OSPF](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328218) 路由协议                          |
| **/103**               | [Multicast&PIM](https://wiki.mikrotik.com/wiki/Manual:Routing "Manual:Routing")                              |
| **/112**               | [VRRP](https://help.mikrotik.com/docs/display/ROS/VRRP)                                                      |