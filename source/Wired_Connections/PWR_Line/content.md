# 概述

PWR-Line系列设备允许在支持的设备之间通过常规电源线进行类似以太网的连接。当插入同一电路时，PWR-Line设备将使用HomePlug AV标准建立连接。


**属性**

| 属性                                                                             | 说明                                                                                                                                                                                                                                                                                         |
| -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **arp** (_disabled \| enabled \| proxy-arp \| reply-only_; Default: **enabled**) | 地址解析协议模式:<br>- disabled表示接口不使用ARP<br>- enabled接口使用ARP<br>- proxy- ARP指定接口使用ARP代理特性<br>- reply-only表示接口只响应在/IP arp表中以静态表项形式输入的匹配的IP /MAC地址组合发出的请求。ARP表中不会自动存储动态表项。因此，要使通信成功，必须已经存在有效的静态条目。 |
| **bandwidth** (_integer/integer_; Default: **unlimited/unlimited**)              | 设置接口处理的最大rx/tx带宽(kbps)。所有Atheros [交换芯片](https://help.mikrotik.com/docs/display/ROS/Switch+Chip+Features) 端口都支持TX限制。RX限制仅支持在动脉粥样硬化8327/QCA8337开关芯片端口                                                                                              |
| **comment** (_string_;Default:)                                                  | 项目的描述性名称                                                                                                                                                                                                                                                                             |
| **l2mtu** (_integer [0..65536]_;Default:)                                        | Layer2最大传输单元。[RouterOS中的MTU](https://help.mikrotik.com/docs/display/ROS/MTU+in+RouterOS)                                                                                                                                                                                            |
| **mac-address** (_MAC_;Default:)                                                 | 接口的媒体访问控制号                                                                                                                                                                                                                                                                         |
| **mtu** (_integer [0..65536]_;Default:**1500**)                                  | Layer3最大传输单元                                                                                                                                                                                                                                                                           |
| **name** (_string_;Default:)                                                     | 接口名称                                                                                                                                                                                                                                                                                     |
| **orig-mac-address** (_MAC_;Default:)                                            |                                                                                                                                                                                                                                                                                              |
| **rx-flow-control** (_on \| off \| auto_;Default:**off**)                        | 当设置为on时，端口将处理接收到的暂停帧并在需要时暂停传输。**auto** 与 **on** 相同，除了当auto-negotiation=yes时，流量控制状态是通过考虑另一端的广告来解决的。支持AR724x、AR9xxx、QCA9xxx CPU端口、所有CCR端口和所有Atheros交换芯片端口                                                       |
| **tx-flow-control** (_on \| off \| auto_;Default:**off**)                        | 当设置为on时，端口将在满足特定缓冲区使用阈值时发送暂停帧。**auto** 与 **on** 相同，除了当auto-negotiation=yes时，流量控制状态是通过考虑另一端的广告来解决的。支持AR724x、AR9xxx、QCA9xxx CPU端口、所有CCR端口和所有Atheros交换芯片端口                                                       |

# 菜单特定命令

| 属性                   | 说明                                                                                         |
| ---------------------- | -------------------------------------------------------------------------------------------- |
| **configure** ()       | 该命令用来配置附加的PWR-Line设备的network-key、network-password、plc- ccco -selection-mode。 |
| **join**()             | 启动配对序列，该序列将查找处于配对模式的同一电路中的其他PWR-Line设备。此模式持续60秒。       |
| **leave**()            | 启动离开序列，本质上随机化设备的网络密钥。                                                   |
| **monitor**()          | 实时输出pwr线相关状态。                                                                      |
| **upgrade-firmware**() | 使用指定的firmware-file和pib-file文件升级PWR-Line设备。                                      |

# 配置示例

要使两个或多个设备能够相互连接，它们必须共享相同的网络密钥值。使用monitor命令可以看到当前配置的网络密钥为plc-actual-network-key。

```shell
[admin@MikroTik] > /interface pwr-line monitor pwr-line1
name: pwr-line1
connection-to-plc: ok
tx-flow-control: no
rx-flow-control: no
plc-actual-network-key: c973947c200e1540b0f84b571d92bebe
plc-hw-platform: QCA7420
plc-sw-platform: MAC
plc-fw-version: 1.4.0(24-20180515-CS)
plc-line-freq: 50Hz
plc-zero-crossing: detected
plc-mac: B8:69:F4:C4:34:68
```

## 方法1

有两种方法可以在不同的设备上设置相同的网络密钥。您可以使用network-key参数，它是network-password参数的散列版本。或者使用network-password参数，让路由器将哈希值应用于一个人类可读的字符串。

例如:

`/interface pwr-line configure pwr-line1 network-password=mynetwork`

同样的: 

`/interface pwr-line configure pwr-line1 network-key=cb01fcc6167bf3d1edb1433c2ebde4b3`

必须在希望相互通信的所有设备上设置相同的密钥或密码。

## 方法2

可以使用join和leave命令，使PWR-Line设备自动同步网络密钥值。建议在使用join命令之前使用leave命令，以确保新网络密钥是随机生成的，并且设备不属于任何旧网络。

`/interface pwr-line leave pwr-line1`

然后我们可以发出join命令。这样做时，配对序列将启用60秒，这意味着您必须在60秒内在另一台设备上启用配对模式才能成功配对。

`/interface pwr-line join pwr-line1`

## 方法3

还可以使用plc- ccco -selection-mode参数为PWR-Line设备(主或从)设置指定角色。

| 属性                                                                  | 说明                                                                                                                                                                                                |
| --------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **plc-cco-select -mode** (_auto \| always \| never_;Default:**auto**) | 设置PWR-Line设备模式:<br>- auto - PWR-Line将根据加入PWR-Line网络的情况自动决定扮演什么角色。<br>- always - PWR-Line将永远被迫充当“中央协调器”或主设备。<br>- never - PWR-Line将永远被迫充当从设备。 |

例子: 

```shell
/interface pwr-line configure pwr-line1 plc-cco-selection-mode=auto

/interface pwr-line configure pwr-line1 plc-cco-selection-mode=always

/interface pwr-line configure pwr-line1 plc-cco-selection-mode=never
```

# Sync按钮使用情况

- 保持0.5 - 3秒打开同步模式。120秒后将尝试与另一个PWR-LINE设备通信。橙色LED灯闪烁，表示处于搜索模式。您还必须在其他PWR-LINE设备上执行相同的操作，以便它们能够同步。再次按下按钮取消搜索。您也可以在RouterOS设置中手动设置安全密钥。

- 等待5 - 8秒生成新的安全密钥。这需要从现有的PWR-LINE网络中移除PWR-LINE设备。

- 长按10 ~ 15秒，重置PWR-LINE相关设置。

# 支持的硬件

该设备与我们的PWR-LINE AP完全兼容，并且具有microrousb端口的最新版本的产品，如hAP lite, hAP lite塔，hAP mini, mAP和mAP lite具有PWR-LINE接口。一个简单的软件升级到v6.44+就可以启用这个特性(由上述序列号以/9xx结尾的设备支持)。一些以前生产的设备也支持PWR-LINE功能-如果您的设备序列号以/8xx结尾，请升级到6.44+并查看PWR-LINE接口是否显示。