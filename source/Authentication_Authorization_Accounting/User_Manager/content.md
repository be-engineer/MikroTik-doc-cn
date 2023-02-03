# 概述

用户管理器是 RouterOS 中的 RADIUS 服务器实现，它为某个服务提供集中的用户身份验证和授权。 拥有中央用户数据库可以更好地跟踪系统用户和客户。 作为一个单独的包，用户管理器可用于包括 SMIPS 在内的所有体系结构，但由于可用空间有限，必须小心。 它支持许多不同的身份验证方法，包括 PAP、CHAP、MS-CHAP、MS-CHAPv2、EAP-TLS、EAP-TTLS 和 EAP-PEAP。 在 RouterOS 中，DHCP、Dot1x、Hotspot、IPsec、PPP、Wireless 是最受益于用户管理器的功能。 每个用户都可以使用 WEB 界面查看他们的帐户统计信息并管理可用的配置文件。 此外，用户可以使用最流行的支付网关 - PayPal 购买他们自己的数据计划（配置文件），使其成为服务提供商的绝佳系统。 可以生成定制报告以简化计费部门的处理。 用户管理器根据 [RFC2865](https://tools.ietf.org/html/rfc2865) 和 [RFC3579](https://tools.ietf.org/html/rfc3579) 中定义的 RADIUS 标准工作。

![](https://help.mikrotik.com/docs/download/attachments/2555940/usermanager.jpg?version=1&modificationDate=1657264766867&api=v2)

## 属性

**子菜单:** `/user-manager attribute`

RADIUS 属性是在 RADIUS 服务器和客户端之间传递的已定义授权、信息和配置参数。 用户管理器允许发送在“属性”菜单中定义的自定义属性。 RouterOS 有一组已经存在的预定义属性，但也可以在必要时添加其他属性。 预定义属性：

| 属性                            | 供应商ID         | 类型ID | 值类型                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | 包类型                          | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| ------------------------------- | ---------------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Framed-IP-Address               | 0 (standard)     | 8      | ip地址                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Access-Accept                   | [RFC2865 section 5.8](https://tools.ietf.org/html/rfc2865#section-5.8)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| Framed-IP-Netmask               | 0 (standard)     | 9      | ip 地址                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Access-Accept                   | [RFC2865 section 5.9](https://tools.ietf.org/html/rfc2865#section-5.9)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| Session-Timeout                 | 0 (standard)     | 27     | integer                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Access-Accept, Access-Challenge | [RFC2865 section 5.27](https://tools.ietf.org/html/rfc2865#section-5.27)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| Idle-Timeout                    | 0 (standard)     | 28     | integer                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Access-Accept, Access-Challenge | [RFC2865 section 5.28](https://tools.ietf.org/html/rfc2865#section-5.28)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| Tunnel-Type                     | 0 (standard)     | 64     | 值 &emsp;说明<br>1&emsp;	Point-to-Point Tunneling Protocol (PPTP)<br>2&emsp;Layer Two Forwarding (L2F)<br>3&emsp;Layer Two Tunneling Protocol (L2TP)<br>4&emsp;Ascend Tunnel Management Protocol (ATMP<br>5&emsp;Virtual Tunneling Protocol (VTP)<br>6&emsp;IP Authentication Header in the Tunnel-mode (AH)<br>7&emsp;IP-in-IP Encapsulation (IP-IP)<br>8&emsp;Minimal IP-in-IP Encapsulation (MIN-IP-IP)<br>9&emsp;IP Encapsulating Security Payload in the Tunnel-mode (ESP)<br>10&emsp;Generic Route Encapsulation (GRE)<br>11&emsp;Bay Dial Virtual Services (DVS)<br>12&emsp;IP-in-IP Tunneling | Access-Accept                   | [RFC2868 section 3.1](https://tools.ietf.org/html/rfc2868#section-3.1)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| Tunnel-Medium-Type              | 0 (standard)     | 65     | 值&emsp; 说明<br>1&emsp;	IPv4 (IP version 4)<br>2&emsp;IPv6 (IP version 6<br>3&emsp;	NSAP<br>4&emsp;	HDLC (8-bit multidrop)<br>5&emsp;	BBN 1822<br>6&emsp;	802 (includes all 802 media plus Ethernet "canonical format")<br>7&emsp;	E.163 (POTS)<br>8&emsp;	E.164 (SMDS, Frame Relay, ATM)<br>9&emsp;	F.69 (Telex)<br>10&emsp;	X.121 (X.25, Frame Relay)<br>11&emsp;	IPX<br>12&emsp;	Appletalk<br>13&emsp;	Decnet IV<br>14&emsp;	Banyan Vines<br>15&emsp;	E.164 with NSAP format subaddress                                                                                                           | Access-Accept                   | [RFC2868 section 3.2](https://tools.ietf.org/html/rfc2868#section-3.2)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| Tunnel-Private-Group-ID         | 0 (standard)     | 81     | string                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Access-Accept                   | [RFC2868 section 3.6](https://tools.ietf.org/html/rfc2868#section-3.6)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| Framed-Pool                     | 0 (standard)     | 88     | string                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Access-Accept                   | [RFC2869 section 5.18](https://tools.ietf.org/html/rfc2869#section-5.18)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| Framed-IPv6-Prefix              | 0 (standard)     | 97     | ipv6 prefix                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Access-Accept                   | [RFC3162 section 2.3](https://tools.ietf.org/html/rfc3162#section-2.3)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| Framed-IPv6-Pool                | 0 (standard)     | 100    | string                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Access-Accept                   | [RFC3162 section 2.6](https://tools.ietf.org/html/rfc3162#section-2.6)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| Delegated-IPv6-Prefix           | 0 (standard)     | 123    | ipv6 prefix                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Access-Accept                   | [RFC4818](https://tools.ietf.org/html/rfc4818)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| Framed-IPv6-Address             | 0 (standard)     | 168    | ip address                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | Access-Accept                   | [RFC6911 section 3.1](https://tools.ietf.org/html/rfc6911#section-3.1)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| Mikrotik-Recv-Limit             | 14988 (Mikrotik) | 1      | integer                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Access-Accept                   | 客户端总接收字节数限制。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| Mikrotik-Xmit-Limit             | 14988 (Mikrotik) | 2      | integer                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Access-Accept                   | 客户端的总传输限制（以字节为单位）。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| Mikrotik-Group                  | 14988 (Mikrotik) | 3      | string                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Access-Accept                   | 本地用户组。<br>HotSpot 用户的 配置文件。<br>PPP 用户的配置文件。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| Mikrotik-Wireless-Forward       | 14988 (Mikrotik) | 4      | integer                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Access-Accept                   | 如果此属性设置为“0”（仅限无线），则不会将客户端的帧转发回无线基础设施。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| Mikrotik-Wireless-Skip-Dot1x    | 14988 (Mikrotik) | 5      | integer                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Access-Accept                   | 如果设置为非零值（仅无线），则禁用特定无线客户端的 802.1x 身份验证。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| Mikrotik-Wireless-Enc-Algo      | 14988 (Mikrotik) | 6      | 值&emsp;   说明<br>0&emsp; 	不加密<br>1&emsp; 	40-bit-WEP<br>2&emsp; 	104-bit-WEP<br>3&emsp; 	AES-CCM<br>4&emsp; TKIP                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | Access-Accept                   | WEP 加密算法(仅无线).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| Mikrotik-Wireless-Enc-Key       | 14988 (Mikrotik) | 7      | string                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Access-Accept                   | 客户端的 WEP 加密密钥（仅无线）。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| Mikrotik-Rate-Limit             | 14988 (Mikrotik) | 8      | string                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Access-Accept                   | 客户端的数据速率限制。 格式为：rx-rate[/tx-rate] [rx-burst-rate[/tx-burst-rate] [rx-burst-threshold[/tx-burst-threshold] [rx-burst-time[/tx- burst-time] [priority] [rx-rate-min[/tx-rate-min]]]] 从路由器的角度来看（“rx”是客户端上传，“tx”是客户端下载）。 所有比率都带有可选“k”（1,000s）或“M”（1,000,000s）的数字。 如果未指定 tx-rate，则 rx-rate 也与 tx-rate 相同。 tx-burst-rate 和 tx-burst-threshold 以及 tx-burst-time 也是如此。 如未指定 rx-burst-threshold 和 tx-burst-threshold（但指定了 burst-rate），则使用 rx-rate 和 tx-rate 作为突发阈值。 如果 rx-burst-time 和 tx-burst-time 均未指定，则默认使用 1s。 优先级取值 1..8，其中 1 表示最高优先级，8 - 最低。 如果未指定 rx-rate-min 和 tx-rate-min，则使用 rx-rate 和 tx-rate 值。 rx-rate-min 和 tx-rate-min 值不能超过 rx-rate 和 tx-rate 值。 |
| Mikrotik-Realm                  | 14988 (Mikrotik) | 9      | string                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Access-Request                  | 如果在 /radius 菜单中设置，它将作为 Mikrotik-Realm 属性包含在每个 RADIUS 请求中。 如果未设置，则发送与 MS-CHAP-Domain 属性中相同的值（如果缺少 MS-CHAP-Domain，则也不包括Realm）。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| Mikrotik-Host-IP                | 14988 (Mikrotik) | 10     | ip 地址                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Access-Request                  | Universal Client转换前HotSpot客户端的IP地址（客户端的原始IP地址）。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| Mikrotik-Mark-Id                | 14988 (Mikrotik) | 11     | string                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Access-Accept                   | 防火墙 mangle 链名称（仅限 HotSpot）。 MikroTik RADIUS 客户端在收到此属性后创建一个动态防火墙mangle规则，其中 action=jump chain=hotspot 和 jump-target 等于属性值。 Mangle 链名称可以有后缀 .in 或 .out，仅为传入或传出流量设置规则。 可以提供多个 Mark-id 属性，但只使用传入和传出的最后一个。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| Mikrotik-Advertise-URL          | 14988 (Mikrotik) | 12     | string                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Access-Accept                   | 包含向客户显示的广告页面的 URL。 如果指定了此属性，则会自动启用广告，包括透明代理，即使它们在相应的用户配置文件中被明确禁用。 多个属性实例可以由 RADIUS 服务器发送以指定循环方式选择的附加 URL。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| Mikrotik-Advertise-Interval     | 14988 (Mikrotik) | 13     | integer                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Access-Accept                   | 两个相邻广告之间的时间间隔。 多个属性实例可以由 RADIUS 服务器发送以指定额外的间隔。 所有间隔值都被视为一个列表，并针对每个成功的广告逐一获取。 如果到达列表末尾，则继续使用最后一个值。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| Mikrotik-Recv-Limit-Gigawords   | 14988 (Mikrotik) | 14     | integer                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Access-Accept                   | 4G (2^32) 字节的总接收限制（当 0..31位在 Mikrotik-Recv-Limit 中传送时使用32..63位）。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| Mikrotik-Xmit-Limit-Gigawords   | 14988 (Mikrotik) | 15     | integer                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Access-Accept                   | 4G (2^32) 字节的总接收限制（当 0..31位在 Mikrotik-Recv-Limit 中传送时使用32..63位）。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| Mikrotik-Wireless-PSK           | 14988 (Mikrotik) | 16     | string                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Access-Accept                   |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| Mikrotik-Total-Limit            | 14988 (Mikrotik) | 17     | integer                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Access-Accept                   |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| Mikrotik-Total-Limit-Gigawords  | 14988 (Mikrotik) | 18     | integer                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Access-Accept                   |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| Mikrotik-Address-List           | 14988 (Mikrotik) | 19     | string                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Access-Accept                   |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| Mikrotik-Wireless-MPKey         | 14988 (Mikrotik) | 20     | string                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Access-Accept                   |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| Mikrotik-Wireless-Comment       | 14988 (Mikrotik) | 21     | string                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Access-Accept                   |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| Mikrotik-Delegated-IPv6-Pool    | 14988 (Mikrotik) | 22     | string                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Access-Accept                   | 用于前缀委派的 IPv6 池。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| Mikrotik-DHCP-Option-Set        | 14988 (Mikrotik) | 23     | string                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Access-Accept                   |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| Mikrotik-DHCP-Option-Param-STR1 | 14988 (Mikrotik) | 24     | string                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Access-Accept                   |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| Mikrotik-DHCP-Option-Param-STR2 | 14988 (Mikrotik) | 25     | string                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Access-Accept                   |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| Mikrotik-Wireless-VLANID        | 14988 (Mikrotik) | 26     | integer                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Access-Accept                   | 客户端的 VLAN ID（仅无线）。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| Mikrotik-Wireless-VLANIDtype    | 14988 (Mikrotik) | 27     | 值&emsp;      说明<br>0&emsp;     802.1q <br>1 &emsp;   802.1ad                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | Access-Accept                   | 客户端的 VLAN ID 类型（仅无线）。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| Mikrotik-Wireless-Minsignal     | 14988 (Mikrotik) | 28     | string                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Access-Accept                   |
|                                 |
| Mikrotik-Wireless-Maxsignal     | 14988 (Mikrotik) | 29     | string                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Access-Accept                   |
| Mikrotik-Switching-Filter       | 14988 (Mikrotik) | 30     | string                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Access-Accept                   | 允许在使用 dot1x 服务器验证客户端时创建动态交换规则。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |

**属性**

 | 属性                                                    | 说明                                                                                                                           |
 | ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
 | **name** (_string_; Default: )                          | 属性名称。                                                                                                                     |
 | **packet-types** (_string_; Default: **access-accept**) | - access-accept - 在 RADIUS Access-Accept 消息中使用此属性<br>- access-challenge - 在 RADIUS Access-Challenge 消息中使用此属性 |
 | **type-id** (_integer:1..255_; Default: )               | 来自特定供应商属性数据库的属性标识号。                                                                                         |
 | **value-type** (_string_; Default: )                    | -   hex<br>-   ip地址 <br>- IPv4 ，IPv6 IP 地址<br>-   ip6-prefix - IPv6 prefix<br>-   macro<br>-   string<br>-   uint32       |
 | **vendor-id** (_integer_; Default: **0**)               | IANA 分配特定的企业标识号。                                                                                                    |

## 数据库

**子菜单:** `/user-manager database`

所有 RADIUS 相关信息都存储在单独的用户管理器数据库中，可配置在“数据库”子菜单下。 “Enabled”和“db-path”是唯一没有存储在用户管理器数据库中的参数，它们存储在主 RouterOS 配置表中，这意味着这些参数将受到 RouterOS 配置重置的影响。 其余配置、会话和支付数据存储在设备闪存上的单独 SQLite 数据库中。 在对数据库进行操作时，建议操作前后都进行备份。

**属性**

 | 属性                              | 说明                                                  |
 | --------------------------------- | ----------------------------------------------------- |
 | **db-path** (_string_; Default: ) | Path to location where database files will be stored. |

**只读属性**

| 属性                | 说明                             |
| ------------------- | -------------------------------- |
| **db-size**         | 当前数据库大小                   |
| **free-disk-space** | 存储数据库磁盘上剩余的可用空间。 |

**命令**

| 属性                                               | 说明                                                                           |
| -------------------------------------------------- | ------------------------------------------------------------------------------ |
| **load** (_name_)                                  | 以 .umb 格式恢复以前创建的备份文件。                                           |
| **migrate-legacy-db** (_database-path; overwrite_) | 将旧用户管理器（从 RouterOS v6 或更早版本）转换为新标准。 可以覆盖当前数据库。 |
| **optimize-db** ()                                 |
| **save** (name; overwrite)                         | 保存用户管理器数据库的当前状态。                                               |

## 限制

**子菜单:** `/user-manager limitation`

限制由配置文件使用，并由配置文件限制链接在一起。 必须启用 RADIUS 记帐和临时更新，以便在达到 _download-limit_、_upload-limit_ 或 _uptime-limit_ 时在多个限制之间无缝切换或断开活动会话。

要从用户管理器断开已激活的会话，必须在 RADIUS 客户端上将_accept_设置为 _yes_。 如果并发会话限制不是无限的（共享用户）并且已达到最大允许数量，则路由器将首先尝试断开旧用户会话。

用户管理器在接受新用户之前尝试断开活动会话（当设置了适当的限制时），这就是为什么在此类设置中建议将 1s 用于/radius client timeout。
  
RouterOS 中的 IPsec 服务不支持速率限制。

**属性**

| 属性                                                  | 说明                                                                                                                                      |
| ----------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| **comment** (_string_; Default: )                     | 限制的简短描述。                                                                                                                          |
| **download-limit** (_integer_; Default: **0**)        | 用户可以下载的总流量（以字节为单位）。                                                                                                    |
| **name** (_string_; Default: )                        | 限制的唯一名称。                                                                                                                          |
| **rate-limit-burst-rx** ()                            | _MT-Rate-Limit_ RADIUS 属性的一部分。 请参阅 [Queues#SimpleQueue](https://help.mikrotik.com/docs/display/ROS/Queues#Queues-SimpleQueue)。 |
| **rate-limit-burst-threshold-rx** ()                  | _MT-Rate-Limit_ RADIUS 属性的一部分。 请参阅 [Queues#SimpleQueue](https://help.mikrotik.com/docs/display/ROS/Queues#Queues-SimpleQueue)。 |
| **rate-limit-burst-threshold-tx** ()                  | _MT-Rate-Limit_ RADIUS 属性的一部分。 请参阅 [Queues#SimpleQueue](https://help.mikrotik.com/docs/display/ROS/Queues#Queues-SimpleQueue)。 |
| **rate-limit-burst-time-rx** ()                       | _MT-Rate-Limit_ RADIUS 属性的一部分。 请参阅 [Queues#SimpleQueue](https://help.mikrotik.com/docs/display/ROS/Queues#Queues-SimpleQueue)。 |
| **rate-limit-burst-time-tx** ()                       | _MT-Rate-Limit_ RADIUS 属性的一部分。 请参阅 [Queues#SimpleQueue](https://help.mikrotik.com/docs/display/ROS/Queues#Queues-SimpleQueue)。 |
| **rate-limit-burst-tx** ()                            | _MT-Rate-Limit_ RADIUS 属性的一部分。 请参阅 [Queues#SimpleQueue](https://help.mikrotik.com/docs/display/ROS/Queues#Queues-SimpleQueue)。 |
| **rate-limit-min-rx** ()                              | _MT-Rate-Limit_ RADIUS 属性的一部分。 请参阅 [Queues#SimpleQueue](https://help.mikrotik.com/docs/display/ROS/Queues#Queues-SimpleQueue)。 |
| **rate-limit-min-tx** ()                              | _MT-Rate-Limit_ RADIUS 属性的一部分。 请参阅 [Queues#SimpleQueue](https://help.mikrotik.com/docs/display/ROS/Queues#Queues-SimpleQueue)。 |
| **rate-limit-priority** ()                            | _MT-Rate-Limit_ RADIUS 属性的一部分。 请参阅 [Queues#SimpleQueue](https://help.mikrotik.com/docs/display/ROS/Queues#Queues-SimpleQueue)。 |
| **rate-limit-rx** ()                                  | _MT-Rate-Limit_ RADIUS 属性的一部分。 请参阅 [Queues#SimpleQueue](https://help.mikrotik.com/docs/display/ROS/Queues#Queues-SimpleQueue)。 |
| **rate-limit-tx** ()                                  | _MT-Rate-Limit_ RADIUS 属性的一部分。 请参阅 [Queues#SimpleQueue](https://help.mikrotik.com/docs/display/ROS/Queues#Queues-SimpleQueue)。 |
| **reset-counters-interval** (_hourly_                 | _daily_                                                                                                                                   | _weekly_ | _monthly_ | _disabled_); Default: **disabled**) | 从 _reset-counters-start-time_ 清除所有相关用户统计信息的时间间隔。 |
| **reset-counters-start-time** (_datetime_; Default: ) | 计算 _reset-counters-interval_ 的静态日期和时间值。                                                                                       |
| **transfer-limit** (_integer_; Default: **0**)        | 以字节为单位的聚合（下载+正常运行）总流量。                                                                                               |
| **upload-limit** (_integer_; Default: **0**)          | 用户可以上传的总流量（以字节为单位）。                                                                                                    |
| **uptime-limit** (_time_; Default: **00:00:00**)      | 用户可以保持活跃的总正常运行时间。                                                                                                        |

## 付费

**子菜单:** `/user-manager payment`

本节提供有关所有已付款的信息。

**只读属性**

 | 属性                                   | 说明                                                                                                                                                          |
 | -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
 | **currency** (_string_)                | 交易中使用的货币。                                                                                                                                            |
 | **method** (_string_)                  | 用于交易的服务（目前仅限 PayPal）。                                                                                                                           |
 | **price** (_decimal_)                  | 用户支付的金额。                                                                                                                                              |
 | **profile** (_profile_)                | 用户购买的配置文件名称。                                                                                                                                      |
 | **trans-end** (_datetime_)             | 交易开始的日期和时间。                                                                                                                                        |
 | **trans-start** (_datetime_)           | 交易结束的日期和时间。                                                                                                                                        |
 | **trans-status** (_string_)            | 交易的状态。 可能的状态 - _started_、_pending_、_approved_、_declined_、_error_、_timeout_、_aborted_、_user approved_。 只有 _approved_ 才被视为完整的交易。 |
 | **user** (_string_; Default: )         | 执行交易的用户姓名。                                                                                                                                          |
 | **user-message** (_string_; Default: ) |

## 配置文件

**子菜单:** `/user-manager profile`

**属性**

 | 属性                                                                                                                                           | 说明                                                                                                                   |
 | ---------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
 | **comment** (_string_; Default: )                                                                                                              | 条目的短描述。                                                                                                         |
 | **name** (_string_; Default: )                                                                                                                 | 配置文件的唯一名称。                                                                                                   |
 | **name-for-users** (_string_; Default: )                                                                                                       | 将在网页上为用户显示的配置文件的名称。                                                                                 |
 | **override-shared-users** (_decimal      \| off                                                               \| unlimited_; Default: **off**) | 是否允许具有相同用户名的多个会话。 会覆盖 _shared-users_ 设置。                                                        |
 | **price** (_decimal_; Default: **0.00**)                                                                                                       |
 | **starts-when** (_assigned_              \| _first-auth_; Default: **assigned**)                                                               | 配置文件何时变为活动状态。 _Assigned_ - 创建用户配置文件条目时立即分配。 _First-auth_ - 根据用户的第一次身份验证请求。 |
 | **validity** (_time                      \| unlimited_; Default: **unlimited**)                                                                | 用户可以使用此配置文件的总时间。                                                                                       |

## 配置文件限制

**子菜单:** `/user-manager profile-limitation`

Profile-Limitations 表将 Limitations 和 Profiles 链接在一起并定义其有效期。 当多个限制分配给同一个配置文件时，用户必须遵守所有限制才能建立会话。 这允许创建更复杂的设置，例如，单独的每月和每天带宽限制。

**属性**

| 属性                                                                                                      | 说明                     |
| --------------------------------------------------------------------------------------------------------- | ------------------------ |
| **comment** (_string_; Default: )                                                                         | 条目的简短描述。         |
| **from-time** (_time_; Default: **00:00:00**)                                                             | 限制开始的一天中的时间。 |
| **limitation** (_limitation_; Default: )                                                                  | 已创建的**限制**名称 。  |
| **profile** (_profile_; Default: )                                                                        | 已创建的**配置文件**名称 |
| **till-time** (_time_; Default: **23:59:59**)                                                             | 限制结束的时间。         |
| **weekdays** (_day of week_; Default: **Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday**) | 激活限制的星期。         |

## 路由器

**子菜单:** `/user-manager router`

这里定义了所有可使用 User Manager 作为 RADIUS 服务器的 NAS 设备。

**属性**

| 属性                                                                          | 说明                                               |
| ----------------------------------------------------------------------------- | -------------------------------------------------- |
| **coa-port** (_integer:1..65535_; Default: **3799**)                          | CoA（授权变更）通信的端口号。                      |
| **address** (_IP/IPv6_**;** Default: )                                        | RADIUS客户端的IP地址。                             |
| **comment** (_string_; Default: )                                             | NAS 的简短描述。                                   |
| **disabled** (_yes                                   \| no_; Default: **no**) | 控制条目当前是否处于活动状态。                     |
| **name** (_string_; Default: )                                                | RADIUS 客户端的唯一名称。                          |
| **shared-secret** (_string_; Default: )                                       | 用于保护 RADIUS 服务器和 RADIUS 客户端之间的通信。 |

**命令**
| 属性                  | 说明                                   |
| --------------------- | -------------------------------------- |
| **reset-counters** () | 清除特定 RADIUS 客户端的所有统计信息。 |

## 会话

**子菜单:** `/user-manager session`

仅当在 NAS 上启用记帐时才会记录会话。

**只读属性**

 | 属性                                            | 说明                                                                                                                                                                             |
 | ----------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
 | **acct-session-id** (_string_)                  | 计费会话的唯一标识。                                                                                                                                                             |
 | **active** (_yes                        \| no_) | 当前是否使用会话。                                                                                                                                                               |
 | **calling-station-id** (_string_)               | 用户的标识符，通常是 IP 地址或 MAC 地址。                                                                                                                                        |
 | **download** (_Bytes_)                          | 下载的流量。                                                                                                                                                                     |
 | **ended** (_datetime_)                          | 会话结束的日期和时间。 活动会话为空。                                                                                                                                            |
 | **last-accounting-packet** (_datetime_)         | 收到最后一次计费更新的日期和时间。                                                                                                                                               |
 | **nas-ip-address** (_IP address_)               | NAS的IP地址。                                                                                                                                                                    |
 | **nas-port-id** (_string_)                      | 对用户进行身份验证的 NAS 端口的标识符。                                                                                                                                          |
 | **nas-port-type** (_string_)                    | 对用户进行身份验证的端口类型（_physical_ 或 _virtual_）。                                                                                                                        |
 | **started** (_datetime_)                        | 建立会话的日期和时间。                                                                                                                                                           |
 | **status** (_list of statuses_)                 | 会话的可用状态：_start -_accounting message_Start_已收到，_stop -_accounting message_Stop_已收到，_interim -Interim update_已收到，_close-acked_ - session已成功关闭，_expired._ |
 | **terminate-cause** (_string_)                  | 会话关闭原因。                                                                                                                                                                   |
 | **upload** (_Bytes_)                            | 上传的流量。                                                                                                                                                                     |
 | **uptime** (_time_)                             | 会话中记录的总正常运行时间。                                                                                                                                                     |
 | **user** (_string_)                             | 用户名                                                                                                                                                                           |
 | **user-address** (_IP address_)                 | 提供给用户的 IP 地址。                                                                                                                                                           |

## 设置

**子菜单:** `/user-manager`

**属性**

| 属性                                                                            | 说明                                                                                          |
| ------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| **accounting-port** (_integer_; Default: **1813**)                              | 监听 RADIUS 记帐请求的端口。                                                                  |
| **authentication-port** (_integer_; Default: **1812**)                          | 监听 RADIUS 身份验证请求的端口。                                                              |
| **_certificate_** (_certificate_; Default: )                                    | 用于 EAP TLS 类型身份验证方法的证书。                                                         |
| **_enabled_** (_yes                                    \| no_; Default: **no**) | 是否启用了用户管理器功能。                                                                    |
| **use-profiles** (_yes                                 \| no_; Default: **no**) | 是否使用 **配置文件** 和 **限制**。 当设置为 _no 时，_ 只有 **用户** 配置需要运行用户管理器。 |

## 高级属性

**子菜单:** `/user-manager advanced`

**属性**

| 属性                                                                      | 说明                                         |
| ------------------------------------------------------------------------- | -------------------------------------------- |
| **paypal-allow** (_yes                           \| no_; Default: **no**) | 是否为用户管理器启用 PayPal 功能。           |
| **paypal-currency** (_string_; Default: **USD**)                          | 对用户计费的 _价格_ 设置相关的货币。         |
| **paypal-password** (_string_; Default: )                                 | 你的 PayPal API 帐户的密码。                 |
| **paypal-signature** (_string_; Default: )                                | 你的 PayPal API 帐户的签名。                 |
| **paypal-use-sandbox** (_yes                     \| no_; Default: **no**) | 是否使用 PayPal 的沙盒环境进行测试。         |
| **paypal-user** (_string_; Default: )                                     | 你的 PayPal API 帐户的用户名。               |
| **web-private-password** (_string_; Default: )                            | 通过 HTTP 访问 _/um/PRIVATE/_ 部分的密码。   |
| **web-private-username** (_string_; Default: )                            | 通过 HTTP 访问 _/um/PRIVATE/_ 部分的用户名。 |

## 用户

**子菜单:** `/user-manager user`

**属性**

| 属性                                                                             | 说明                                                        |
| -------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| **attributes** (_array of attributes_; Default: )                                | 自定义的 **属性** 集和值将另外添加到 Access-Accept 消息中。 |
| **caller-id** (_string_; Default: )                                              | 允许使用特定的 _Calling-Station-Id_ 值进行用户身份验证。    |
| **comment** (_string_; Default: )                                                | 用户的简短描述。                                            |
| **disabled** (_yes                                \| no_; Default: **no**)       | 控制用户是否可以使用。                                      |
| **group** (_group_; Default: **default**)                                        | 用户关联的**组**名称。                                      |
| **name** (_string_; Default: )                                                   | 会话验证的用户名。                                          |
| **otp-secret** (_string_; Default: )                                             | 附加到密码的一次性密码令牌。                                |
|                                                                                  |
| **password** (_string_; Default: )                                               | 会话认证的用户密码。                                        |
| **shared-users** (_integer                        \| unlimited_; Default: **1**) | 用户可以同时建立的会话总数。                                |

**命令**

| 属性                    | 说明                                                                                                                                             |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| **add-batch-users** ()  | 该命令可以根据各种参数生成多个用户帐户。                                                                                                         |
| **generate-voucher** () | 基于可以呈现给最终用户的 _voucher-template_ 生成一个文件。                                                                                       |
| **monitor** ()          | 显示用户的总统计信息。 统计数据包括_total-uptime_、_total-download_、_total-upload_、_active-sessions_、_actual-profile_、_attributes-details_。 |

## 用户组

**子菜单:** `/user-manager user group`

用户组定义了多个用户的共同特征，例如允许的身份验证方法和 RADIUS 属性。 用户管理器中已经存在两个组，称为 _default_ 和 _default-anonymous_。

**属性**

| 属性                                              | 说明                                                                                                                                      |
| ------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| **attributes** (_array of attributes_; Default: ) | 一组自定义的 **属性** 和值将另外添加到该组中用户的 Access-Accept 消息中。                                                                 |
| **comment** (_string_; Default: )                 | 组的简短描述。                                                                                                                            |
| **inner-auths** (_list of auths_; Default: )      | 隧道（外部）允许的身份验证方法列表。 支持的内部验证方法 - _ttls-pap_、_ttls-chap_、_ttls-mschap1_、_ttls-mschap2_、_peap-mschap2_。       |
| **name** (_string_; Default: )                    | 唯一的组名称                                                                                                                              |
| **outer-auths** (_list of auths_; Default: )      | 允许的身份验证方法列表。 支持的外部身份验证方法 - _pap_、_chap_、_mschap1_、_mschap2_、_eap-tls_、_eap-ttls_、_eap-peap_、_eap-mschap2_。 |

## 用户配置文件

**子菜单:** `/user-manager user-profile`

此菜单为用户分配配置文件并跟踪配置文件的状态。 单个用户可以分配多个配置文件，但同时只能使用一个。 当前活动配置文件到期时，用户将无缝切换到下一个配置文件，而不会中断用户的会话。

**属性**

| 属性                               | 说明                           |
| ---------------------------------- | ------------------------------ |
| **profile** (_profile_; Default: ) | 要为用户分配的配置文件的名称。 |
| **user** (_user_; Default: )       | 使用特定配置文件的用户名。     |

**只读属性**

| 属性                                                                                      | 说明                                                                                                                                            |
| ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| **end-time** (_datetime_)                                                                 | **用户配置文件** 到期的日期和时间。                                                                                                             |
| **state** (_running active_ \| running                                         \| _used_) | **用户配置文件**的当前状态。 _Running active -_ 用户当前使用的配置文件。 _Running_ - 配置文件已准备好使用。 _Used_ - 无法再激活的过期配置文件。 |

**命令**

| 属性                         | 说明                             |
| ---------------------------- | -------------------------------- |
| **activate-user-profile** () | 立即激活 **用户配置文件** 条目。 |

## WEB接口

每个用户都可以使用 WEB 界面访问他的个人资料。 WEB界面可以通过在路由器的IP或域中添加“/um/”目录来访问，例如[http://example.com/um/](http://router.ip/um/)。 请注意，WEB 界面受 IP 服务“www”和“www-ssl”的影响。 可以使用 CSS、JavaScript 和 HTML 自定义 WEB 界面。

**可定制的文件参考**

| 文件                            | 说明                                       |
| ------------------------------- | ------------------------------------------ |
| **css/login.css**               | 用于登录页面的级联样式表文件。             |
| **css/user.css**                | 用户个人资料页面中使用的级联样式表文件。   |
| **img/PayPal\_mark\_37x23.gif** | PayPal 标志图                              |
| **img/ajax-loader.gif**         | 在处理页面切换时加载 gif。                 |
| **img/mikrotik\_logo.png**      | MikroTik 标志显示在所有页面上。            |
| **js/generic.js**               | 所有页面上使用的 Javascript 文件。         |
| **js/login.js**                 | 登录页面中使用的 Javascript 文件。         |
| **js/user.js**                  | 用户个人资料页面中使用的 Javascript 文件。 |
| **user/login\_dynamic.html**    | 登录页面的布局。                           |
| **user/user\_dynamic.html**     | 用户个人资料页面的布局。                   |

## 应用指南

### 批量创建用户

可以使用随机生成的用户名和密码创建多个新用户。 例如，以下命令将生成 3 个新用户，用户名为 6 个小写符号，密码为 6 个小写、大写和数字。

```shell
/user-manager user
add-batch-users number-of-users=3 password-characters=lowercase,numbers,uppercase password-length=6 username-characters=lowercase username-length=6

```

命令生成的用户可以通过打印用户表看到：

```shell
/user-manager user print
Flags: X - disabled
0   name="olsgkl" password="86a6zH" otp-secret="" group=default shared-users=1 attributes=""
1   name="lkbwss" password="jaKY5V" otp-secret="" group=default shared-users=1 attributes=""
2   name="cwxbwu" password="a62yZd" otp-secret="" group=default shared-users=1 attributes=""

```

### 为 NAS 提供自定义 RADIUS 属性

可以在身份验证过程中发送额外的 RADIUS 属性，以向 NAS 提供有关会话的自定义信息，例如应将哪个 IP 地址分配给请求者或将哪个地址池用于地址分配。

#### 用户的静态IP地址

要为最终用户分配静态 IP 地址，可以使用 _Framed-IP-Address_ 属性。 使用静态 IP 地址分配时，_shared-sessions_ 必须设置为 1，以防止用户有多个同时会话但只有一个 IP 地址的情况。 例如：

```shell
/user-manager user
set [find name=username] shared-users=1 attributes=Framed-IP-Address:192.168.1.4

```

#### 为用户组指定地址池

我们可以将多个相似的用户分组，并同时为所有这些用户分配 RADIUS 属性。 首先，创建一个新组：

```shell
/user-manager user group
add name=location1 outer-auths=chap,eap-mschap2,eap-peap,eap-tls,eap-ttls,mschap1,mschap2,pap \
inner-auths=peap-mschap2,ttls-chap,ttls-mschap1,ttls-mschap2,ttls-pap attributes=Framed-Pool:pool1

```

下一步是将用户分配给该组：

```shell
/user-manager user
 set [find name=username] group=location1

```

在这种情况下，来自 _pool1_ 的 IP 地址将在身份验证时分配给用户 - 确保 _pool1_ 是在 NAS 设备上创建的。

### 使用 TOTP（基于时间的一次性密码）进行用户身份验证

用户管理器支持将基于时间的身份验证令牌添加到每 30 秒重新生成一次的用户密码字段。

OTP 取决于时钟，因此请确保正确配置时间设置。

TOTP 的工作原理是在请求者（客户端）和身份验证服务器（用户管理器）上共享一个秘密。 要在 RouterOS 上配置 TOTP，只需为用户设置 _otp-secret_。 例如：

```shell
/user-manager user
set [find name=username] password=mypass otp-secret=mysecret

```

要在请求方计算 TOTP 令牌，可以使用许多广泛可用的应用程序，例如 Google Authenticator 或 [https://totp.app/](https://totp.app/)。 将 _mysecret_ 添加到 TOTP 令牌生成器将提供一个新的唯一 6 位代码，必须将其添加到用户密码中。

![](https://help.mikrotik.com/docs/download/attachments/2555940/TOTP_generator.PNG?version=1&modificationDate=1657111279930&api=v2)

以下示例将接受用户的身份验证，并将计算出的 TOTP 令牌添加到通用密码中，直到生成新的 TOTP 令牌为止，例如，

```
User-Name=username
User-Password=mypass620872

```

### 导出用户凭据

#### 单个用户的可打印登录凭据

要生成单个用户的可打印凭证卡，只需使用 _generate-voucher_ 命令即可。 指定用户的 RouterOS ID 号或使用 _find_ 命令指定用户名。 模板已包含在用户管理器的安装中，可在设备的“文件”部分找到。 你可以根据需要自定义模板。

```shell
/user-manager user
generate-voucher voucher-template=printable_vouchers.html [find where name=username]

```

通过使用 WEB 浏览器访问路由器的 _/um/PRIVATE/GENERATED/vouchers/gen\_printable\_vouchers.html_ 可获得生成的优惠券卡

默认情况下，可打印卡片如下所示：

![](https://help.mikrotik.com/docs/download/attachments/2555940/image.png?version=1&modificationDate=1663149747172&api=v2)

要通过WEB浏览器访问/um/目录的PRIVATE路径，必须配置_private-username_和_private-password_。 请参阅**设置**部分。

生成凭证时可以使用不同的变量。 目前支持的变量有：

\$(username) - Represents User Manager username  
\$(password) - Password of the username  
\$(userprofname) - Profile that is active for the particular user  
\$(userprofendtime) - Profile validity end time if specified

#### 多用户凭证导出

通过使用 _export.xml_ 或 _export.csv_ 作为 _voucher-template_，可以一次生成包含多个或所有用户凭据的 CSV 或 XML 文件。

```shell
/user-manager user
generate-voucher voucher-template=export.xml [find]

```

该命令生成一个 XML 文件 _um5files/PRIVATE/GENERATED/vouchers/gen\_export.xml_ 可以通过 WEB 浏览器或任何其他文件访问工具访问。

```html
<?xml version="1.0" encoding="UTF-8"?>
<users>
    <user>
        <username>olsgkl</username>
        <password>86a6zH</password>
    </user>
    <user>
        <username>lkbwss</username>
        <password>jaKY5V</password>
    </user>
    <user>
        <username>cwxbwu</username>
        <password>a62yZd</password>
    </user>
    <user>
        <username>username</username>
        <password>secretpassword</password>
    </user>
 
</users>

```

### 生成使用报告

如果公司账单或法律团队需要可呈现的网络使用信息，则可以使用 _generate-report_ 命令创建自动会话导出。 该命令需要输入报告模板 - _um5files/PRIVATE/TEMPLATES/reports/report\_default.html_ 中提供了模板示例。 报告生成示例：

```shell
/user-manager
generate-report report-template=report_default.html columns=username,uptime,download,upload

```

通过使用 WEB 浏览器访问路由器的 _/um/PRIVATE/GENERATED/reports/gen\_report\_default.html_ 可获得生成的报告

_![](https://help.mikrotik.com/docs/download/attachments/2555940/Capture.PNG?version=2&modificationDate=1657102682105&api=v2)_

### 购买配置文件

通过使用 WEB 浏览器访问路由器的 _/um/_ 目录登录到用户的私人配置文件后，例如 [http://example.com/um/,](http://example.com/um/,) 他 将能够在各自的菜单中看到所有可用的**配置文件**。 已指定 _price_ 值的配置文件将具有可用的_购买此配置文件_按钮。

![](https://help.mikrotik.com/docs/download/attachments/2555940/buy_profile.PNG?version=1&modificationDate=1657107133572&api=v2)

按下_购买此配置文件_按钮后，用户将被要求从可用的交易服务提供商中进行选择（目前只有 PayPal 可用），随后将被重定向到 PayPal 的付款处理页面。

![](https://help.mikrotik.com/docs/download/attachments/2555940/paypal_purchase.PNG?version=1&modificationDate=1657107263155&api=v2)

付款完成后，用户经理会要求 PayPal 批准交易。 批准后，配置文件将分配给用户使用。！[](https://help.mikrotik.com/docs/download/attachments/2555940/purchase_complete.PNG?version=1&modificationDate=1657107833111&api=v2)

### 从RouterOS v6 迁移

## 应用实例

### 具有用户管理器身份验证的基本 L2TP/IPsec 服务器

![](https://help.mikrotik.com/docs/download/attachments/2555940/scheme.jpg?version=1&modificationDate=1657282433977&api=v2)

**用户管理器配置**

首先启用用户管理器功能。

```shell
/user-manager
set enabled=yes

```

允许从本地主机（路由器本身）接收 RADIUS 请求。

```shell
/user-manager router
add address=127.0.0.1 comment=localhost name=local shared-secret=test

```

接下来，添加用户及其凭据，客户端将使用这些凭据向服务器进行身份验证。

```shell
/user-manager user
add name=user1 password=password

```

**配置 RADIUS 客户端**

对于使用 RADIUS 服务器进行用户身份验证的路由器，需要添加一个新的 RADIUS 客户端，该客户端具有我们已经在用户管理器上配置的相同共享密钥。

```shell
/radius
add address=127.0.0.1 secret=test service=ipsec

```

**L2TP/IPsec 服务器配置**

配置要分配给用户的 IP 池，并将其分配给 PPP 配置文件。

```shell
/ip pool
add name=vpn-pool range=192.168.99.2-192.168.99.100
 
/ppp profile
set default-encryption local-address=192.168.99.1 remote-address=vpn-pool

```

允许使用 RADIUS 进行 PPP 身份验证。

```shell
/ppp aaa
set use-radius=yes

```

使用 IPsec 加密启用 L2TP 服务器。

```shell
/interface l2tp-server server
set enabled=yes use-ipsec=required ipsec-secret=mySecret

```

这样就对了。 路由器现在已准备好接受 L2TP/IPsec 连接并向内部用户管理器验证它们
