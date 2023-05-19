## 摘要

`/ip dhcp-client`

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
| **disabled** (_yes \| no_; Default: **yes**)                               |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
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
| **IP address pool** (_string \| static-only_; Default: **static-only**)                                                               | IP地址池，用于为客户获取IP地址。如果设置为static-only，那么只有拥有静态租约的客户（在租约子菜单中添加）才会被允许。                                                                                                                                                                                                                                                                                                                                                                                                      |
| **allow-dual-stack-queue** (_yes \| no_; Default: **yes**)                                                                            | 为IPv4和IPv6地址创建一个简单的队列条目，并使用MAC地址和DUID进行识别。需要IPv6 DHCP服务器也启用这个选项才能正常工作。                                                                                                                                                                                                                                                                                                                                                                                                     |
| **always-broadcast** (_yes\| no_; Default: **no**)                                                                                    | 始终以广播的形式发送回复，即使目的地IP是已知的。会增加L2网络的额外负载。                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| **authoritative** (_after-10sec-delay \| after-2sec-delay\| yes \| no_; Default: **yes**)                                             | 选项改变了服务器对DHCP请求的响应方式：<br>- yes 回应客户对本服务器不可用的地址的请求，DHCP服务器将发送一个否定的确认（DHCPNAK）；<br>- no DHCP服务器忽略客户对该服务器不可用的地址的请求；<br>- after-10sec-延迟请求 "secs < 10 "将按 "no "设置的情况处理，"secs >= 10 "的请求将按 "yes "的情况处理；<br>- 在 "secs<2 "的情况下，after-2sec-delay请求将按照 "no "的设置进行处理，在 "secs>=2 "的情况下，将按照 "yes "的设置进行处理；<br>如果所有 "secs < x" 的请求都应该被忽略，那么应该使用 "delay-threshold=x" 设置。 |
| **bootp-lease-time** (_forever \| lease-time \| time_; Default: **forever**)                                                          | 接受两个预定义的选项或时间值：<br>- 永久租赁，永不过期<br>- 租赁时间使用租赁时间参数中的时间                                                                                                                                                                                                                                                                                                                                                                                                                             |
| **bootp-support** (_none \| static \| dynamic_; Default: **static**)                                                                  | Support for BOOTP客户：<br>- 没有，不响应BOOTP请求<br>- 静态只向BOOTP客户提供静态租约<br>- 动态为BOOTP客户端提供静态和动态租约                                                                                                                                                                                                                                                                                                                                                                                           |
| **client-mac-limit** (_integer \| unlimited_; Default: **unlimited**)                                                                 | 指定是否限制每个单一MAC地址的特定客户数量或不限制。注意，这个设置不能在中继设置中使用。                                                                                                                                                                                                                                                                                                                                                                                                                                  |
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

## 租约

**Sub-menu:** `/ip dhcp-server lease`

DHCP服务器租约子菜单被用来监视和管理服务器租约。所发布的租约在这里显示为动态条目。也可以添加静态租约，向特定客户（通过MAC地址识别）发出特定的IP地址。

一般来说，DHCP租约的分配方式如下：

- 未使用的租约处于 "等待 "状态
- 如果一个客户要求一个IP地址，服务器会选择一个
- 如果客户收到一个静态分配的地址，租约就会被提供，然后与各自的租约时间绑定
- 如果客户端收到一个动态地址（从IP地址池中获取），路由器将发送一个ping包，并等待0.5秒的答复。在这段时间内，租赁被标记为测试
- 在地址没有回应的情况下，租约变为提供，然后与各自的租约时间绑定
- 在其他情况下，租约在租约时间内变得繁忙（有一个命令是重新测试所有繁忙的地址），客户的请求仍然没有得到回应（客户将很快再次尝试）。

客户端可以释放租赁的地址。动态租约被删除，分配的地址被退回到地址池中。但是静态租约变得繁忙，直到客户端重新获得地址。

静态分配的IP地址不会被探测到!

  
| 属性                                                                                                                                                                                                             | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **address** (_IP_; Default: **0.0.0.0**)                                                                                                                                                                         | 指定静态租赁的IP地址（或ip池）。如果设置为 0.0.0.0，将使用DHCP服务器的池。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| **address-list** (_string_; Default: **none**)                                                                                                                                                                   | 地址列表，如果租约被绑定，地址将被添加到该列表中。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **allow-dual-stack-queue** (_yes\| no_; Default: **yes**)                                                                                                                                                        | 为IPv4和IPv6地址创建一个简单的队列条目，并使用MAC地址和DUID进行识别。需要  [IPv6 DHCP Server](https://help.mikrotik.com/docs/display/ROS/DHCP#DHCP-DHCPv6Server) 也启用此选项才能正常工作。                                                                                                                                                                                                                                                                                                                                                                  |
| **always-broadcast** (_yes \| no_; Default: **no**)                                                                                                                                                              | 将所有回复作为广播发送。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| **block-access** (_yes\| no_; Default: **no**)                                                                                                                                                                   | 屏蔽该客户的访问。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **client-id** (_string_; Default: **none**)                                                                                                                                                                      | 如果指定，必须与请求中的DHCP "客户标识符 "选项相匹配。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| **dhcp-option** (_string_; Default: **none**)                                                                                                                                                                    | 从 [选项列表]中添加额外的DHCP选项(https://help.mikrotik.com/docs/display/ROS/DHCP#DHCP-DHCPOptions.1)。                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| **dhcp-option-set** (_string_; Default: **none**)                                                                                                                                                                | 添加额外的DHCP选项集。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| **insert-queue-before** (_bottom                                                                                                                                                                                 | first                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | name_; Default: **first**)                           | 指定设置了速率限制参数的静态DCHP租约的动态简单队列条目放置位置。 |
| **释放时间** (_time_; Default: **0s**)                                                                                                                                                                           | 客户端可以使用该地址的时间。如果设置为**0s**，租约将永不过期。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| **mac-address** (_MAC_; Default: **00:00:00:00:00**)                                                                                                                                                             | 如果指定，必须与客户机的MAC地址匹配。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| **parent-queue** (_string                                                                                                                                                                                        | none_; Default: **none**)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | 此租赁的动态创建队列将被配置为指定的父队列的子队列。 |
| **queue-type** (_default, ethernet-default, multi-queue-ethernet-default, pcq-download-default, synchronous-default, default-small, hotspot-default, only-hardware-queue, pcq-upload-default, wireless-default_) | 可分配给特定租约的队列类型                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| **rate-limit** (_integer[/integer] [integer[/integer] [integer[/integer] [integer[/integer];_; Default: )                                                                                                        | 添加一个动态的简单队列，将IP的带宽限制在一个指定的速率。要求租约是静态的。格式是：rx-rate[/tx-rate] [rx-burst-rate[/tx-burst-rate] [rx-burst-threshold[/tx-burst-threshold] [rx-burst-time[/tx-burst-time]。所有的速率都应该是数字，可以选择'k'（1,000s）或'M'（1,000,000s）。如果没有指定tx-rate，rx-rate也是tx-rate。tx-bulst-rate和tx-bulst-threshold以及tx-bulst-time也是如此。如果没有指定rx-burst-threshold和tx-burst-threshold（但指定了burst-rate），rx-rate和tx-rate被用作burst阈值。如果没有指定rx-burst-time和tx-burst-time，则使用1s作为默认值。 |
| _**routes**_ ([dst-address/mask] [gateway] [distance]; Default：_**none**_)                                                                                                                                      | 客户端连接时出现在服务器上的路线。可以指定由逗号分隔的多个路由。对于OpenVPN，此设置将被忽略。                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| **server** (_string_)                                                                                                                                                                                            | 为该客户端提供服务的服务器名称。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| **us-src-mac** (_yes \| no_; Default: **no**)                                                                                                                                                                    | 当此选项被设置时，服务器使用源MAC地址而不是接收到的CHADDR来分配地址。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |

### 特定的菜单命令

|                       |                                                                                |
| --------------------- | ------------------------------------------------------------------------------ |
| **check-status (id)** | 检查一个给定的繁忙状态（状态为冲突或拒绝），动态租约，如果没有回应，则释放它。 |
| **make-static (id)**  | 将一个动态租约转换为静态租约。                                                 |


### 存储配置

**Sub-menu:** `/ip dhcp-server config`

这个子菜单配置DHCP租约在磁盘上的存储频率。如果每次租约变化都保存在磁盘上，就会发生大量的磁盘写入，这对Compact Flash非常不利（特别是如果租约时间很短）。为了尽量减少对磁盘的写入，所有的变化都会在每一个存储-租赁-磁盘的秒数上保存。此外，在宽松的关机和重启时，租约总是被保存在磁盘上。

对租约的手动更改-增加/删除静态租约，删除动态租约将导致该租约的更改被推送到存储。
### 速率限制

通过使用DHCPv4租约，可以为特定的IPv4地址设置带宽。可以通过在DHCPv4租约上设置速率限制来实现，这样做，一个动态的简单队列规则将添加到与DHCPv4租约相对应的IPv4地址上。通过使用 _rate-limit_ 参数可以方便地限制一个用户的带宽。

为了使任何队列正常工作，流量不能被快速跟踪，请确保防火墙不对你想限制的流量进行快速跟踪。

  
首先，使DHCPv4租约成为静态的，否则，就不可能为DHCPv4租约设置速率限制：

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

  
可以给DHCPv4租约设置一个速率，它将创建一个新的动态简单队列条目：

```shell
[admin@MikroTik] > /ip dhcp-server lease set 0 rate-limit=10M/10M
 
[admin@MikroTik] > /queue simple print
Flags: X - disabled, I - invalid, D - dynamic
 0  D name="dhcp-ds<6C:3B:6B:7C:41:3E>" target=192.168.88.254/32 parent=none packet-marks="" priority=8/8 queue=default-small/default-small limit-at=10M/10M max-limit=10M/10M burst-limit=0/0 burst-threshold=0/0 burst-time=0s/0s
      bucket-size=0.1/0.1
```


默认情况下，allow-dual-stack-queue是启用的，这将为DCHPv6绑定和DHCPv4租赁添加一个单一的动态简单队列条目，如果不启用这个选项，将为IPv6和IPv4添加单独的动态简单队列条目。

如果启用 _allow-dual-stack-queue_ ，那么将创建一个包含IPv4和IPv6地址的单一动态简单队列条目：

```shell
[admin@MikroTik] > /queue simple print
Flags: X - disabled, I - invalid, D - dynamic
 0  D name="dhcp-ds<6C:3B:6B:7C:41:3E>" target=192.168.88.254/32,fdb4:4de7:a3f8:418c::/66 parent=none packet-marks="" priority=8/8 queue=default-small/default-small limit-at=10M/10M max-limit=10M/10M burst-limit=0/0 burst-threshold=0/0
      burst-time=0s/0s bucket-size=0.1/0.1
```

## 网络

**Sub-menu:** `/ip dhcp-server network`

**属性**

| 属性                                                                    | 说明                                                                                                                                                                                     |
| ----------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **address** (_IP/netmask_; Default: )                                   | 网络DHCP服务器将向其租赁地址                                                                                                                                                             |
| **boot-file-name** (_string_; Default: )                                | 启动文件名                                                                                                                                                                               |
| **caps-manager** (_string_; Default: )                                  | 一个逗号分隔的IP地址列表，用于一个或多个CAPsMAN系统管理器。将使用DHCP选项138（capwap）。                                                                                                 |
| **dhcp-option** (_string_; Default: )                                   | 从选项列表中添加额外的DHCP选项。                                                                                                                                                         |
| **dhcp-option-set** (_string_; Default: )                               | 添加额外的DHCP选项集。                                                                                                                                                                   |
| **dns-none** (_yes                             \| no_; Default: **no**) | 如果设置了，如果没有设置DNS-server中的DNS服务器，DHCP服务器就不会把配置在路由器上的动态DNS服务器传给DHCP客户。默认情况下，如果没有配置DNS服务器，那么动态DNS服务器将被传递给DHCP客户端。 |
| **dns-server** (_string_; Default: )                                    | DHCP客户端将使用这些作为默认的DNS服务器。可以指定两个用逗号分隔的DNS服务器，由DHCP客户端作为主要和次要DNS服务器使用。                                                                    |
| **domain** (_string_; Default: )                                        | DHCP客户端将使用这个作为网络适配器的 "DNS域 "设置。                                                                                                                                      |
| **gateway** (_IP_; Default: **0.0.0.0**)                                | DHCP客户端使用的默认网关。                                                                                                                                                               |
| **netmask** (_integer: 0..32_; Default: **0**)                          | DHCP客户端将使用的实际网络掩码。如果设置为'0' - 将使用网络地址的掩码。                                                                                                                   |
| **next-server** (_IP_; Default: )                                       | 下一个服务器的IP地址，在启动时使用。                                                                                                                                                     |
| **ntp-server** (_IP_; Default: )                                        | DHCP客户端将使用这些作为默认的NTP服务器。可以指定两个用逗号隔开的NTP服务器，由DHCP客户端作为主要和次要NTP服务器使用。                                                                    |
| **wins-server** (_IP_; Default: )                                       | Windows DHCP客户端将使用这些作为默认的WINS服务器。可以指定两个用逗号隔开的WINS服务器，作为DHCP客户端的主要和次要WINS服务器。                                                             |

## RADIUS支持

从RouterOS v6.43开始，可以使用RADIUS为每个租约分配一个速率限制，要实现这一点，需要从RADIUS服务器为租约传递Mikrotik-Rate-Limit属性。要实现这一点，首先需要将DHCPv4服务器设置为使用RADIUS来分配租约。下面是一个设置的例子：

```shell
/radius
add address=10.0.0.1 secret=VERYsecret123 service=dhcp
/ip dhcp-server
set dhcp1 use-radius=yes
```

之后需要告诉RADIUS服务器传递Mikrotik-rate-Limit属性。如果使用的是带有MySQL的FreeRADIUS，那么要在 **radcheck** 和 **radreply** 表中为DHCPv4客户端使用的MAC地址添加适当条目。下面是一个表项的例子：


```
INSERT INTO `radcheck` (`username`, `attribute`, `op`, `value`) VALUES
('00:0C:42:00:D4:64', 'Auth-Type', ':=', 'Accept'),

INSERT INTO `radreply` (`username`, `attribute`, `op`, `value`) VALUES
('00:0C:42:00:D4:64', 'Framed-IP-Address', '=', '192.168.88.254'),
('00:0C:42:00:D4:64', 'Mikrotik-Rate-Limit', '=', '10M'),
```

## 警报

为了在网络中出现任何流氓DHCP服务器时立即发现它们，可以使用DHCP警报工具。它将监视接口上所有的DHCP回复，并检查这个回复是否来自一个有效的DHCP服务器。如果检测到一个来自未知DHCP服务器的回复，就会触发警报：

```shell
[admin@MikroTik] ip dhcp-server alert>/log print
00:34:23 dhcp,critical,error,warning,info,debug dhcp alert on Public:
    discovered unknown dhcp server, mac 00:02:29:60:36:E7, ip 10.5.8.236
[admin@MikroTik] ip dhcp-server alert>
```

当系统对一个流氓DHCP服务器发出警报时，可以执行一个自定义脚本。

由于DHCP的回复可以是单播的，流氓DHCP检测器可能根本就没有收到对其他DHCP客户端的任何提议。为了处理这个问题，流氓DHCP检测器也充当了DHCP客户端-它每分钟发出一次DHCP发现请求。

在被配置为DHCP客户端的设备上，不推荐使用DHCP警报。因为警报本身会产生DHCP发现数据包，它可能会影响DHCP客户端本身的运行。只在作为DHCP服务器或使用静态IP地址的设备上使用这个功能。

**Sub-menu:** `/ip dhcp-server alert`

**属性**

| 属性                                   | 说明                                       |
| -------------------------------------- | ------------------------------------------ |
| **alert-timeout** (none                | time; Default: 1h)                         | 时间过后，警报将被遗忘。如果过了这个时间，检测到相同的服务器，将产生一个新的警报。如果设置为无，则永远不会过期。 |
| **interface** (_string_; Default: )    | 在这个接口上运行流氓DHCP服务器搜索器。     |
| **on-alert** (_string_; Default: )     | 当检测到一个未知的DHCP服务器时运行的脚本。 |
| **valid-server** (_string_; Default: ) | 有效DHCP服务器的MAC地址列表。              |

**只读属性**

| 属性                          | 说明                                                                      |
| ----------------------------- | ------------------------------------------------------------------------- |
| **unknown-server** (_string_) | 检测到的未知DHCP服务器的MAC地址列表。警报超时后，该服务器将从该列表中删除 |

**Menu specific commands**

| 属性                   | 说明                 |
| ---------------------- | -------------------- |
| **reset-alert** (_id_) | 清除接口上的所有警告 |

## DHCP选项

**Sub-menu:** `/ip dhcp-server option`

在DHCP选项列表的帮助下，可以定义额外的自定义选项供DHCP服务器公布。选项的优先顺序如下：

- 雷达
- 租赁
- 服务器
- 网络

这是客户端选项请求将被填入的顺序。

根据DHCP协议，只有当DHCP客户端请求该参数，并在DHCP请求的Parameter-List（代码55）属性中指定相应的代码时，该参数才会返回给DHCP客户端。如果该代码没有包含在Parameter-List属性中，DHCP服务器将不会把它发送给DHCP客户端，但是从RouterOS v7.1rc5开始，即使DHCP-客户端没有请求这样的参数，也可以从服务器端强制执行DHCP选项：

`ip/dhcp-server/option/set force=yes`

**属性**

| 属性                                   | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| -------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **code** (_integer:1..254_; Default: ) | dhcp选项代码。所有代码都可以在 [http://www.iana.org/assignments/bootp-dhcp-parameters](http://www.iana.org/assignments/bootp-dhcp-parameters) 看到                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **name** (_string_; Default: )         | 选项的描述性名称                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| **value** (_string_; Default: )        | 参数值。选项的可用数据类型是：<br>- 'test' -> ASCII到Hex 0x74657374<br>    - '10.10.10.10' -> Unicode IP 到十六进制 0x0a0a0a0a<br>    - s'10.10.10.10' -> ASCII到十六进制 0x31302e31302e31302e3130<br>    - s'160' -> ASCII转为十六进制 0x313630<br>    - '10' -> 十进制到十六进制 0x0a<br>    - 0x0a0a --> 没有转换<br>    - \$(VARIABLE) -> 硬编码值<br>RouterOS有预定义的变量可供使用：<br>- HOSTNAME - 客户端主机名 <br> - RADIUS_MT_STR1 - 来自radius MT attr nr. 24的信息 <br> - RADIUS_MT_STR2 - 来自radius MT attr nr. 25<br>- REMOTE_ID - 代理商远程ID <br> - NETWORK_GATEWAY - 来自 _/ip dhcp-server network_ 的第一个网关，注意，如果从租赁中使用，这个选项将不起作用。<br>现在也可以将数据类型合并为一个，例如： "0x01'vards'\$（HOSTNAME）" <br>例如，如果HOSTNAME是'kvm'，那么原始值将是0x0176617264736b766d。 |
| **raw-value** (_HEX string_ )          | 只读字段，显示原始DHCP选项值（实际发送的格式）。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |

### DHCP选项集

**Sub-menu:** `/ip dhcp-server option sets`

这个菜单允许在选项集中组合多个选项，以后可以用来覆盖默认的DHCP服务器选项集。

### 例子

**无类路由**

无类别路由在客户的路由表中添加一个指定的路由。在我们的例子中，它将添加

- dst-address=160.0.0.0/24 gateway=10.1.101.1
- dst-address=0.0.0.0/0 gateway=10.1.101.1

  
根据RFC 3442：第一部分是网络掩码（"18"=netmask/24）。第二部分是目的网络的重要部分（"A00000"=160.0.0）。第三部分是网关的IP地址（"0A016501"=10.1.101.1）。然后是默认路由的部分，目的网络掩码（0x00=0.0.0.0/0），然后是默认路由（0x0A016501=10.1.101.1）。

```shell
/ip dhcp-server option
add code=121 name=classless value=0x18A000000A016501000A016501
/ip dhcp-server network
set 0 dhcp-option=classless
```

结果:

```shell
[admin@MikroTik] /ip route> print
Flags: X - disabled, A - active, D - dynamic, C - connect, S - static, r - rip, b - bgp, o - ospf,
m - mme, B - blackhole, U - unreachable, P - prohibit
 #      DST-ADDRESS        PREF-SRC        GATEWAY            DISTANCE
 0 ADS  0.0.0.0/0                          10.1.101.1         0
 1 ADS  160.0.0.0/24                       10.1.101.1         0
```

一个更可靠的方法是使用内部变量，前面的例子可以改写为：

`/ip dhcp-server option
add name=classless code=121 value="0x18A00000\$(NETWORK_GATEWAY)0x00\$(NETWORK_GATEWAY)"`

  
**自动代理配置**

`/ip dhcp-server option
  add code=252 name=auto-proxy-config value="'https://autoconfig.something.lv/wpad.dat'"`

## 供应商类

从6.45beta6版本开始，RouterOS支持厂商类、ID匹配器。供应商类被DHCP客户端用来选择性地识别供应商和配置。

从RouterOS v7.4beta4开始，供应商类-ID匹配器变成了通用匹配器。

### 例子

在下面的配置例子中，从一个特定的池子里为一个基于Android的手机提供一个IP地址。将使用RouterBOARD的默认配置

```shell
/ip pool
add name=default-dhcp ranges=192.168.88.10-192.168.88.254
add name=pool-for-VID ranges=172.16.16.10-172.16.16.120
```

配置 `vendor-class-id` 。DHCP服务器的配置仍然是默认的

```shell
/ip dhcp-server
add address-pool=default-dhcp disabled=no interface=bridge name=defconf
/ip dhcp-server network
add address=192.168.88.0/24 comment=defconf gateway=192.168.88.1
/ip dhcp-server vendor-class-id
add address-pool=pool-for-VID name=samsung server=defconf vid=android-dhcp-9
```
 

将手机连接到设备上，从172.16.16.0网络接收一个IP地址。

```shell
[admin@mikrotik] > /ip dhcp-server lease print detail
Flags: X - disabled, R - radius, D - dynamic, B - blocked
 0 D address=172.16.16.120 mac-address=30:07:4D:F5:07:49 client-id="1:30:7:4d:f5:7:49" address-lists="" server=defconf dhcp-option=""
     status=bound expires-after=8m55s last-seen=1m5s active-address=172.16.16.120 active-mac-address=30:07:4D:F5:07:49
     active-client-id="1:30:7:4d:f5:7:49" active-server=defconf host-name="Galaxy-S8"
```

  

如果不知道设备的Vendor Class ID，可以用 `/system logging add topics=dhcp` 打开DHCP调试日志。然后，在日志条目中会看到 **Class-ID**。

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

## 通用匹配器

自从RouterOS 7.4beta4 (2022-Jun-15 14:04)以来，供应商-ID匹配器被转换为一个通用匹配器。通用匹配器允许匹配任何DHCP选项。

举个例子，匹配DHCP选项60，类似于vendor-id类匹配器：

```shell
/ip dhcp-server matcher
add address-pool=pool1 code=60 name=test value=android-dhcp-11
```

匹配客户-ID，选项61被配置为十六进制值：

```shell
/ip dhcp-server matcher
add address-pool=pool1 code=61 name=test value=0x016c3b6bed8364
```

使用字符串匹配代码12：

```shell
/ip dhcp-server matcher
add address-pool=testpool code=12 name=test server=dhcp1 value="MikroTik"
```

## 配置实例

### 设置

要简单地配置DHCP服务器，可以使用setup命令。

首先在接口上配置一个IP地址：

`[admin@MikroTik] > /ip address add address=192.168.88.1/24 interface=ether3 disabled=no`

  

然后用setup命令，它将自动询问必要的参数：

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

  

这样就配置了一个活跃的DHCP服务器。

### 手动配置

要手动配置DHCP服务器以响应本地请求，必须配置以下内容：

- 一个IP池用于发放地址，确保网关/DHCP服务器地址不在该池中。

`/ip pool add name=dhcp_pool0 ranges=192.168.88.2-192.168.88.254`

- 一个 **网络** 表示DHCP-server将租赁地址的子网，以及其他信息，如网关、DNS-server、NTP-server、DHCP选项，等等。

`/ip dhcp-server network add address=192.168.88.0/24 dns-server=192.168.88.1 gateway=192.168.88.1`

- 在这个例子中，设备本身是作为网关的，所以将 **地址** 添加到网桥接口：

`/ip address add address=192.168.88.1/24 interface=bridge1 network=192.168.88.0`

- 最后，添加 **DHCP服务器**，这里添加先前创建的地址池，并指定DHCP服务器应该在哪个接口上工作

`/ip dhcp-server add address-pool=dhcp_pool0 disabled=no interface=bridge1 name=dhcp1`

# DHCPv6服务器

## 摘要

**标准：** `RFC 3315, RFC 3633`

单一的DUID用于客户和服务器的识别，只有IAID在客户之间有所不同，与他们分配的接口相对应。

客户端绑定会创建一个动态池，其超时时间设置为绑定的过期时间（注意现在动态池可以有超时时间），每次绑定被更新时都会更新。

当一个客户被绑定到一个前缀时，DHCP服务器会添加路由信息以知道如何到达被分配的前缀。

服务器中的客户端绑定不再显示MAC地址（像v5.8中那样），而是使用DUID（十六进制）和IAID。升级后，MAC地址将被自动转换为DUID，但由于DUID类型和IAID未知，它们应该由用户进一步更新；

RouterOS DHCPv6服务器只能委托IPv6前缀，不能委托地址。

## 常规的

**Sub-menu:** `/ipv6 dhcp-server`

这个子菜单列出并允许配置DHCP-PD服务器。

## DHCPv6服务器属性

| 属性                                                                                | 说明                                                                                                                                                                                                                                           |
| ----------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **address-pool** (_enum                  \| static-only_; Default: **static-only**) | [IPv6 pool](https://wiki.mikrotik.com/wiki/Manual:IPv6/Pool "Manual:IPv6/Pool")，从中为客户提取IPv6前缀。                                                                                                                                      |
| ****allow-dual-stack-queue**** (_yes     \| no_; Default: ****yes****)              | 为IPv4和IPv6地址创建一个简单的队列条目，并使用MAC地址和DUID进行识别。需要IPv6 DHCP服务器也启用这个选项才能正常工作。                                                                                                                           |
| **binding-script** (_string_; Default: )                                            | 在分配或取消绑定后执行的脚本。可以在脚本中使用的内部 "全局 "变量：<br>- bindingBound 如果绑定，设置为 "1"，否则设置为 "0"<br>- bindingServerName dhcp服务器名称<br>- bindingDUID DUID<br>- bindingAddress 活动地址<br>- bindingPrefix 活动前缀 |
| **dhcp-option** (_string_; Default: **none**)                                       | 从 [选项列表](https://help.mikrotik.com/docs/display/ROS/DHCP#DHCP-DHCPOptions.1) 中添加额外的DHCP选项。                                                                                                                                       |
| **disabled** (_yes \| no_; Default: **no**)                                         | DHCP-PD服务器是否参与前缀分配过程。                                                                                                                                                                                                            |
| **interface** (_string_; Default: )                                                 | 服务器在哪个接口上运行。                                                                                                                                                                                                                       |
| **lease-time** (_time_; Default: **3d**)                                            | 客户端可以使用分配地址的时间。客户端将在这个时间的一半后尝试更新这个地址，并在时间限制到期后请求一个新的地址。                                                                                                                                 |
| **name** (_string_; Default: )                                                      | 参考名称                                                                                                                                                                                                                                       |

**只读属性**

| 属性                      | 说明 |
| ------------------------- | ---- |
| **dynamic** (_yes \| no_) |      |
| **invalid** (_yes \| no_) |      |

## 绑定

**Sub-menu:** `/ipv6 dhcp-server binding`

DUID只用于动态绑定，如果它发生变化，那么客户端将收到一个与之前不同的前缀。

| 属性                                                                                                        | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| ----------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **address** (_IPv6 prefix_; Default: )                                                                      | 将分配给客户端的IPv6前缀。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **allow-dual-stack-queue** (_yes \| no_; Default: **yes**)                                                  | 为IPv4和IPv6地址创建一个简单的队列条目，使用MAC地址和DUID进行识别。需要IPv4 DHCP服务器也启用该选项才能正常工作。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| **comment** (_string_; Default: )                                                                           | 项目的简短描述。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| **disabled** (_yes \| no_; Default: **no**)                                                                 | 项目是否被禁用                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| **dhcp-option** (_string_; Default: )                                                                       | 从选项列表中添加额外的DHCP选项。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| **dhcp-option-set* (_string_; Default: )                                                                    | 添加额外的DHCP选项集。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| **life-time** (_time_; Default: **3d**)                                                                     | 绑定过期的时间段。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| **duid** (_hex string_; Default: )                                                                          | DUID值。只能以十六进制格式指定。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| **iaid** (_integer [0..4294967295]_; Default: )                                                             | 身份协会标识符，是客户ID的一部分。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| **prefix-pool** (_string_; Default: )                                                                       | 正在向DHCPv6客户端公布的前缀池。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| **rate-limit** (_integer[/integer] [integer[/integer] [integer[/integer] [integer[/integer]]]]_; Default: ) | Adds a dynamic simple queue to limit IP's bandwidth to a specified rate. Requires the lease to be static. Format is: rx-rate[/tx-rate] [rx-burst-rate[/tx-burst-rate] [rx-burst-threshold[/tx-burst-threshold] [rx-burst-time[/tx-burst-time]]]]. 所有的速率都应该是数字，可以选择'k'（1,000s）或'M'（1,000,000s）。如果没有指定tx-rate，rx-rate也是tx-rate。tx-bulst-rate和tx-bulst-threshold以及tx-bulst-time也是如此。如果没有指定rx-burst-threshold和tx-burst-threshold（但指定了burst-rate），则rx-rate和tx-rate被用作burst阈值。如果没有指定rx-burst-time和tx-burst-time，则使用1s作为默认值。 |
| **server** (_string\| all_; Default: **all**)                                                               | 服务器的名称。如果设置为 **所有**，那么绑定就适用于所有创建的DHCP-PD服务器。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |

**只读属性**

| 属性                                       | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| ------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **dynamic** (_yes \| no_)                  | 项目是否是动态创建的。                                                                                                                                                                                                                                                                                                                                                                                                                        |
| **expires-after** (_time_)                 | 绑定过期的时间段。                                                                                                                                                                                                                                                                                                                                                                                                                            |
| **last-seen** (_time_)                     | 客户端最后一次被看到的时间段。                                                                                                                                                                                                                                                                                                                                                                                                                |
| **status** (_waiting \| offered \| bound_) | 有三种状态值可以选择： <br>- **waiting** 如果不使用静态绑定，则显示为静态绑定。对于动态绑定，如果以前使用过，则显示此状态，服务器将等待10分钟，让老客户获得此绑定，否则绑定将被清除，前缀将提供给其他客户。<br>- **offered** 如果收到了 **请求** 信息，并且服务器以 **广告** 信息作为回应，但没有收到 **请求**。在这个状态下，客户端有2分钟的时间来获得这个绑定，否则，它将被释放或改变状态为 **等待** 的静态绑定。<br>- **bound** 当前绑定。 |

例如，动态分配的/62前缀

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

**菜单的具体命令**

| 属性               | 说明               |
| ------------------ | ------------------ |
| **make-static** () | 设置动态绑定为静态 |

### 速率限制

可以通过使用 DHCPv6 绑定来设置特定 IPv6 地址的带宽。这可以通过在DHCPv6绑定本身上设置速率限制来实现，通过这样做，一个动态的简单队列规则将被添加到与DHCPv6绑定相对应的IPv6地址上。通过使用 `rate-limit` 参数，可以方便地限制用户的带宽。

为了使任何队列正常工作，流量必须不被快速跟踪，请确保防火墙不对想限制的流量进行快速跟踪。

首先，使DHCPv6绑定成为静态的，否则就不能为DHCPv6绑定设置速率限制：

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

可以给DHCPv6绑定设置一个速率，它将创建一个新的动态简单队列条目：

```shell
[admin@MikroTik] > /ipv6 dhcp-server binding set 0 rate-limit=10M/10
[admin@MikroTik] > /queue simple print
Flags: X - disabled, I - invalid, D - dynamic
0 D name="dhcp<6c3b6b7c413e fdb4:4de7:a3f8:418c::/66>" target=fdb4:4de7:a3f8:418c::/66 parent=none packet-marks="" priority=8/8 queue=default
-small/default-small limit-at=10M/10M max-limit=10M/10M burst-limit=0/0
burst-threshold=0/0 burst-time=0s/0s bucket-size=0.1/0.1
```

默认情况下，`allow-dual-stack-queue` 被启用，这将为DCHPv6绑定和DHCPv4租赁添加一个单一的动态简单队列条目，如果不启用这个选项，将为IPv6和IPv4添加单独的动态简单队列条目。

如果 `allow-dual-stack-queue` 被启用，那么将创建一个包含IPv4和IPv6地址的单一动态队列条目：

```shell
[admin@MikroTik] > /queue simple print
Flags: X - disabled, I - invalid, D - dynamic
 0 D name="dhcp-ds<6C:3B:6B:7C:41:3E>" target=192.168.1.200/32,fdb4:4de7:a3f8:418c::/66 parent=none packet-marks="" priority=8/8 queue=default
-small/default-small limit-at=10M/10M max-limit=10M/10M
burst-limit=0/0 burst-threshold=0/0 burst-time=0s/0s bucket-size=0.1/0.1
```

## RADIUS支持

从RouterOS v6.43开始，可以用RADIUS为每个DHCPv6绑定分配一个速率限制，要实现这一点，需要从RADIUS服务器为DHCPv6绑定传递Mikrotik-Rate-Limit属性。要实现这一点，首先需要将DHCPv6服务器设置为使用RADIUS来分配绑定。下面是一个设置的例子：

```shell
/radius
add address=10.0.0.1 secret=VERYsecret123 service=dhcp
/ipv6 dhcp-server
set dhcp1 use-radius=yes
```

之后需要告诉RADIUS服务器传递Mikrotik-rate-Limit属性。如果用的是带有MySQL的FreeRADIUS，那么需要在 **radcheck** 和 **radreply** 表中为一个MAC地址添加适当的条目，该地址用于DHCPv6客户端。下面是一个表项例子：

```shell
INSERT INTO `radcheck` (`username`, `attribute`, `op`, `value`) VALUES
('000c4200d464', 'Auth-Type', ':=', 'Accept'),
 INSERT INTO `radreply` (`username`, `attribute`, `op`, `value`) VALUES
('000c4200d464', 'Delegated-IPv6-Prefix', '=', 'fdb4:4de7:a3f8:418c::/66'),
('000c4200d464', 'Mikrotik-Rate-Limit', '=', '10M');
```

默认情况下，allow-dual-stack-queue是启用的，如果IPv4租约的MAC地址（或DUID，如果DHCPv4客户端支持RFC4361中的 "Node-specific Client Identifiers"），将添加一个动态队列条目，但DHCPv6客户端的DUID并不总是基于DHCPv6客户端运行的接口的MAC地址，DUID是以每个设备为单位生成的。由于这个原因，可能不会创建一个单一的动态队列条目，而会创建单独的动态队列条目。

## 配置实例

### 启用 IPv6 前缀授权

现在已经有一个正在运行的DHCP服务器。

要启用IPv6前缀委托，首先要创建一个地址池：

`/ipv6 pool add name=myPool prefix=2001:db8:7501::/60 prefix-length=62`

注意，前缀长度是62位，这意味着客户将从/60池中接收/62前缀。

下一步是启用DHCP-PD：

`/ipv6 dhcp-server add name=myServer address-pool=myPool interface=local`

  
为了测试服务器，将在ubuntu机器上设置owe-dhcpv6：

- 安装owe-dhcpv6-client
- 像上面那样编辑"/etc/wide-dhcpv6/dhcp6c.conf"。

也可以用RouterOS作为DHCP-PD客户端。

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

-   运行DHCP-PD客户端:

`sudo dhcp6c -d -D -f eth2`

-  确认前缀被添加：

```shell
mrz@bumba:/media/aaa$ ip -6 addr
 ..
2: eth3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qlen 1000
 inet6 2001:db8:7501:1:200:ff:fe00:0/64 scope global
 valid_lft forever preferred_lft forever
 inet6 fe80::224:1dff:fe17:81f7/64 scope link
 valid_lft forever preferred_lft forever
```

- 可以让特定客户的绑定成为静态的，以便它收到相同的前缀：

```shell
[admin@RB493G] /ipv6 dhcp-server binding> print
Flags: X - disabled, D - dynamic
# ADDRESS DU IAID SER.. STATUS 0 D 2001:db8:7501:1::/62 16 0 loc.. bound
[admin@RB493G] /ipv6 dhcp-server binding> make-static 0
```

- DHCP-PD还将分配给前缀的路由安装到IPv6路由表：

```shell
[admin@RB493G] /ipv6 route> print
 Flags: X - disabled, A - active, D - dynamic, C - connect, S - static, r - rip, o - ospf, b - bgp, U - unreachable
 # DST-ADDRESS GATEWAY DISTANCE
...
2 ADS 2001:db8:7501:1::/62 fe80::224:1dff:fe17:8... 1
```

# DHCP中继

## 摘要

**Sub-menu：** `/ip dhcp-relay`。

DHCP中继的目的是在DHCP客户和DHCP服务器之间充当一个代理。在DHCP服务器与DHCP客户不在同一广播域的网络中，它很有用。

DHCP中继不会在DHCP-服务器列表中选择特定的DHCP服务器，它只是将传入的请求发送到所有列出的服务器。

## 属性

| 属性                                                                    | 说明                                                                                                                             |
| ----------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| **add-relay-info** (_yes                       \| no_; Default: **no**) | 如果根据RFC 3046启用，则添加DHCP中继代理信息。代理电路ID子选项包含接口的MAC地址，代理远程ID子选项包含接收请求的客户端的MAC地址。 |
| 如果DHCP数据包中的secs字段小于延迟阈值，那么这个数据包将被忽略。        |
| **dhcp-server** (_string_; Default: )                                   | DHCP服务器的IP地址列表，DHCP请求应该被转发到这些地址。                                                                           |
| **interface** (_string_; Default: )                                     | DHCP中继工作的接口名称。                                                                                                         |
| **local-address** (_IP_; Default: **0.0.0.0**)                          | 这个DHCP中继的唯一IP地址，需要DHCP服务器来区分中继。如果设置为 **0.0.0.0** - IP地址将自动选择。                                  |
| **relay-info-remote-id** (_string_; Default: )                          | 指定的字符串将被用来构建选项82，而不是客户的MAC地址。选项82包括：接收数据包的接口+客户的MAC地址或 **relay-info-remote-id**。     |
| **name** (_string_; Default: )                                          | 中继的描述名称。                                                                                                                 |

## 配置实例  

考虑一下有几个 "在其他路由器后面 "的IP网络，想把所有的DHCP服务器放在一个路由器上。要实现这一点，需要在网络上有一个 DHCP 中继器，把客户的 DHCP 请求转发给 DHCP 服务器。

这个例子说明如何配置一个DHCP服务器和一个为2个IP网络服务的DHCP中继器--192.168.1.0/24和192.168.2.0/24，它们在一个路由器DHCP-Relay后面。

![](https://help.mikrotik.com/docs/download/attachments/24805500/DHCPrelay.png?version=1&modificationDate=1587718227300&api=v2)

**IP地址配置**

DHCP-服务器的IP地址：

```shell
[admin@DHCP-Server] ip address> print
Flags: X - disabled, I - invalid, D - dynamic
 #   ADDRESS            NETWORK         BROADCAST       INTERFACE
 0   192.168.0.1/24     192.168.0.0     192.168.0.255   To-DHCP-Relay
 1   10.1.0.2/24    10.1.0.0    10.1.0.255  Public
[admin@DHCP-Server] ip address>
```

DHCP-Relay的IP地址：

```shell
/ip pool add name=Local1-Pool ranges=192.168.1.11-192.168.1.100
/ip pool add name=Local1-Pool ranges=192.168.2.11-192.168.2.100
[admin@DHCP-Server] ip pool> print
 # NAME                                         RANGES
 0 Local1-Pool                                  192.168.1.11-192.168.1.100
 1 Local2-Pool                                  192.168.2.11-192.168.2.100
[admin@DHCP-Server] ip pool>
```
  

**DHCP服务器的设置**

要在DHCP-服务器路由器上设置2个DHCP服务器，需要添加2个池。对于网络192.168.1.0/24和192.168.2.0：

```shell
/ip pool add name=Local1-Pool ranges=192.168.1.11-192.168.1.100
/ip pool add name=Local1-Pool ranges=192.168.2.11-192.168.2.100
[admin@DHCP-Server] ip pool> print
 # NAME                                         RANGES
 0 Local1-Pool                                  192.168.1.11-192.168.1.100
 1 Local2-Pool                                  192.168.2.11-192.168.2.100
[admin@DHCP-Server] ip pool>
```
 

创建DHCP服务器:

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

  

配置相应的网络：

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


**DHCP中继配置**

DHCP-服务器的配置已经完成。现在配置DHCP-Relay：

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