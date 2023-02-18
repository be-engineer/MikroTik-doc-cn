# 建立高级防火墙

根据到现在学到的一切，尝试构建一个高级防火墙。在这个构建防火墙的例子中，尝试使用尽可能多的防火墙功能，来说明它们是如何工作的，以及何时应该以正确的方式使用它们。

大部分过滤将在RAW防火墙中完成，普通的防火墙将只包含一个基本的规则集，接受_已建立的、相关的和未跟踪的连接，丢弃所有其他来自非LAN的连接，充分保护路由器。

## 接口列表

为了便于今后的管理，用两个接口列表 **WAN** 和 **LAN**。连接到全球互联网的接口添加到WAN列表中，在这种情况下，它是 _ether1_!

```shell
/interface list
  add comment=defconf name=WAN
  add comment=defconf name=LAN
/interface list member
  add comment=defconf interface=bridge list=LAN
  add comment=defconf interface=ether1 list=WAN
```

## 保护设备

这里的主要目标是只允许从局域网访问路由器，而丢弃其他的。

注意，这里也接受ICMP，用来接受通过RAW规则的ICMP数据包。

```shell
/ip firewall filter
  add action=accept chain=input comment="defconf: accept ICMP after RAW" protocol=icmp
  add action=accept chain=input comment="defconf: accept established,related,untracked" connection-state=established,related,untracked
  add action=drop chain=input comment="defconf: drop all not coming from LAN" in-interface-list=!LAN
```

IPv6部分比较复杂，根据RFC建议，接受UDP跟踪路由、DHCPv6客户端PD和IPSec（IKE、AH、ESP）。

```shell
/ipv6 firewall filter
add action=accept chain=input comment="defconf: accept ICMPv6 after RAW" protocol=icmpv6
add action=accept chain=input comment="defconf: accept established,related,untracked" connection-state=established,related,untracked
add action=accept chain=input comment="defconf: accept UDP traceroute" port=33434-33534 protocol=udp
add action=accept chain=input comment="defconf: accept DHCPv6-Client prefix delegation." dst-port=546 protocol=udp src-address=fe80::/16
add action=accept chain=input comment="defconf: accept IKE" dst-port=500,4500 protocol=udp
add action=accept chain=input comment="defconf: accept IPSec AH" protocol=ipsec-ah
add action=accept chain=input comment="defconf: accept IPSec ESP" protocol=ipsec-esp
add action=drop chain=input comment="defconf: drop all not coming from LAN" in-interface-list=!LAN
```

## 保护客户端

在实际设置规则之前，先创建一个必要的 _地址列表_，其中包含所有不能被转发的IPv4/6地址。

注意，在这个列表中，添加了多播地址范围。它之所以出现，是因为在大多数情况下不使用多播。如果打算使用多播转发，这个地址列表应该禁用。

```shell
/ip firewall address-list
  add address=0.0.0.0/8 comment="defconf: RFC6890" list=no_forward_ipv4
  add address=169.254.0.0/16 comment="defconf: RFC6890" list=no_forward_ipv4
  add address=224.0.0.0/4 comment="defconf: multicast" list=no_forward_ipv4
  add address=255.255.255.255/32 comment="defconf: RFC6890" list=no_forward_ipv4
```

在IPv6的相同情况下，如果使用多播转发，应该从 _地址列表_ 中禁用多播条目。

```shell
/ipv6 firewall address-list
  add address=fe80::/10  comment="defconf: RFC6890 Linked-Scoped Unicast" list=no_forward_ipv6
  add address=ff00::/8  comment="defconf: multicast" list=no_forward_ipv6
```

_forward_ 链有比input多的规则。

- 接受 _已建立的、相关的_ 和 _未跟踪的_ 连接。
- 快速跟踪 _已建立的_ 和 _相关的_ 连接（目前只有IPv4）。
- 丢弃无效的连接。
- 丢弃坏的转发IP，因为无法在RAW链中可靠地确定哪些数据包被转发。
- 丢弃从互联网上发起的连接（从没有目标NAT的WAN端）。
- 丢弃不应该被转发的虚假IP。

如果攻击者知道内部局域网的网络，会丢弃所有非静态的IPv4数据包以保护对客户的直接攻击。通常情况下，这条规则是不必要的，因为RAW过滤器会丢弃这样的数据包，然而，这条规则是为了双重安全，以防RAW规则被不小心弄乱。

```shell
/ip firewall filter
  add action=accept chain=forward comment="defconf: accept all that matches IPSec policy" ipsec-policy=in,ipsec disabled=yes
  add action=fasttrack-connection chain=forward comment="defconf: fasttrack" connection-state=established,related
  add action=accept chain=forward comment="defconf: accept established,related, untracked" connection-state=established,related,untracked
  add action=drop chain=forward comment="defconf: drop invalid" connection-state=invalid
  add action=drop chain=forward comment="defconf:  drop all from WAN not DSTNATed" connection-nat-state=!dstnat connection-state=new in-interface-list=WAN
  add action=drop chain=forward src-address-list=no_forward_ipv4 comment="defconf: drop bad forward IPs"
  add action=drop chain=forward dst-address-list=no_forward_ipv4 comment="defconf: drop bad forward IPs"
```

IPv6 _forward_ 链非常相似，除了根据RFC建议接受IPsec和HIP，并丢弃 _hop-limit=1_ 的ICMPv6。

```shell
/ipv6 firewall filter
add action=accept chain=forward comment="defconf: accept established,related,untracked" connection-state=established,related,untracked
add action=drop chain=forward comment="defconf: drop invalid" connection-state=invalid
add action=drop chain=forward src-address-list=no_forward_ipv6 comment="defconf: drop bad forward IPs"
add action=drop chain=forward dst-address-list=no_forward_ipv6 comment="defconf: drop bad forward IPs"
add action=drop chain=forward comment="defconf: rfc4890 drop hop-limit=1" hop-limit=equal:1 protocol=icmpv6
add action=accept chain=forward comment="defconf: accept ICMPv6 after RAW" protocol=icmpv6
add action=accept chain=forward comment="defconf: accept HIP" protocol=139
add action=accept chain=forward comment="defconf: accept IKE" protocol=udp dst-port=500,4500
add action=accept chain=forward comment="defconf: accept AH" protocol=ipsec-ah
add action=accept chain=forward comment="defconf: accept ESP" protocol=ipsec-esp
add action=accept chain=forward comment="defconf: accept all that matches IPSec policy" ipsec-policy=in,ipsec
add action=drop chain=forward comment="defconf: drop everything else not coming from LAN" in-interface-list=!LAN
```

注意IPsec策略匹配器的规则。让IPsec封装的流量绕过快速通道是非常重要的。这就是为什么作为一个例子，添加了一个禁用的规则来接受匹配IPsec策略流量。只要在路由器上使用IPsec隧道，这个规则就应该启用。对于IPv6就简单多了，因为它不支持快速通道。

解决 IPsec 问题的另一种方法是添加 RAW 规则，将在后面的 RAW 部分讨论这种方法

## 伪装本地网络

为了使路由器后面的本地设备能够访问互联网，必须对本地网络进行伪装。在大多数情况下，建议使用src-nat而不是masquerade，在这种情况下，WAN地址是动态的，这是唯一的选择。

```shell
/ip firewall nat
  add action=accept chain=srcnat comment="defconf: accept all that matches IPSec policy" ipsec-policy=out,ipsec disabled=yes
  add action=masquerade chain=srcnat comment="defconf: masquerade" out-interface-list=WAN
```

注意禁用的策略匹配器规则与防火墙过滤器一样，IPSec流量必须排除在NAT之外（除了IPsec策略配置为匹配NAT地址的特定场景）。因此，只要在路由器上使用IPsec隧道，这个规则就必须启用。

## RAW过滤

## IPv4地址列表

在设置RAW规则之前，创建一些过滤策略所需的地址列表。RFC 6890将被用来作为参考。

首先，_address-list_ 包含所有不能用作src/dst/forwarded等的IPv4地址（如果看到这样的地址，将立即被丢弃）。

```shell
/ip firewall address-list
  add address=127.0.0.0/8 comment="defconf: RFC6890" list=bad_ipv4
  add address=192.0.0.0/24 comment="defconf: RFC6890" list=bad_ipv4
  add address=192.0.2.0/24 comment="defconf: RFC6890 documentation" list=bad_ipv4
  add address=198.51.100.0/24 comment="defconf: RFC6890 documentation" list=bad_ipv4
  add address=203.0.113.0/24 comment="defconf: RFC6890 documentation" list=bad_ipv4
  add address=240.0.0.0/4 comment="defconf: RFC6890 reserved" list=bad_ipv4
```

另一个地址列表包含所有不能全局路由的IPv4地址。

```shell
/ip firewall address-list
  add address=0.0.0.0/8 comment="defconf: RFC6890" list=not_global_ipv4
  add address=10.0.0.0/8 comment="defconf: RFC6890" list=not_global_ipv4
  add address=100.64.0.0/10 comment="defconf: RFC6890" list=not_global_ipv4
  add address=169.254.0.0/16 comment="defconf: RFC6890" list=not_global_ipv4
  add address=172.16.0.0/12 comment="defconf: RFC6890" list=not_global_ipv4
  add address=192.0.0.0/29 comment="defconf: RFC6890" list=not_global_ipv4
  add address=192.168.0.0/16 comment="defconf: RFC6890" list=not_global_ipv4
  add address=198.18.0.0/15 comment="defconf: RFC6890 benchmark" list=not_global_ipv4
  add address=255.255.255.255/32 comment="defconf: RFC6890" list=not_global_ipv4
```

最后两个地址列表用于不能作为目的地或源地址的地址。

```shell
/ip firewall address-list
  add address=224.0.0.0/4 comment="defconf: multicast" list=bad_src_ipv4
  add address=255.255.255.255/32 comment="defconf: RFC6890" list=bad_src_ipv4
add address=0.0.0.0/8 comment="defconf: RFC6890" list=bad_dst_ipv4
  add address=224.0.0.0/4 comment="defconf: RFC6890" list=bad_dst_ipv4
```

## IPv4 RAW规则

原始IPv4规则将执行以下操作:

- **添加禁用的 "接受 "规则** - 可用于快速禁用RAW过滤，而无需禁用所有RAW规则。
- **接受** DHCP发现 - 大多数DHCP数据包不会被IP防火墙看到，但其中一些会被看到，所以要确保它们被接受。
- **丢弃** 使用虚假IP的数据包。
- 从无效的SRC和DST IP中 **丢弃** 。
- **丢弃** 来自广域网的全局性不可路由的IP。
- **丢弃** 来自LAN的源地址不等于192.168.88.0/24（默认IP范围）的数据包。
- **丢弃** 来自广域网的数据包，将其转发到192.168.88.0/24网络，如果攻击者知道内部网络，这会保护其免受攻击。
- **丢弃** 损坏的ICMP、UDP和TCP。
- **接受** 来自广域网和局域网的所有其他信息。
- **丢弃** 其他一切，确保任何新增加的接口（如PPPoE连接到服务提供商）得到保护，防止意外的错误配置。

```shell
/ip firewall raw
add action=accept chain=prerouting comment="defconf: enable for transparent firewall" disabled=yes
add action=accept chain=prerouting comment="defconf: accept DHCP discover" dst-address=255.255.255.255 dst-port=67 in-interface-list=LAN protocol=udp src-address=0.0.0.0 src-port=68
add action=drop chain=prerouting comment="defconf: drop bogon IP's" src-address-list=bad_ipv4
add action=drop chain=prerouting comment="defconf: drop bogon IP's" dst-address-list=bad_ipv4
add action=drop chain=prerouting comment="defconf: drop bogon IP's" src-address-list=bad_src_ipv4
add action=drop chain=prerouting comment="defconf: drop bogon IP's" dst-address-list=bad_dst_ipv4
add action=drop chain=prerouting comment="defconf: drop non global from WAN" src-address-list=not_global_ipv4 in-interface-list=WAN
add action=drop chain=prerouting comment="defconf: drop forward to local lan from WAN" in-interface-list=WAN dst-address=192.168.88.0/24
add action=drop chain=prerouting comment="defconf: drop local if not from default IP range" in-interface-list=LAN src-address=!192.168.88.0/24
add action=drop chain=prerouting comment="defconf: drop bad UDP" port=0 protocol=udp
add action=jump chain=prerouting comment="defconf: jump to ICMP chain" jump-target=icmp4 protocol=icmp
add action=jump chain=prerouting comment="defconf: jump to TCP chain" jump-target=bad_tcp protocol=tcp
add action=accept chain=prerouting comment="defconf: accept everything else from LAN" in-interface-list=LAN
add action=accept chain=prerouting comment="defconf: accept everything else from WAN" in-interface-list=WAN
add action=drop chain=prerouting comment="defconf: drop the rest"
```

请注意，这里使用了一些可选的链，第一个 **TCP** 链用来丢弃已知 _无效的_ **TCP** 数据包。

```shell
/ip firewall raw
add action=drop chain=bad_tcp comment="defconf: TCP flag filter" protocol=tcp tcp-flags=!fin,!syn,!rst,!ack
add action=drop chain=bad_tcp comment=defconf protocol=tcp tcp-flags=fin,syn
add action=drop chain=bad_tcp comment=defconf protocol=tcp tcp-flags=fin,rst
add action=drop chain=bad_tcp comment=defconf protocol=tcp tcp-flags=fin,!ack
add action=drop chain=bad_tcp comment=defconf protocol=tcp tcp-flags=fin,urg
add action=drop chain=bad_tcp comment=defconf protocol=tcp tcp-flags=syn,rst
add action=drop chain=bad_tcp comment=defconf protocol=tcp tcp-flags=rst,urg
add action=drop chain=bad_tcp comment="defconf: TCP port 0 drop" port=0 protocol=tcp
```

而另一条链用于 **ICMP** 。注意，如果想要一个非常严格的防火墙，可以使用严格的 **ICMP** 过滤，但大多数情况下没有必要，它只是给路由器的CPU增加更多的负担。大多数情况下，ICMP速率限制也是不必要的，因为Linux内核已经将ICMP数据包限制在100pps。

```shell
/ip firewall raw
add action=accept chain=icmp4 comment="defconf: echo reply" icmp-options=0:0 limit=5,10:packet protocol=icmp
add action=accept chain=icmp4 comment="defconf: net unreachable" icmp-options=3:0 protocol=icmp
add action=accept chain=icmp4 comment="defconf: host unreachable" icmp-options=3:1 protocol=icmp
add action=accept chain=icmp4 comment="defconf: protocol unreachable" icmp-options=3:2 protocol=icmp
add action=accept chain=icmp4 comment="defconf: port unreachable" icmp-options=3:3 protocol=icmp
add action=accept chain=icmp4 comment="defconf: fragmentation needed" icmp-options=3:4 protocol=icmp
add action=accept chain=icmp4 comment="defconf: echo" icmp-options=8:0 limit=5,10:packet protocol=icmp
add action=accept chain=icmp4 comment="defconf: time exceeded " icmp-options=11:0-255 protocol=icmp
add action=drop chain=icmp4 comment="defconf: drop other icmp" protocol=icmp
```

## IPv6地址列表

应该立即丢弃的IPv6地址列表

```shell
/ipv6 firewall address-list
add address=::1/128 comment="defconf: RFC6890 lo" list=bad_ipv6
add address=::ffff:0:0/96 comment="defconf: RFC6890 IPv4 mapped" list=bad_ipv6
add address=2001::/23 comment="defconf: RFC6890" list=bad_ipv6
add address=2001:db8::/32 comment="defconf: RFC6890 documentation" list=bad_ipv6
add address=2001:10::/28 comment="defconf: RFC6890 orchid" list=bad_ipv6
add address=::/96 comment="defconf: ipv4 compat" list=bad_ipv6
```

不可全局路由的IPv6地址列表

```shell
/ipv6 firewall address-list
add address=100::/64 comment="defconf: RFC6890 Discard-only" list=not_global_ipv6
add address=2001::/32 comment="defconf: RFC6890 TEREDO" list=not_global_ipv6
add address=2001:2::/48 comment="defconf: RFC6890 Benchmark" list=not_global_ipv6
add address=fc00::/7 comment="defconf: RFC6890 Unique-Local" list=not_global_ipv6
```

作为无效目标地址的地址列表

`/ipv6 firewall address-list add address=::/128 comment="defconf: unspecified" list=bad_dst_ipv6`

作为无效源地址的地址列表

```shell
/ipv6 firewall address-list
  add address=::/128 comment="defconf: unspecified" list=bad_src_ipv6
  add address=ff00::/8  comment="defconf: multicast" list=bad_src_ipv6
```

## IPv6 RAW规则

原始IPv6规则将执行以下操作：

- **添加禁用的接受规则** - 可用于快速禁用RAW过滤，而无需禁用所有RAW规则。
- **丢弃** 使用假IP的数据包。
- **丢弃** 来自无效的SRC和DST IP。
- **丢弃** 来自广域网的全局无法路由的IP。
- **丢弃** 损坏的ICMP。
- **接受** 来自广域网和局域网的其他所有数据。
- **丢弃** 其他所有数据，确保任何新增加的接口（如PPPoE连接到服务提供商）受到保护，防止意外的错误配置。

```shell
/ipv6 firewall raw
add action=accept chain=prerouting comment="defconf: enable for transparent firewall" disabled=yes
add action=accept chain=prerouting comment="defconf: RFC4291, section 2.7.1" src-address=::/128 dst-address=ff02:0:0:0:0:1:ff00::/104 icmp-options=135 protocol=icmpv6
add action=drop chain=prerouting comment="defconf: drop bogon IP's" src-address-list=bad_ipv6
add action=drop chain=prerouting comment="defconf: drop bogon IP's" dst-address-list=bad_ipv6
add action=drop chain=prerouting comment="defconf: drop packets with bad SRC ipv6" src-address-list=bad_src_ipv6
add action=drop chain=prerouting comment="defconf: drop packets with bad dst ipv6" dst-address-list=bad_dst_ipv6
add action=drop chain=prerouting comment="defconf: drop non global from WAN" src-address-list=not_global_ipv6 in-interface-list=WAN
add action=jump chain=prerouting comment="defconf: jump to ICMPv6 chain" jump-target=icmp6 protocol=icmpv6
add action=accept chain=prerouting comment="defconf: accept local multicast scope" dst-address=ff02::/16
add action=drop chain=prerouting comment="defconf: drop other multicast destinations" dst-address=ff00::/8
add action=accept chain=prerouting comment="defconf: accept everything else from WAN" in-interface-list=WAN
add action=accept chain=prerouting comment="defconf: accept everything else from LAN" in-interface-list=LAN
add action=drop chain=prerouting comment="defconf: drop the rest"
```

请注意，使用了可选的 **ICMP**链。如果想要一个非常严格的防火墙，可以用这种严格的 **ICMP** 过滤，但大多数情况下是没有必要的，只是给路由器的CPU增加了更多的负载。大多数情况下，ICMP速率限制也是不必要的，因为Linux内核已经将ICMP数据包限制在100pps以内了。

```shell
/ipv6 firewall raw
# Be aware that different operating systems originate packets with different default TTL values
add action=accept chain=icmp6 comment="defconf: rfc4890 drop ll if hop-limit!=255" dst-address=fe80::/10 hop-limit=not-equal:255 protocol=icmpv6
add action=accept chain=icmp6 comment="defconf: dst unreachable" icmp-options=1:0-255 protocol=icmpv6
add action=accept chain=icmp6 comment="defconf: packet too big" icmp-options=2:0-255 protocol=icmpv6
add action=accept chain=icmp6 comment="defconf: limit exceeded" icmp-options=3:0-1 protocol=icmpv6
add action=accept chain=icmp6 comment="defconf: bad header" icmp-options=4:0-2 protocol=icmpv6
add action=accept chain=icmp6 comment="defconf: Mobile home agent address discovery" icmp-options=144:0-255 protocol=icmpv6
add action=accept chain=icmp6 comment="defconf: Mobile home agent address discovery" icmp-options=145:0-255 protocol=icmpv6
add action=accept chain=icmp6 comment="defconf: Mobile prefix solic" icmp-options=146:0-255 protocol=icmpv6
add action=accept chain=icmp6 comment="defconf: Mobile prefix advert" icmp-options=147:0-255 protocol=icmpv6
add action=accept chain=icmp6 comment="defconf: echo request limit 5,10" icmp-options=128:0-255 limit=5,10:packet protocol=icmpv6
add action=accept chain=icmp6 comment="defconf: echo reply limit 5,10" icmp-options=129:0-255 limit=5,10:packet protocol=icmpv6
add action=accept chain=icmp6 comment="defconf: rfc4890 router solic limit 5,10 only LAN" hop-limit=equal:255 icmp-options=133:0-255 in-interface-list=LAN limit=5,10:packet protocol=icmpv6
add action=accept chain=icmp6 comment="defconf: rfc4890 router advert limit 5,10 only LAN" hop-limit=equal:255 icmp-options=134:0-255 in-interface-list=LAN limit=5,10:packet protocol=icmpv6
add action=accept chain=icmp6 comment="defconf: rfc4890 neighbor solic limit 5,10 only LAN" hop-limit=equal:255 icmp-options=135:0-255 in-interface-list=LAN limit=5,10:packet protocol=icmpv6
add action=accept chain=icmp6 comment="defconf: rfc4890 neighbor advert limit 5,10 only LAN" hop-limit=equal:255 icmp-options=136:0-255 in-interface-list=LAN limit=5,10:packet protocol=icmpv6
add action=accept chain=icmp6 comment="defconf: rfc4890 inverse ND solic limit 5,10 only LAN" hop-limit=equal:255 icmp-options=141:0-255 in-interface-list=LAN limit=5,10:packet protocol=icmpv6
add action=accept chain=icmp6 comment="defconf: rfc4890 inverse ND advert limit 5,10 only LAN" hop-limit=equal:255 icmp-options=142:0-255 in-interface-list=LAN limit=5,10:packet protocol=icmpv6
add action=drop chain=icmp6 comment="defconf: drop other icmp" protocol=icmpv6
```
