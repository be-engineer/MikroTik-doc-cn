# General Properties

每个带有支持LTE调制解调器的miniPCI-e插槽的RouterBOARD可以通过安装 **R11e-LoRa8** 或 **R11e-LoRa9** 卡作为LoRaWAN网关使用。为了与Lora一起工作，需要安装Lora软件包。你可以在 [下载](https://mikrotik.com/download) 页面的额外软件包档案中找到适合你设备架构的软件包。

**注**： RouterOS不支持第三方LoRaWAN网关卡。

# 属性

**Sub-menu:** /lora

| 属性                                                                                                                                            | 说明                                                                                                                                                                              |
| ----------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **antenna-gain** (_integer [-128..127]_; Default: **0**)                                                                                        | 天线增益的dBi值                                                                                                                                                                   |
| **channel-plan** (_as-923 \| au-915\| custom\| eu-868\| in-865 \| kr-920 \| ru-864 \| ru-864-mid \| us-915-1 \| us-915-2_; Default: **eu-868**) | 各地区的频率计划。                                                                                                                                                                |
| **disabled** (_yes\| no_; Default: **yes**)                                                                                                     | LoRaWAN网关是否被禁用。                                                                                                                                                           |
| **forward** (_crc-disabled \| crc-error\| crc-valid_; Default: **crc-valid,crc-error**)                                                         | 定义什么样的数据包应该被转发到网络服务器： <br>- crc-disabled - 转发没有检查CRC码的数据包<br>- crc-error - 转发有错误CRC码的数据包<br>- crc-valid - 转发具有正确CRC的有效数据包。 |
| **lbt-enabled** (_yes \| no_; Default: **no**)                                                                                                  | 网关是否应使用LBT（先听后说）协议。                                                                                                                                               |
| **listen-time** (_integer [0us..4294967295us]_; Default: **5000us**)                                                                            | TX前跟踪RSSI的时间（微秒）（当 lbt-enabled=yes时使用）。                                                                                                                          |
| **name** (_string_; Default: )                                                                                                                  | LoRaWAN网关的名称。                                                                                                                                                               |
| **network** (_private \| public_; Default: **public**)                                                                                          | 是否使用（network=private）或不使用（network=public）同步词。                                                                                                                     |
| **rssi-threshold** (_integer [-32,768 ... 32,767]_; Default: **-65dB**)                                                                         | RSSI值决定转发者是否可以使用特定的通道进行通话。如果RSSI值低于 **rssi-threshold**，则可以使用通道（当 **lbt-enabled=yes** 时使用）。                                              |
| **servers** (_list of string_; Default: )                                                                                                       | /lora servers中的一个或多个服务器名称。                                                                                                                                           |
| **src-address** (_IP_; Default: )                                                                                                               | 必要时指定上行数据包的源地址（地址应与RB上配置的地址一致）。                                                                                                                      |
| **spoof-gps** (_string_; Default: )                                                                                                             | 设置自定义的GPS位置：<br>-   Latitude [-90..90]<br>-   Longitude [-180..180]<br>-   Altitude(**m**) [-2147483648..2147483647]                                                     |

  

# 频道

**Sub-menu:** `/lora channels`

| 属性                                                                                                                         | 说明                                                                                                                                                 |
| ---------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| **bandwidth** (_7.8_kHz \| 15.6_kHz \| 31.2_kHz\| 62.5_kHz \| 125_kHz \| 250_kHz          \| 500_kHz_; Default: **125_kHz**) | Bandwidth of specific channel, predefined when any of channel-plan preset is used, but could be manually changed when channel-plan is set to custom. |
| **disabled** (_yes\| no_; Default: **no**)                                                                                   | 特定通道是否被禁用。                                                                                                                                 |
| **freq-off** (_integer_ [-400000...400000]; Default: )                                                                       | 通道频率与无线电中心频率的偏移，它可以调整通道频率，使通道不会重叠。                                                                                 |
| **radio** (_radio0 \| radio1_; Default: )                                                                                    | 定义哪个电台使用所选频道。                                                                                                                           |
| **spread-factor** (_SF7 \| SF8 \| SF9 \| SF10 \| SF11 \| SF12_; Default: )                                                   | type=LoRa的频道的传播因子。较低的扩展因子意味着较高的数据速率。                                                                                      |
  

# 服务器

**Sub-menu:** `/lora servers`

有两个预定义的服务器可以使用（需要建立一个 [The Things Network](https://thethingsnetwork.org) 账户才能使用）。

```shell
[admin@MikroTik] > lora servers print
 # NAME             UP-PORT DOWN-PORT ADDRESS                                                                                                                                          
 0 TTN-EU              1700      1700 eu.mikrotik.thethings.industries                                                                                                                 
 1 TTN-US              1700      1700 us.mikrotik.thethings.industries
```

`Custom servers can be added as well. Data forwarding to multiple servers can work simultaneously if the first server does not change "DevAdress" part of the packet and under the condition that all servers are able to decode the packet.   `

| 属性                                                 | 说明                                                                                                                                                                  |
| ---------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **address** (_domain name or IP address_; Default: ) | 定义LoRaWAN网络服务器地址。                                                                                                                                           |
| **down-port** (_integer [0..65535]_; Default: )      | 定义与LoRaWAN网络服务器进行下行链路通信的端口（从服务器到节点）。大多数已知的开源服务器使用1700端口作为默认端口，但如果在同一台机器上配置了多个服务器，它可能会改变。 |
| **name** (_string_; Default: )                       | 定义服务器名称。                                                                                                                                                      |
| **up-port** (_integer [0..65535]_; Default: )        | 定义与LoRaWAN网络服务器的上行链路通信（从节点到服务器）的端口。大多数已知的开源服务器使用1700端口作为默认端口，但如果在同一台机器上配置了多个服务器，可能会不同。     |