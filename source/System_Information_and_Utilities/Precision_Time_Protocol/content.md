# 概述

精确时间协议用于同步整个网络的时钟。在局域网中，它的时钟精度达到亚微秒范围，适用于测量和控制系统。RouterOS支持IEEE 1588-2008、PTPv2。支持取决于硬件，请参阅下面的支持设备列表。

支持功能:

- 边界/普通时钟
- 端到端延迟模式
- PTP延迟模式
- UDP over IPv4组播传输模式
- L2传输模式
- 可以配置priity1来决定主备关系
- PTP时钟不与系统时钟同步

# 通用属性

**Sub-menu:** `/system ptp`

| 属性                                                            | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **port**                                                        | 用于添加、删除或查看指定端口的子菜单                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| **status**                                                      | 显示PTP端口状态和从端口延迟的子菜单                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| **comment** (_string_;Default:)                                 | PTP配置文件的简短描述                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| **name** (_string_;Default:)                                    | PTP配置文件名称                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **delay-mode** (_auto \| e2e \| ptp_; Default: **auto**)        | 配置PTP配置文件的延迟模式<br>-  _auto_ -自动选择延迟模式<br>- _e2e_ -使用延迟请求-响应机制<br>- _ptp_ -使用对等体延迟机制                                                                                                                                                                                                                                                                                                                                                                                          |
| **priority1** (_integer [0..255]_; auto; Default: **auto**)     | 影响特级大师选择的优先级值                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| **profile** (_802.1as; default; g8275.1;_ Default: **default**) | IEEE 1588-2008包含了一个定义PTP操作参数和选项的_profile概念。<br>IEEE 802.1AS是PTP的一个改编版本，用于音视频桥接和时间敏感网络。使用delay-mode=p2p, transport-mode=l2;建议使用priity1 =auto。<br>g8275.1配置文件用于完全感知ptp的网络中的频率和相位同步。只允许priority1=auto (128)， priority2=128, domain=24, delay-mode=e2e, transport=l2。<br>默认配置文件，PTPv2默认配置，允许比其他配置文件更多的配置选项，但是自动设置的默认值对应于:priority =128。Priority2 =128, domain=0,transport=ipv4, delay-mode=e2e |
| **transport** (_auto; ipv4;  l2;_ Default: **auto**)            | 传输协议:IPv4或layer2                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |

有关精确时间协议的更多详细信息，请参见以下标准IEEE 1588和IEEE 802.1as。

强烈建议保留默认自动值，因为配置文件之间有不同的需求。手动分配它们可能会导致配置错误。

# 配置

要配置设备参与PTP，首先需要创建PTP配置文件:

```shell
/system ptp add name=ptp1
#to view the created profile use
/system ptp print
Flags: I - inactive, X - disabled
0 name="ptp1" priority1=auto delay-mode=auto transport=auto profile=default
```

请注意

每台设备只支持1个PTP配置文件


创建PTP配置文件后，您需要为其分配端口:

```shell
/system ptp port add interface=ether1 ptp=ptp1
#to view assigned ports use
/system ptp port print
Flags: I - inactive
0 ptp=ptp1 interface=ether8
 
1 ptp=ptp1 interface=ether22
```

需要监控PTP配置文件，使用monitor命令:

```shell
#on grandmaster device
[admin@grandmaster] > system ptp monitor numbers=0
name: test
clock-id: 64:D1:54:FF:FE:EB:AE:C3
priority1: 30
priority2: 128
i-am-gm: yes
 
#on non-grandmaster device
[admin@328] /system ptp monitor 0
name: ptp1
clock-id: 64:D1:54:FF:FE:EB:AD:C7
priority1: 128
priority2: 128
i-am-gm: no
gm-clock-id: 64:D1:54:FF:FE:EB:AE:C3
gm-priority1: 30
gm-priority2: 128
master-clock-id: 64:D1:54:FF:FE:EB:AE:C3
slave-port: ether8
freq-drift: 2147483647 ppb
offset: 1396202830 ns
hw-offset: 1306201921 ns
slave-port-delay: 2075668440 ns
```

## 监控属性

| 属性                   | 说明                                                                                          |
| ---------------------- | --------------------------------------------------------------------------------------------- |
| **clock- ID:**         | 本地时钟ID                                                                                    |
| **priority1:**         | priority1值，取决于所选择的PTP配置文件，用于影响宗师选举的可调值。                            |
| **priority2:**         | priority2的值，在RouterOS中不可调整                                                           |
| **i-am-gm:** yes \| no | 显示设备是否是特级大师时钟                                                                    |
| **gm-clock-id:**       | grandmaster时钟ID -在一个域中，一个时钟是使用协议进行时钟同步的最终时间源。                   |
| **gm-priority1:**      | 大师优先级1                                                                                   |
| **gm-priority2:**      | 大师优先级2                                                                                   |
| **master-clock-id:**   | 主时钟ID -在单个精确时间协议(PTP)通信路径的上下文中，是该路径上所有其他时钟同步的时间源时钟。 |
| **slave-port:**        | 显示哪个端口指向主时钟或宗师时钟                                                              |
| **freq-drift:**        | 频率漂移:PPB(十亿分之一)频率漂移-如果没有同步，每秒相对于主时钟丢失的时间。                   |
| **offset:**            | 时钟值之间的差异                                                                              |
| **hw-offset:**         | 与硬件时钟的偏移量                                                                            |
| **slave-port-delay:**  | 数据包送到直连设备所花费的时间                                                                |

# 设备支持

## 支持设备

- CRS326-24G-2S+仅支持千兆以太网接口
- CRS328-24P-4S+仅支持千兆以太网接口
- CRS317-1G-16S+所有端口支持
- SFP+和QSFP+接口支持CRS326-24S+2Q+
- CRS312-4C+8XG所有端口支持
- CRS318-16P-2S+仅支持千兆以太网接口

## 不支持设备

-   CRS305-1G-4S+
-   CRS309-1G-8S+
-   CRS328-4C-20S-4S+
-   CRS354-48G-4S+2Q+
-   CRS354-48P-4S+2Q+