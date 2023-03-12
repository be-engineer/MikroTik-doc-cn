# 概述

**Sub-menu:** `/interface ethernet poe`

本页介绍了如何在有一个 PoE 输出接口的 MikroTik 设备上使用 PoE 输出（[以太网供电](https://en.wikipedia.org/wiki/Power_over_Ethernet)）功能。 MikroTik 用 RJ45 模式 B 引脚分配进行配电，其中 PoE 通过引脚 4,5 (+) 和 7,8 (-) 传递。 如果设备支持使用 PoE 输出为其他设备供电，则建议使用 **至少 18V** 作为输入电压，但支持多个输出电压的设备除外（例如 [CRS112-8P-4S-IN](https://mikrotik.com/product/crs112_8p_4s_in), [CRS328-24P-4S+RM](https://mikrotik.com/product/crs328_24p_4s_rm), [CRS354-48P-4S+2Q+RM](https://mikrotik.com/product/crs354_48p_4s_2q_rm))。

## MikroTik 支持 PoE 输出标准

MikroTik 设备可以支持以下部分或全部 PoE 标准：

- **Passive PoE-Out up to 30 V** - PoE 标准，不需要 PSE（供电设备）和 PD（受电设备）之间的协商。 PoE 输出使用与提供给 PSE（供电设备）相同的电压。 支持高达 30 V 输入电压的设备的 PoE 输出标准。PD 电阻应介于 3kΩ 至 26.5kΩ 之间。 （例如 [hEX PoE lite](https://mikrotik.com/product/RB750UPr2)、[RB3011UiAS-RM](https://mikrotik.com/product/RB3011UiAS-RM)、[RB2011iL-IN](https://mikrotik.com/product/RB2011iL-IN)

- **Passive PoE-Out up to 57 V** - 与低压（高达 30 V）PoE 输出一样工作，但也能够通过 PoE 端口提供高压。 输出电压取决于连接到 PSE 的电源。 可以为 af/at 兼容设备供电，这些设备接受 4,5 (+) 和 7,8 (-) 供电，并且不需要 PoE 协商。 PD 电阻的范围应为 3kΩ 至 26.5kΩ。 （例如 [cAP ac](https://mikrotik.com/product/cap_ac)、[hAP ac](https://mikrotik.com/product/RB962UiGS-5HacT2HnT)、 [wsAP ac lite](https://mikrotik.com/product/wsap_ac_lite)

- **IEEE Standards 802.3af/at** - 也称为 PoE Type 1/PoE+ Type 2，是由 IEEE 定义的 PoE 标准。 这些标准的目的是减少供应商之间的不兼容性。 支持 af/at 的 MikroTik PSE 能够为 Type 1 和 Type 2 PD 供电。 有效的 PD 应具有 23.75kΩ 至 26.25kΩ 的 PoE-In 电阻。 支持 af/at 标准的 MikroTik 设备也可以切换到 Passive PoE-Out 模式。 （例如 [CRS112-8P-4S-IN](https://mikrotik.com/product/crs112_8p_4s_in)、[CRS328-24P-4S+RM](https://mikrotik.com/product/crs328_24p_4s_rm)、[CRS354 -48P-4S+2Q+RM](https://mikrotik.com/product/crs354_48p_4s_2q_rm)

每个 PoE-Out 实施都支持过载和短路检测。

**注意：** 一些 MikroTik 设备支持所有标准(例如 [CRS112-8P-4S-IN](https://mikrotik.com/product/crs112_8p_4s_in)、[CRS328-24P-4S+RM]( https://mikrotik.com/product/crs328_24p_4s_rm), [netPower 16P](https://mikrotik.com/product/netpower_16p), [CRS354-48P-4S+2Q+RM](https://mikrotik.com/product/crs354_48p_4s_2q_rm) 等...)

## 如何选择PoE PSE

此表可帮助选择最适合需求的 PSE 设备。

<table class="relative-table wrapped confluenceTable" style="border: 1px solid #000000"><colgroup><col style="width: 114.0px;"><col style="width: 110.0px;"><col style="width: 99.0px;"><col style="width: 107.0px;"><col style="width: 89.0px;"><col style="width: 186.0px;"><col style="width: 114.0px;"><col style="width: 111.0px;"><col style="width: 111.0px;"></colgroup><tbody><tr><th rowspan="2" style="border: 1px solid #000000" class="confluenceTh"><p><br></p><p >Device name</p></th><th rowspan="2"  style="border: 1px solid #000000" text-align: center;" class="confluenceTh"><p><br></p><p>PoE-Out port count</p></th><th rowspan="2" style="border: 1px solid #000000" text-align: center;" class="confluenceTh"><p><br></p><p>Passive PoE</p></th><th rowspan="2" style="border: 1px solid #000000" text-align: center;" class="confluenceTh"><p><br></p><p>802.3af/at</p></th><th rowspan="2" style="border: 1px solid #000000" text-align: center;" class="confluenceTh"><p><br></p><p>802.3bt</p></th><th rowspan="2"  style="border: 1px solid #000000" text-align: center;" class="confluenceTh"><p><br></p><p>Power input</p></th><th colspan="2" style="border: 1px solid #000000" text-align: center;" class="confluenceTh">Maximum output per port</th><th rowspan="2" style="border: 1px solid #000000" class="confluenceTh"><p style="text-align: center;">Maximum power output, W</p></th></tr><tr><th style="border: 1px solid #000000" class="confluenceTh"><p>Input 18-30V, mA</p></th><th style="border: 1px solid #000000" class="confluenceTh">Input 30-57V, mA</th></tr>
<tr><td style="border: 1px solid #000000"  class="confluenceTd"><p><strong>CSS610-8P-2S+IN</strong></p></td><td style="border: 1px solid #000000"  class="confluenceTd">8</td><td style="border: 1px solid #000000"  class="confluenceTd">+</td><td style="border: 1px solid #000000"  85.4883px;" class="confluenceTd">+</td><td style="border: 1px solid #000000"  class="confluenceTd">-</td><td style="border: 1px solid #000000"  class="confluenceTd"><p>AC &amp;<span style="letter-spacing: 0.0px;">DC 48-57 V</span></p></td><td style="border: 1px solid #000000"  class="confluenceTd">1000</td><td style="border: 1px solid #000000"  class="confluenceTd">625</td><td style="border: 1px solid #000000"  class="confluenceTd">140</td></tr>
<tr><td style="border: 1px solid #000000"  class="confluenceTd"><p><strong>CRS328-24P-4S+RM</strong></p></td><td style="border: 1px solid #000000"  class="confluenceTd">24</td><td style="border: 1px solid #000000"  class="confluenceTd">+</td><td style="border: 1px solid #000000"  85.4883px;" class="confluenceTd">+</td><td style="border: 1px solid #000000"  class="confluenceTd">-</td><td style="border: 1px solid #000000"  class="confluenceTd">AC</td><td style="border: 1px solid #000000"  class="confluenceTd">1000</td><td style="border: 1px solid #000000"  class="confluenceTd">450</td><td style="border: 1px solid #000000"  class="confluenceTd">450</td></tr><tr><td style="border: 1px solid #000000"  class="confluenceTd"><p><strong>CRS354-48P-4S+2Q+RM</strong></p></td><td style="border: 1px solid #000000"  class="confluenceTd">48</td><td style="border: 1px solid #000000"  class="confluenceTd">+</td><td style="border: 1px solid #000000"  85.4883px;" class="confluenceTd">+</td><td style="border: 1px solid #000000"  class="confluenceTd">-</td><td style="border: 1px solid #000000"  class="confluenceTd">AC</td><td style="border: 1px solid #000000"  class="confluenceTd">1000</td><td style="border: 1px solid #000000"  class="confluenceTd">570</td><td style="border: 1px solid #000000"  class="confluenceTd">700</td></tr>
<tr><td style="border: 1px solid #000000"  class="confluenceTd"><p><strong>CRS112-8P-4S-IN</strong></p></td><td style="border: 1px solid #000000"  class="confluenceTd">8</td><td style="border: 1px solid #000000"  class="confluenceTd">+</td><td style="border: 1px solid #000000"  85.4883px;" class="confluenceTd">+</td><td style="border: 1px solid #000000"  class="confluenceTd">-</td><td style="border: 1px solid #000000"  class="confluenceTd">DC 18-30V &amp; DC 30-57V</td><td style="border: 1px solid #000000"  class="confluenceTd">1000</td><td style="border: 1px solid #000000"  class="confluenceTd">450</td><td style="border: 1px solid #000000"  class="confluenceTd">80</td></tr><tr><td style="border: 1px solid #000000"  class="confluenceTd"><p><strong>netPower 16P</strong></p></td><td style="border: 1px solid #000000"  class="confluenceTd">16</td><td style="border: 1px solid #000000"  class="confluenceTd">+</td><td style="border: 1px solid #000000"  85.4883px;" class="confluenceTd">+</td><td style="border: 1px solid #000000"  class="confluenceTd">-</td><td style="border: 1px solid #000000"  class="confluenceTd">DC 18-30V &amp; DC 30-57V</td><td style="border: 1px solid #000000"  class="confluenceTd">1100</td>
<td style="border: 1px solid #000000"  class="confluenceTd">600</td><td style="border: 1px solid #000000"  class="confluenceTd">160</td></tr><tr><td style="border: 1px solid #000000"  class="confluenceTd"><p><strong>RB5009UPr+S+IN</strong></p></td><td style="border: 1px solid #000000"  class="confluenceTd">8</td><td style="border: 1px solid #000000"  class="confluenceTd">+</td><td style="border: 1px solid #000000"  85.4883px;" class="confluenceTd">+</td><td style="border: 1px solid #000000"  class="confluenceTd">-</td><td style="border: 1px solid #000000"  class="confluenceTd">DC 18-30V or DC 30-57V</td><td style="border: 1px solid #000000"  class="confluenceTd">640</td><td style="border: 1px solid #000000"  class="confluenceTd">420</td><td style="border: 1px solid #000000"  class="confluenceTd">130</td></tr><tr><td style="border: 1px solid #000000"  class="confluenceTd"><p><strong>hEX PoE</strong></p></td><td style="border: 1px solid #000000"  class="confluenceTd">4</td><td style="border: 1px solid #000000"  class="confluenceTd">+</td><td style="border: 1px solid #000000"  85.4883px;" class="confluenceTd">+</td><td style="border: 1px solid #000000"  class="confluenceTd">-</td><td style="border: 1px solid #000000"  class="confluenceTd">DC 18-30V or DC 30-57V</td><td style="border: 1px solid #000000"  class="confluenceTd">1000</td><td style="border: 1px solid #000000"  class="confluenceTd">450</td><td style="border: 1px solid #000000"  class="confluenceTd">102</td></tr>
<tr><td style="border: 1px solid #000000"  class="confluenceTd"><p><strong>PowerBox Pro</strong></p></td><td style="border: 1px solid #000000"  class="confluenceTd">4</td><td style="border: 1px solid #000000"  class="confluenceTd">+</td><td style="border: 1px solid #000000"  85.4883px;" class="confluenceTd">+</td><td style="border: 1px solid #000000"  class="confluenceTd">-</td><td style="border: 1px solid #000000"  class="confluenceTd">DC 18-30V or DC 30-57V</td><td style="border: 1px solid #000000"  class="confluenceTd">1000</td><td style="border: 1px solid #000000"  class="confluenceTd">450</td><td style="border: 1px solid #000000"  class="confluenceTd">102</td></tr><tr><td style="border: 1px solid #000000"  class="confluenceTd"><p><strong>OmniTIK 5 PoE ac</strong></p></td><td style="border: 1px solid #000000"  class="confluenceTd">4</td><td style="border: 1px solid #000000"  class="confluenceTd">+</td><td style="border: 1px solid #000000"  85.4883px;" class="confluenceTd">+</td><td style="border: 1px solid #000000"  class="confluenceTd">-</td><td style="border: 1px solid #000000"  class="confluenceTd">DC 18-30V or DC 30-57V</td><td style="border: 1px solid #000000"  class="confluenceTd">1000</td><td style="border: 1px solid #000000"  class="confluenceTd">450</td><td style="border: 1px solid #000000"  class="confluenceTd">102</td></tr><tr><td style="border: 1px solid #000000"  class="confluenceTd"><p><strong>hEX PoE lite</strong></p></td><td style="border: 1px solid #000000"  class="confluenceTd">4</td><td style="border: 1px solid #000000"  class="confluenceTd">+</td><td style="border: 1px solid #000000"  85.4883px;" class="confluenceTd">-</td><td style="border: 1px solid #000000"  class="confluenceTd">-</td><td style="border: 1px solid #000000"  class="confluenceTd">DC 18-30V</td><td style="border: 1px solid #000000"  class="confluenceTd">1000</td><td rowspan="4" style="width: 88.6914px;text-align: center;" class="confluenceTd"><p><br></p><p><br></p><p>-</p></td><td style="border: 1px solid #000000"  class="confluenceTd">60</td></tr>
<tr><td style="border: 1px solid #000000"  class="confluenceTd"><p><strong>PowerBox</strong></p></td><td style="border: 1px solid #000000"  class="confluenceTd">4</td><td style="border: 1px solid #000000"  class="confluenceTd">+</td><td style="border: 1px solid #000000"  85.4883px;" class="confluenceTd">-</td><td style="border: 1px solid #000000"  class="confluenceTd">-</td><td style="border: 1px solid #000000"  class="confluenceTd">DC 18-30V</td><td style="border: 1px solid #000000"  class="confluenceTd">1000</td><td style="border: 1px solid #000000"  class="confluenceTd">60</td></tr><tr><td style="border: 1px solid #000000"  class="confluenceTd"><p><strong>RB260GSP</strong></p></td><td style="border: 1px solid #000000"  class="confluenceTd">4</td><td style="border: 1px solid #000000"  class="confluenceTd">+</td><td style="border: 1px solid #000000"  85.4883px;" class="confluenceTd">-</td><td style="border: 1px solid #000000"  class="confluenceTd">-</td><td style="border: 1px solid #000000"  class="confluenceTd">DC 18-30V</td><td style="border: 1px solid #000000"  class="confluenceTd">1000</td><td style="border: 1px solid #000000"  class="confluenceTd">60</td></tr><tr><td style="border: 1px solid #000000"  class="confluenceTd"><p><strong>OmniTIK 5 PoE</strong></p></td><td style="border: 1px solid #000000"  class="confluenceTd">4</td><td style="border: 1px solid #000000"  class="confluenceTd">+</td><td style="border: 1px solid #000000"  85.4883px;" class="confluenceTd">-</td><td style="border: 1px solid #000000"  class="confluenceTd">-</td><td style="border: 1px solid #000000"  class="confluenceTd">DC 18-30V</td><td style="border: 1px solid #000000"  class="confluenceTd">1000</td><td style="border: 1px solid #000000"  class="confluenceTd">60</td></tr></tbody></table>

## PoE 输出配置

所有带有 PoE 输出接口的 MikroTik 设备都支持 PoE 配置，可以从 RouterOS 和 SwOS 接口编辑配置。

### RouterOS

#### 用法

RouterOS 提供 Winbox、Webfig 和 CLI 配置 PoE-Out 的选项，使用 CLI 的基本命令是

| 属性                                                                   | 说明                                                                                       |
| ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| **print** ()                                                           | 打印 PoE-Out 相关设置。                                                                    |
| **export** ()                                                          | 导出显示在`/interface ethernet` 菜单下。                                                   |
| **monitor** (_string             \| interface_)                        | 使用`/interface ethernet poe monitor [find]` 命令显示指定端口或所有端口的 poe-out-status。 |
| **power-cycle** (_duration:0..1m                \| _; Default: **5s**) | 在指定的时间段内禁用 PoE 输出电源。                                                        |

##### 全局设置

一些 MikroTik PoE-Out 设备支持全局 PoE 设置，可以在“/interface ethernet poe settings”菜单下进行配置。 全局设置 ether1-poe-in-long-cable 功能禁用严格的输入/输出电流监控（短路检测），允许 PoE-Out 和长以太网电缆一起使用，避免不正确的短路检测。

| 属性                                       | 说明                                                                           |
| ------------------------------------------ | ------------------------------------------------------------------------------ |
| **ether1-poe-in-long-cable** (_yes \| no_) | 设置为 "yes" 会禁用所有Poe-out端口的短路检测。这是潜在的危险设置，应谨慎使用。 |

**注意：** 全局设置 _**ether1-pe-in-long-cable**_ 也会影响使用DC连接器供电的PSE的PoE-Out行为。

#### 端口设置

PoE-Out可以在菜单下进行配置。每个端口都可以独立控制。

| 属性                                                                         | 说明                                                                                                                                                                                                                                                                                                                                                                                                |
| ---------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **name** ()                                                                  | 接口名称                                                                                                                                                                                                                                                                                                                                                                                            |
| **poe-out** (_auto-on \| forced-on            \| off_; Default: **auto-on**) | 指定PoE-Out状态 <br>- auto-on - 电路板尝试检测是否可以向端口供电。对于供电，应该有3kΩ到26.5kΩ范围内的电阻。<br>- forced-on - 检测范围被取消。以太网电源始终处于开启状态。<br>- off - 端口的所有检测和电源都被关闭。                                                                                                                                                                                 |
| **poe-priority** (_integer:0..99 \| any_; Default: **10**)                   | poe-priority指定了PoE-Out端口的重要性，在达到PoE-Out总限额的情况下，端口优先级最低的接口将首先被关闭。<br>最高的优先级是0，最低的优先级是99。 如果有2个或更多的端口具有相同的优先级，那么端口号最小的端口将具有更高的优先级。例如，如果ether2和ether3有相同的优先权，并且检测到过流，那么ether3的PoE-Out将被关闭。<br>每隔6秒，如果PoE-Out因端口优先级而被关闭，则会检查端口是否有可能提供PoE-Out。 |
| **poe-voltage** (_auto \| low \| high_; Default: **auto**)                   | 这项功能允许在PoE-Out端口的两个电压输出之间进行手动切换。只对有可切换电压模式的PSE生效（[CRS112-8P-4S-IN](https://mikrotik.com/product/crs112_8p_4s_in), [CRS328-24P-4S+RM](https://mikrotik.com/product/crs328_24p_4s_rm), [netPower 16P](https://mikrotik.com/product/netpower_16p), [CRS354-48P-4S+2Q+RM](https://mikrotik.com/product/crs354_48p_4s_2q_rm)。                                    |
| **poe-lldp-enabled** _( yes \/ no;_ Default: **no**)                         | [链接层发现协议](https://en.wikipedia.org/wiki/Link_Layer_Discovery_Protocol "Link Layer Discovery Protocol")  (LLDP)是一个用于管理设备的二层以太网协议。LLDP允许PSE和PD之间进行信息交换。                                                                                                                                                                                                          |

**注意**。如果Poe-voltage=auto和Poe-out被设置为 "forced-on"，默认情况下将使用低电压。如果PD只支持高电压，请确保在强制PoE输出时也设置pe-voltage=high。

#### 电源循环设置

RouterOS提供了一种使用ping监控PD的可能性，当主机没有响应时，可以对PoE-Out端口进行电源循环。电源循环ping功能在 `/interface ethernet poe` 菜单下启用。

| 属性                                                                                   | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **power-cycle-ping-enabled** (_yes        \| no_; Default: **no**)                     | 启用PING看门狗，如果主机不响应ICMP或MAC-Telnet数据包，则关闭端口电源。                                                                                                                                                                                                                                                                                                                                                                                                           |
| **power-cycle-ping-address** (_IPv4       \| IPv6                  \| MAC_; Default: ) | 被监控的地址。从RouterOS 6.46beta16开始，如果配置了IP地址，就需要一个指向PD的活动路由，要确保PSE能够到达PD。如果指定了 MAC 地址， PSE 只从指定的以太网接口发送 MAC-Telnet ping 请求。当配置[bridge vlan-filtering](https://wiki.mikrotik.com/wiki/Manual:Interface/Bridge#Bridge_VLAN_Filtering "Manual:Interface/Bridge") 或某种方式的 [VLAN switching](https://wiki.mikrotik.com/wiki/Manual:Basic_VLAN_switching "Manual:Basic VLAN switching")，建议使用IP地址来监控你的PD。 |
| **power-cycle-ping-timeout** (_time:0..1h \| _; Default: **5s**)                       | 如果主机超过<timeout>时间没有反应，则PoE-Out端口将被关闭5秒。                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **power-cycle-interval** (_time           \| any_; Default: )                          | 在指定的时间间隔内禁用PoE-Out电源5s。与power-cycle-ping功能不相关。                                                                                                                                                                                                                                                                                                                                                                                                              |
  
如果启用了电源循环，`/interface ethernet poe monitor` 将显示主机的实际状态和电源循环执行的时间 [1](https://wiki.mikrotik.com/wiki/Manual:PoE-Out#PoE-Out_Monitoring)

### SwOS

SwOS接口提供基本的PoE-Out配置和监控选项，更多详情请见 [SwOS PoE](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=76415036#CRS3xxandCSS32624G2S+seriesManual-PoE) 用户手册。

## PoE-Out监控

### RouterOS

带有PoE-Out控制器（非注入器）的MikroTik设备提供端口监控选项。`/interface ethernet poe monitor [find]`。

| 属性                   | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **name** ()            | 接口名称                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| **poe-out** ()         | 显示PoE-Out设置                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| **poe-out-status** ()  | 显示端口上当前的PoE-Out状态<br>- powered-on - 电源已应用到端口，PoE-Out运行正常。<br>- waiting-for-load - PSE试图检测是否可以向端口供电。对于供电，应该有3kΩ到26.5kΩ范围内的电阻。<br>- short-circuit - 在PoE-Out端口上检测到短路，电源关闭，只有低电压的检测发生。<br>- overload - 超过PoE-Out的电流限制，PoE-Out端口的电源被关闭。关于端口限制，请参见各型号规格。<br>- voltage-too-low - PD不能用PSE提供的电压供电。<br>- current-too-low - 电流过低意味着PD消耗的电流（<10mA）比正常PoE-Out设备的电流要低，其原因可能是：<br>PD的输送电压太低，无法正常供电（例如，Vmin =>30V，但提供了24V）。<br>PD使用第二个电源，其电压高于PSE，所以所有的电流都来自第二个直流电源，而不是PSE PoE-Out端口。<br>- off - 该端口的所有检测和电源都关闭。 |
| **poe-out-voltage** () | 显示用于PD的PoE电压。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| **poe-out-current** () | 显示PD的端口电流（mA）。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| **poe-out-power** ()   | 显示PD的耗电量。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |

如果使用了 `power-cycle-ping` 功能，`/interface ethernet poe monitor [find]` 将显示额外的字段：

power-cycle-host-alive: <YES/NO>（显示受监控主机是否可达）
power-cycle-after:<TIME>（显示时间，之后端口将被重启）

### SNMP

用 SNMP 协议监控 PoE-Out 值，需要在 PSE 上启用 SNMP。 [SNMP 维基](https://wiki.mikrotik.com/wiki/Manual:SNMP)

SNMP OID 表：

- 1.3.6.1.4.1.14988.1.1.15.1.1.1 - interface-id
- 1.3.6.1.4.1.14988.1.1.15.1.1.2 - interface names
- 1.3.6.1.4.1.14988.1.1.15.1.1.4 - voltage in dV (decivolt)
- 1.3.6.1.4.1.14988.1.1.15.1.1.5 - current in mA
- 1.3.6.1.4.1.14988.1.1.15.1.1.6 - power usage in dW (deviwatt)

也可以从 RouterOS 请求 SNMP 值，例如，`snmp-walk`  将从所有可用的 PoE 输出端口打印电流 mA值：

/tool snmp-walk address=10.155.149.252 oid=1.3.6.1.4.1.14988.1.1.15.1.1.5

要获取具体的 OID 值，请使用 `snmp-get` 工具（在 ether3 接口上显示电流 mA值）：
tool snmp-get address=10.155.149.252 oid=1.3.6.1.4.1.14988.1.1.15.1.1.5.3

## PoE-Out提醒

### PoE-Out LED

#### 具有依赖性电压输出的型号

不同型号的PoE-Out LED行为可能有所不同，大多数型号会在一个额外的LED上显示PoE-Out状态。有一个电压输出的设备会亮起。

- 红色LED - PoE-Out端口状态为 **电源开启**（自动或强制开启模式）。
- 红色LED闪烁 - PoE-Out端口的状态是 **短路**。

#### 具有可选电压输出的型号

具有多种电压选项的型号可以显示额外的信息。

- 绿色三角形LED - PoE-Out端口状态为 **powered-on** （自动或强制开启模式），PD使用低电压。
- 红色三角形LED - PoE-Out端口状态为 **powered-on** （自动或强制开启模式），PD使用高电压（af/at或无源）。
- 闪烁的绿色三角形LED - PoE-Out端口状态（低电压）是 **短路** 或 **过载**。
- 闪烁的红色三角形LED - PoE-Out端口状态（高电压）是 **短路** 或 **过载**。

#### 特定型号的LED行为

- [CRS112-8P-4S-IN](https://mikrotik.com/product/crs112_8p_4s_in) - 所有PoE LED灯闪烁：在其中一个端口插入了错误的电压PSU。
- [netPower 16P](https://mikrotik.com/product/netpower_16p) - 所有PoE LED灯闪烁：电压错误的PSU被插入其中一个端口。
- [CRS328-24P-4S+RM](https://mikrotik.com/product/crs328_24p_4s_rm) - 表示超过了整体最大PoE输出限制。端口PoE-Out优先级将在3个独立的部分（每个8个端口）工作，任何部分超过150W的消耗都会发生过载。

### PoE-Out日志

默认情况下，PoE-Out事件 [logging](https://wiki.mikrotik.com/wiki/Manual:System/Log) 被启用，并使用 "警告 "和 "信息 "主题来通知用户PoE-Out状态的变化。日志添加到每个PoE-Out状态变化中。重要的日志将添加到 "警告 "主题中，信息性的日志将添加到 "信息 "主题中。 当PoE LLDP启用时，LLDP状态的更新可在设备日志中看到，例如。

`06:56:50 poe-out,debug ether4 LLDP TLV 25.0W request denied : hw-limit`

可能的拒绝原因：

- budget - 请求的功率超过PSE的总预算。
- hw-limit - 请求的功率超过硬件支持（PSU会影响这一点）。
- lowvoltage - 向低电压端口发出的LLDP请求。
- off - 端口关闭。
- class-limit - LLDP请求的功率超过类别所能提供的。
- cmd-failed - RouterOS无法向控制器发出请求。

为了避免在PD因为电流过低而不供电的情况下进行不必要的日志记录，RouterOS将过滤此类事件，每512个电流过低的事件添加一个日志。

如果有必要，可以禁用日志。

```shell
/system logging set [find topics~"info"] topics=info,!poe-out  
/system logging set [find topics~"warning"] topics=warning,!poe-out
```

### GUI/CLI中的PoE-Out警告

为了通知用户与PoE-Out有关的重要问题，信息将显示在Winbox/WebFig和CLI界面上。

`1 RS ;;; poe-out status: overload`
`ether1 ether 1500 1588 9204 64:D1:54:61:D5:E0`

WebFig和Winbox会在接口下通知用户。

![](https://help.mikrotik.com/docs/download/attachments/19136769/image2020-3-4_14-3-39.png?version=1&modificationDate=1583323419121&api=v2)

## 如何工作

### PoE-Out模式

#### 自动开启模式

如果在PoE-Out接口上选择了自动开启，那么端口就按照这个严格的顺序运行：

- 带有低电压的PSE检查所连接端口的电阻。如果检测到的电阻范围在（3kΩ到26.5kΩ）之间，则接通电源。
- 当电源接通时，PSE连续检查是否未达到过载极限或检测到短路
- 如果电缆被拔掉，端口返回检测状态，并保持关闭，直到检测到合适的PD为止

#### 强制开启模式

如果选择了forced-on，那么端口将严格按照这个顺序运行：

- PSE禁用端口上的电阻检查，并在4,5(+)和7,8(-)针脚上施加电源，即使没有连接电缆
- 当通电时，PSE仍然持续检查，如果没有检测到过载或短路。
- 拔掉电缆后，端口上的电源仍然是启用的。

#### 关闭模式

如果使用关闭模式，端口上的PoE-Out将关闭，不进行检测，接口像一个简单的以太网端口一样运行。

### PoE-Out限制

检查PoE-Out规格找出硬件限制是很重要的，因为不同的型号会有差异。

#### PoE-Out端口限制

PoE-Out端口有最大电流值的限制，这些电流值在特定的电压下工作，通常最大电流对于低电压设备（高达30V）和高电压设备（31至57V）是不同的。

#### PoE-Out总限制

PSE也有一个PoE-Out的总电流限制，即使单个端口的限制允许也不能超过。

#### PoE输出极性

所有MikroTik PSE使用相同的PoE-Out针脚极性 [Mode B](https://en.wikipedia.org/wiki/Power_over_Ethernet#Pinouts) 4,5 (+)和7,8 (-)，其他供应商可以在PD上使用相反或模式A针脚。反向极性需要使用交叉电缆，但模式A PD需要模式B到模式A转换器。

**注：** 无源PD的高输入浪涌电流可能导致PSE过流保护，请确保PD规格支持从PSE供电（而不仅仅是从无源电源注入器供电）。

### 安全

PSE具有以下安全特性：

#### PoE-Out兼容性检测

自动开启模式被认为是安全的，它将检查端口上的电阻是否在允许的范围内，然后才在接口上启用PoE out。该范围是3kΩ到26.5kΩ

##### 过载保护

当PoE-Out端口通电时，它将不断检查过载情况。如果检测到过载，PoE-Out会在端口上关闭，避免对PD或PSE造成损害。

几秒钟后，PoE Out功能将再次打开，以查看环境是否已经改变，PD是否可以再次供电。这对于没有连接到主电源的配置非常重要（比如太阳能装置、由于主电源故障而用电池运行的设备），当电压下降时-将被检测到过载，连接的设备将关闭。一段时间后，当电压水平恢复到通常的工作值时，连接的设备就可以再次通电。

##### 短路检测

当PoE-Out端口上的电源被启用时，PSE持续检查短路。如果检测到，确保对PD和PSE没有损害，所有端口的电源都会关闭。PSE将继续检查PoE-Out端口，直到环境恢复正常。

**警告：** 确保没有连接非标准的不兼容PD，电阻范围为3kΩ至26.5kΩ，这样PSE就不会尝试对其进行供电。

### 特定型号的功能

具有独立8端口部分的PSE（[CRS112-8P-4S-IN](https://mikrotik.com/product/crs112_8p_4s_in), [CRS328-24P-4S+RM](https://mikrotik.com/product/crs328_24p_4s_rm), [netPower 16P](https://mikrotik.com/product/netpower_16p), [CRS354-48P-4S+2Q+RM](https://mikrotik.com/product/crs354_48p_4s_2q_rm) 允许PoE-Out独立于RouterOS工作，这意味着可以重新启动/升级RouterOS而PD不会重新启动。

注意：[CRS328-24P-4S+](https://mikrotik.com/product/crs328_24p_4s_rm), [netPower 16P](https://mikrotik.com/product/netpower_16p) PoE-Out的优先级在每个8端口部分独立工作!

## PoE输出的例子

RouterOS允许在PoE-Out端口上定义优先级，所以如果安装要超过预算，PSE会以最低的优先级禁用不太重要的PD。

_0_ 优先级最高，_99_ 优先级最低。

### 设置优先级

CLI设置优先级的例子：

```shell
/interface ethernet poe set ether2 poe-priority=10  
/interface ethernet poe set ether3 poe-priority=13  
/interface ethernet poe set ether4 poe-priority=11  
/interface ethernet poe set ether5 poe-priority=14
```

当电源预算超过PoE-Out的总限额时，会发生什么情况 - 首先，如果检测到过载，ether5将被关闭（最低的优先级），然后重新检查，如果仍然检测到总限额过载，下一个优先级的端口将被关闭，在这个例子中，ether3将被关闭。这两个端口每隔几秒钟就会到达，以检查是否有可能打开这些端口的PoE-Out。开机将按照切断电源的相反顺序进行。

### 相同的优先级

如果所有或某些端口都有相同的优先级，那么端口号最低的端口将有更高的优先级。

```shell
/interface ethernet poe set ether2 poe-priority=10  
/interface ethernet poe set ether3 poe-priority=10  
/interface ethernet poe set ether4 poe-priority=10  
/interface ethernet poe set ether5 poe-priority=10
```

在这个例子中，如果达到总的PoE-Out限制，ether5将首先被关闭，然后是ether4和ether3，因为这些端口都有相同的Poe优先权。

### 监控PoE-Out

可以使用 `/interface ethernet poe monitor <interface>` 命令来监控PoE-Out端口。

```shell
[admin@MikroTik] > interface ethernet poe monitor [find]  
name: ether2 ether3 ether4 ether5  
poe-out-voltage: 23.2V 23.2V 23.2V  
poe-out-current: 224mA 116mA 64mA  
poe-out-power: 5.1W 2.6W 1.4W```
```

### 电源循环ping

用power-cycle-ping功能监控连接的PD。

`/interface ethernet poe set ether1 power-cycle-ping-enabled=yes power-cycle-ping-address=192.168.88.10 power-cycle-ping-timeout=30s`

在这个例子中，连接到ether1的PD使用power-cycle-ping功能持续监控，它发送ICMP ping请求并等待回复。如果IP地址为192.168.88.10的PD超过30s没有回应，PoE-Out端口将被关闭5s。

## 故障排除

在PD从PSE供电时不开机或意外重启的情况下，建议首先检查。

- **PD支持的输入电压** - PSE的输出电压必须在PD支持的范围内。否则，PD与PSE不兼容将无法上电。检查PD的数据手册。
- **PD支持输入PoE-in标准** - 有些PD不支持af/at标准，即使它有PoE-in支持到57V，检查PD数据表。
- **PD是由PSE重新启动的**。
  - 检查PD是否超过PSE的PoE-Out端口限制和Total-PoE-Out端口限制，检查PSE数据表。
  - 检查电压限制是否下降到支持的水平（可能是由于电线上的电压降造成的）。
  - 检查是否使用了合适的电源，电源的输出功率应从以下方面计算:
     `(MAX power consumption of PSE) + (MAX power consumption of all PD) + 10%)`
- 检查是否使用了高质量的以太网电缆，这对使用PoE尤其重要。
- **检查RouterOS版本** - 有可能一些PoE相关的功能会随着RouterOS的更新而更新，确保你运行的是最新的 [RouterOS版本](https://mikrotik.com/download)。
- **PD不开机**
  - 在某些情况下，即使PD支持无源PoE，并且消耗的电量没有超过指定的PSE端口限制，也不会开机。这可能是由于浪涌电流触发了PSE上的过流保护造成的。确保PD规格支持从PSE供电（而不仅仅是从无源电源注入器供电）。
  - 极性 - 具有相反或不同引脚的设备可能无法从所有PSE上电。检查PD的数据手册。
  - 不兼容的电阻 - PD的电阻应该在3kΩ到26.5kΩ之间（对于无源PoE），在af/at上从23.75kΩ到26.25kΩ。

## 传统

### PoE-Out控制器升级

运行RouterOS 5.x的PoE-Out设备也可以持有旧的PoE-Out控制器固件，升级到RouterOS 6.x将自动更新PoE-Out固件。1.x和2.x之间的PoE-Out控制器固件的变化将导致更高的最大端口限制（0.5A到1A），如果硬件支持的话，还将提供一些可以监测的额外数据，并允许使用PoE-Out优先权。

所有带有RouterOS 6.x的MikroTik设备已经支持最新的PoE-Out固件。
