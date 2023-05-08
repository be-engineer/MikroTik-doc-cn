<!--
 * @Author: be-engineer 41234995@qq.com
 * @Date: 2023-05-04 21:55:23
 * @LastEditors: be-engineer 41234995@qq.com
 * @LastEditTime: 2023-05-05 21:46:30
 * @FilePath: /MikroTik-doc-cn/source/Firewall_and_Quality_of_Service/UPnP/content.md
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
# 介绍

MikroTik RouterOS支持通用即插即用架构，用于个人电脑和支持网络的智能设备或电器的透明对等网络连接。

UPnP使任何两个设备在网络上任何控制设备的命令下进行数据通信。通用即插即用完全独立于任何特定的物理介质。无需任何初始配置就能自动发现的网络，据此，设备可以动态地加入一个网络。DHCP和DNS服务器是可选的，如果网络上有，就会使用。UPnP实现了一个简单而强大的NAT穿越解决方案，使客户能够从NAT后面获得完全的双向对等网络支持。

UPnP有两种接口类型。内部（本地客户连接的接口）和外部（互联网连接的接口）。一个路由器只能有一个活动的外部接口，上面有一个"公共"IP地址，并根据需要有许多内部接口，都有源NAT的 "内部"IP地址。该协议通过创建动态NAT条目工作。

UPnP协议用于许多现代应用，如大多数DirectX游戏，以及各种Windows Messenger功能，如远程协助、应用共享、文件传输、语音、防火墙后的视频。

## 配置

### 常规属性

`/ip upnp`

| 属性                                                                                             | 说明                                                                                                                                                                                                                                                         |
| ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **allow-disable-external-interface** (_yes                            \| no_ ; Default: **yes**) | 是否允许用户禁用路由器的外部接口。这个功能（让用户能够在没有任何认证的情况下关闭路由器的外部接口）是标准所要求的，但由于在UPnP部署中有时并不期望或不需要这个功能，而这个标准并不是为其设计的（它主要是为家庭用户建立自己的本地网络而设计），可以禁用这个行为 |
| **enabled** (_yes                          \| no_ ; Default: **no**)                             | 启用UPnP服务                                                                                                                                                                                                                                                 |
| **show-dummy-rule** (_yes                  \| no_ ; Default: **yes**)                            | 启用一个解决方法以应对一些破损的实现，这些实现正在错误地处理没有UPnP规则的情况（例如，弹出错误信息）。这个选项指示服务器安装一个假的（无意义的）UPnP规则，可以被客户端观察到，否则会拒绝正确工作                                                             |

如果没有禁用 **允许禁用外部接口**，任何来自本地网络的用户都可以（无需任何认证程序）禁用路由器的外部接口。

### UPnP 接口

`/ip upnp interface`

| 属性                                                               | 说明                                                                                                               |
| ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------ |
| **interface** (_string_; Default: )                                | 运行uPnP的接口名称                                                                                                 |
| **type** (_external                 \| internal_; Default: **no**) | UPnP接口类型：<br>- external （外部）- 全局IP地址分配的接口<br>- internal （内部）- 客户端连接到路由器的本地接口。 |
| **forced-external-ip** (_Ip_; Default: )                           | 如果外部接口有多个IP可用，允许指定使用哪个公共IP。                                                                 |

在带有VLAN的更复杂的设置中，VLAN接口被认为是LAN接口，VLAN接口本身应被指定为内部接口，使UPnP正常工作。

## 配置实例

![](https://help.mikrotik.com/docs/download/attachments/24805490/UPnP.png?version=2&modificationDate=1587632829058&api=v2)

路由器上已经启用了伪装功能:

```shell
[admin@MikroTik] ip upnp> /ip firewall src-nat print
Flags: X - disabled, I - invalid, D - dynamic
  0   chain=srcnat action=masquerade out-interface=ether1
[admin@MikroTik] ip upnp>
```

启用UPnP特性:

```shell
[admin@MikroTik] ip upnp> set enable=yes
[admin@MikroTik] ip upnp> print
                             enabled: yes
    allow-disable-external-interface: yes
                     show-dummy-rule: yes
[admin@MikroTik] ip upnp>
```

现在要做的就是添加接口:

```shell
[admin@MikroTik] ip upnp interfaces> add interface=ether1 type=external
[admin@MikroTik] ip upnp interfaces> add interface=ether2 type=internal
[admin@MikroTik] ip upnp interfaces> print
Flags: X - disabled
  #   INTERFACE TYPE
  0 X ether1    external
  1 X ether2    internal
 
[admin@MikroTik] ip upnp interfaces> enable 0,1
```

现在，一旦客户端从内部接口一侧发送UPnP请求，动态NAT规则将在路由器上创建，示例规则看起来类似以下内容:

```shell
[admin@MikroTik] > ip firewall nat print
Flags: X - disabled, I - invalid, D - dynamic
 
0 chain=srcnat action=masquerade out-interface=ether1
 
1 D ;;; upnp 192.168.88.10: ApplicationX
chain=dstnat action=dst-nat to-addresses=192.168.88.10 to-ports=55000 protocol=tcp
dst-address=10.0.0.1 in-interface=ether1 dst-port=55000
 
2 D ;;; upnp 192.168.88.10: ApplicationX
chain=dstnat action=dst-nat to-addresses=192.168.88.10 to-ports=55000 protocol=udp
dst-address=10.0.0.1 in-interface=ether1 dst-port=55000
```
