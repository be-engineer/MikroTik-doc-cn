# 标签范围和TTL

从“/mpls设置”菜单中，可以分配特定的动态标签范围和TTL传播。如果由于某种原因使用了静态标签映射，则可以调整动态范围，以排除任何标签分发协议动态分配静态分配的标签号。

| 属性                                                                               | 说明                                                                                                                                                    |
| ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **dynamic-label-range** (_range of integer[16..1048575]_; Default: **16-1048575**) | 用于动态分配的标签号范围。前16个标签保留用于特殊用途(如RFC中定义的)。如果您打算静态配置标签，那么调整动态默认范围，使其不包括将在静态配置中使用的数字。 |
| **propagate-ttl** (_yes\| no_;Default:**yes**)                                     | 是否将TTL值从IP头复制到MPLS头。如果将此选项设置为 **no**，则MPLS云中的跳将对traceroutes不可见。                                                         |
| **allow-fast-path**(_yes\| no_;Default:**yes)**                                    | 开启/关闭MPLS快速路径支持                                                                                                                               |

# MPLS MTU

配置MPLS MTU(路径MTU + MPLS标签大小)在路径上可能存在多种MTU的情况下非常有用。将MPLS MTU配置为可以通过所有跳数的最小值，可以保证MPLS报文在MTU不够大的设备上不会被静默丢弃。

通过“/MPLS interface”菜单配置MPLS mtu。

```shell
[admin@rack1_b35_CCR1036] /mpls/interface> print
Flags: X - disabled; * - builtin
 0    ;;; router-test
      interface=ether1 mpls-mtu=1580 input=yes
 
 1    ;;; router-test
      interface=ether2 mpls-mtu=1580 input=yes
 
 2    interface=all mpls-mtu=1500
```

  

**属性**

| 属性                                                   | 说明                                                   |
| ------------------------------------------------------ | ------------------------------------------------------ |
| **comment** (_string_;Default:)                        | 接口的简短描述                                         |
| **disabled** (_yes\| no_;Default:**no**)               | 如果设置为 **yes**，则忽略此配置。                     |
| **interface** (_name_;Default:)                        | 要匹配的接口名或接口列表名。                           |
| **input** (_yes \| no_;Default:**yes**)                | 接口是否允许MPLS输入                                   |
| **mpls-mtu** (_integer [512. 65535]_;Default:**1508**) | 该选项表示在添加MPLS标签的接口上可以携带多大的数据包。 |

  

列出的条目是有序的，与接口匹配的第一个条目(从上到下迭代)将被使用。

条目的顺序很重要，因为不同的接口列表可能包含相同的接口，此外，该接口可以被直接引用。

MPLS MTU的选择有以下几个步骤:

- 如果接口匹配该表项，则尝试使用配置的MPLS MTU值
- 如果接口没有匹配到任何表项，则认为MPLS MTU等于L2MTU
- 如果接口不支持L2MTU，则认为MPLS MTU等于L3 MTU

在MPLS入接口路径上，MTU用min(MPLS MTU - tagsize, l3mtu)来选择。这意味着在不支持L2MTU和默认L3 MTU设置为1500的接口上，最大路径MTU将是1500 -标签大小(接口将无法通过完整的IP帧而不分片)。在这种情况下，L3MTU必须增加到最大观察到的标签大小。

在 [RouterOS中的MTU](https://help.mikrotik.com/docs/display/ROS/MTU+in+RouterOS) 文章中阅读更多关于MTU的信息。

  

## 转发表

'/mpls forwarding-table'菜单中的表项显示用于mpls标签交换的特定路由的标签绑定。此菜单中的属性是只读的。

```shell
[admin@rack1_b35_CCR1036] /mpls/forwarding-table> print
Flags: L, V - VPLS
Columns: LABEL, VRF, PREFIX, NEXTHOPS
#   LABEL  VRF   PREFIX         NEXTHOPS                                           
0 L    16  main  10.0.0.0/8     { nh=10.155.130.1; interface=ether12 }             
1 L    18  main  111.111.111.3  { label=impl-null; nh=111.12.0.1; interface=ether2 }
2 L    17  main  111.111.111.2  { label=impl-null; nh=111.11.0.1; interface=ether1 }
```

  

| 属性                      | 说明                                                                                                                                                                  |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **prefix** (_IP/Mask_)    | 指定标签的目的前缀                                                                                                                                                    |
| **label** (_integer_)     | 入接口MPLS标签                                                                                                                                                        |
| **ldp** (_yes\| no_)      | 标签是否有 [ldp](https://help.mikrotik.com/docs/display/ROS/LDP) 信号                                                                                                 |
| **nexthops** ()           | 下一跳的数组，数组中的每个表项代表一个ECMP下一跳。数组条目可以包含几个参数:<br>- **label** -出接口MPLS标签<br>- **nh** - out下一跳IP地址<br>- **interface** -输出接口 |
| **out-label** (_integer_) | 为出包添加或切换的标签号。                                                                                                                                            |
| **packets** (_integer_)   | 此表项匹配的数据包数                                                                                                                                                  |
| **te-sender**             |                                                                                                                                                                       |
| **te-session**            |                                                                                                                                                                       |
| **Traffic -eng**          | 显示条目是否由RSVP-TE (Traffic Engineering)发出信号                                                                                                                   |
| **type** _(string)_       | 表项类型，如“vpls”等                                                                                                                                                  |
| **vpls** (_yes \| no_)    | 显示该表项是否用于 [vpls](https://help.mikrotik.com/docs/display/ROS/VPLS) 隧道。                                                                                     |
| **vpn**                   |                                                                                                                                                                       |
| **vrf**                   | 该表项所属vrf表名                                                                                                                                                     |