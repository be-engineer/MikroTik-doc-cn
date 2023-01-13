## 概述
MikroTik HotSpot Gateway 在访问公共网络之前为客户端提供身份验证。

### HotSpot网关功能:

- 使用路由器或远程 RADIUS 服务器上的本地客户端数据库的客户端的不同身份验证方法；
- 在路由器或远程 RADIUS 服务器上的本地数据库中记账的用户；
- 围墙花园系统，未经授权访问某些网页；
- 登录页面修改，可以在其中放置公司信息；
- 自动和透明地将客户端的任何 IP 地址更改为有效地址；
- 从 v6.48 开始，HotSpot可以通知 DHCP 客户端他们在网页认证 (RFC7710) 后面；

HotSpot只有在使用 IPv4 时才能可靠地工作。依赖于防火墙 NAT 规则的HotSpot当前不支持IPv6。

### 示例

```shell
[admin@MikroTik] /ip hotspot> setup
Select interface to run HotSpot on
 
hotspot interface: ether3
Set HotSpot address for interface
 
local address of network: 10.5.50.1/24
masquerade network: yes
Set pool for HotSpot addresses
 
address pool of network: 10.5.50.2-10.5.50.254
Select hotspot SSL certificate
 
select certificate: none
Select SMTP server
 
ip address of smtp server: 0.0.0.0
Setup DNS configuration
 
dns servers: 10.1.101.1
DNS name of local hotspot server
 
dns name: myhotspot
Create local hotspot user
 
name of local hotspot user: admin
password for the user:
[admin@MikroTik] /ip hotspot>

```

校验HotSpot配置:

```shell
[admin@MikroTik] /ip hotspot> print
Flags: X - disabled, I - invalid, S - HTTPS
# NAME INTERFACE ADDRESS-POOL PROFILE IDLE-TIMEOUT
0 hotspot1 ether3 hs-pool-3 hsprof1 5m
[admin@MikroTik] /ip hotspot>
[admin@MikroTik] /ip pool> print
# NAME RANGES
0 hs-pool-3 10.5.50.2-10.5.50.254
[admin@MikroTik] /ip pool> /ip dhcp-server
[admin@MikroTik] /ip dhcp-server> print
Flags: X - disabled, I - invalid
# NAME INTERFACE RELAY ADDRESS-POOL LEASE-TIME ADD-ARP
0 dhcp1 ether3 hs-pool-3 1h
[admin@MikroTik] /ip dhcp-server> /ip firewall nat
[admin@MikroTik] /ip firewall nat> print
Flags: X - disabled, I - invalid, D - dynamic
0 X ;;; place hotspot rules here
chain=unused-hs-chain action=passthrough
 
1 ;;; masquerade hotspot network
chain=srcnat action=masquerade src-address=10.5.50.0/24
[admin@MikroTik] /ip firewall nat>

```

### 设置过程中询问的参数

| 参数                                                                                                     | 说明                                                                                                       |
| -------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| **hotspot interface** (_string_; Default: **allow**)                                                     | 运行 HotSpot 的接口名称。 要在网桥接口上运行 HotSpot，请确保公共接口不包含在网桥端口中。                   |
| **local address of network** (_IP_; Default: **10.5.50.1/24**)                                           | HotSpot网关地址                                                                                            |
| **masquerade network** (_yes                                    \| no_; Default: **yes**)                | 当 **yes** 规则添加到 _/ip firewall nat with action=masquerade_ ,是否伪装 HotSpot 网络                     |
| **address pool of network** (_string_; Default: **yes**)                                                 | HotSpot网络地址池，用于将用户IP地址修改为有效地址。 为不愿意更改其网络设置的移动客户端提供网络访问很有用。 |
| **select certificate** (_none                                   \| import-other-certificate_; Default: ) | 需要 HTTPS 授权方式时，选择 SSL 证书。                                                                     |
| **ip address of smtp server** (_IP_; Default: **0.0.0.0**)                                               | SMTP服务器的IP地址，重定向HotSpot的网络SMTP请求（25 TCP端口）                                              |
| **dns servers** (_IP_; Default: **0.0.0.0**)                                                             | 用于 HotSpot 客户端的 DNS 服务器地址，配置取自 HotSpot 网关的 _/ip dns menu_                               |
| **dns name** (_string_; Default: **""**)                                                                 | HotSpot 服务器的域名，需要完整的域名，例如 [www.example.com](http://www.example.com/)                      |
| **name of local hotspot user** (_string_; Default: **"admin"**)                                          | 自动创建的 HotSpot 用户的用户名，添加到 _/ip hotspot user_                                                 |
| **password for the user'** (_string_; Default: )                                                         | 自动创建的 HotSpot 用户密码                                                                                |

### IP HotSpot

`/ip/hotspot`

该菜单用于管理路由器的 HotSpot 服务器。 可以在以太网、无线、VLAN 和网桥接口上运行 HotSpot。 每个接口允许一个 HotSpot 服务器。 在桥接接口上配置HotSpot时，将HotSpot接口设置为桥接接口，而不是桥接端口，不要将公共接口添加到桥接端口。 您可以手动将 HotSpot 服务器添加到 _/ip/hotspot_ 菜单，但建议运行 _/ip/hotspot/setup_，这会添加所有必要的设置。

| 参数                                                      | 说明                                                                                                                                                           |
| --------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **name** (text)                                           | HotSpot 服务器名称或标识符                                                                                                                                     |
| **address-pool** (name/none; default: _none_)             | 用于将 HotSpot 客户端 _任意_IP 地址改为有效地址。 用于为不愿更改其网络设置的移动客户端提供公共网络访问                                                         |
| **idle-timeout** (time/none; default: _5m_)               | 未经授权客户的非活动期。 当没有来自该客户端的流量时（客户端计算机应该关闭），一旦超时，用户就会从 HotSpot 主机列表中删除，其用过的地址变为可用                 |
| **keepalive-timeout** (time/none; default: _none_)        | 主机停留多长时间才从 HotSpot 中删除的值                                                                                                                        |
| **login-timeout** (time/none; default: _none_)            | 一段时间后，如果主机未被系统授权，则主机条目将从主机表中删除。 循环重复，直到主机登录系统。 如果出现主机在未授权主机表中停留时间过长后无法登录的情况，请启用。 |
| **interface** (name of an interface)                      | 运行 HotSpot 的接口                                                                                                                                            |
| **addresses-per-mac** (integer**/**unlimited; default: 2) | 当多个 HotSpot 客户端连接一个 MAC 地址时，允许与 MAC 地址绑定的 IP 地址数                                                                                      |
| **profile** (name; default: **_default_)**                | HotSpot 服务器默认的 HotSpot 配置文件，位于 _/ip/hotspot/profile_                                                                                              |

只读参数

| 参数                            | 说明                                                                        |
| ------------------------------- | --------------------------------------------------------------------------- |
| keepalive-timeout（只读；时间） | 用户 keepalive-timeout 的准确值。 值显示主机保持多长时间才从 HotSpot 中删除 |

### IP HotSpot激活

HotSpot 活动菜单显示所有在 HotSpot 中验证的客户端，该菜单只是信息（只读），无法更改任何内容。

| 参数                                                                                                                                | 说明                                                                               |
| ----------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| **server** (read-only; name)                                                                                                        | 客户端已登录时的HotSpot 服务器名称                                                 |
| **user** (read-only; name)                                                                                                          | HotSpot 用户名                                                                     |
| **domain** (read-only; text)                                                                                                        | 用户域（从用户名中分离出来），参数仅用于 RADIUS 身份验证                           |
| **address** (read-only; IP address)                                                                                                 | HotSpot 用户的IP地址                                                               |
| **mac-address** (read-only; MAC-address)                                                                                            | HotSpot用户的MAC地址                                                               |
| **login-by** (read-only; multiple-choice: cookie **/** http-chap **/** http-pap **/** https **/** mac **/** mac-cookie **/** trial) | HotSpot 客户端使用的身份验证方法                                                   |
| **uptime** (read-only; time)                                                                                                        | 用户的当前会话时间，它显示用户登录了多长时间                                       |
| **idle-time** (read-only; time)                                                                                                     | 用户闲置时间                                                                       |
| **session-time-left** (read-only; time)                                                                                             | 用户会话时间的准确值。 显示允许用户在线多长时间达到**正常运行时间**后自动注销      |
| **idle-timeout** (read-only; time)                                                                                                  | 用户空闲超时的准确值                                                               |
| **keepalive-timeout** (read-only; time)                                                                                             | 用户的 keepalive-timeout 的准确值。 值显示主机保持多长时间才从 HotSpot 中删除      |
| **limit-bytes-in** (read-only; integer)                                                                                             | 显示从客户端接收到的字节数，为 HotSpot 用户配置适当的参数时，选项处于活动状态      |
| **limit-bytes-out** (read-only; integer)                                                                                            | 显示发送到客户端的字节数，为 HotSpot 用户配置适当的参数时，选项处于活动状态        |
| **limit-bytes-total** (read-only; integer)                                                                                          | 显示从客户端发送/接收的总字节数，为 HotSpot 用户配置适当的参数时，选项处于活动状态 |

### IP HotSpot主机

`/ip/hotspot/host`

列出了连接到 HotSpot 服务器的所有计算机。 主机表只是信息，无法更改任何值：

| 参数                                     | 说明                                                                             |
| ---------------------------------------- | -------------------------------------------------------------------------------- |
| **mac-address** (read-only; MAC-address) | HotSpot用户MAC地址                                                               |
| **address** (read-only; IP address)      | HotSpot 客户原始IP地址                                                           |
| **to-address** (read-only; IP address)   | HotSpot 分配的新客户端地址可能与原始**地址**相同                                 |
| **server** (read-only; name)             | 客户端已连接的HotSpot 服务器名称  to                                             |
| **bridge-port** (read-only; name)        | _/interface bridge port_ 已连接的客户端，当 HotSpot 没有在桥接上配置时值是未知的 |
| **uptime** (read-only; time)             | 值显示用户在线多长时间（连接到 HotSpot）                                         |
| **idle-time** (read-only; time)          | 用户空闲时间                                                                     |
| **idle-timeout** (read-only; time)       | 客户端空闲超时值（未经授权的客户端）                                             |
| **keepalive-timeout** (read-only; time)  | 未授权客户端的 keepalive-timeout 值                                              |
| **bytes-in** (read-only; integer)        | 从未经授权的客户端接收到的字节数                                                 |
| **packet-in** (read-only; integer)       | 从未经授权的客户端收到的数据包数量                                               |
| **bytes-out** (read-only; integer)       | 发送给未授权客户端的字节数                                                       |
| **packet-out** (read-only; integer)      | 发送给未授权客户端的数据包数量                                                   |

## IP绑定

`/ip/hotspot/ip-binding`

IP 绑定 HotSpot 菜单允许设置静态一对一 NAT 转换，允许绕过特定的 HotSpot 客户端而无需任何身份验证，还允许从 HotSpot 网络中阻止特定的主机和子网

| 属性                                                                   | 说明                                                                                                                                                                                                                |
| ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **address** (_IP Range_; Default: **""**)                              | 客户的原始IP地址                                                                                                                                                                                                    |
| **mac-address** (_MAC_; Default: **""**)                               | 客户的MAC地址                                                                                                                                                                                                       |
| **server** (_string                       \| all_; Default: **"all"**) | HotSpot服务器名称<br>-   **all** \- 将应用于所有HotSpot服务器                                                                                                                                                       |
| **to-address** (_IP_; Default: **""**)                                 | 客户端的新 IP 地址，在路由器上进行转换（客户端对转换一无所知）                                                                                                                                                      |
| **type** (_blocked \| bypassed \| regular_; Default: **""**)           | IP 绑定操作的类型<br>-   **regular** \- 根据规则执行一对一 NAT，将**address** 转换为 **to-address**<br>-   **bypassed** \- 执行转换，但不让客户端登录HotSpot<br>-   **blocked** \- 不执行转换并丢弃来自主机的数据包 |


## Cookies

菜单包含所有发送给 HotSpot 客户端的 cookie，这些 cookie 是通过 cookie 方法授权的，所有条目都是只读的。

`/ip/hotspot/cookie`

| 属性                    | 说明                       |
| ----------------------- | -------------------------- |
| **domain** (_string_)   | 域名（从用户名中拆分出来） |
| **expires-in** (_time_) | cookie 的有效期是多久      |
| **mac-address** (_MAC_) | 客户的MAC地址              |
| **user** (_string_)     | HotSpot用户名              |

## 使用 DHCP 选项来发布HotSpot URL

大多数设备，例如现代智能手机，都会进行某种背景检查，以查看它们是否位于强制门户之后。 他们请求一个已知网页并将该页面的内容与它们应有的内容进行比较来做到。 如果内容不同，设备会假设有一个登录页面，并使用该登录页面创建一个弹出窗口。

这并不总是发生，因为这个“已知网页”可能会被阻止、列入白名单或无法在内部网络中访问。 为了改进这种机制，建立了 RFC 7710，允许 HotSpot 通知所有 DHCP 客户端他们在强制门户设备后面，并且他们需要进行身份验证才能访问 Internet，无论他们请求或不请求网页。

此 DHCP 选项会自动启用，前提是路由器配置了 DNS 名称并有有效的 SSL 证书（以便可以通过 HTTPS 访问登录页面）。 当满足这些要求时，将发送一个特殊的 DHCP 选项，其中包含指向 `https://<dns-name-of-hotspot>/api` 的链接。 此链接包含 JSON 格式的信息，指示客户端设备的强制门户状态以及登录页面的位置。

`https://<dns-name-of-hotspot>/api` 的内容如下：

```shell
{
"captive": $(if logged-in == 'yes')false$(else)true$(endif),
"user-portal-url": "$(link-login-only)",
$(if session-timeout-secs != 0)
"seconds-remaining": $(session-timeout-secs),
$(endif)
$(if remain-bytes-total)
"bytes-remaining": $(remain-bytes-total),
$(endif)
"can-extend-session": true
}

```
