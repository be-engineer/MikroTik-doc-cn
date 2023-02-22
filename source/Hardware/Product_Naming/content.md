# 介绍

MikroTik的产品命名乍一看会让人困惑，但所有的产品代码都有一个合理的解释，并遵循一个代码。

## RouterBOARD产品命名细节

RouterBOARD (小版本RB)

\<board name> \<board features>-\<built-in wireless> \<wireless card features>-\<connector type>-\<enclosure type>

## 板名

Currently, there can be three types of board names:

- **3-symbol name**
  - 第1个符号代表系列（可以是一个数字或字母）
  - 第2位数字表示潜在的有线接口的数量（以太网、SFP、SFP+）。
  - 第3位数字表示潜在的无线接口的数量（内置和mPCI和mPCIe插槽）

- **Word** - 目前使用的名称：**OmniTIK, Groove, SXT, SEXTANT, Metal, LHG, DynaDish, cAP, wAP, LDF, DISC, mANTBox, QRT, DynaDish, cAP, hAP, hEX**。 如果板子在硬件上有根本性的变化（如完全不同的CPU），修订版本将添加在最后。

- **Exceptional naming** - 600、800、1000、1100、1200、2011、3011、4011板是该系列的独立代表，或有9个以上的有线接口，所以名称简化为百或开发年份。

## Board Features

板卡特征紧跟在板名之后（没有空格或破折号），除非板名称是一个单词，那么板特征就用空格隔开。

目前使用的功能（按使用顺序排列）：

- **U** - USB
- **P** - 带有控制器的电源注入器
- **i** - 无控制器的单端口电源注入器
- **A** - 更多的内存和（或）更高的许可级别
- **H** - 更强大的CPU
- **G** - 千兆（包括 "U"、"A"、"H"，如果不与 "L "一起使用）。
- **L** - 精简版
- **S** - SFP端口（传统用途 - SwitchOS设备）。
- **e** - PCIe接口扩展卡
- **x\<N>** - 其中N是CPU核心的数量（x2、x16、x36等）。
- **R** - MiniPCI或迷你PCIe插槽

## 内置无线的详细信息

如果板卡内置无线，那么所有功能都以下列格式表示：

`<band><power_per_chain><protocol><number_of_chains>`

- **band**
  - **5** - 5Ghz
  - **2** - 2.4Ghz
  - **52** - 双频5Ghz and 2.4Ghz

- **power per chain**
  - (not used) - "Normal" - <23dBm at 6Mbps 802.11a; <24dBm at 6Mbps 802.11g
  - **H** - "High" - 23-24dBm at 6Mbps 802.11a; 24-27dBm at 6Mbps 802.11g
  - **HP** - "High Power" - 25-26dBm 6Mbps 802.11a; 28-29dBm at 6Mbps 802.11g
  - **SHP** - "Super High Power" - 27+dBm at 6Mbps 802.11a; 30+dBm at 6Mbps 802.11g

- **protocol**
  - (not used) - for cards with only 802.11a/b/g support
  - **n** - for cards with 802.11n support
  - **ac** - for cards with 802.11ac support

- **number_of_chains**
  - (not used) - single chain
  - **D** - dual chain
  - **T** - triple chain

- **connector type**
  - (not used) - only one connector option on the model
  - **MMCX** - MMCX connector type
  - **u.FL** - u.FL connector type

## 外壳类型

- (not used) -产品的主要外壳类型
- **BU** - 板卡单元（无外壳）-适用于只需要板卡选项的情况，主要产品装在箱子里
- **RM** - 机架安装外壳
- **IN** - 室内机柜
- **EM** - 扩展内存
- **LM** - 简易内存
- **BE** - 黑色版机箱
- **TC** - 塔式（垂直）机箱
- **PC** - 被动冷却机箱(用于CCR)
- **TC** - 塔式（垂直）机箱外壳（用于hEX，hAP和其他家用路由器）
- **OUT** - 户外机箱

**更多的具体类型外壳是：**

- **SA** - 扇形天线罩(用于SXT)
- **HG** - 高增益天线罩（用于SXT）
- **BB** - Basebox外壳（用于RB911）
- **NB** - NetBox外壳（用于RB911）
- **NM** - NetMetal外壳(用于RB911)
- **QRT** - QRT机柜(用于RB911)
- **SX** - Sextant机柜(用于RB911,RB711)
- **PB** - PowerBOX机箱(用于RB750P, RB950P)

## 示例

解码 [RB912UAG-5HPnD](https://routerboard.com/RB912UAG-5HPnD)的命名。

- RB (RouterBOARD)
- 912 - 第9系列板卡，有1个有线（以太网）接口和2个无线接口（内置迷你PCIe）。
- UAG - 有一个USB接口，更多的内存和千兆以太网接口
- 5HPnD - 内置5GHz高功率双链无线网卡，支持802.11n

## CloudCoreRouter的命名细节

CloudCoreRouter（简称CCR）的命名包括：

`<4 digit number>-<list of ports>-<enclosure type>`

- **4位数的数字**
  - 第1位数字代表系列
  - 第2位（保留）
  - 第3-4位数字表示设备上总的CPU核的数量

- **端口列表**
  - -\<n>**G** 1G以太网端口数量
  - -\<n>**P** 带PoE输出的1G以太网端口数量
  - -\<n>**C** 组合式1G以太网/SFP端口数量
  - -\<n>**S** 1G SFP端口数量
  - -\<n>**G+** 2.5G以太网端口数量
  - -\<n>**P+** 带PoE输出的2.5G以太网端口数量
  - -\<n>**C+** 10G以太网/SFP+组合端口数量
  - -\<n>**S+** 10G SFP+端口数量
  - -\<n>**XG** 个5G/10G以太网端口
  - -\<n>**XP** 带PoE输出的5G/10G以太网端口数量
  - -\<n>**XC** 组合10G/25G SFP+端口数量
  - -\<n>**XS** 25G SFP+端口数量
  - -\<n>**Q+** 40G QSFP+端口数量
  - -\<n>**XQ** 100G QSFP+端口数量

- **外壳类型** - 与RouterBOARD产品相同。

## CloudRouterSwitch和CloudSmartSwitch的命名细节

CloudRouterSwitch（简称CRS，RouterOS设备）CloudSmartSwitch（简称CSS，SwOS设备）的命名包括：

`<3 digit number>-<list of ports>-<built-in wireless card>-<enclosure type>`

- **3位数字**
  - 第1位数字代表系列
  - 第2-3位数字 - 有线接口的总数（以太网、SFP、SFP+）。

- **端口列表**
  - -\<n>**F** 100M以太网端口数量
  - -\<n>**Fi** 带PoE-out注入器的100M以太网端口数量
  - -\<n>**Fp** 带有受控PoE-out的100M以太网端口数量
  - -\<n>**Fr** 带反向PoE（PoE-in）的100M以太网端口数量
  - -\<n>**G** 1G以太网端口数量
  - -\<n>**P** 带PoE-out的1G以太网端口数量
  - -\<n>**C** 组合式1G以太网/SFP端口数量
  - -\<n>**S** 1G SFP端口数量
  - -\<n>**G+** 2.5G以太网端口数量
  - -\<n>**P+** 带PoE输出的2.5G以太网端口数量
  - -\<n>**C+** 10G以太网/SFP组合端口数量
  - -\<n>**S+** 10G SFP+端口数量
  - -\<n>**XG** 个5G/10G以太网端口
  - -\<n>**XP**  带PoE输出的5G/10G以太网端口数量
  - -\<n>**XC** 组合10G/25G SFP+端口数量
  - -\<n>**XS** 25G SFP+端口数量
  - -\<n>**Q+** 40G QSFP+端口数量
  - -\<n>**XQ** 100G QSFP+端口数量

- **内置无线卡** - 与RouterBOARD产品相同。

- **外壳类型** - 与RouterBOARD产品相同。
