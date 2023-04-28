# 使用 MQTT 和 ThingsBoard 进行蓝牙标签跟踪

RouterOS中的蓝牙接口实现允许设备捕获通过37、38和39个广播通道广播的蓝牙广播数据包。更多信息可以在 [指南](https://help.mikrotik.com/docs/display/ROS/Bluetooth) 中找到。

蓝牙标签，例如，[TG-BT5-IN](https://mikrotik.com/product/tg_bt5_in) 和 [TG-BT5-OUT](https://mikrotik.com/product/tg_bt5_out)，正是这样做 的。在上述频道上广播有效载荷。要了解有效载荷中存储了什么样的信息，请查看 [链接](https://help.mikrotik.com/docs/display/UM/MikroTik+Tag+advertisement+formats#heading-MikroTikPDUPayloadstructure)。可以对标签进行配置（使用 [MikroTik信标管理器](https://help.mikrotik.com/docs/display/UM/MikroTik+Beacon+Manager) 应用），以便在检测到移动、倾斜或自由落体触发时，以一定的时间间隔自动广播有效载荷。简单地说，标签将定期 "告诉"（广播到）周围所有的蓝牙扫描器（如 [KNOT](https://mikrotik.com/product/knot)）关于自己的信息。

当有效载荷被标签广播，并且标签在KNOT的蓝牙范围内时，KNOT将捕获并在其 "扫描者 "蓝牙接口部分显示有效载荷。看起来像这样：

```shell

/iot bluetooth scanners advertisements print
Columns: DEVICE, PDU-TYPE, TIME, ADDRESS-TYPE, ADDRESS, RSSI, LENGTH, DATA
#  DEVICE  PDU-TYPE        TIME                  ADDRESS-TYPE  ADDRESS            RSSI    LENGTH  DATA                                       
0  bt1     adv-noconn-ind  mar/07/2023 12:11:57  public        DC:2C:6E:0F:C0:3D  -51dBm      22  15ff4f09010079100000ffff0000cf188a6b2b000064
1  bt1     adv-noconn-ind  mar/07/2023 12:11:58  public        2C:C8:1B:4B:BB:0A  -49dBm      22  15ff4f090100168dfefffffffeffa51ae1362200005e
```

上面的例子显示，KNOT在其工作范围内看到两个蓝牙标签，MAC地址分别为 "DC:2C:6E:0F:C0:3D "和 "2C:C8:1B:4B:BB:0A"，它们各自的有效载荷（"数据 "字段）和信号强度（"RSSI "字段）。

在本地测试KNOT可以处理多少有效载荷时，取得了如下结果：300个标签（出厂设置），分散在KNOT周围，使用蓝牙过滤器 "keep-newest"（用最新的MAC地址覆盖以前收到的有效载荷，这样蓝牙列表在任何时候都会显示每个标签MAC地址的1个有效载荷），所有300个MAC地址在30-40秒后出现在KNOT的范围。这时需要记住，所有300个标签同时在同一频道上广播会造成干扰（接收延迟）。当我们 "清除 "蓝牙有效载荷列表时，每一秒列表都有20个新条目，大约15秒后，列表中有250-290个有效载荷。然后又过了大约15秒，列表中显示了所有300个独特的标签有效载荷。**KNOT能够处理的标签的实际数量在很大程度上取决于环境，所以最好在现场进行测试**。

在RouterOS [scripting](https://help.mikrotik.com/docs/display/ROS/Scripting) 和 [scheduling](https://help.mikrotik.com/docs/display/ROS/Scheduler) 的帮助下，可以使KNOT自动定期扫描有效载荷列表，如果在列表中发现特定的有效载荷或特定标签的MAC地址，我们可以使KNOT结构一个MQTT消息（从上面的例子中显示的打印信息）并通过 [MQTT](https://help.mikrotik.com/docs/display/ROS/MQTT) 、 [e-mail](https://help.mikrotik.com/docs/display/ROS/E-mail)  或 [HTTP](https://help.mikrotik.com/docs/display/ROS/Fetch) 邮寄给配置的服务器。脚本例子在本指南的后面显示。

如标题所示，目标是实现一个 **蓝牙标签跟踪解决方案**，想法很简单。**当你有两个KNOT** （KNOT-A和KNOT-B），在调度器上运行同一个脚本时， **标签在它们的蓝牙操作范围之间移动** ，**服务器上的数据将表明** 是KNOT-A还是KNOT-B **发送了** 标签的载荷。这将帮助弄清该标签的近况。标签是在KNOT-A区，还是在KNOT-B区广播有效载荷。

这需要一个服务器保存数据并被可视化。在本指南中，我们将展示一个名为 [ThingsBoard](https://thingsboard.io/) 的服务器以及如何使用MQTT协议与之通信。

ThingsBoard有一个云解决方案和不同的本地安装选项（在不同的操作系统上）。增加了 [容器](https://help.mikrotik.com/docs/display/ROS/Container) 功能后，也可以在RouterOS内运行该平台了。为了做到这一点，需要一个RouterOS设备， 最小至少有2GB内存或1GB内存， 并且可以增加存储（例如一个额外的USB端口），并且是ARM64或AMD64架构。考虑使用 [CHR](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=18350234) 机器可能是一个很好的选择。

## 设置要求:

- 一个正在运行的ThingsBoard服务器；
- 2 + [KNOT](https://mikrotik.com/product/knot)，通过以太网、Wi-Fi或手机连接进入服务器的网络（所需的单元数量取决于需要覆盖的区域大小）；
- 1+ 蓝牙  [TG-BT5-IN](https://mikrotik.com/product/tg_bt5_in) 和 [TG-BT5-OUT](https://mikrotik.com/product/tg_bt5_out) 标签（取决于你需要追踪的资产数量--每个资产一个标签）。

# 场景说明

先看一个基本的例子。有两个KNOTs（KNOT-A和KNOT-B）。已经在环境中测试了蓝牙范围，可以验证这两个KNOT能够在70米的距离内捕获标签。如果将KNOT-A和KNOT-B安装在相距140米的地方，它们的蓝牙范围将不会重叠或只是轻微重叠。当标签移动到KNOT-A范围内时→被监测的标签的有效载荷将出现在蓝牙扫描器列表下→脚本将按设定的时间表启动→带有报告的MQTT消息将被发送到服务器→最后，服务器将显示标签在KNOT-A区域内。当标签进入KNOT-B区域时，同样的情况发生，服务器将显示标签在KNOT-B区域内。

实际的蓝牙工作距离可能因场地而异，因为有很多因素会影响它，如2.4GHz干扰或周围使用的材料。例如，在视线范围内没有干扰的情况下，KNOT能够捕获标签的广播有效载荷的距离，可以达到180米（KNOT - ~180米 - TG-BT5-OUT）。但随着距离的增加，更多的数据包会在途中丢失。在办公室环境中，范围会下降到30-100米。

从逻辑上讲，如果蓝牙工作范围重叠，并且标签在重叠区域内（同时在KNOT-A和KNOT-B的蓝牙范围内），两个KNOT将发送数据，服务器将显示标签同时被两个设备报告。

**可能会有两个或多个KNOT的蓝牙范围重叠的区域，可以利用它的优点**。 你可以获得处于蓝牙范围的边缘，在特定的KNOT区域之间 的标签信息。换句话说，当资产移动到重叠区域时，将在服务器上得到资产处于两个KNOT操作范围之间的信息，这是很有用的，**因为它能提供更精确的信息**。

此外，标签的输出功率可以通过 [Tx power](https://help.mikrotik.com/docs/display/UM/MikroTik+Beacon+Manager+for+Android+devices#heading-TxPower) 参数来降低。这意味着，即使标签的有效载荷广播得太远，它们被其他不应该看到这些有效载荷的KNOT捕获（距离较远）→可以降低标签的输出功率，减少KNOT能够捕获它的距离。这样可以 "调整 "接收 "范围"，也可以避免 "干扰 "其他区域的信号。

我们准备的脚本允许设置一个过滤器（以后会显示），使KNOT忽略扫描者捕获的有效载荷，除非信号强度（RSSI）高于指定值。在上面的 [简介](https://help.mikrotik.com/docs/display/ROS/Bluetooth+tag-tracking+using+MQTT+and+ThingsBoard#BluetoothtagtrackingusingMQTTandThingsBoard-Introduction) 部分可以看到KNOT看到其中一个标签的 **RSSI** 信号强度为 **-51 dBm** （标签的MAC地址为 **DC： 2C:6E:0F:C0:3D**），另一个的 **RSSI** 信号强度为 **-49 dBm** （标签的MAC地址为 **2C:C8:1B:4B:BB:0A**）。因此，如果 **在脚本中应用一个过滤器来** 忽略 **所有收到的信号强度（RSSI）** 弱于-50 dBm的有效载荷，我们的 **KNOT将报告只有标签 "2C:C8:1B:4B:BB:0A "在蓝牙范围内，因为其RSSI为-49 dBm，而第二个标签（RSSI为-51 dBm）将被忽略。这意味着，它是 "调整 "接收 "范围 "的第二种方式。不同地点的实际信号强度会有所不同（如前所述，因为有干扰和周围的材料），所以需要现场测试。

## 实例1

其中一个用例显示在下面的拓扑结构中：

![](https://help.mikrotik.com/docs/download/attachments/176914435/image-2023-3-8_11-47-43.png?version=1&modificationDate=1678268845440&api=v2)

对象的规模和蓝牙工作范围只作为一个例子显示，帮助直观地理解和想象拓扑结构

有一个仓库区，**有3个资产** （托盘）要追踪。有3个区域：**A** 区新到的托盘存放在这里；**B** 区的资产被转移到这里接受检查；**C** 区资产在检查后被移动。为了实现蓝牙资产追踪，只需在每个区域安装1个KNOT，每个资产安装1个标签。

如果TAG 1和TAG 2（托盘）到达区域A，KNOT A将向服务器报告这两个资产都在其蓝牙范围内。如果TAG 3被移到C区，服务器将报告它在KNOT C的范围内。如果TAG 1和TAG 2向B区移动，并停留在A区和B区之间的边缘，服务器将显示它处于重叠区域（同时在KNOT-A和KNOT-B范围内）。如果标签向仓库中间移动，服务器将显示它们同时在3个区，在重叠区。

### 配置

在这个例子中将展示一个基本的拓扑结构，当使用两个KNOT时，只想知道标签是位于建筑物的一个部分还是另一个部分（是在A区还是B区）。

#### ThingsBoard准备

查看 [指南](https://help.mikrotik.com/docs/display/ROS/MQTT+and+ThingsBoard+configuration) 了解如何设置ThingsBoard和RouterOS以利用MQTT通信。

这个例子将展示 [access-token](https://help.mikrotik.com/docs/display/ROS/MQTT+and+ThingsBoard+configuration#MQTTandThingsBoardconfiguration-Accesstokenscenario.1) 方案，也可以使用其他可用选项。对于生产环境，建议使用SSL-MQTT，因为非SSL-MQTT很容易被抓包和检查。

要了解如何在 [容器](https://help.mikrotik.com/docs/display/ROS/Container) 运行的实例上实现SSL-MQTT通信。请查看 [这里](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=166920348) 的指南（[Enabling HTTPS and SSL MQTT](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=166920348#ContainerThingsBoardMQTT/HTTPserver-EnablingHTTPSandSSLMQTT) 部分）。

在ThingsBoard GUI下创建2个KNOTs，并 设为 "网关"。

进入 "设备 "部分，点击 "+"按钮和 "添加新设备"：

![](https://help.mikrotik.com/docs/download/attachments/176914435/image-2023-3-8_13-29-22.png?version=1&modificationDate=1678274944385&api=v2)

为设备命名，并勾选 "是否为网关 "选项：

![](https://help.mikrotik.com/docs/download/attachments/176914435/image-2023-3-8_13-31-35.png?version=1&modificationDate=1678275077067&api=v2)

对每个KNOT都这样做：

![](https://help.mikrotik.com/docs/download/attachments/176914435/image-2023-3-8_13-38-3.png?version=1&modificationDate=1678275465028&api=v2)

在 "管理证书"标签下，为刚刚创建的设备下的每个KNOT设置一个唯一的访问令牌（唯一的证书）：

![](https://help.mikrotik.com/docs/download/attachments/176914435/image-2023-3-8_13-47-8.png?version=1&modificationDate=1678276010748&api=v2)

#### RouterOS配置

##### 准备工作

在继续之前需要确认蓝牙标签确实出现在KNOT的蓝牙范围内，并且KNOT可以检测到它们。可以用 `/iot bluetooth scanners advertisements print` 命令来实现：

```shell

/iot bluetooth scanners advertisements print
 # DEVICE     PDU-TYPE        TIME                 ADDRESS-TYPE ADDRESS                    RSSI     LENGTH DATA                                          
 0 bt1        adv-noconn-ind  mar/08/2023 12:35:15 public       2C:C8:1B:4B:BB:0A        -50dBm         22 15ff4f090100b0110100ffff00000019d68d2300005d  
 1 bt1        adv-noconn-ind  mar/08/2023 12:35:16 public       DC:2C:6E:0F:C0:3D        -39dBm         22 15ff4f0901008f3cfcfffbfffaff301783c22c000064  
 2 bt1        adv-noconn-ind  mar/08/2023 12:35:35 public       2C:C8:1B:4B:BB:0A        -50dBm         22 15ff4f09010084d500000400ffff0319ea8d2300005d  
 3 bt1        adv-noconn-ind  mar/08/2023 12:35:45 public       2C:C8:1B:4B:BB:0A        -50dBm         22 15ff4f090100e607faffffff03000319f48d2300005d  
```

或者可以用 [Webfig](https://help.mikrotik.com/docs/display/ROS/Webfig) 或 [Winbox](https://help.mikrotik.com/docs/display/ROS/Winbox) 在物联网>蓝牙>广播报告标签下检查。

该列表可能是乱的。随机有效载荷可能会出现在列表中，因为扫描器会捕获周围的所有蓝牙设备。为了减少列表，可以使用标签的MAC地址 `/iot bluetooth scanners advertisements print where address=DC:2C:6E:0F:C0:3D` 来过滤：

```shell
/iot bluetooth scanners advertisements print where address=DC:2C:6E:0F:C0:3D
 # DEVICE    PDU-TYPE        TIME                 ADDRESS-TYPE ADDRESS                    RSSI     LENGTH DATA                                          
 0 bt1       adv-noconn-ind  mar/08/2023 12:41:06 public       DC:2C:6E:0F:C0:3D        -49dBm         22 15ff4f0901005ab20100fdfffdff4017e1c32c000064  
 1 bt1       adv-noconn-ind  mar/08/2023 12:41:26 public       DC:2C:6E:0F:C0:3D        -40dBm         22 15ff4f090100349704000000fcff4017f5c32c000064  
 2 bt1       adv-noconn-ind  mar/08/2023 12:41:36 public       DC:2C:6E:0F:C0:3D        -49dBm         22 15ff4f09010073fb0000000000003017ffc32c000064  
 3 bt1       adv-noconn-ind  mar/08/2023 12:41:46 public       DC:2C:6E:0F:C0:3D        -43dBm         22 15ff4f090100b88cffffffffffff401709c42c000064  
```

要弄清楚如何解密有效载荷，请查看 [指南](https://help.mikrotik.com/docs/display/UM/MikroTik+Tag+advertisement+formats#heading-Scriptfordecoding)。

##### MQTT代理

在每个KNOT上设置MQTT代理。

对于KNOT A：

`/iot/mqtt/brokers/add name=tb address=x.x.x.x port=1883 username=knot-A_access_token`

其中：

- `name` 是你希望给broker的名字，这个名字将在后面的脚本中使用；
- `address` 是broker/ThingsBoard服务器的IP地址；
- `port` 是broker监听的TCP端口，对于非SSL，通常是TCP 1883；
- `username` 是由MQTT代理决定的，在我们的例子中，它是一个在ThingsBoard管理门户中生成的 "访问令牌"。

对于KNOT B → 做同样的步骤。只需将 `用户名` 改为为KNOT B设备（网关）生成的相应访问令牌。

##### 脚本

将下面显示的脚本导入到每个KNOT。复制下面所示的 "代码 "并将其粘贴到一个新的终端窗口，然后按 "ENTER "键：

```shell
/system script add dont-require-permissions=no name=tracking owner=admin policy=\
    ftp,reboot,read,write,policy,test,password,sniff,sensitive,romon source="# Requ\
    ired packages: iot\r\
    \n\r\
    \n################################ Configuration ##############################\
    ##\r\
    \n# Name of an existing MQTT broker that should be used for publishing\r\
    \n:local broker \"tb\"\r\
    \n\r\
    \n# MQTT topic where the message should be published\r\
    \n:local topic \"v1/gateway/telemetry\"\r\
    \n\r\
    \n# POSIX regex for filtering advertisement Bluetooth addresses. E.g. \"^BC:33:\
    AC\"\r\
    \n# would only include addresses which start with those 3 octets.\r\
    \n# To disable this filter, set it to \"\"\r\
    \n:local addressRegex \"\"\r\
    \n\r\
    \n# POSIX regex for filtering Bluetooth advertisements based on their data. Sam\
    e\r\
    \n# usage as with 'addressRegex'.\r\
    \n:local advertisingDataRegex \"\"\r\
    \n\r\
    \n# Signal strength filter. E.g. -40 would only include Bluetooth advertisement\
    s\r\
    \n# whose signal strength is stronger than -40dBm.\r\
    \n# To disable this filter, set it to \"\"\r\
    \n:local rssiThreshold \"\"\r\
    \n\r\
    \n#Name the KNOT. Identity of the unit that will be senting the message. This n\
    ame will be reported to the MQTT broker.\r\
    \n:local gwName \"KNOT_A\"\r\
    \n\r\
    \n################################## Bluetooth ################################\
    ##\r\
    \n:put (\"[*] Gathering Bluetooth info...\")\r\
    \n\r\
    \n:global makeRecord do={\r\
    \n    :local jsonStr \"{\\\"ts\\\":\$ts,\\\"values\\\":{\\\"reporter\\\":\\\"\$\
    gwName\\\",\\\"rssi\\\":\$rssi}}\"\r\
    \n    :return \$jsonStr\r\
    \n}   \r\
    \n\r\
    \n# array of record strings collected for each advertising MAC address\r\
    \n:global macRecords [:toarray \"\"]\r\
    \n\r\
    \n# process advertisements and update macRecords\r\
    \n:local advertisements [/iot bluetooth scanners advertisements print detail as\
    -value where \\\r\
    \naddress ~ \$addressRegex and \\\r\
    \ndata ~ \$advertisingDataRegex and \\\r\
    \nrssi > \$rssiThreshold]\r\
    \n\r\
    \n/iot/bluetooth/scanners/advertisements clear\r\
    \n\r\
    \n:foreach adv in=\$advertisements do={\r\
    \n:local address (\$adv->\"address\")\r\
    \n:local rssi (\$adv->\"rssi\")\r\
    \n:local epoch (\$adv->\"epoch\")\r\
    \n                \r\
    \n:local recordStr [\$makeRecord ts=\$epoch gwName=\$gwName rssi=\$rssi]\r\
    \n\r\
    \n:if ([:len (\$macRecords->\$address)] > 0) do={\r\
    \n:local str (\$macRecords->\$address)\r\
    \n:local newStr \"\$str,\$recordStr\"\r\
    \n:set (\$macRecords->\$address) \$newStr} else={:set (\$macRecords->\$address)\
    \_\$recordStr}}\r\
    \n\r\
    \n# TODO: add some logic to decide when we want to send data\r\
    \n:local sendData true\r\
    \n\r\
    \n:if (\$sendData) do={\r\
    \n:local jsonStr \"{\"\r\
    \n\r\
    \n:foreach addr,advRec in=\$macRecords do={\r\
    \n:set jsonStr \"\$jsonStr\\\"\$addr\\\":[\$advRec],\"}\r\
    \n\r\
    \n:local payloadlength\r\
    \n:set payloadlength [:len (\$jsonStr)]\r\
    \n:local remcom\r\
    \n:set remcom [:pick \$jsonStr 0 (\$payloadlength-1)]\r\
    \n:set jsonStr \"\$remcom}\"\r\
    \n:local message\r\
    \n:set message \"\$jsonStr\"\r\
    \n:log info \"\$message\";\r\
    \n:put (\"[*] Message structured: \$message\")\r\
    \n:put (\"[*] Total message size: \$[:len \$message] bytes\")\r\
    \n:put (\"[*] Sending message to MQTT broker...\")\r\
    \n/iot mqtt publish broker=\"\$broker\" topic=\"\$topic\" message=\$message}"
```

该脚本应出现在“System>Scripts>Script List”选项卡下，名称为“tracking”或在命令 `/system script print` 的帮助下。

需要注意某些脚本行。

Broker名称配置行，这里需要输入你设置的MQTT broker名称：

>      :local broker "tb"

要输入一个正确的主题，供 MQTT 代理使用。 查看 [ThingsBoard 文档](https://thingsboard.io/docs/reference/gateway-mqtt-api/) 了解更多详情，默认情况下，主题应该是：

>      :local topic "v1/gateway/telemetry"

脚本内的 MAC 地址过滤选项。 可以输入 MAC 地址的所有 6 个八位字节（将过滤器应用于 1 个特定标签），或者可以用几个八位字节过滤列表，例如“^BC:33:AC”（应用过滤器 ，以便只处理以“BC:33:AC:...”开头的 MAC 地址）：

>     :local addressRegex "DC:2C:6E:0F:C0:3D"

有效载荷内容/数据。 允许根据特定有效负载内容过滤列表，例如 [制造商数据](https://help.mikrotik.com/docs/display/UM/MikroTik+Tag+advertisement+formats#heading-MikroTikPDUPayloadstructure) 。 例如，“15ff4f09”将丢弃所有不是 MikroTik 格式的有效载荷：

>     :local advertisingDataRegex "15ff4f09"

RSSI 信号强度过滤选项。 [场景说明](https://help.mikrotik.com/docs/display/ROS/Bluetooth+tag-tracking+using+MQTT+and+ThingsBoard#BluetoothtagtrackingusingMQTTandThingsBoard-Scenarioexample) 部分提到了此过滤选项。 此过滤器允许您忽略 RSSI 弱于配置值的任何负载。 例如。 “-40”将仅包括信号强度高于 -40dBm 的蓝牙广播：

>     :local rssiThreshold "-40"

KNOT标识符行。需要为每个独特的KNOT改变它。例如，将第一个KNOT称为KNOT_A，第二个KNOT称为KNOT_B：

> :local gwName "KNOT_A"

脚本的其他部分不需要更改

当运行该脚本时脚本使用过滤器 "检查广播报告" 选项卡（有效载荷列表选项卡），并构建一个JSON消息。一个JSON消息的例子是：

```json
{
  "2C:C8:1B:4B:BB:0A": [
    {
      "ts": 1678967250600,
      "values": {
        "reporter": "KNOT_A",
        "rssi": -47
      }
    }
  ],
  "DC:2C:6E:0F:C0:3D": [
    {
      "ts": 1678967247850,
      "values": {
        "reporter": "KNOT_A",
        "rssi": -59
      }
    },
    {
      "ts": 1678967257849,
      "values": {
        "reporter": "KNOT_A",
        "rssi": -67
      }
    }
  ]
}
```

数据的结构按照 [ThingsBoard指南]（https://thingsboard. io/docs/reference/gateway-mqtt-api/#telemetry-upload-api），其中"2C:C8:1B:4B:BB:0A"和"DC:2C:6E:0F:C0:3D"是出现在KNOT范围内的标签的MAC地址，"ts"是标签广播的每个有效载荷的unix时间戳（毫秒），"reporter"表示哪个具体的KNOT发送了信息，"rssi"是标签广播的每个有效载荷的信号强度（dBm）。

在有效载荷列表被 "搜索"并且JSON消息被结构化后，蓝牙接口有效载荷列表被 "清理"（或 "闪现"），之前结构化的JSON消息被发送到ThingsBoard MQTT代理。

要运行该脚本，请使用以下命令：

`/system script run tracking`

##### 调度器

在脚本中应用一个调度器，这样RouterOS就会定期自动运行脚本：

`/system/scheduler/add name=bluetoothscheduler interval=30s on-event="/system/script/run tracking"`

可以设置更短或更长的时间间隔。如果想更频繁地发送数据，使数据 "更新"，设置较短的时间间隔（10-15秒）。如果想发送更少的信息，更少的频率，可以设置更长的时间间隔（30分钟以上）。

使用脚本结构的JSON消息为每个收到的有效载荷分配一个"ts"值（时间戳）。意味着当脚本运行时，例如，**每分钟** 使用1个标签，**标签每10秒广播** 1个有效载荷（即每分钟6个有效载荷）→ ThingsBoard数据（GUI）将每分钟更新，每分钟将出现6个新条目（每个条目将表明它是在前一个条目10秒后收到的）。而如果每15分钟发送一次信息，使用1个标签，每10秒广播一次有效载荷（即每15分钟6/15=90个有效载荷）→ ThingsBoard数据（GUI）将每15分钟更新一次，会出现90个条目。

### ThingsBoard数据的可视化和结果验证

用 `/system script run tracking` 或通过调度器运行脚本并刷新GUI后在JSON消息中发现的所有MAC地址（标签），将在ThingsBoard GUI下成为新设备：

![](https://help.mikrotik.com/docs/download/attachments/176914435/image-2023-3-10_16-27-20.png?version=1&modificationDate=1678458439042&api=v2)

为了可视化数据，可以使用内置的 [部件](https://thingsboard.io/docs/user-guide/ui/widget-library/) 或创建自己的部件。

从设备列表中选择标签的MAC地址，进入 "最新遥测"，勾选 "报告者"参数，然后点击 "显示在小工具上"按钮：

![](https://help.mikrotik.com/docs/download/attachments/176914435/image-2023-3-10_16-28-25.png?version=1&modificationDate=1678458504104&api=v2)

选择一个要用的部件，例如在 "卡片"包下的 "时间序列表"，然后点击 "添加到仪表板"：

![](https://help.mikrotik.com/docs/download/attachments/176914435/image-2023-3-10_16-31-2.png?version=1&modificationDate=1678458660778&api=v2)

创建一个新的仪表板，并以喜欢的方式命名它。点击 "添加"：

![](https://help.mikrotik.com/docs/download/attachments/176914435/image-2023-3-10_16-32-45.png?version=1&modificationDate=1678458764038&api=v2)

对出现在 "设备 "标签下的其他标签做同样的动作。在同一仪表板下为每个独特的标签创建一个新的小组件。

将小组件的 "时间窗口"从 "实时-最后一分钟"（默认）改为 "实时-当前一天"：

![](https://help.mikrotik.com/docs/download/attachments/176914435/image-2023-3-16_15-5-32.png?version=1&modificationDate=1678971906709&api=v2)

因此，如果两个标签都在 **KNOT A** 的范围内，仪表板会显示：

![](https://help.mikrotik.com/docs/download/attachments/176914435/image-2023-3-16_15-10-47.png?version=1&modificationDate=1678972222157&api=v2)

如果他们移动到 **KNOT B** 范围内，就会显示：

![](https://help.mikrotik.com/docs/download/attachments/176914435/image-2023-3-16_15-18-17.png?version=1&modificationDate=1678972671628&api=v2)

如果标签移动到 **重叠区域**，在两个范围内，两个报告者（KNOT_A和KNOT_B）应该在彼此的几秒钟内显示出来，这取决于调度器中的间隔：

![](https://help.mikrotik.com/docs/download/attachments/176914435/image-2023-3-16_15-20-49.png?version=1&modificationDate=1678972824047&api=v2)

## 实例2

In the second example, we will showcase another topology:

![](https://help.mikrotik.com/docs/download/attachments/176914435/KNOT_illustration_2023_advanced%283%29.png?version=1&modificationDate=1681458868009&api=v2)

有几个仓库，几辆公司的送货车辆，以及3项有兴趣追踪的资产。资产是装载货物的托盘，目的是要知道：

- 资产（配备了KNOT）目前在哪个特定的仓库中（配备了标签），以及它在特定仓库中待了多少时间；
- 资产（配备标签）是否在路上，在仓库之间传送，以及它在车辆（配备KNOT）内花了多少时间；
- （可选）如果使用 [TG-BT5-OUT](https://mikrotik.com/product/tg_bt5_out) 标签，在这段时间内的温度是多少？也可以监测其他参数，可以从广播的 [有效载荷](https://help.mikrotik.com/docs/display/UM/MikroTik+Tag+advertisement+formats#heading-Example) 中得到，比如加速度；
- （可选）找出KNOT的GPS位置。

要实现蓝牙资产追踪，只需在每个仓库安装1个KNOT，每个车辆安装1个KNOT，每个资产安装1个标签。

可以看到，TAG 1在车内，而这辆车正好停在仓库附近。KNOT 1和KNOT 4都会向服务器报告，资产在它们的范围内。这将告诉你资产已经停放，但还没有被运输。

可以看到，TAG 2正在仓库之间运输，只在KNOT 5的蓝牙范围内。在这种情况下，KNOT 5将是唯一的报告者，服务器上显示的结果将意味着资产正在被运输。

可以看到，TAG 3在仓库内。服务器显示的就是这一点。

服务器上的数据将显示KNOT发送的每个报告的时间戳，这将告诉你资产在特定设备的蓝牙范围内停留了多长时间。

### 配置

在这个例子中将展示一个基本的拓扑结构，其中有2个仓库，1辆卡车在它们之间行驶，以及1个资产/托盘/标签。

#### ThingsBoard准备

检查 [指南](https://help.mikrotik.com/docs/display/ROS/MQTT+and+ThingsBoard+configuration) 了解如何设置ThingsBoard和RouterOS以利用MQTT通信。

这个例子将展示 [access-token](https://help.mikrotik.com/docs/display/ROS/MQTT+and+ThingsBoard+configuration#MQTTandThingsBoardconfiguration-Accesstokenscenario.1) 方案，也可以使用其他可用选项。对于生产环境，建议使用SSL-MQTT，因为非SSL-MQTT很容易被抓包和检查。

要了解如何在 [容器](https://help.mikrotik.com/docs/display/ROS/Container) 运行的实例上实现SSL-MQTT通信。请查看 [这里](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=166920348) 的指南（[启用HTTPS和SSL MQTT](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=166920348#ContainerThingsBoardMQTT/HTTPserver-EnablingHTTPSandSSLMQTT) 部分）。

在ThingsBoard GUI下创建3个KNOTs，并设置为 "网关"。

进入 "设备 "部分，点击 "+"按钮和 "添加新设备"：

![](https://help.mikrotik.com/docs/download/attachments/176914435/image-2023-3-8_13-29-22.png?version=1&modificationDate=1678274944385&api=v2)

命名该设备，并勾选 "是否为网关"选项：

![](https://help.mikrotik.com/docs/download/attachments/176914435/image-2023-4-3_14-57-56.png?version=1&modificationDate=1680523075535&api=v2)

对每个KNOT都这样设置：

![](https://help.mikrotik.com/docs/download/attachments/176914435/image-2023-4-3_14-58-22.png?version=1&modificationDate=1680523101926&api=v2)

在 "管理证书 "标签下，为刚刚创建的设备下的每个KNOT设置一个唯一的访问令牌（唯一的证书）：

![](https://help.mikrotik.com/docs/download/attachments/176914435/image-2023-4-3_14-59-8.png?version=1&modificationDate=1680523147189&api=v2)

#### RouterOS配置

##### 准备工作

在继续之前需要确认的蓝牙标签确实出现在KNOT的蓝牙范围内，并且KNOT可以检测到它们。可以用 `/iot bluetooth scanners advertisements print` 命令来查看：

```shell
/iot bluetooth scanners advertisements print
 # DEVICE     PDU-TYPE        TIME                 ADDRESS-TYPE ADDRESS                    RSSI     LENGTH DATA                                          
 0 bt1        adv-noconn-ind  mar/08/2023 12:35:15 public       2C:C8:1B:4B:BB:0A        -50dBm         22 15ff4f090100b0110100ffff00000019d68d2300005d  
 1 bt1        adv-noconn-ind  mar/08/2023 12:35:16 public       DC:2C:6E:0F:C0:3D        -39dBm         22 15ff4f0901008f3cfcfffbfffaff301783c22c000064  
 2 bt1        adv-noconn-ind  mar/08/2023 12:35:35 public       2C:C8:1B:4B:BB:0A        -50dBm         22 15ff4f09010084d500000400ffff0319ea8d2300005d  
 3 bt1        adv-noconn-ind  mar/08/2023 12:35:45 public       2C:C8:1B:4B:BB:0A        -50dBm         22 15ff4f090100e607faffffff03000319f48d2300005d  
```

或者可以使用 [Webfig](https://help.mikrotik.com/docs/display/ROS/Webfig) 或 [Winbox](https://help.mikrotik.com/docs/display/ROS/Winbox) 在物联网>蓝牙>广播报告标签下检查。

该列表可能是乱的。随机有效载荷可能会出现在列表中，因为扫描器会捕获周围的一切。为了减少列表内容，可以使用标签的MAC地址 `/iot bluetooth scanners advertisements print where address=DC:2C:6E:0F:C0:3D` 来过滤它：

```shell
/iot bluetooth scanners advertisements print where address=DC:2C:6E:0F:C0:3D
 # DEVICE    PDU-TYPE        TIME                 ADDRESS-TYPE ADDRESS                    RSSI     LENGTH DATA                                          
 0 bt1       adv-noconn-ind  mar/08/2023 12:41:06 public       DC:2C:6E:0F:C0:3D        -49dBm         22 15ff4f0901005ab20100fdfffdff4017e1c32c000064  
 1 bt1       adv-noconn-ind  mar/08/2023 12:41:26 public       DC:2C:6E:0F:C0:3D        -40dBm         22 15ff4f090100349704000000fcff4017f5c32c000064  
 2 bt1       adv-noconn-ind  mar/08/2023 12:41:36 public       DC:2C:6E:0F:C0:3D        -49dBm         22 15ff4f09010073fb0000000000003017ffc32c000064  
 3 bt1       adv-noconn-ind  mar/08/2023 12:41:46 public       DC:2C:6E:0F:C0:3D        -43dBm         22 15ff4f090100b88cffffffffffff401709c42c000064 
```

要弄清楚如何解密有效载荷，请查看 [指南](https://help.mikrotik.com/docs/display/UM/MikroTik+Tag+advertisement+formats#heading-Scriptfordecoding)。

##### MQTT代理

在每个KNOT上设置MQTT代理。

对于KNOT_1：

`/iot/mqtt/brokers/add name=tb address=x.x.x.x port=1883 username=knot-1_access_token`

其中：

- `name` 是你希望给broker 的名字，这个名字将在后面的脚本中使用；
- `address` 是broker /ThingsBoard服务器的IP地址；
- `port` 是经纪人监听的TCP端口，对于非SSL，通常是TCP 1883；
- `username` 是由MQTT代理决定的，在我们的例子中，它是在ThingsBoard管理门户中生成的 "访问令牌"。

对于KNOT_2和KNOT_3做同样的设置。只需将 "用户名 "改为各自生成的访问令牌。

##### 脚本

将下面脚本导入到每个KNOT。复制下面显示的 "代码 "并将其粘贴到一个新的终端窗口，然后按 "ENTER "键：

```shell
/system script add dont-require-permissions=no name=tracking owner=admin policy=\
    ftp,reboot,read,write,policy,test,password,sniff,sensitive,romon source="# Required package\
    s: iot\r\
    \n\r\
    \n################################ Configuration ################################\r\
    \n# Name of an existing MQTT broker that should be used for publishing\r\
    \n:local broker \"tb\"\r\
    \n\r\
    \n# MQTT topic where the message should be published\r\
    \n:local topic \"v1/gateway/telemetry\"\r\
    \n\r\
    \n# POSIX regex for filtering advertisement Bluetooth addresses. E.g. \"^BC:33:AC\"\r\
    \n# would only include addresses which start with those 3 octets.\r\
    \n# To disable this filter, set it to \"\"\r\
    \n:local addressRegex \"\"\r\
    \n\r\
    \n# POSIX regex for filtering Bluetooth advertisements based on their data. Same\r\
    \n# usage as with 'addressRegex'.\r\
    \n:local advertisingDataRegex \"\"\r\
    \n\r\
    \n# Signal strength filter. E.g. -40 would only include Bluetooth advertisements\r\
    \n# whose signal strength is stronger than -40dBm.\r\
    \n# To disable this filter, set it to \"\"\r\
    \n:local rssiThreshold \"\"\r\
    \n\r\
    \n#Name the KNOT. Identity of the unit that will be senting the message. This name will be \
    reported to the MQTT broker.\r\
    \n:local gwName \"1\"\r\
    \n\r\
    \n################################## Bluetooth ##################################\r\
    \n:put (\"[*] Gathering Bluetooth info...\")\r\
    \n\r\
    \n:global makeRecord do={\r\
    \n    :local jsonStr \"{\\\"ts\\\":\$ts,\\\"values\\\":{\\\"KNOT_\$gwName\\\":\\\"\$gwName\
    \\\",\\\"rssi\\\":\$rssi}}\"\r\
    \n    :return \$jsonStr\r\
    \n}   \r\
    \n\r\
    \n# array of record strings collected for each advertising MAC address\r\
    \n:global macRecords [:toarray \"\"]\r\
    \n\r\
    \n# process advertisements and update macRecords\r\
    \n:local advertisements [/iot bluetooth scanners advertisements print detail as-value where\
    \_\\\r\
    \naddress ~ \$addressRegex and \\\r\
    \ndata ~ \$advertisingDataRegex and \\\r\
    \nrssi > \$rssiThreshold]\r\
    \n\r\
    \n/iot/bluetooth/scanners/advertisements clear\r\
    \n\r\
    \n:foreach adv in=\$advertisements do={\r\
    \n:local address (\$adv->\"address\")\r\
    \n:local rssi (\$adv->\"rssi\")\r\
    \n:local epoch (\$adv->\"epoch\")\r\
    \n                \r\
    \n:local recordStr [\$makeRecord ts=\$epoch gwName=\$gwName rssi=\$rssi]\r\
    \n\r\
    \n:if ([:len (\$macRecords->\$address)] > 0) do={\r\
    \n:local str (\$macRecords->\$address)\r\
    \n:local newStr \"\$str,\$recordStr\"\r\
    \n:set (\$macRecords->\$address) \$newStr} else={:set (\$macRecords->\$address) \$recordStr\
    }}\r\
    \n\r\
    \n# TODO: add some logic to decide when we want to send data\r\
    \n:local sendData true\r\
    \n\r\
    \n:if (\$sendData) do={\r\
    \n:local jsonStr \"{\"\r\
    \n\r\
    \n:foreach addr,advRec in=\$macRecords do={\r\
    \n:set jsonStr \"\$jsonStr\\\"\$addr\\\":[\$advRec],\"}\r\
    \n\r\
    \n:local payloadlength\r\
    \n:set payloadlength [:len (\$jsonStr)]\r\
    \n:local remcom\r\
    \n:set remcom [:pick \$jsonStr 0 (\$payloadlength-1)]\r\
    \n:set jsonStr \"\$remcom}\"\r\
    \n:local message\r\
    \n:set message \"\$jsonStr\"\r\
    \n:log info \"\$message\";\r\
    \n:put (\"[*] Message structured: \$message\")\r\
    \n:put (\"[*] Total message size: \$[:len \$message] bytes\")\r\
    \n:put (\"[*] Sending message to MQTT broker...\")\r\
    \n/iot mqtt publish broker=\"\$broker\" topic=\"\$topic\" message=\$message}"
```

脚本应该出现在 "系统>脚本>脚本列表 "标签下，名称为 "tracking"，或者在 `/system script print` 命令下出现。

有些脚本行需要注意。

Broker 名称配置行需要输入设定的MQTT broker 名称：

> :local broker "tb"

要输入一个正确的主题，由MQTT代理使用。查看 [ThingsBoard documentation](https://thingsboard.io/docs/reference/gateway-mqtt-api/) 了解更多细节，默认情况下，主题应该是：

> :local topic "v1/gateway/telemetry"

脚本本身的MAC地址过滤选项。可以输入MAC地址的所有6个八位数（过滤器应用于一个特定的标签），或者你可以使用几个八位数来过滤列表，比如"^BC:33:AC"（应用过滤器，所以只有以 "BC:33:AC:... "开头的MAC地址会被处理）：

>     :local addressRegex "DC:2C:6E:0F:C0:3D"

有效载荷内容数据。允许根据特定的有效载荷内容过滤列表，如 [制造商数据](https://help.mikrotik.com/docs/display/UM/MikroTik+Tag+advertisement+formats#heading-MikroTikPDUPayloadstructure)。例如，"15ff4f09 "将丢弃所有非MikroTik格式的有效载荷：

> :local advertisingDataRegex "15ff4f09"

RSSI信号强度过滤选项。这个过滤选项在 [场景解释](https://help.mikrotik.com/docs/display/ROS/Bluetooth+tag-tracking+using+MQTT+and+ThingsBoard#BluetoothtagtrackingusingMQTTandThingsBoard-Scenarioexample)  部分提到。这个过滤器允许忽略任何RSSI弱于配置值的有效载荷。例如。"-40 "将只包括信号强度高于-40dBm的蓝牙广播：

>     :local rssiThreshold "-40"

KNOT标识符行。需要为每个独特的KNOT改变它。例如，将第一个KNOT标识为 "1"，第二个KNOT为 "2"，第三个KNOT为 "3"：

> :local gwName "1"

脚本的其他部分不需要更改

运行该脚本时，脚本使用过滤器 "检查广播报告"选项卡（有效载荷列表选项卡），并构建一个JSON消息。JSON消息的例子是：

```json
{
  "2C:C8:1B:4B:BB:0A": [
    {
      "ts": 1680526087729,
      "values": {
        "KNOT_1": "1",
        "rssi": -47
      }
    }
  ],
  "DC:2C:6E:0F:C0:3D": [
    {
      "ts": 1680526065000,
      "values": {
        "KNOT_1": "1",
        "rssi": -49
      }
    },
    {
      "ts": 1680526075001,
      "values": {
        "KNOT_1": "1",
        "rssi": -50
      }
    }
  ]
}
```

数据的结构是按照 [ThingsBoard指南]（https://thingsboard. io/docs/reference/gateway-mqtt-api/#telemetry-upload-api），其中"2C:C8:1B:4B:BB:0A"和"DC:2C:6E:0F:C0:3D"是出现在KNOT范围内的标签的MAC地址，"ts"是标签广播的每个有效载荷的unix时间戳（毫秒），"KNOT_X"表示哪个具体的KNOT发送了信息，"rssi"是标签广播的每个有效载荷的信号强度（dBm）。

在有效载荷列表被 "搜索 "并且JSON消息被结构化后，蓝牙接口有效载荷列表被 "清理"或 "闪现"，之前结构化的JSON消息被发送到ThingsBoard MQTT代理。

要运行该脚本，请使用以下命令：

`/system script run tracking`

###### 包含温度数据的脚本（可选）

如果要在结构化信息中加入温度报告，请使用下面的脚本：

```shell
/system script add dont-require-permissions=no name=tracking+temp owner=admin policy=\
    ftp,reboot,read,write,policy,test,password,sniff,sensitive,romon source="# Required package\
    s: iot\r\
    \n\r\
    \n################################ Configuration ################################\r\
    \n# Name of an existing MQTT broker that should be used for publishing\r\
    \n:local broker \"tb\"\r\
    \n\r\
    \n# MQTT topic where the message should be published\r\
    \n:local topic \"v1/gateway/telemetry\"\r\
    \n\r\
    \n# POSIX regex for filtering advertisement Bluetooth addresses. E.g. \"^BC:33:AC\"\r\
    \n# would only include addresses which start with those 3 octets.\r\
    \n# To disable this filter, set it to \"\"\r\
    \n:local addressRegex \"\"\r\
    \n\r\
    \n# POSIX regex for filtering Bluetooth advertisements based on their data. Same\r\
    \n# usage as with 'addressRegex'.\r\
    \n:local advertisingDataRegex \"\"\r\
    \n\r\
    \n# Signal strength filter. E.g. -40 would only include Bluetooth advertisements\r\
    \n# whose signal strength is stronger than -40dBm.\r\
    \n# To disable this filter, set it to \"\"\r\
    \n:local rssiThreshold \"\"\r\
    \n\r\
    \n#Name the KNOT. Identity of the unit that will be senting the message. This name will be \
    reported to the MQTT broker.\r\
    \n:local gwName \"1\"\r\
    \n\r\
    \n################################## Bluetooth ##################################\r\
    \n:global invertU16 do={\r\
    \n    :local inverted 0\r\
    \n    :for idx from=0 to=15 step=1 do={\r\
    \n        :local mask (1 << \$idx)\r\
    \n        :if (\$1 & \$mask = 0) do={\r\
    \n            :set \$inverted (\$inverted | \$mask)\r\
    \n        }\r\
    \n    }\r\
    \n    return \$inverted\r\
    \n}\r\
    \n\r\
    \n:global le16ToHost do={\r\
    \n    :local lsb [:pick \$1 0 2]\r\
    \n    :local msb [:pick \$1 2 4]\r\
    \n\r\
    \n    :return [:tonum \"0x\$msb\$lsb\"]\r\
    \n}\r\
    \n:local from88 do={\r\
    \n    :global invertU16\r\
    \n    :global le16ToHost\r\
    \n    :local num [\$le16ToHost \$1]\r\
    \n\r\
    \n    # Handle negative numbers\r\
    \n    :if (\$num & 0x8000) do={\r\
    \n        :set num (-1 * ([\$invertU16 \$num] + 1))\r\
    \n    }\r\
    \n\r\
    \n    # Convert from 8.8. Scale by 1000 since floating point is not supported\r\
    \n    :return ((\$num * 125) / 32)\r\
    \n}\r\
    \n:put (\"[*] Gathering Bluetooth info...\")\r\
    \n\r\
    \n:global makeRecord do={\r\
    \n    :local jsonStr \"{\\\"ts\\\":\$ts,\\\"values\\\":{\\\"KNOT_\$gwName\\\":\\\"\$gwName\
    \\\",\\\"temp\\\":\$temp}}\"\r\
    \n    :return \$jsonStr\r\
    \n}   \r\
    \n\r\
    \n# array of record strings collected for each advertising MAC address\r\
    \n:global macRecords [:toarray \"\"]\r\
    \n\r\
    \n# process advertisements and update macRecords\r\
    \n:local advertisements [/iot bluetooth scanners advertisements print detail as-value where\
    \_\\\r\
    \naddress ~ \$addressRegex and \\\r\
    \ndata ~ \$advertisingDataRegex and \\\r\
    \nrssi > \$rssiThreshold]\r\
    \n\r\
    \n/iot/bluetooth/scanners/advertisements clear\r\
    \n\r\
    \n:foreach adv in=\$advertisements do={\r\
    \n:local address (\$adv->\"address\")\r\
    \n:local ad (\$adv->\"data\")\r\
    \n:local rssi (\$adv->\"rssi\")\r\
    \n:local epoch (\$adv->\"epoch\")\r\
    \n:local temp [\$from88 [:pick \$ad 28 32]]\r\
    \n                \r\
    \n:local recordStr [\$makeRecord ts=\$epoch gwName=\$gwName temp=\$temp]\r\
    \n\r\
    \n:if ([:len (\$macRecords->\$address)] > 0) do={\r\
    \n:local str (\$macRecords->\$address)\r\
    \n:local newStr \"\$str,\$recordStr\"\r\
    \n:set (\$macRecords->\$address) \$newStr} else={:set (\$macRecords->\$address) \$recordStr\
    }}\r\
    \n\r\
    \n# TODO: add some logic to decide when we want to send data\r\
    \n:local sendData true\r\
    \n\r\
    \n:if (\$sendData) do={\r\
    \n:local jsonStr \"{\"\r\
    \n\r\
    \n:foreach addr,advRec in=\$macRecords do={\r\
    \n:set jsonStr \"\$jsonStr\\\"\$addr\\\":[\$advRec],\"}\r\
    \n\r\
    \n:local payloadlength\r\
    \n:set payloadlength [:len (\$jsonStr)]\r\
    \n:local remcom\r\
    \n:set remcom [:pick \$jsonStr 0 (\$payloadlength-1)]\r\
    \n:set jsonStr \"\$remcom}\"\r\
    \n:local message\r\
    \n:set message \"\$jsonStr\"\r\
    \n:log info \"\$message\";\r\
    \n:put (\"[*] Message structured: \$message\")\r\
    \n:put (\"[*] Total message size: \$[:len \$message] bytes\")\r\
    \n:put (\"[*] Sending message to MQTT broker...\")\r\
    \n/iot mqtt publish broker=\"\$broker\" topic=\"\$topic\" message=\$message}"
```

在这种情况下，JSON信息看起来是这样的：

```json
{
  "2C:C8:1B:4B:BB:0A": [
    {
      "ts": 1680527467840,
      "values": {
        "KNOT_1": "1",
        "temp": 26460
      }
    }
  ],
  "DC:2C:6E:0F:C0:3D": [
    {
      "ts": 1680527464996,
      "values": {
        "KNOT_1": "1",
        "temp": 24750
      }
    },
    {
      "ts": 1680527474996,
      "values": {
        "KNOT_1": "1",
        "temp": 24750
      }
    }
  ]
}
```

由于不支持浮点运算，每一个小数点后面的计算都会被 "四舍五入"为整数。这就是为什么脚本会计算温度和加速度的值，**按1000** 缩放（乘以 **1000** ）。 
所以，如果看到温度是 **temp=24750**，实际温度是 **24.750 C**。要添加小数点，要在服务器端做一个额外的结果 "翻译"，或者在RouterOS端使用额外的脚本将增加设备的CPU使用率。

###### 包含GPS数据的脚本（可选）

如果希望包括GPS数据（来自KNOTs的经度和纬度值），请使用下面的脚本：

```shell
/system script add dont-require-permissions=no name=tracking+gps+temp owner=admin policy=\
    ftp,reboot,read,write,policy,test,password,sniff,sensitive,romon source="# Required package\
    s: iot\r\
    \n\r\
    \n################################ Configuration ################################\r\
    \n# Name of an existing MQTT broker that should be used for publishing\r\
    \n:local broker \"tb\"\r\
    \n\r\
    \n# MQTT topic where the message should be published\r\
    \n:local topic \"v1/gateway/telemetry\"\r\
    \n:local gwtopic \"v1/devices/me/telemetry\"\r\
    \n\r\
    \n# POSIX regex for filtering advertisement Bluetooth addresses. E.g. \"^BC:33:AC\"\r\
    \n# would only include addresses which start with those 3 octets.\r\
    \n# To disable this filter, set it to \"\"\r\
    \n:local addressRegex \"\"\r\
    \n\r\
    \n# POSIX regex for filtering Bluetooth advertisements based on their data. Same\r\
    \n# usage as with 'addressRegex'.\r\
    \n:local advertisingDataRegex \"15ff\"\r\
    \n\r\
    \n# Signal strength filter. E.g. -40 would only include Bluetooth advertisements\r\
    \n# whose signal strength is stronger than -40dBm.\r\
    \n# To disable this filter, set it to \"\"\r\
    \n:local rssiThreshold \"\"\r\
    \n\r\
    \n#Name the KNOT. Identity of the unit that will be senting the message. This name will be \
    reported to the MQTT broker.\r\
    \n:local gwName \"2\"\r\
    \n\r\
    \n###########GPS#############\r\
    \n:global lat\r\
    \n:global lon\r\
    \n\r\
    \n/interface ppp-client set ppp-out1 disabled=yes\r\
    \n:log info (\"disabling WWAN to get GPS coordinates\")\r\
    \n\r\
    \n/interface ppp-client at-chat ppp-out1 input=\"AT+QGPSCFG=\\\"priority\\\",0\"\r\
    \n:log info (\"enabling priority for GPS\")\r\
    \n\r\
    \n###the time in the delay below is the time that the device will wait for to get the coord\
    inate fix\r\
    \n:delay 32000ms\r\
    \n:log info (\"reading GPS coordinates\")\r\
    \n/system gps monitor once do={\r\
    \n:set \$lat \$(\"latitude\")\r\
    \n:set \$lon \$(\"longitude\")\r\
    \n}\r\
    \n:if (\$lat != \"none\") do={\\\r\
    \n:log info (\"enabling priority back to WWAN\")\r\
    \n/interface ppp-client at-chat ppp-out1 input=\"AT+QGPSCFG=\\\"priority\\\",1\"\r\
    \n:log info (\"enabling WWAN\")\r\
    \n/interface ppp-client set ppp-out1 disabled=no\r\
    \n:delay 1000ms\r\
    \n###if dial on demand is enabled\r\
    \n/ping 1.1.1.1 count=1\r\
    \n\r\
    \n#the delay below waits for 5 seconds for the ppp connection to get established - this tim\
    e can differ based on the signal strength\r\
    \n:delay 5000ms\r\
    \n:log info (\"posting coordinates via mqtt\")\r\
    \n:local gpsmessage \\\r\
    \n    \"{\\\"latitude\\\":\$lat,\\\r\
    \n    \\\"longitude\\\":\$lon}\"\r\
    \n/iot mqtt publish broker=\$broker topic=\$gwtopic message=\$gpsmessage} else={\\\r\
    \n:log info (\"could not read GPS coordinates...enabling back WWAN\")\r\
    \n/interface ppp-client at-chat ppp-out1 input=\"AT+QGPSCFG=\\\"priority\\\",1\"\r\
    \n/interface ppp-client set ppp-out1 disabled=no\r\
    \n:delay 1000ms\r\
    \n###if dial on demand is enabled\r\
    \n/ping 1.1.1.1 count=1\r\
    \n:delay 5000ms\r\
    \n}\r\
    \n\r\
    \n##################################Bluetooth##################################\r\
    \n:global invertU16 do={\r\
    \n    :local inverted 0\r\
    \n    :for idx from=0 to=15 step=1 do={\r\
    \n        :local mask (1 << \$idx)\r\
    \n        :if (\$1 & \$mask = 0) do={\r\
    \n            :set \$inverted (\$inverted | \$mask)\r\
    \n        }\r\
    \n    }\r\
    \n    return \$inverted\r\
    \n}\r\
    \n\r\
    \n:global le16ToHost do={\r\
    \n    :local lsb [:pick \$1 0 2]\r\
    \n    :local msb [:pick \$1 2 4]\r\
    \n\r\
    \n    :return [:tonum \"0x\$msb\$lsb\"]\r\
    \n}\r\
    \n:local from88 do={\r\
    \n    :global invertU16\r\
    \n    :global le16ToHost\r\
    \n    :local num [\$le16ToHost \$1]\r\
    \n\r\
    \n    # Handle negative numbers\r\
    \n    :if (\$num & 0x8000) do={\r\
    \n        :set num (-1 * ([\$invertU16 \$num] + 1))\r\
    \n    }\r\
    \n\r\
    \n    # Convert from 8.8. Scale by 1000 since floating point is not supported\r\
    \n    :return ((\$num * 125) / 32)\r\
    \n}\r\
    \n:put (\"[*] Gathering Bluetooth info...\")\r\
    \n\r\
    \n:global makeRecord do={\r\
    \n    :local jsonStr \"{\\\"ts\\\":\$ts,\\\"values\\\":{\\\"KNOT_\$gwName\\\":\\\"\$gwName\
    \\\",\\\"temp\\\":\$temp}}\"\r\
    \n    :return \$jsonStr\r\
    \n}   \r\
    \n\r\
    \n# array of record strings collected for each advertising MAC address\r\
    \n:global macRecords [:toarray \"\"]\r\
    \n\r\
    \n# process advertisements and update macRecords\r\
    \n:local advertisements [/iot bluetooth scanners advertisements print detail as-value where\
    \_\\\r\
    \naddress ~ \$addressRegex and \\\r\
    \ndata ~ \$advertisingDataRegex and \\\r\
    \nrssi > \$rssiThreshold]\r\
    \n\r\
    \n/iot/bluetooth/scanners/advertisements clear\r\
    \n\r\
    \n:foreach adv in=\$advertisements do={\r\
    \n:local address (\$adv->\"address\")\r\
    \n:local ad (\$adv->\"data\")\r\
    \n:local rssi (\$adv->\"rssi\")\r\
    \n:local epoch (\$adv->\"epoch\")\r\
    \n:local temp [\$from88 [:pick \$ad 28 32]]\r\
    \n                \r\
    \n:local recordStr [\$makeRecord ts=\$epoch gwName=\$gwName temp=\$temp]\r\
    \n\r\
    \n:if ([:len (\$macRecords->\$address)] > 0) do={\r\
    \n:local str (\$macRecords->\$address)\r\
    \n:local newStr \"\$str,\$recordStr\"\r\
    \n:set (\$macRecords->\$address) \$newStr} else={:set (\$macRecords->\$address) \$recordStr\
    }}\r\
    \n\r\
    \n# TODO: add some logic to decide when we want to send data\r\
    \n:local sendData true\r\
    \n\r\
    \n:if (\$sendData) do={\r\
    \n:local jsonStr \"{\"\r\
    \n\r\
    \n:foreach addr,advRec in=\$macRecords do={\r\
    \n:set jsonStr \"\$jsonStr\\\"\$addr\\\":[\$advRec],\"}\r\
    \n\r\
    \n:local payloadlength\r\
    \n:set payloadlength [:len (\$jsonStr)]\r\
    \n:local remcom\r\
    \n:set remcom [:pick \$jsonStr 0 (\$payloadlength-1)]\r\
    \n:set jsonStr \"\$remcom}\"\r\
    \n:local message\r\
    \n:set message \"\$jsonStr\"\r\
    \n:log info \"\$message\";\r\
    \n:put (\"[*] Message structured: \$message\")\r\
    \n:put (\"[*] Total message size: \$[:len \$message] bytes\")\r\
    \n:put (\"[*] Sending message to MQTT broker...\")\r\
    \n/iot mqtt publish broker=\"\$broker\" topic=\"\$topic\" message=\$message}"
  ```

这时需要记住 [BG77调制解调器行为](https://help.mikrotik.com/docs/display/UM/WWAN+and+GNSS+priority+automatization) BG77蜂窝调制解调器（在KNOT中使用）不能用于蜂窝CAT-M/NB-IoT的持续连接和同时获得GPS坐标。

脚本运行时：

- PPP接口被禁用，最高优先级被设置为GPS接收（当蜂窝PPP接口被关闭时），持续32秒（这个时间可以在脚本中改变）；
- (a) 如果设备在配置的32秒内设法获得了GPS纬度值（如果获得的值等于 "无 "以外的任何值），脚本将构造一个带有捕获的经纬度值的JSON消息，脚本将为WWAN设置最高优先级（将优先级从GPS改为WWAN）并重新启用PPP接口（用于互联网接入）。之后，脚本将通过第一个MQTT发布发送GPS数据JSON消息，并且，脚本将运行蓝牙部分，其中蓝牙数据JSON消息被结构化，并通过第二个MQTT发布发送（发送2个MQTT消息→GPS数据MQTT消息和蓝牙数据MQTT消息）；
- (b) 如果设备在32秒间隔内未能获得GPS纬度值（如果获得的值等于 "无"），脚本将为WWAN设置最高优先级（将优先级从GPS改为WWAN），将PPP接口启用用于互联网访问，并只处理蓝牙部分，其中蓝牙数据JSON消息被结构化并通过MQTT发布发送（如果无法获得GPS数据，将发送带有蓝牙数据的1条MQTT消息）。

##### 调度器

在脚本中应用一个调度器，这样RouterOS就会定期自动运行脚本：

`/system/scheduler/add name=bluetoothscheduler interval=50s on-event="/system/script/run tracking"`

可以设置更短和更长的时间间隔。如果想更频繁地发送数据，使数据 "更新"，设置较短的时间间隔（10-15秒）。如果想发送更少的信息，更少的频率，可以设置更长的时间间隔（30分钟以上）。

使用脚本结构的JSON消息为每个收到的有效载荷分配一个"ts"值（时间戳）。意味着当脚本运行时，例如，**每分钟**，使用1个标签，**标签每10秒广播** 1个有效载荷（即每分钟6个有效载荷），ThingsBoard数据（GUI）将每分钟更新，每分钟将出现6个新条目（每个条目将表明它是在前一个条目10秒后收到的）。而如果每15分钟发送一次信息，使用1个标签，每10秒广播一次有效载荷（即每15分钟6/15=90个有效载荷）， ThingsBoard数据（GUI）将每15分钟更新一次，会出现90个条目。

### ThingsBoard数据的可视化和结果验证

在你用 `/system script run tracking`  或通过调度器运行脚本并刷新GUI门户后，所有在JSON消息中发现的MAC地址（标签），将变成ThingsBoard GUI下的新设备：

![](https://help.mikrotik.com/docs/download/attachments/176914435/image-2023-3-10_16-27-20.png?version=1&modificationDate=1678458439042&api=v2)

为了可视化数据，可以使用内置的 [部件](https://thingsboard.io/docs/user-guide/ui/widget-library/) 或创建你自己的部件。

从设备列表中选择标签的MAC地址，进入 "最新遥测 "部分，勾选你希望监测的KNOT ID，然后点击 "在部件上显示 "按钮：

![](https://help.mikrotik.com/docs/download/attachments/176914435/image-2023-4-3_16-25-5.png?version=1&modificationDate=1680528304274&api=v2)

选择一个要用的部件，例如在 "图表 "包下，"时间序列条形图"，然后点击 "添加到仪表板"：

![](https://help.mikrotik.com/docs/download/attachments/176914435/image-2023-4-3_16-26-10.png?version=1&modificationDate=1680528369090&api=v2)

创建一个新的仪表板，并以喜欢的方式命名。点击 "添加"：

![](https://help.mikrotik.com/docs/download/attachments/176914435/image-2023-4-3_16-26-58.png?version=1&modificationDate=1680528417752&api=v2)

将小组件的 "时间窗口 "从 "实时-最后一分钟"（默认）改为 "实时-最后5小时"，并禁用 "数据聚合功能"（选择 "无"）：

![](https://help.mikrotik.com/docs/download/attachments/176914435/image-2023-4-3_16-29-52.png?version=1&modificationDate=1680528591988&api=v2)

为了更好地可视化结果，编辑小组件，然后编辑每个 "KNOT_X "参数键。启用每个键的 "显示点 "复选框：

![](https://help.mikrotik.com/docs/download/attachments/176914435/image-2023-4-3_16-34-15.png?version=1&modificationDate=1680528854462&api=v2)

检查ThingsBoard小组件 [指南](https://thingsboard.io/docs/user-guide/ui/chart-widget/#timeseries-bar-chart)，了解更多选项。

最终的结果是这样的：

![](https://help.mikrotik.com/docs/download/attachments/176914435/image-2023-4-4_12-44-37.png?version=1&modificationDate=1680601435706&api=v2)

根据仪表板可以知道：

- 从~11:00到~11:30，资产在KNOT_1蓝牙范围内（1号仓库内）；
- 从~11:30到~11:35，资产被转移到停在仓库附近的车辆（KNOT_2）上（标签在两个KNOT的范围内）；
- 从~11:35到~12:00，标签在卡车（KNOT_2）内--驶向另一个仓库；
- 从~12:00到~12:05，资产停在2号仓库外，同时在KNOT_2和KNOT_3范围内；
- 从~12:05到12:30，资产存放在2号仓库（KNOT_3）内；
- 从~12:30开始，标签再次出现在路上的卡车内（KNOT_2）。

#### 温度可视化(可选)

从设备列表中选择标签的MAC地址，进入 "最新遥测 "部分，勾选"temp"参数，然后点击 "显示在小部件上 "按钮：

![](https://help.mikrotik.com/docs/download/attachments/176914435/image-2023-4-4_12-47-9.png?version=1&modificationDate=1680601587777&api=v2)

选择一个想用的部件，例如在 "图表 "下，"时间序列线图"。点击 "添加到仪表盘"，并选择想添加小工具的仪表盘。

结果是这样的：

![](https://help.mikrotik.com/docs/download/attachments/176914435/image-2023-4-4_12-52-40.png?version=1&modificationDate=1680601919137&api=v2)

现在有一个额外的图表，表明标签的温度在不同的时间间隔内如何变化。

#### GPS坐标的可视化（可选）

根据 [包含GPS数据的脚本](https://help.mikrotik.com/docs/display/ROS/Bluetooth+tag-tracking+using+MQTT+and+ThingsBoard#BluetoothtagtrackingusingMQTTandThingsBoard-ScriptthatincludesGPSdata) ，该脚本发送了2条MQTT消息。每个消息都被发送到一个不同的MQTT主题。GPS坐标信息将被发布到一个名为 "1/devices/me/telemetry "的主题，而蓝牙数据将被发布到一个名为 "v1/gateway/telemetry "的主题。坐标将在ThingsBoard设备列表中的特定网关下提供：

![](https://help.mikrotik.com/docs/download/attachments/176914435/image-2023-4-19_14-5-14.png?version=1&modificationDate=1681902313515&api=v2)

勾选 "纬度"和 "经度"两个参数，点击 "在部件上显示按钮"，选择 "当前捆绑 "到 "地图"，并选择 "Route Map-OpenStreetMap "部件：

![](https://help.mikrotik.com/docs/download/attachments/176914435/image-2023-4-19_14-8-34.png?version=1&modificationDate=1681902513884&api=v2)

最后，点击 "添加到仪表盘 "按钮，选择想显示的仪表盘。

再将3个部件添加到一个仪表板中（温度线图、蓝牙记者条形图和GPS坐标地图）后，得到类似这样的东西：

![](https://help.mikrotik.com/docs/download/attachments/176914435/image-2023-4-19_14-14-2.png?version=1&modificationDate=1681902841547&api=v2)

- 有一个显示温度变化的图表（标签的周围温度）;
- 有一个图表，表明哪个特定的KNOT发送了报告，告诉你标签目前在哪个KNOT的蓝牙范围内；
- 有一张地图，显示KNOT的GPS位置。