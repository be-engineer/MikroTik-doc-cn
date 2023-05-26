# 互联工作

互联工作是指两个或多个事物一起工作的现象。为了获得更好的无线网络体验，必须在接入点和无线客户端设备之间交换有关网络的信息，可以在基本无线信标和探测请求中找到的信息是有限的。因此，IEEE 802.11u™-2011(与外部网络的交互)标准被创建，该标准规定了设备之间应该如何交换信息。该互联服务可以增强网络发现和接入点选择过程。无线客户机设备可以有更多的标准来选择要关联的网络。

# 热点2.0

Hotspot 2.0是由Wi-Fi联盟开发和拥有的规范。它的设计目的是在连接Wi-Fi网络时提供更像蜂窝的体验。为了提高无线网络的安全性，Hotspot 2.0接入点使用强制的WPA2认证。Hotspot 2.0依赖于互操作，并添加了一些自己的属性和过程。


对接配置文件根据IEEE 802.11u和Hotspot 2.0 Release 1规范实现。

本手册页面描述了常规无线包的配置，WifiWave2包中也有相同的参数。

# 配置属性

**Sub-menu:** `/interface wireless interworking-profiles`

## 信标和探测响应中的信息元素

一些信息可以添加到信标和探测响应数据包与一个互操作元素。对接元素可配置的参数如下:

| 属性                                                                                                                                                               | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **asra** (_yes\| no_; Default: **no**)                                                                                                                             | 访问所需的其他步骤。设置为“是”，如果用户需要采取额外的步骤来访问互联网，如围墙花园。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| **esr** (_yes \| no_;Default:**no**)                                                                                                                               | 紧急服务可达(ESR)。设置为“是”，以指示可通过接入点访问紧急服务。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **hessid** (_MAC地址_;Default:)                                                                                                                                    | 同构扩展服务集标识符(HESSID)。提供对相同外部网络访问的设备位于一个同构扩展服务集中。该服务集可以由HESSID标识，它在该集的所有接入点上都是相同的。HESSID的6字节值表示为MAC地址。全局唯一，建议使用服务集中接入点的MAC地址之一。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| **internet** (_yes\| no_; Default: **yes**)                                                                                                                        | 通过这种连接是否可以使用互联网。该信息包含在Interworking元素中。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **network-type** (_emergency-only) \|personal-device \| private \| private-with-guest \| public-charge \| public-free \| test \| wildcard_;(Default: **wildcard**) | 网络接入类型信息。 <br>- "emergency-only"——专门用于获取紧急服务的网络;<br>- "personal-device"——个人设备网络。这种类型的网络的一个例子是连接到打印机的相机，从而形成用于打印图片的网络;<br>- "private" -为拥有用户帐户的用户提供的网络。通常在企业中用于员工，而非客人;<br>- "private-with-guest" -与private相同，但可以使用guest帐户;<br>-“public-chargeable”-任何愿意付费的人都可以使用的网络。例如，订阅Hotspot 2.0服务或在酒店房间内上网;<br>-“public-free”-任何人都可以免费使用网络。例如，城市或机场的市政网络热点;<br>- test -用于测试和实验用途的网络。不用于生产的;<br>- 'wildcard' -用于无线客户端。发送带有通配符作为网络类型值的探测请求将使所有互连接入点响应，尽管它们的实际网络类型设置。<br>客户端发送一个探测请求帧，将网络类型设置为它感兴趣的值。它将只从具有相同值的接入点接收应答(通配符的情况除外)。 |
| **usa** (_yes \| no_;Default:**no**)                                                                                                                               | 未经身份验证的紧急服务可访问(UESA)。<br>- "no" -表示无法通过该接入点访问未经身份验证的紧急服务;<br>- "yes"-表示可通过此接入点访问更高层未经身份验证的紧急服务。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **venue** (_venue_; Default: **unspecified**)                                                                                                                      | 指定接入点所在的场地。从可用值中选择值。一些例子:<pre><br>venue=business-bank<br>venue=mercantile-shopping-mall<br>venue=educational-university-or-college                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| </pre>                                                                                                                                                             |

## ANQP元素

接入网络查询协议(ANQP)。并非所有必要的信息都包含在探测响应和信标帧中。为了使客户端设备在选择接入点与ANQP相关联之前获得更多的信息。接入点可以在多个ANQP元素中存储信息。客户端设备将使用ANQP只查询它感兴趣的信息。这减少了联想之前所需的时间。

| 属性                                                                                                                                                                                                       | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **3gpp-raw** (_octet string in hex_; Default: )                                                                                                                                                            | 蜂窝网络通告信息-国家和网络代码。这有助于Hotspot 2.0客户端选择接入3GPP网络的接入点。请参阅3GPP TS 24.302。(附件H)的格式。查询时发送ANQP响应。                                                                                                                                                                                                                                                                                                                                                                                                                |
| **3gpp-info** (_number/number_; Default: )                                                                                                                                                                 | 蜂窝网络通告信息-国家和网络代码。这有助于Hotspot 2.0客户端选择接入3GPP网络的接入点。写为“mcc/mnc”。用法与“3gpp-raw”相同，但不使用十六进制。可以定义多个mcc/mnc对，用逗号分隔。                                                                                                                                                                                                                                                                                                                                                                               |
| **authentication-types** (_dns-redirection:`url` \| https-redirection:`url`\| online-enrollment:`url` \| terms-and-conditions:`url`_; Default: )                                                           | 此属性仅在asra设置为“yes”时有效。如果选择了“dns-重定向”或“在线注册”，url的值是可选的，不需要。要设置' url '的值为空字符串，请使用双引号。例如:<br><pre>authentication-types=online-enrollment:""</pre>                                                                                                                                                                                                                                                                                                                                                       |
| **connection-capabilities** (_number:number:closed \| open \| unknown_; Default: )                                                                                                                         | 此选项允许提供有关允许的IP协议和端口的信息。这些信息可以在ANQP响应中提供。第一个数字表示IP协议号，第二个数字表示端口号。<br>- ' closed ' -如果不允许协议和端口组合设置;<br>- ' open ' -设置是否允许协议和端口组合;<br>- ' unknown ' -设置协议和端口组合是打开还是关闭。<br>例子:<br><pre>connection-capabilities=6:80:open,17:5060:closed</pre><br>在接入点上设置这样的值通知连接到接入点的无线客户端，允许HTTP (6 - TCP, 80 - HTTP)和VoIP (17 - UDP;5060 (VoIP)是不允许的。<br>此属性不限制或允许使用这些协议和端口，它仅向连接到接入点的站点设备提供信息。 |
| **domain-names** (_list of strings_; Default: )                                                                                                                                                            | 无或多个FQDN (fully qualified domain names)，用于标识运行热点的实体。连接到接入点的站点可以请求此AQNP属性，并检查是否有一个后缀与其拥有凭据的任何域名相匹配。                                                                                                                                                                                                                                                                                                                                                                                                |
| **ipv4-availability** (_double-nated \| not-available\| port-restricted \| port-restricted-double-nated \| port-restricted-single-nated \| public \| single-nated \| unknown_; Default: **not-available**) | 关于可用的IPv4地址和访问的信息。<br>- ' not-available ' -地址类型不可用;<br>- ' public ' -公共IPv4地址可用;<br>- ' port-restricted ' -端口限制的IPv4地址可用;<br>- ' single- NATed ' -单个NATed私有IPv4地址可用;<br>- ' double- NATed ' -双NATed私有IPv4地址可用;<br>- ' port-restricted-single-nated ' -port-restricted IPv4地址和single- NATed IPv4地址可用;<br>- ' port-restricted-double- NATed ' - port-restricted IPv4地址和double- NATed IPv4地址可用;<br>- ' unknown ' -地址类型的可用性未知。                                                       |
| **ipv6-availability** (_available \| not-available \| unknown_; Default: **not-available**)                                                                                                                | 关于可用的IPv6地址和访问的信息。<br>- ' not-available ' -地址类型不可用;<br>- ' available ' -可用的地址类型;<br>- ' unknown ' -地址类型的可用性未知。                                                                                                                                                                                                                                                                                                                                                                                                        |
| **realms** (_string:eap-sim\|eap-aka\|eap-tls\|not-specified_; Default: )                                                                                                                                  | 有关支持的领域和相应EAP方法的信息。<br><pre>realms=example.com:eap-tls,foo.ba:not-specified</pre>                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| **realms-raw** (_octet string in hex_; Default: )                                                                                                                                                          | 手动设置NAI Realm anqp元素。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| **roaming-ois** (_octet string in hex_; Default: )                                                                                                                                                         | 组织标识符(OI)通常是24位的唯一标识符，如组织唯一标识符(OUI)或公司标识符(CID)。在某些情况下，OI更长，例如OUI-36。<br>订阅服务提供者(SSP)可以由其OI指定。routing - OIs属性可以包含0个或多个ssp OI，这些ssp的网络可以通过该AP访问。OI的长度应该在OI本身之前指定。例如，设置E4-8D-8C和6C-3B-6B:<br><pre>roam -ois=03E48D8C036C3B6B</pre>                                                                                                                                                                                                                         |
| **venue-names** (_string:lang_; Default: )                                                                                                                                                                 | 场地名称可用于提供有关场地的其他信息。它可以帮助客户端选择合适的接入点。<br>参数由零个或多个包含场馆名称和语言代码的双元组组成:<br><pre>venue-names=CoffeeShop:eng,TiendaDeCafe:es</pre><br>语言代码字段值是从ISO-639中选择的两个或三个字符的8个语言代码。                                                                                                                                                                                                                                                                                                   |

### Realms raw

**realms-raw** -十六进制值的字符串列表。每个字符串指定“NAI Realm Tuple”的内容，不包括“NAI Realm Data Field Length”字段。

每个十六进制编码字符串必须包含以下字段:

```
- NAI Realm Encoding (1 byte)
- NAI Realm Length (1 byte)
- NAI Realm (variable)
- EAP Method Count (1 byte)
- EAP Method Tuples (variable)

```

例如，值“00045465737401020d00”解码为:

```
- NAI Realm Encoding: 0 (rfc4282)
- NAI Realm Length: 4
- NAI Realm: Test
- EAP Method Count: 1
- EAP Method Length: 2
- EAP Method Tuple: TLS, no EAP method parameters

```

注意，设置“realms-raw=00045465737401020d00”会产生与设置“realms=Test:eap-tls”相同的通告内容。

有关完整的NAI Realm编码，请参阅802.11-2016，第9.4.5.10节。

## 热点2.0 ANQP元素

Hotspot 2.0规范引入了一些额外的ANQP元素。这些元素使用ANQP供应商特定的元素ID。以下是可用于更改这些元素的属性。

| 属性                                                                     | 说明                                                                                                                                                                                                                                                              |
| ------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **hotspot20** (_yes\| no_; Default: **yes**)                             | 表示接入点的Hotspot 2.0能力。                                                                                                                                                                                                                                     |
| **hotspot20-dgaf** (_yes \| no_; Default: **yes**)                       | 下游组寻址转发(DGAF)。设置DGAF位的值，以指示向客户端发送的组播和广播帧是禁用还是启用。<br>- ' yes ' -向客户端启用组播和广播帧<br>- ' no ' -禁止向客户端发送组播和广播帧。<br>要禁用多播和广播帧，请设置“multicast-helper=full”。                                  |
| **operational-classes** (_list of numbers_; Default: )                   | 同一ESS的其他可用频带信息。                                                                                                                                                                                                                                       |
| **operator-names** (_string:lang_; Default: )                            | 设置操作符名称。必须为每个操作符名称条目指定语言。<br>Operator-names形参由0个或多个包含Operator Name和Language Code的双元组组成:<br><pre>operator-names=BestOperator:eng,MejorOperador:es</pre><br>语言代码字段值是从ISO-639中选择的两个或三个字符的8个语言代码。 |
| **wan-at-capacity** (_yes \| no_; Default: **no**)                       | 接入点或网络是否处于最大容量。如果设置为“是”，则不允许其他移动设备与AP关联                                                                                                                                                                                        |
| **wan-downlink** (_number_;Default:**0**)                                | 广域网连接的下行速度，单位为kbps。如果下行速率未知，则设置为0。                                                                                                                                                                                                   |
| **wan-downlink-load** (_number_; Default: **0**)                         | 在“WAN -measurement-duration”期间测量的WAN连接的下行链路负载。取值范围为0 ~ 255。<br>-   `0` - unknown;<br>-   `255` - 100%.                                                                                                                                      |
| **wan-measurement-duration** (_number_; Default: **0**)                  | 测量wan-下行链路负载和wan-上行链路负载的持续时间。Value为数字，取值范围为0 ~ 65535，代表十分之一秒。<br>-   `0` - 未测量;<br>-   `10` - 1秒;<br>-   `65535` - 1小时49分或更多.                                                                                    |
| **wan-status** (_down \| reserved \| test \| up_; Default: **reserved**) | 有关接入点WAN连接状态的信息。没有使用“reserved”值。                                                                                                                                                                                                               |
| **wan-symmetric** (_yes \| no_;Default:**no**)                           | 广域网链路是否对称(上传和下载速度相同)。                                                                                                                                                                                                                          |
| **wan-uplink** (_number_;Default:**0**)                                  | 广域网连接上行速率，单位为kbps。如果上行链路速率未知，则设置为0。                                                                                                                                                                                                 |
| **wan-uplink-load** (_number_; Default: **0**)                           | WAN -measurement-duration内测量的WAN连接上行链路负载。取值范围为0 ~ 255。<br>-   `0` - unknown;<br>-   `255` - 100%.                                                                                                                                              |

## 其他属性

| 属性                            | 说明                 |
| ------------------------------- | -------------------- |
| **comment** (_string_;Default:) | 配置文件的简短描述   |
| **name** (_string_;Default:)    | 对接配置文件的名称。 |

使用本地RadSec和Orion Wifi的配置指南:

本指南描述了如何设置您的MikroTik设备，以便您可以与RadSec代理和Orion Wifi一起使用它们，尽管主要配置步骤保持不变，并且可以与不同的提供商一起工作:
确保使用最新的长期或稳定的RouterOS版本。

在无线局域网控制器和Orion Wifi之间建立一个安全的RADIUS连接是很重要的。
Orion Wifi采用RADIUS over TLS (RadSec)技术，保证AAA流量的端到端加密。

1) 导入从Orion下载的RadSec证书:

在WinBox中拖放证书，然后使用导入功能对其进行导入，该功能可以在WinBox的/system certificates下找到，命令行相当于:"/certificate import file-name=bw.radsec.cacert. "Pem passphrase="""， "/certificate import file-name=cert. PemPem passphrase="""， "/certificate import file-name=key. Pem passphrase= " "

![](https://help.mikrotik.com/docs/download/attachments/7962628/radsecCert.png?version=1&modificationDate=1624954284764&api=v2)

![](https://help.mikrotik.com/docs/download/attachments/7962628/radsec_cert1.png?version=1&modificationDate=1626168620468&api=v2)

![](https://help.mikrotik.com/docs/download/attachments/7962628/radsec_key.png?version=1&modificationDate=1626168193158&api=v2)

证书导入后应该是这样的:

![](https://help.mikrotik.com/docs/download/attachments/7962628/radsec_endresult.png?version=1&modificationDate=1626168225808&api=v2)

2) 配置Radius客户端

![](https://help.mikrotik.com/docs/download/attachments/7962628/radsec.png?version=1&modificationDate=1628589240137&api=v2)

命令行等效:"/radius add address=216.239.32.91 certificate=cert. pem_0 protocol=radsec service=wireless timeout=1s500ms "

3) 创建执行802.1x认证的无线安全配置文件

![](https://help.mikrotik.com/docs/download/attachments/7962628/image2021-5-19_15-50-58.png?version=1&modificationDate=1621428658412&api=v2)

![](https://help.mikrotik.com/docs/download/attachments/7962628/image2021-5-19_15-53-40.png?version=1&modificationDate=1621428820578&api=v2)

![](https://help.mikrotik.com/docs/download/attachments/7962628/image2021-5-19_15-54-46.png?version=1&modificationDate=1621428886421&api=v2)

命令行相当于 "/interface wireless security-profiles add authentication-types=wpa2-eap management-protection=allowed mode=dynamic-keys name=dot1x_profile supplicagent -identity="" radius-eap-accounting=yes eap-methods=passthrough"。

4) 下一步是配置无线接口，并分配创建的安全配置文件。按“高级模式”查看所有选项。

![](https://help.mikrotik.com/docs/download/attachments/7962628/image2021-5-19_16-11-18.png?version=1&modificationDate=1621429878808&api=v2)

命令行相当于:“/interface wireless set [find default-name=wlan1] mode=ap-bridge security-profile=dot1x_profile wps-mode=disabled”。

确保配置了正确的国家配置文件。在这个例子中，我们使用的是" wlan1 "，但是同样的命令也可以用于其他接口，或者使用" /interface wireless set wlan1 "。

5) 配置对接设置(热点2.0)。

![](https://help.mikrotik.com/docs/download/attachments/7962628/creating_iw_profile.png?version=2&modificationDate=1626170039913&api=v2)

![](https://help.mikrotik.com/docs/download/attachments/7962628/ANQP.png?version=2&modificationDate=1628065144346&api=v2)

![](https://help.mikrotik.com/docs/download/attachments/7962628/hs2.png?version=2&modificationDate=1628066327616&api=v2)

命令行相当于:/interface wireless interworking-profile add domain-names=[orion.area120.com](http://orion.area120.com) ipv4-availability=public name=Orion_MikroTik network-type=public-chargeable operator-names=Orion:eng realms=[orion.area120.com](http://orion.area120.com):eap-tls roaming-ois=f4f5e8f5f4,baa2D00100,baa2d00000 venue=business-unspecified venue-names=Orion:eng wan-downlink=50 wan-uplink=50 wan-status=up”

特别注意“wan-downlink”和“wan-uplink”，在这种情况下，“50”的值被用作占位符，请确保根据您的设置调整值，一些客户端设备使用它来评估是否应该加入网络。设置“场地”-场地类型，“场地名称”和其他适用的属性。“domain-names”应该是热点2.0操作符。

6) 为接口配置对接配置文件。

![](https://help.mikrotik.com/docs/download/attachments/7962628/interworking_wireless_int.png?version=2&modificationDate=1626170014924&api=v2)

命令行相当于:" /interface wireless set wlan1 interworking-profile=Orion_MikroTik "。如果没有看到交互配置文件字段，请按“高级模式”。

注意:Orion用于区分网络的NAS-id等于系统标识，可以执行“/system identity set name=exampleName”命令调整NAS-id。从6.47.10和6.48.3以上的版本中添加了对互联配置文件的图形界面支持。

使用RadSec代理和Orion Wifi的配置指南:

本指南描述了如何设置您的MikroTik设备，以便您可以与RadSec代理和Orion Wifi一起使用它们，尽管主要配置步骤保持不变，并且可以与不同的提供商一起工作:
本指南假设您已经配置了具有Orion Wifi凭据的radsecproxy。确保使用最新的长期或稳定的RouterOS版本。

在无线局域网控制器和Orion Wifi之间建立一个安全的RADIUS连接是很重要的。
Orion Wifi采用RADIUS over TLS (RadSec)技术，保证AAA流量的端到端加密。本指南适用于以下场景:在AAA流量通过internet发送之前，RouterOS接入点将AAA流量重定向到RadSec代理(radsecproxy)。
1) 配置指向radsecproxy的Radius客户端。

![](https://help.mikrotik.com/docs/download/attachments/7962628/radproxy.png?version=1&modificationDate=1628587191157&api=v2)

命令行相当于"/radius add address=192.168.88.233 secret=yourSecret service=wireless timeout= 1500ms"

该密钥应该与radsecproxy上配置的密钥匹配，在本例中，“192.168.88.233”是运行该代理的虚拟机。

2) 创建执行802.1x认证的无线安全配置文件

![](https://help.mikrotik.com/docs/download/attachments/7962628/image2021-5-19_15-50-58.png?version=1&modificationDate=1621428658412&api=v2)

![](https://help.mikrotik.com/docs/download/attachments/7962628/image2021-5-19_15-53-40.png?version=1&modificationDate=1621428820578&api=v2)

![](https://help.mikrotik.com/docs/download/attachments/7962628/image2021-5-19_15-54-46.png?version=1&modificationDate=1621428886421&api=v2)

  

命令行相当于"/interface wireless security-profiles add authentication-types=wpa2-eap management-protection=allowed mode=dynamic-keys name=dot1x_profile supplicant-identity="" radius-eap-accounting=yes eap-methods=passthrough "。

3) 下一步是配置无线接口，并分配创建的安全配置文件。按“高级模式”查看所有选项。

![](https://help.mikrotik.com/docs/download/attachments/7962628/image2021-5-19_16-11-18.png?version=1&modificationDate=1621429878808&api=v2)

命令行相当于:"/interface wireless set [find default-name=wlan1] mode=ap-bridge security-profile=dot1x_profile wps-mode=disabled"。

确保配置了正确的国家配置文件。在这个例子中用的是" wlan1 "，但是同样的命令也可以用于其他接口，或者使用" /interface wireless set wlan1 "。

4) 配置对接设置(热点2.0)。

![](https://help.mikrotik.com/docs/download/attachments/7962628/creating_iw_profile.png?version=2&modificationDate=1626170039913&api=v2)

![](https://help.mikrotik.com/docs/download/attachments/7962628/ANQP%20%281%29.png?version=1&modificationDate=1628066313271&api=v2)

![](https://help.mikrotik.com/docs/download/attachments/7962628/hs2.png?version=2&modificationDate=1628066327616&api=v2)

命令行相当于:“/interface wireless internetworking -profile add domain-names=[orion.area120.com](http://orion.area120.com) ipv4-availability=public name=Orion_MikroTik network-type=public-chargeable carrier -names=Orion:eng realms=[orion.area120.com](http://orion.area120.com):eap-tls roaming-ois=f4f5e8f5f4,baa2D00100,baa2d00000 venue=业务未指定的venue-names=Orion:eng wan-downlink=50 wan-uplink=50 wan-status=up”。

一定要在“wan-downlink”和“wan-uplink”中指定一些值，在这种情况下，“50”的值被用作占位符，一些客户端设备使用它来评估是否应该加入网络。设置“场地”-场地类型，“场地名称”和其他适用的属性。“domain-names”应该是热点2.0操作符。

5) 为接口配置对接配置文件。

![](https://help.mikrotik.com/docs/download/attachments/7962628/interworking_wireless_int.png?version=2&modificationDate=1626170014924&api=v2)

此步骤也可以通过以下命令完成:" /interface wireless set wlan1 interworking-profile=Orion_MikroTik "。

如果radsecproxy正常工作，那么安装了适当Hotspot配置文件的客户机应该能够连接。

注意:Orion用于区分网络的NAS-id等于系统标识，可以执行“/system identity set name=exampleName”命令调整NAS-id。从6.47.10、6.48.3以上的版本中增加了对互联配置文件的图形界面支持。

# 故障排除

可以通过RADIUS菜单查看RADIUS消息的状态。
![](https://help.mikrotik.com/docs/download/attachments/7962628/rad_stat.png?version=1&modificationDate=1628585948146&api=v2)  
或者通过命令行运行“/radius monitor X”，X是数字ID，可以看到带有“/radius print”的ID。
要了解更多信息，可以在“/system logging add topics=radius,debug,packet”下配置额外的日志记录。可以在 [/log](https://help.mikrotik.com/docs/display/ROS/Log) 下查看结果。

要查看活动的无线连接，请检查无线注册表(/interface wireless registration-table print)

![](https://help.mikrotik.com/docs/download/attachments/7962628/wireless_registration.png?version=1&modificationDate=1628586992199&api=v2)