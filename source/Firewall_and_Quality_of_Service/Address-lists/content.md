# 概述

`/ip firewall address-list`

防火墙地址列表允许用户创建IP地址列表，这些地址在一个共同的名称下组合在一起。然后防火墙过滤器、mangle和NAT可以使用这些地址列表来匹配数据包。

地址列表记录也可以通过NAT、Mangle和过滤器中的action=add-src-to-address-list或action=add-dst-to-address-list项目动态更新。

具有_add-src-to-address-list_或_add-dst-to-address-list_动作的防火墙规则在穿透模式下工作，匹配的数据包将传递到下一个防火墙规则。

## 属性

| 属性                                                                        | 说明                                                                                                                                   |
| --------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| **address** (_DNS Name          \| IP address/netmask \| IP-IP_; Default: ) | 要添加到地址列表或DNS名称中的单个IP地址或IP范围。例如，可以输入'192.168.0.0-192.168.1.255'，保存时自动修改输入的条目为192.168.0.0/23。 |
| **list** (_string_; Default: )                                              | 添加IP地址的地址列表名称                                                                                                               |
| **timeout** (_time_; Default: )                                             | 地址将从地址列表中删除的时间。如果没有指定超时，地址将永远保存在地址列表中。                                                           |

如果没有指定超时参数，地址将永远保存在列表中。如果指定了超时，那么该地址将被保存在RAM上，并在系统重启后被删除。

例子

下面的例子创建了一个连接到路由器23号端口（telnet）的动态地址列表，并在5分钟内丢弃所有来自他们的进一步通信。此外，地址列表还包含一个静态地址列表项192.0.34.166/32（[www.example.com](http://www.example.com)）：

`/ip firewall address-list add list=drop_traffic address=192.0.34.166/32`

```shell
/ip firewall address-list print
Flags: X - disabled, D - dynamic
 #   LIST         ADDRESS
 0   drop_traffic 192.0.34.166
```

```shell
/ip firewall mangle add action=add-src-to-address-list address-list=drop_traffic address-list-timeout=5m chain=prerouting dst-port=23 protocol=tcp
/ip firewall filter add action=drop chain=input src-address-list=drop_traffic
```

```shell
/ip firewall address-list print
Flags: X - disabled, D - dynamic
 #   LIST         ADDRESS
 0   drop_traffic 192.0.34.166
 1 D drop_traffic 1.1.1.1
 2 D drop_traffic 10.5.11.8
```

从最后一条打印命令的输出可以看出，地址列表中出现了两个新的动态条目（标记为 "D "状态）。拥有这些IP地址的主机试图初始化一个到路由器的telnet会话，随后被过滤规则丢弃。
