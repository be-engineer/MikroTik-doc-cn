# 概述

邻居发现协议允许在Layer2广播域中找到与MNDP (MikroTik邻居发现协议)，CDP (Cisco发现协议)或LLDP(链路层发现协议)兼容的设备。它可以用来规划你的网络。

# 邻居列表

邻居列表显示二层广播域中所有已发现的邻居。它显示连接到哪个接口邻居，它的IP/MAC地址，以及其他相关参数。该列表是只读的，邻居列表的示例如下:

```shell
[admin@MikroTik] /ip neighbor print
 # INTERFACE ADDRESS         MAC-ADDRESS       IDENTITY   VERSION    BOARD     
 0 ether13   192.168.33.2    00:0C:42:00:38:9F MikroTik   5.99       RB1100AHx2
 1 ether11   1.1.1.4         00:0C:42:40:94:25 test-host  5.8        RB1000  
 2 Local     10.0.11.203     00:02:B9:3E:AD:E0 c2611-r1   Cisco I...                   
 3 Local     10.0.11.47      00:0C:42:84:25:BA 11.47-750  5.7        RB750 
 4 Local     10.0.11.254     00:0C:42:70:04:83 tsys-sw1   5.8        RB750G   
 5 Local     10.0.11.202     00:17:5A:90:66:08 c7200      Cisco I...
```

**Sub-menu:** `/ip neighbor`

| 属性                                                                    | 说明                                                       |
| ----------------------------------------------------------------------- | ---------------------------------------------------------- |
| **address** (_IP_)                                                      | 发现设备配置的最高IP地址                                   |
| **address6** (_IPv6_)                                                   | 发现设备上配置的IPv6地址                                   |
| **age** (_time_)                                                        | 距离上次发现数据包的时间间隔                               |
| **discovered-by** (_cdp \| lldp\| mndp_)                                | 显示邻居被发现的协议列表。该属性从RouterOS 7.7版开始可用。 |
| **board** (_string_)                                                    | RouterBoard模型。仅对安装了RouterOS的设备显示              |
| **identity** (_string_)                                                 | 配置的系统标识                                             |
| **interface** (_string_)                                                | 发现设备所连接的接口名                                     |
| **Interface -name** (_string_)                                          | L2广播域连接的邻居设备的接口名称。适用于CDP。              |
| **ipv6** (_yes\| no_)                                                   | 显示设备是否使能IPv6。                                     |
| **Mac -address** (_MAC_)                                                | 远端设备的Mac地址。可用于与mac-telnet连接。                |
| **platform** (_string_)                                                 | 平台名。例如“microtik”、“cisco”等                          |
| **software- ID** (_string_)                                             | 远端设备的RouterOS软件ID。仅适用于安装了RouterOS的设备。   |
| **System -caps** (_string_)                                             | 链路层发现协议(LLDP)报告的系统能力。                       |
| **system-caps- Enabled** (_string_)                                     | 链路层发现协议(LLDP)报告的启用的系统能力。                 |
| **unpack** (_none \| simple\| uncompressed-headers\| uncompressed-all_) | 显示发现报文的压缩类型。                                   |
| **uptime** (_time_)                                                     | 远端设备的正常运行时间。仅对安装了RouterOS的设备显示。     |
| **version** (_string_)                                                  | 远程设备上安装的软件版本号                                 |

从RouterOS v6.45开始，为了避免内存耗尽，每个接口的邻居表项数量被限制为(总RAM(兆字节))*16。

# 发现配置

使用interface列表可以改变接口是否参与邻居发现。如果该接口被包含在发现接口列表中，则该接口将发送系统的基本信息，并处理接收到的在二层网络中广播的发现报文。将接口从接口列表中删除，将使该接口无法发现邻居，也无法在该接口上发现该设备本身。

`/ip neighbor discovery-settings`

  

| 属性                                                                    | 说明                                                                                                                                                                                                                                                                                                                                                                                          |
| ----------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ** find -interface-list** (_string_;Default:**static**)                 | 发现协议将在其上运行的接口列表                                                                                                                                                                                                                                                                                                                                                                |
| **lldp-med-net-policy-vlan** (_integer 0..4094_; Default: **disabled**) | LLDP-MED网络策略TLV发布的VLAN ID。允许为支持LLDP-MED的设备(如VoIP电话)分配VLAN ID。只有发现了支持LLDP-MED的设备的接口才会添加TLV。其他TLV值是预定义的，不能修改:<br>- 应用类型—语音<br>- VLAN类型<br>- L2优先级- 0<br>- DSCP优先级- 0<br>当与网桥接口配合使用时，(R/M)STP协议应启用protocol-mode设置。<br>另外，为了避免LLDP-MED配置错误，应该使用“protocol”设置排除其他邻居发现协议(如CDP)。 |
| **mode** (_rx-only \| tx-only \| tx-and-rx_; Default: **tx-and-rx**)    | 选择邻居发现报文的发送和接收方式。该配置从RouterOS 7.7版开始生效。                                                                                                                                                                                                                                                                                                                            |
| **protocol** (_cdp \| lldp \| mndp_; Default: **cdp,lldp,mndp**)        | 使用的发现协议列表                                                                                                                                                                                                                                                                                                                                                                            |

从RouterOS v6.44开始，邻居发现工作在单独的从接口上。当一个主接口(如bonding或bridge)被包含在发现接口列表中时，它的所有从接口将自动参与邻居发现。可能只允许对某些从接口发现邻居。为此，请在列表中包括特定的从接口，并确保不包括主接口。

```shell
/interface bonding
add name=bond1 slaves=ether5,ether6
/interface list
add name=only-ether5
/interface list member
add interface=ether5 list=only-ether5
/ip neighbor discovery-settings
set discover-interface-list=only-ether5
```

现在，邻居列表显示了接收到发现消息的主接口和实际的从接口。

```shell
[admin@R2] > ip neighbor print
 # INTERFACE ADDRESS                                           MAC-ADDRESS       IDENTITY   VERSION    BOARD        
 0 ether5    192.168.88.1                                      CC:2D:E0:11:22:33 R1         6.45.4 ... CCR1036-8G-2S+
   bond1
```

# LLDP

根据RouterOS的配置，可以在LLDP报文中发送不同的TLV (type-length-value)，包括:

- 机箱子类型(MAC地址)
- 端口子类型(接口名称)
- 生存时间
- 系统名称(系统标识)
- 系统描述(平台—MikroTik、软件版本—RouterOS版本、硬件名称—RouterBoard名称)
- 管理地址(端口上配置的所有IP地址)
- 系统功能(启用的系统功能，例如网桥或路由器)
- LLDP-MED媒体功能(MED功能列表)
- LLDP-MED网络策略(为语音流量分配VLAN ID)
- 端口扩展(端口扩展器和控制器桥通告)
- LLDPDU结束
  