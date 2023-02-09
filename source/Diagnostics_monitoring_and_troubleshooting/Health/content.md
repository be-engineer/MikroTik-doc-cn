# 概述

支持监控的硬件会显示不同的硬件状态信息，如温度、电压、电流、风扇速度等。

以CCR1072-1G-8S+设备为例。

```shell
          cpu-overtemp-check: yes
      cpu-overtemp-threshold: 100C
  cpu-overtemp-startup-delay: 1m
             cpu-temperature: 46C
           power-consumption: 62.9W
          board-temperature1: 31C
          board-temperature2: 34C
                psu1-voltage: 12.1V
                psu2-voltage: 0V
                psu1-current: 5.2A
                psu2-current: 0A
                  fan1-speed: 6375RPM
                  fan2-speed: 6436RPM
                  fan3-speed: 6375RPM
                  fan4-speed: 6467RPM
```

**警告：** 关于RouterBOARD产品的功能可用性，请查看 [mikrotik.com](https://mikrotik.com/products)

## 电压

支持电压监控的路由器会显示供电电压值。在CLI/Winbox中显示为伏特。在脚本/API/SNMP中，是dV或CLI/Winbox中显示的值乘以10。

**注：** 有PEXT和PoE电源输入的路由器使用PEXT进行校准，因此，由于额外的以太网保护链，PoE上显示的值可能低于输入电压。

**注意：** 如果旧版本的CRS112、CRS210和CRS109设备使用PoE供电--健康状况仅显示正确的电压，最高为26.7V。如果使用更高的电压--健康状况将显示恒定的16V。

## 温度

支持温度监控的路由器会显示温度。在CLI/Winbox中显示摄氏度。使用脚本/API/SNMP，这个值将在CLI/Winbox中显示，并乘以10。根据设备的不同，有各种温度传感器。这些传感器可能指的是：Cpu-温度、pcb-温度、sfp-温度。设备测试的环境温度范围可以在 [mikrotik.com](https://mikrotik.com/products) 的规格描述中找到。测试的环境温度范围是指设备可以被实际使用的温度。它和报告系统健康监测的温度 **不一样!**

## 风扇控制和行为

`/system health set`

使用这个菜单，用户能够控制TILE架构 [设备](https://mikrotik.com/download) 上的风扇行为。目前，对于其他RouterBOARD设备，没有 **no** 选项手动控制风扇行为。

**注意：** 从6.45.5版本开始，改进了风扇的稳定性。

有三个参数可能会影响风扇行为。PoE-out功耗、SFP温度和CPU温度。一旦其中一个参数超过了阈值，风扇就会启动。

### PoE-out功耗

如果设备有PoE-out，那么风扇的转速将发生变化，如下所述。

| PoE-out负载 | RPM % of max FAN speed (**DC** fans) |
| ----------- | ------------------------------------ |
| 0%..24%     | FAN speed 0%                         |
| 25%..46%    | FAN speed 25%                        |
| 47%..70%    | FAN speed 50%                        |
| 71%..92%    | FAN speed 75%                        |
| 93%..       | FAN speed 100%                       |

对于带有 **PWM** 风扇的设备，速度将从9...88%线性增加或减少（注意：低于100W时风扇RPM=0）。

### CPU和SFP温度

如果CPU或SFP温度超过58C，风扇将开始旋转。温度越高，风扇的转速越快。对于带有PWM风扇的设备，当CPU或SFP温度超过58C时，风扇将线性增加其RPM，以尽可能地保持温度在58C。对于有直流风扇的设备，当CPU或SFP的温度超过58C时，风扇将开始旋转，默认情况下是以更高转速，可能会导致设备冷却到风扇完全关闭。之后温度可能慢慢上升到58℃，风扇将再次打开。有一个例外。S+RJ10模块的温度阈值为65C才触发风扇。由于这是一个较高的温度阈值，风扇将以较高的初始速度开始旋转以冷却设备。

**注意：** 所有读数都是近似值，不是100%的精确。目的是让用户了解可能发生的故障。
