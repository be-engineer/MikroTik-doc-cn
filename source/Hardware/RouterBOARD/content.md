# 介绍

在RouterBOARD设备上，下面的菜单提供关于设备的一些基本信息。

```shell
[admin@demo.mt.lv] /system routerboard> print
       routerboard: yes
             model: 1200
     serial-number: 3B5E02741BF0
     firmware-type: amcc460
  factory-firmware: 2.38
  current-firmware: 7.1beta3
  upgrade-firmware: 7.2
```

## 属性

**只读属性**

| 属性                            | 说明                                                                                                                                                                                                                                    |
| ------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **current-firmware** (_string_) | 目前正在使用的RouterBOOT加载器的版本。不要与RouterOS操作系统的版本相混淆。                                                                                                                                                              |
| **factory-firmware** (_string_) | 特定设备制造时使用的RouterBOOT加载器版本。                                                                                                                                                                                              |
| **firmware-type** (_string_)    | 特定设备上使用的固件类型。                                                                                                                                                                                                              |
| **model** (_string_)            | 型号名称。                                                                                                                                                                                                                              |
| **routerboard** (_yes \| no_)   | 是否是一个MikroTik RouterBOARD设备。                                                                                                                                                                                                    |
| **serial-number** (_string_)    | 这个特定设备的序列号。                                                                                                                                                                                                                  |
| **upgrade-firmware** (_string_) | RouterOS的升级也包括新的RouterBOOT版本文件，但必须手动应用。这一行显示在设备中是否发现了一个新的RouterBOOT文件。该文件是通过最近的RouterOS升级所包含的，也可以是手动上传到路由器的FWF文件。无论哪种情况，最新发现的版本都会显示在这里。 |

## 升级RouterBOOT

RouterBOOT的升级通常包括对整个RouterBOARD操作的微小改进。建议保持版本的升级。如果看到 **upgrade-firmware** 值大于 **current firmware**，只需要执行 **upgrade** 命令，用 **y** 接受，然后用 **/system reboot** 重启。

```shell
[admin@mikrotik] /system routerboard> upgrade
Do you really want to upgrade firmware? [y/n]
y
echo: system,info,critical Firmware upgraded successfully, please reboot for changes to take effect!
```

重新启动后，**当前固件** 值应与 **升级固件** 值相同。

## 设置

**Sub-menu level:** `/system routerboard settings`

```shell
[admin@demo.mt.lv] /system routerboard settings> print
 baud-rate: 115200
boot-delay: 2s
enter-setup-on: any-key
boot-device: nand-if-fail-then-ethernet
cpu-frequency: 1200MHz
memory-frequency: 1066DDR
boot-protocol: bootp
enable-jumper-reset: yes
force-backup-booter: no
silent-boot: no
```

| 属性                                                                                       | 说明                                                                                                                                                                                                                                                          |
| ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **auto-upgrade** (_yes \| no_; Default: **no*)                                             | RouterOS升级后是否自动升级固件。最新的固件将在另外一次重启后应用。                                                                                                                                                                                            |
| **baud-rate** (_integer_; Default: **115200**)                                             | 选择板载RS232速度，单位为比特每秒（如果已安装）。                                                                                                                                                                                                             |
| **boot-delay** (_time_; Default: **1s**)                                                   | 开机时等待按键的时间。                                                                                                                                                                                                                                        |
| **boot-device** (_nand-if-fail-then-ethernet ..._;Default: **nand-if-fail-then-ethernet**) | 选择RouterBOOT加载操作系统的方式。<br>- flash-boot <br>- flash-boot-once-then-nand <br>- nand-if-fail-then-ethernet <br>- nand-only <br>- try-ethernet-once-then-nand                                                                                         |
| **boot-os** (_router-os \|swos_; Default: **router-os**)                                   | 改变CRS3xx系列交换机的 [操作系统](https://help.mikrotik.com/docs/display/ROS/CRS3xx+series+switches#CRS3xxseriesswitches-DualBoot) 启动                                                                                                                       |
| **boot-protocol** (_bootp \|dhcp ..._; Default: **bootp**)                                 | 使用的启动协议。<br>- bootp是启动RouterOS的默认选项。<br>- dhpc用于OpenWRT，也可能用于其他操作系统。                                                                                                                                                          |
| **cpu-frequency** (_depends on model_; Default: **depends on model**)                      | 这个选项允许改变设备的CPU频率。数值取决于型号，要查看可用的选项，请在此提示下按键盘上的 [?] （RouterOS版本6）或 [F1] （RouterOS版本7）。                                                                                                                      |
| **cpu-mode** (_power-save \| regular_; Default: **power-save**)                            | 是否在HLT指令中进入CPU暂停模式。大多数操作系统在CPU空闲周期中使用HLT指令。当CPU处于暂停模式时，它的功耗较小，但在低温条件下，建议选择常规模式，这样整个系统的温度会比较高。                                                                                   |
| **enable-jumper-reset** (_yes \| no_; Default: **yes**)                                    | 禁用此功能，以避免通过板载跳线意外重置设置。                                                                                                                                                                                                                  |
| **enter-setup-on** (_any-key \| delete-key_; Default: **any-key**)                         | 哪个键会导致 BIOS 在启动延迟期间进入配置模式。当串行控制台在启动过程中打印出符号并自行进入RouterBOOT菜单时很有用。请注意，在某些串行终端程序中，不能使用Delete键进入设置-在这种情况下，也许可以用Backspace键来完成。                                          |
| **force-backup-booter** (_yes \| no_; Default: **no**)                                     | 如果要使用备份的RouterBOOT。只有在主加载器以某种方式损坏而无法修复时才有用。这样，就不必通过按下复位按钮来启动设备（会加载备份加载器），可以使用这个设置每次都加载它<br>- yes - 始终用备份加载器<br>- no - 主启动器将被使用                                   |
| **memory-frequency** (_depends on model_; Default: **depends on model**)                   | 该选项允许改变设备的内存频率。数值取决于型号，要查看可用的选项，请在此提示下按键盘上的 [？] 按钮（RouterOS版本6）或 [F1] （RouterOS版本7）。                                                                                                                  |
| **memory-data-rate** (_depends on model_; Default: **depends on model**)                   | 该选项允许改变设备的内存数据率。数值取决于型号，要查看可用的选项，请在此提示下按键盘上的 [？] 按钮（RouterOS版本6）或 [F1] 按钮（RouterOS版本7）。                                                                                                            |
| **regulatory-domain-ce** (_yes \| no_; Default: **no**)                                    | 为高天线增益设备启用超低的发射功率（需要重启）。                                                                                                                                                                                                              |
| **silent-boot** (_yes \| no_; Default: **no**)                                             | 该选项在启动过程中禁止串行控制台输出和蜂鸣声，避免文本输出干扰到连接的设备。如果有温度监测器或调制解调器连接到串口上会很有用。<br>- yes 没有串行控制台输出，也没有启动时的蜂鸣声（不会禁用RouterOS: beep命令）。<br>- no 串行控制台没有常规的信息和选项菜单。 |

如果CPU或内存被超频了，这就是路由器性能不如人意的原因，那么这不属于保修范围，你应该把这两个频率恢复到额定值。

### 受保护的引导程序

该功能通过禁用etherboot来保护RouterOS的配置和文件免受物理攻击者的攻击。称为 "受保护的RouterBOOT"。这个功能只能在登录后从RouterOS内部启用和禁用，也就是说，没有RouterBOOT设置来启用/禁用这个功能。这些额外的选项只在特定条件下出现。当这个设置被启用时，复位按钮和复位针孔都被禁用。RouterBOOT菜单也被禁用。改变启动模式或启用RouterBOOT设置菜单的唯一办法是通过RouterOS。如果不知道RouterOS的密码则只有完全格式化才行。

提供了一个特殊的软件包来升级备份的RouterBOOT（**危险**）。较新的设备在出厂时就已经安装了这个新的备份加载器。如果RouterOS是 **v7**， **出厂固件** 版本低于 **7.6**，并且设备在启用该功能时显示信息 **"受保护的路由器启动"功能需要升级备份路由器启动器**，请执行以下操作： 
a) 将设备升级或降级到 **7.6** 版本（从我们的 [下载页面](https://mikrotik.com/download) 或 [存档](https://mikrotik.com/download/archive)）。 
b) 用 `/system routerboard upgrade` 升级当前的RouterBOOT版本，然后重启设备，使RouterBOOT版本（检查 "/system routerboard print " 时的 **当前固件** 版本）与安装的固件版本（"/system resource print"）相同，应该是7.6。 
c) 将 [适用于所有架构的v7通用包](https://box.mikrotik.com/f/3bd8cc7b2a6545228377/?dl=1) 拖入设备的文件系统，然后再次重启设备。这将使 **出厂固件** 版本为7.6，这里允许启用该功能。之后，可以将设备升级到一个较新的版本。 
  
如果你的RouterOS版本是 **v6**，并且得到了同样的提示，请遵循上述同样的步骤，但只是更新/降级/比较设备版本，具体为 **6.49.7**，并使用 [适用于所有架构的v6通用包](https://box.mikrotik.com/f/b062a26b4bd34c55aa52/?dl=1)。

从v7版本开始，启用或修改protected-routerboard功能时，必须按下复位或模式按钮进行确认。

例如，当设置启用protected-routeboard时，有60秒的时间按复位按钮来确认，否则，这个设置不会启用。

```shell
[admin@450] > system/routerboard/settings/set protected-routerboot=enabled ;
[admin@450] > system/routerboard/settings/print 
                        ;;; press button within 60 seconds to confirm 
                            protected routerboot enable
              auto-upgrade: no
                 baud-rate: 115200
                boot-delay: 2s
            enter-setup-on: any-key
               boot-device: nand-if-fail-then-ethernet
             cpu-frequency: auto
             boot-protocol: bootp
       enable-jumper-reset: yes
       force-backup-booter: no
               silent-boot: yes
      protected-routerboot: enabled
      reformat-hold-button: 20s
  reformat-hold-button-max: 10m
```

| 属性                                                                    | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **protected-routerboot** (_enabled \| disabled_; Default: **disabled**) | 此项设置禁止通过控制台电缆访问RouterBOOT配置，禁止通过重置按钮来改变启动模式（**网络安装将被禁用**）。只有使用已知的RouterOS管理密码才能访问RouterOS。只有在RouterOS上才可以解除这个设置。如果忘记了RouterOS的密码，唯一的选择是用下面的方法对NAND和RAM进行彻底格式化，必须知道复位按钮的保持时间（秒）。<br>- 启用安全模式，只有RouterOS管理员密码可以访问RouterOS。任何来自串口的用户输入都会被忽略。Etherboot不可用，RouterBOOT设置不能改变。<br>- 禁用常规操作，RouterBOOT设置可用串行控制台，复位按钮可用于启动Netinstall。                                                            |
| **reformat-hold-button** (_5s .. 300s_; Default: **20s**)               | 作为紧急恢复选项，可以在开机时按下按钮，使之超过reformat-hold-button时间，但少于reformat-hold-button-max时间（RouterBOOT 3.38.3中的新内容）来重置。<br>当用该按钮进行完全复位时，会有以下动作：<br>**极度危险。只有失去了对设备的所有访问权限时才使用**<br>1. RouterOS所有文件和配置都被nand重新格式化而不可逆转地删除。<br>2. 所有的RouterBOOT设置都被重置为默认值。<br>3. 电路板重新启动。<br>4. 由于从NAND启动失败，自动转到Etherboot。<br>5. 需要用Netinstall来重新安装RouterOS。<br>**请注意！** 某些RouterBOARDS的格式化可能需要5分钟以上。在格式化之后，板子就可以进行Netinstall了。 |
| **reformat-hold-button-max** (_5s .. 600s_; Default: **10m**)           | 通过设置最大保持时间提高安全性，必须在指定的时间内释放复位按钮。如果把 "reformat-hold-button "设置为60秒，"reformat-hold-button-max "设置为65秒，这意味着必须按住按钮60到65秒，不能少也不能多，这样就不可能猜到了。在RouterBOOT 3.38.3引入                                                                                                                                                                                                                                                                                                                                                  |

启用受保护的RouterBOOT设置的RouterBOARD将每秒钟闪烁一次LED，以方便计数。LED灯将在一秒钟内关闭，在下一秒钟内打开。

### 模式和复位按钮

所有运行RouterOS的MikroTik设备都支持复位按钮的附加功能。

一些RouterBOARD设备有一个模式按钮，当按钮被按下时，可以运行任何脚本。

支持的设备列表：

- RBcAP-2nD (cAP)
- RBcAPGi-5acD2nD (cAP ac)
- RBwsAP5Hac2nD (wsAP ac lite)
- RB750Gr3 (hEX)
- RB760iGS (hEX S)
- RB912R-2nD (LtAP mini, LtAP mini LTE/4G kit)
- RBD52G-5HacD2HnD (hAP ac^2)
- RBLHGR (LHG LTE/4G kit)
- RBSXTR (SXT LTE/4G kit)
- CRS328-4C-20S-4S+RM
- CRS328-24P-4S+RM
- CCR1016-12G r2
- CCR1016-12S-1S+ r2
- CCR1036-12G-4S r2
- CCR1036-8G-2S+ r2
- RBD53G-5HacD2HnD (Chateau)
- RBD53GR-5HacD2HnD (hAP ac^3)

| 属性                                                                                            | 说明                                                                      |
| ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| **enabled** (_no \| yes_; Default: **no**)                                                      | 禁用或启用按钮的操作                                                      |
| **hold-time** (_time interval Min..Max_; Default: )                                             | HoldTime:= 按钮被按下一定时间，就可以调用功能。                           |
| Min...Max: Min -- 0s...1m (时间间隔), Max -- 0s...1m (时间间隔) (从RouterOS 6.47beta60开始可用) |
| **on-event** (_string_; Default: )                                                              | 按下按钮后运行的脚本名称。该脚本必须在"/system scripts"菜单中定义和命名。 |

模式按钮示例:

```shell
/system script add name=test-mode-button source={:log info message=("mode button pressed");}
/system routerboard mode-button set on-event=test-mode-button enabled=yes
```

按下按钮后，消息 _"模式按钮被按下"_ 被记录在系统日志中。

从RouterOS 6.47开始，已经添加重置按钮功能和保持时间选项

6.47之前的RouterOS版本的例子：

```shell
/system script add name=test-mode-button source={:log info message=("mode button pressed");}
/system routerboard mode-button set on-event=test-mode-button hold-time=3..5 enabled=yes
```

重置按钮以同样的方式工作，但菜单移到了：`/system routerboard reset-button` 下。

```shell
/system script add name=test-reset-button source={:log info message=("reset button pressed");}
/system routerboard reset-button set on-event=test-reset-button hold-time=0..10 enabled=yes
```

用模式按钮控制 [LED暗模式](https://help.mikrotik.com/docs/display/ROS/LEDs#LEDs-LEDSettings) :

```shell
/system script add name=dark-mode source={
   :if ([system leds settings get all-leds-off] = "never") do={
      /system leds settings set all-leds-off=immediate ;
   } else={
        /system leds settings set all-leds-off=never
   }
 }
/system routerboard mode-button set enabled=yes on-event=dark-mode
```
