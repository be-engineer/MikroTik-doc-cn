# 概述

**Sub-menu:** `/system leds`

RouterOS允许以用户希望的方式配置每个LED的动作。可以把LED灯配置为显示无线强度，在接口流量活动中闪烁LED灯，以及其他选项。

例如，Groove的默认LED配置

```shell
[admin@MikroTik] /system leds> print
Flags: X - disabled
# TYPE INTERFACE LEDS
0 wireless-signal-strength led1
led2
led3
led4
led5
1 interface-activity ether1 user-led
```

RB Groove用五个LED灯来显示无线强度，一个LED灯用于以太网活动监测。
## 属性说明

| 属性                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **disabled** (_yes                                             \| no_; Default: **no**)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | 是否禁用                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| **interface** (_string_; Default: )                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | 用于引导状态的接口名称。仅当 **类型** 是特定接口时可用。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| **modem-signal-treshold** (_integer [-113..-51]_; Default: )                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | 如果类型是**调制解调器-信号**则适用。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| **leds** (_list of leds_; Default: )                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | 用于状态报告的LED名称列表。例如，无线信号强度需要一个以上的LED。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| **type** (_align-down                                                                   \| align-left                                                                                                        \| align-right \| align-up \| ap-cap \| fan-fault \| flash-access \| interface-activity \| interface-receive \| interface-speed \| interface-speed-1G \| interface-speed-25G \| interface-status \| interface-transmit \| modem-signal \| modem-technology \| off \| on \| poe-fault \| poe-out \| wireless-signal-strength \| wireless-status_; Default: ) | 状态类型：<br>- align-down - 如果w60g设备要向下对齐以获得最佳的信号质量，则点亮led。<br>- align-left - 如果w60g设备要向左对齐，则点亮LED灯<br>- align-right - 如果w60g设备要向右对齐，则点亮该指示灯<br>- align-up - 如果w60g设备要向上对齐，则点亮led。<br>- ap-cap - CAPsMAN初始化时闪烁，连接后稳定。<br>- fan-fault -当任何一个设备控制的风扇停止工作时点亮led<br>- flash-access - 当flash访问时，led闪烁。<br>- interface-activity - 在接口（流量）活动时闪烁LED灯<br>- interface-receive - 当接口收到流量时，指示灯闪烁。<br>- interface-speed - 当接口工作在10Gbit速率时，指示灯亮。<br>- interface-speed-1G - 当接口以1Gbit速率工作时，指示灯亮<br>- interface-speed-25G - 当接口以25Gbit速率工作时，指示灯亮。<br>- interface-speed-100G - 当接口以100Gbit的速率工作时，指示灯亮。<br>- interface-status - 在接口状态改变时亮起LED灯<br>- interface-transmit - 在接口传输流量时闪烁指示灯<br>- modem-signal - 在3G调制解调器信号（USB或miniPCIe）上闪烁灯。<br>- modem-technology - 按调制解调器技术世代的顺序打开LED。GSM；3G；LTE；只有当LTE处于活动状态时，单个LED才会亮。<br>- off - 关闭LED灯<br>- on - 打开LED灯<br>- Poe-fault - 当PoE输出预算接近最大支持限度时，点亮LED灯。<br>- poe-out - 当接口PoE输出打开时点亮指示灯<br>- wireless-signal-strength - 点亮显示无线信号的LED（需要一个以上的LED）。<br>- wireless-status - 无线状态改变时点亮LED。 |

## LED设置

全局设置存储在LED设置菜单中。

**Sub-menu:** `/system leds setting`

| 属性                                                                                  | 说明                                |
| ------------------------------------------------------------------------------------- | ----------------------------------- |
| **all-leds-off** (_after-1h \| after-1min \| immediate \| never_; Default: **never**) | 路由器的所有LED是否关闭以及何时关闭 |
  
所列设备支持关闭LED，但是，由于设备设计因素，一些LED仍然无法关闭。

### 室内设备

| RouterBoard                                                                             | LED 说明                                             |
| --------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| **CRS305-1G-4S+**                                                                       | Turns off all LEDs except Ethernet LED and Power LED |
| **CRS309-1G-8S+**                                                                       | Turns off all LEDs except Ethernet LEDs              |
| **RB5009UG+S+IN**                                                                       | Turns off all LEDs                                   |
| **RB760iGS (hEX S)**                                                                    | Turns off Power LED and SFP LED                      |
| **RB924i-2nD-BT5&BG77; RB924iR-2nD-BT5&BG77 (KNOT series)**                             | Turns off all LEDs                                   |
| **RB951Ui-2HnD**                                                                        | Turns off all LEDs except Power LED                  |
| **RB951Ui-2nD (hAP); RB952Ui-5ac2nD (hAP ac lite); RB952Ui-5ac2nD-TC (hAP ac lite TC)** | Turns off all LEDs except Power LED                  |
| **RB962UiGS-5HacT2HnT (hAP ac)**                                                        | Turns off all LEDs except Port5 PoE LED              |
| **RBcAP2n; RBcAP2nD (cAP)**                                                             | Turns off all LEDs                                   |
| **RBcAPGi-5acD2nD (cAP ac); RBcAPGi-5acD2nD-XL (cAP XL ac)**                            | Turns off all LEDs                                   |
| **RBD25G/RB25GR-5HPacQD2HPnD (Audience)**                                               | Turns off all LEDs except Ethernet LEDs              |
| **RBD52G-5HacD2HnD-TC (hAP ac^2)**                                                      | Turns off all LEDs                                   |
| **RBD53iG-5HacD2HnD (hAP ac^3)**                                                        | Turns off all LEDs                                   |
| **RBD53G-5HacD2HnD-TC (Chateau series)**                                                | Turns off all LEDs                                   |
| **RBwsAP5Hac2nD (wsAP ac lite)**                                                        | Turns off all LEDs                                   |
| **C52iG-5HaxD2HaxD-TC (hAP ax^2)**                                                      | Turns off all LEDs except Ethernet LEDs              |
| **C53UiG+5HPaxD2HPaxD (hAP)**                                                           | Turns off all LEDs                                   |
| **S53UG+5HaxD2HaxD-TC (Chateau ax series)**                                             | Turns off all LEDs                                   |

### 无线系统

| RouterBoard                                                                                                             | LED 说明                                |
| ----------------------------------------------------------------------------------------------------------------------- | --------------------------------------- |
| **CubeG-5ac60ay (Cube 60Pro ac); CubeG-5ac60ay-SA (CubeSA 60Pro ac)**                                                   | Turns off all LEDs                      |
| **CubeG-5ac60ad (Cube 60G ac)**                                                                                         | Turns off all LEDs                      |
| **RB912R-2nD-LTm (ltAP mini / ltAP mini LTE kit)**                                                                      | Turns off all LEDs                      |
| **RB912UAG-6HPnD (BaseBox 6)**                                                                                          | Turns off all LEDs                      |
| **RBD23UGS-5HPacD2HnD (NetMetal ac^2)**                                                                                 | Turns off all LEDs                      |
| **RBLDF-2nD (LDF 2); RBLDF-5nD (LDF 5); RBLHGR**                                                                        | Turns off all LEDs                      |
| **RBLDFG-5acD (LDF 5 ac)**                                                                                              | Turns off all LEDs except Ethernet LED  |
| **RBLHG2nD (LHG 2); RBLHG2nD-XL (LHG XL 2)**                                                                            | Turns off all LEDs                      |
| **RBLHG5nD (LHG 5); RBLHG5HPnD (LHG HP5); RBLHG5HPnD-XL (LHG XL HP5)**                                                  | Turns off all LEDs                      |
| **RBLHGG-5acD (LHG 5 ac); RBLHGG-5acD-XL (LHG XL 5 ac); RBLHGG-5HPacD2HPnD (LHG XL 52 ac); RBSXTsqG-5acD (SXTsq 5 ac)** | Turns off all LEDs except Ethernet LED  |
| **RBLHGG-60ad (Wireless Wire Dish)**                                                                                    | Turns off all LEDs                      |
| **LHGGM&EG18-EA (LHG LTE18 kit)**                                                                                       | Turns off all LEDs                      |
| **RBLtAP-2HnD (LtAP)**                                                                                                  | Turns off all LEDs except Ethernet LEDs |
| **RBSXTsq-60ad (SXTsq Lite60); RBCube-60ad (Cube Lite60)**                                                              | Turns off all LEDs                      |
| **RBwAPG-60ad (Wireless Wire)**                                                                                         | Turns off all LEDs                      |
| **RBwAPGR-5HacD2HnD (wAP ac)**                                                                                          | Turns off all LEDs except Ethernet LED  |

## 例子

### 基本示例

通过CLI命令控制LED，用于编写脚本:

```shell
#add led entry with specific type "on" or "off" to leds menu
/system leds add leds=led1 type=off
#to control led
/system leds set [find where leds="led1"] type=on
or
/system leds set [find where leds="led1"] type=off
```

启用用户ACT LED显示RB951上的当前CAP状态

`/system leds
add leds=user-led type=ap-cap`

### 调制解调器信号强度例子

调制解调器信号强度范围是[-113...-51]，调制解调器信号阈值将最弱的信号限制增加到-91，所以LED指示的信号范围是[-91...-51]。这个范围根据配置在调制解调器信号LED触发器上的LED数量，分成相等的部分。当信号高于-91时，第一个LED打开，当信号达到-51时，最后一个LED打开。

`/system leds
add interface=lte1 leds=led1,led2,led3,led4,led5 modem-signal-treshold=-91 type=modem-signal`

### 调制解调器接入技术实例

这些LED触发例子按照调制解调器技术产生的顺序打开LED。GSM；3G；LTE。

- 1个LED：当LTE激活时，led1会打开。

`/system leds add interface=lte1 leds=led1 modem-type=modem-technology`

- 2 LEDs: led1 - 3G; led2 - LTE;

`/system leds
add interface=lte1 leds=led1,led2 modem-type=modem-technology`

- 3 LEDs: led1 - GSM; led2 - 3G; led3 - LTE

`/system leds add interface=lte1 leds=led1,led2,led3 modem-type=modem-technology`
