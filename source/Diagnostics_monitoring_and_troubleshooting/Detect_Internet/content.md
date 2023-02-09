# 介绍

互联网探测是一个工具，它把监测的接口分类为以下状态-- **互联网**、**WAN**、**LAN**、**未知** 和 **无链接**。

## 状态

子菜单显示由 _detect-interface-list_ 参数定义的所有监测接口的状态。

`interface/detect-internet/state/print`

## LAN

所有二层接口最初都有这种状态。

## WAN

任何L3隧道和LTE接口最初都会有这个状态。在以下情况下，二层接口可以获得这种状态：

- 一个接口在主路由表里有一个到8.8.8.8的活动路由。
- 一个接口从DHCP获得（或已经获得）一个地址（如果DHCP服务器也在DHCP服务器接口上运行Detect Internet则不适用）。

广域网接口只有在链路状态改变时才能回到局域网状态。局域网接口在1小时后被锁定为局域网，然后只在链路状态改变时才改变。

## 互联网

能够使用UDP协议端口30000到达cloud.mikrotik.com的 _WAN_ 接口可以获得这种状态。每分钟都会检查可达性。如果3分钟内没有到达云端，状态就会退回到 **WAN**。

### 配置

`/interface detect-internet`

| 属性                                                              | 说明                                       |
| ----------------------------------------------------------------- | ------------------------------------------ |
| **detect-interface-list** (_interface list_; Default: **none**)   | 列表中的所有接口都被Detect Internet监控。  |
| **internet-interface-list** (_interface list_; Default: **none**) | 有互联网状态的接口将被动态地添加到列表中。 |
| **lan-interface-list** (_interface list_; Default: **none**)      | 有Lan状态的接口将被动态地添加到列表中。    |
| **wan-interface-list** (_interface list_; Default: **none**)      | 有Wan状态的接口将被动态地添加到列表中。    |

```shell
[admin@MikroTik] > interface/detect-internet/print
detect-interface-list: none
lan-interface-list: none
wan-interface-list: none
internet-interface-list: none
[admin@MikroTik] > interface/detect-internet/set internet-interface-list=all wan-interface-list=all lan-interface-list=all detect-interface-list=all
[admin@MikroTik] > interface/detect-internet/state/print
Columns: NAME, STATE, STATE-CHANGE-TIME, CLOUD-RTT
# NAME STATE STATE-CHANGE-TIME CLO
0 ether1 internet dec/22/2020 13:46:18 5ms
```
