# 概述

LAC/LNS设置，也称为虚拟专用网VPDN (Virtual Private DialUp Network)，允许远程拨号用户与专用网进行远距离点对点连接。

拨号客户端通过PPPOE连接到LAC (L2TP access concentrator)， LAC决定会话通过IP网络转发到LNS (L2TP network Server)，建立L2TP隧道，并将PPP帧转发到服务器进行认证并建立会话(见下图)。

  

![](https://help.mikrotik.com/docs/download/attachments/9863181/LNS_LAC_CISCO.svg?version=1&modificationDate=1583326332898&api=v2&effects=drop-shadow)

  

在撰写本文时，RouterOS还不能作为LAC角色使用。因此，本文将演示如何将RouterOS作为LNS, Cisco路由器作为LAC建立一个非常基本的网络。

# 配置

使用简单的配置来演示VPDN设置的基本知识。假设LAC将转发给LNS客户端的FQDN名称包含 [mt.lv](https://mt.lv) 域。

## 客户

为了简单起见，假设客户端是RouterOS路由器:

`/interface pppoe-client add interface=ether1 user=good_worker@mt.lv password=strongpass`

## LAC

假设客户端与GigabitEthernet1端口相连，LNS服务器的IP地址为10.155.101.231

```shell
aaa new-model
!
aaa authentication ppp default local
!
vpdn enable
vpdn aaa attribute nas-ip-address vpdn-nas
vpdn search-order domain dnis
!
vpdn-group LAC
 request-dialin
  protocol l2tp
  domain mt.lv
 initiate-to ip 10.155.101.231
 source-ip 10.155.101.216
 local name LAC
 l2tp tunnel password 0 tunnelpass
!
bba-group pppoe MAIN-BBA
 virtual-template 1
!
interface GigabitEthernet1
 pppoe enable group MAIN-BBA
!
interface Virtual-Template1
 description pppoe MAIN-BBA
 no ip address
 no peer default ip address
 ppp mtu adaptive
 ppp authentication chap
!
```

注意，这个设置既不验证客户端，也不本地验证，也不通过RADIUS验证，实际上不检查域名，为了简单起见，不控制L2访问。如果您想使用这些功能，请参阅Cisco配置手册。

## LNS

在LNS端需要启用L2TP服务器，并设置LAC对L2TP连接进行验证的方法。

```shell
/interface l2tp-server server
set enabled=yes
/ppp l2tp-secret
add address=10.155.101.216/32 secret=tunnelpass
```

现在是实际的用户身份验证。在本例中，为了简单起见，我们将使用本地身份验证方法。

```shell
/ip pool
add name=pool0 ranges=192.168.99.2-192.168.99.99
/ppp profile
set default local-address=192.168.99.1 remote-address=pool0
/ppp secret
add name=good_worker@mt.lv password=strongpass
```

# 状态检查

在LNS上，通过查看l2tp服务器接口或查看活跃的ppp连接，可以看到所有成功连接的客户端:

```shell
[admin@CHR_v6_bgp] /interface l2tp-server> print
Flags: X - disabled, D - dynamic, R - running
# NAME USER MTU CLIENT-ADDRESS UPTIME ENCODING
0 DR <l2tp-... good_worker@mt.lv 1450 10.155.101.216 6h13m49s
 
[admin@CHR_v6_bgp] /ppp active> print
Flags: R - radius
# NAME SERVICE CALLER-ID ADDRESS UPTIME ENCODING
0 good_worker@mt.lv l2tp 10.155.101.216 192.168.99.2 6h15m57s
```

在LAC上，我们还可以看到活跃的客户端会话和LAC与LNS之间活跃的L2TP隧道:

```shell
csrLAC#show vpdn
 
L2TP Tunnel and Session Information Total tunnels 1 sessions 1
 
LocTunID RemTunID Remote Name State Remote Address Sessn L2TP Class/
Count VPDN Group
26090 11 CHR_v6_bgp est 10.155.101.231 50 LAC
 
LocID RemID TunID Username, Intf/ State Last Chg Uniq ID
Vcid, Circuit
18521 16 26090 good_worker@mt.lv, Gi1 est 06:17:07 571
```

# 会话建立

让我们仔细看看客户端会话是如何通过LAC进行身份验证和建立的。

![](https://help.mikrotik.com/docs/download/attachments/9863181/LNS_LAC_Establishment.svg?version=2&modificationDate=1583326052852&api=v2&effects=drop-shadow)

- 客户端发起PPPoE呼叫
- LAC和客户端开始LCP协商
- 协商成功后，LAC发送CHAP挑战
- 客户端发送CHAP响应
- LAC根据接收到的域名来判断是否将客户端会话转发到LNS。检查可以在本地完成，也可以使用RADIUS服务器完成。在转发会话之前，客户端也可以在这里进行身份验证。
- LAC建立L2TP隧道
- LNS检查LAC是否允许打开隧道并进行验证。隧道已经开通，可以转发VPDN会话。
- LAC将与客户端协商好的LCP选项、用户名和密码转发给LNS
- LNS对客户端进行本地认证或RADIUS认证，并发送CHAP响应
- 进入IPCP (IP Control Protocol)阶段，安装IP地址和路由。在这一点上，会议被认为是建立的。