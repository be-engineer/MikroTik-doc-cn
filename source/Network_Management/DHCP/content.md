## 摘要

`/ip dhcp-client'

DHCP（动态主机配置协议）是用来在网络中轻松分配IP地址的。MikroTik RouterOS的实现包括服务器和客户端两部分，并且符合RFC 2131的规定。

MikroTik RouterOS的DHCP客户端可以在任何类似以太网的接口上一次启用。该客户端将接受一个地址、网络掩码、默认网关和两个DNS服务器地址。收到的IP地址将被添加到带有各自净掩码的接口上。默认网关将作为一个动态条目添加到路由表中。如果DHCP客户端被禁用或不更新地址，动态默认路由将被删除。如果在DHCP客户端获得默认路由之前已经安装了一个默认路由，DHCP客户端获得的路由将被显示为无效。

RouterOS DHCP客户端要求提供以下选项：

- 选项1 - SUBNET_MASK
- 选项3 - GATEWAY_LIST
- 选项6 - TAG_DNS_LIST
- 选项33 - STATIC_ROUTE
- 选项42 - NTP_LIST
- 选项121 - CLASSLESS_ROUTE

## DHCP选项

DHCP客户端有可能设置发送给DHCP服务器的选项。例如，主机名和MAC地址。其语法与DHCP服务器选项相同。

目前，有三个变量可以在选项中使用：

- HOSTNAME；
- CLIENT_MAC - 客户端接口MAC地址；
- CLIENT_DUID - 路由器的客户DIUD，与用于DHCPv6客户的相同。按照RFC4361的规定

DHCP客户端默认选项包括这些默认选项：

| 名称          | 代码 | 值                 |
| ------------- | ---- | ------------------ |
| clientid_duid | 61   | 0xff$(CLIENT_DUID) |
| clientid      | 61   | 0x01$(CLIENT_MAC)  |
| hostname      | 12   | $(HOSTNAME)        |

## 属性

| 属性                                                                       | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **add-default-route** (_yes \| no \| special-classless_; Default: **yes**) | 是否在从DHCP服务器收到的路由表中安装默认路由。默认情况下，如果收到无类选项121，RouterOS客户端会遵守RFC的规定，忽略选项3。要强制客户端不忽略选项3，请设置_special-classless_。这个参数在v6rc12+中可用。<br>- **yes** - 如果收到无类路由，则添加无类路由，如果没有，则添加默认路由（旧行为）。<br>- **special-classless** - 如果收到无类路由，则同时添加无类路由和默认路由（MS风格）。                                                                                                                                                 |
| **client-id** (_string_; Default: )                                        | 对于网络管理员或ISP建议的设置。如果不指定，将发送客户的MAC地址。                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| **comment** (_string_; Default: )                                          | 客户端的简短描述。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| **default-route-distance** (_integer:0..255_; Default: )                   | 默认路由的距离。如果 `add-default-route` 设置为“yes”，则适用。                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| **disabled** (_yes \| no_; Default: **yes**)                               |
|                                                                            |
| **host-name** (_string_; Default: )                                        | 客户端的主机名会被发送到DHCP服务器。如果不指定，将使用客户端的系统标识。                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| **interface** (_string_; Default: )                                        | DHCP客户端将在哪个接口上运行。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| **script** (_script_; Default: )                                           | 当DHCP客户端获得一个新的租约或失去一个现有的租约时执行脚本。这个参数在v6.39rc33+中可用，这些是事件脚本可以访问的可用变量：<br>- bound - 1 - 租赁被添加/改变；0 - 租赁被删除<br>- server-address - 服务器地址<br>- lease-address - 由服务器提供的租赁地址<br>- interface - 客户端所配置的接口的名称<br>- gateway-address - 由服务器提供的网关地址<br>- vendor-specific - 存储从DHCP服务器收到的选项43的值<br>- lease-options - 一个接收到的选项数组的 [实例](https://help.mikrotik.com/docs/display/ROS/DHCP#DHCP-LeaseScriptExample) |
| **use-peer-dns** (_yes \| no_; Default: **yes**)                           | 是否接受由 [DHCP服务器](https://help.mikrotik.com/docs/display/ROS/DHCP#DHCP-DHCPServer) 公布的 [DNS](https://help.mikrotik.com/docs/display/ROS/DNS) 设置。会覆盖"/ip dns "子菜单中的设置。                                                                                                                                                                                                                                                                                                                                         |
| **use-peer-ntp** (_yes \| no_; Default: **yes**)                           | 是否接受由 [DHCP服务器](https://help.mikrotik.com/docs/display/ROS/DHCP#DHCP-DHCPServer) 公布的 [NTP](https://wiki.mikrotik.com/wiki/Manual:System/Time#NTP_client_and_server "Manual:System/Time") 设置。(会覆盖在"/system ntp client "子菜单中的设置)                                                                                                                                                                                                                                                                              |

**只读属性**

| 属性                                                                                      | 说明                                             |
| ----------------------------------------------------------------------------------------- | ------------------------------------------------ |
| **address** (_IP/Netmask_)                                                                | IP地址和网络掩码，是由服务器分配给DHCP客户端的。 |
| **dhcp-server** (_IP_)                                                                    | DHCP服务器的IP地址。                             |
| **expires-after** (_time_)                                                                | 租约过期的时间（由DHCP服务器指定）。             |
| **gateway** (_IP_)                                                                        | 由DHCP服务器分配的网关的IP地址。                 |
| **invalid** (_yes \| no_)                                                                 | 显示一个配置是否无效。                           |
| **netmask** (_IP_)                                                                        |                                                  |
| **primary-dns** (_IP_)                                                                    | 第一个DNS解析器的IP地址，由DHCP服务器分配。      |
| **primary-ntp** (_IP_)                                                                    | 第一台NTP服务器的IP地址，由DHCP服务器分配。      |
| **secondary-dns** (_IP_)                                                                  | 第二个DNS解析器的IP地址，由DHCP服务器分配。      |
| **secondary-ntp** (_IP_)                                                                  | 第二台NTP服务器的IP地址，由DHCP服务器分配。      |
| **status** (_bound \| error \| rebinding... \| requesting... \| searching... \| stopped_) | 显示DHCP客户端的状态。                           |


**Menu specific commands**

| 属性                    | 说明                                                                                                                     |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| **release** (_numbers_) | 释放当前的绑定，并重新启动DHCP客户端。                                                                                   |
| **renew** (_numbers_)   | 更新当前租约。如果更新操作不成功，客户端会尝试重新初始化租约（即开始租约请求程序（重新绑定），就像没有收到IP地址一样）。 |

## 配置实例

### 简单的 DHCP 客户端

在 ether1 接口上添加一个 DHCP 客户端：

`/ip dhcp-client add interface=ether1 disabled=no`

在接口添加后，可以用 "print"或 "print detail"命令来查看DHCP客户端获得了哪些参数：

```shell
[admin@MikroTik] ip dhcp-client> print detail
Flags: X - disabled, I - invalid
 0   interface=ether1 add-default-route=yes use-peer-dns=yes use-peer-ntp=yes
     status=bound address=192.168.0.65/24 gateway=192.168.0.1
     dhcp-server=192.168.0.1 primary-dns=192.168.0.1 primary-ntp=192.168.0.1
     expires-after=9m44s
[admin@MikroTik] ip dhcp-client>
```

如果DHCP客户端使用的接口是VRF配置的一部分，那么默认路由和其他从DHCP服务器接收的路由将被添加到VRF路由表。

可以用以下方法检查DHCP客户端的状态：

`/ip dhcp-client print detail`

### 租约脚本示例

当一个DHCP客户获得一个新的租约或失去一个现有的租约时，可以执行一个脚本。这是一个脚本的例子，它自动添加一个带有routing-mark=WAN1的默认路由，并在租约到期或被删除时将其删除。

```shell
/ip dhcp-client
add add-default-route=no dhcp-options=hostname,clientid disabled=no interface=ether2 script="{\r\
    \n    :local rmark \"WAN1\"\r\
    \n    :local count [/ip route print count-only where comment=\"WAN1\"]\r\
    \n    :if (\$bound=1) do={\r\
    \n        :if (\$count = 0) do={\r\
    \n            /ip route add gateway=\$\"gateway-address\" comment=\"WAN1\" routing-mark=\$rmark\r\
    \n        } else={\r\
    \n            :if (\$count = 1) do={\r\
    \n                :local test [/ip route find where comment=\"WAN1\"]\r\
    \n                :if ([/ip route get \$test gateway] != \$\"gateway-address\") do={\r\
    \n                    /ip route set \$test gateway=\$\"gateway-address\"\r\
    \n                }\r\
    \n            } else={\r\
    \n                :error \"Multiple routes found\"\r\
    \n            }\r\
    \n        }\r\
    \n    } else={\r\
    \n        /ip route remove [find comment=\"WAN1\"]\r\
    \n    }\r\
    \n}\r\
    \n"
```

### 当路由器（选项3）来自不同的子网时，解决默认网关问题

在某些情况下，管理员倾向于设置路由器选项，而该选项不能与所提供的IP的子网一起解决。例如，DHCP服务器向客户提供192.168.88.100/24，而选项3被设置为172.16.1.1。会导致一个未解决的默认路由：

```shell
#      DST-ADDRESS        PREF-SRC        GATEWAY            DISTANCE
0  DS  0.0.0.0/0                          172.16.1.1              1
1 ADC  192.168.88.0/24    192.168.88.100  ether1
```

为了解决这个问题，需要添加/32路由来解决ether1上的网关，可以通过在DHCP客户端每次获得地址时运行以下脚本来完成

```shell
/system script add name="dhcpL" source={ /ip address add address=($"lease-address" . "/32") network=$"gateway-address" interface=$interface }
```

现在可以进一步扩展这个脚本，检查地址是否已经存在，如果需要修改，就删除旧的地址

```shell
/system script add name="dhcpL" source={
  /ip address {
    :local ipId [find where comment="dhcpL address"]
    :if ($ipId != "") do={
      :if (!([get $ipId address] = ($"lease-address" . "/32") && [get $ipId network]=$"gateway-address" )) do={
        remove $ipId;
        add address=($"lease-address" . "/32") network=$"gateway-address" \
          interface=$interface comment="dhcpL address"
      }
    } else={
      add address=($"lease-address" . "/32") network=$"gateway-address" \
        interface=$interface comment="dhcpL address"
    }
  }
}
```

# DHCPv6客户端

## 摘要

**Sub-menu:** `/ipv6 dhcp-client`

RouterOS中的DHCP-client可以成为DHCPv6-client和DHCP-PD客户端。它能够从DHCP-PD服务器获得前缀，也能从DHCPv6服务器获得DHCPv6状态地址。

## 属性

| 属性                                                | 说明                                                                                                                                                                                                                                                                  |
| --------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **add-default-route** (_yes\| no_; Default: **no**) | 客户端连接后是否添加默认的IPv6路由。                                                                                                                                                                                                                                  |
| **comment** (_string_; Default: )                   | 客户端的简短描述                                                                                                                                                                                                                                                      |
| **disabled** (_yes\| no_; Default: **no**)          |                                                                                                                                                                                                                                                                       |
| **interface** (_string_; Default: )                 | DHCPv6客户端将运行的接口。                                                                                                                                                                                                                                            |
| **pool-name** (_string_; Default: )                 | [IPv6 pool](https://wiki.mikrotik.com/wiki/Manual:IPv6/Pool "Manual:IPv6/Pool")的名称，收到的IPv6前缀将被加入其中。                                                                                                                                                   |
| **pool-prefix-length** (_string_; Default: )        | 为 [IPv6 pool](https://wiki.mikrotik.com/wiki/Manual:IPv6/Pool "Manual:IPv6/Pool") 设置的前缀长度参数，接收的IPv6前缀将被添加到其中。前缀长度必须大于接收的前缀长度，否则，前缀长度将被设置为接收的前缀长度+8位。                                                     |
| **prefix-hint** (_string_; Default: )               | 包括一个首选的前缀长度。                                                                                                                                                                                                                                              |
| **request** (_prefix, address_; Default: )          | 选择DHCPv6请求是询问地址还是IPv6前缀，或者两者都询问。                                                                                                                                                                                                                |
| **script** (_string_; Default: )                    | 在DHCP-客户端状态改变时运行这个脚本。可用的变量：<br>- pd-valid 如果客户端获得了前缀；<br>- pd-prefix 客户端获得的前缀，如果有的话；<br>- na-valid 如果地址是由客户获得的；<br>- na-address 客户端获得的地址，如果有的话；<br>- options 接收选项的数组（只有ROSv7）。 |
| **use-peer-dns** (_yes \| no_; Default: **yes**)    | 是否接受由IPv6 DHCP服务器公布的DNS设置。                                                                                                                                                                                                                              |

**只读属性**

| 属性                                                                                                            | 说明                                                                                                                                                                                                                                                                                                                                                                                            |
| --------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **duid** (_string_)                                                                                             | 自动生成的DUID发送到服务器。DUID是使用路由器上可用的MAC地址之一生成的。                                                                                                                                                                                                                                                                                                                         |
| **request** (_list_)                                                                                            | 指定请求的内容 - 前缀，地址，或两者。                                                                                                                                                                                                                                                                                                                                                           |
| **dynamic** (_yes \| no_)                                                                                       |                                                                                                                                                                                                                                                                                                                                                                                                 |
| **expires-after* (_time_)                                                                                       | IPv6前缀过期的时间（由DHCPv6服务器指定）。                                                                                                                                                                                                                                                                                                                                                      |
| **invalid** (_yes \| no_)                                                                                       | 显示配置是否无效。                                                                                                                                                                                                                                                                                                                                                                              |
| **prefix** (_IPv6 prefix_)                                                                                      | 显示从DHCPv6-PD服务器收到的IPv6前缀。                                                                                                                                                                                                                                                                                                                                                           |
| **status** (_stopped       \| searching\| requesting...\| bound \| renewing \| rebinding \| error \| stopping_) | 显示DHCPv6客户端的状态： <br>- **stopped** dhcpv6 客户端已停止。<br>- **searching** 发送 "征求 "并试图获得 "广告"。<br>- **requesting** 发送 "request"，等待 "reply"。<br>- **bound** 收到 "回复"。分配的前缀。<br>- **renewing** 发送 "续订"，等待 "回复"。<br>- **rebinding** 发送了 "rebind"，等待 "reply"。<br>- **error** 没有及时收到回复或发生其他错误。<br>- **stopping** 发送 "释放"。 |

**菜单的具体命令**

| 属性                    | 说明                                                                                                                               |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| **release** (_numbers_) | 释放当前的绑定并重新启动DHCPv6客户端。                                                                                             |
| **renew** (_numbers_)   | 更新当前租约。如果更新操作不成功，客户端会尝试重新初始化租约（也就是说，它启动租约请求程序（重新绑定），就像还没有收到IP地址一样） |

## 脚本

可以添加一个脚本，当一个前缀或地址被获取并应用，或过期并被删除时，使用DHCP客户端执行。有几组分开的变量，它们的值由客户端根据前缀或地址状态的变化来设置，因为客户端可以获取这两种东西，而且每一种都会对路由器配置产生不同的影响。

dhcp-client的可用变量

- pd-valid值 - 1或0 - 如果前缀被获取并应用或不应用
- pd-prefix值ipv6/num (带掩码的ipv6前缀) - 前缀本身
- na-valid值 - 1或0 - 如果地址被获取并且被应用或不被应用
- na-address值 - ipv6地址 - 地址

## IAID

为了确定使用什么IAID，将DHCP客户端运行的接口的内部ID从十六进制转换为十进制。

例如，DHCP客户端运行在PPPoE-out1接口上。要获得内部ID，请使用以下命令：

`[admin@t36] /interface> :put [find name="pppoe-out1"] *15`


现在将十六进制值15转换为十进制，会得到IAID=21

## 配置实例

### 简单的DHCPv6客户端

这个简单的例子演示了如何使DHCP客户端接收IPv6前缀并将其加入池中。

`/ipv6 dhcp-client add request=prefix pool-name=test-ipv6 pool-prefix-length=64 interface=ether13`

  
详细打印应显示客户的状态，可以验证是否收到前缀。

```shell
[admin@x86-test] /ipv6 dhcp-client> print detail
Flags: D - dynamic, X - disabled, I - invalid
 0 interface=bypass pool-name="test-ipv6" pool-prefix-length=64 status=bound
prefix=2001:db8:7501:ff04::/62 expires-after=2d23h11m53s request=prefix
```
 

注意，服务器给了前缀 2a02:610:7501:ff04::/62 。应该添加到IPv6池中

```shell
[admin@MikroTik] /ipv6 pool> print
Flags: D - dynamic
# NAME PREFIX REQUEST PREFIX-LENGTH
0 D test-ipv6 2001:db8:7501:ff04::/62 prefix 64
```

成功了! 现在你可以使用这个池子，例如，用于pppoe客户端。

### 使用接收到的前缀作为本地RA

考虑以下设置：

![](https://help.mikrotik.com/docs/download/attachments/24805500/Dhcpv6-pd-example.jpg?version=1&modificationDate=1657264950828&api=v2)

- ISP将前缀2001:DB8::/62路由给路由器R1
- 路由器R1运行DHCPv6服务器，将/64前缀委托给客户路由器CE1 CE2
- 路由器CE1和CE2上的DHCP客户端从DHCP服务器（R1）接收委托的/64前缀。
- 客户路由器使用收到的前缀在本地接口上设置RA。

 
**配置**

  
**R1**

```shell
/ipv6 route
add gateway=fe80::1:1%to-ISP
 
/ipv6 pool
add name=myPool prefix=2001:db8::/62 prefix-length=64
 
/ipv6 dhcp-server
 add address-pool=myPool disabled=no interface=to-CE-routers lease-time=3m name=server1
```
  
**CE1**

```shell
/ipv6 dhcp-client
add interface=to-R1 request=prefix pool-name=my-ipv6
 
/ipv6 address
add address=::1/64 from-pool=my-ipv6 interface=to-clients advertise=yes
```

**CE2**

```shell
/ipv6 dhcp-client
 add interface=to-R1 request=prefix pool-name=my-ipv6
/ipv6 address add address=::1/64 from-pool=my-ipv6 interface=to-clients advertise=yes
```

  
**检查状态**

配置完成后，我们可以验证每个CE路由器是否收到自己的前缀

服务器设置：

```shell
[admin@R1] /ipv6 dhcp-server binding> print
 Flags: X - disabled, D - dynamic
# ADDRESS DUID IAID SERVER STATUS
 1 D 2001:db8:1::/64 0019d1393536 566 server1 bound
2 D 2001:db8:2::/64 0019d1393535 565 server1 bound
```

  

客户端设置:

```shell
[admin@CE1] /ipv6 dhcp-client> print
Flags: D - dynamic, X - disabled, I - invalid
# INTERFACE STATUS REQUEST PREFIX
0 to-R1 bound prefix 2001:db8:1::/64
 
[admin@CE1] /ipv6 dhcp-client> /ipv6 pool print
Flags: D - dynamic
# NAME PREFIX PREFIX-LENGTH
0 D my-ipv6 2001:db8:1::/64 64
```

  

还可以看到IPv6地址自动从前缀池中添加：

```shell
[admin@CE1] /ipv6 address> print
Flags: X - disabled, I - invalid, D - dynamic, G - global, L - link-local
# ADDRESS FROM-POOL INTERFACE ADVERTISE 0 G 2001:db8:1::1/64 to-clients yes
..
```

而池子的使用情况显示，'地址'在分配池子

```shell
[admin@CE1] /ipv6 pool used> print
 POOL PREFIX OWNER INFO
my-ipv6 2001:db8:1::/64 Address to-clients
```

# DHCP服务器

## 摘要

DHCP是用来在网络中轻松分配IP地址的。MikroTik RouterOS的实现包括服务器和客户端两部分，并且符合RFC 2131的规定。

路由器支持每个类似以太网的接口的单独服务器。MikroTik RouterOS DHCP服务器支持给每个请求的客户提供IP地址/网络掩码租约、默认网关、域名、DNS-服务器和WINS-服务器（针对Windows客户）信息的基本功能（在DHCP网络子菜单中设置）。

为了让DHCP服务器工作，还必须配置IP池（不要把DHCP服务器自己的IP地址纳入池子范围）和DHCP网络。

也可以使用RADIUS服务器为DHCP客户发放租约；RADIUS服务器支持的参数如下：

  
访问-请求：

- NAS-Identifier - 路由器身份
- NAS-IP-Address - 路由器本身的IP地址
- NAS-Port - 唯一的会话ID
- NAS-Port-Type--以太网
- Calling-Station-Id - 客户端标识（active-client-id）。
- Framed-IP-Address - 客户端的IP地址(active-address)
- Called-Station-Id - DHCP服务器的名称
- User-Name - 客户端的MAC地址(active-mac-address)
- 密码 - ""

访问-接受：

- Framed-IP-Address - 分配给客户的IP地址
- Framed-Pool - 为客户分配IP地址的IP池。
- Rate-Limit - DHCP客户端的数据速率限制。格式是：rx-rate[/tx-rate] [rx-burst-rate[/tx-burst-rate] [rx-burst-threshold[/tx-burst-threshold] [rx-burst-time[/tx-burst-time][priority] [rx-rate-min[/tx-rate-min]。所有的速率都应该是数字，可以选择'k'（1,000s）或'M'（1,000,000s）。如果没有指定tx-rate，rx-rate也是tx-rate。tx-bulst-rate和tx-bulst-threshold以及tx-bulst-time也是如此。如果没有指定rx-burst-threshold和tx-burst-threshold（但指定了burst-rate），则rx-rate和tx-rate被用作burst阈值。如果没有指定rx-burst-time和tx-burst-time，则使用1s作为默认值。优先级取值为1...8，其中1意味着最高的优先级，而8是最低的。如果没有指定rx-rate-min和tx-rate-min，则使用rx-rate和tx-rate值。rx-rate-min和tx-rate-min值不能超过rx-rate和tx-rate值。
- Ascend-Data-Rate - TX/RX数据速率限制，如果提供多个属性，第一个限制tx数据速率，第二个-RX数据速率。如果与Ascend-Xmit-Rate一起使用，指定RX速率。如果无限制则为0
- Ascend-Xmit-Rate--tx数据速率限制。它可用于只指定TX限制，而不是发送两个连续的Ascend-Data-Rate属性（在这种情况下，Ascend-Data-Rate将指定接收速率）。如果无限制，则为0
- 会话超时--最大租赁时间(lease-time)

DHCP服务器需要一个真实的接口来接收原始以太网数据包。如果该接口是一个网桥接口，那么网桥必须有一个真实的接口作为端口连接到该网桥，以接收原始以太网数据包。它不能在一个假的（空桥）接口上正常工作。

## DHCP服务器属性

| 属性                                                                                                                                  | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **add-arp** (_yes \| no_; Default: **no**)                                                                                            | 是否添加动态ARP条目。如果设置为**no**，则应在该接口上启用ARP模式，或者在 _/ip arp_ 子菜单中管理定义静态ARP条目。                                                                                                                                                                                                                                                                                                                                                                                                         |
| IP地址池** (_string \| static-only_; Default: **static-only**)                                                                        | IP地址池，用于为客户获取IP地址。如果设置为static-only，那么只有拥有静态租约的客户（在租约子菜单中添加）才会被允许。                                                                                                                                                                                                                                                                                                                                                                                                      |
| **allow-dual-stack-queue** (_yes \| no_; Default: **yes*)                                                                             | 为IPv4和IPv6地址创建一个简单的队列条目，并使用MAC地址和DUID进行识别。需要IPv6 DHCP服务器也启用这个选项才能正常工作。                                                                                                                                                                                                                                                                                                                                                                                                     |
| **always-broadcast** (_yes\| no_; Default: **no**)                                                                                    | 始终以广播的形式发送回复，即使目的地IP是已知的。会增加L2网络的额外负载。                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| **authoritative** (_after-10sec-delay \| after-2sec-delay\| yes \| no_; Default: **yes**)                                             | 选项改变了服务器对DHCP请求的响应方式：<br>- yes 回应客户对本服务器不可用的地址的请求，DHCP服务器将发送一个否定的确认（DHCPNAK）；<br>- no DHCP服务器忽略客户对该服务器不可用的地址的请求；<br>- after-10sec-延迟请求 "secs < 10 "将按 "no "设置的情况处理，"secs >= 10 "的请求将按 "yes "的情况处理；<br>- 在 "secs<2 "的情况下，after-2sec-delay请求将按照 "no "的设置进行处理，在 "secs>=2 "的情况下，将按照 "yes "的设置进行处理；<br>如果所有 "secs < x" 的请求都应该被忽略，那么应该使用 "delay-threshold=x" 设置。 |
| **bootp-lease-time** (_forever \| lease-time \| time_; Default: **forever**)                                                          | 接受两个预定义的选项或时间值：<br>- 永久租赁，永不过期<br>- 租赁时间使用租赁时间参数中的时间                                                                                                                                                                                                                                                                                                                                                                                                                             |
| **bootp-support** (_none \| static \| dynamic_; Default: **static**)                                                                  | Support for BOOTP客户：<br>- 没有，不响应BOOTP请求<br>- 静态只向BOOTP客户提供静态租约<br>- 动态为BOOTP客户端提供静态和动态租约                                                                                                                                                                                                                                                                                                                                                                                           |
| **client-mac-limit** (_integer \| unlimited_; Default: **unlimited*)                                                                  | 指定是否限制每个单一MAC地址的特定客户数量或不限制。注意，这个设置不能在中继设置中使用。                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| **conflict-detection** (_yes \| no_; Default: **yes**)                                                                                | 允许禁用/启用冲突检测。如果该选项启用，那么每当服务器试图分配一个租约时，它将发送ICMP和ARP消息来检测网络中是否已经存在这样的地址。如果上述任何一个得到回复的地址被认为已经被使用。                                                                                                                                                                                                                                                                                                                                       |
| **delay-threshold** (_time \| none_; Default: **none**)                                                                               | 如果DHCP数据包中的秒字段小于延迟阈值，那么这个数据包将被忽略。如果设置为**无**，则没有阈值（所有DHCP数据包都被处理）。                                                                                                                                                                                                                                                                                                                                                                                                   |
| **dhcp-option-set** (_name \| none_; Default: **none**)                                                                               | 使用选项集菜单中定义的自定义DHCP选项。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| **insert-queue-before** (_bottom \| first \| name_; Default: **first**)                                                               | 指定设置了限速参数的静态DCHP租约的动态简单队列条目的位置。                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| **interface** (_string_; Default: )                                                                                                   | DHCP服务器将运行的接口。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| **lease-script** (_string_; Default: **""**)                                                                                          | 一个在分配或取消租赁后执行的脚本。内部的全局变量，可以在脚本中使用：<br>- leaseBound 如果绑定，则设置为 "1"，否则设置为 "0"<br>- leaseServerName DHCP服务器名称<br>- leaseActMAC 活动的MAC地址<br>- leaseActIP 活动的 IP 地址<br>- lease-hostname 客户端主机名<br>- lease-options 一个接收选项的数组                                                                                                                                                                                                                     |
| **lease-time** (_time_; Default: **3****0m**)                                                                                         | 客户端可以使用分配的地址的时间。客户端将在这个时间的一半后尝试更新这个地址，并在时间限制到期后请求一个新的地址。                                                                                                                                                                                                                                                                                                                                                                                                         |
| **name** (_string_; Default: )                                                                                                        | 参考名称                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| **parent-queue** (_string \| none_; Default: **none**)                                                                                | 为这个租约动态创建的队列将被配置为指定父队列的子队列。                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| **relay** (_IP_; Default: **0.0.0.0**)                                                                                                | 这个DHCP服务器应该处理来自中继的请求的IP地址：<br>- 0.0.0.0 该DHCP服务器将只用于客户的直接请求（不允许DHCP中继）。                                                                                                                                                                                                                                                                                                                                                                                                       |
| - 255.255.255.255 DHCP服务器应该用于任何来自DHCP中继的请求，除了那些由存在于 `/ip dhcp-server` 子菜单中的另一个DHCP服务器处理的请求。 |
| **server-address** (_IP_; Default: **0.0.0.0**)                                                                                       | 在客户端启动过程的下一步要使用的服务器IP地址（例如，在为接口分配了几个地址的情况下，要分配一个特定的服务器地址）                                                                                                                                                                                                                                                                                                                                                                                                         |
| **use-framed-as-classless** (_yes \| no_; Default: **yes**)                                                                           | 将RADIUS有框路由作为DHCP无框-静态路由转发给DHCP-客户端。当同时收到Framed-Route和Classless-Static-Route时，首选Classless-Static-Route。                                                                                                                                                                                                                                                                                                                                                                                   |
| **use-radius** (_yes  \| no\| accounting_; Default: **no**)                                                                           | 是否使用RADIUS服务器：<br>- no 不使用RADIUS；<br>- yes 使用RADIUS进行会计和租赁；<br>- accounting仅使用RADIUS进行会计处理。                                                                                                                                                                                                                                                                                                                                                                                              |

## Leases

**Sub-menu:** `/ip dhcp-server lease`

DHCP server lease submenu is used to monitor and manage server leases. The issued leases are shown here as dynamic entries. You can also add static leases to issue a specific IP address to a particular client (identified by MAC address).

Generally, the DHCP lease is allocated as follows:

-   an unused lease is in the "waiting" state
-   if a client asks for an IP address, the server chooses one
-   if the client receives a statically assigned address, the lease becomes offered, and then bound with the respective lease time
-   if the client receives a dynamic address (taken from an IP address pool), the router sends a ping packet and waits for an answer for 0.5 seconds. During this time, the lease is marked testing
-   in the case where the address does not respond, the lease becomes offered and then bound with the respective lease time
-   in other cases, the lease becomes busy for the lease time (there is a command to retest all busy addresses), and the client's request remains unanswered (the client will try again shortly)

A client may free the leased address. The dynamic lease is removed, and the allocated address is returned to the address pool. But the static lease becomes busy until the client reacquires the address.

IP addresses assigned statically are not probed!

  
| Property                                                                                                                                                                                                         | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **address** (_IP_; Default: **0.0.0.0**)                                                                                                                                                                         | Specify IP address (or ip pool) for static lease. If set to **0.0.0.0**  a pool from the DHCP server will be used                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| **address-list** (_string_; Default: **none**)                                                                                                                                                                   | Address list to which address will be added if the lease is bound.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| **allow-dual-stack-queue** (_yes                                                                                                                                                                                 | no_; Default: **yes**)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | Creates a single simple queue entry for both IPv4 and IPv6 addresses, and uses the MAC address and DUID for identification. Requires [IPv6 DHCP Server](https://help.mikrotik.com/docs/display/ROS/DHCP#DHCP-DHCPv6Server) to have this option enabled as well to work properly. |
| **always-broadcast** (_yes                                                                                                                                                                                       | no_; Default: **no**)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | Send all replies as broadcasts                                                                                                                                                                                                                                                   |
| **block-access** (_yes                                                                                                                                                                                           | no_; Default: **no**)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | Block access for this client                                                                                                                                                                                                                                                     |
| **client-id** (_string_; Default: **none**)                                                                                                                                                                      | If specified, must match the DHCP 'client identifier' option of the request                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **dhcp-option** (_string_; Default: **none**)                                                                                                                                                                    | Add additional DHCP options from [option list](https://help.mikrotik.com/docs/display/ROS/DHCP#DHCP-DHCPOptions.1).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| **dhcp-option-set** (_string_; Default: **none**)                                                                                                                                                                | Add an additional set of DHCP options.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| **insert-queue-before** (_bottom                                                                                                                                                                                 | first                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | name_; Default: **first**)                                                                                                                                                                                                                                                       | Specify where to place dynamic simple queue entries for static DCHP leases with rate-limit parameter set. |
| **lease-time** (_time_; Default: **0s**)                                                                                                                                                                         | Time that the client may use the address. If set to **0s** lease will never expire.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| **mac-address** (_MAC_; Default: **00:00:00:00:00:00**)                                                                                                                                                          | If specified, must match the MAC address of the client                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| **parent-queue** (_string                                                                                                                                                                                        | none_; Default: **none**)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | A dynamically created queue for this lease will be configured as a child queue of the specified parent queue.                                                                                                                                                                    |
| **queue-type** (_default, ethernet-default, multi-queue-ethernet-default, pcq-download-default, synchronous-default, default-small, hotspot-default, only-hardware-queue, pcq-upload-default, wireless-default_) | Queue type that can be assigned to the specific lease                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **rate-limit** (_integer[/integer] [integer[/integer] [integer[/integer] [integer[/integer];_; Default: )                                                                                                        | Adds a dynamic simple queue to limit IP's bandwidth to a specified rate. Requires the lease to be static. Format is: rx-rate[/tx-rate] [rx-burst-rate[/tx-burst-rate] [rx-burst-threshold[/tx-burst-threshold] [rx-burst-time[/tx-burst-time]. All rates should be numbers with optional 'k' (1,000s) or 'M' (1,000,000s). If tx-rate is not specified, rx-rate is as tx-rate too. Same goes for tx-burst-rate and tx-burst-threshold and tx-burst-time. If both rx-burst-threshold and tx-burst-threshold are not specified (but burst-rate is specified), rx-rate and tx-rate is used as burst thresholds. If both rx-burst-time and tx-burst-time are not specified, 1s is used as default. |
| _**routes**_ ([dst-address/mask] [gateway] [distance]; Default: _**none**_)                                                                                                                                      |

Routes that appear on the server when the client is connected. It is possible to specify multiple routes separated by commas. This setting will be ignored for OpenVPN.

 |
| **server** (_string_) | Server name which serves this client |
| **use-src-mac (_yes | no_; Default: no)** | When this option is set server uses the source MAC address instead of the received CHADDR to assign the address. |

### Menu specific commands

<table class="relative-table wrapped confluenceTable" style="width: 77.8319%;"><colgroup><col style="width: 7.68242%;"><col style="width: 92.3176%;"></colgroup><tbody><tr><td class="confluenceTd"><strong>check-status</strong><span>&nbsp;</span>(<em>id</em>)</td><td class="confluenceTd">Check the status of a given busy (status is conflict or declined) dynamic lease, and free it in case of no response</td></tr><tr><td class="confluenceTd"><strong>make-static</strong><span>&nbsp;</span>(<em>id</em>)</td><td class="confluenceTd">Convert a dynamic lease to a static one</td></tr></tbody></table>

### Store Configuration

**Sub-menu:** `/ip dhcp-server config`

This sub-menu allows the configuration of how often the DHCP leases will be stored on disk. If they would be saved on a disk on every lease change, a lot of disk writes would happen which is very bad for Compact Flash (especially, if lease times are very short). To minimize writes on disk, all changes are saved on disk every store-leases-disk seconds. Additionally, leases are always stored on disk on graceful shutdown and reboot.

Manual changes to leases - addition/removal of a static lease, removal of a dynamic lease will cause changes to be pushed for this lease to storage.

### Rate limiting

It is possible to set the bandwidth to a specific IPv4 address by using DHCPv4 leases. This can be done by setting a rate limit on the DHCPv4 lease itself, by doing this a dynamic simple queue rule will be added for the IPv4 address that corresponds to the DHCPv4 lease. By using the _rate-limit_ parameter you can conveniently limit a user's bandwidth.

For any queues to work properly, the traffic must not be FastTracked, make sure your Firewall does not FastTrack traffic that you want to limit.

  
First, make the DHCPv4 lease static, otherwise, it will not be possible to set a rate limit to a DHCPv4 lease:

```shell
[admin@MikroTik] > /ip dhcp-server lease print
Flags: X - disabled, R - radius, D - dynamic, B - blocked
 #   ADDRESS               MAC-ADDRESS       HOST-NAME               SERVER               RATE-LIMIT               STATUS
 0 D 192.168.88.254        6C:3B:6B:7C:41:3E MikroTik                DHCPv4_Server                                 bound
 
[admin@MikroTik] > /ip dhcp-server lease make-static 0
 
[admin@MikroTik] > /ip dhcp-server lease print
Flags: X - disabled, R - radius, D - dynamic, B - blocked
 #   ADDRESS               MAC-ADDRESS       HOST-NAME               SERVER               RATE-LIMIT               STATUS
 0   192.168.88.254        6C:3B:6B:7C:41:3E MikroTik                DHCPv4_Server                                 bound
```

  
Then you can set a rate to a DHCPv4 lease that will create a new dynamic simple queue entry:

```shell
[admin@MikroTik] > /ip dhcp-server lease set 0 rate-limit=10M/10M
 
[admin@MikroTik] > /queue simple print
Flags: X - disabled, I - invalid, D - dynamic
 0  D name="dhcp-ds<6C:3B:6B:7C:41:3E>" target=192.168.88.254/32 parent=none packet-marks="" priority=8/8 queue=default-small/default-small limit-at=10M/10M max-limit=10M/10M burst-limit=0/0 burst-threshold=0/0 burst-time=0s/0s
      bucket-size=0.1/0.1
```

  

By default allow-dual-stack-queue is enabled, this will add a single dynamic simple queue entry for both DCHPv6 binding and DHCPv4 lease, without this option enabled separate dynamic simple queue entries will be added for IPv6 and IPv4.

If _allow-dual-stack-queue_ is enabled, then a single dynamic simple queue entry will be created containing both IPv4 and IPv6 addresses:

```shell
[admin@MikroTik] > /queue simple print
Flags: X - disabled, I - invalid, D - dynamic
 0  D name="dhcp-ds<6C:3B:6B:7C:41:3E>" target=192.168.88.254/32,fdb4:4de7:a3f8:418c::/66 parent=none packet-marks="" priority=8/8 queue=default-small/default-small limit-at=10M/10M max-limit=10M/10M burst-limit=0/0 burst-threshold=0/0
      burst-time=0s/0s bucket-size=0.1/0.1
```

## Network

**Sub-menu:** `/ip dhcp-server network`

**Properties**

| Property                                       | Description                                                                                                                                                                               |
| ---------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **address** (_IP/netmask_; Default: )          | the network DHCP server(s) will lease addresses from                                                                                                                                      |
| **boot-file-name** (_string_; Default: )       | Boot filename                                                                                                                                                                             |
| **caps-manager** (_string_; Default: )         | A comma-separated list of IP addresses for one or more CAPsMAN system managers. DHCP Option 138 (capwap) will be used.                                                                    |
| **dhcp-option** (_string_; Default: )          | Add additional DHCP options from the option list.                                                                                                                                         |
| **dhcp-option-set** (_string_; Default: )      | Add an additional set of DHCP options.                                                                                                                                                    |
| **dns-none** (_yes                             | no_; Default: **no**)                                                                                                                                                                     | If set, then DHCP Server will not pass dynamic DNS servers configured on the router to the DHCP clients if no DNS Server in DNS-server is set. By default, if there are no DNS servers configured, then the dynamic DNS Servers will be passed to DHCP clients. |
| **dns-server** (_string_; Default: )           | the DHCP client will use these as the default DNS servers. Two comma-separated DNS servers can be specified to be used by the DHCP client as primary and secondary DNS servers            |
| **domain** (_string_; Default: )               | The DHCP client will use this as the 'DNS domain' setting for the network adapter.                                                                                                        |
| **gateway** (_IP_; Default: **0.0.0.0**)       | The default gateway to be used by DHCP Client.                                                                                                                                            |
| **netmask** (_integer: 0..32_; Default: **0**) | The actual network mask is to be used by the DHCP client. If set to '0' - netmask from network address will be used.                                                                      |
| **next-server** (_IP_; Default: )              | The IP address of the next server to use in bootstrap.                                                                                                                                    |
| **ntp-server** (_IP_; Default: )               | the DHCP client will use these as the default NTP servers. Two comma-separated NTP servers can be specified to be used by the DHCP client as primary and secondary NTP servers            |
| **wins-server** (_IP_; Default: )              | The Windows DHCP client will use these as the default WINS servers. Two comma-separated WINS servers can be specified to be used by the DHCP client as primary and secondary WINS servers |

## RADIUS Support

Since RouterOS v6.43 it is possible to use RADIUS to assign a rate limit per lease, to do so you need to pass the Mikrotik-Rate-Limit attribute from your RADIUS Server for your lease. To achieve this you first need to set your DHCPv4 Server to use RADIUS for assigning leases. Below is an example of how to set it up:

```shell
/radius
add address=10.0.0.1 secret=VERYsecret123 service=dhcp
/ip dhcp-server
set dhcp1 use-radius=yes
```

After that, you need to tell your RADIUS Server to pass the Mikrotik-Rate-Limit attribute. In case you are using FreeRADIUS with MySQL, then you need to add appropriate entries into **radcheck** and **radreply** tables for a MAC address, that is being used for your DHCPv4 Client. Below is an example for table entries:

呈现代码宏出错: 参数'com.atlassian.confluence.ext.code.render.InvalidValueException'的值无效

```
INSERT INTO `radcheck` (`username`, `attribute`, `op`, `value`) VALUES
('00:0C:42:00:D4:64', 'Auth-Type', ':=', 'Accept'),

INSERT INTO `radreply` (`username`, `attribute`, `op`, `value`) VALUES
('00:0C:42:00:D4:64', 'Framed-IP-Address', '=', '192.168.88.254'),
('00:0C:42:00:D4:64', 'Mikrotik-Rate-Limit', '=', '10M'),
```

## Alerts

To find any rogue DHCP servers as soon as they appear in your network, the DHCP Alert tool can be used. It will monitor the interface for all DHCP replies and check if this reply comes from a valid DHCP server. If a reply from an unknown DHCP server is detected, an alert gets triggered:

```shell
[admin@MikroTik] ip dhcp-server alert>/log print
00:34:23 dhcp,critical,error,warning,info,debug dhcp alert on Public:
    discovered unknown dhcp server, mac 00:02:29:60:36:E7, ip 10.5.8.236
[admin@MikroTik] ip dhcp-server alert>
```

When the system alerts about a rogue DHCP server, it can execute a custom script.

As DHCP replies can be unicast, the rogue DHCP detector may not receive any offer to other DHCP clients at all. To deal with this, the rogue DHCP detector acts as a DHCP client as well - it sends out DHCP discover requests once a minute.

The DHCP alert is not recommended on devices that are configured as DHCP clients. Since the alert itself generates DHCP discovery packets, it can affect the operation of the DHCP client itself. Use this feature only on devices that are DHCP servers or using a static IP address.

**Sub-menu:** `/ip dhcp-server alert`

**Properties**

| Property                               | Description                                             |
| -------------------------------------- | ------------------------------------------------------- |
| **alert-timeout** (none                | time; Default: 1h)                                      | Time after which the alert will be forgotten. If after that time the same server is detected, a new alert will be generated. If set to **none** timeout will never expire. |
| **interface** (_string_; Default: )    | Interface, on which to run rogue DHCP server finder.    |
| **on-alert** (_string_; Default: )     | Script to run, when an unknown DHCP server is detected. |
| **valid-server** (_string_; Default: ) | List of MAC addresses of valid DHCP servers.            |

**Read-only properties**

|Property | Description |  

 |                               |
 | ----------------------------- | ---------------------------------------------------------------------------------------------------------------- |
 | **unknown-server** (_string_) | List of MAC addresses of detected unknown DHCP servers. The server is removed from this list after alert-timeout |

**Menu specific commands**

|Property | Description |  

 |                        |
 | ---------------------- | -------------------------------- |
 | **reset-alert** (_id_) | Clear all alerts on an interface |

## DHCP Options

**Sub-menu:** `/ip dhcp-server option`

With the help of the DHCP Option list, it is possible to define additional custom options for DHCP Server to advertise. Option precedence is as follows:

-   radius,
-   lease,
-   server,
-   network.

This is the order in which the client option request will be filled in.

According to the DHCP protocol, a parameter is returned to the DHCP client only if it requests this parameter, specifying the respective code in the DHCP request Parameter-List (code 55) attribute. If the code is not included in the Parameter-List attribute, the DHCP server will not send it to the DHCP client, but **since RouterOS v7.1rc5 it is possible to force the DHCP option** from the server-side even if the DHCP-client does not request such parameter:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">ip</code><code class="ros constants">/dhcp-server/option/</code><code class="ros functions">set </code><code class="ros value">force</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

**Properties**

|Property | Description |  

 |                                        |
 | -------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
 | **code** (_integer:1..254_; Default: ) | dhcp option code. All codes are available at [http://www.iana.org/assignments/bootp-dhcp-parameters](http://www.iana.org/assignments/bootp-dhcp-parameters) |
 | **name** (_string_; Default: )         | Descriptive name of the option                                                                                                                              |
 | **value** (_string_; Default: )        | Parameter's value. Available data types for options are:                                                                                                    |

-   -   'test' -> ASCII to Hex 0x74657374
    -   '10.10.10.10' -> Unicode IP to Hex 0x0a0a0a0a
    -   s'10.10.10.10' -> ASCII to hex 0x31302e31302e31302e3130
    -   s'160' -> ASCII to hex 0x313630
    -   '10' -> Decimal to Hex 0x0a
    -   0x0a0a -> No conversion
    -   $(VARIABLE) -> hardcoded values

RouterOS has predefined variables that can be used:

-   HOSTNAME - client hostname
-   RADIUS_MT_STR1 - from radius MT attr nr. 24
-   RADIUS_MT_STR2 - from radius MT attr nr. 25
-   REMOTE_ID - agent remote-id
-   NETWORK_GATEWAY - the first gateway from '_/ip dhcp-server network_', note that this option won't work if used from lease

  
Now it is also possible to combine data types into one, for example: "0x01'vards'$(HOSTNAME)"

For example if HOSTNAME is 'kvm', then raw value will be 0x0176617264736b766d.

 |
| **raw-value** (_HEX string_ ) | Read-only field which shows raw DHCP option value (the format actually sent out) |

### DHCP Option Sets

**Sub-menu:** `/ip dhcp-server option sets`

This menu allows combining multiple options in option sets, which later can be used to override the default DHCP server option set.

### Example

**Classless Route**

A classless route adds a specified route in the clients routing table. In our example, it will add

-   dst-address=160.0.0.0/24 gateway=10.1.101.1
-   dst-address=0.0.0.0/0 gateway=10.1.101.1

  
According to RFC 3442: The first part is the netmask ("18" = netmask /24). Second part is significant part of destination network ("A00000" = 160.0.0). Third part is IP address of gateway ("0A016501" = 10.1.101.1). Then There are parts of the default route, destination netmask (0x00 = 0.0.0.0/0) followed by default route (0x0A016501 = 10.1.101.1)

```shell
/ip dhcp-server option
add code=121 name=classless value=0x18A000000A016501000A016501
/ip dhcp-server network
set 0 dhcp-option=classless
```

Result:

```shell
[admin@MikroTik] /ip route> print
Flags: X - disabled, A - active, D - dynamic, C - connect, S - static, r - rip, b - bgp, o - ospf,
m - mme, B - blackhole, U - unreachable, P - prohibit
 #      DST-ADDRESS        PREF-SRC        GATEWAY            DISTANCE
 0 ADS  0.0.0.0/0                          10.1.101.1         0
 1 ADS  160.0.0.0/24                       10.1.101.1         0
```

A much more robust way would be to use built-in variables, the previous example can be rewritten as:

`/ip dhcp-server option
add name=classless code=121 value="0x18A00000\$(NETWORK_GATEWAY)0x00\$(NETWORK_GATEWAY)"`

  
**Auto proxy config**

`/ip dhcp-server option
  add code=252 name=auto-proxy-config value="'https://autoconfig.something.lv/wpad.dat'"`

## Vendor Classes

Since the 6.45beta6 version RouterOS support vendor class, ID matcher. The vendor class is used by DHCP clients to optionally identify the vendor and configuration.

Vendor-class-id matcher changes to generic matcher since RouterOS v7.4beta4.

### Example

In the following configuration example, we will give an IP address from a particular pool for an Android-based mobile phone. We will use the RouterBOARD with a default configuration

```shell
/ip pool
add name=default-dhcp ranges=192.168.88.10-192.168.88.254
add name=pool-for-VID ranges=172.16.16.10-172.16.16.120
```

Configure `vendor-class-id` matcher. DHCP servers configuration remains the default

```shell
/ip dhcp-server
add address-pool=default-dhcp disabled=no interface=bridge name=defconf
/ip dhcp-server network
add address=192.168.88.0/24 comment=defconf gateway=192.168.88.1
/ip dhcp-server vendor-class-id
add address-pool=pool-for-VID name=samsung server=defconf vid=android-dhcp-9
```
 

Connect your mobile phone to the device to receive an IP address from the 172.16.16.0 network

```shell
[admin@mikrotik] > /ip dhcp-server lease print detail
Flags: X - disabled, R - radius, D - dynamic, B - blocked
 0 D address=172.16.16.120 mac-address=30:07:4D:F5:07:49 client-id="1:30:7:4d:f5:7:49" address-lists="" server=defconf dhcp-option=""
     status=bound expires-after=8m55s last-seen=1m5s active-address=172.16.16.120 active-mac-address=30:07:4D:F5:07:49
     active-client-id="1:30:7:4d:f5:7:49" active-server=defconf host-name="Galaxy-S8"
```

  

If you do not know your devices Vendor Class ID, you can turn on DHCP debug logs with `/system logging add topics=dhcp`. Then in the logging entries, you will see **Class-ID**

```shell
10:30:31 dhcp,debug,packet defconf received request with id 4238230732 from 0.0.0.0
10:30:31 dhcp,debug,packet     secs = 3
10:30:31 dhcp,debug,packet     ciaddr = 0.0.0.0
10:30:31 dhcp,debug,packet     chaddr = 30:07:4D:F5:07:49
10:30:31 dhcp,debug,packet     Msg-Type = request
10:30:31 dhcp,debug,packet     Client-Id = 01-30-07-4D-F5-07-49
10:30:31 dhcp,debug,packet     Address-Request = 172.16.16.120
10:30:31 dhcp,debug,packet     Server-Id = 192.168.88.1
10:30:31 dhcp,debug,packet     Max-DHCP-Message-Size = 1500
10:30:31 dhcp,debug,packet     Class-Id = "android-dhcp-9"
10:30:31 dhcp,debug,packet     Host-Name = "Galaxy-S8"
10:30:31 dhcp,debug,packet     Parameter-List = Subnet-Mask,Router,Domain-Server,Domain-Name,Interface-MTU,Broadcast-Address,Address-Time,Ren
ewal-Time,Rebinding-Time,Vendor-Specific
10:30:31 dhcp,info defconf assigned 172.16.16.120 to 30:07:4D:F5:07:49
10:30:31 dhcp,debug,packet defconf sending ack with id 4238230732 to 172.16.16.120
10:30:31 dhcp,debug,packet     ciaddr = 0.0.0.0
10:30:31 dhcp,debug,packet     yiaddr = 172.16.16.120
10:30:31 dhcp,debug,packet     siaddr = 192.168.88.1
10:30:31 dhcp,debug,packet     chaddr = 30:07:4D:F5:07:49
10:30:31 dhcp,debug,packet     Msg-Type = ack
10:30:31 dhcp,debug,packet     Server-Id = 192.168.88.1
10:30:31 dhcp,debug,packet     Address-Time = 600
10:30:31 dhcp,debug,packet     Domain-Server = 192.168.88.1,10.155.0.1,10.155.0.126
```

## Generic matcher

Since RouterOS 7.4beta4 (2022-Jun-15 14:04) the vendor-id matcher is converted to a generic matcher. The genric matcher allows matching any of the DHCP options.

And an example to match DHCP option 60 similar to vendor-id-class matcher:

```shell
/ip dhcp-server matcher
add address-pool=pool1 code=60 name=test value=android-dhcp-11
```

Match the client-id with option 61 configured as hex value:

```shell
/ip dhcp-server matcher
add address-pool=pool1 code=61 name=test value=0x016c3b6bed8364
```

Match the code 12 using the string:

```shell
/ip dhcp-server matcher
add address-pool=testpool code=12 name=test server=dhcp1 value="MikroTik"
```

## Configuration Examples

### Setup

To simply configure DHCP server you can use a `setup` command.

First, you configure an IP address on the interface:

`[admin@MikroTik] > /ip address add address=192.168.88.1/24 interface=ether3 disabled=no`

  

Then you use `setup` a command which will automatically ask necessary parameters:

```shell
[admin@MikroTik] > /ip dhcp-server setup
Select interface to run DHCP server on
 
dhcp server interface: ether3
Select network for DHCP addresses
 
dhcp address space: 192.168.88.0/24
Select gateway for given network
 
gateway for dhcp network: 192.168.88.1
Select pool of ip addresses given out by DHCP server
 
addresses to give out: 192.168.88.2-192.168.88.254
Select DNS servers
 
dns servers: 10.155.126.1,10.155.0.1,                              
Select lease time
 
lease time: 10m
```

  

That is all. You have configured an active DHCP server.

### Manual configuration

To configure the DHCP server manually to respond to local requests you have to configure the following:

-   An **IP pool** for addresses to be given out, make sure that your gateway/DHCP server address is not part of the pool.

`/ip pool add name=dhcp_pool0 ranges=192.168.88.2-192.168.88.254`

-   A **network** indicating subnets that DHCP-server will lease addresses from, among other information, like a gateway, DNS-server, NTP-server, DHCP options, etc.

`/ip dhcp-server network add address=192.168.88.0/24 dns-server=192.168.88.1 gateway=192.168.88.1`

-   In our case, the device itself is serving as the gateway, so we'll add the **address** to the bridge interface:

`/ip address add address=192.168.88.1/24 interface=bridge1 network=192.168.88.0`

-   And finally, add **DHCP Server**, here we will add the previously created address **pool**, and specify on which **interface** the DHCP server should work on

`/ip dhcp-server add address-pool=dhcp_pool0 disabled=no interface=bridge1 name=dhcp1`

# DHCPv6 Server

## Summary

**Standards:** `RFC 3315, RFC 3633`

Single DUID is used for client and server identification, only IAID will vary between clients corresponding to their assigned interface.

Client binding creates a dynamic pool with a timeout set to binding's expiration time (note that now dynamic pools can have a timeout), which will be updated every time binding gets renewed.

When a client is bound to a prefix, the DHCP server adds routing information to know how to reach the assigned prefix.

Client bindings in the server do not show MAC address anymore (as it was in v5.8), DUID (hex) and IAID are used instead. After upgrade, MAC addresses will be converted to DUIDs automatically, but due to unknown DUID type and unknown IAID, they should be further updated by the user;

RouterOS DHCPv6 server can only delegate IPv6 prefixes, not addresses.

## General

**Sub-menu:** `/ipv6 dhcp-server`

This sub-menu lists and allows to configure DHCP-PD servers.

## DHCPv6 Server Properties

| Property                                 | Description                                                                                                                          |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| **address-pool** (_enum                  | static-only_; Default: **static-only**)                                                                                              | [IPv6 pool](https://wiki.mikrotik.com/wiki/Manual:IPv6/Pool "Manual:IPv6/Pool"), from which to take IPv6 prefix for the clients.                                                                            |
| ****allow-dual-stack-queue**** (_yes     | no_; Default: ****yes****)                                                                                                           | Creates a single simple queue entry for both IPv4 and IPv6 addresses, and uses the MAC address and DUID for identification. Requires IPv6 DHCP Server to have this option enabled as well to work properly. |
| **binding-script** (_string_; Default: ) | A script that will be executed after binding is assigned or de-assigned. Internal "global" variables that can be used in the script: |

-   bindingBound  set to "1" if bound, otherwise set to "0"
-   bindingServerName  dhcp server name
-   bindingDUID  DUID
-   bindingAddress  active address
-   bindingPrefix  active prefix

 |
| **dhcp-option** (_string_; Default: **none**) | Add additional DHCP options from [option list](https://help.mikrotik.com/docs/display/ROS/DHCP#DHCP-DHCPOptions.1). |
| **disabled** (_yes | no_; Default: **no**) | Whether DHCP-PD server participates in the prefix assignment process. |
| **interface** (_string_; Default: ) | The interface on which server will be running. |
| **lease-time** (_time_; Default: **3d**) | The time that a client may use the assigned address. The client will try to renew this address after half of this time and will request a new address after the time limit expires. |
| **name** (_string_; Default: ) | Reference name |

**Read-only Properties**

|Property | Description |    

 |                   |
 | ----------------- | ---- |
 | **dynamic** (_yes | no_) |
 |                   |
 | **invalid** (_yes | no_) |
 |                   |

## Bindings

**Sub-menu:** `/ipv6 dhcp-server binding`

DUID is used only for dynamic bindings, so if it changes then the client will receive a different prefix than previously.

|Property | Description |    

 |                                                                                                             |
 | ----------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
 | **address** (_IPv6 prefix_; Default: )                                                                      | IPv6 prefix that will be assigned to the client                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
 | **allow-dual-stack-queue** (_yes                                                                            | no_; Default: **yes**)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | Creates a single simple queue entry for both IPv4 and IPv6 addresses, uses the MAC address and DUID for identification. Requires IPv4 DHCP Server to have this option enabled as well to work properly. |
 | **comment** (_string_; Default: )                                                                           | Short description of an item.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
 | **disabled** (_yes                                                                                          | no_; Default: **no**)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | Whether an item is disabled                                                                                                                                                                             |
 | **dhcp-option** (_string_; Default: )                                                                       | Add additional DHCP options from the option list.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
 | **dhcp-option-set** (_string_; Default: )                                                                   | Add an additional set of DHCP options.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
 | **life-time** (_time_; Default: **3d**)                                                                     | The time period after which binding expires.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
 | **duid** (_hex string_; Default: )                                                                          | DUID value. Should be specified only in hexadecimal format.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
 | **iaid** (_integer [0..4294967295]_; Default: )                                                             | Identity Association Identifier, part of the Client ID.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
 | **prefix-pool** (_string_; Default: )                                                                       | Prefix pool that is being advertised to the DHCPv6 Client.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
 | **rate-limit** (_integer[/integer] [integer[/integer] [integer[/integer] [integer[/integer]]]]_; Default: ) | Adds a dynamic simple queue to limit IP's bandwidth to a specified rate. Requires the lease to be static. Format is: rx-rate[/tx-rate] [rx-burst-rate[/tx-burst-rate] [rx-burst-threshold[/tx-burst-threshold] [rx-burst-time[/tx-burst-time]]]]. All rates should be numbers with optional 'k' (1,000s) or 'M' (1,000,000s). If tx-rate is not specified, rx-rate is as tx-rate too. Same goes for tx-burst-rate and tx-burst-threshold and tx-burst-time. If both rx-burst-threshold and tx-burst-threshold are not specified (but burst-rate is specified), rx-rate and tx-rate is used as burst thresholds. If both rx-burst-time and tx-burst-time are not specified, 1s is used as default. |
 | **server** (_string                                                                                         | all_; Default: **all**)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Name of the server. If set to **all**, then binding applies to all created DHCP-PD servers.                                                                                                             |

**Read-only properties**

|Property | Description |    

 |                            |
 | -------------------------- | -------------------------------------------- |
 | **dynamic** (_yes          | no_)                                         | Whether an item is dynamically created. |
 | **expires-after** (_time_) | The time period after which binding expires. |
 | **last-seen** (_time_)     | Time period since the client was last seen.  |
 | **status** (_waiting       | offered                                      | bound_)                                 | Three status values are possible: |

-   **waiting**  Shown for static bindings if it is not used. For dynamic bindings this status is shown if it was used previously, the server will wait 10 minutes to allow an old client to get this binding, otherwise binding will be cleared and prefix will be offered to other clients.
-   **offered**  if **solicit** message was received, and the server responded with **advertise** a message, but the **request** was not received. During this state client have 2 minutes to get this binding, otherwise, it is freed or changed status to **waiting** for static bindings.
-   **bound**  currently bound.

 |

For example, dynamically assigned /62 prefix

```shell
[admin@RB493G] /ipv6 dhcp-server binding> print detail
 Flags: X - disabled, D - dynamic
0 D address=2a02:610:7501:ff00::/62 duid="1605fcb400241d1781f7" iaid=0
 server=local-dhcp life-time=3d status=bound expires-after=2d23h40m10s
last-seen=19m50s
1 D address=2a02:610:7501:ff04::/62 duid="0019d1393535" iaid=2
server=local-dhcp life-time=3d status=bound expires-after=2d23h43m47s
last-seen=16m13s
```

**Menu specific commands**

| Property           | Description                    |
| ------------------ | ------------------------------ |
| **make-static** () | Set dynamic binding as static. |

### Rate limiting

It is possible to set the bandwidth to a specific IPv6 address by using DHCPv6 bindings. This can be done by setting a rate limit on the DHCPv6 binding itself, by doing this a dynamic simple queue rule will be added for the IPv6 address that corresponds to the DHCPv6 binding. By using the `rate-limit` the parameter you can conveniently limit a user's bandwidth.

For any queues to work properly, the traffic must not be FastTracked, make sure your Firewall does not FastTrack traffic that you want to limit.

First, make the DHCPv6 binding static, otherwise, it will not be possible to set a rate limit to a DHCPv6 binding:

```shell
[admin@MikroTik] > /ipv6 dhcp-server binding print
Flags: X - disabled, D - dynamic
# ADDRESS DUID SERVER STATUS
0 D fdb4:4de7:a3f8:418c::/66 0x6c3b6b7c413e DHCPv6_Server bound
 
[admin@MikroTik] > /ipv6 dhcp-server binding make-static 0
 
[admin@MikroTik] > /ipv6 dhcp-server binding print
Flags: X - disabled, D - dynamic
# ADDRESS DUID SERVER STATUS
0 fdb4:4de7:a3f8:418c::/66 0x6c3b6b7c413e DHCPv6_Server bound
```

Then you need can set a rate to a DHCPv6 binding that will create a new dynamic simple queue entry:

```shell
[admin@MikroTik] > /ipv6 dhcp-server binding set 0 rate-limit=10M/10
[admin@MikroTik] > /queue simple print
Flags: X - disabled, I - invalid, D - dynamic
0 D name="dhcp<6c3b6b7c413e fdb4:4de7:a3f8:418c::/66>" target=fdb4:4de7:a3f8:418c::/66 parent=none packet-marks="" priority=8/8 queue=default
-small/default-small limit-at=10M/10M max-limit=10M/10M burst-limit=0/0
burst-threshold=0/0 burst-time=0s/0s bucket-size=0.1/0.1
```

By default `allow-dual-stack-queue` is enabled, this will add a single dynamic simple queue entry for both DCHPv6 binding and DHCPv4 lease, without this option enabled separate dynamic simple queue entries will be added for IPv6 and IPv4.

If `allow-dual-stack-queue` is enabled, then a single dynamic simple queue entry will be created containing both IPv4 and IPv6 addresses:

```shell
[admin@MikroTik] > /queue simple print
Flags: X - disabled, I - invalid, D - dynamic
 0 D name="dhcp-ds<6C:3B:6B:7C:41:3E>" target=192.168.1.200/32,fdb4:4de7:a3f8:418c::/66 parent=none packet-marks="" priority=8/8 queue=default
-small/default-small limit-at=10M/10M max-limit=10M/10M
burst-limit=0/0 burst-threshold=0/0 burst-time=0s/0s bucket-size=0.1/0.1
```

## RADIUS Support

Since RouterOS v6.43 it is possible to use RADIUS to assign a rate-limit per DHCPv6 binding, to do so you need to pass the Mikrotik-Rate-Limit attribute from your RADIUS Server for your DHCPv6 binding. To achieve this you first need to set your DHCPv6 Server to use RADIUS for assigning bindings. Below is an example of how to set it up:

```shell
/radius
add address=10.0.0.1 secret=VERYsecret123 service=dhcp
/ipv6 dhcp-server
set dhcp1 use-radius=yes
```

After that, you need to tell your RADIUS Server to pass the Mikrotik-Rate-Limit attribute. In case you are using FreeRADIUS with MySQL, then you need to add appropriate entries into **radcheck** and **radreply** tables for a MAC address, that is being used for your DHCPv6 Client. Below is an example for table entries:

```shell
INSERT INTO `radcheck` (`username`, `attribute`, `op`, `value`) VALUES
('000c4200d464', 'Auth-Type', ':=', 'Accept'),
 INSERT INTO `radreply` (`username`, `attribute`, `op`, `value`) VALUES
('000c4200d464', 'Delegated-IPv6-Prefix', '=', 'fdb4:4de7:a3f8:418c::/66'),
('000c4200d464', 'Mikrotik-Rate-Limit', '=', '10M');
```

By default allow-dual-stack-queue is enabled and will add a single dynamic queue entry if the MAC address from the IPv4 lease (or DUID, if the DHCPv4 Client supports `Node-specific Client Identifiers` from RFC4361), but DUID from DHCPv6 Client is not always based on the MAC address from the interface on which the DHCPv6 client is running on, DUID is generated on a per-device basis. For this reason, a single dynamic queue entry might not be created, separate dynamic queue entries might be created instead.

## Configuration Example

### Enabling IPv6 Prefix delegation

Let's consider that we already have a running DHCP server.

To enable IPv6 prefix delegation, first, we need to create an address pool:

`/ipv6 pool add name=myPool prefix=2001:db8:7501::/60 prefix-length=62`

Notice that prefix-length is 62 bits, which means that clients will receive /62 prefixes from the /60 pool.

The next step is to enable DHCP-PD:

`/ipv6 dhcp-server add name=myServer address-pool=myPool interface=local`

  
To test our server we will set up wide-dhcpv6 on an ubuntu machine:

-   install wide-dhcpv6-client
-   edit "/etc/wide-dhcpv6/dhcp6c.conf" as above

You can use also RouterOS as a DHCP-PD client.

```shell
interface eth2{
send ia-pd 0;
};
 
id-assoc pd {
prefix-interface eth3{
sla-id 1;
sla-len 2;
};
};
```

-   Run DHCP-PD client:

`sudo dhcp6c -d -D -f eth2`

-   Verify that prefix was added to the:

```shell
mrz@bumba:/media/aaa$ ip -6 addr
 ..
2: eth3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qlen 1000
 inet6 2001:db8:7501:1:200:ff:fe00:0/64 scope global
 valid_lft forever preferred_lft forever
 inet6 fe80::224:1dff:fe17:81f7/64 scope link
 valid_lft forever preferred_lft forever
```

-   You can make binding to specific client static so that it always receives the same prefix:

```shell
[admin@RB493G] /ipv6 dhcp-server binding> print
Flags: X - disabled, D - dynamic
# ADDRESS DU IAID SER.. STATUS 0 D 2001:db8:7501:1::/62 16 0 loc.. bound
[admin@RB493G] /ipv6 dhcp-server binding> make-static 0
```

-   DHCP-PD also installs a route to assigned prefix into IPv6 routing table:

```shell
[admin@RB493G] /ipv6 route> print
 Flags: X - disabled, A - active, D - dynamic, C - connect, S - static, r - rip, o - ospf, b - bgp, U - unreachable
 # DST-ADDRESS GATEWAY DISTANCE
...
2 ADS 2001:db8:7501:1::/62 fe80::224:1dff:fe17:8... 1
```

# DHCP Relay

## Summary

**Sub-menu:** `/ip dhcp-relay`

The purpose of the DHCP relay is to act as a proxy between DHCP clients and the DHCP server. It is useful in networks where the DHCP server is not on the same broadcast domain as the DHCP client.

DHCP relay does not choose the particular DHCP server in the DHCP-server list, it just sends the incoming request to all the listed servers.

## Properties

| Property                                       | Description                                                                                                                                                                                            |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **add-relay-info** (_yes                       | no_; Default: **no**)                                                                                                                                                                                  | Adds DHCP relay agent information if enabled according to RFC 3046. Agent Circuit ID Sub-option contains mac address of an interface, Agent Remote ID Sub-option contains MAC address of the client from which request was received. |
| **delay-threshold** (_time                     | none_; Default: **none**)                                                                                                                                                                              | If secs field in DHCP packet is smaller than delay-threshold, then this packet is ignored                                                                                                                                            |
| **dhcp-server** (_string_; Default: )          | List of DHCP servers' IP addresses which should the DHCP requests be forwarded to                                                                                                                      |
| **interface** (_string_; Default: )            | Interface name the DHCP relay will be working on.                                                                                                                                                      |
| **local-address** (_IP_; Default: **0.0.0.0**) | The unique IP address of this DHCP relay needed for DHCP server to distinguish relays. If set to **0.0.0.0** - the IP address will be chosen automatically                                             |
| **relay-info-remote-id** (_string_; Default: ) | specified string will be used to construct Option 82 instead of client's MAC address. Option 82 consist of: interface from which packets was received + client mac address or **relay-info-remote-id** |
| **name** (_string_; Default: )                 | Descriptive name for the relay                                                                                                                                                                         |

## Configuration Example  

Let us consider that you have several IP networks 'behind' other routers, but you want to keep all DHCP servers on a single router. To do this, you need a DHCP relay on your network which will relay DHCP requests from clients to the DHCP server.

This example will show you how to configure a DHCP server and a DHCP relay that serves 2 IP networks - 192.168.1.0/24 and 192.168.2.0/24 that are behind a router DHCP-Relay.

![](https://help.mikrotik.com/docs/download/attachments/24805500/DHCPrelay.png?version=1&modificationDate=1587718227300&api=v2)

**IP Address Configuration**

IP addresses of DHCP-Server:

```shell
[admin@DHCP-Server] ip address> print
Flags: X - disabled, I - invalid, D - dynamic
 #   ADDRESS            NETWORK         BROADCAST       INTERFACE
 0   192.168.0.1/24     192.168.0.0     192.168.0.255   To-DHCP-Relay
 1   10.1.0.2/24    10.1.0.0    10.1.0.255  Public
[admin@DHCP-Server] ip address>
```

IP addresses of DHCP-Relay:

```shell
/ip pool add name=Local1-Pool ranges=192.168.1.11-192.168.1.100
/ip pool add name=Local1-Pool ranges=192.168.2.11-192.168.2.100
[admin@DHCP-Server] ip pool> print
 # NAME                                         RANGES
 0 Local1-Pool                                  192.168.1.11-192.168.1.100
 1 Local2-Pool                                  192.168.2.11-192.168.2.100
[admin@DHCP-Server] ip pool>
```

  

**DHCP Server Setup**

To setup 2 DHCP Servers on the DHCP-Server router add 2 pools. For networks 192.168.1.0/24 and 192.168.2.0:

```shell
/ip pool add name=Local1-Pool ranges=192.168.1.11-192.168.1.100
/ip pool add name=Local1-Pool ranges=192.168.2.11-192.168.2.100
[admin@DHCP-Server] ip pool> print
 # NAME                                         RANGES
 0 Local1-Pool                                  192.168.1.11-192.168.1.100
 1 Local2-Pool                                  192.168.2.11-192.168.2.100
[admin@DHCP-Server] ip pool>
```

  

Create DHCP Servers:

```shell
/ip dhcp-server add interface=To-DHCP-Relay relay=192.168.1.1 \
   address-pool=Local1-Pool name=DHCP-1 disabled=no
/ip dhcp-server add interface=To-DHCP-Relay relay=192.168.2.1 \
   address-pool=Local2-Pool name=DHCP-2 disabled=no
[admin@DHCP-Server] ip dhcp-server> print
Flags: X - disabled, I - invalid
 #   NAME         INTERFACE     RELAY           ADDRESS-POOL LEASE-TIME ADD-ARP
 0   DHCP-1       To-DHCP-Relay 192.168.1.1     Local1-Pool  3d00:00:00
 1   DHCP-2       To-DHCP-Relay 192.168.2.1     Local2-Pool  3d00:00:00
[admin@DHCP-Server] ip dhcp-server>
```

  

Configure respective networks:

```shell
/ip dhcp-server network add address=192.168.1.0/24 gateway=192.168.1.1 \
   dns-server=159.148.60.20
/ip dhcp-server network add address=192.168.2.0/24 gateway=192.168.2.1 \
   dns-server 159.148.60.20
[admin@DHCP-Server] ip dhcp-server network> print
 # ADDRESS            GATEWAY         DNS-SERVER      WINS-SERVER     DOMAIN
 0 192.168.1.0/24     192.168.1.1     159.148.60.20
 1 192.168.2.0/24     192.168.2.1     159.148.60.20
[admin@DHCP-Server] ip dhcp-server network>
```


**DHCP Relay Config**

Configuration of DHCP-Server is done. Now let's configure DHCP-Relay:

```shell
/ip dhcp-relay add name=Local1-Relay interface=Local1 \
   dhcp-server=192.168.0.1 local-address=192.168.1.1 disabled=no
/ip dhcp-relay add name=Local2-Relay interface=Local2 \
   dhcp-server=192.168.0.1 local-address=192.168.2.1 disabled=no
[admin@DHCP-Relay] ip dhcp-relay> print
Flags: X - disabled, I - invalid
 #   NAME                        INTERFACE      DHCP-SERVER     LOCAL-ADDRESS
 0   Local1-Relay                Local1         192.168.0.1     192.168.1.1
 1   Local2-Relay                Local2         192.168.0.1     192.168.2.1
[admin@DHCP-Relay] ip dhcp-relay>
```