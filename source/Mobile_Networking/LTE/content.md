## 概述

`Package: system`

只支持Direct-IP模式类型的卡。MBIM支持在RouterOS v7版本中可用，MBIM驱动会自动加载。如果调制解调器在RouterOS v6中没有被识别 - 请在RouterOS v6中要求支持之前在v7版本中进行测试。

要启用通过PPP接口而不是LTE接口的访问，请用 `/port firmware set ignore-directip-modem=yes` 命令改变Direct-IP模式，并重新启动。请注意，使用PPP模拟模式可能无法获得与使用LTE接口模拟类型相同的吞吐速度。 

对于RouterOS v7 ignore-direct-modem参数更名为 "模式"，并移至 `/interface lte settings` 菜单。

## LTE客户端

`Sub-menu: /interface lte`

### 属性

| 属性                                              | 说明                                                                                                                                                                                  |
| ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **allow-roaming** (_yes\| no_; Default: **no**)   | 启用数据漫游功能，以便连接到其他国家的数据供应商。并非所有LTE调制解调器都支持这一功能。一些不完全支持该功能的调制解调器将连接到网络，但在允许漫游设置为 "否 "时，不会建立IP数据连接。 |
| **apn-profiles** (_string_; Default: **default**) | 这个接口要使用哪个APN配置文件。                                                                                                                                                       |
| **band** (_integer list_; Default: **""**)        | 通讯中使用的LTE频段 [LTE频段和带宽](https://en.wikipedia.org/wiki/LTE_frequency_bands#Frequency_bands_and_channel_bandwidths)。                                                       |
| **nr-band** (_integer list_; Default: "")         | 5G NR 用于通信的频段 [5G NR频段和带宽](https://en.wikipedia.org/wiki/5G_NR_frequency_bands)。                                                                                         |
| **comment** (_string_; Default: **""**)           | 项目的描述名称                                                                                                                                                                        |
| **disabled** (_yes \| no_; Default: **yes**)      | 接口是否被禁用。默认是禁用的。                                                                                                                                                        |
| **modem-init** (_string_; Default: **""**)        | 调制解调器初始字符串（调制解调器启动时将执行的AT命令）。                                                                                                                              |
| **mtu** (_integer_; Default: **1500**)            | 最大传输单元。LTE接口在没有数据包碎片的情况下能够发送的最大数据包大小。                                                                                                               |
| **name** (_string_; Default: **""**)              | 接口的描述名称。                                                                                                                                                                      |
| **network-mode** (_3g \| gsm \| lte\| 5g_)        | 选择或增强LTE接口的工作模式。                                                                                                                                                         |
| **operator** (_integer_; Default: **""**)         | 用于锁定设备到特定的运营商，完整的PLMN号码用于锁定，由MCC+MNC组成。[PLMN代码](https://en.wikipedia.org/wiki/Public_land_mobile_network)                                               |
| **pin** (_integer_; Default: **""**)              | SIM卡的PIN码。                                                                                                                                                                        |

### APN配置文件

从RouterOS 6.41开始，所有与网络有关的设置都被移到配置文件下。

`Sub-menu: /interface lte apn`

| 属性                                                                | 说明                                                                                                                                         |
| ------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **add-default-route** (_yes \| no_)                                 | 是否添加默认路由转发所有通过LTE接口的流量                                                                                                    |
| **apn** (_string_)                                                  | 服务提供商的接入点名称                                                                                                                       |
| **authentication** (_pap\| chap\| none_; Default: **none**)         | 允许使用的认证协议                                                                                                                           |
| **default-route-distance** (_integer_; Default: **2**)              | 设置应用于自动创建的默认路由的距离值，如果也选择了add-default-route。默认情况下，LTE路由的距离为2，以使有线路由优先于LTE                     |
| **ip-type** (_ipv4 \| ipv4-ipv6\| ipv6_; Default: )                 | 要求的PDN类型                                                                                                                                |
| **ipv6-interface** (; Default: )                                    | 在其上发布IPv6前缀通告的接口                                                                                                                 |
| **name** (_string_; Default: )                                      | APN配置文件名称                                                                                                                              |
| **number** (_integer_; Default: )                                   | APN配置文件名称                                                                                                                              |
| **passthrough-interface** (; Default: )                             | 直通IP配置的接口（激活直通）                                                                                                                 |
| **passthrough-mac** (_MAC_; Default: **auto**)                       | 如果设置为自动，那么将从第一个数据包中学习MAC                                                                                                |
| **passthrough-subnet-selection** (_auto \| p2p_; Default: **auto**) | "auto "选择最小的子网，用于直通接口。"p2p "将直通接口的子网设置为/32，并从10.177.0.0/16范围内选择网关地址。网关地址保持不变，直到改变apn配置 |
| **password** (_string_; Default: )                                  | 如果任何认证协议处于活动状态，则使用密码                                                                                                     |
| **use-network-apn** (_yes\| no_; Default: **yes**)                  | 参数从RouterOS v7开始可用，仅用于MBIM调制解调器。如果设置为是，则使用网络提供的APN                                                           |
| **use-peer-dns** (_yes\| no_; Default: **yes**)                     | 如果设置为 "是"，则使用从LTE接口接收的DNS                                                                                                    |
| **user** (_integer_)                                                | 如果任何认证协议处于活动状态，则使用用户名                                                                                                   |

### 扫描器

可以用 `/interface lte scan` 命令扫描LTE接口。

可用的只读属性：

| 属性                                  | 说明                       |
| ------------------------------------- | -------------------------- |
| **duration** (_integer_)              | 扫描的持续时间，以秒为单位 |
| **freeze-frame-interval** (_integer_) | 数据打印间隔时间           |
| **number** (_integer_)                | 接口号码或名称             |

### 用户信息命令

可以用 `/interface lte info` 命令向LTE接口发送特殊的 "info "命令。在RouterOS v7中，命令被移到 `/interface lte monitor` 菜单。

#### 属性 (至6.40)

| 属性                                           | 说明                                              |
| ---------------------------------------------- | ------------------------------------------------- |
| **user-command** (_string_; Default: **""**)   | 向LTE卡发送命令以提取有用的信息，例如使用AT命令。 |
| **user-command-only** (_yes \| no_; Default: ) |                                                   |

### 用户at-chat命令

可以通过 `/interface lte at-chat` 命令向LTE接口发送用户定义的 "at-chat "命令。

```shell
[admin@MikroTik] > /interface lte at-chat lte1 input="AT*mrd_imei\?"                        
  output: *MRD_IMEI:356159060388208
 
OK
```

可以在脚本中使用 "at-chat "函数，将命令输出分配给变量。

```shell
[admin@MikroTik] > :global "lte_command" [/interface lte at-chat lte1 input="AT*mrd_imei\?" as-value ]
[admin@MikroTik] > :put $"lte_command"
output=*MRD_IMEI:356159060388208
 
OK
```

## 快速设置示例

从网络设置开始 -

本指南适用于从6.41开始的RouterOS版本

从网络设置开始 - 在LTE apn配置文件下添加新的连接参数（由网络供应商提供）：

`/interface lte apn add name=profile1 apn=phoneprovider.net authentication=chap password=web user=web`

选择为LTE连接新创建的配置文件：

`/interface lte set [find] apn-profiles=profile1`

LTE接口应出现运行（R）标志：

```shell
[admin@MikroTik] > /interface lte print
Flags: X - disabled, R - running
0 R name="lte1" mtu=1500 mac-address=AA:AA:AA:AA:AA:AA
```

从RouterOS=>6.41开始，DHCP客户端会自动添加。如果没有添加-请手动添加一个DHCP客户端到LTE接口：

`/ip dhcp-client add default-route-distance=1 disabled=no interface=lte1`

如果需要，为LTE接口添加NAT Masquerade获得互联网到本地网络：

`/ip firewall nat add action=masquerade chain=srcnat out-interface=lte1`

接口添加完毕后，可以用 "info "命令查看客户端获取了哪些参数（返回的参数取决于LTE硬件设备）：

```shell
[admin@MikroTik] > /interface lte info lte1 once 
status: call in progress
pin-status: no password required
functionality: full
manufacturer: Huawei Technologies Co., Ltd.
model: ME909u-521
revision: 12.631.07.01.00
current-operator: vodafone ES
current-cellid: 44436007
access-technology: Evolved 3G (LTE)
signal-strengh: -79 dBm
frame-error-rate: n/a
earfcn: n/a
imei: 860461024123456
imsi: 234012555034981
uicc: n/a
rssi: -79dBm
rsrp: -109dBm
rsrq: -13dB
sinr: -1dB
```

## Passthrough 示例

从RouterOS v6.41开始，一些LTE接口支持LTE Passthrough功能，IP配置直接应用于客户端设备。这样调制解调器固件负责IP配置，路由器只用来配置调制解调器的设置--APN、网络技术和IP类型。在这种配置下，路由器将不会从调制解调器获得IP配置。如果调制解调器支持IPv4和IPv6地址，LTE Passthrough调制解调器可以同时传递这两个地址。有些调制解调器支持多个APN，可以将每个APN的流量传递到一个特定的路由器接口。

穿透只对一个主机有效。路由器将自动检测第一个收到的数据包的MAC地址，并将其用于Passthrough。如果网络上有多个主机，可以将直通车锁定在一个特定的MAC上。在Passthrough提供IP的网络上的主机上，应该在该接口上启用DHCP-客户端。请注意，不可能通过公共lte IP地址或从被Passthrough使用的主机连接到LTE路由器。建议从LTE路由器到主机建立额外的连接，以达到配置目的。例如，在LTE路由器和主机之间建立vlan接口。

要启用Passthrough，需要在"/interface lte apn "菜单中输入一个新条目或改变默认条目。

并非所有芯片组都支持Passthrough。
  
举例说明。

要在ether1上配置Passthrough：

```shell
[admin@MikroTik] > /interface lte apn add apn=apn1 passthrough-interface=ether1
[admin@MikroTik] > /interface lte set lte1 apn-profiles=apn1
```

要在ether1主机00:0C:42:03:06:AB上配置直通车：

```shell
[admin@MikroTik] > /interface lte apn add apn=apn1 passthrough-interface=ether1 passthrough-mac=00:0C:42:03:06: AB
[admin@MikroTik] > /interface lte set lte1 apn-profiles=apn1
```

要在ether1和ether2上配置多个APN：

```shell
[admin@MikroTik] > /interface lte apn add apn=apn1 passthrough-interface=ether1
[admin@MikroTik] > /interface lte apn add apn=apn2 passthrough-interface=ether2
[admin@MikroTik] > /interface lte set lte1 apn-profiles=apn1,apn2
```

要为不同的接口配置相同的多个APN：

```shell
[admin@MikroTik] > /interface lte apn add name=interface1 apn=apn1
[admin@MikroTik] > /interface lte apn add name=interface2 apn=apn1 passthrough-interface=ether1
[admin@MikroTik] > /interface lte set lte1 apn-profiles=interface1
[admin@MikroTik] > /interface lte set lte2 apn-profiles=interface2
```

## 双SIM  

### 带有可切换SIM卡插槽的板子

| RouterBoard | Modem slot | SIM slots  | Switchable |
| ----------- | ---------- | ---------- | ---------- |
| RouterBoard | Modem slot | SIM slots  | Switchable |
| ---         | ---        | ---        | ---        |
| LtAP        | lower      | 2          | 3          | Y |
| LtAP        | upper      | 1          | N          |
| LtAP mini   |            | up \| down | Y          |
| SXT R       |            | a \|  b    | Y          |

SIM卡插槽切换命令

-   RouterOS v7

`/interface lte settings set sim-slot=down`

-   RouterOS v6 after 6.45.1

`/system routerboard modem set sim-slot=down`

-   RouterOS v6 pre 6.45.1:

`/system routerboard sim set sim-slot=down`

更多参考资料请见板块图、快速指南和用户手册。

### 使用实例

按照这个链接 [双卡应用](https://wiki.mikrotik.com/wiki/Dual_SIM_Application "Dual SIM Application") 可以看到如何在RouterOS脚本和调度程序的帮助下，根据漫游状态和接口状态的变化来改变SIM卡插槽。

## 技巧和窍门

本段包含其他功能和使用情况的信息。

### 使用小区信息查找设备位置

在使用R11e-LTE国际版卡（wAP LTE套件）的设备上，info命令下提供了一些额外的信息（从6.41rc61开始）。

```
   current-operator: 24701
                lac: 40
     current-cellid: 2514442
```

| 属性                                        | 说明                                                             |
| ------------------------------------------- | ---------------------------------------------------------------- |
| **current-operator** (_integer_; Default: ) | 包含MCC和MNC。例如：current-operator: 24701拆成： MCC=247 MNC=01 |
| **lac** (_integer_; Default: )              | 位置区域代码（LAC）                                              |
| **current-cellid** (_integer_; Default: )   | 站点识别码                                                       |

数值可用于在数据库中查找位置： [Cell Id Finder](https://cellidfinder.com/cells/findcell)

### 使用小区锁定

可以将R11e-LTE、R11e-LTE6和R11e-4G调制解调器和配备的设备锁定在准确的LTE塔上。LTE信息命令提供了当前使用的蜂窝电话塔信息：

```
         phy-cellid: 384
             earfcn: 1300 (band 3, bandwidth 20Mhz)
```

| 属性                                  | 说明                                |
| ------------------------------------- | ----------------------------------- |
| **phy-cellid** (_integer_; Default: ) | 当前使用的基站的物理小区标识（PCI） |
| **earfcn** (_integer_; Default: )     | 绝对无线电频率频道号                |

准确的信号塔位置以及可用的频段和其他信息可以从移动运营商或通过使用在线服务获得：[CellMapper](https://www.cellmapper.net/map)

通过使用这些获得的变量，可以向调制解调器发送AT命令，以便以当前格式锁定塔台：

**用于R11e-LTE和R11e-LTE6**。

```shell
AT*Cell=<mode>,<NetworkMode>,<band>,<EARFCN>,<PCI>

where

<mode> :
0 – Cell/Frequency disabled
1 – Frequency lock enabled
2 – Cell lock enabled

<NetworkMode>
0 – GSM
1 – UMTS_TD
2 – UMTS_WB
3 – LTE

<band>
Not in use, leave this blank

<EARFCN>
earfcn from lte info

<PCI>
phy-cellid from lte info
```

可以在以前使用的塔台上锁定调制解调器：

`/interface lte at-chat lte1 input="AT*Cell=2,3,,1300,384"`

对于R11e-LTE来说，所有设置的锁在重启或调制解调器复位后都会丢失。手机数据也可以从 "cell-monitor "收集。

对于 R11e-LTE6，小区锁定只适用于主频段，如果在同一频段上有多个频道，想把它锁定在一个特定的EARFCN上可能很有用。请注意，小区锁定不是针对特定频段的，对于ca频段，它也可以使用其他频段，除非使用频段锁定。

使用小区锁定，将主频段设置为1300 earfcn，并将第二个频道用于ca-band：

`/interface lte at-chat lte1 input="AT*Cell=2,3,,1300,138"`

现在它使用earfcn： 1300作为主通道：

```
         primary-band: B3@20Mhz earfcn: 1300 phy-cellid: 138
              ca-band: B3@5Mhz earfcn: 1417 phy-cellid: 138
```

你也可以反过来设置：

`/interface lte at-chat lte1 input="AT*Cell=2,3,,1417,138"`

现在用earfcn： 1417作为主通道：

```
         primary-band: B3@5Mhz earfcn: 1417 phy-cellid: 138
              ca-band: B3@20Mhz earfcn: 1300 phy-cellid: 138
```

对于 R11e-LTE6 调制解调器，在重新启动或调制解调器复位后，小区锁定信息不会丢失。要删除手机锁，请使用at-chat命令：

`/interface lte at-chat lte1 input="AT*Cell=0"`

**对R11e-4G**

```shell
AT%CLCMD=<mode>,<mode2>,<EARFCN>,<PCI>,<PLMN>
AT%CLCMD=1,1,3250,244,\"24705\"

where

<mode> :
0 – Cell/Frequency disabled
1 – Cell lock enabled

<mode2> :
0 - Save lock for first scan
1 - Always use lock 
(after each reset modem will clear out previous settings no matter what is used here)

<EARFCN>
earfcn from lte info

<PCI>
phy-cellid from lte info

<PLMN>
Mobile operator code
```

所有的PLMN代码都在 [这里](https://en.wikipedia.org/wiki/Mobile_country_code) ，变量也可以留空。

要将调制解调器锁定在小区--调制解调器需要处于非工作状态，对于 **R11e-4G** 调制解调器最简单的方法是在 "modem-init "字符串中添加CellLock行：

`/interface lte set lte1 modem-init="AT%CLCMD=1,1,3250,244,\"24705\""`

也可以通过列表而不是以下格式的塔信息来添加多个单元：

```
AT%CLCMD=<mode>,<mode2>,<EARFCN_1>,<PCI_1>,<PLMN_1>,<EARFCN_2>,<PCI_2>,<PLMN_2>
```

例如，在同一频段和运营商内锁定到两个不同的PCI：

`/interface lte set lte1 modem-init="AT%CLCMD=1,1,6300,384,\"24701\",6300,385,\"24701\""`

**用于Chateau LTE12、Chateau 5G和LHG LTE18**

```
AT+QNWLOCK="common/4g",<num of cells>,[[<freq>,<pci>],...]
AT+QNWLOCK=\"common/4g\",1,6300,384

where

<num of cells>
number of cells to cell lock

<freq>
earfcn from lte info

<pci>
phy-cellid from lte info

```

单个单元格锁的例子：

`/interface/lte/at-chat lte1 input="AT+QNWLOCK=\"common/4g\",1,3050,448"`
 

多个单元格也可以添加到单元格锁定中。例如，锁定到两个不同的单元格：

`/interface/lte/at-chat lte1 input="AT+QNWLOCK=\"common/4g\",2,3050,448,1574,474"`
  

要删除单元格锁，请使用这个at-chat命令：

`/interface/lte/at-chat lte1 input="at+qnwlock=\"common/4g\",0"`

  
1. 重启或重设调制解调器后，单元锁定信息不会被保存。

2.  AT+QNWLOCK命令可以锁定单元和频率。因此，模块可以优先注册到锁定的单元，但是，根据3gpp协议，即使不在命令的锁定范围内，模块也会被重定向或交接到信号更好的单元指示。这种现象是正常的。

### 单元监控

单元监控器允许扫描附近可用的移动网络单元：

```shell
[admin@MikroTik] > /interface lte cell-monitor lte1
PHY-CELLID BAND         PSC EARFCN                 RSRP          RSRQ          RSSI         SINR
        49 B20              6300                -110dBm       -19.5dB
       272 B20              6300                -116dBm       -19.5dB
       374 B20              6300                -108dBm         -16dB
       384 B1               150                 -105dBm       -13.5dB
       384 B3               1300                -106dBm         -12dB
       384 B7               2850                -107dBm       -11.5dB
       432 B7               2850                -119dBm       -19.5dB
```

收集的数据可用于更精确的位置检测或用于小区锁定。

不是所有的调制解调器都支持这个功能

## 故障排除

启用LTE日志：

`[admin@MikroTik] > /system logging add topics=lte`

检查日志中是否有错误：

```shell
[admin@MikroTik] > /log print
 
11:08:59 lte,async lte1: sent AT+CPIN?
11:08:59 lte,async lte1: rcvd +CME ERROR: 10
```

在网上搜索CME错误描述、

在这种情况下： CME错误10 - 未插入SIM卡

### 锁定华为和其他调制解调器的频段

要锁定华为调制解调器的频段，不能使用 `/interface lte set lte1 band=""` 选项。

可以使用AT命令手动锁定到所需的频段。

要检查所有支持的频段，请运行at-chat命令：

```shell
[admin@MikroTik] /interface lte at-chat lte1 input="AT^SYSCFGEX=\?"
 
output: ^SYSCFGEX: ("00","03","02","01","99"),((2000004e80380,"GSM850/GSM900/GSM1800/GSM1900/WCDMA BCI/WCDMA BCII/WCDMA BCV/WCDMA BCVIII"),
(3fffffff,"All Bands")),(0-2),(0-4),((800d7,"LTE BC1/LTE BC2/LTE
BC3/LTE BC5/LTE BC7/LTE BC8/LTE BC20"),(7fffffffffffffff,"All Bands"))
OK
```

例如，锁定到LTE频段7：

`[admin@MikroTik] /interface lte set lte1 modem-init="AT^SYSCFGEX=\"03\",3FFFFFFF,2,4,40,,"`

将最后一部分 **40** 改为所需波段指定十六进制值，其中：

```
4 LTE BC3
40 LTE BC7
80000 LTE BC20
7FFFFFFFFFFFFFFF  All bands
etc
```

所有频段的HEX值和AT命令可以在 [华为AT命令接口规范指南](https://download-c.huawei.com/download/downloadCenter?downloadId=29741&version=72288&siteCode=) 中找到

检查频段是否被锁定：

```shell
[admin@MikroTik] /interface lte at-chat lte1 input="AT^SYSCFGEX\?"
 
output: ^SYSCFGEX: "03",3FFFFFFF,0,2,40
OK
```

更多信息请查看调制解调器制造商的AT命令参考手册。

### 带有RB9xx系列设备的mPCIe调制解调器

如果调制解调器在软重启后没有识别，那可能要在USB端口被初始化前增加一个延迟。可以用下面的命令来完成：

`/system routerboard settings set init-delay=5s`

### 带有USB-A端口和mPCIe的板子  

一些设备，如特定的RB9xx和RBLtAP-2HnD在一个mPCIe插槽和一个USB-A端口之间共享相同的USB线路。如果没有自动切换，调制解调器没有被检测到，可能要手动切换到使用USB-A或mini-PCIe：

`/system routerboard usb set type=mini-PCIe`

### 调制解调器固件升级

在尝试LTE调制解调器固件升级之前--将RouterOS版本升级到最新版本 [如何升级RouterOS](https://wiki.mikrotik.com/wiki/Manual:Upgrading_RouterOS)
  
从RouterOS 6.44beta20版本开始，可以升级调制解调器固件。从7.1beta1版本开始，Chateau系列的产品也可以进行固件升级。

固件升级只适用于FOTA空中固件 - 固件升级只能通过工作的移动连接来完成：

- )R11e-LTE
- )R11e-LTE-US

固件更新可用于FOTA，也可从文件中升级，适用于：

- )R11e-4G
- )R11e-LTE-6

固件更新可用于FOTA，通过任何接口接入互联网：

- )EG12-EA (Chateau LTE12)
- )RG502Q-EA (Chateau 5G)
- )EG18-EA (LHG LTE18)

固件更新通常包括在稳定性方面的小改进或小的错误修复，不能包含在RouterOS中。

通过运行检查当前使用的固件版本：

```shell
[admin@MikroTik] > /interface lte info lte1 once
 
-----
revision: "MikroTik_CP_2.160.000_v008"
-----
```

检查是否有新固件：

```shell
[admin@MikroTik] > /interface lte firmware-upgrade lte1
  installed: MikroTik_CP_2.160.000_v008
     latest: MikroTik_CP_2.160.000_v010
```

更新固件:

`[admin@MikroTik] > interface lte firmware-upgrade lte1 upgrade=yes
  status: downloading via LTE connection (>2min)`

整个升级过程可能需要10分钟，取决于连接速度。

升级成功后，发出USB电源复位，重新启动设备或运行AT+reset命令，用更新信息命令下的调制解调器版本读出：

`[admin@MikroTik] > /interface lte at-chat lte1 input="AT+reset"`

如果调制解调器在更新后有连接到电池的问题，或有任何其他不相关的问题-请清除旧配置：

`/interface lte at-chat lte1 input="AT+RSTSET"`

### 避免连接速度节流

一些运营商（TMobile，YOTA等）只允许在SIM卡上使用无限的数据，所有其他来自移动热点的数据都受到数量或吞吐速度的高度限制。[一些消息来源](https://www.reddit.com/r/hacking/comments/54a7dd/bypassing_tmobiles_tethering_data_capthrottling/) 发现，这种限制是通过监测数据包的TTL(Time To Live)值来确定是否需要应用限制(TTL每 "跳 "一次，就减少1)。RouterOS允许改变来自路由器的数据包的TTL参数允许隐藏子网络。记住，这可能与公平使用政策相冲突。

```shell
IPv4 mangle rule:
/ip firewall mangle
add action=change-ttl chain=postrouting new-ttl=set:65 out-interface=lte1 passthrough=yes
IPv6 mangle rule:
/ipv6 firewall mangle
add action=change-hop-limit chain=postrouting new-hop-limit=set:65 passthrough=yes
```

更多信息： [YOTA](https://m.habr.com/en/post/238351/), [TMobile](https://www.reddit.com/r/mikrotik/comments/acq4kz/anyone_familiar_with_configuring_the_ltap_us_with/)

### 在多次尝试错误的PIN码后解锁SIM卡

锁定SIM卡后，可以通过 "at-chat "解锁。

检查当前的PIN码状态：

`/interface lte at-chat lte1 input="at+cpin\?"`

如果卡被锁定 - 通过命令解锁：

`/interface lte at-chat lte1 input="AT+CPIN="PUK_code\",\"NEW_PIN\""`。

用匹配的值替换PUK_code和NEW_PIN。

在v6.45.1版本中，选择SIM卡槽的命令有所改变，在v7版本中又有所改变。 一些设备型号，如SXT，其SIM卡槽被命名为 "a "和 "b"，而不是 "up "和 "down"。