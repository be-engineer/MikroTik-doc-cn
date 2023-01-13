## 概述

RADIUS 是 Remote Authentication Dial-In User Service 的缩写，是一种远程服务器，可为各种网络设备提供身份验证和计费功能。 RADIUS 身份验证和计费使 ISP 或网络管理员能够通过大型网络中的一台服务器管理 PPP 用户访问和计费。 MikroTik RouterOS 有一个 RADIUS 客户端，可以验证 HotSpot，[PPP](https://help.mikrotik.com/docs/display/ROS/PPP)，[PPPoE](https://help.mikrotik.com/docs/display/ROS/PPPoE), [PPTP](https://help.mikrotik.com/docs/display/ROS/PPTP), [L2TP](https://help.mikrotik.com/docs/display/ROS/L2TP) 和 ISDN 连接。 从 RADIUS 服务器收到的属性会覆盖默认配置文件中设置的属性，但如果未收到某些参数，则它们会从相应的默认配置文件中获取。

只有在路由器的本地数据库中找不到匹配的用户访问记录时，才会查询 RADIUS 服务器数据库。

如果启用 RADIUS 计费，计费信息也会发送到该服务的默认 RADIUS 服务器。

## RADIUS 客户端

 **子菜单:** `/radius`

此子菜单允许添加/删除 RADIUS 客户端。

!!! warning 此列表中添加项目的顺序很重要。

### 属性

| 属性                                                                                                                                                                                                                                                                                                                          | 说明                                                                                                                                                                                                                                      |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **accounting-backup** (_yes                                     \| no_; Default: **no**)                                                                                                                                                                                                                                      | 配置是否为备份RADIUS服务器                                                                                                                                                                                                                |
| **accounting-port** (_integer [1..65535]_; Default: **1813**)                                                                                                                                                                                                                                                                 | 用于计费的RADIUS服务器端口                                                                                                                                                                                                                |
| **address** (_IPv4/IPv6 address_; Default: **0.0.0.0**)                                                                                                                                                                                                                                                                       | RADIUS 服务器的 IPv4 或 IPv6 地址。<br>接受以下格式：<br>\- _ipv4_  <br>\- _ipv4_`@`_vrf_  <br>\- _ipv6_  <br>\- _ipv6_`@`_vrf_                                                                                                           |
| **authentication-port** (_integer [1..65535]_; Default: **1812**)                                                                                                                                                                                                                                                             | 用于身份验证的 RADIUS 服务器端口。                                                                                                                                                                                                        |
| **called-id** (_string_; Default: )                                                                                                                                                                                                                                                                                           | 该值取决于点对点协议：PPPoE - 服务名称，PPTP - 服务器的 IP 地址，L2TP - 服务器的 IP 地址。                                                                                                                                                |
| **certificate** (_string_; Default: )                                                                                                                                                                                                                                                                                         | 用于和启用了 RadSec 的 RADIUS 服务器通信的证书文件。                                                                                                                                                                                      |
| **comment** (_string_; Default: )                                                                                                                                                                                                                                                                                             |                                                                                                                                                                                                                                           |
| **disabled** (_yes                                                                        \| no_; Default: **no**)                                                                                                                                                                                                            |
|                                                                                                                                                                                                                                                                                                                               |
| **domain** (_string_; Default: )                                                                                                                                                                                                                                                                                              | 客户端的 Microsoft Windows 域传递给需要域验证的 RADIUS 服务器。                                                                                                                                                                           |
| **protocol** (_radsec                                                                                                                                                                                                                                                                                                         | udp_; Default: **udp**)                                                                                                                                                                                                                   | 指定与 RADIUS 服务器通信时使用的协议。 |
| **realm** (_string_; Default: )                                                                                                                                                                                                                                                                                               | 明确规定的领域（用户域），因此用户不必在用户名中提供正确的 ISP 域名。                                                                                                                                                                     |
| **secret** (_string_; Default: )                                                                                                                                                                                                                                                                                              | 用于访问 RADIUS 服务器的共享机密。                                                                                                                                                                                                        |
| **service** (_ppp                                                                                                  \| login \| hotspot                                                                                                                         \| wireless                               \| dhcp_; Default: ) | 将使用此 RADIUS 服务器的路由器服务：<br> - hotspot - HotSpot 认证服务<br> - login - 路由器的本地用户认证<br> - ppp - 点对点客户端认证<br> - wireless - 无线客户端认证<br> - dhcp - DHCP 协议客户端认证（客户端的 MAC 地址作为用户名发送） |
| **src-address** (_ipv4/ipv6 address_; Default: **0.0.0.0**)                                                                                                                                                                                                                                                                   | 发送到RADIUS服务器的报文的源IP/IPv6地址                                                                                                                                                                                                   |
| **timeout** (_time_; Default: **100ms**)                                                                                                                                                                                                                                                                                      | 应重新发送请求的超时时间，例如 radius set timeout=300ms numbers=0                                                                                                                                                                         |

!!!info 当 RADIUS 服务器使用 CHAP、MS-CHAPv1、MS-CHAPv2 对用户进行身份验证时，它不使用共享密钥，该密钥仅在身份验证回复中使用，路由器正在对其进行验证。 因此，如果您的共享密钥有误，RADIUS 服务器将接受请求，但路由器不会接受回复。 您可以看到，使用 /radius monitor 命令，只要有人尝试连接，“错误回复”数量就会增加。

!!!warning 如果启用了 RadSec，请确保您的 RADIUS 服务器使用“**radsec**”作为共享密钥，否则，RADIUS 服务器将无法正确解密数据（不可打印的字符）。 使用 RadSec RouterOS 强制将共享机密设置为“radsec”，而不管手动设置的是什么 (RFC6614)。

### 例子

要为将针对 RADIUS 服务器 (10.0.0.3) 进行身份验证的 HotSpot 和 PPP 服务设置 RADIUS 客户端，您需要执行以下操作：

````shell
[admin@MikroTik] > /radius add service=hotspot,ppp address=10.0.0.3 secret=ex
[admin@MikroTik] > /radius print
Flags: X - disabled
# SERVICE CALLED-ID DOMAIN ADDRESS SECRET
0 ppp,hotspot

````

要使用 RadSec 设置 RADIUS 客户端，您需要执行以下操作：

```shell
[admin@MikroTik] > /radius add service=hotspot,ppp address=10.0.0.3 secret=radsec protocol=radsec certificate=client.crt
[admin@MikroTik] > /radius print
Flags: X - disabled
# SERVICE CALLED-ID DOMAIN ADDRESS SECRET
0 ppp,hotspot 10.0.0.3 radsec

```

确保指定的证书是可信的。

要查看 RADIUS 客户端统计信息，您需要执行以下操作：

```shell
[admin@MikroTik] > /radius monitor 0
pending: 0
requests: 10
accepts: 4
rejects: 1
resends: 15
timeouts: 5
bad-replies: 0
last-request-rtt: 0s

```

确保为所需服务启用 RADIUS 身份验证：

```shell
/ppp aaa set use-radius=yes
/ip hotspot profile set default use-radius=yes

```

## 从RADIUS连接终端

**子菜单:** `/radius incoming`

此工具支持从 RADIUS 服务器发送的未经请求的消息。 未经请求的消息扩展了 RADIUS 协议命令，允许终止已经从 RADIUS 服务器连接的会话。 为此，使用了 DM（断开连接消息）。 断开连接消息会导致用户会话立即终止。

!!! warning RouterOS 不支持 POD (Packet of Disconnect) 另一个 RADIUS 访问请求数据包，它执行与断开连接类似的功能

## 属性

| 属性                                                             | 说明                       |
| ---------------------------------------------------------------- | -------------------------- |
| **accept** (_yes                        \| no_; Default: **no**) | 是否接受主动消息           |
| **port** (_integer_; Default: **1700**)                          | 监听请求的端口号           |
| **vrf** (_VRF name_; default value: **main**)                    | 设置服务侦听传入连接的 VRF |