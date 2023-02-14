# 概述

**Sub-menu:** `/system ups`  
**Standards:** `[APC Smart Protocol](http://www.exploits.org/nut/library/protocols/apcsmart.html)`

UPS监控功能支持串行RS232或USB连接的 "智能 "APC UPS设备。UPS监控服务不包含在默认的软件包中，需要下载并手动安装ups.npk软件包。这个功能使网络管理员能够监控UPS，路由器可以 "优雅地 "处理任何断电，不会损坏路由器。这个功能的基本目的是确保路由器在长时间停电后能重新上线。要做到这一点，路由器将监测UPS，并在市电中断和UPS电池剩余电量少于10%时，将自己设置为休眠模式。然后，路由器将继续监测UPS（在休眠模式下），然后在市电恢复时重新启动。如果UPS电池电量耗尽，路由器失去所有电源，当 "市电 "恢复时，路由器将恢复运行。

MikroTik RouterOS上的UPS监控功能支持

- 电源和电池故障时休眠和安全重启
- UPS电池测试和运行时间校准测试
- 监测UPS支持的 "智能 "模式状态信息
- 记录电源变化

## 连接UPS单元

串行接口的APC UPS（BackUPS Pro或SmartUPS）需要一根特殊的串行电缆（除非用USB连接）。如果UPS没有附带电缆，可以向APC订购，也可以 "自行 "制作。请使用以下图示:

| Router Side (DB9f) | Signal  | Direction | UPS Side (DB9m) |
| ------------------ | ------- | --------- | --------------- |
| 2                  | Receive | IN        | 2               |
| 3                  | Send    | OUT       | 1               |
| 5                  | Ground  |           | 4               |
| 7                  | CTS     | IN        | 6               |

如果使用RouterBOARD设备，请确保 "RouterBOOT设置键"设置为 _Delete_ 而不是默认的 _Any key_。这是为了避免在RouterBOARD启动过程中UPS设备向串口发送一些数据而意外打开设置菜单。可以在启动时在RouterBOOT选项中完成，或者通过Winbox中的RouterBoard设置完成。

```shell
Select key which will enter setup on boot:
 * 1 - any key
   2 - <Delete> key only
your choice:
```

## 常规属性

| 属性                                                                                        | 说明                                                                                                                                                                                                                                                      |
| ------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **alarm-setting** (_delayed \| immediate   \| low-battery \| none_; Default: **immediate**) | UPS声音报警设置：<br>- delayed - 电池事件的报警延迟<br>- immediate -发生电池爆炸事件后立即报警<br>- low-battery - 只在电池电量不足时报警<br>- none - 不报警                                                                                               |
| **check-capabilities** (_yes \| no_; Default: **yes**)                                      | 是否在读取信息前检查UPS的能力。禁用可以解决某些UPS型号的兼容性问题。(适用于RouterOS第6版，从v6.17开始实施)                                                                                                                                                |
| **min-runtime** (_time_; Default: **never**)                                                | 最小的剩余运行时间。在 "产生 "故障后，路由器将监测运行时间剩余值。当该值达到最小运行时间值时，路由器将进入休眠模式。 <br>- never - 当 "电池电量低 "信号表明电池电量低于10%时，路由器将进入休眠模式。<br>- 0s - 只要电池有足够的电压，路由器就会继续工作。 |
| **offline-time** (_time_; Default: **0s**)                                                  | 用电池工作多长时间。路由器等待这个时间，然后进入休眠模式，直到UPS报告 "市电 "恢复。<br>- 0s - 路由器根据最小运行时间的设置进入休眠模式。这样路由器将等待直到UPS报告电池电量低于10%。                                                                      |
| **port** (_string_; Default: )                                                              | 路由器通信端口                                                                                                                                                                                                                                            |
  
只读属性:

| 属性                                    | 说明                                                                                                                                                                            |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **load** (_percent_)                    | UPS的输出负载占全部额定负载的百分比（瓦特）。此项测量的典型精度是最大105%的±3%。                                                                                                |
| **manufacture-date** (_string_)         | UPS制造日期，格式为 "mm/dd/yy"（月、日、年）。                                                                                                                                  |
| **model** (_string_)                    | 小于32个ASCII字符的字符串，由UPS的型号名称组成（UPS本身前面的字）。                                                                                                             |
| **nominal-battery-voltage** (_integer_) | UPS标称电池电压（这不是UPS的实际电池电压）。                                                                                                                                    |
| **offline-after** (_time_)              | 路由器何时下线？                                                                                                                                                                |
| **serial** (_string_)                   | 至少8个字符的字符串，代表UPS在工厂设置的序列号。较新的SmartUPS型号有12个字符的序列号。                                                                                          |
| **version** (_string_)                  | UPS版本，由三个字组成。SKU号码、固件修订版、国家代码。国家代码可以是以下之一。 <br>- I - 220/230/240 Vac<br>- D - 115/120 Vac<br>- A - 100 Vac<br>- M - 208 Vac<br>- J - 200Vac |

**注意：** 为了启用UPS监控，串口要可用。

### 例子

启用串行端口1的UPS监控:

```shell
[admin@MikroTik] system ups> add port=serial1 disabled=no
[admin@MikroTik] system ups> print
Flags: X - disabled, I - invalid
 0    name="ups" port=serial1 offline-time=5m min-runtime=5m
      alarm-setting=immediate model="SMART-UPS 1000" version="60.11.I"
      serial="QS0030311640" manufacture-date="07/18/00"
      nominal-battery-voltage=24V
[admin@MikroTik] system ups>

```

## 运行时校准

**Command:** `/system ups rtc <id>`

rtc命令使UPS开始运行时间校准，直到电池降到满载的25%以下。该命令对返回的运行时间值进行校准。

**注意：** 只有当电池容量达到100%时才开始测试。

## 监控

**Command:** `/system ups monitor <id>`

| 属性                                          | 说明                                                                                                                      |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| **battery-charge** ()                         | UPS的剩余容量占完全充电状态的百分比                                                                                       |
| **battery-voltage** ()                        | UPS的当前电池电压。测量的典型精度为最大值的±5%（取决于UPS的额定电池电压）                                                 |
| **frequency** ()                              | 在线工作时，UPS的内部工作频率与线路同步，在额定50或60赫兹的3赫兹范围内变化。测量典型精度为63Hz满刻度值的±1%。             |
| **line-voltage** ()                           | 市电电压                                                                                                                  |
| **load** ()                                   | UPS的输出负载占额定负载的百分比，单位是瓦特。测量典型精度是最大105%的±3%。                                                |
| **low-battery** (_yes                 \| no_) | 只在UPS报告此状态时显示                                                                                                   |
| **on-battery** (_yes                  \| no_) | UPS电池是否在供电                                                                                                         |
| **on-line** (_yes                     \| no_) | 是否由市电供电                                                                                                            |
| **output-voltage** ()                         | UPS输出电压                                                                                                               |
| **overloaded-output** (_yes           \| no_) | UPS报告状态时才显示                                                                                                       |
| **replace-battery** (_yes             \| no_) | UPS报告状态时才显示                                                                                                       |
| **runtime-calibration-running** (_yes \| no_) | UPS报告状态时才显示                                                                                                       |
| **runtime-left** (_time_)                     | UPS的估计剩余时间（分钟）。可以查询UPS的在线、旁路或电池工作模式下的运行情况。UPS的剩余时间基于可用的电池容量和输出负载。 |
| **smart-boost-mode** (_yes            \| no_) | UPS报告状态时才显示                                                                                                       |
| **smart-ssdd-mode** ()                        | UPS报告状态时才显示                                                                                                       |
| **transfer-cause** (_string_)                 | 最近一次转入电池工作的原因（仅在设备处于电池状态时显示）。                                                                |

### 例子

当使用市电时:

```shell
[admin@MikroTik] system ups> monitor 0
          on-line: yes
       on-battery: no
      RTC-running: no
     runtime-left: 20m
   battery-charge: 100%
  battery-voltage: 27V
     line-voltage: 226V
   output-voltage: 226V
             load: 45%
      temperature: 39C
        frequency: 50Hz
  replace-battery: no
      smart-boost: no
       smart-trim: no
         overload: no
      low-battery: no

[admin@MikroTik] system ups>

```
  
电池供电时:

```shell
[admin@MikroTik] system ups> monitor 0
          on-line: no
       on-battery: yes
   transfer-cause: "Line voltage notch or spike"
      RTC-running: no
     runtime-left: 19m
    offline-after: 4m46s
   battery-charge: 94%
  battery-voltage: 24V
     line-voltage: 0V
   output-voltage: 228V
             load: 42%
      temperature: 39C
        frequency: 50Hz
  replace-battery: no
      smart-boost: no
       smart-trim: no
         overload: no
      low-battery: no

      [admin@MikroTik] system ups>
```
