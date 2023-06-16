## 介绍

域名系统（DNS）通常是指互联网的电话簿。换句话说，DNS是一个数据库，它将字符串（称为主机名），如 [www.mikrotik.com](https://www.google.com) 链接到一个特定的IP地址，如159.148.147.196。

启用了DNS功能的MikroTik路由器可以设置为任何符合DNS的客户端的DNS缓存。此外，MikroTik路由器可以在其DHCP服务器设置下被指定为一个主要的DNS服务器。当远程请求被启用时，MikroTik路由器会在53端口响应TCP和UDP的DNS请求。

当静态和动态服务器都被设置时，静态服务器条目会被优先考虑，然而，这并不表明静态服务器会一直被使用（例如，之前收到来自动态服务器的查询，但后来添加了静态服务器，那么动态条目会被优先考虑）。

当DNS服务器 _allow-remote-requests_ 被使用时，确保限制通过TCP和UDP协议端口53访问服务器，只针对已知的主机。

关于如何管理局域网上的DNS功能，有几种选择--使用公共DNS，使用路由器作为缓存，或者不干涉DNS配置。让我们以下面的设置为例： 互联网服务提供商（ISP）→网关（GW）→局域网（LAN）。网关是基于RouterOS的设备，具有默认配置：

- 不在 "GW "的DHCP服务器网络配置上配置任何DNS服务器-设备将把从 "ISP "收到的DNS服务器IP地址配置转发给 "LAN "设备；
- 在 "GW "DHCP服务器网络配置上配置DNS服务器--设备将把配置的DNS服务器给"LAN "设备（还必须启用"/ip dns set allow-remote-requests=yes" ）；
- 在 "GW "DHCP服务器网络配置下配置的 "dns-none"-设备不会将任何 **动态** 的DNS服务器转发给"LAN "设备；

## DNS配置

DNS设施用于为路由器本身以及连接到它的客户提供域名解析。

| 属性                                                               | 说明                                                                                                                  |
| ------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------- |
| **allow-remote-requests** (_yes_ \| _no_; Default: **no**)                                                                                                | 指定是否允许路由器作为远程客户端的DNS缓存使用。否则只有路由器本身会使用DNS配置。 |
| **cache-max-ttl** (_time_; Default: **1w**)                         | 缓存记录的最长生存时间。换句话说，缓存记录将在cache-max-TTL时间后无条件过期。从DNS服务器收到的较短的TTL会被尊重。     |
| **cache-size** (_integer[64..4294967295]_; Default: **2048**)      | 指定DNS缓存的大小，KiB。                                                                                              |
| **max-current-queries** (_integer_; Default: **100**)              | 指定允许多少个并发的查询。                                                                                            |
| **max-concurrent-tcp-sessions** (_integer_; Default: **20**)       | 指定允许多少个并发的TCP会话。                                                                                         |
| **max-udp-packet-size** (_integer [50..65507]_; Default: **4096**) | 允许UDP数据包的最大尺寸。                                                                                             |
| **query-server-timeout** (_time_; Default: **2s**)                 | 指定等待服务器的查询响应的时间。                                                                                      |
| **query-total-timeout** (_time_; Default: **10s**)                 | 指定等待查询响应的总时间。注意，这个设置必须考虑到 "查询服务器超时 "和使用的DNS服务器的数量。                         |
| **servers** (_list of IPv4/IPv6 addresses_; Default: )             | DNS服务器的IPv4/IPv6地址列表。                                                                                        |
| **cache-used** (_integer_)                                         | 显示当前使用的缓存大小（KiB）。                                                                                       |
| **dynamic-server** (_IPv4/IPv6 list_)                              | 来自不同服务的动态添加的DNS服务器列表，例如DHCP。                                                                     |
| **doh-max-concurrent-queries** (_integer_; Default: **50**)        | 指定允许多少个DoH并发查询。                                                                                           |
| **doh-max-server-connections** (_integer_; Default: **5**)         | 指定允许多少个与DoH服务器的并发连接。                                                                                 |
| **doh-timeout** (_time_; Default: **5s**)                          | 指定等待DoH服务器的查询响应的时间。                                                                                   |
| **use-doh-server** (_string; Default: )_                           | 指定必须使用哪个DoH服务器进行DNS查询。如果指定了DoH功能，将覆盖"servers"的使用。服务器必须以 "https://"为前缀来指定。 |
| **verify-doh-cert**  (_yes_ \| _no_; Default: **no**)              | 指定是否验证DoH服务器，如果使用的是DoH服务器，则使用"/certificate "列表验证服务器的有效性。                           |


```shell
[admin@MikroTik] > ip dns print        
                      servers:
              dynamic-servers: 10.155.0.1
               use-doh-server:
              verify-doh-cert: no
   doh-max-server-connections: 5
   doh-max-concurrent-queries: 50
                  doh-timeout: 5s
        allow-remote-requests: yes
          max-udp-packet-size: 4096
         query-server-timeout: 2s
          query-total-timeout: 10s
       max-concurrent-queries: 100
  max-concurrent-tcp-sessions: 20
                   cache-size: 2048KiB
                cache-max-ttl: 1d
                   cache-used: 48KiB
```

动态DNS服务器是通过RouterOS中的不同设施获得的，例如，DHCP客户端、VPN客户端、IPv6路由器通告等。

## DNS缓存

这个菜单提供了两个存储在服务器上的DNS记录的列表：

- "/ip dns cache"：这个菜单提供了一个带有缓存DNS条目的列表，RouterOS缓存可以回复客户端的请求；
- "/ip dns cache all"： 这个菜单提供了一个完整的列表，包括所有存储的缓存DNS记录，例如，PTR记录。

可以用命令清空DNS缓存： "/ip dns cache flush"。

## 静态DNS

MikroTik RouterOS的DNS缓存有一个额外的嵌入式DNS服务器功能，允许配置多种类型的DNS条目，可以被使用路由器作为DNS服务器的DNS客户使用。这个功能也可以用来向网络客户提供虚假的DNS信息。例如，将某一组域（或整个互联网）的任何DNS请求解析到自己的页面。

`[admin@MikroTik] /ip dns static add namewww.mikrotik.com address=10.0.0.1`

服务器也能够根据POSIX基本正则表达式来解析DNS请求，因此多个请求可以与同一个条目匹配。在条目不符合DNS命名标准的情况下，它被认为是一个正则表达式。列表被排序，并从上到下检查。首先检查正则表达式，然后是普通记录。

使用regex来匹配DNS请求：

`[admin@MikroTik] /ip dns static add regexp="[*mikrotik*]" address=10.0.0.2`

如果DNS静态条目列表与请求的域名相匹配，那么路由器将认为该路由器负责该特定名称的任何类型的DNS请求。例如，如果列表中只有一个 "A "记录，但路由器收到一个 "AAAA "请求，那么它将从静态列表中回复一个 "A "记录，并将查询上游服务器的 "AAAA "记录。如果有记录存在，那么回复将被转发，如果没有，那么路由器将回复一个没有任何记录的 "ok "DNS回复。如果想用不可用的记录覆盖来自上游服务器的域名记录，那么可以为特定的域名添加一个静态条目，并为它指定一个假的IPv6地址":fff"。

将所有配置的DNS条目作为一个有序的列表列出：

```shell
[admin@MikroTik] /ip/dns/static/print
Columns: NAME, REGEXP, ADDRESS, TTL
# NAME             REGEXP       ADDRESS   TTL
0 www.mikrotik.com               10.0.0.1  1d
1                  [*mikrotik*]  10.0.0.2  1d
```

| 属性                                                                                                        | 说明                                                                           |
| ----------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| **address** (_IPv4/IPv6_)                                                                                   | 用于 "A "或 "AAAA "类型记录的地址。                                            |
| **cname** (_string_)                                                                                        | 一个域名的别名。                                                               |
| **forward-to**                                                                                              | 域名服务器的IP地址，特定的DNS请求必须被转发到该服务器。                        |
| **mx-exchange** (_string_)                                                                                  | MX服务器的域名。                                                               |
| **name** (_string)_                                                                                         | 域名。                                                                         |
| **srv-port** (_integer_; Default: 0)                                                                        | 查找服务的TCP或UDP端口。                                                       |
| **srv-target**                                                                                              | 提供服务的机器的标准主机名，以点结束。                                         |
| **text** (_string_)                                                                                         | 域名的文本信息。                                                               |
| **type** (_A_ \| _AAAA_ \| _CNAME_ \| _FWD_ \| _MX_ \| _NS_ \| _NXDOMAIN_ \| _SRV_ \| _TXT_ ; Default: _A_) | DNS记录类型                                                                    |
| **address-list** (_string_)                                                                                 | 防火墙地址列表的名称，当某些请求与该条目匹配时，必须将地址动态添加到该列表中。 |
| **comment** (_string_)                                                                                      | 关于域名记录的评论。                                                           |
| **disabled** (_yes_ \| _no_; Default: yes)                                                                  | 域名记录是否激活。                                                             |
| **match-subdomain** (_yes_ \| _no_; Default: no)                                                            | 该记录是否会匹配子域的请求。                                                   |
| **mx-preference** (_integer_; Default: 0)                                                                   | 特定MX记录的偏好。                                                             |
| **ns** (_string_)                                                                                           | 特定记录的权威域名服务器的名称。                                               |
| **regexp** (POSIX regex)                                                                                    | 正则表达式，应根据它来验证域名。                                               |
| **srv-priority** (_integer_; Default: 0)                                                                    | 特定SRV记录的优先级。                                                          |
| **src-weight** (_integer_; Default: 0)                                                                      | 特定SRC记录的重量。                                                            |
| **ttl** (_time_; Default: _24h_)                                                                            | 缓存记录的最长生存时间。                                                       |

Regexp是区分大小写的，但是DNS请求不区分大小写，RouterOS在匹配任何静态条目之前会将DNS名称转换为小写。应该用小写字母来编写regex。正则表达式匹配的速度明显比纯文本慢，所以建议尽量减少正则表达式规则的数量，并优化表达式本身。

当通过混合用户界面CLI和GUI配置regex时要小心。从CLI添加条目时，条目本身可能需要转义字符。建议添加一个条目并执行打印命令，以验证在添加过程中没有改变regex。

# DNS over HTTPS (DoH)

从RouterOS v6.47版本开始，可以使用HTTPS的DNS（DoH）。DoH使用HTTPS协议来发送和接收DNS请求，以提高数据的完整性。其主要目的是通过消除 "中间人 "攻击（MITM）来提供隐私。目前，DoH与FWD型静态条目不兼容，为了利用FWD条目，必须不配置DoH。   
  
请观看 [关于此功能的视频](https://youtu.be/w4erB0VzyIE)。 

强烈建议导入你选择使用的DoH服务器的根CA证书以提高安全性。我们强烈建议不要使用第三方的下载链接来获取证书。使用证书颁发机构自己的网站。

有多种方法可以找出所需的根 CA 证书。最简单的方法是使用WEB浏览器导航到DoH网站并检查网站的安全性。例如，使用Firefox可以看到Cloudflare DoH服务器使用的是DigiCert全球根CA。可以直接从浏览器中下载证书，或者导航到DigiCert网站，从一个受信任的来源获取证书。 

![](https://help.mikrotik.com/docs/download/attachments/37748767/Rootca.PNG?version=1&modificationDate=1628148171413&api=v2)

下载证书，将其上传到你的路由器，然后导入： 

`/certificate import file-name=DigiCertGlobalRootCA.crt.pem`

配置DoH服务器： 

`/ip dns set use-doh-server=https://cloudflare-dns.com/dns-query verify-doh-cert=yes`

请注意，至少要为路由器配置一个常规的DNS服务器来解析DoH主机名本身。如果没有配置任何动态或静态的DNS服务器，要为DoH服务器域名添加一个静态DNS条目，像这样： 

`/ip dns set servers=1.1.1.1`

如果设备上同时配置了DoH和DNS服务器，RouterOS会优先考虑DoH。