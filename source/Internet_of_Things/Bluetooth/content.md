# 摘要

蓝牙是一种短距离的无线技术，允许在特定的蓝牙频道上广播数据。

有40个独特的频段（通道），每个频段有2兆赫的间隔。37、38和39通道用于主要广播，0-36通道用于数据传输。

在广播过程中，BLE数据包被广播。这个数据包包含序言、访问地址、PDU和CRS字段。

序言和访问地址字段帮助接收器检测帧。CRS字段用于检查错误。PDU由PDU头和PDU有效载荷组成。PDU定义了数据包本身。

PDU头包含关于PDU类型的信息。基于该类型，有效载荷字段可能不同。

例如，当PDU类型为ADV\NONCONN\IND时，PDU有效载荷由 "AdvA"（一个包含广告商地址信息的字段）和 "AdvData"（一个包含数据信息的字段）字段组成:

1 octet = 1 byte = 8 bits


<table class="relative-table wrapped confluenceTable" style="border: 1px solid #000000 "><colgroup><col style="border: 1px solid #000000 "><col style="border: 1px solid #000000 "></colgroup><tbody><tr><td style="border: 1px solid #000000" class="confluenceTd">Preamble</td><td style="border: 1px solid #000000" class="confluenceTd">1 octet</td></tr><tr><td style="border: 1px solid #000000" class="confluenceTd">Access-Address</td><td style="border: 1px solid #000000" class="confluenceTd">4 octets</td></tr><tr><td style="border: 1px solid #000000" class="confluenceTd">PDU</td><td style="border: 1px solid #000000" class="confluenceTd"><ul><li>PDU Header = 2 octets</li><li>PDU Payload = AdvA (6 octets)+AdvData (0...31 octets)</li></ul></td></tr><tr><td colspan="1" style="border: 1px solid #000000" class="confluenceTd">CRS</td><td colspan="1" style="border: 1px solid #000000" class="confluenceTd">3 octets</td></tr></tbody></table>

有不同的PDU类型。

- ADV_IND（其中有效载荷由AdvA[6octets]+AdvData[0-31 octets]组成，用于可连接、可扫描的无定向广告）。
- ADV_NOCONN_IND（有效载荷由AdvA[6octets]+AdvData[0-31 octets]组成，用于不可连接的、不可扫描的不定向广告）。
- ADV_SCAN_IND（其中有效载荷由AdvA[6octets]+AdvData[0-31 octets]组成，用于可扫描、无定向广告）。
- SCAN_REQ（其中有效载荷由ScanA[6octets]+AdvA[6octets]组成，ScanA字段包含扫描仪的地址，AdvA包含广告商的地址，用于请求SCAN_RSP响应）。
- SCAN_RSP（其中有效载荷由AdvA[6octets]+ScanRspData[0-31 octets]组成，其中ScanRspData可以包含来自广告主主机的任何数据，它用于响应SCAN_REQ请求）。
- ADV_DIRECT_IND（其中有效载荷由AdvA[6octets]+TargetA[6octets]组成，其中TargetA是PDU寻址的设备地址域，用于可连接、定向广告）。
- 等等

你可以在 [这里](https://www.bluetooth.com/specifications/specs/core-specification/) 找到更多关于数据包结构的信息（蓝牙规格）。

RouterOS中的蓝牙接口的主要应用是监测由其他设备（例如 [蓝牙标签](https://help.mikrotik.com/docs/display/UM/TG-BT5-IN) 广播的蓝牙广告数据包（扫描器功能）或广播广告数据包（广告商功能）。

# 配置

**Sub-menu：** `/iot bluetooth`

**注**: 要使用 **iot** 包。

**注**：检查设备的规格页面，确保设备支持蓝牙。

物联网软件包可与RouterOS 6.48.3版本一起使用。可以从 [下载页面](https://mikrotik.com/download)  -  "额外包 "下获得。

## 设备

在这个菜单中，可以检查和设置一般的蓝牙芯片参数:

```shell
[admin@device] > iot bluetooth print
Columns: NAME, PUBLIC-ADDRESS, RANDOM-STATIC-ADDRESS, ANTENNA
  #  NAM  PUBLIC-ADDRESS     RANDOM-STATIC-ADD  ANTENNA
  0  bt1  00:00:00:00:00:00  F4:4E:E8:04:77:3A  internal
[admin@device] /iot bluetooth set
```


**注**：公共地址是IEEE注册的永久地址。这个地址不能被改变。在上面的 "打印 "例子中，设备没有分配公共地址（所有八位数都设置为0）。

可配置的设置显示如下:

| 属性                                                 | 说明                       |
| ---------------------------------------------------- | -------------------------- |
| **antenna** (_string_; Default: internal)            | 选择使用内部或外部蓝牙天线 |
| **name** (_string_; Default: )                       | 蓝牙芯片/接口的描述名称    |
| **random-static-address** (_MAC address_; Default: ) | 用户可配置的蓝牙芯片的地址 |

可以用以下命令监控芯片的统计信息:


```shell
[admin@device] /iot bluetooth print stats
Columns: NAME, RX-BYTES, TX-BYTES, RX-ERRORS, TX-ERRORS, RX-EVT, TX-CMD, RX-ACL, TX-ACL
  #  NAM  RX-BYTE  TX-  R  T  RX-EV  TX  R  T
  0  bt1  1857835  235  0  0  46677  45  0  0
```

## 广播者

在这个菜单中，可以设置蓝牙芯片广播广告包。可以用命令检查和设置广播者设置：


```shell
[admin@device] > iot bluetooth advertisers print
Flags: X - DISABLED
Columns: DEVICE, MIN-INTERVAL, MAX-INTERVAL, OWN-ADDRESS-TYPE, CHANNEL-MAP, AD-SIZE
#   DEVICE  MIN-INTERVAL  MAX-INTERVAL  OWN-ADDRESS-TYPE  CHANNEL-MAP  AD-SIZE
0 X bt1     1280ms        2560ms        random-static              37        0
                                                                   38        
                                                                   39        
[admin@device] /iot bluetooth advertisers set
```

可配置的设置如下:

| 属性                                                                                                                             | 说明                                                                                                                                                                                                                                                                                                                                                                                                         |
| -------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **ad-structures** (_string_; Default: )                                                                                          | 为广告数据包选择一个预先配置的结构。更多信息见 "AD结构 "部分。                                                                                                                                                                                                                                                                                                                                               |
| **channel-map** (_37\|38 \| 39_; Default: 37, 38, 39)                                                                            | 用于广播的通道                                                                                                                                                                                                                                                                                                                                                                                               |
| **disabled** (_yes \| no_; Default: **yes**)                                                                                     | 禁用或启用蓝牙芯片广播包的选项                                                                                                                                                                                                                                                                                                                                                                               |
| **max-interval** (_integer:_20..10240;__ Default: **2560** **ms**)                                                               | 广播广告数据包的最大间隔时间。                                                                                                                                                                                                                                                                                                                                                                               |
| **min-interval** (_integer:_20..10240;__ Default: **1280 ms**)                                                                   | 广播广告数据包的最小间隔。                                                                                                                                                                                                                                                                                                                                                                                   |
| **own-address-type** (_public \| random-static \| rpa-fallback-to-public \| rpa-fallback-to-random_; Default: **random-static**) | 在广播数据包有效载荷中使用的MAC地址：<br>- public → 使用IEEE注册的永久地址。<br>- random-static → 使用用户可配置的地址（会在下一次上电时改变）。<br>- rpa-fallback-to-public → 使用可解析的随机私人地址（RPA），只有当接收方拥有身份解析密钥（IRK）时才能解析。如果不能生成RPA，将使用公共地址。<br>- rpa-fallback-to-random → 与 "rpa-fallback-to-public "相同，但如果不能生成RPA，将使用随机静态地址代替。 |

**注**： 广告包将在每一个 _min-interval_  <= **X** <=  _max-interval_ 毫秒的时间内广播。

## AD结构

本节允许定义由蓝牙芯片广播的广告数据包有效载荷。

目前只支持3种类型： 0x08 "缩短的本地名称"；0x09 "完整的本地名称"；0xFF "制造商特定数据"。

可以用命令检查和设置 "AD结构 "：


```shell
[admin@device] > iot bluetooth advertisers ad-structures print
Columns: NAME, TYPE, DATA
#  NAME  TYPE              DATA
0  test  short-local-name  TEST
[admin@device] > iot bluetooth advertisers ad-structures set
```

可配置的属性如下所示:

| 属性                                                                             | 说明                                                                                                    |
| -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| **data** (_string_; Default: )                                                   | 定义广播包的AdvData部分有效载荷                                                                         |
| **name** (_string_; Default: )                                                   | AD结构的描述名称                                                                                        |
| **type** (complete-local-name / manufacturer-data / short-local-name; Default: ) | 设置AD结构类型的选项：<br>- 0x08 "缩短的本地名称"<br>- 0x09 "完整的本地名称"<br>- 0xFF "制造商特定数据" |

例如，如果选择了 "缩短的本地名称 "类型，并且 "数据 "字段被配置为 "TEST"→有效载荷的AdvData部分将看起来像这样：

05 08 54 45 53 54 (十六进制格式)

其中第一个八位字节（05）显示后面的字节数（5个字节），第二个八位字节（08）显示类型（缩短的本地名称）。第三个、第四个、第五个和第六个（等等）八位字节是 "数据"/[54（十六进制）= T（ASCII），45（十六进制）= E（ASCII），53（十六进制）= S（ASCII），54（十六进制）= T（ASCII）] 。

这同样适用于 "完整本地名称 "类型。只有AdvData有效载荷中的第二个八位数会有所不同，将被设置为09。

对于 "制造商特定数据 "类型，需要以十六进制格式配置 "数据 "字段。这种类型的第二个八位数将被设置为FF。

## 扫描者

在这个菜单中，你可以设置蓝牙芯片的扫描者设置。如果禁用，设备就不能再接收广播报告。启用后，可以在 "广播报告 "选项卡中监测广播报告（本指南后面会有解释）。可以用命令检查和设置扫描设置：


```shell
[admin@device] > iot bluetooth scanners print
Flags: X - DISABLED
Columns: DEVICE, TYPE, INTERVAL, WINDOW, OWN-ADDRESS-TYPE, FILTER-POLICY, FILTER-DUPL
ICATES
#   DEVICE  TYPE     INTERVAL  WINDOW  OWN-ADDRESS-TYPE  FILTER-POLICY  FIL
0 X bt1     passive  10ms      10ms    random-static     default        off
[admin@device] /iot bluetooth scanners set
```

可配置的属性如下:

| 属性                                                                                                                                                                                                                                                                                                                                                                                                                                                               | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **disabled** (_yes\|no_; Default: **no**)                                                                                                                                                                                                                                                                                                                                                                                                                          | 禁用或启用蓝牙芯片接收广播报告的选项。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| **filter-duplicates** (keep-newest \| keep-oldest \| off; Default: **off**)                                                                                                                                                                                                                                                                                                                                                                                        | 丢弃重复广告的选项：<br>- keep-newest → 保留最新的报告（丢弃最旧的）。只有来自单一AdvA的最新PDU会被保留。<br>- keep-oldest → 保留最老的报告（丢弃最新的）。只有来自单个AdvA的最老的PDU将被保留。这种类型的PDU过滤发生在控制器层面，因此它是最有效的（能源/带宽方面）重复过滤方法。<br>-  off → 不丢弃重复的内容。所有相同AdvA的PDU将被保留。<br>重复的广播报告是指从同一设备地址发送的广告报告。实际数据（有效载荷的 "AdvData "部分）可能会改变/不同，在确定重复的广播报告时，它不被视为重要的。意思是说，例如，如果蓝牙接口从同一个标签收到10个有效载荷（有效载荷后，间隔1秒）：<br>- 如果你使用 "keep-oldest "设置→蓝牙接口将只显示从该标签收到的第一个有效载荷（9个后续有效载荷将被过滤掉）。 <br>- 如果你使用 "keep-newest "设置→蓝牙接口将只显示从该标签收到的最后一个有效载荷（每个后续有效载荷将重写前一个）。 |
| **filter-policy** (default \| whitelist _\| no_; Default: **default**)                                                                                                                                                                                                                                                                                                                                                                                             | 设置过滤策略（控制器级广播过滤）的选项：<br>- 默认→当此策略被启用时，扫描者只接受ADV_IND、ADV_NOCONN_IND、ADV_SCAN_IND、SCAN_RSP和ADV_DIRECT_IND（其中TargetA是扫描仪自己的蓝牙地址）PDU类型。<br>- 白名单→当此策略启用时，扫描者只接受由广播者广播的ADV_IND、ADV_NOCONN_IND、ADV_SCAN_IND、SCAN_RSP PDU类型，其地址配置为 "白名单 "部分，以及ADV_DIRECT_IND类型PDU（其中TargetA是扫描仪自己的蓝牙地址）。                                                                                                                                                                                                                                                                                                                                                                                                            |
| **interval** (_integer:3..10240_;Default: **10 ms**)                                                                                                                                                                                                                                                                                                                                                                                                               | 扫描者开始扫描下一个广播频道的时间。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| **own-address-type** (_public \| random-static \| rpa-fallback-to-public                                                                                                                                                                                                                                                                                                                                   \| rpa-fallback-to-random_; Default: **random-static**) | 扫描请求中使用的地址类型（如果使用主动扫描类型）：<br>- public → 使用IEEE注册的永久地址。<br>- random-static → 使用用户可配置的地址（将在下一次上电时改变）。<br>- rpa-fallback-to-public → 使用可解析的随机私人地址（RPA），只能用身份解析密钥（IRK）来解析。如果不能生成RPA，将使用公共地址。<br>- rpa-fallback-to-random → 与 "rpa-fallback-to-public "相同，但如果不能生成RPA，将使用随机静态地址。                                                                                                                                                                                                                                                                                                                                                                                                               |
| **type** (_active                                                                                                                                                                                                                                                                                                                                                                                          \| passive;_ Default: **passive**)                      | 定义扫描 者类型：<br>- active → 扫描者如果收到一个可扫描的广播就可以发送扫描请求。扫描者可以发送SCAN_REQ，以获得SCAN_RSP的响应。<br>- passive  → 扫描者将只监听广告，不发送数据（例如扫描请求）。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| **window** (_integer:3..10240;_ Default: **10 ms**)                                                                                                                                                                                                                                                                                                                                                                                                                | 扫描者扫描一个广告通道的时间。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |

例如，如果扫描间隔设置为20ms，意味着只有在20ms之后，设备才会开始扫描下一个通道。如果扫描窗口设置为10ms，意味着设备将只在这10ms的窗口内扫描每个通道。意思是，扫描37号通道10ms（窗口时间），再过10ms后开始扫描下一个通道（20ms[interval]-10ms[window]）。用10ms来扫描通道38，再过10ms后，设备将开始扫描通道39。

## 广播报告

这部分可以监测蓝牙广播报告（来自附近的广播）。可以用命令监控广播报告：


```shell

[admin@device] > iot bluetooth scanners advertisements print     
Columns: DEVICE, PDU-TYPE, TIME, ADDRESS-TYPE, ADDRESS, RSSI
 #  DEV  PDU-TYPE        TIME                  ADDRES  ADDRESS            RSSI 
 0  bt1  adv-noconn-ind  jul/28/2021 09:30:56  public  2C:C8:1B:93:16:49  -24dBm
 1  bt1  adv-noconn-ind  jul/28/2021 09:30:56  random  0B:16:17:9E:7B:EF  -60dBm
```

可以用以下命令为报告设置一个过滤器:


`[admin@device] > iot bluetooth scanners advertisements print where`

例如，要打印由特定蓝牙地址广播的报告，使用命令:


```shell

[admin@device] > iot bluetooth scanners advertisements print where address=XX:XX:XX:XX:XX:XX
 # DEVICE    PDU-TYPE       TIME                 ADD... ADDRESS                    RSSI     LENGTH DATA   
79 bt1       adv-noconn-ind jul/28/2021 09:46:38 public XX:XX:XX:XX:XX:XX        -70dBm         30 02010...
80 bt1       adv-noconn-ind jul/28/2021 09:46:43 public XX:XX:XX:XX:XX:XX        -67dBm         30 02010...
81 bt1       adv-noconn-ind jul/28/2021 09:46:44 public XX:XX:XX:XX:XX:XX        -70dBm         28 1bff0...
82 bt1       adv-noconn-ind jul/28/2021 09:46:48 public XX:XX:XX:XX:XX:XX        -75dBm         30 02010...
```

只显示RSSI强于-30 dBm的广播报告，使用命令：


```shell

[admin@device] > iot bluetooth scanners advertisements print where rssi > -30
 # DEVICE         PDU-TYPE       TIME                 ADDRESS-TYPE ADDRESS                    RSSI     LENGTH DATA      
307 bt1            adv-noconn-ind jul/29/2021 10:11:31 public       2C:C8:1B:93:16:49        -24dBm         22 15ff4f09.>
308 bt1            adv-noconn-ind jul/29/2021 10:11:31 public       2C:C8:1B:93:16:49        -26dBm         22 15ff4f09.>
```

可用的过滤器（可以在以下参数的帮助下过滤广播报告列表）：

| 过滤器             | 说明                                      |
| ------------------ | ----------------------------------------- |
| **address**        | 蓝牙广播者地址                            |
| **address-type**   | 广播者地址类型 (例如，公共或随机)         |
| **data**           | 十六进制格式的广播数据（AdvData有效载荷） |
| **device**         | 蓝牙芯片/接口名称                         |
| **epoch**          | 自Unix Epoch以来的毫秒数                  |
| **filter-comment** | 匹配的白名单过滤器的注释                  |
| **length**         | 广播数据长度                              |
| **pdu-type**       | 广播PDU的类型                             |
| **rssi**           | 信号强度                                  |
| **time**           | 广播数据包的接收时间                      |

## 白名单

在这个选项卡中，可以配置白名单，在 "扫描者"过滤策略中使用。换句话说，这是一个指定哪些蓝牙地址将被扫描的选项（显示在 "广播报告 "中）。

可以用命令查看白名单条目：


```shell
[admin@device] > iot bluetooth whitelist print
Columns: DEVICE, ADDRESS-TYPE, ADDRESS
# DEVICE  ADDRESS-TYPE  ADDRESS         
0 bt1     public        08:55:31:CF:F3:9C
```

可以用命令添加一个新的白名单条目：


`[admin@device] > iot bluetooth whitelist add`

可配置属性:

| 属性                                             | 说明                                                                                                         |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------ |
| **address** (_MAC address_; Default: )           | 广播者地址                                                                                                   |
| **address-type** (_public \| random_; Default: ) | 广播者地址地址类型                                                                                           |
| **comment** (_string_; Default: )                | 白名单的简短说明                                                                                             |
| **copy-from**                                    | 复制条目的选项 - 更多信息请查看 [控制台文档](https://wiki.mikrotik.com/wiki/Manual:Console#General_Commands) |
| **device** (_bt1_; Default: )                    | 选择蓝牙接口/芯片名称                                                                                        |
| **disabled** (_yes\|no_; Default: )              | 禁用或启用条目的选项                                                                                         |

只能添加8个白名单条目。
