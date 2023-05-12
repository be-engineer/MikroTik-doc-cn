# 概述

microtik RouterOS实现RIP version 2 (RFC 2453)。不支持Version 1 (RFC 1058)。

RIP使自治系统中的路由器能够相互交换路由信息。它总是使用可用的最佳路径(跳数最少的路径(即路由器))。

## 常规

**Sub-menu:** `/routing rip instance`

| 属性                                                                                                     | 说明                                                                               |
| -------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| **name**                                                                                                 | 实例名                                                                             |
| **vrf**(Default:**main**)                                                                                | 使用哪个 [vrf](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206) |
| **afi** (_ipv4 \| ipv6_;Default:)                                                                        | 指定使用哪个afi。                                                                  |
| **in-filter-chain**(Default:)                                                                            | 输入过滤器链                                                                       |
| **out-filter-chain**(Default:)                                                                           | 输出过滤器链                                                                       |
| **out-filter-select**(Default:)                                                                          | 输出过滤器选择规则链                                                               |
| **redistribute** (_bgp, bgp-mpls-vpn, connected, dhcp, fantasy, modem, ospf, rip, static, vpn_;Default:) | 重新分发哪些路由                                                                   |
| **originate- Default** (Default:)                                                                        | 是否发起默认路由                                                                   |
| **routing-table**(Default:main)                                                                          | 在该路由表中添加路由                                                               |
| **route-timeout**(Default:)                                                                              | 路由超时                                                                           |
| **route-gc-timeout**(Default:)                                                                           |                                                                                    |
| **update-interval** (_time_;Default:)                                                                    | 指定时间间隔，超过该时间间隔，路由将被视为无效                                     |

**备注:** RIP路由的最大度量值为15。大于15的度量值被认为是“无穷大”，具有该度量值的路由被认为是不可达的。因此，RIP不能用于任何两个路由器之间的跳数超过15的网络，使用大于1的重分发度量会进一步减少这个最大跳数。

## 接口

**Sub-menu:** `/routing rip interface-template`

| 属性                            | 说明                                                                               |
| ------------------------------- | ---------------------------------------------------------------------------------- |
| **name**                        | 实例名                                                                             |
| **instance**                    | 使用哪个 [VRF](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206) |
| **interfaces**                  | 指定使用哪个afi。                                                                  |
| **source-addresses**            | 输入过滤器链                                                                       |
| **cost**(Default:)              | 输出过滤器链                                                                       |
| **split-horizon** (_no\| yes_)  |                                                                                    |
| **poison-reverse** (_no\| yes_) |                                                                                    |
| **mode** (_passive\| strict_)   |                                                                                    |
| **key-chain** (_name_)          | key-chain名称                                                                      |
| **password**                    | 密码                                                                               |
  
**Sub-menu:** `/routing rip interface`

只读属性:

| 属性                              | 说明           |
| --------------------------------- | -------------- |
| **instance** (_name)              | 实例名         |
| **address** (_address%interface_) | IP地址和接口名 |

## 邻居

**Sub-menu:** `/routing rip neighbor`

该子菜单用于定义邻居路由器，以便与之交换路由信息。通常情况下，如果组播在网络中正常工作，则不需要添加邻居。如果路由信息交换有问题，可以将邻居路由器加入到列表中。它将强制路由器使用常规的单播报文与邻居交换路由信息。

只读属性:

| 属性                       | 说明               |
| -------------------------- | ------------------ |
| **address** (_IP address_) | 邻居路由器的IP地址 |
| **routes**                 | 路由数量           |
| **packets-total**          | 所有数据包总数     |
| **packets-bad**            | 坏包数量           |
| **entries-bad**            | 错误条目数量       |
| **last-update** (_time_)   | 上次更新的时间     |

**Sub-menu:** `/routing rip static-neighbor`

| 属性                       | 说明               |
| -------------------------- | ------------------ |
| **instance** (name)        | 使用的实例名称     |
| **address** (_IP address_) | 邻居路由器的IP地址 |

## 密钥

**Sub-menu:** `/routing rip keys`

MD5认证密钥链。

| 属性                                                               | 说明                                                                                   |
| ------------------------------------------------------------------ | -------------------------------------------------------------------------------------- |
| **chain** (_string_;Default:**""**)                                | 放置此密钥的链名。                                                                     |
| **key** (_string_;Default:**""**)                                  | 认证密钥。最大长度16个字符                                                             |
| **key-id** (_integer:0..255_;Default:)                             | 密钥标识符。该数字包含在经过MD5验证的RIP消息中，并决定使用哪个密钥对特定消息进行验证。 |
| **valid-from** (_date and time_;Default:今天的日期和时间:00:00:00) | 密钥从这个日期和时间开始生效                                                           |
| **valid-till** (_date and time_;Default:今天的日期和时间:00:00:00) | 密钥在此日期和时间之前有效                                                             |
