# 概述

**Package requirement:** `gps`  
**Sub-menu:** `/system gps`  
**Standards:** `GPS, NMEA 0183, [Simple Text Output Protocol](http://www8.garmin.com/support/text_out.html)`

全球定位系统（GPS）用于确定GPS接收器的精确位置。 

## 配置属性

| 属性                                                                   | 说明                                                                     |
| ---------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| **channel** (_integer [0..4294967295]_; Default: **0*)                 | 设备使用的通道。                                                         |
| **coordinate-format** (_dd \| dms \| ddmm_; Default: **no*)            | 使用哪种坐标格式，"十进制度数"、"度数分钟秒数 "或 "NMEA格式DDDMM.MM[MM]" |
| **enabled** (_yes \| no_; Default: **no**)                             | 是否启用了GPS？                                                          |
| **gps-antenna-select** (_external \| internal_; Default: **internal**) | 取决于型号。如果设备安装了内部天线，可以选择内部天线。                   |
| **init-channel** (_integer [0..4294967295]_; Default: )                | 用于执行init-string的通道。                                              |
| **init-string** (_string_; Default: )                                  | GPS初始化的AT初始字符串。                                                |
| **port** (_string_; Default: )                                         | 连接GPS接收机的USB/串口名称。                                            |
| **set-system-time** (_yes \| no_; Default: **no**)                     | 是否将路由器的日期和时间设置为GPS接收的日期和时间。                      |

# 状态监控

**Command:** `/system gps monitor`

该命令用于监测从GPS接收器接收的数据。

**参数：**

从7.1rc3固件版本开始，增加了一个新的参数，叫做 "data-age"（单位：秒）。该参数显示设备收到最后一条NMEA信息后所经过的时间。

| 属性                                       | 说明                                     |
| ------------------------------------------ | ---------------------------------------- |
| **date-and-time** (_date_)                 | 从GPS收到的日期和时间                    |
| **latitude** (_none \| string_)            | 纬度以DM(Degrees Minute decimal)格式表示 |
| **longitude** (_none \| string_)           | 经度以DM(度分小数)格式表示               |
| **altitude** (_none \| string_)            | 基于GPS数据的海拔高度                    |
| **speed** (_none \| string_)               | 当前GPS设备的移动速度                    |
| **destination-bearing** (_none \| string_) | GPS移动的方向                            |
| **true-bearing** (_none \| string_)        | GPS移动的方向                            |
| **magnetic-bearing** (_none \| string_)    | GPS移动的方向                            |
| **valid** (_yes \| no_)                    |                                          |
| **satellites** (_integer_)                 | 设备看到的卫星数量                       |
| **fix-quality** (_integer_)                | 信号的质量                               |
| **horizontal-dilution** (_integer_)        | 水平稀释精度(HDOP)                       |
| **data-age** (_integer_)                   | 设备收到最后一次NMEA信息后的时间         |

# 基本实例

检查端口使用情况，因为只有一个实例可以同时使用串行端口：

```shell
[admin@MikroTik] /port print
Flags: I - inactive
 #   DEVICE NAME                     CHANNELS USED-BY                   BAUD-RATE
 0          serial0                         1 Serial Console            auto
```

如果有一个端口被控制台使用，请从控制台菜单中释放它：

```shell
[admin@MikroTik] > /system console print
Flags: X - disabled, U - used, F - free
 #   PORT                                                                       TERM                                                                    
 0 U serial0                                                                    vt102
 
[admin@MikroTik] > /system console disable 0
```

Adjust port settings specifically for your device (leave "auto" for LtAP mini):

```shell
[admin@MikroTik] /port> set 0 baud-rate=4800 parity=odd
[admin@MikroTik] /port> print detail
Flags: I - inactive
 0   name="usb1" used-by="" channels=1 baud-rate=4800 data-bits=8 parity=odd stop-bits=1 flow-control=none
```

启用GPS:

```shell
[admin@MikroTik] /system gps> set enable=yes port=usb1
[admin@MikroTik] /system gps> print
          enabled: yes
             port: usb1
          channel: 0
     init-channel: 0
      init-string:
  set-system-time: no
```

监控状态:

```shell
[admin@MikroTik] /system gps> monitor
        date-and-time: sep/07/2021 08:26:26
             latitude: 56.969689
            longitude: 24.162471
             altitude: 25.799999m
                speed: 0.759320 km/h
  destination-bearing: none
         true-bearing: 185.500000 deg. True
     magnetic-bearing: 0.000000 deg. Mag
                valid: yes
           satellites: 6
          fix-quality: 1
  horizontal-dilution: 1.3
```

 **LtAP** 的端口和GPS设置

`/port set serial1 baud-rate=115200`

`/system gps set port=serial1 channel=0 enabled=yes`

我们有一篇关于实时GPS跟踪的深度文章，使用脚本和网络服务器： [Manual:GPS-tracking](https://wiki.mikrotik.com/wiki/Manual:GPS-tracking"Manual:GPS-tracking")。

# 故障排除

注意，有时为了使GPS模块在RouterOS下被识别，需要改变"/port "菜单中的波特率设置。

[LtAP mini](https://mikrotik.com/product/ltap_mini) 内置了一个低增益的GPS天线，为了获得更好的体验，建议用一个额外的 [外部天线](https://mikrotik.com/product/acgpsa)。

在GPS菜单下切换内部和外部天线：

`[admin@MikroTik] > /system gps set gps-antenna-select=external`

在一些支持GPS的调制解调器上，要发送多个init命令来进行连续的GPS监控，例如，华为卡需要发送 "AT^WPDST=1,AT^WPDGP "init字符串来获得连续监控。