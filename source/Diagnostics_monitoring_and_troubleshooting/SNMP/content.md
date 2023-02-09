# 概述

简单网络管理协议（SNMP）是一个互联网标准协议，用于管理IP网络上的设备。SNMP可以用CACTI、MRTG或The Dude等工具绘制各种数据。

SNMP的写入支持只对某些OID有效。对于支持的OIDs，支持SNMP v1、v2或v3的写入。

![](https://help.mikrotik.com/docs/download/attachments/8978519/Total-download-cacti.png?version=1&modificationDate=1607502471040&api=v2)

 SNMP在收到SNMP请求的接口上响应查询，迫使响应具有与发送到路由器的请求目的地相同的源地址

## 快速配置

在RouterOS中启用SNMP：

```shell
[admin@MikroTik] /snmp> print
enabled: no
contact:
location:
engine-id:
trap-community: (unknown)
trap-version: 1
[admin@MikroTik] /snmp> set enabled yes
```

可以在上述设置中指定管理联系信息。所有的SNMP数据都将提供给 _community_ 菜单中配置的属性。

## 常规属性

**Sub-menu:** `/snmp`

这个子菜单允许启用SNMP并完成常规设置。

| 属性                                                                                                                                     | 说明                                                                                                                                                           |
| ---------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **contact** (_string_; Default: **""**)                                                                                                  | 联系信息                                                                                                                                                       |
| **enabled** (_yes                                                                      \| no_; Default: **no**)                          | 停用/启用SNMP服务                                                                                                                                              |
| **engine-id** (_string_; Default: **""**)                                                                                                | 对于SNMP v3，作为标识符的一部分使用。可以用这个参数配置引擎ID的后缀部分。如果SNMP客户端不能检测设置的引擎ID值，那么就必须使用这个前缀的十六进制值 0x80003a8c04 |
| **location** (_string_; Default: **""**)                                                                                                 | 位置信息                                                                                                                                                       |
| **trap-community** (_string_; Default: **public**)                                                                                       | 发送陷阱时，在 _community_ 菜单中配置要用的公共属性。                                                                                                          |
| **trap-generators** (_interfaces                                                       \| start-trap_; Default: )                        | 什么动作会产生陷阱： <br>- 接口 - 接口变化； <br>- 启动陷阱 - 路由器上启动SNMP服务器                                                                           |
| **trap-interfaces** (_string                                                           \| all_; Default: )                               | 要发送陷阱的接口列表。                                                                                                                                         |
| **trap-target** (_list of IP/IPv6_; Default: **0.0.0.0**)                                                                                | 接收陷阱的SNMP数据采集器的IP（IPv4或IPv6）地址                                                                                                                 |
| **trap-version** (_1                                                                   \| 2                       \| 3_; Default: **1**) | 用于陷阱的SNMP协议的一个版本                                                                                                                                   |
| **src-address** (_IPv4 or IPv6 address_; Default: **::**)                                                                                | 强制路由器对所有的SNMP信息始终使用相同的IP源地址                                                                                                               |
| **vrf** (_VRF name_; default value: **main**)                                                                                            | 设置VRF服务监听传入连接                                                                                                                                        |

engine-id字段有engine-id的后缀值，通常情况下，SNMP客户应该能够检测到这个值，作为SNMP值，并从路由器上读取。然而，有一种可能性并非如此。在这种情况下，engine-ID值必须按照这个规则来设置。<engine-id prefix> + <hex-dump suffix>，所以作为一个例子，如果设置了1234作为后缀值，则必须提供80003a8c04 + 31323334，合并后hex是80003a8c0431323334

## community属性

**Sub-menu:** `/snmp community`

这个子菜单允许设置SNMP数据的访问权限。

在v1和v2c中几乎没有安全保障，只有清晰的文本公共字符串（"用户名"）和按IP地址限制访问的能力。

在生产环境中应该使用SNMP v3，因为它提供了安全性--用MD5/SHA1授权（用户+密码），用DES和AES加密。

```shell
[admin@MikroTik] /snmp community> print value-list
name: public
address: 0.0.0.0/0
security: none
read-access: yes
write-access: no
authentication-protocol: MD5
encryption-protocol: DES
authentication-password: *****
encryption-password: *****
```

默认设置只有一个名为 _public_ 的community属性，没有任何额外的安全设置。这些设置是不安全的，要根据所需的安全配置文件来调整。

### 属性

| 属性                                                                                                                                                           | 说明                                                    |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| **address** (_IP/IPv6 address_; Default: **0.0.0.0/0**)                                                                                                        | 允许与SNMP服务器连接的地址                              |
| **authentication-password** (_string_; Default: **""**)                                                                                                        | 验证服务器连接的密码（SNMPv3）。                        |
| **authentication-protocol** (_MD5                       \| SHA1_; Default: **MD5**)                                                                            | 认证的协议（SNMPv3）。                                  |
| **encryption-password** (_string_; Default: **""**)                                                                                                            | 加密的密码（SNMPv3）。                                  |
| **encryption-protocol** (_DES                           \| AES_; Default: **DES**)                                                                             | 加密通信协议（SNMPv3）。AES（见rfc3826）自v6.16起可用。 |
| **name** (_string_; Default: )                                                                                                                                 |
| **read-access** (_yes                                   \| no_; Default: **yes**)                                                                              | community是否启用了读权限                               |
| **security** (_authorized                               \| none                                                                \| private_; Default: **none**) |
| **write-access** (_yes                                  \| no_; Default: **no**)                                                                               | 是否为community启用了写权限                             |

## 对象标识符(OID)

每个OID都标识了一个可以通过SNMP读取的变量。尽管MIB文件包含了所有需要的OID值，也可以在任何菜单级别上用 **print oid** 命令在控制台中打印单个OID信息。

```shell
[admin@MikroTik] /interface> print oid
 
Flags: D - dynamic, X - disabled, R - running, S - slave
0 R name=.1.3.6.1.2.1.2.2.1.2.1 mtu=.1.3.6.1.2.1.2.2.1.4.1
mac-address=.1.3.6.1.2.1.2.2.1.6.1 admin-status=.1.3.6.1.2.1.2.2.1.7.1
oper-status=.1.3.6.1.2.1.2.2.1.8.1 bytes-in=.1.3.6.1.2.1.2.2.1.10.1
packets-in=.1.3.6.1.2.1.2.2.1.11.1 discards-in=.1.3.6.1.2.1.2.2.1.13.1
errors-in=.1.3.6.1.2.1.2.2.1.14.1 bytes-out=.1.3.6.1.2.1.2.2.1.16.1
packets-out=.1.3.6.1.2.1.2.2.1.17.1 discards-out=.1.3.6.1.2.1.2.2.1.19.1
errors-out=.1.3.6.1.2.1.2.2.1.20.1
```

## 陷阱

SNMP陷阱使路由器能够通过发送陷阱通知数据采集器接口变化和SNMP服务状态变化。可以发送具有安全功能的陷阱，支持SNMPv1（无安全），SNMPv2和变种以及带有加密和授权的SNMPv3。

对于SNMPv2和v3，必须设置一个适当配置的community作为 _trap-community_，以启用所需的功能（密码或加密/授权）。

## SNMP写

SNMP写允许用SNMP请求改变路由器配置。当SNMP和写权限被启用时，要考虑确保对路由器或路由器SNMP的访问安全。

要通过SNMP请求改变设置，请使用下面的命令，允许SNMP对所选community进行写入。

`/snmp community set <number> write-access=yes`

### 系统身份

可以通过SNMP set命令来改变路由器的系统身份。

```shell
$ snmpset -c public -v 1 192.168.0.0 1.3.6.1.2.1.1.5.0 s New_Identity
```

- _snmpset_ - SNMP应用，用于SNMP SET请求，设置网络实体的信息。
- _public_ - 路由器的community名称。
- _192.168.0.0_ - 路由器的IP地址。
- _1.3.6.1.2.1.5.0_ - 路由器身份的SNMP值。

上面的SNMPset命令等同于RouterOS命令。

`/system identity set identity=New_Identity`

### 重启

可以用SNMP设置命令来重启路由器，需要设置重启SNMP的值，这个值不等于0。

```shell
$ snmpset -c public -v 1 192.168.0.0 1.3.6.1.4.1.14988.1.1.7.1.0 s 1
```

- **1.3.6.1.4.1.14988.1.7.1.0**, SNMP值用于路由器重启。
- **s 1**，snmpset命令设置的值，不能等于0。

重启SNMPset命令等同于RouterOS命令。

`/system reboot`

### 运行脚本

当需要为脚本的SNMP设置值时，SNMP写允许在路由器上从 **系统脚本** 菜单中运行脚本。

```shell
$ snmpset -c public -v 1 192.168.0.0 1.3.6.1.4.1.14988.1.1.8.1.1.3.X s 1
```

- **X**，脚本编号，从1开始。
- **s 1**，snmpset命令的设置值，不能等于0。

在RouterOS上也有同样的命令。

```shell
/system script> print
Flags: I - invalid
0 name="test" owner="admin" policy=ftp,reboot,read,write,policy,
test,winbox,password,sniff last-started=jan/01/1970
01:31:57 run-count=23 source=:beep
 
/system script run 0
```

### 用GET运行脚本

可以通过SNMP对脚本OID的GET请求来运行 **/system scripts** （从6.37开始）。要做到这一点，需要有写权限的SNMP community。脚本的 OID 可以通过 SNMPWALK 命令来获取，因为这个表是动态的。

添加脚本:

```shell
/system script
add name=script1 owner=admin policy=ftp,reboot,read,write,policy,test,password,sniff,sensitive,romon source="/sy reboot "
add name=script2 owner=admin policy=ftp,reboot,read,write,policy,test,password,sniff,sensitive,romon source="[:put output]"
```

 获取脚本的OID表

```shell
$ snmpwalk -v2c -cpublic 192.168.88.1 1.3.6.1.4.1.14988.1.1.8
iso.3.6.1.4.1.14988.1.1.8.1.1.2.1 = STRING: "script1"
iso.3.6.1.4.1.14988.1.1.8.1.1.2.2 = STRING: "script2"
iso.3.6.1.4.1.14988.1.1.8.1.1.3.1 = INTEGER: 0
iso.3.6.1.4.1.14988.1.1.8.1.1.3.2 = INTEGER: 0
```

要运行该脚本，请使用表18

```shell
$ snmpget -v2c -cpublic 192.168.88.1 1.3.6.1.4.1.14988.1.1.18.1.1.2.2
iso.3.6.1.4.1.14988.1.1.18.1.1.2.2 = STRING: "output"
```
