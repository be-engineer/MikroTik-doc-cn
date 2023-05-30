# 以太网

**Sub-menu:** `/interface ethernet`  
**Standards:** `[IEEE 802.3](http://grouper.ieee.org/groups/802/3/)`

# 概述

microtik RouterOS支持多种类型的以太网接口，包括10Mbps到10Gbps的铜绞线以太网，1Gbps和10Gbps SFP/SFP+接口和40Gbps QSFP接口。某些RouterBoard设备配备了combo接口，该接口同时包含两种接口类型(例如1Gbps以太网双绞线和SFP接口)，允许选择最合适的选项或创建物理链路故障转移。通过RouterOS，可以控制不同的以太网相关属性，如链路速度、自动协商、双工模式等，监控收发器诊断信息，并查看广泛的以太网相关统计信息。

**属性**

| 属性                                                                                                                                            | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| ----------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **advertise** (_10M-full \| 10M-half \| 100M-full \| 100M-half \| 1000M-full \| 1000M-half \| 2500M-full \| 5000M-full \| 10000M-full;Default:) | 双绞线以太网接口的通告速度和双工模式，仅在使能自协商时生效。通告速度高于实际接口支持的速度将没有影响，允许多个选项。                                                                                                                                                                                                                                                                                                                         |
| **arp** (_disabled \| enabled  \| local-proxy-arp \| proxy-arp \| reply-only_; Default: **enabled**)                                            | 地址解析协议模式:<br>- disabled表示接口不使用ARP<br>- enabled接口使用ARP<br>- local-proxy-arp路由器在接口上执行代理ARP，并向同一接口发送应答<br>- proxy- ARP -在接口上执行代理ARP，对其他接口进行应答<br>- reply-only表示接口只响应在 [ARP](https://wiki.mikrotik.com/wiki/Manual:IP/ARP "Manual:IP/ARP") 表中以静态表项形式输入的匹配的IP/ MAC地址组合的请求。ARP表中不会自动存储动态表项。因此，要使通信成功，必须已经存在有效的静态条目。 |
| **auto-negotiation** (_yes \| no_; Default: **yes**)                                                                                            | 当启用时，接口“发布”其最大功能以实现最佳连接。<br>- 注1:不能只关闭一端的自协商功能，否则可能导致以太网接口不能正常工作。<br>- 注2:禁用自协商功能时，千兆以太网和NBASE-T以太网链路不能工作。                                                                                                                                                                                                                                                  |
| **bandwidth** (_integer/integer_; Default: **unlimited/unlimited**)                                                                             | 设置接口处理的最大rx/tx带宽(kbps)。所有Atheros [交换芯片](https://wiki.mikrotik.com/wiki/Manual:Switch_Chip_Features "Manual:Switch Chip Features") 端口都支持TX限制。RX限制仅支持Atheros8327/QCA8337交换芯片端口。                                                                                                                                                                                                                          |
| **cable-setting** (_default \| short \| standard_;Default:**default**)                                                                          | 改变电缆长度设置(仅适用于NS DP83815/6卡)                                                                                                                                                                                                                                                                                                                                                                                                     |
| **combo-mode** (_auto \| copper \| sfp_;Default:**auto**)                                                                                       | 当选择auto模式时，首先连接的端口将建立链接。如果这个链路失败，另一个端口将尝试建立一个新的链路。如果两个端口同时连接(例如重启后)，则优先级为SFP/SFP+端口。当选择sfp模式时，接口只能通过sfp / sfp +笼工作。当选择铜模式时，接口只能通过RJ45以太网接口工作。                                                                                                                                                                                   |
| **comment** (_string_;Default:)                                                                                                                 | 项目的描述性名称                                                                                                                                                                                                                                                                                                                                                                                                                             |
| **disable-running-check** (_yes \| no_;Default:**yes**)                                                                                         | 关闭运行检查。如果设置为no，路由器将自动检测网卡是否与网络中的设备连接。默认值为“yes”，因为旧的网卡不支持。(仅适用于x86)                                                                                                                                                                                                                                                                                                                     |
| **tx-flow-control** (_on \| off \| auto_; Default: **off**)                                                                                     | 设置为on时，向上游设备生成暂停帧，暂时停止报文的传输。只有当某些路由器的输出接口拥塞，报文无法继续传输时，才会产生暂停帧。**auto** 与 **on** 相同，除了当auto-negotiation=yes时，流量控制状态是通过考虑另一端的通告来解决的。                                                                                                                                                                                                                |
| **rx-flow-control** (_on \| off \| auto_;Default:**off**)                                                                                       | 当设置为on时，端口将处理接收到的暂停帧并在需要时暂停传输。**auto** 与 **on** 相同，除了当auto-negotiation=yes时，流量控制状态是通过考虑另一端的通告来解决的。                                                                                                                                                                                                                                                                                |
| **full-duplex** (_yes \| no_;Default:**yes**)                                                                                                   | 定义数据是否同时在两个方向上传输，仅在禁用自协商时适用。                                                                                                                                                                                                                                                                                                                                                                                     |
| **l2mtu** (_integer [0..65536]_; Default: )                                                                                                     | Layer2最大传输单元。[阅读更多](https://wiki.mikrotik.com/wiki/Maximum_Transmission_Unit_on_RouterBoards "Maximum Transmission Unit on RouterBoards")                                                                                                                                                                                                                                                                                         |
| **mac-address** (_MAC_;Default:)                                                                                                                | 接口的媒体访问控制号。                                                                                                                                                                                                                                                                                                                                                                                                                       |
| **master-port** (_name_;Default:**none**)                                                                                                       | 过时的属性，有关此属性的更多详细信息可以在[Master-port](https://wiki.mikrotik.com/wiki/Manual:Master-port“Manual:Master-port”)页面中找到。                                                                                                                                                                                                                                                                                                   |
| **mdix-enable** (_yes \| no_;Default:**yes**)                                                                                                   | 端口是否启用MDI/X自动交叉电缆校正功能(特定于硬件，例如RB500上的ether1可以设置为yes/no。在其他硬件上固定为“yes”)                                                                                                                                                                                                                                                                                                                              |
| **mtu** (_integer [0..65536]_;Default:**1500**)                                                                                                 | Layer3最大传输单元                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **name** (_string_;Default:)                                                                                                                    | 接口名称                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| **origin -mac-address** (_read-only: MAC_;Default:)                                                                                             | 接口的原始媒体访问控制编号。                                                                                                                                                                                                                                                                                                                                                                                                                 |
| **poe-out** (_auto-on \| forced-on \| off_;Default:**off**)                                                                                     | Poe Out设置。[阅读更多](https://wiki.mikrotik.com/wiki/Manual:PoE-Out "Manual:PoE-Out")                                                                                                                                                                                                                                                                                                                                                      |
| **priority** (_integer [0..99]_;Default:)                                                                                                       | Poe Out设置。[阅读更多](https://wiki.mikrotik.com/wiki/Manual:PoE-Out "Manual:PoE-Out")                                                                                                                                                                                                                                                                                                                                                      |
| **sfp-shutdown-temperature** (_integer_;Default:**95**                                                                                          | **80**)                                                                                                                                                                                                                                                                                                                                                                                                                                      | 由于检测到的SFP模块温度过高，接口将暂时关闭的摄氏温度(v6.48引入)。SFP/SFP+/SFP28接口的缺省值是95,QSFP+/QSFP28接口的缺省值是80 (v7.6引入)。 |
| **speed** (_10Mbps \| 10Gbps \| 100Mbps \| 1Gbps_;Default:)                                                                                     | 设置接口数据传输速度，只有关闭自协商功能后才生效。                                                                                                                                                                                                                                                                                                                                                                                           |

**只读属性**

| 属性                           | 说明                                                                                               |
| ------------------------------ | -------------------------------------------------------------------------------------------------- |
| **running** (_yes      \| no_) | 接口是否运行。请注意，有些接口没有运行检查，它们总是报告为“正在运行”                               |
| **slave** (_yes \| no_)        | 接口是否被配置为其他接口的从接口(例如 [Bonding](https://wiki.mikrotik.com/wiki/Bonding "Bonding")) |
| **switch** (_integer_)         | 交换芯片接口所属的ID。                                                                             |

# 特殊菜单命令

| 属性                                    | 说明                                                                                                               |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| **blink** (_[id, name]_)                | 闪烁以太网指示灯                                                                                                   |
| **monitor** (_[id, name]_)              | 监控以太网状态。[阅读更多](https://wiki.mikrotik.com/wiki/Manual:Interface/Ethernet#Monitor)                       |
| **Reset -counters** (_[id, name]_)      | 重置统计计数器。[阅读更多](https://wiki.mikrotik.com/wiki/Manual:Interface/Ethernet#Stats)                         |
| **Reset - MAC -address** (_[id, name]_) | 重置MAC地址为厂商默认值。                                                                                          |
| **cable-test** (_string_)               | 显示检测到的电缆对问题。[阅读更多](https://wiki.mikrotik.com/wiki/Manual:Interface/Ethernet#Detect_Cable_Problems) |

# 监控

要打印当前链路速率、双工模式和其他以太网相关属性或查看收发器的详细诊断信息，请使用 /interface Ethernet monitor命令。对于不同的接口类型(如双绞线以太网或SFP接口)或不同的收发器(如SFP和QSFP)，所提供的信息可能不同。

**属性**

| 属性                                                                                                                                                    | 说明                                                                                                                                  |
| ------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| **advertising** (_10M-full \| 10M-half \| 100M-full \| 100M-half \| 1000M-full \| 1000M-half \| 2500M-full \| 5000M-full \| 10000M-full_)               | 双绞线以太网接口的通告速度和双工模式，仅在启用自协商时有效                                                                            |
| **auto-negotiation** (_disabled \| done     \| failed    \| incomplete_)                                                                                | 当前自动协商状态:<br>- disabled -关闭协商功能<br>- done -协商完成<br>- failed -协商失败<br>- incomplete -协商未完成                   |
| **default-cable-settings** (_short \| standard_)                                                                                                        | 默认电缆长度设置(仅适用于NS DP83815/6卡)<br>- short -支持短电缆<br>- standard -支持标准电缆                                           |
| **full-duplex** (_yes \| no_)                                                                                                                           | 数据是否同时在两个方向上传输                                                                                                          |
| **Link -partner-advertising** (_10M-full \| 10M-half \| 100M-full \| 100M-half \| 1000M-full \| 1000M-half \| 2500M-full \| 5000M-full \| 10000M-full_) | 双绞线以太网接口的链路伙伴通告速度和双工模式，仅在启用自协商时有效                                                                    |
| **rate** (_10Mbps \| 100Mbps \| 1Gbps \| 2.5Gbps \| 5Gbps \| 10Gbps \| 40Gbps \|_)                                                                      | 连接的实际数据速率。                                                                                                                  |
| **status** (_link-ok \| no-link \| unknown_)                                                                                                            | 接口的当前链路状态<br>- link-ok表示网卡已连接到网络<br>- no-link表示网卡未连接到网络<br>- unknown -连接不被识别(如果卡不报告连接状态) |
| **tx-flow-control** (_yes \| no_)                                                                                                                       | 是否使用TX流量控制                                                                                                                    |
| **RX -flow-control** (_yes \| no_)                                                                                                                      | 是否使用RX流量控制                                                                                                                    |
| **combo-state** (_copper \| sfp_)                                                                                                                       | 组合接口使用的组合模式                                                                                                                |
| **sfp-module-present** (_yes \| no_)                                                                                                                    | 收发器是否在cage中                                                                                                                    |
| **sfp-rx-lose** (_yes \| no_)                                                                                                                           | 接收端信号是否丢失                                                                                                                    |
| **sfp-tx-fault** (_yes \| no_)                                                                                                                          | 收发器是否处于故障状态                                                                                                                |
| **sfp-type** (_SFP-or-SFP+ \| DWDM-SFP、                                                                                                                | QSFP+_)                                                                                                                               | 使用的光模块类型 |
| **sfp-connector-type** (_SC \| LC \| optical-pigtail \| copper-pigtail \| multifiber-parallel-optic-1x12 \| no-separable-connector\| RJ45_)             | 使用的收发器连接器类型                                                                                                                |
| **sfp-link-length-9um** (_m_)                                                                                                                           | 单模9/125um光纤收发器支持的链路长度                                                                                                   |
| **sfp-link-length-50um** (_m_)                                                                                                                          | 多模50/125um光纤(OM2)收发器支持的链路长度                                                                                             |
| **sfp-link-length-62um** (_m_)                                                                                                                          | 多模62.5/125um光纤(OM1)收发器支持的链路长度                                                                                           |
| **sfp-link-length-copper** (_m_)                                                                                                                        | 支持的铜收发器链路长度                                                                                                                |
| **sfp-vendor-name** (_string_)                                                                                                                          | 收发器制造商                                                                                                                          |
| **sfp-vendor-part-number** (_string_)                                                                                                                   | 收发器部件号                                                                                                                          |
| **sfp-vendor-revision** (_string_)                                                                                                                      | 收发器版本号                                                                                                                          |
| **sfp-vendor-serial** (_string_)                                                                                                                        | 收发器序列号                                                                                                                          |
| **sfp-manufacturing-date** (_date_)                                                                                                                     | 收发器生产日期                                                                                                                        |
| **sfp-wavelength** (_nm_)                                                                                                                               | 收发端发射器光信号波长                                                                                                                |
| **sfp-temperature** (_C_)                                                                                                                               | 收发器温度                                                                                                                            |
| **sfp-supply-voltage** (_V_)                                                                                                                            | 收发电源电压                                                                                                                          |
| **sfp-tx -bias-current** (_mA_)                                                                                                                         | 收发器Tx偏置电流                                                                                                                      |
| **sfp-tx-power** (_dBm_)                                                                                                                                | 收发器传输光功率                                                                                                                      |
| **sfp-rx-power** (_dBm_)                                                                                                                                | 收发器接收光功率                                                                                                                      |
| **EEPROM -checksum** (_good \| bad_)                                                                                                                    | EEPROM校验和是否正确                                                                                                                  |
| **eeprom** (_hex dump_)                                                                                                                                 | 收发器的原始eeprom                                                                                                                    |

以太网状态输出示例:

```shell
[admin@MikroTik] > /interface ethernet monitor ether1
name: ether1
status: link-ok
auto-negotiation: done
rate: 1Gbps
full-duplex: yes
tx-flow-control: no
rx-flow-control: no
advertising: 10M-half,10M-full,100M-half,100M-full,1000M-half,1000M-full
link-partner-advertising: 10M-half,10M-full,100M-half,100M-full,1000M-full
```

SFP状态输出示例:

```shell
[admin@MikroTik] > /interface ethernet monitor sfp-sfpplus24
name: sfp-sfpplus24
status: link-ok
auto-negotiation: done
rate: 10Gbps
full-duplex: yes
tx-flow-control: no
rx-flow-control: no
advertising:
link-partner-advertising:
sfp-module-present: yes
sfp-rx-loss: no
sfp-tx-fault: no
sfp-type: SFP-or-SFP+
sfp-connector-type: LC
sfp-link-length-50um: 80m
sfp-link-length-62um: 30m
sfp-vendor-name: Mikrotik
sfp-vendor-part-number: S+85DLC03D
sfp-vendor-revision: A
sfp-vendor-serial: STST85S84700155
sfp-manufacturing-date: 18-12-07
sfp-wavelength: 850nm
sfp-temperature: 33C
sfp-supply-voltage: 3.251V
sfp-tx-bias-current: 6mA
sfp-tx-power: -2.843dBm
sfp-rx-power: -1.203dBm
eeprom-checksum: good
eeprom: 0000: 03 04 07 10 00 00 00 20 40 0c c0 06 67 00 00 00 ....... @...g...
0010: 08 03 00 1e 4d 69 6b 72 6f 74 69 6b 20 20 20 20 ....Mikr otik
0020: 20 20 20 20 00 00 00 00 53 2b 38 35 44 4c 43 30 .... S+85DLC0
0030: 33 44 20 20 20 20 20 20 41 20 20 20 03 52 00 45 3D A .R.E
0040: 00 1a 00 00 53 54 53 54 38 35 53 38 34 37 30 30 ....STST 85S84700
0050: 31 35 35 20 31 38 31 32 30 37 20 20 68 f0 05 b6 155 1812 07 h...
0060: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ........ ........
0070: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ........ ........
0080: 64 00 d8 00 5f 00 dd 00 8c a0 6d 60 88 b8 71 48 d..._... ..m`..qH
0090: 1d 4c 00 fa 17 70 01 f4 31 2d 04 ea 27 10 06 30 .L...p.. 1-..'..0
00a0: 31 2d 01 3c 27 10 01 8e 00 00 00 00 00 00 00 00 1-.<'... ........
00b0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ........ ........
00c0: 00 00 00 00 3f 80 00 00 00 00 00 00 01 00 00 00 ....?... ........
00d0: 01 00 00 00 01 00 00 00 01 00 00 00 00 00 00 26 ........ .......&
00e0: 21 8a 7f 00 0c cd 14 4c 1d 9c 00 00 00 00 00 00 !......L ........
00f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ........ ........
```

# 检测电缆问题

电缆测试可以检测问题或测量电缆的大致长度，如果电缆在另一端未插入，因此存在“无连接”。RouterOS将显示:

- 哪对线缆损坏
- 到问题的距离
- 电缆到底是怎么断的-短路还是开路

如果另一端简单地拔掉，这也可以工作-在这种情况下，总电缆长度将显示。

下面是一个示例输出:

```shell
[admin@CCR] > interface ethernet cable-test ether2
name: ether2
status: no-link
cable-pairs: open:4,open:4,open:4,open:4
```

在上面的例子中，电缆在4米的距离上没有短路而是“开路”，在距离交换芯片相同的距离上，所有的电缆对都是同样的故障。

目前在以下设备上实现了“cable-test”:

-   CCR series devices
-   CRS1xx series devices
-   CRS2xx series devices
-   OmniTIK series devices
-   RB450G series devices
-   RB951 series devices
-   RB2011 series devices
-   RB4011 series devices
-   RB750Gr2
-   RB750UPr2
-   RB751U-2HnD
-   RB850Gx2
-   RB931-2nD
-   RB941-2nD
-   RB952Ui-5ac2nD
-   RB962UiGS-5HacT2HnT
-   RB1100AHx2
-   RB1100x4
-   RBD52G-5HacD2HnD
-   RBcAPGi-5acD2nD
-   RBmAP2n
-   RBmAP2nD
-   RBwsAP-5Hac2nD
-   RB3011UiAS-RM
-   RBMetal 2SHPn
-   RBDynaDishG-5HacD
-   RBLDFG-5acD
-   RBLHGG-5acD

  

目前Combo端口不支持“电缆测试”。

# 数据

使用'/interface ethernet print stats'命令，可以看到广泛的以太网相关统计信息。由于不同的以太网驱动，不同的RouterBoard设备的统计列表可能会有所不同。下面的列表包含了所有RouterBoard设备上所有可用的计数器。大多数以太网统计数据可以通过 [SNMP](https://wiki.mikrotik.com/wiki/Manual:SNMP "Manual:SNMP") 和MIKROTIK-MIB进行远程监控。

  

| 属性                                        | 说明                                                      |
| ------------------------------------------- | --------------------------------------------------------- |
| **driver-rx-byte** (_integer_)              | 设备CPU接收字节总数                                       |
| **driver-rx-packet** (_integer_)            | 设备CPU接收报文总数                                       |
| **driver-tx-byte** (_integer_)              | 设备CPU传输字节总数                                       |
| **driver-tx-packet** (_integer_)            | 设备CPU传输数据包总数                                     |
| **rx-64** (_integer_)                       | 接收到的64字节帧总数                                      |
| **rx-65-127** (_integer_)                   | 接收到的65到127字节帧的总数                               |
| **rx-128-255** (_integer_)                  | 接收到的128到255字节帧的总数                              |
| **rx-256-511** (_integer_)                  | 接收到的256到511字节帧的总数                              |
| **rx-512-1023** (_integer_)                 | 接收到的512到1023字节帧总数                               |
| **rx-1024-1518** (_integer_)                | 接收1024到1518字节帧的总数                                |
| **rx-1519-max** (_integer_)                 | 大于1519字节的接收帧总数                                  |
| **rx-align-error** (_integer_)              | 接收到的对齐错误事件总数-位不沿八位边界对齐的数据包       |
| **rx-broadcast** (_integer_)                | 接收的广播帧总数                                          |
| **rx-bytes** (_integer_)                    | 接收字节总数                                              |
| **rx-carrier-error** (_integer_)            | 接收到的载波感知错误帧总数                                |
| **rx-code-error** (_integer_)               | 编码错误的接收帧总数                                      |
| **rx-control** (_integer_)                  | 接收到的控制帧或暂停帧总数                                |
| **rx-error-events** (_integer_)             | 带有活动错误事件的接收帧总数                              |
| **rx-fcs-error** (_integer_)                | 校验和错误的接收帧总数                                    |
| **rx-fragment** (_integer_)                 | 接收到的分片帧总数(与IP分片无关)                          |
| **rx-ip-header-checksum-error** (_integer_) | IP报头校验和错误的接收帧总数                              |
| **rx-jabber** (_integer_)                   | 接收到的戳戳报文总数-发送的数据包长度大于最大数据包长度   |
| **rx-length-error** (_integer_)             | 接收帧长度错误的总数                                      |
| **rx-multicast** (_integer_)                | 接收到的组播帧总数                                        |
| **rx-overflow** (_integer_)                 | 当设备资源不足以接收某个帧时，会导致接收到的溢出帧总数    |
| **rx-pause** (_integer_)                    | 接收到的暂停帧总数                                        |
| **rx-runt** (_integer_)                     | 接收帧总数小于最小64字节，通常是由碰撞引起的              |
| **rx-tcp-checksum-error** (_integer_)       | 接收到的TCP报头校验和错误帧总数                           |
| **rx-too-long** (_integer_)                 | 超过网络设备支持的最大帧长的接收帧总数，参见max-l2mtu属性 |
| **rx-too-short** (_integer_)                | 接收帧小于最小64字节的总数                                |
| **rx-udp-checksum-error** (_integer_)       | 接收到的UDP报头校验和错误帧总数                           |
| **rx-unicast** (_integer_)                  | 接收到的单播帧总数                                        |
| **rx-unknown-op** (_integer_)               | 接收到的未知以太网协议帧总数                              |
| **tx-64** (_integer_)                       | 传输的64字节帧总数                                        |
| **tx-65-127** (_integer_)                   | 传输65到127字节帧的总数                                   |
| **tx-128-255** (_integer_)                  | 传输128到255字节帧的总数                                  |
| **tx-256-511** (_integer_)                  | 传输256到511字节帧的总数                                  |
| **tx-512-1023** (_integer_)                 | 512到1023字节帧传输总数                                   |
| **tx-1024-1518** (_integer_)                | 传输1024到1518字节帧的总数                                |
| **tx-1519-max** (_integer_)                 | 大于1519字节的传输帧总数                                  |
| **tx-align-error** (_integer_)              | 传输的对齐错误事件总数-位不沿八位边界对齐的数据包         |
| **tx-broadcast** (_integer_)                | 传输的广播帧总数                                          |
| **tx-bytes** (_integer_)                    | 传输字节总数                                              |
| **tx-collision** (_integer_)                | 产生碰撞的传输帧总数                                      |
| **tx-control** (_integer_)                  | 传输控制帧或暂停帧的总数                                  |
| **tx-deferred** (_integer_)                 | 由于介质繁忙导致第一次传输尝试延迟的传输帧总数            |
| **tx-drop** (_integer_)                     | 由于输出队列已满而丢弃的传输帧总数                        |
| **tx-excess -collision** (_integer_)        | 已经发生多次碰撞但从未成功传输的帧总数                    |
| **tx-excessive-deferred** (_integer_)       | 由于介质已经很忙而延迟了一段时间的传输帧总数              |
| **tx-fc -error** (_integer_)                | 校验和错误的传输帧总数                                    |
| **tx-fragment** (_integer_)                 | 传输的分片帧总数(与IP分片无关)                            |
| **tx-carrier-sense-error** (_integer_)      | 带有载波感知错误的传输帧总数                              |
| **tx-late-collision** (_integer_)           | 传输帧中发生碰撞的总数                                    |
| **tx-multicast** (_integer_)                | 传输的组播帧总数                                          |
| **tx-multiple-collision** (_integer_)       | 产生多个碰撞并随后成功传输的传输帧总数                    |
| **tx-overflow** (_integer_)                 | 传输溢出帧总数                                            |
| **tx-pause** (_integer_)                    | 传输暂停帧总数                                            |
| **tx-all-queue-drop-byte** (_integer_)      | 所有输出队列丢弃的传输字节总数                            |
| **tx-all-queue-drop-packet** (_integer_)    | 所有输出队列丢弃的传输数据包总数                          |
| **tx-queueX-byte** (_integer_)              | 某个队列上传输的字节总数，**X** 应替换为队列号            |
| **tx-queueX-packet** (_integer_)            | 在某个队列上传输帧的总数，**X** 应替换为队列号            |
| **tx-runt** (_integer_)                     | 小于最小64字节的传输帧总数，通常是由碰撞引起的            |
| **tx-too short** (_integer_)                | 小于最小64字节的传输帧总数                                |
| **tx-rx-64** (_integer_)                    | 发送和接收的64字节帧总数                                  |
| **tx-rx-64-127** (_integer_)                | 发送和接收64到127字节帧的总数                             |
| **tx-rx-128-255** (_integer_)               | 发送和接收128到255字节帧的总数                            |
| **tx-rx-256-511** (_integer_)               | 发送和接收的256到511字节帧的总数                          |
| **tx-rx-512-1023** (_integer_)              | 发送和接收512到1023字节帧的总数                           |
| **tx-rx-1024-max** (_integer_)              | 发送和接收大于1024字节的帧总数                            |
| **tx-single-collision** (_integer_)         | 仅发生一次碰撞而随后传输成功的传输帧总数                  |
| **tx-too-long** (_integer_)                 | 大于最大数据包大小的传输总数                              |
| **tx-underrun** (_integer_)                 | 传输欠运行包总数                                          |
| **tx-unicast** (_integer_)                  | 发送的单播帧总数                                          |

以设备hAP ac2上的以太网统计信息为例:

```shell
[admin@MikroTik] > /interface ethernet print stats
                      name:           ether1 ether2         ether3        ether4 ether5
            driver-rx-byte:  182 334 805 898      0  5 836 927 820    24 895 692      0
          driver-rx-packet:    4 449 562 546      0  4 320 155 362       259 449      0
            driver-tx-byte:   15 881 099 971      0 70 502 669 211    60 498 056     53
          driver-tx-packet:       52 724 428      0     54 231 229       106 498      1
                  rx-bytes:  178 663 398 808      0  5 983 590 739 1 358 140 795      0
              rx-too-short:                0      0              0             0      0
                     rx-64:       12 749 144      0        362 459       125 917      0
                 rx-65-127:        9 612 406      0     20 366 513       292 189      0
                rx-128-255:        6 259 883      0      1 672 588       261 013      0
                rx-256-511:        2 950 578      0        211 380       278 147      0
               rx-512-1023:        3 992 258      0        185 666       163 241      0
              rx-1024-1518:      119 034 611      0      2 796 559       696 254      0
               rx-1519-max:                0      0              0             0      0
               rx-too-long:                0      0              0             0      0
              rx-broadcast:       12 025 189      0      1 006 377        64 178      0
                  rx-pause:                0      0              0             0      0
              rx-multicast:        4 687 869      0         36 188       220 136      0
              rx-fcs-error:                0      0              0             0      0
            rx-align-error:                0      0              0             0      0
               rx-fragment:                0      0              0             0      0
               rx-overflow:                0      0              0             0      0
                  tx-bytes:   16 098 535 973      0 72 066 425 886   225 001 772      0
                     tx-64:        1 063 375      0        924 855        37 877      0
                 tx-65-127:       26 924 514      0      2 442 200       959 209      0
                tx-128-255:       14 588 113      0        924 746       295 961      0
                tx-256-511:        1 323 733      0      1 036 515        33 252      0
               tx-512-1023:        1 287 464      0      2 281 554         3 625      0
              tx-1024-1518:        7 537 154      0     48 212 304        64 659      0
               tx-1519-max:                0      0              0             0      0
               tx-too-long:                0      0              0             0      0
              tx-broadcast:              590      0        145 800       823 038      0
                  tx-pause:                0      0              0             0      0
              tx-multicast:                0      0      1 039 243        41 716      0
               tx-underrun:                0      0              0             0      0
              tx-collision:                0      0              0             0      0
    tx-excessive-collision:                0      0              0             0      0
     tx-multiple-collision:                0      0              0             0      0
       tx-single-collision:                0      0              0             0      0
     tx-excessive-deferred:                0      0              0             0      0
               tx-deferred:                0      0              0             0      0
         tx-late-collision:                0      0              0             0      0
```