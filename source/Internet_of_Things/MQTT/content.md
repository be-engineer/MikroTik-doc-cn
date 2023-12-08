# 概述

MQTT是一个开放的OASIS和ISO标准的轻量级、发布-订阅网络协议，在设备之间传输消息。一个典型的MQTT通信拓扑结构由以下部分组成：

- MQTT发布者→向服务器发送信息的设备；
- MQTT代理→存储数据的服务器；
- MQTT用户→读取/监控服务器上发布的数据的设备。

目前，RouterOS可以作为MQTT发布者，也可以通过 [container](https://help.mikrotik.com/docs/display/ROS/Container) 功能运行一个MQTT broker 。

# 配置

**Sub-menu:** `/iot mqtt`

**注**：iot包是必需的。

IoT软件包在RouterOS 6.48.3版本中可用。可以从 [下载页面](https://mikrotik.com/download) 的"额外包"下获得。

可以在下面找到更多关于MQTT发布场景的应用实例：

a) [MQTT/HTTPS example with AWS cloud platform](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=63045633)

b) [MQTT example with Azure cloud platform](https://help.mikrotik.com/docs/display/UM/MQTT+and+Azure+configuration)

c) [MQTT and ThingsBoard configuration](https://help.mikrotik.com/docs/display/ROS/MQTT+and+ThingsBoard+configuration)

上面的例子中显示的设置适用于任何RouterOS设备。唯一需要记住的是，AWS和Azure的例子展示了蓝牙有效载荷中MQTT消息的脚本，目前，只有 [KNOT](https://mikrotik.com/product/knot) 支持蓝牙。对于KNOT以外的RouterOS设备，要根据要求改变脚本（例如，可以使用本指南的基本脚本）。

## Broker

要添加一个新的Broker，运行以下命令：

`[admin@device] /iot mqtt brokers add`。

可配置的属性如下：

| 属性                                                    | 说明                                            |
| ------------------------------------------------------- | ----------------------------------------------- |
| **address** (_IP \| hostname_; Default: )               | broker 的IP地址或主机名。                       |
| **证书** (_string_; Default: )                          | 用于SSL连接的证书。                             |
| **client-id** (_string_; Default: )                     | 用于连接的唯一ID。broker 使用这个ID来识别客户。 |
| **name** (_string_; Default: )                          | broker 的描述性名称。                           |
| **password** (_string_; Default: )                      | broker 的密码(如果broker 要求的话)              |
| **port** (_integer:_0..4294967295__; Default: **1883**) | broker 使用的网络端口。                         |
| **ssl** (_yes \| no_; Default: **no**)                  | 安全套接字层配置                                |
| **username** (_string_; Default: )                      | broker 的用户名(如果broker需要)                 |

## Publish

| 属性                                                | 说明                                                                   |
| --------------------------------------------------- | ---------------------------------------------------------------------- |
| **broker** (_string_; Default: )                    | 选择要发布信息的broker。                                               |
| **message** (_string_; Default: )                   | 希望发布给broker的信息。                                               |
| **qos** (_integer:_0..4294967295__; Default: **0**) | 服务质量参数，由broker定义。                                           |
| **retain** (_yes\| no_; Default: **no**)            | 如果没有人订阅该主题，是保留该消息还是将其丢弃。这个参数由broker定义。 |
| **topic** (_string_; Default: )                     | 主题，由broker定义。                                                   |

一个MQTT发布的例子：

`[admin@device] /iot mqtt> publish broker=AWS topic=my/test/topic message="{\"temperature\":15}"`

在这种情况下，**AWS** 是在broker部分配置的broker名称，**my/test/topic** 是一个主题（因为它是在服务器端/broker配置的），**"{\"temperature\":15}"** 是希望发布的消息（在这个例子中为JSON格式）。Retain和QoS参数是可选的--两者都由broker定义。

在这种情况下的broker是 [AWS](https://aws.amazon.com/iot/)。

为了看到显示的消息，需要事先订阅该主题（例子，**my/test/topic**）。

一旦订阅了该主题，就可以发布消息了。AWS（或任何其他broker）应该显示该消息：

![](https://help.mikrotik.com/docs/download/attachments/46759978/image2021-5-26_8-34-1.png?version=1&modificationDate=1622007236280&api=v2)

  

可以使用脚本使该过程自动化。例如，可以运行一个这样的脚本：

```shell
# Required packages: iot

################################ Configuration ################################
# Name of an existing MQTT broker that should be used for publishing
:local broker "AWS"

# MQTT topic where the message should be published
:local topic "my/test/topic"

#################################### System ###################################
:put ("[*] Gathering system info...")
:local cpuLoad [/system resource get cpu-load]
:local freeMemory [/system resource get free-memory]
:local usedMemory ([/system resource get total-memory] - $freeMemory)
:local rosVersion [/system package get value-name=version \
    [/system package find where name ~ "^routeros"]]
:local model [/system routerboard get value-name=model]
:local serialNumber [/system routerboard get value-name=serial-number]
:local upTime [/system resource get uptime]

#################################### MQTT #####################################
:local message \
    "{\"model\":\"$model\",\
                \"sn\":\"$serialNumber\",\
                \"ros\":\"$rosVersion\",\
                \"cpu\":$cpuLoad,\
                \"umem\":$usedMemory,\
                \"fmem\":$freeMemory,\
                \"uptime\":\"$upTime\"}"

:log info "$message";
:put ("[*] Total message size: $[:len $message] bytes")
:put ("[*] Sending message to MQTT broker...")
/iot mqtt publish broker=$broker topic=$topic message=$message
:put ("[*] Done")
```

该脚本从RouterOS设备上收集数据（型号名称、序列号、RouterOS版本、当前CPU、已用内存、可用内存和正常运行时间），并将消息（数据）以JSON格式发布给broker ：

![](https://help.mikrotik.com/docs/download/attachments/46759978/image2021-5-26_9-33-13.png?version=1&modificationDate=1622010788772&api=v2)

不要忘记根据设置修改脚本的 "配置 "部分。
