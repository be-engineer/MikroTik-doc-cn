# 介绍

RouterOS中的MLAG（多机箱链路聚合组）允许在两个独立的设备上配置LACP绑定，而客户设备认为是连接到同一台机器上。这在交换机发生故障的情况下提供了物理冗余。所有的CRS3xx、CRS5xx系列交换机和CCR2116、CCR2216设备都可以使用RouterOS V7配置MLAG。

两个对等体使用ICCP（机箱间控制协议）建立MLAG接口并通过 `peer-port` 更新网桥主机表。RouterOS ICCP不需要IP配置，但要用一个专用的无标记VLAN和网络的其他部分隔离。这个无标记的VLAN可以用 `vlan-filtering` 和 `pvid` 来配置。对等端口也可以配置为LACP绑定接口。

当 `peer-port` 运行并建立ICCP时，发生主设备选举动作。有最低网桥MAC地址的对等体会作为主设备，`system-id` 被选中。这个 `system-id ` 用于 STP BPDU 网桥标识和 LACP 系统标识。MLAG要启用STP或RSTP协议，不支持MSTP。在两个节点上的双连接网桥端口使用相同的 STP 优先级和相同的 STP 配置。当 MLAG 网桥选为 STP 根节点时，两台设备在网桥监控器下都会显示为根节点。

MLAG与 [L3硬件卸载](https://help.mikrotik.com/docs/display/ROS/L3+Hardware+Offloading) 不兼容。当使用 MLAG 时，L3 硬件卸载必须禁用。

![](https://help.mikrotik.com/docs/download/attachments/67633179/1.png?version=1&modificationDate=1621431547740&api=v2)

## 快速设置

在这个例子中，CRS317和CRS309设备用作MLAG对等体，任何有两个SFP+接口的设备都可以用作LACP客户端。SFP+1接口在两个对等节点上用于创建 **对等端口** ，用于ICCP，见下面的网络方案。

![](https://help.mikrotik.com/docs/download/attachments/67633179/2.png?version=1&modificationDate=1621431568977&api=v2)

以下是在RouterOS中为客户端设备创建常规 [LACP绑定](https://help.mikrotik.com/docs/display/ROS/Bonding#Bonding-802.3ad) 的配置命令:

`/interface bonding`

`add mode =802.3ad name =bond1 slaves =sfp-sfpplus1,sfp-sfpplus2`

接下来，在Peer1和Peer2设备上配置MLAG绑定接口，在两个对等设备上使用匹配的 `mlag-id` 设置:

`/interface bonding`

`add mlag-id =10 mode =802.3ad name =client-bond slaves =sfp-sfpplus2`

`/interface bonding`

`add mlag-id =10 mode =802.3ad name =client-bond slaves =sfp-sfpplus2`

在配置网桥时启用 `vlan-filtering`，将需要的接口作为网桥端口。专用的无标记VLAN应用于对等端口的机箱间通信，要用不同的 `pvid` 设置。下面是Peer1和Peer2设备的配置命令:

`/interface bridge`

`add name =bridge1 vlan-filtering =yes`

`/interface bridge port`

`add bridge =bridge1 interface =sfp-sfpplus1 pvid =99`

`add bridge =bridge1 interface =client-bond`

`/interface bridge`

`add name =bridge1 vlan-filtering =yes`

`/interface bridge port`

`add bridge =bridge1 interface =sfp-sfpplus1 pvid =99`

`add bridge =bridge1 interface =client-bond`

MLAG需要启用STP或RSTP协议，不支持MSTP。在两个节点的双连接桥接端口上使用相同的STP优先级和相同的STP配置。

在这个例子中，客户端绑定的接口使用默认的无标记VLAN 1（默认 `pvid=1` ）。为了通过对等端口发送数据包，需要把它们添加为有标签的 VLAN 1 成员。注意，对等端口的默认 `pvid` 值在上一步已经改变了，重要的是把对等端口包括在其他网桥端口使用的所有VLAN中，包括无标记和有标记的VLAN。下面是两个对等设备的配置命令:

`/interface bridge vlan`

`add bridge =bridge1 tagged =sfp-sfpplus1 vlan-ids =1`

`/interface bridge vlan`

`add bridge =bridge1 tagged =sfp-sfpplus1 vlan-ids =1`

所有用于桥接从属端口的VLAN必须同时配置为peer-port的标记VLAN，这样peer-port就是这些VLAN的成员，可以转发数据。

最后，指定“bridge“ 和“peer-port“启用MLAG。下面是两个对等设备的配置命令:

`/interface bridge mlag`

`set bridge =bridge1 peer-port =sfp-sfpplus1`

`/interface bridge mlag`

`set bridge =bridge1 peer-port =sfp-sfpplus1`

此外，检查对等设备上的MLAG状态，确保客户端LACP的两个接口都处于活动状态。

```shell
[admin@Peer1] > /interface/bridge/mlag/ monitor   
       status : connected
    system-id : 74:4D:28:11:70:6B`
  active-role : primary
[admin@Peer2] > /interface/bridge/mlag/ monitor          
       status : connected
    system-id : 74:4D:28:11:70:6B
  active-role : secondary
[admin@Client] > /interface bonding monitor bond1
                    mode : 802.3ad
            active-ports : sfp-sfpplus1,sfp-sfpplus2
          inactive-ports :
          lacp-system-id : 74:4D:28:7B:7F:96
    lacp-system-priority : 65535
  lacp-partner-system-id : 74:4D:28:11:70:6C
```

## MLAG settings and monitoring

This section describes the available MLAG settings and monitoring options.

**Sub-menu:** `/interface bridge mlag`

| 属性                                           | 说明                                                                                                                                                                                     |
| ---------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **bridge** (_interface;_ Default: **none**)    | 正在创建 MLAG 的桥接口。                                                                                                                                                                 |
| **peer-port** (_interface;_ Default: **none**) | 将被用作对等端口的接口。两个对等设备都通过这些对等端口使用机箱间的通信来建立MLAG并更新主机表。对等端口应该使用 `pvid` 设置在不同的无标记VLAN上进行隔离。对等端口可以配置为一个绑定接口。 |

使用 `monitor` 命令查看当前MLAG状态。

```shell
[admin@Peer1] > /interface/bridge/mlag/monitor   
       status: connected
    system-id: 74:4D:28:11:70:6B
  active-role: primary
```

| 属性                                               | 说明                                                                                                    |
| -------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| **status** (_connected \| connecting \| disabled_) | MLAG状态。                                                                                              |
| **system-id** (_MAC address_)                      | 两个对等桥的最低MAC地址将用作 "system-id"。这个 "system-ID "用于(R)STP BPDU网桥标识和LACP系统ID。       |
| **active-role** (_primary \| secondary_)           | 有最低网桥MAC地址的对等设备会作为主设备。主设备的 "system-id "用来发送(R)STP BPDU网桥标识和LACP系统ID。 |

**Sub-menu:** `/interface bonding`

| 属性                                             | 说明                                                                                                                   |
| ------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------- |
| **mlag-id** (_integer: 0..4294967295_; Default:) | 更改绑定接口的MLAG ID。两个对等设备上应该使用相同的MLAG ID，以便为客户设备创建一个LAG。`peer-port` 不能配置为MLAG ID。 |

LACP绑定接口和绑定从属端口可以用 `monitor` 和 `monitor-slaves` 命令监控。更多细节见 [Bonding monitoring](https://help.mikrotik.com/docs/display/ROS/Bonding#Bonding-Bondingmonitoring)。
