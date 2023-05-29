# 概述

WifiWave2包包含用于管理兼容的802.11ax和802.11ac wave 2无线接口的软件。
x86、ppc、mmips和tile架构的构建包含集中管理接口(作为CAPsMAN控制器)所需的配置实用程序。arm和arm64的构建还包含接口驱动程序和固件。

该软件包可以作为 [Extra Packages存档](https://mikrotik.com/download) 的一部分下载。

RouterOS中的WifiWave2包增加了部分Wave2特性，满足802.11ax设备的需求。一些带有标准“无线”封装的产品可以替换为wifiwave2，有关详细信息，请参阅 [本节](https://help.mikrotik.com/docs/display/ROS/WifiWave2#WifiWave2-Replacingstockwireless)。

命令行中的配置在/interface/wifiwave2/下完成，当使用图形配置工具(WinBox或WebFig)时，wifiwave2接口可以使用'Wireless'或'QuickSet'选项卡进行配置。

# WifiWave2术语

在我们继续之前，让我们熟悉一下对于理解WifiWave2的操作很重要的术语。这些术语将贯穿全文。

- **Profile** -指在以下WifiWave2子菜单之一下创建的预设配置:aaa、通道、安全、数据路径或互联。
- **Configuration** **profile** -配置在/interface/wifiwave2/ Configuration下预置，可以引用各种配置文件。
- **Station** -无线客户端。

# 基本配置:

**基本密码保护AP**

```shell
/interface/wifiwave2
set wifi1 disabled=no configuration.country=Latvia configuration.ssid=MikroTik security.authentication-types=wpa2-psk,wpa3-psk security.passphrase=8-63_characters
```

**以OWE转换模式打开AP**

机会无线加密(OWE)允许创建不需要知道密码就可以连接的无线网络，但仍然提供流量加密和管理框架保护的好处。这是对常规开放接入点的改进。

然而，由于网络不能同时进行加密和非加密，因此需要两个单独的接口配置来为不支持OWE的旧设备提供连接，并为支持OWE的设备提供OWE的好处。

此配置称为OWE转换模式。

```shell
/interface/wifiwave2
add master-interface=wifi1 name=wifi1_owe configuration.ssid=MikroTik_OWE security.authentication-types=owe security.owe-transition-interface=wifi1 configuration.hide-ssid=yes
set wifi1 configuration.country=Latvia configuration.ssid=MikroTik security.authentication-types="" security.owe-transition-interface=wifi1_owe
enable wifi1,wifi1_owe
```

支持OWE的客户端设备将优先使用OWE接口。如果在注册表中没有看到与常规打开AP关联的任何设备，则可能需要从运行转换模式设置转向运行单个ow加密接口。

**重置配置**

使用reset命令可以重置WifiWave2接口配置。

`/interface/wifiwave2 reset wifi1`

# 配置文件

WifiWave2新增的一个功能是配置文件，您可以创建各种预置，这些预置可以根据需要分配给接口。WifiWave2的配置设置根据本页面末尾的参数部分分组在配置文件中- aaa， 通道，配置，数据路径，互联和安全，然后可以分配给接口。**配置** **配置文件** 可以包括其他配置文件，以及从其他类别分开的参数。

这种可选的灵活性意味着允许每个用户以对他们最有意义的方式安排他们的配置，但这也意味着每个参数可能在配置的不同部分被分配不同的值。

以下优先级决定使用哪个值:

1.  接口设置中的值
2.  分配给接口的配置文件中的值
3.  分配给接口的配置文件中的值
4.  配置文件中的值分配给配置文件(该配置文件又分配给接口)。

如果您在任何时候都不确定将用于接口的哪个参数值，请参阅实际配置菜单。有关配置文件使用的示例，请参见以下示例。

**例如双频家用AP**

```shell
# Creating a security profile, which will be common for both interfaces
/interface wifiwave2 security
add name=common-auth authentication-types=wpa2-psk,wpa3-psk passphrase="diceware makes good passwords" wps=disable
# Creating a common configuration profile and linking the security profile to it
/interface wifiwave2 configuration
add name=common-conf ssid=MikroTik country=Latvia security=common-auth
# Creating separate channel configurations for each band
/interface wifiwave2 channel
add name=ch-2ghz frequency=2412,2432,2472 width=20mhz
add name=ch-5ghz frequency=5180,5260,5500 width=20/40/80mhz
# Assigning to each interface the common profile as well as band-specific channel profile
/interface wifiwave2
set wifi1 channel=ch-2ghz configuration=common-conf disabled=no
set wifi2 channel=ch-5ghz configuration=common-conf disabled=no
 
/interface/wifiwave2/actual-configuration print
 0 name="wifi1" mac-address=74:4D:28:94:22:9A arp-timeout=auto radio-mac=74:4D:28:94:22:9A
   configuration.ssid="MikroTik" .country=Latvia
   security.authentication-types=wpa2-psk,wpa3-psk .passphrase="diceware makes good passwords" .wps=disable
   channel.frequency=2412,2432,2472 .width=20mhz
 
 1 name="wifi2" mac-address=74:4D:28:94:22:9B arp-timeout=auto radio-mac=74:4D:28:94:22:9B  
   configuration.ssid="MikroTik" .country=Latvia
   security.authentication-types=wpa2-psk,wpa3-psk .passphrase="diceware makes good passwords" .wps=disable
   channel.frequency=5180,5260,5500 .width=20/40/80mhz
```

# 访问列表

访问列表提供了过滤和管理无线连接的多种方法。

RouterOS将检查每个新连接，看它的参数是否与任何访问列表规则中指定的参数匹配。

规则按照它们在列表中出现的顺序进行检查。只有第一个匹配规则中指定的管理操作才应用于每个连接。

已被访问列表规则接受的连接将定期检查，以查看它们是否保持在允许的 **时间** 和 **信号范围** 内。如果不这样做，他们将被终止。

在编写拒绝客户端的访问列表规则时要小心。在多次被AP拒绝后，客户端设备可能会开始回避它。

访问列表有两种参数: [filtering](https://help.mikrotik.com/docs/display/ROS/WifiWave2#WifiWave2-filtering) 和 [action](https://help.mikrotik.com/docs/display/ROS/WifiWave2#WifiWave2-action) 。过滤属性仅用于匹配应该应用访问列表规则的客户端。操作参数可以更改该特定客户端的连接参数，并可能使用访问列表规则中指定的参数覆盖其默认连接参数。

## MAC地址认证

MAC地址认证通过query-radius动作实现，是通过RADIUS服务器实现客户端MAC地址集中白名单的一种方式。

当客户端设备与配置了MAC地址认证的AP进行关联时，AP将向RADIUS服务器发送访问请求消息，用户名为设备的MAC地址，密码为空。如果RADIUS服务器以access-accept回答这样的请求，则AP继续执行为接口配置的任何常规身份验证过程(passphrase或EAP身份验证)。

## 访问规则示例

在工作时间内，只接受从附近设备到来宾网络的连接

```shell
/interface/wifiwave2/access-list/print detail
Flags: X - disabled
 0   signal-range=-60..0 allow-signal-out-of-range=5m ssid-regexp="MikroTik Guest" time=7h-19h,mon,tue,wed,thu,fri action=accept
 
 1   ssid-regexp="MikroTik Guest" action=reject
```

拒绝来自本地管理(anonymous/randomized)MAC地址的连接

```shell
/interface/wifiwave2/access-list/print detail
Flags: X - disabled
 0   mac-address=02:00:00:00:00:00 mac-address-mask=02:00:00:00:00:00 action=reject
```

如果需要提供对客户机的无线访问，但又不想共享无线密码，或者不想创建单独的SSID，那么为特定客户机分配不同的密码可能会很有用。当匹配的客户端连接到该网络时，访问列表将使该客户端使用不同的密码，而不是使用接口配置中定义的密码。只要确保特定的客户端不会首先被更通用的访问列表规则匹配即可。

```shell
/interface wifiwave2 access-list
add action=accept disabled=no mac-address=22:F9:70:E5:D2:8E interface=wifi1 passphrase=StrongPassword
```

# 频率扫描

/interface/wifiwave2/frequency-scan wifi1命令提供了执行frequency-scan命令可以获得的可用信道的射频条件信息。用于近似频谱使用，它可以帮助找到较少拥挤的频率。

![](https://help.mikrotik.com/docs/download/attachments/46759946/image-2023-3-10_18-6-37.png?version=1&modificationDate=1678464582039&api=v2)

运行频率扫描将断开所有连接的客户端，或者如果接口处于站模式，它将断开与AP的连接。

# 扫描命令

/interface wifiwave2 scan命令将扫描接入点并打印出它检测到的任何ap的信息。它不会显示每个频道的频率使用情况，但它会显示所有正在传输的接入点。可以使用“connect”按钮启动到特定AP的连接。

scan命令的参数与frequency-scan命令相同。

![](https://help.mikrotik.com/docs/download/attachments/46759946/image-2023-3-10_18-16-42.png?version=1&modificationDate=1678465186656&api=v2)

# 嗅探器

sniffer命令用来开启无线接口的监控模式。这使得接口成为所有WiFi传输的被动接收器。
该命令连续输出接收到的数据包的信息，并可以将它们本地保存到pcap文件中，或者使用TZSP协议将它们流式传输。

嗅探器将在为所选接口配置的任何通道上操作。

![](https://help.mikrotik.com/docs/download/attachments/46759946/wave2_sniffer.png?version=2&modificationDate=1679904643347&api=v2)

# WPS

## WPS客户端

wps-client命令用来从启用wps的AP获取认证信息。

`/interface/wifiwave2/wps-client wifi1`

## WPS服务器

配置AP接受客户端设备的WPS认证2分钟。

`/interface/wifiwave2 wps-push-button wifi1`

# Radios

可以通过运行 /interface/wifiwave2/radio print detail命令获得有关每个无线电功能的信息。查看接口支持哪些频带以及可以选择哪些信道是有用的。应用于接口的国家概况将影响结果。

```shell
interface/wifiwave2/radio/print detail
Flags: L - local
 0 L radio-mac=48:A9:8A:0B:F7:4A phy-id=0 tx-chains=0,1 rx-chains=0,1
     bands=5ghz-a:20mhz,5ghz-n:20mhz,20/40mhz,5ghz-ac:20mhz,20/40mhz,20/40/80mhz,5ghz-ax:20mhz,
      20/40mhz,20/40/80mhz
     ciphers=tkip,ccmp,gcmp,ccmp-256,gcmp-256,cmac,gmac,cmac-256,gmac-256 countries=all
     5g-channels=5180,5200,5220,5240,5260,5280,5300,5320,5500,5520,5540,5560,5580,5600,5620,5640,5660,
            5680,5700,5720,5745,5765,5785,5805,5825
     max-vlans=128 max-interfaces=16 max-station-interfaces=3 max-peers=120 hw-type="QCA6018"
     hw-caps=sniffer interface=wifi1 current-country=Latvia
     current-channels=5180/a,5180/n,5180/n/Ce,5180/ac,5180/ac/Ce,5180/ac/Ceee,5180/ax,5180/ax/Ce,
                 5180/ax/Ceee,5200/a,5200/n,5200/n/eC,5200/ac,5200/ac/eC,5200/ac/eCee,5200/ax...
                 ...5680/n/eC,5680/ac,5680/ac/eC,5680/ax,5680/ax/eC,5700/a,5700/n,5700/ac,5700/ax
     current-gopclasses=115,116,128,117,118,119,120,121,122,123 current-max-reg-power=30
```

虽然无线电信息为我们提供了有关支持通道宽度的信息，但也可以从产品页面推断出此信息，为此您需要检查以下参数:链数，最大数据速率。一旦知道了这些参数，就需要查看调制和编码方案(MCS)表，例如: [https://mcsindex.com/](https://mcsindex.com/)。

以hAP ax <sup>2</sup> 为例，我们可以看到MCS表中的链数为2，最大数据速率为1200 - 1201。在MCS表中，我们需要找到2个空间流链的入口，以及各自的数据速率，在这种情况下，80MHz是支持的最大信道宽度。

# 注册表

/interface/wifiwave2/registration-table/显示已连接的无线客户端列表及其详细信息。

![](https://help.mikrotik.com/docs/download/attachments/46759946/image-2023-3-10_18-29-11.png?version=1&modificationDate=1678465935336&api=v2)

## De-authentication

可以通过从注册表中删除无线对等体来手动解除身份验证(强制重新关联)。

`/interface/wifiwave2/registration-table remove [find where mac-address=02:01:02:03:04:05]`

# WifiWave2 CAPsMAN

WifiWave2 CAPsMAN允许从中央配置界面将无线设置应用于多个microtik WifiWave2 AP设备。

更具体地说，受控接入点系统管理器(CAPsMAN)允许无线网络管理的集中化。当使用CAPsMAN功能时，网络将由许多提供无线连接的“受控接入点”(CAP)和管理ap配置的“系统管理器”(CAPsMAN)组成，它还负责客户端身份验证。

WifiWave2 CAPsMAN仅将无线配置传递给CAP，所有转发决策都留给CAP自己-没有CAPsMAN转发模式。

要求:

- 任何支持WifiWave2包的RouterOS设备，只要拥有4级以上的RouterOS license，都可以成为受控无线接入点(CAP)。
- WifiWave2 CAPsMAN服务器可以安装在任何支持WifiWave2包的RouterOS设备上，即使设备本身没有无线接口
- 无限CAPs(接入点)由CAPsMAN支持

WifiWave2 CAPsMAN只能控制WifiWave2接口，WifiWave2 CAPs只能加入WifiWave2 CAPsMAN，同样，普通CAPsMAN只支持非WifiWave2 CAPs。

## CAPsMAN - CAP配置示例:

WifiWave2中的CAPsMAN使用与常规WifiWave2接口相同的菜单，这意味着当您将配置传递给CAPs时，您必须使用与常规WifiWave2接口相同的配置，安全性，通道配置等。

可以直接在“/interface/wifiwave2/configuration”下配置子配置菜单，或者参考之前在主配置文件中创建的配置文件

CAPsMAN:

```shell
#create a security profile
/interface wifiwave2 security
add authentication-types=wpa3-psk name=sec1 passphrase=HaveAg00dDay
 
#create configuraiton profiles to use for provisioning
/interface wifiwave2 configuration
add country=Latvia name=5ghz security=sec1 ssid=CAPsMAN_5
add name=2ghz security=sec1 ssid=CAPsMAN2
add country=Latvia name=5ghz_v security=sec1 ssid=CAPsMAN5_v
 
#configure provisioning rules, configure band matching as needed
/interface wifiwave2 provisioning
add action=create-dynamic-enabled master-configuration=5ghz slave-configurations=5ghz_v supported-bands=\
    5ghz-n
add action=create-enabled master-configuration=2ghz supported-bands=2ghz-n
 
#enable CAPsMAN service
/interface wifiwave2 capsman
set ca-certificate=auto enabled=yes
```

CAP:

```shell
#enable CAP service, in this case CAPsMAN is on same LAN, but you can also specify "caps-man-addresses=x.x.x.x" here
/interface/wifiwave2/cap set enabled=yes
 
#set configuration.manager= on the WifiWave2 interface that should act as CAP
/interface/wifiwave2/set wifi1,wifi2 configuration.manager=capsman-or-local
```

如果CAP为hAP ax<sup>2</sup>或hAP ax<sup>3</sup>，则强烈建议在CAP的网桥配置中启用RSTP

配置。manager应该只在CAP设备本身上设置，不要将其传递给您提供的CAP vai配置文件。

应该作为CAP的接口需要在"interface/wifiwave2/set wifiX configuration.manager="下进行额外配置。

# 高级示例

[企业无线安全与用户管理器v5](https://help.mikrotik.com/docs/display/ROS/Enterprise+wireless+security+with+User+Manager+v5)

为无线通信分配VLAN标签可以通过以下方法实现-[通用VLAN配置示例](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-VLANExample-TrunkandAccessPorts).

# 替换库存无线

wifiwave2包可以安装在一些产品上，这些产品随“无线”包一起发货，以取代它。

安装wifiwave2包将禁用其他无线接口配置方式。在安装之前，请确保备份您可能想要保留的任何无线和常规CAPsMAN配置。

## 兼容性

由于存储、RAM和架构的要求，只有以下产品可以将其捆绑的无线软件包替换为wifiwave2:

- hAP ac³(非lte)
- 观众和观众LTE6套件
- RB4011iGS + 5 hacq2hnd *

* RB4011iGS+5HacQ2HnD的2.4GHz无线接口与wifiwave2包不兼容。它将无法与安装的包一起使用。

## 好处

- WPA3认证和OWE(机会无线加密)
- 802.11w标准管理帧保护
- 802.11 r / k
- MU-MIMO和波束成形
- 2.4GHz频段IPQ4019接口的最大数据速率为400Mb/s
- OFDMA

## 丢失的功能

捆绑无线包的以下显著特性在wifiwave2包中尚不具备

- 站桥接或其他4地址模式
- nstream和Nv2无线协议

# 属性参考

## AAA属性

此类别中的属性配置接入点与AAA (RADIUS)服务器的交互。

下表中的某些参数以_format-string_作为它们的值。在format-string中，某些字符以以下方式解释:

| 角色         | 诠释                                      |
| ------------ | ----------------------------------------- |
| a            | 构成客户端设备MAC地址的十六进制字符(小写) |
| A            | 构成客户端设备MAC地址的大写十六进制字符   |
| i            | 构成AP接口MAC地址的十六进制字符(小写)     |
| I(大写' i ') | 构成AP接口MAC地址的大写十六进制字符       |
| N            | AP接口的全称(如:N;“wifi1 ')               |
| S            | 整个SSID                                  |

All other characters are used without interpreting them in any way. For examples, see default values.

| 属性                                                                                | 说明                                                                                                                                                     |
| ----------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **called-format** (_format-string_)                                                 |
| AP发送给RADIUS服务器的消息中被叫站id RADIUS属性值的格式。默认值:II-II-II-II-II-II:S |
| **calling-format** (_format-string_)                                                | AP发送给RADIUS服务器的消息中呼叫站id RADIUS属性值的格式。默认值:AA-AA-AA-AA-AA-AA                                                                        |
| **interim-update** (_time interval)_                                                | 向RADIUS服务器发送流量计费临时更新的时间间隔。默认值:5m                                                                                                  |
| **mac-caching** (_time interval_ \| _'disabled'_)                                   | 启用MAC地址认证时，RADIUS服务器应答的缓存时间长度。<br>这解决了由于RADIUS服务器应答延迟相对较高而导致客户端设备身份验证超时的问题。<br>默认值:disabled。 |
| **name** (_string_)                                                                 | AAA配置文件的唯一名称。无默认值。                                                                                                                        |
| **nas-identifier** (_string_)                                                       | AP发送给RADIUS服务器的消息中nas-identifier属性的值。默认为设备的主机名(/system/identity)。                                                               |
| **password-format** (_format-string_)                                               | 在进行MAC地址认证时，AP发送给RADIUS服务器的消息中计算User-Password属性值时使用的值格式。<br>默认值:""(空字符串)。                                        |
| **username-format** (_format-string_)                                               | 配置ap发送给RADIUS服务器的报文中User-Name属性值的格式。<br>默认值:' AA:AA:AA:AA:AA '                                                                     |

## 通道属性

此类别中的属性指定所需的无线电频道。

| 属性                                                                                                                            | 说明                                                                                                                                                                                                                                                                                                                                                                                                     |
| ------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **band** (_2ghz-g_ \| _2ghz-n_ \| _2ghz-ax_ \| _5ghz-a_ \| _5ghz-ac_ \| _5ghz-an_ \| _5ghz-ax_)                                 | 支持频段和无线标准。默认为最新支持的标准。<br>请注意，波段支持受无线电能力的限制                                                                                                                                                                                                                                                                                                                         |
| **frequency** (_list of integers or integer ranges_)                                                                            | 对于处于AP模式的接口，指定选择控制通道中心频率时要考虑的频率(MHz)。<br>当接口处于站模式时，指定扫描ap的频率。<br>不设置(默认)，以考虑无线电支持的所有频率，并由适用的监管配置文件允许。<br>该参数可以包含1个或多个以逗号分隔的整数值，也可以包含整数范围，使用语法rangebegin - rangeend:RangeStep表示<br>有效的channel.frequency值示例:<br>- 2412<br>- 2412, 2432, 2472<br>- 5180 5240:20 5500 - 5580:20 |
| **secondary-frequency** (_list of integers_ \| 'disabled')                                                                      | 频率(以MHz为单位)用于分割80+80MHz信道的次要部分的中心。<br>只支持 [官方80MHz频道](https://en.wikipedia.org/wiki/List_of_WLAN_channels#5_GHz_(802.11a/h/j/n/ac/ax)) 支持5210, 5290, 5530, 5610, 5690, 5775。<br>不设置(默认)自动选择辅助通道频率。                                                                                                                                                        |
| **skip-dfs-channels**  (_10min-cac_ \| _all_ \| _disabled_)                                                                     | 是否避免使用信道，需要对哪个信道进行可用性检查(监听雷达信号的存在)。<br>- _10min-cac_ - interface将避免使用需要10分钟CAC的通道<br>- _all_ - interface将避免使用所有需要CAC的通道<br>- _disabled_ (默认)-接口可以选择任何支持的通道，而不考虑CAC要求                                                                                                                                                      |
| **width** ( _20mhz_ \| _20/40mhz_ \| _20/40mhz-Ce_ \| _20/40mhz-eC_ \| _20/40/80mhz_ \| _20/40/80+80mhz_ \|  _20/40/80/160mhz_) | 无线电频道的宽度。默认为无线电硬件支持的最宽信道。                                                                                                                                                                                                                                                                                                                                                       |

## 配置属性

本节包括与接口和相关无线电操作相关的属性。

| 属性                                                 | 说明                                                                                                                                                                                                                     |
| ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **antenna-gain** (_integer 0..30_)                   | 覆盖默认天线增益。每个无线电的主接口设置使用同一无线电的每个接口的天线增益。<br>此设置不能覆盖天线增益低于无线电的最小天线增益。<br>无默认值。                                                                           |
| **beacon-interval** (_time interval 100ms..1s_)      | AP的信标帧间隔。缺省值:100ms。<br>802.11标准以_time单位_ (1 TU = 1.024 ms)定义信标间隔。信标之间的实际间隔将为每配置1毫秒的1 TU。<br>在同一无线电上运行的每个AP(即主AP及其所有“virtual/slave”AP)必须使用相同的信标间隔。 |
| **chains** (_list of integer 0..7_ )                 | [无线电链](https://en.wikipedia.org/wiki/RF_chain) 用于接收信号。默认为对应无线电硬件可用的所有链。                                                                                                                      |
| **country** (_name of a country_)                    | 确定将哪些监管域限制应用于接口。默认为“United States”。<br>为了符合当地法规并确保与其他设备的互操作性，正确设置此值非常重要。                                                                                            |
| **dtim-period** (_integer 1..255_)                   | 当AP上有节电模式的客户端设备时，发送组播流量的周期。用信标周期的倍数表示。<br>更高的值可以使客户端设备节省更多的能源，但会增加网络延迟。<br>默认值:1                                                                     |
| **hide-ssid** (_no_ \| _yes_)                        | - _yes_ - AP不将SSID包含在信标帧中，对广播SSID的探测请求不予回应。<br>- _no_ - AP在信标帧中包含自己的SSID，对广播SSID的探测请求进行应答。<br>默认值:无                                                                   |
| **mode** (_ap_ \| _station_)                         | 接口操作方式<br>- _ap_ (默认)-接口作为接入点运行<br>- _station_ - interface作为客户端设备，扫描发布已配置SSID的接入点                                                                                                    |
| **rrm** (_no_ \| _yes_)                              | - yes -开启对802.11k无线资源测量的支持<br>- no -禁用对802.11k无线资源测量的支持<br>默认值:是的                                                                                                                           |
| **ssid** (_string_)                                  | 无线网络的名称，即(E)SSID。无默认值。                                                                                                                                                                                    |
| **tx-chains** (_list of integer 0..7_)               | [Radio chains](https://en.wikipedia.org/wiki/RF_chain) 用于传输信号。默认为对应无线电硬件可用的所有链。                                                                                                                  |
| **tx-power** (_integer 0..40_)                       | 接口的发射功率限制(以dBm为单位)。不能用来设定权力超过监管规定的限制。默认不设置。                                                                                                                                        |
| **manager** (_capsman \| capsman-or-local \| local)_ | capsman -接口将仅作为CAP，此选项不应通过配置规则传递给CAP<br>CAPsMAN-or-local -如果/interface/wifiwave2/cap未启用，接口将通过CAPsMAN或使用自己的CAPsMAN进行配置。<br>本地接口不会与CAPsMAN联系以获得配置。               |

## 数据路径属性

与无线客户端设备之间的数据包转发有关的参数。

| 属性                                      | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ----------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **bridge** (_bridge interface_)           | 桥接接口添加接口，作为桥接端口。无默认值。                                                                                                                                                                                                                                                                                                                                                                                             |
| **Bridge-cost** (_integer_)               | 添加为网桥端口时使用的网桥端口开销。默认值:10                                                                                                                                                                                                                                                                                                                                                                                          |
| **Bridge-horizon** (_none_ \| _integer)_  | 添加为桥接端口时使用的桥接地平线默认值:none。                                                                                                                                                                                                                                                                                                                                                                                          |
| **client-isolation** (_no_ \| _yes_)      | 确定连接到此接口的客户端设备是否(默认情况下)与其他设备隔离。<br>可以使用访问列表规则在每个客户机的基础上覆盖此策略，因此AP可以混合使用隔离客户机和非隔离客户机。<br>被隔离客户端的流量不会被转发到其他客户端，非隔离客户端的单播流量不会被转发到被隔离的客户端。<br>默认值:无                                                                                                                                                          |
| **interface-list** (_interface list_)     | 将接口添加为其成员的列表。无默认值。                                                                                                                                                                                                                                                                                                                                                                                                   |
| **OpenFlow -switch** (_interface_)        | OpenFlow开关添加接口，当启用时作为端口。无默认值                                                                                                                                                                                                                                                                                                                                                                                       |
| **vlan-id** (_none_ \| _integer_ 1..4095) | 与该接口相连的客户端设备分配的缺省VLAN ID(仅与AP模式的接口相关)。<br>当为客户端分配了VLAN ID后，来自该客户端的流量会自动贴上该VLAN ID的标签，只有标有该VLAN ID的报文才会被转发到该客户端。<br>默认值:无<br>802.11n/ac接口在wifiwave2包下不支持这种类型的VLAN标签，但可以在网桥设置中 [配置](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-VLANExample-TrunkandAccessPorts) 作为VLAN访问端口。 |

## 安全属性

与认证相关的参数。

| 属性                                                                                                                               | 说明                                                                                                                                                                                                                                                                                                                                                                                             |
| ---------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **authentication-types** (_list of wpa-psk, wpa2-psk, wpa-eap, wpa2-eap, wpa3-psk, owe, wpa3-eap, wpa3-eap-192_)                   | 接口上要启用的认证类型。<br>缺省值为空列表(没有身份验证，开放网络)。<br>配置密码短语，将_wpa2-psk_身份验证方法(如果接口是AP)或wpa-psk和wpa2-psk(如果接口是站点)添加到默认列表中。<br>配置eap-username和eap-password将在默认列表中添加wpa-eap和wpa2-eap认证方法。                                                                                                                                 |
| **dh-groups** (_list of 19, 20, 21_)                                                                                               | SAE (WPA3)认证中使用的 [椭圆曲线加密组](http://www.iana.org/assignments/ipsec-registry/ipsec-registry.xhtml#ipsec-registry-10) 标识符。                                                                                                                                                                                                                                                          |
| **disable-pmkid** (_no_ \| _yes_)                                                                                                  | 对于AP模式的接口，禁用在EAPOL帧中包含PMKID。禁用PMKID可能导致与使用它的客户端设备的兼容性问题。<br>- _yes_ - EAPOL帧中不包含PMKID。<br>- _no_ (默认值)-在EAPOL帧中包含PMKID。                                                                                                                                                                                                                    |
| **eap-accounting** (_no_ \| _yes_)                                                                                                 | 对通过eap认证的对等体，向RADIUS服务器发送计费信息。默认值:不。<br>与EAP相关的属性仅与站模式下的接口相关。ap将EAP认证委托给RADIUS服务器。                                                                                                                                                                                                                                                         |
| **eap-anonymous-identity** (_string_)                                                                                              | EAP外部身份验证的可选匿名标识。无默认值。                                                                                                                                                                                                                                                                                                                                                        |
| **eap-certificate-mode** (_dont-verify-certificate_ \| _no-certificates_ \| _verify-certificate_ \| _verify-certificate-with-crl_) | RADIUS服务器TLS证书的处理策略。<br>- verify-certificate -要求服务器拥有有效的证书。检查它是否由受信任的证书颁发机构签名。<br>- not - verify-certificate(默认值)—不对证书进行任何校验。<br>- no-certificates—尝试通过匿名Diffie-Hellman密钥交换建立TLS隧道。当RADIUS服务器没有证书时使用。<br>- verify-certificate-with-crl—与_verify-certificate相同，但通过查看证书吊销列表来检查证书是否有效。 |
| **eap-methods** (_list of_ _peap, tls, ttls_)                                                                                      | 用于身份验证的EAP方法。默认为所有支持的方法。                                                                                                                                                                                                                                                                                                                                                    |
| **EAP-Password** (_string_)                                                                                                        | 当选择的EAP方法需要密码时，使用的密码。无默认值。                                                                                                                                                                                                                                                                                                                                                |
| **EAP-tls-certificate** (_certificate_)                                                                                            | 当选择的EAP认证方法需要证书时，设备证书存储中要使用的证书的名称或id。无默认值。                                                                                                                                                                                                                                                                                                                  |
| **eap-username** (_string_)                                                                                                        | 当所选EAP方法需要一个用户名时使用。无默认值。<br>在配置加密密码时要小心。<br>所有客户端设备必须支持AP用于连接的组加密密码，如果单播密码列表中包含任何它们不支持的密码，则某些客户端设备(特别是Intel®8260)也将无法连接。                                                                                                                                                                          |
| **encryption** (_list of  ccmp, ccmp-256, gcmp, gcmp-256, tkip_)                                                                   | 支持对单播通信进行加密的密码列表。<br>默认为ccmp。<br>802.11r快速BSS转换相关属性仅适用于AP模式的接口。站模式下的Wifiwave2接口不支持802.11r。<br>为了使客户端设备能够在两个ap之间顺利漫游，这两个ap需要由同一个RouterOS实例管理。有关如何集中管理多个ap的信息，请参见 [CAPsMAN](https://help.mikrotik.com/docs/display/ROS/WifiWave2#WifiWave2-WifiWave2CAPsMAN)。                                |
| **ft** (_no \| yes_)                                                                                                               | 是否开启802.11r快速BSS转换(漫游)。默认值:no。                                                                                                                                                                                                                                                                                                                                                    |
| **ft- mobile -domain** (_integer 0..65535_)                                                                                        | 快速BSS迁移域ID。默认值:44484 (0xADC4)。                                                                                                                                                                                                                                                                                                                                                         |
| **ft-nas-identifier**(字符串 _2..96个十六进制字符_ )                                                                               | 快速BSS转换PMK-R0密钥持有人标识符。默认值:接口的MAC地址。                                                                                                                                                                                                                                                                                                                                        |
| **ft-over-ds** (_no_ \| _yes_)                                                                                                     | 是否启用在DS(分布式系统)上的快速BSS转换。默认值:no。                                                                                                                                                                                                                                                                                                                                             |
| **ft-preserve-vlanid** (_no_ \| _yes_ )                                                                                            | - no-当客户端通过802.11r快速BSS转换连接到该AP时，根据访问和/或接口设置为其分配VLAN ID<br>- yes(默认) -当客户端通过802.11r快速BSS转换连接到该AP时，它保留在初始认证期间分配的VLAN ID<br>当依赖RADIUS服务器为用户分配VLAN id时，默认行为是必不可少的，因为RADIUS服务器仅用于初始身份验证。                                                                                                         |
| **ft-r0-key-lifetime** (_time interval 1s..6w3d12h15m_)                                                                            | 快速BSS转换PMK-R0加密密钥的生命周期。默认值:600000s(~7天)                                                                                                                                                                                                                                                                                                                                        |
| **ft- reasassociation -deadline** (_time interval 0..70s_)                                                                         | 快速BSS迁移重新关联截止时间。默认值:20s。                                                                                                                                                                                                                                                                                                                                                        |
| **group-encryption** (_ccmp \| ccmp - 256  \| gcmp \| gcmp - 256  \| tkip_)                                                        | 用于加密多播流量的密码。默认为ccmp。                                                                                                                                                                                                                                                                                                                                                             |
| **group-key-update** (_time interval_)                                                                                             | 组临时密钥(加密广播流量的密钥)更新的时间间隔。默认为24小时。                                                                                                                                                                                                                                                                                                                                     |
| **management-encryption** (_cmac \| cmac-256 \| gmac \| gmac-256_)                                                                 | 用于加密受保护的管理帧的密码。默认为cmac。                                                                                                                                                                                                                                                                                                                                                       |
| **management-protection** (_allowed \| disabled \| required_)                                                                      | 是否使用802.11w管理帧保护。不兼容标准无线封装中的管理框架保护。<br>缺省值取决于所选认证类型的值。WPA2允许使用管理保护，WPA3需要它。                                                                                                                                                                                                                                                              |
| **owe-transition-interface** (_i__nterface_)                                                                                       | 运行在OWE切换模式时，需要将MAC地址和SSID作为匹配AP发布的接口名称或接口内部id。<br>需要设置提供OWE的开放ap，但也可以使用不支持该标准的旧设备。参见 [下面的配置示例](https://help.mikrotik.com/docs/display/ROS/WifiWave2#WifiWave2-owe-transition-mode)。                                                                                                                                         |
| **passphrase** (_string of up to 63 characters_)                                                                                   | 用于PSK认证类型的密码短语。默认为空字符串- ""。<br>WPA-PSK和WPA2-PSK认证至少需要8个字符，而WPA3-PSK没有最小口令长度。                                                                                                                                                                                                                                                                            |
| **sae-anti-clogging-threshold** (_'disabled' \| integer_)                                                                          | 由于SAE (WPA3)关联是CPU资源密集型的，因此用虚假身份验证请求压倒AP会导致可行的拒绝服务攻击。<br>此参数通过指定正在进行的SAE身份验证的阈值提供了一种减轻此类攻击的方法，在该阈值时，AP将开始请求客户端设备在其身份验证请求中包含与其MAC地址绑定的cookie。然后，它将只处理包含有效cookie的身份验证请求。<br>默认值:5。                                                                              |
| **sae-max-failure-rate** (_disabled_ \| _integer_)                                                                                 | 每分钟失败的SAE (WPA3)关联速率，在此速率下AP将停止处理新的关联请求。默认值:40。                                                                                                                                                                                                                                                                                                                  |
| **SAE-pwe** (_both_ \| _hash-to-element_ \| _hunting-and-pecking_)                                                                 | 方法支持SAE密码元素的派生。默认值:both。                                                                                                                                                                                                                                                                                                                                                         |
| **wps** (_disabled_ \| _push-button_)                                                                                              | - _push-button_ (默认值)-调用 WPS -push-button命令后，AP将接受WPS认证2分钟。物理WPS按钮功能尚未实现。<br>- _disabled_ - AP将不接受WPS认证                                                                                                                                                                                                                                                        |

## 其他属性

| 属性                                                                                    | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| --------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **arp** (_disabled_ \| _enabled_   \| _local-proxy-arp_ \| _proxy-arp_ \| _reply-only)_ | 地址解析协议模式:<br>- _disabled_ 接口不使用ARP<br>- _enabled_ 接口将使用ARP(默认)<br>- _local-proxy-arp_ 在接口上执行代理ARP，并向同一接口发送应答<br>- _proxy-arp_ 在该接口上执行代理ARP，并向其他接口发送应答<br>- _reply-only_ 接口只响应在 [ARP](https://wiki.mikrotik.com/wiki/Manual:IP/ARP "Manual:IP/ARP") 表中以静态表项形式输入的IP/ MAC地址组合请求。ARP表中不会自动存储动态表项。因此，要使通信成功，必须已经存在有效的静态条目。 |
| **arp-timeout** (_time interval_ \| _auto_)                                             | 确定动态添加的ARP表项自收到来自相应IP地址的最后一个数据包以来的有效时间。<br>“auto”的值等于“/ip settings”中的“arp-timeout”的值，默认为30s。                                                                                                                                                                                                                                                                                                    |
| **disable-running-check** _(no_ \| _yes_)                                               | - _yes_ - interface的_r__unning_属性将在接口未被禁用时为true<br>- _no_ (默认)-接口的_running_属性将只在它已经建立到另一个设备的链接时为真                                                                                                                                                                                                                                                                                                      |
| **disabled** (_no \| yes_) (X)                                                          | 硬件接口默认关闭。虚接口则不然。                                                                                                                                                                                                                                                                                                                                                                                                               |
| **mac-address** (_MAC_)                                                                 | 用于接口的MAC地址(BSSID)。<br>硬件接口默认使用关联射频接口的MAC地址。<br>虚拟接口的缺省MAC地址由<br>1.  取关联主接口的MAC地址<br>2.  将第一个八位的倒数第二位设置为1，得到一个 [本地管理的MAC地址](https://en.wikipedia.org/wiki/MAC_address#Universal_vs._local)<br>3.如果需要，增加地址的最后八位元，以确保它不会与设备上另一个接口的地址重叠                                                                                                |
| **master-interface** (_interface_)                                                      | 多个接口配置可以在每个无线电台上同时运行。<br>它们中只有一个决定无线电的状态(是否启用，使用什么频率等)。这个“主”接口，被绑定到一个带有相应的_radio-mac._的无线电上<br>要在无线电上创建额外的(“虚拟”)接口配置，需要将它们绑定到相应的主接口。<br>无默认值。                                                                                                                                                                                     |
| **name** (_string_)                                                                     | 接口的名称。默认为wifiN，其中N是尚未用于命名接口的最小整数。                                                                                                                                                                                                                                                                                                                                                                                   |

## 只读属性

| 属性                         | 说明                                                                                                                                                                         |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **bound** (_boolean_) (B)    | 对于master接口(连接到无线电硬件的配置)总是为true。<br>当接口本身和主接口都未被禁用时，虚拟接口(与主接口链接的配置)为True。                                                   |
| **default-name** (_string_)  | 接口的默认名称                                                                                                                                                               |
| **inactive** (_boolean_) (I) | 当接口在AP模式下选择了一个通道进行操作(即配置已成功应用)时，为False。<br>当接口连接到AP(即配置已成功应用，找到具有匹配设置的AP)时，处于站模式的接口为False。<br>真正的否则。 |
| **master** (_boolean_) (M)   | 接口配置为True，它与无线电硬件绑定。虚接口为False。                                                                                                                          |
| **radio-MAC** (_MAC_)        | 关联电台的MAC地址。                                                                                                                                                          |
| **running** (_boolean_) (R)  | 当一个接口与另一个设备建立了链路时，为True。<br>如果disable-running-check设置为'yes'，则当接口未被禁用时为true。                                                             |

## 访问列表

**过滤参数**

| 参数                                                      | 说明                                                                                                                                                         |
| --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **interface** (_interface_ \| _interface-list_\| _'any'_) | 如果连接发生在指定的接口或属于指定列表的接口上，则匹配。默认值:any。                                                                                         |
| **MAC-address** (_MAC address_)                           | 如果客户端设备有指定的MAC地址，则匹配。无默认值。                                                                                                            |
| **mac-address-mask** (_MAC地址_)                          | 修改MAC-address参数以匹配是否等于对客户端MAC地址和给定地址掩码执行逐位与操作的结果。<br>默认值:FF:FF:FF:FF:FF(即客户端MAC地址必须与 MAC-address的值完全匹配) |
| **signal-range** (_min..max_)                             | 如果从客户端设备接收到的信号强度在给定范围内，则匹配。默认值:-120 . .120                                                                                     |
| **SSID-regexp** (_regex_)                                 | 如果给定的正则表达式与SSID匹配，则进行匹配。                                                                                                                 |
| **time** (_start-end,days_)                               | 匹配指定的时间和(可选的)星期。默认值:0s-1d                                                                                                                   |

**动作参数**

| 参数                                                                                                                                       | 说明                                                                                                                                                        |
| ------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **allow-signal-out-of-range** (_time period_ \| 'always')                                                                                  | 允许被连接的对等体的信号强度超出signal-range参数所要求的范围的时间长度。<br>如果设置为always，则只在关联过程中检查对端信号强度。<br>默认值:0。              |
| **action** (_accept_ \| _reject_ \| _query-radius_)                                                                                        | 是否授权连接<br>- _accept_ -允许连接<br>- _reject_ -不允许连接<br>-如果客户端MAC地址认证通过，则允许执行_query-radius_ - connection命令<br>默认值: _accept_ |
| **client-isolation** (_no_ \| _yes_)                                                                                                       |
| 是否将客户端与连接到同一AP的其他客户端 [隔离](https://help.mikrotik.com/docs/display/ROS/WifiWave2#WifiWave2-Datapathproperties)。无默认值 |
| **passphrase** (_string_)                                                                                                                  | 用给定的值覆盖默认的passphrase。无默认值。                                                                                                                  |
| **RADIUS-accounting** (_no_ \| _yes_)                                                                                                      | 用给定的值覆盖缺省RADIUS计费策略。无默认值。                                                                                                                |
| **vlan-id** (_none_ \| _integer 1..4095_)                                                                                                  | 为匹配的客户端分配给定的 [VLAN ID](https://help.mikrotik.com/docs/display/ROS/WifiWave2#WifiWave2-Datapathproperties) 。无默认值。                          |

## 频率扫描

可以通过命令frequency-scan获取可用信道的射频情况。

**命令参数**

| 参数                                        | 说明                                                                                                                                                                         |
| ------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **duration** (_time interval)_              | 退出前执行扫描的时间长度。用于非交互式使用。没有默认设置。                                                                                                                   |
| **freeze-frame-interval** (_time interval)_ | 更新命令输出的时间间隔。默认值:1s。                                                                                                                                          |
| **frequency** (_list of frequency /ranges)_ | 执行扫描的频率。参见上面的 [channel.frequency参数语法](https://help.mikrotik.com/docs/display/ROS/WifiWave2#WifiWave2-frequency-syntax) 了解更多细节。默认为所有支持的频率。 |
| **numbers** (_string)_                      | 要进行扫描的接口的名称或内部id。必需的。没有默认设置。                                                                                                                       |
| **rounds** (_integer)_                      | 退出前遍历可扫描频率列表的次数。用于非交互式使用。没有默认设置。                                                                                                             |
| **save-file** (string)                      | 要保存输出的文件名。没有默认设置。                                                                                                                                           |

  

**输出参数**

| 参数                        | 说明                                        |
| --------------------------- | ------------------------------------------- |
| **channel** (_integer)_     | 被扫描信道的频率(MHz)。                     |
| **networks** (_integer)_    | 通道上检测到的接入点数量。                  |
| **load** (_integer_)        | 扫描期间通道繁忙的时间百分比。              |
| **nf** (_integer_)          | 通道的本底噪声(以dBm为单位)。               |
| **max-signal** (_integer_)  | 通道中检测到ap的最大信号强度(以dBm为单位)。 |
| **min-signal** (_integer_)  | 通道中检测到ap的最小信号强度(以dBm为单位)。 |
| **primary** (_boolean_) (P) | 通道被AP用作主(控制)通道                    |
| **secondary** (boolean) (S) | 通道被AP用作辅助(扩展)通道                  |

## 扫描命令

/interface wifiwave2 scan命令将扫描接入点并打印出它检测到的任何ap的信息。

scan命令的参数与frequency-scan命令相同。

**输出参数**


| 参数                       | 说明                                                         |
| -------------------------- | ------------------------------------------------------------ |
| **active** (_boolean_) (A) | 表示在过去30秒内收到了来自AP的信标。                         |
| **address** (_MAC_)        | AP的MAC地址(BSSID)                                           |
| **channel** (_string_)     | AP使用的控制信道频率，其支持的无线标准和控制/扩展信道布局。  |
| **security** (_string_)    | AP支持的认证方法                                             |
| **signal** (_integer_)     | AP信标信号强度(单位:dBm)。                                   |
| **ssid** (_string_)        | AP的扩展服务集标识符                                         |
| **sta-count** (_integer_)  | 与AP关联的客户端设备数量。仅当AP在其信标中包含此信息时可用。 |

## Sniffer

**命令参数**

| 参数                            | 说明                                                                                                     |
| ------------------------------- | -------------------------------------------------------------------------------------------------------- |
| **duration** (_time interval_)  | 在指定时间过后自动中断嗅探器。无默认值。                                                                 |
| **number** (_interface_)        | 用于嗅探的接口。                                                                                         |
| **pcap-file** (_string_)        | 将捕获的帧保存到给定名称的文件中。无默认值(默认情况下捕获的帧不保存到文件中)。                           |
| **pcap-size-limit** (_integer_) | 本地存储捕获帧时的文件大小限制(以字节为单位)。<br>当达到这个限制时，不会向捕获文件添加新的帧。无默认值。 |
| **Stream-address** (IP地址)     | 通过TZSP协议将捕获的数据包流到给定的地址。无默认值(默认情况下捕获的数据包不会流到任何地方)。             |
| **stream-rate** (_integer_)     | 捕获的帧通过TZSP流传输的速率限制(以每秒数据包为单位)。                                                   |

## WPS

interface/wifiwave2/wps-client wifi

**命令参数**

| 参数                           | 说明                                               |
| ------------------------------ | -------------------------------------------------- |
| **duration** (_time interval_) | 如果未找到AP，则命令超时的时间长度。默认为无限制。 |
| **interval** (_time interval_) | 更新命令输出的时间间隔。默认值:1 s。               |
| **MAC-address** (_MAC_)        | 只尝试使用指定的MAC (BSSID)连接AP。没有默认值。    |
| **numbers** (_string_)         | 要尝试连接的接口的名称或内部id。没有默认值。       |
| **ssid** (_string_)            | 只尝试连接指定ssid的ap。没有默认值。               |

## 无线电

通过运行 /interface/wifiwave2/radio print detail 命令可以获得有关每个无线电功能的信息。

| 属性                                   | 说明                                                |
| -------------------------------------- | --------------------------------------------------- |
| **2g-channels** (_list of_ _integers_) | 支持2.4GHz频段的频率。                              |
| **5g-channels** (_list of integers_)   | 5GHz频段支持的频率。                                |
| **bands** (_list of strings_)          | 支持的频带、无线标准和信道宽度。                    |
| **ciphers** (_list of strings_)        | 支持的加密密码。                                    |
| **countries** (_list of strings_)      | 接口支持的监管域。                                  |
| **min-antenna-gain** (_integer_)       | 接口允许的最小天线增益。                            |
| **phy-id** (_string_)                  | 唯一标识符。                                        |
| **radio-MAC** (_MAC_)                  | 无线接口的MAC地址。可用于将无线电与接口配置相匹配。 |
| **rx-chains** (_list of integers_)     | 用于接收无线电信号的无线电id。                      |
| **tx-chains** (_list of integers_)     | 用于传输无线电信号的无线电id。                      |

## 注册表

注册表包含了关联无线设备的只读信息。

| 参数                             | 说明                                     |
| -------------------------------- | ---------------------------------------- |
| **authorized** (_boolean_) (A)   | 当对等体身份验证成功时为True。           |
| **bytes** (_list of integers_)   | 向对等体发送和从对等体接收的报文字节数。 |
| **interface** (_string_)         | 关联对等体时使用的接口名。               |
| **MAC-address** (_MAC_)          | 对端MAC地址。                            |
| **packets** (_list of integers_) | 向对等体发送和从对等体接收的数据包数。   |
| **rx-rate** _(string)_           | 接收到的对端传输的比特率。               |
| **signal** (_integer)_           | 接收到的对端信号强度(以dBm为单位)。      |
| **tx-rate** (_string)_           | 传输到对端使用的比特率。                 |
| **uptime** (_time interval)_     | 关联后的时间。                           |

## CAPsMAN全局配置

**Menu:** `/interface/wifiwave2/capsman`

| 参数                                                                                         | 说明                                                                                                                                                                                                                                      |
| -------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **ca-certificate** _(auto_ \| _certificate name_ )                                           | 设备CA证书，CAPsMAN服务器需要证书，CAP上的证书是可选的。                                                                                                                                                                                  |
| **certificate** (_auto \|certificate name\| none_;Default:**none**)                          | 设备证书                                                                                                                                                                                                                                  |
| **enabled** _(no_ \| _yes_)                                                                  | 禁用或启用CAPsMAN功能                                                                                                                                                                                                                     |
| **package-path** (_string \|_;Default:)                                                      | RouterOS包的文件夹位置。例如，使用"/upgrade"从files部分指定升级文件夹。如果设置为空字符串，则CAPsMAN可以使用内置的RouterOS包，注意在这种情况下，只有与CAPsMAN架构相同的cap才会升级。                                                      |
| **require-peer-certificate** (_yes \| no_;Default:**no**)                                    | 要求所有连接的CAPs具有有效的证书                                                                                                                                                                                                          |
| **upgrade-policy** (_none \| require-same-version \| suggest-same-upgrade_;Default:**none**) | 升级策略选项<br>- none -不升级<br>- require-same-version - CAPsMAN建议升级CAP的RouterOS版本，如果升级失败，则不会发放CAP。(手动发放仍然是可能的)<br>- suggest-same-version - CAPsMAN建议升级CAP的RouterOS版本，如果升级失败，仍会继续发放 |
| **interfaces** _(all \| interface name \| none;Default:**all**)_                             | CAPsMAN将监听CAP连接的接口                                                                                                                                                                                                                |

## CAPsMAN Provisioning

匹配无线电的发放规则在/interface/wifiwave2/Provisioning /菜单中配置:

| 参数                                                                                                   | 说明                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **action** (_create-disabled \| create-enabled \| create-dynamic-enabled \| none_; Default: **none**)  | 如果规则匹配由以下设置指定，则采取的操作:<br>- **create-disabled** -创建禁用的无线静态接口。即，接口将被绑定到无线电，但无线电将不会运行，直到手动启用接口;<br>- **create-enabled** -创建已启用的静态接口。也就是说，接口将被绑定到无线电，无线电将是可操作的;<br>- **create-dynamic-enabled** -创建启用的动态接口。也就是说，接口将被绑定到无线电，无线电将是可操作的;<br>- **none** -什么都不做，使无线电处于未提供状态; |
| **comment** (_string_; Default: )                                                                      | 发放规则的简要说明                                                                                                                                                                                                                                                                                                                                                                                                         |
| **common-name-regexp** (_string_;Default:)                                                             | 通过通用名称匹配无线电的正则表达式。每个CAP的通用名称标识符可以在“/interface/wifiwave2/radio”下找到，值为“REMOTE-CAP-NAME”                                                                                                                                                                                                                                                                                                 |
| **supported-bands** (_2ghz-ax \| 2ghz-g \| 2ghz-n \| 5ghz-a \| 5ghz-ac \| 5ghz-ax \| 5ghz-n_;Default:) | 按支持的无线模式匹配无线电                                                                                                                                                                                                                                                                                                                                                                                                 |
| **identity-regexp** (_string_;Default:)                                                                | 根据路由器标识匹配无线电的正则表达式                                                                                                                                                                                                                                                                                                                                                                                       |
| **address-ranges** (_IpAddressRange[，IpAddressRanges] max 100x_;Default:**""**)                       | 在配置的地址范围内匹配CAPs和ip。                                                                                                                                                                                                                                                                                                                                                                                           |
| **master-configuration** (_string_;Default:)                                                           | 如果action指定创建接口，则将创建一个新的主接口，其配置设置为此配置文件                                                                                                                                                                                                                                                                                                                                                     |
| **name-format** (_cap \| identity_ ; Default: **cap**)                                                 | 指定创建CAP接口名称的语法<br>-“example1-**%I**”- cap标识<br>- “example2-**%C**” - cap通用名称                                                                                                                                                                                                                                                                                                                              |
| **name-prefix** (_string_; Default: )                                                                  | 名称前缀，可以在名称格式中使用，用于创建CAP接口名称                                                                                                                                                                                                                                                                                                                                                                        |
| **radio-mac** (_MAC address_;Default:**00:00:00:00:00**)                                               | 要匹配的无线电MAC地址，空MAC(00:00:00:00:00)表示匹配所有MAC地址                                                                                                                                                                                                                                                                                                                                                            |
| **slave-configurations** (_string_;Default:)                                                           | 如果**action**指定创建接口，则为此列表中的每个配置文件创建一个新的从接口。                                                                                                                                                                                                                                                                                                                                                 |
| **disabled** (_yes_ \| no_;Default:**no**)                                                             | 是否禁用provision规则。                                                                                                                                                                                                                                                                                                                                                                                                    |

## CAP配置

**Menu:** `/interface/wifiwave2/cap`

| 参数                                                                | 说明                                                                            |
| ------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| **caps-man-addresses** _(list of IP addresses; Default: **empty**)_ | 在发现过程中CAP将尝试联系的管理器IP地址列表                                     |
| **CAPs-man-names** ()                                               | CAPs将连接到的CAPs管理器名称的有序列表，如果为空- CAP不检查管理器名称           |
| **discovery-interfaces** (_list of interfaces_; )                   | CAP尝试发现Manager的接口列表                                                    |
| **lock-to-caps-man** (_no_ \| _yes;_ Default:**no**)                | 设置，如果CAP应该锁定它连接到的第一个CAPsMAN                                    |
| **slave -static** ()                                                |                                                                                 |
| **caps-man-certificate-common-names** ()                            | CAP将连接到的管理器证书CommonNames列表，如果为空- CAP不检查管理器证书CommonName |
| **certificate**()                                                   | 用于认证的证书                                                                  |
| **enabled** (_yes \| no_;Default:**no**)                            | 禁用或启用CAP功能                                                               |
| **slaves-datapath** ()                                              |                                                                                 |