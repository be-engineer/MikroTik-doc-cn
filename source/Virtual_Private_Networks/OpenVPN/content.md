# 概述

OpenVPN的安全模型是基于SSL的，SSL是通过互联网进行安全通信的行业标准。OpenVPN使用SSL/TLS协议实现OSI第2层或第3层安全网络扩展。

# 介绍

OpenVPN已经移植到各种平台，包括Linux和Windows，它的配置在这些系统上都是类似的，所以它更容易支持和维护。OpenVPN可以在用户数据报协议(UDP)或传输控制协议(TCP)传输上运行，在单个TCP/UDP端口上复用创建的SSL隧道。OpenVPN是少数几个可以使用代理的VPN协议之一，这有时可能很方便。

# 局限性

目前，不支持的OpenVPN功能:

- LZO压缩
- TLS认证
- 不需要用户名和密码的鉴权

OpenVPN用户名不超过27个字符，密码不超过233个字符。

# OVPN客户端

| 属性                                                         | 说明                                                                       |
| ------------------------------------------------------------ | -------------------------------------------------------------------------- |
| **add-default-route** (_yes_ \| _no_; Default: **no**)       | 是否添加OVPN远端地址作为缺省路由。                                         |
| **auth** (_md5_ \                                            | _sha1_ \                                                                   | _null_ \                                 | _sha256_ \   | _sha512_;Default:**sha1**) | 允许的认证方式。 |
| **certificate** (_string_ \| _none_;Default:**none**)        | 客户端证书名称                                                             |
| **cipher** (_null_ \                                         | _aes128-cbc_ \                                                             | _aes128-gcm_ \                           | _aes192-cbc_ | _aes192-gcm_ \             | _aes256-cbc_ \   | _aes256-gcm_ \ | _blowfish128_;Default:**blowfish128**) | 允许的密码。为了使用GCM类型的密码，“auth”参数必须设置为“null”，因为如果使用GCM密码，也负责“auth”。 |
| **comment** (_string_;Default:)                              | 项目的描述性名称                                                           |
| **connect-to** (_IP_;Default:)                               | OVPN服务器的远程地址。                                                     |
| **disabled** (_yes_ \| _no_; Default: **yes**)               | 接口是否被禁用。缺省情况下是关闭的。                                       |
| **mac-address** (_MAC_;Default:)                             | OVPN接口的Mac地址。如果未指定，将自动生成。                                |
| **max-mtu** (_integer_;Default:**1500**)                     | 最大传输单元。OVPN接口在不产生数据包碎片的情况下能够发送的最大数据包大小。 |
| **mode** (_ip_                                               | _ethernet_;Default:**ip**)                                                 | Layer3或layer2隧道模式(也可选择tun、tap) |
| **name** (_string_;Default:)                                 | 接口的描述性名称。                                                         |
| **password** (_string_;Default:**""**)                       | 鉴权密码。                                                                 |
| **port** (_integer_;Default:**1194**)                        | 要连接的端口。                                                             |
| **profile** (_name_; Default: **default**)                   | 指定建立隧道时使用哪一种PPP配置文件。                                      |
| **protocol** (_tcp_ \| _udp_;Default:**tcp**)                | 表示与远程端点连接时使用的协议。                                           |
| **verify-server-certificate** (_yes_ \| _no_;Default:**no**) | 根据“connect-to”参数检查证书CN或SAN。IP或主机名必须出现在服务器的证书中。  |
| **tls-version** (_any_ \| _only-1.2_;Default:**any**)        | 指定允许的TLS版本                                                          |
| **use-peer-dns** (_yes_ \| _no_;Default:**no**)              | 是否将OVPN服务器提供的DNS服务器添加到IP/DNS配置中。                        |
| **route-nopull** (_yes_ \| _no_;Default:**no**)              | 是否允许OVPN服务器向OVPN客户端实例路由表中添加路由。                       |
| **user** (_string_;Default:)                                 | 用于鉴权的用户名。                                                         |

此外，还可以从OVPN配置文件导入OVPN客户机配置。这样的文件通常由OVPN服务器端提供，并且已经包含了配置，因此您只需要担心几个参数。

`/interface/ovpn-client/import-ovpn-configuration ovpn-password=securepassword \
key-passphrase=certificatekeypassphrase ovpn-user=myuserid skip-cert-import=no`

# OVPN服务器

为每一条与给定服务器建立的隧道创建一个接口。在OVPN服务器的配置中有两种类型的接口

—如果需要引用为特定用户创建的特定接口名称(在防火墙规则或其他地方)，则通过管理方式添加静态接口。
—动态接口将自动添加到此列表中，每当用户连接时，如果其用户名与任何现有的静态表项不匹配(或者如果该表项已经激活，因为不可能有两个单独的隧道接口被相同的名称引用)。

动态接口在用户连接时出现，一旦用户断开连接就消失，因此不可能在路由器配置中(例如在防火墙中)引用为该用途创建的隧道，因此如果需要为该用户创建持久规则，请为他/她创建静态条目。否则，可以安全地使用动态配置。

在这两种情况下，都必须正确配置PPP用户，静态表项不能替代PPP配置。

## 属性

| 属性                                                                                                                                                                   | 说明                                                                                                                                                                                                                                                                                                                                                            |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **auth** (_md5_\| _sha1_\| _null_\| _sha256_\| _sha512_; Default: **sha1,md5,sha256,sha512**)                                                                          | 服务器将接受的身份验证方法。                                                                                                                                                                                                                                                                                                                                    |
| **certificate** (_name_\| _none_; Default: **none**)                                                                                                                   | OVPN服务器使用的证书名称。                                                                                                                                                                                                                                                                                                                                      |
| **cipher** (_null_\| _aes128-cbc_\| _aes128-gcm_ \| _aes192-cbc_ \| _aes192-gcm_ \| _aes256-cbc_\| _aes256-gcm_ \| _blowfish128_; Default: **aes128-cbc,blowfish128**) | 允许密码。                                                                                                                                                                                                                                                                                                                                                      |
| **default-profile** (_name_; Default: **default**)                                                                                                                     | 要使用的默认配置文件。                                                                                                                                                                                                                                                                                                                                          |
| **enabled** (_yes_ \| _no_;Default:**no**)                                                                                                                             | 定义是否启用OVPN服务器。                                                                                                                                                                                                                                                                                                                                        |
| **protocol**(_tcp_\| _udp_;Default:tcp)                                                                                                                                | 表示与远程端点连接时使用的协议。                                                                                                                                                                                                                                                                                                                                |
| **keepalive-timeout** (_integer_ \| _disabled_; Default: **60**)                                                                                                       | 定义路由器每秒钟开始发送keepalive报文的时间间隔(单位为秒)。如果在这段时间内(即2 * keepalive-timeout)没有流量和keepalive响应，则未响应的客户端被宣布断开连接                                                                                                                                                                                                     |
| **mac-address** (_MAC_;Default:)                                                                                                                                       | 服务器自动生成的MAC地址。                                                                                                                                                                                                                                                                                                                                       |
| **max-mtu** (_integer_;Default:**1500**)                                                                                                                               | 最大传输单元。OVPN接口在不产生数据包碎片的情况下能够发送的最大数据包大小。                                                                                                                                                                                                                                                                                      |
| **mode** (_ip_ \| _ethernet_;Default:**ip**)                                                                                                                           | Layer3或layer2隧道模式(也可选择tun、tap)                                                                                                                                                                                                                                                                                                                        |
| **netmask** (_integer_;Default:**24**)                                                                                                                                 | 客户端应用的子网掩码。                                                                                                                                                                                                                                                                                                                                          |
| **port** (_integer_; Default: **1194**)                                                                                                                                | 运行服务器的端口。                                                                                                                                                                                                                                                                                                                                              |
| **require-client-certificate** (_yes_\| _no_;Default:**no**)                                                                                                           | 如果设置为yes，则服务器检查客户端证书是否属于同一证书链。                                                                                                                                                                                                                                                                                                       |
| **redirect-gateway** (_def1_ \| _disabled_ \| _ipv6;_ Default: **disabled**)                                                                                           | 指定OVPN客户端必须添加到路由表中的路由类型。<br>' def1 ' -使用此标志覆盖默认网关，使用0.0.0.0/1和128.0.0.0/1而不是0.0.0.0/0。这样做的好处是覆盖而不是清除原来的默认网关。<br>' disabled ' -不向OVPN客户端发送重定向网关标志。<br>' ipv6 ' -在客户端将ipv6路由重定向到隧道。这与def1标志类似，即添加更具体的IPv6路由(2000::/4和3000::/4)，覆盖整个IPv6单播空间。 |
| **enable-tun-ipv6** (_yes_\| _no;_ Default: **no**)                                                                                                                    | 指定该OVPN服务器是否可以使用IPv6 IP隧道模式。                                                                                                                                                                                                                                                                                                                   |
| **IPv6 -prefix-len** (_integer;_ Default:**64**)                                                                                                                       | 服务器端生成OVPN接口时使用的IPv6地址前缀长度。                                                                                                                                                                                                                                                                                                                  |
| **tun_server - IPv6** (_IPv6 prefix;_ Default:**::**)                                                                                                                  | 服务器端生成OVPN接口时使用的IPv6前缀地址。                                                                                                                                                                                                                                                                                                                      |

此外，还可以为OVPN客户端准备一个.OVPN文件，以便在终端设备上轻松导入。
 
`/interface/ovpn-server/server/export-client-configuration ca-certificate=myCa.crt \
client-certificate=client1.crt client-cert-key=client1.key server-address=192.168.88.1`

路由器上的日期必须在安装证书的过期日期范围内，这一点非常重要。为了克服任何证书验证问题，请在服务器和客户端同时启用 **NTP** 日期同步。

# 例子

## 设置概述

![](https://help.mikrotik.com/docs/download/attachments/2031655/OpenVPN.png?version=1&modificationDate=1615380050324&api=v2)

假设办公室的公网IP地址为2.2.2.2，我们希望两个远程OVPN客户端能够访问办公室网关后面的10.5.8.20和192.168.55.0/24网络。

## 创建证书

所有证书都可以在RouterOS服务器上通过证书管理器生成。[示例](https://wiki.mikrotik.com/wiki/Manual:Create_Certificates#Generate_certificates_on_RouterOS "Manual:Create Certificates")

对于最简单的设置，您只需要一个OVPN服务器证书。

## 服务器配置

第一步是创建一个IP池，将从中分配客户机地址和一些用户。

```shell
/ip pool add name=ovpn-pool range=192.168.77.2-192.168.77.254
 
/ppp profile add name=ovpn local-address=192.168.77.1 remote-address=ovpn-pool
/ppp secret
add name=client1 password=123 profile=ovpn
add name=client2 password=234 profile=ovpn
```

假设已经创建了服务器证书并命名为“server”

`/interface ovpn-server server set enabled=yes certificate=server`

## 客户端配置

由于RouterOS不支持路由推送，你需要手动添加你想通过隧道访问的网络。

```shell
/interface ovpn-client
add name=ovpn-client1 connect-to=2.2.2.2 user=client1 password=123 disabled=no
/ip route
add dst-address=10.5.8.20 gateway=ovpn-client1
add dst-address=192.168.55.0/24 gateway=ovpn-client1
/ip firewall nat add chain=srcnat action=masquerade out-interface=ovpn-client1
```