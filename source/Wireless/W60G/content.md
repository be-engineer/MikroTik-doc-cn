# 概述

**Packages:** `system`,`wireless`

802.11ad实现能够在无线网络上提供千兆以太网速度。

通过透明的AES加密无线60GHz链路扩展您的千兆网络，而不会出现通常的有线或无线网络问题。

## 通用接口属性

**Sub-menu:** `/interface w60g`

**警告:** 无线电线套件设备是预先配置的连接对。手动配置是可选的


| 属性                                                                                                                                                       | 说明                                                                                                                |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **arp** (_disabled \| enabled \| proxy-arp \| reply-only_; Default: **enabled**)                                                                           | [阅读更多 ](https://wiki.mikrotik.com/wiki/Manual:IP/ARP#ARP_Modes "Manual:IP/ARP")                                 |
| **arp-timeout** (_auto \| integer_; Default: **auto**)                                                                                                     | ARP超时是指在没有收到来自IP的报文后，ARP记录在ARP表中保留的时间。值auto等于/ip settings中arp-timeout的值，默认为30s |
| **comment** (_string_;Default:)                                                                                                                            | 接口的简短描述                                                                                                      |
| **disabled** (_yes \| no_;Default:**yes**)                                                                                                                 | 接口是否被禁用                                                                                                      |
| **frequency** (_58320 \| 60480 \| 62640 \| 64800 \| 66000\| auto_; Default: **auto**)                                                                      | 用于通信的频率(仅在桥接设备上有效)                                                                                  |
| **isolate-stations** (_yes \| no_; Default: **yes**)                                                                                                       | 不允许连接的客户端之间通信(从RouterOS 6.41以后)                                                                     |
| **l2mtu** (_integer [0..7882]_; Default: **1600**)                                                                                                         | 2层最大发送单元                                                                                                     |
| **mac-address** (_MAC_; Default: )                                                                                                                         | 无线接口的MAC地址                                                                                                   |
| **mdmg-fix** (_yes \| no_; Default: **no**)                                                                                                                | 实验特性仅在wAP60Gx3设备上工作，在某些情况下提供更好的点到多点稳定性                                                |
| **mode** (_ap-bridge \| bridge \| sniff\| station-bridge_; Default: **bridge**)                                                                            | 工作模式                                                                                                            |
| **mtu** (_integer [32..8192]_; Default: **1500**)                                                                                                          | 3层最大发送单元                                                                                                     |
| **name** (_string_; Default: **wlan60-1**)                                                                                                                 | 接口名称                                                                                                            |
| **password** (_string_; Default: **randomly generated**)                                                                                                   | 用于AES加密的密码                                                                                                   |
| **put-stations-in-bridge** (; Default: )                                                                                                                   | 将新创建的站点设备接口放在这个网桥中                                                                                |
| **region** (_asia\| australia \| canada\| china \| eu \| japan \| no-region-set\| usa_; Default: **no-region-set**)                                        | 参数限制频率使用                                                                                                    |
| **scan-list** (_58320,60480,62640,64800,66000_; Default: **58320,60480,62640,64800**)                                                                      | 扫描列表以限制在电台模式下的频率连接                                                                                |
| **ssid** (_string (0..32 chars)_; Default: **value of [System Identity](https://wiki.mikrotik.com/wiki/Manual:System/identity "Manual:System/identity")**) | SSID(服务集标识符)是标识无线网络的名称                                                                              |
| **tx-sector** (_integer [0..63] \| auto_; Default: **auto**)                                                                                               | 禁用波束形成并锁定选定的辐射模式                                                                                    |

  

**Sub-menu:** `/interface w60g print stats`

提供有关Beaforming事件的更详细信息和一些调试信息:


```shell
/interface w60g print stats name: wlan60-1 
beamforming-event: 310 
tx-io-msdu: 0 
tx-sw-msdu: 154 663
tx-fw-msdu: 102 
tx-ppdu: 220 147 
tx-ppdu-from-q: 40 327 
tx-mpdu-new: 154 663 
tx-mpdu-total: 184 759 
tx-mpdu-retry: 30 096 
rx-ppdu: 166 636 
rx-mpdu-crc-err: 4 817 
rx-mpdu-crc-ok: 285 649
```


站点接口属性

**警告:**  ap-bridge设备需要许可证级别4 [点击获取更多信息](https://wiki.mikrotik.com/wiki/Manual:License“Manual:License”) 才能支持多个已连接的客户端


从RouterOS 6.41开始，增加了点对多点的支持。

**在以后的版本中有几个重要的变化和改进。请始终升级到最新版本!**

连接的客户端被视为单独的接口，连接成功后创建新的工作站接口。

更新后默认配置仍然有效-新创建的站点接口被移动到默认桥接。

**Sub-menu:** `/interface w60g station`

| 属性                                                                | 说明                          |
| ------------------------------------------------------------------- | ----------------------------- |
| **parent** (_string_;Default:**wlan60-**)                           | 父接口名                      |
| **put-in-bridge** (_none                                            | parent                        | bridge-name_;Default:**parent**) | 将站点设备接口添加到特定网桥 |
| **remote-address** (_MAC_;Default:**matches bridge interface MAC**) | 网桥接口MAC地址，站点正在连接 |

## scan


```
/interface w60g scan wlan60-1
```

Scan命令用于搜索并显示W60G接口支持的频率范围内可用的AP。

使用scan命令禁止接口操作(扫描时无线链路断开)。

目前还不可能进行后台扫描。

## monitor


```shell
/interface w60g monitor wlan60-1 
connected: yes frequency: 58320 
remote-address: 04:D6:AA:AA:AA:AA 
mcs: 8 
phy-rate: 2.3Gbps 
signal: 80 rssi: -68 
tx-sector: 28 
tx-sector-info: center 
distance: 160.9m
```

监视器显示活动连接的当前状态。距离测量工具提供非常精确的距离测量。“tx-sector-info”(测试阶段的功能)提供当前使用的波束形成模式的信息，并显示到中心的方向-理论最高功率输出点。

## Align

```shell
/interface w60g align wlan60-1 
connected: yes 
frequency: 58320 
remote-address: 04:D6:AA:AA:AA:AB 
tx-mcs: 6 
tx-phy-rate: 1540.0Mbps 
signal: 70 
rssi: -62 
10s-average-rssi: -63.1 
tx-sector: 62 
tx-sector-info: left 19 degrees, up 26.6 degrees 
rx-sector: 96 
distance: 220.88m 
tx-packet-error-rate: 5%
```

  
在对齐模式下，两个设备之间的帧交换得更快，有关信号质量的信息显示得更频繁。使用“rssi”，“10s-average-rssi”和“tx-sector-info”(可从6.44beta39获得)值进行更精确的链接对齐。当设备进入对齐模式时，链路将丢失几秒钟。

## Sniff

嗅探模式允许捕获附近的802.11ad帧。要使用嗅探模式，需要使用相同的频率，并且需要将接口操作模式设置为嗅探:

```
/interface w60g set wlan60-1 mode=sniff
```

现在这个接口可以在 [Tools/Packet Sniffer](https://wiki.mikrotik.com/wiki/Manual:Tools/Packet_Sniffer "Manual:Tools/Packet Sniffer") 中用于抓包。嗅探模式不能与常规接口工作模式一起使用。

## 点到多点设置示例

所有的microtik设备都可以相互连接。目前有三种不同版本的wAP60G设备可供选择:

-   Wireless Wire kit
-   wAP 60G
-   SXTsq60 Lite60
-   wAP 60G AP
-   Wireless Wire Dish

硬件方面wAP设备是相同的，但存在一些软件限制

**wAP 60G AP** 专为PtMP(点对多点)设置中的接入点使用而设计，但也可以用作PtP(点对点)或站设备。它已经为多个连接的客户端支持配备了level4许可证 [更多关于许可证](https://wiki.mikrotik.com/wiki/Manual:License "Manual:License")

**无线线路套件**，**无线线路碟**，**SXTsq Lite60** 和 **wAP60G** 设备配备三级许可证。无线天线由于辐射方向图狭窄，只能作为客户端设备使用。

在Access Point模式下，需要升级License才能解锁多个同时连接的客户端，但设备可以像普通的Station设备一样连接到Access Point。

**警告:** 配置前，请确保设备运行的是最新的软件版本: [如何升级](https://wiki.mikrotik.com/wiki/Manual:Upgrading_RouterOS "Manual:Upgrading RouterOS")

  

透明无线链路的最小配置是匹配SSID、正确模式(网桥|站桥)以及将无线和以太网接口放在同一个网桥中。

在当前的示例中，我们将看到使用wAP60G AP作为接入点，wAP60G和Wireless Wire kit设备作为站设备，形成4单元网络的使用情况。

**警告:** 建议更改默认IP地址，以避免连接到设备



wAP60G AP 单元预先配置了WISP Bridge [默认配置](https://wiki.mikrotik.com/wiki/Manual:Default_Configurations "Manual: default Configurations")

已经配置了无线接口和以太网接口之间的SSID和网桥。建议设置无线密码并更改SSID。如果设备已经复位，还可以设置正确模式和使能接口。

一个行程序完成了前面提到的所有步骤:

```
/interface w60g set wlan60-1 password="put_your_safe_password_here" ssid="put_your_new_ssid_here" disabled=no mode=ap-bridge
```


无线线路和wAP60G单元预先配置了PTP桥的默认配置。

无线有线设备已经随机生成匹配的SSID和无线密码。

网桥设备(网桥或接入点设备与一个连接的客户端支持)需要无线模式切换到站桥。

一个可以用来在客户端模式下设置设备的行:


```
/interface w60g set wlan60-1 password="put_your_safe_password_here" ssid="put_your_new_ssid_here" disabled=no mode=station-bridge
```


如果配置是从空配置中完成的(没有默认配置的重置)

需要创建包含无线和以太网接口的新网桥，并应添加易于访问的IP地址。


```
{ /interface bridge add name=bridge1 /interface bridge port add bridge=bridge1 interface=ether1 add bridge=bridge1 interface=wlan60-1 /ip address add address=192.168.88.1/24 interface=bridge1 }
```


对于接入点添加这条线，以确保所有连接的站将放在同一个桥接。


```
/interface w60g set wlan60-1 put-stations-in-bridge=bridge1
```


成功连接每个客户端设备后，接入点设备上将出现以下新条目:



```
/interface w60g station print
```


```shell
Flags: X - disabled, R - running 

0 name="wlan60-station-1" parent=wlan60-1 remote-address=AA:AA:AA:AA:AA:AA mtu=1500 mac-address=AA:AA:AA:AA:AA:AB arp=enabled arp-timeout=auto put-in-bridge=parent 

0 name="wlan60-station-2" parent=wlan60-1 remote-address=AA:AA:AA:AA:AB:AA mtu=1500 mac-address=AA:AA:AA:AA:AA:AC arp=enabled arp-timeout=auto put-in-bridge=parent 

0 name="wlan60-station-3" parent=wlan60-1 remote-address=AA:AA:AA:AA:AC:AA mtu=1500 mac-address=AA:AA:AA:AA:AA:AD arp=enabled arp-timeout=auto put-in-bridge=parent 

0 name="wlan60-station-4" parent=wlan60-1 remote-address=AA:AA:AA:AA:AD:AA mtu=1500 mac-address=AA:AA:AA:AA:AA:AE arp=enabled arp-timeout=auto put-in-bridge=parent 
```


对于每个客户端，可以应用单独的设置(队列、vlan、防火墙规则等)，从而提供更大的配置灵活性。

为了限制客户端-客户端在同一网桥中的通信，可以在接入点设备上使用隔离站选项:


```
/interface w60g set wlan60-1 isolate-stations=yes
```


## 点到点GUI配置示例

[点到点GUI配置示例](https://help.mikrotik.com/docs/display/ROS/PtP+GUIexample)

## 故障排除和建议


microtik 60GHz解决方案功能包括对ATPC(自适应发射功率控制)的支持

### 物理属性

802.11ad标准中使用的无线频率的大气衰减非常高，在部署链路之前应考虑到这一点。

Wireless Wire套件已在长达200米的距离上进行了测试。

为了稳定和全速可用性，建议在距离达1500米的情况下使用该套件。

wAP60G设备配备了相控阵60°波束形成天线，可以帮助信号在短距离内找到物体周围的路径，但在较远距离上保持视线清晰仍然至关重要。

LHG60G设备单辐射方向图小于1度(水平和垂直)，所有方向图组合在水平和垂直平面上都提供接近3度的覆盖，每种情况下使用波束形成算法计算最佳方向图。波束宽度和方向取决于所使用的预定义校准扇区。

### 设备射频特性

60 GHz设备


<table class="wrapped confluenceTable"><colgroup><col><col><col><col></colgroup><tbody><tr><td style="border: 1px solid #000000" class="confluenceTd"><strong>Device</strong></td><td style="border: 1px solid #000000" class="confluenceTd"><strong>Width of single antenna pattern and full span in degrees</strong></td><td style="border: 1px solid #000000" class="confluenceTd"><strong>EIRP</strong></td><td style="border: 1px solid #000000" class="confluenceTd"><strong>Tx-power</strong></td></tr><tr><td style="border: 1px solid #000000" class="confluenceTd">wAP 60G</td><td style="border: 1px solid #000000" class="confluenceTd">15-20 degrees single pattern and full span 60 degrees over horizontal and 30 degrees vertical plane</td><td style="border: 1px solid #000000" class="confluenceTd">&lt; 40 dBm</td><td style="border: 1px solid #000000" class="confluenceTd"><br></td></tr><tr><td style="border: 1px solid #000000" class="confluenceTd">wAP 60G AP</td><td style="border: 1px solid #000000" class="confluenceTd">15-20 degrees single pattern and full span 60 degrees over horizontal and 30 degrees vertical plane</td><td style="border: 1px solid #000000" class="confluenceTd">&lt; 40 dBm</td><td style="border: 1px solid #000000" class="confluenceTd"><br></td></tr><tr><td style="border: 1px solid #000000" class="confluenceTd">Wireless Wire</td><td style="border: 1px solid #000000" class="confluenceTd">15-20 degrees single pattern and full span 60 degrees over horizontal and 30 degrees vertical plane</td><td style="border: 1px solid #000000" class="confluenceTd">&lt; 40 dBm</td><td style="border: 1px solid #000000" class="confluenceTd"><br></td></tr><tr><td style="border: 1px solid #000000" class="confluenceTd">wAP 60Gx3 AP</td><td style="border: 1px solid #000000" class="confluenceTd">15-20 degrees single pattern and full span 180 degrees over horizontal and 30 degrees vertical plane</td><td style="border: 1px solid #000000" class="confluenceTd">&lt; 40 dBm</td><td style="border: 1px solid #000000" class="confluenceTd"><br></td></tr><tr><td style="border: 1px solid #000000" class="confluenceTd">SXTsq Lite 60</td><td style="border: 1px solid #000000" class="confluenceTd">15-20 degrees single pattern and full span 60 degrees over horizontal and 30 degrees vertical plane</td><td style="border: 1px solid #000000" class="confluenceTd">&lt; 40 dBm</td><td style="border: 1px solid #000000" class="confluenceTd"><br></td></tr><tr><td style="border: 1px solid #000000" class="confluenceTd">Cube Lite 60</td><td style="border: 1px solid #000000" class="confluenceTd">4-8 degrees single pattern and full span 12 degrees over horizontal and 12 degrees vertical plane</td><td style="border: 1px solid #000000" class="confluenceTd">&lt; 40 dBm</td><td style="border: 1px solid #000000" class="confluenceTd">&lt; 10 dBm</td></tr><tr><td style="border: 1px solid #000000" class="confluenceTd">Cube 60G ac</td><td style="border: 1px solid #000000" class="confluenceTd">4-8 degrees single pattern and full span 12 degrees over horizontal and 12 degrees vertical plane</td><td style="border: 1px solid #000000" class="confluenceTd">&lt; 40 dBm</td><td style="border: 1px solid #000000" class="confluenceTd">&lt; 10 dBm</td></tr><tr><td style="border: 1px solid #000000" class="confluenceTd">Cube 60Pro ac&nbsp;</td><td style="border: 1px solid #000000" class="confluenceTd">4-8 degrees single pattern and full span 11 degrees over horizontal and 11 degrees vertical plane</td><td style="border: 1px solid #000000" class="confluenceTd">&lt; 40 dBm</td><td style="border: 1px solid #000000" class="confluenceTd">&lt; 10 dBm</td></tr><tr><td style="border: 1px solid #000000" class="confluenceTd">CubeSA 60Pro ac</td><td style="border: 1px solid #000000" class="confluenceTd">15 degrees single pattern and full span 60 degrees over horizontal and 30 degrees vertical plane</td><td style="border: 1px solid #000000" class="confluenceTd">&lt; 40 dBm</td><td style="border: 1px solid #000000" class="confluenceTd">&lt; 10 dBm</td></tr><tr><td style="border: 1px solid #000000" class="confluenceTd">LHG Lite 60</td><td style="border: 1px solid #000000" class="confluenceTd">&lt; 1 degree single pattern and full span 3 degrees over horizontal and 3 degrees vertical plane</td><td style="border: 1px solid #000000" class="confluenceTd">&lt; 55 dBm</td><td style="border: 1px solid #000000" class="confluenceTd">&lt; 10 dBm</td></tr><tr><td style="border: 1px solid #000000" class="confluenceTd">LHG 60G</td><td style="border: 1px solid #000000" class="confluenceTd">&lt; 1 degree single pattern and full span 3 degrees over horizontal and 3 degrees vertical plane</td><td style="border: 1px solid #000000" class="confluenceTd">&lt; 55 dBm</td><td style="border: 1px solid #000000" class="confluenceTd">&lt; 10 dBm</td></tr><tr><td style="border: 1px solid #000000" class="confluenceTd">Wireless Wire Dish</td><td style="border: 1px solid #000000" class="confluenceTd">&lt; 1 degree single pattern and full span 3 degrees over horizontal and 3 degrees vertical plane</td><td style="border: 1px solid #000000" class="confluenceTd">&lt; 55 dBm</td><td style="border: 1px solid #000000" class="confluenceTd">&lt; 10 dBm</td></tr><tr><td style="border: 1px solid #000000" class="confluenceTd">Wireless Wire nRAY</td><td style="border: 1px solid #000000" class="confluenceTd">&lt; 1 degree single pattern and full span 3 degrees over horizontal and 3 degrees vertical plane</td><td style="border: 1px solid #000000" class="confluenceTd">&lt; 55 dBm or &lt;40 dBm with EU region</td><td style="border: 1px solid #000000" class="confluenceTd">&lt; 10 dBm</td></tr></tbody></table>
  

### 区域

MikroTik 802.11ad设备支持的频率范围:57240 MHz - 67080 MHz，如果使用“区域”参数，可以限制频率和信道的使用。

<table class="wrapped confluenceTable"><colgroup><col><col><col><col></colgroup><tbody><tr><td style="border: 1px solid #000000" class="confluenceTd"><strong>Region</strong></td><td style="border: 1px solid #000000" class="confluenceTd"><strong>lower frequency</strong></td><td style="border: 1px solid #000000" class="confluenceTd"><strong>upper frequency</strong></td><td style="border: 1px solid #000000" class="confluenceTd"><strong>usable channels</strong></td></tr><tr><td style="border: 1px solid #000000" class="confluenceTd">USA</td><td style="border: 1px solid #000000" class="confluenceTd">57.24 GHz</td><td style="border: 1px solid #000000" class="confluenceTd">70.20 GHz</td><td style="border: 1px solid #000000" class="confluenceTd">1, 2, 3, 4, 5, 6</td></tr><tr><td style="border: 1px solid #000000" class="confluenceTd">Canada</td><td style="border: 1px solid #000000" class="confluenceTd">57.24 GHz</td><td style="border: 1px solid #000000" class="confluenceTd">63.72 GHz</td><td style="border: 1px solid #000000" class="confluenceTd">1, 2, 3</td></tr><tr><td style="border: 1px solid #000000" class="confluenceTd">Asia</td><td style="border: 1px solid #000000" class="confluenceTd">57.24 GHz</td><td style="border: 1px solid #000000" class="confluenceTd">63.72 GHz</td><td style="border: 1px solid #000000" class="confluenceTd">1, 2, 3</td></tr><tr><td style="border: 1px solid #000000" class="confluenceTd">EU</td><td style="border: 1px solid #000000" class="confluenceTd">57.24 GHz</td><td style="border: 1px solid #000000" class="confluenceTd">65.88 GHz</td><td style="border: 1px solid #000000" class="confluenceTd">1, 2, 3, 4</td></tr><tr><td style="border: 1px solid #000000" class="confluenceTd">Japan</td><td style="border: 1px solid #000000" class="confluenceTd">57.24 GHz</td><td style="border: 1px solid #000000" class="confluenceTd">65.88 GHz</td><td style="border: 1px solid #000000" class="confluenceTd">1, 2, 3, 4</td></tr><tr><td style="border: 1px solid #000000" class="confluenceTd">Australia</td><td style="border: 1px solid #000000" class="confluenceTd">57.24 GHz</td><td style="border: 1px solid #000000" class="confluenceTd">65.88 GHz</td><td style="border: 1px solid #000000" class="confluenceTd">1, 2, 3, 4</td></tr><tr><td style="border: 1px solid #000000" class="confluenceTd">China</td><td style="border: 1px solid #000000" class="confluenceTd">59.40 GHz</td><td style="border: 1px solid #000000" class="confluenceTd">63.72 GHz</td><td style="border: 1px solid #000000" class="confluenceTd">2, 3</td></tr></tbody></table>

### 连接问题

为了连接需要直接可见的设备，客户端设备上的“扫描列表”需要包括AP设备上使用的“频率”。LHG60设备需要非常精确的校准，以便在更高的距离中获得最佳性能。

### 用于监控的SNMP oid

From RouterOS>=6.42rc6新增对W60G接口监控的SNMP支持

```
For main interfaces:
1.3.6.1.4.1.14988.1.1.1.8.1.2.1  integer  Mode
1.3.6.1.4.1.14988.1.1.1.8.1.3.1  string   SSID
1.3.6.1.4.1.14988.1.1.1.8.1.4.1  integer  Connected status
1.3.6.1.4.1.14988.1.1.1.8.1.5.1  string   Remote MAC
1.3.6.1.4.1.14988.1.1.1.8.1.6.1  integer  Frequency
1.3.6.1.4.1.14988.1.1.1.8.1.7.1  integer  MCS
1.3.6.1.4.1.14988.1.1.1.8.1.8.1  integer  Signal quality
1.3.6.1.4.1.14988.1.1.1.8.1.9.1  integer  tx-sector
1.3.6.1.4.1.14988.1.1.1.8.1.11.1 string   Sector info
1.3.6.1.4.1.14988.1.1.1.8.1.12.1 integer  RSSI
1.3.6.1.4.1.14988.1.1.1.8.1.13.1 gauge32  PHY rate

```

工位接口将在不同的表下编号:

```
1.3.6.1.4.1.14988.1.1.1.9.1.2.(interfaceID) = integer Connected status
1.3.6.1.4.1.14988.1.1.1.9.1.3.(interfaceID) = Hex-STRING mac-address
1.3.6.1.4.1.14988.1.1.1.9.1.4.(interfaceID) = INTEGER: MCS 
1.3.6.1.4.1.14988.1.1.1.9.1.5.(interfaceID) = INTEGER: Signal Quality Index
1.3.6.1.4.1.14988.1.1.1.9.1.6.(interfaceID) = INTEGER: tx-sector
1.3.6.1.4.1.14988.1.1.1.9.1.8.(interfaceID) = Gauge32: data-rate [Mbps]
1.3.6.1.4.1.14988.1.1.1.9.1.9.(interfaceID) = INTEGER: RSSI
1.3.6.1.4.1.14988.1.1.1.9.1.10.(interfaceID) = INTEGER: distance [cm]

```

InterfaceID从3开始增加，每连接一个站点增加1。关于SNMP功能和MIB文件的更多信息可以在 [SNMP wiki](https://wiki.mikrotik.com/wiki/Manual:SNMP "Manual:SNMP") 中找到。

### 重置无线电线套件的配置

重置按钮具有与其他设备相同的功能，详细说明 [在这里](https://wiki.mikrotik.com/wiki/Manual:Reset_button "Manual:Reset button")

**按住按钮5秒启动(USR LED灯开始闪烁)** -重置到密码保护状态。

**启动时按住按钮10秒(USR LED闪烁后变为常亮)** -完全删除配置。

**警告:** 完全移除配置后，只能建立 [MAC -telnet](https://wiki.mikrotik.com/wiki/MAC_access "MAC access") 连接