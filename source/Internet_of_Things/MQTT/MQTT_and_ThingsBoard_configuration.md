## MQTT和ThingsBoard配置

可以用云服务来监测由MQTT发布者发送的信息，其中之一是 [Thingsboard](https://thingsboard.io/)。本文将演示如何配置 Thingsboard 和 RouterOS，以使用 MQTT 协议发布数据。RouterOS在这个方案中作为一个网关，将数据从RouterBoard发布到Thingsboard的服务器。Thingsboard在这种情况下作为一个MQTT broker （数据发布的服务器）。

在进行设置之前需要做的是:

- a) 在 Thingsboard 的系统中创建一个账户。可以按照这个 [链接](https://thingsboard.cloud/signup) 来做。允许在有限的测试时间段内免费使用ThingsBoard云解决方案。
- b) 按照 [指南](https://thingsboard.io/docs/iot-gateway/installation/) 建立自己的服务器。有一个社区版，可以免费安装和使用。

请使用 **SSL MQTT（TCP端口8883和证书）**，而不是非SSL MQTT（TCP端口1883）。如果使用非SSL MQTT，客户端（MQTT publisher）和服务器（MQTT broker）之间的通信很容易被嗅探捕获，获取认证数据（如客户端ID，用户名和密码）。

## Thingsboard配置

在本指南中将展示本地实例服务器的安装配置，但同样的原则适用于云选项。

通过浏览器访问登录页面并登录。转到 **设备** 菜单。

通过点击添加按钮 "+" "添加新设备 "来创建一个新设备：

![](https://help.mikrotik.com/docs/download/attachments/105742352/image-2023-1-20_13-14-8.png?version=1&modificationDate=1674213240062&api=v2)

输入设备的名称并点击 "添加"：

![](https://help.mikrotik.com/docs/download/attachments/105742352/image-2023-1-20_13-15-46.png?version=1&modificationDate=1674213337475&api=v2)

默认情况下，新创建的设备会选择访问令牌认证。

### 访问令牌方案

通过点击创建的设备并进入 **管理凭证** 设置（在 **细节** 部分）改变令牌：

![](https://help.mikrotik.com/docs/download/attachments/105742352/image-2023-1-20_13-33-11.png?version=1&modificationDate=1674214382971&api=v2)

这个令牌将被用作MQTT发布者的 "用户名"（在RouterOS设置中）。

可以按照 [链接](https://thingsboard.io/docs/reference/mqtt-api/) 找到更多信息。

### MQTT基本方案

可以在 **设备凭证** 部分为特定设备改变凭证类型：

![](https://help.mikrotik.com/docs/download/attachments/105742352/image-2023-1-20_13-38-37.png?version=1&modificationDate=1674214708907&api=v2)

MQTT基本方案允许为MQTT认证指定客户端ID、用户名和密码。

你可以通过下面的 [链接](https://thingsboard.io/docs/user-guide/basic-mqtt/) 找到更多信息。

### 单向SSL通信方案

推荐使用的场景!

这种类型的认证要求使用服务器证书进行SSL通信。必须生成一个服务器证书并上传到ThingsBoard实例。

要生成服务器证书，请使用 [本指南](https://thingsboard.io/docs/user-guide/mqtt-over-ssl/) 作为参考生成证书（例如，使用OPENSSL工具），将其安装上传至正确的文件夹，并在ThingsBoard配置文件中启用MQTT SSL。

配置将与上面显示的 **访问令牌** 和 **MQTT基本方案** 中的配置相同。选择其中之一。

在这种情况下，唯一的区别是设备和服务器之间的通信（只需要稍微改变RouterOS设置中的MQTT代理配置，将在后面显示）。

**当使用这种方案时，通信将被加密（使用SSL）**。

### X.509（双向SSL通信）方案

这种类型的认证要求使用服务器证书和客户端证书进行SSL通信。必须生成一个服务器证书并上传到ThingsBoard实例。

要生成服务器证书，请使用 [本指南](https://thingsboard.io/docs/user-guide/mqtt-over-ssl/) 作为参考生成证书（例如，使用OPENSSL工具），将其安装上传至正确的文件夹，并在ThingsBoard配置文件中启用MQTT SSL。

要生成客户端证书，请使用 [本指南](https://thingsboard.io/docs/user-guide/certificates/) 作为参考。

可以在 **设备证书** 部分为特定设备改变证书类型：

![](https://help.mikrotik.com/docs/download/attachments/105742352/image-2023-1-20_13-39-23.png?version=1&modificationDate=1674214754226&api=v2)

X.509方案使用客户证书进行认证。

一旦证书生成（例如，使用OPEN SSL），将RSA公钥复制到该字段，并点击 "保存 "按钮。

## RouterOS配置

**注**： 为了配置MQTT，请确保事先安装 [iot包](https://help.mikrotik.com/docs/display/ROS/Packages)。

### MQTT Broker

#### 访问令牌的情况

添加一个MQTT Broker，如下图所示：

`/iot/mqtt/brokers/add name=tb address=x.x.x.x port=1883 username=access_token`

- 将 "地址 "改为 ThingsBoard 服务器的实际 IP/域名地址；
- 将 "用户名 "改为在 ThingsBoard 设置中使用的访问令牌。

#### MQTT基本方案

添加一个MQTT broker ，如下图所示：

`/iot/mqtt/brokers/add name=tb address=x.x.x.x client-id=clientid password=password username=username`

- 将 "地址 "改为 ThingsBoard 服务器的实际 IP/域名地址；
- 将 "用户名"、"密码 "和 "客户ID "改为ThingsBoard设置中使用的实际值。

#### 单向SSL通信方案

推荐使用的场景!

在这个场景中，RouterOS需要有一个服务器证书导入系统中。

将安装在ThingsBoard上的服务器证书拖放到路由器的 "文件列表 "菜单中：

![](https://help.mikrotik.com/docs/download/attachments/105742352/image-2023-1-24_14-47-41.png?version=1&modificationDate=1674564461251&api=v2)

导入服务器证书:

`/certificate/import file-name=mqttserver.pem passphrase=""`

使用 **SSL单向通信** 和 **访问令牌方案** 时添加一个MQTT broker ，如下所示：

`/iot/mqtt/brokers/add name=tb address=x.x.x.x port=8883 username=access_token ssl=yes`

- 将"address"改为 ThingsBoard 服务器的实际 IP/域名地址；
- 将"username"改为你在ThingsBoard设置中使用的访问令牌；
- 确保"port=8883"（服务器正在监听的MQTT SSL端口）；
- 确保"ssl=yes"。

使用 **SSL单向通信** 和 **MQTT基本方案** 时添加一个MQTT broker ，如下所示：

`/iot/mqtt/brokers/add name=tb address=x.x.x.x port=8883 client-id=clientid password=password username=username ssl=yes`

- 将 "address "改为 ThingsBoard 服务器的实际 IP/域名地址；
- 将 "username"、"password "和 "client-id "改为你在ThingsBoard设置中使用的实际值；
- 确保 "port=8883"（服务器正在监听的MQTT SSL端口）；
- 确保 "ssl=yes"。

#### X.509（双向SSL通信）方案

将证书拖入路由器的 "文件列表 "菜单,服务器证书、客户端证书及其私钥。

逐一导入证书：

```shell
/certificate/import file-name=mqttserver.pem passphrase=""
/certificate/import file-name=cert.pem passphrase=""
/certificate/import file-name=key.pem passphrase=""
```

添加一个MQTT broker:

`/iot/mqtt/brokers/add name=tb address=x.x.x.x port=8883 certificate=cert.pem_0 ssl=yes`

- 将"address"改为 ThingsBoard 服务器的实际 IP/域名地址；
- 将选择的"certificate"改为已经导入的实际客户证书名称；
- 确保"port=8883"（服务器正在监听的MQTT SSL端口）；
- 确保"ssl=yes"。

### MQTT Publish

a) 有一个静态值的快速的MQTT发布测试：

`/iot/mqtt/publish broker="tb" topic="v1/devices/me/telemetry" message="{"cpu/":\"7\"}"`。

b) 为了将相关数据从 RouterOS 发布到 Thingsboard 上，可以使用下面的脚本作为参考。该脚本从RouterOS设备中收集数据（型号名称、序列号、RouterOS版本、当前CPU、已用内存、可用内存和正常运行时间），并将消息（数据）以JSON格式发布给代理：

```shell
# Required packages: iot

################################ Configuration ################################
# Name of an existing MQTT broker that should be used for publishing
:local broker "tb"

# MQTT topic where the message should be published
:local topic "v1/devices/me/telemetry"

#################################### System ###################################
:put ("ParseError: KaTeX parse error: Undefined control sequence: \* at position 1: \̲*̲ Gathering system info...")
:local cpuLoad
/system resource get cpu-load
/systemresourcegetcpu−load

:local freeMemory
/system resource get free-memory
/systemresourcegetfree−memory

:local usedMemory (
/system resource get total-memory
/systemresourcegettotal−memory
- $freeMemory)
:local rosVersion ParseError: KaTeX parse error: Undefined control sequence: \[ at position 45: …e=version \\ \̲[̲/system package…]
:local model
/system routerboard get value-name=model
/systemrouterboardgetvalue−name=model

:local serialNumber
/system routerboard get value-name=serial-number
/systemrouterboardgetvalue−name=serial−number

:local upTime
/system resource get uptime
/systemresourcegetuptime

#################################### MQTT #####################################
:local message \
"{\"model\":\"model\\",\\ \\"sn\\":\\"model
",
"sn
":
"serialNumber\",\
\"ros\":\"rosVersion\\",\\ \\"cpu\\":rosVersion
",
"cpu
":cpuLoad,\
\"umem\":usedMemory,\\ \\"fmem\\":usedMemory,
"fmem
":freeMemory,\
\"uptime\":\"$upTime\"}"

:log info "ParseError: KaTeX parse error: Undefined control sequence: \[ at position 20: …age"; :put ("\̲[̲\*\] Total mess…ParseError: KaTeX parse error: Can't use function '$' in math mode at position 6: :len $̲message bytes")
:put ("ParseError: KaTeX parse error: Undefined control sequence: \* at position 1: \̲*̲ Sending message to MQTT broker...")
/iot mqtt publish broker=broker topic=brokertopic=topic message=$message
:put ("ParseError: KaTeX parse error: Undefined control sequence: \* at position 1: \̲*̲ Done")
```

应考虑2个脚本行。

> :local broker "tb"

行中，应该在引号""内指定broker的名字。

> :local topic "v1/devices/me/telemetry"

行中应该在引号""内指定正确的主题（查看 Thingsboard 的 [文档](https://thingsboard.io/docs/reference/mqtt-api/) 了解需要使用的确切主题）。

脚本的其余配置取决于总体要求。

将上述脚本复制并粘贴到记事本中，然后再重新复制。转到系统>脚本菜单，在那里添加一个新的脚本，并粘贴上面显示的脚本。改名，例如，script1。

要运行这个脚本，可以使用命令行：

`/system script run script1`

## 验证

可以在"最新遥测"部分检查设备的接收发布数据：

![](https://help.mikrotik.com/docs/download/attachments/105742352/image-2023-1-20_14-3-41.png?version=1&modificationDate=1674216212931&api=v2)
