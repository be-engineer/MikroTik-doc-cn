# 建立第一个防火墙

强烈建议保持默认防火墙的状态。有一些调整使其更加安全。确保在完全了解这些特定防火墙规则的好处后再配置其他的。

要通过CLI查看默认防火墙规则，可以键入：

`/system default-configuration print`

## Ipv4防火墙 

### 保护路由器

- 和新的连接一起工作，减少路由器的负载。
- 为允许访问路由器的IP地址创建 _地址列表_ 。
- 启用ICMP访问（可选）。
- 丢弃其他所有，_log=yes_ 可能会添加到记录中特定规则的数据包。

```shell
/ip firewall filter
add action=accept chain=input comment="default configuration" connection-state=established,related
add action=accept chain=input src-address-list=allowed_to_router
add action=accept chain=input protocol=icmp
add action=drop chain=input
/ip firewall address-list
add address=192.168.88.2-192.168.88.254 list=allowed_to_router
```

### 保护LAN设备

创建名为 "不在互联网上"的 _地址列表_，把它用于防火墙过滤规则。

```shell
/ip firewall address-list
add address=0.0.0.0/8 comment=RFC6890 list=not_in_internet
add address=172.16.0.0/12 comment=RFC6890 list=not_in_internet
add address=192.168.0.0/16 comment=RFC6890 list=not_in_internet
add address=10.0.0.0/8 comment=RFC6890 list=not_in_internet
add address=169.254.0.0/16 comment=RFC6890 list=not_in_internet
add address=127.0.0.0/8 comment=RFC6890 list=not_in_internet
add address=224.0.0.0/4 comment=Multicast list=not_in_internet
add address=198.18.0.0/15 comment=RFC6890 list=not_in_internet
add address=192.0.0.0/24 comment=RFC6890 list=not_in_internet
add address=192.0.2.0/24 comment=RFC6890 list=not_in_internet
add address=198.51.100.0/24 comment=RFC6890 list=not_in_internet
add address=203.0.113.0/24 comment=RFC6890 list=not_in_internet
add address=100.64.0.0/10 comment=RFC6890 list=not_in_internet
add address=240.0.0.0/4 comment=RFC6890 list=not_in_internet
add address=192.88.99.0/24 comment="6to4 relay Anycast [RFC 3068]" list=not_in_internet
```

简单的防火墙过滤规则解释:

- 把带有 _connection-state=established,related_ 的数据包添加到FastTrack，提高数据吞吐量，防火墙只对新的连接起作用。
- 丢弃无效的连接，并以 "无效 "为前缀进行记录。
- 丢弃从本地网络到达非公共地址的尝试，应用 _address-list=not_in_internet_ 之前，"bridge "是本地网络接口，log=yes用前缀"!public_from_LAN"尝试。
- 丢弃没有被NAT的传入数据包，ether1是公共接口，尝试记录带有"!NAT "前缀的。
- 跳到ICMP链，丢弃不需要的ICMP信息
- 丢弃来自互联网的数据包，这些数据包不是公共IP地址，ether1是公共接口，用"!public "前缀尝试记录。
- 丢弃来自LAN的数据包，这些数据包没有LAN IP，192.168.88.0/24是本地网络使用的子网。

```shell
/ip firewall filter
add action=fasttrack-connection chain=forward comment=FastTrack connection-state=established,related
add action=accept chain=forward comment="Established, Related" connection-state=established,related
add action=drop chain=forward comment="Drop invalid" connection-state=invalid log=yes log-prefix=invalid
add action=drop chain=forward comment="Drop tries to reach not public addresses from LAN" dst-address-list=not_in_internet in-interface=bridge log=yes log-prefix=!public_from_LAN out-interface=!bridge
add action=drop chain=forward comment="Drop incoming packets that are not NAT`ted" connection-nat-state=!dstnat connection-state=new in-interface=ether1 log=yes log-prefix=!NAT
add action=jump chain=forward protocol=icmp jump-target=icmp comment="jump to ICMP filters"
add action=drop chain=forward comment="Drop incoming from internet which is not public IP" in-interface=ether1 log=yes log-prefix=!public src-address-list=not_in_internet
add action=drop chain=forward comment="Drop packets from LAN that do not have LAN IP" in-interface=bridge log=yes log-prefix=LAN_!LAN src-address=!192.168.88.0/24
```

在 "icmp "链中只允许需要的icmp代码:

```shell
/ip firewall filter
  add chain =icmp protocol =icmp icmp-options =0:0 action =accept \
    comment = "echo reply"
  add chain =icmp protocol =icmp icmp-options =3:0 action =accept \
    comment = "net unreachable"
  add chain =icmp protocol =icmp icmp-options =3:1 action =accept \
    comment = "host unreachable"
  add chain =icmp protocol =icmp icmp-options =3:4 action =accept \
    comment = "host unreachable fragmentation required"
  add chain =icmp protocol =icmp icmp-options =8:0 action =accept \
    comment = "allow echo request"
  add chain =icmp protocol =icmp icmp-options =11:0 action =accept \
    comment = "allow time exceed"
  add chain =icmp protocol =icmp icmp-options =12:0 action =accept \
    comment = "allow parameter bad"
  add chain =icmp action =drop comment = "deny all other types"
```

## IPv6 防火墙 

### 保护路由器

创建一个地址列表，从该列表中访问设备。

`/ipv6 firewall address-list add address =fd12:672e:6f65:8899::/64 list =allowed`。

简要的IPv6防火墙过滤规则解释：

- 对新数据包进行处理，接受已建立的相关数据包。
- 拒绝来自互联网（公共）接口或接口列表的 _链接本地_ 地址。
- 接受从 _链接本地_ 地址到路由器的访问，接受用于管理目的的 _多播_ 地址，接受你的源 _地址列表_ 用于路由器访问。
- 丢弃其他东西。

```shell
/ipv6 firewall filter
add action=accept chain=input comment="allow established and related" connection-state=established,related
add chain=input action=accept protocol=icmpv6 comment="accept ICMPv6"
add chain=input action=accept protocol=udp port=33434-33534 comment="defconf: accept UDP traceroute"
add chain=input action=accept protocol=udp dst-port=546 src-address=fe80::/16 comment="accept DHCPv6-Client prefix delegation."
add action=drop chain=input in-interface=sit1 log=yes log-prefix=dropLL_from_public src-address=fe80::/16
add action=accept chain=input comment="allow allowed addresses" src-address-list=allowed
add action=drop chain=input
/ipv6 firewall address-list
add address=fe80::/16 list=allowed
add address=xxxx::/48 list=allowed
add address=ff02::/16 comment=multicast list=allowed
```

### 保护局域网设备

启用IPv6让客户可用于公共网络，设置适当的防火墙来保护客户。

- 接受 _已建立的/相关的_ 数据包并和 _新的_ 数据包一起工作。
- 丢弃无效的数据包，为规则设置前缀。
- 接受ICMP数据包。
- 接受从客户到互联网的 _新_ 连接。
- 丢弃其他一切。

```shell
/ipv6 firewall filter
add action=accept chain=forward comment=established,related connection-state=established,related
add action=drop chain=forward comment=invalid connection-state=invalid log=yes log-prefix=ipv6,invalid
add action=accept chain=forward comment=icmpv6 in-interface=!sit1 protocol=icmpv6
add action=accept chain=forward comment="local network" in-interface=!sit1 src-address-list=allowed
add action=drop chain=forward log-prefix=IPV6
```
