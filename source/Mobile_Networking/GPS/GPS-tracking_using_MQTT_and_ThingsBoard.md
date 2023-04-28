# 简介

许多RouterOS设备有 [GPS](https://help.mikrotik.com/docs/display/ROS/GPS) 支持。允许RouterOS确定其GPS接收器的精确位置。GPS坐标将显示当前位置的纬度和经度值（以及其他参数）。

比如有 [LTAP](https://mikrotik.com/product/ltap)（或任何其他支持GPS的RouterOS设备），希望跟踪它的位置。想让路由器把这些数据发送到服务器上，这些数据将被储存并整合到地图上，因为这样监控起来更方便。在本指南中将展示如何做到这一点。这个方案利用MQTT协议与一个叫做 [ThingsBoard](https://thingsboard.io/) 的平台进行通信。

ThingsBoard有一个云解决方案和不同的本地安装选项（在不同的操作系统上）。

因为已经添加了 [容器](https://help.mikrotik.com/docs/display/ROS/Container) 
 功能，因此也可以在RouterOS中运行该平台。这意味着可以建立该方案，仅在RouterOS设备上→希望跟踪的支持GPS的设备（例如，配备 [LTAP](https://mikrotik.com/product/ltap) 的汽车→作为 **MQTT publishers** 的RouterOS设备），以及在更强大的RouterOS设备内运行的ThingsBoard服务器（如 [CHR](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=18350234) 机器→作为**MQTT broker** 的RouterOS设备）。

如果想选择这个办法（容器），一定要仔细挑选打算用作 "服务器 "的设备，因为这种实现方式内存占用很大（建议设备至少有 **2 GB RAM** 或 **1 GB RAM** ，并且是 **ARM64** 或 **AMD64** 架构）。

# 配置

在本指南中，我们将演示如何配置一个GPS接收器（MQTT发布器）以及如何设置ThingsBoard。

如果想使用容器功能来运行ThingsBoard实例（MQTT代理），请查看 [指南]（https://help.mikrotik.com/docs/pages/viewpage.action?pageId=166920348）。关于ThingsBoard和MQTT配置的一般准则可以在指南中找到 [over here](https://help.mikrotik.com/docs/display/ROS/MQTT+and+ThingsBoard+configuration) 。阅读这两个指南，会有额外的有用信息。

在继续进行之前，确保ThingsBoard已经启动并运行，并且能够访问管理WEB。确认MQTT端口已打开，端口转发正确。

**Package requirement:** `gps, iot`

## ThingsBoard准备

本例将展示 [access-token](https://help.mikrotik.com/docs/display/ROS/MQTT+and+ThingsBoard+configuration#MQTTandThingsBoardconfiguration-Accesstokenscenario.1) 和 [通过access-token进行单向SSL通信](https://help.mikrotik.com/docs/display/ROS/MQTT+and+ThingsBoard+configuration#MQTTandThingsBoardconfiguration-One-waySSLcommunicationscenario.1) 场景，也可以使用其他可用选项。

导航到 **设备** 菜单，通过 **添加新设备** 按钮添加一个新设备→命名并创建它（例如，LTAP）：

![](https://help.mikrotik.com/docs/download/attachments/166920428/image-2023-2-1_12-51-0.png?version=1&modificationDate=1675248641759&api=v2)

点击刚刚添加的设备，进入 **细节** 部分，在 **管理凭证/设备凭证** 设置下生成一个访问令牌：

![](https://help.mikrotik.com/docs/download/attachments/166920428/image-2023-2-1_13-5-15.png?version=1&modificationDate=1675249496173&api=v2)

## MQTT broker配置

如果是本地测试，或者broker可以通过VPN使用，也可以使用非SSL的MQTT：

`/iot/mqtt/brokers/add name=tb address=x.x.x.x port=1883 username=access_token`

其中：

- `name` 是希望的broker的名字，这个名字将在以后的脚本中使用；
- `address` 是broker 的IP地址；
- `port` 是broker 监听的TCP端口，对于非SSL，通常是TCP 1883；
- `username` 是由MQTT broker决定的，在这个例子中是ThingsBoard管理门户中生成的 "访问令牌"。

如果是公共访问（想通过其公共IP地址访问broker 时），**建议使用SSL MQTT**：

```shell
/iot/mqtt/brokers/add name=tb address=x.x.x.x port=8883 username=access_token ssl=yes
```

其中：

- `name` 是给broker 的名字，这个名字将在以后的脚本中使用；
- `address` 是broker 的IP地址；
- `port` 是broker 监听的TCP端口，对于SSL来说，通常是TCP 8883；
- `username` 是由MQTT broker 决定的，在例子中是一个在ThingsBoard管理门户中生成的 "访问令牌"；
- `ssl` 启用SSL MQTT通信。

## MQTT发布

可以通过使用命令来测试MQTT发布的静态消息：

`/iot/mqtt/publish broker="tb" topic="v1/devices/me/telemetry" message="{\"test\":\"123\"}"`

要发布GPS坐标，请导入如下所示的脚本：

```shell
/system/script/add dont-require-permissions=no name=mqttgps owner=admin policy="ftp,re\
    boot,read,write,policy,test,password,sniff,sensitive,romon" \
    source="    ###Configuration###\r\
    \n    #Enter pre-configured broker's name within \"\":\r\
    \n    :local broker \"tb\"\r\
    \n    #Enter the topic name within \"\", per the broker's config\
    uration:\r\
    \n    :local topic \"v1/devices/me/telemetry\"\r\
    \n\r\
    \n    ###Variables####\r\
    \n    :global lat\r\
    \n    :global lon\r\
    \n    :global alt1\r\
    \n    :global alt2\r\
    \n\r\
    \n    ###GPS####\r\
    \n    :put (\"[*] Capturing GPS coordinates...\")\r\
    \n    /system gps monitor once do={\r\
    \n    :set \$lat \$(\"latitude\");\r\
    \n    :set \$lon \$(\"longitude\");\r\
    \n    :set \$alt1 \$(\"altitude\")}\r\
    \n    ###remove \"meters\" from the value because JSON format wi\
    ll not understand it###\r\
    \n    :set \$alt2 [:pick \$alt1 0 [find \$alt1 \" m\"]]\r\
    \n\r\
    \n    :local message \\\r\
    \n    \"{\\\"latitude\\\":\$lat,\\\r\
    \n    \\\"longitude\\\":\$lon,\\\r\
    \n    \\\"altitude\\\":\$alt2}\"\r\
    \n\r\
    \n    ###MQTT###\r\
    \n    :if (\$lat != \"none\") do={\\\r\
    \n    :put (\"[*] Sending message to MQTT broker...\");\r\
    \n    /iot mqtt publish broker=\$broker topic=\$topic message=\$\
    message} else={:put (\"[*] Lattitude=none, not posting anything!\
    \");:log info \"Latitude=none, not posting anything!\"}"
```

简而言之，该脚本捕捉GPS信息，特别是纬度、经度和海拔值。然后从这些信息中构造出一个JSON信息。如果在脚本启动的时候，纬度值不等于 "无"（等于任何实际的数值），那就会通过MQTT将JSON消息发送到名为 **tb** 的broker 那里。如果GPS数据不能被捕获→"纬度 "被识别为 "无"→脚本只记录没有任何东西被捕获，而不做其他事情。

这只是一个非常基本的例子。可以根据自己的需要修改脚本并添加自己的 "if"（也许是在没有GPS信号的情况下发送电子邮件通知）和额外的参数（任何其他的RouterOS捕获值，如固件版本）。

用命令运行脚本：

```shell
/system/script/run mqttgps
[*] Capturing GPS coordinates...
        date-and-time: feb/01/2023 10:39:37
             latitude: 56.969862
            longitude: 24.162425
             altitude: 31.799999 m
                speed: 1.000080 km/h
  destination-bearing: none
         true-bearing: 153.089996 deg. True
     magnetic-bearing: 0.000000 deg. Mag
                valid: yes
           satellites: 6
          fix-quality: 1
  horizontal-dilution: 1.42
             data-age: 0s
[*] Sending message to MQTT broker...
```

要使这个过程自动化，可以添加一个 [时间表](https://help.mikrotik.com/docs/display/ROS/Scheduler) 来运行脚本，如每30秒一次：

```shell
/system/scheduler/add name=mqttgpsscheduler interval=30s on-event="/system/script/run mqttgps"
```

# 结果验证

进入创建的设备下的 "最新遥测 "部分，确认数据已经发布：

![](https://help.mikrotik.com/docs/download/attachments/166920428/image-2023-2-1_13-15-24.png?version=1&modificationDate=1675250105501&api=v2)

# 使用地图进行数据可视化

ThingsBoard允许使用 [Widgets](https://thingsboard.io/docs/user-guide/ui/widget-library/) 来创建具有视觉吸引力的仪表盘。在案例中想跟踪LTAP GPS坐标，所以要添加一个地图部件。

选择纬度和经度值并点击 **显示在部件上** 按钮：

![](https://help.mikrotik.com/docs/download/attachments/166920428/image-2023-2-1_13-20-36.png?version=1&modificationDate=1675250417648&api=v2)

找到 **地图** 包，点击 **添加到仪表板**：

![](https://help.mikrotik.com/docs/download/attachments/166920428/image-2023-2-1_13-21-49.png?version=1&modificationDate=1675250490676&api=v2)

选择一个现有的仪表板或创建一个新的仪表板，并命名：

![](https://help.mikrotik.com/docs/download/attachments/166920428/image-2023-2-1_13-23-9.png?version=1&modificationDate=1675250570740&api=v2)

通过调度程序或手动运行脚本并检查结果：

![](https://help.mikrotik.com/docs/download/attachments/166920428/image-2023-2-1_13-27-0.png?version=1&modificationDate=1675250801888&api=v2)

现在可以把它安装在一个移动的目标上并跟踪它的位置：

![](https://help.mikrotik.com/docs/download/attachments/166920428/image-2023-2-2_15-12-5.png?version=1&modificationDate=1675343523993&api=v2)