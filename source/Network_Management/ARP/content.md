# 概述

**Sub-menu:** `/ip arp`

即使IP数据包是使用IP地址寻址的，但必须使用硬件地址将数据从一台主机实际传输到另一台。地址解析协议用于将OSI第三级IP地址映射到OSI第二级MAC地址。路由器有一个当前使用的ARP条目表。通常情况下，该表是动态建立的，但为了提高网络安全性，可以添加静态条目的方式部分或全部静态建立。

# 属性

本节介绍ARP表的配置选项。

| 属性                                                 | 说明                                                                                                                                                                                                             |
| ---------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **address** (_IP_; Default: )                        | 要映射的IP地址                                                                                                                                                                                                   |
| **interface** (_string_; Default: )                  | IP地址分配的接口名称。                                                                                                                                                                                           |
| **mac-address** (_MAC_; Default: **00:00:00:00:00**) | 要映射的MAC地址                                                                                                                                                                                                  |
| **published** (_yes \| no_; Default: **no**)         | 单个IP地址的静态proxy-arp条目。当收到对特定IP地址的ARP查询时，设备将用自己的MAC地址进行响应。不需要为所有要代理的MAC地址在接口本身设置proxy-arp。只有当设备有通往目的地的活动路由时，接口才会对ARP请求作出响应。 |

  
**只读属性：**

| 属性                      | 说明                        |
| ------------------------- | --------------------------- |
| **dhcp** (_yes \| no_)    | ARP条目是否由DHCP服务器添加 |
| **dynamic** (_yes \| no_) | 该条目是否是动态创建的      |
| **invalid** (_yes \| no_) | 该条目是否无效              |

默认的ARP条目的最大数量取决于安装的RAM数量。可以用"/ip settings set max-neighbor-entries=x "命令来调整，更多细节见 [IPv4 Settings]（https://help.mikrotik.com/docs/display/ROS/IP+Settings#IPSettings-IPv4Settings）。

# ARP模式

在接口配置中可以设置几种ARP模式。

- `disabled` -该接口不使用ARP
- `enabled` -接口使用ARP
- `local-proxy-arp` - 路由器在接口上执行ARP代理并向同一接口发送回复
- `proxy-arp` - 路由器在该接口上执行ARP代理，并向其他接口发送回复
- `reply-only` - 接口将只回复来自匹配的IP地址/MAC地址组合的请求，这些组合在IP/ARP表中被输入为静态条目。在IP/ARP表中不会自动存储任何动态条目。因此，要使通信成功，必须已经存在一个有效的静态条目。

## 禁用

如果接口上的ARP功能被关闭，即arp=disabled，客户端的ARP请求就不会被路由器响应。因此应该给客户端添加一个静态ARP条目。例如用arp命令将路由器的IP和MAC地址添加到Windows工作站上：

`C:\> arp -s 10.5.8.254  00-aa-00-62-c6-09`

## 启用

该模式默认在所有接口上都是启用的。ARP将自动发现，新的动态条目将添加到ARP表中。

## ARP代理

具有正确配置的ARP代理功能的路由器在不同的网络之间充当一个透明的ARP代理。

这种行为很有用，例如想给拨号（ppp、ppoe、pptp）客户的IP地址与连接的LAN上使用的地址空间相同。

可以用 **arp=proxy-arp** 命令在每个接口上单独启用ARP代理：

设置ARP代理：

```shell
[admin@MikroTik] /interface ethernet> set 1 arp=proxy-arp
 
[admin@MikroTik] /interface ethernet> print
 
Flags: X - disabled, R - running
  #    NAME                 MTU   MAC-ADDRESS         ARP
  0  R ether1              1500  00:30:4F:0B:7B:C1 enabled
  1  R ether2              1500  00:30:4F:06:62:12 proxy-arp
```

## 只回复

如果接口上的ARP属性被设置为 "只回复"，那么路由器只回复ARP请求。邻居的MAC地址只能通过"/ip arp "菜单中静态配置的条目来解决，但不需要像禁用ARP那样将路由器的MAC地址添加到其他主机的ARP表中。

## 本地代理Arp

如果接口上的ARP属性被设置为 "本地代理ARP"，那么路由器只对这个接口执行代理ARP，即对从同一接口进出的流量执行代理ARP。在一个正常的局域网中，默认的行为是两个网络主机直接相互通信，不涉及路由器。

启用 `local-proxy-arp` 后，路由器将用路由器自己的接口MAC地址而不是其他主机的MAC地址来响应所有客户主机。

例如：如果主机A（192.168.88.2/24）查询主机B（192.168.88.3/24）的MAC地址，路由器会用自己的MAC地址来回应。换句话说，如果启用 `local-proxy-arp` ，路由器将承担转发主机A 192.168.88.2和主机B 192.168.88.3之间流量的责任。主机A和B上的所有ARP缓存条目将引用路由器的MAC地址。因此路由器对整个子网192.168.88.0/24执行本地代理arp。

RouterOS local-proxy-arp的一个例子是一个带有DHCP服务器和隔离的网桥端口的网桥设置，来自同一子网的主机只能通过网桥IP在第三层相互联系。

```shell
/interface bridge
add arp=local-proxy-arp name=bridge1
/interface bridge port
add bridge=bridge1 horizon=1 interface=ether2
add bridge=bridge1 horizon=1 interface=ether3
add bridge=bridge1 horizon=1 interface=ether4
```

# 无偿ARP

在RouterOS中可以创建 "无偿ARP "请求。要做到这一点，必须使用流量生成器工具，下面是如何生成一个无偿ARP请求以更新远程设备上ARP表的例子：

```shell
/tool traffic-generator inject interface=ether2 \
data="ffffffffffff4c5e0c14ef78080600010800060400014c5e0c14ef780a057a01ffffffffffff0a057a01000000000000000000000000000000000000"
```

必须把MAC地址（4c5e0c14ef78）和IP地址（0a057a01）改为路由器的地址。IP地址和MAC地址必须是来自请求ARP表更新的设备。还需要指定想通过哪个接口（ether2）来发送无偿ARP请求。确保接收设备支持无偿ARP请求。