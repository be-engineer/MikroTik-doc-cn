RouterBOOT 负责在 RouterBOARD 设备中启动 RouterOS。

## 主加载器和备份加载器

默认情况下，使用主加载程序，但 RouterBOARD 设备还有一个辅助（备份）引导加载程序，可以在主加载程序不工作时使用。 可以使用 RouterOS 中的配置调用备份加载程序：

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">system</code><code class="ros constants">/routerboard/settings/</code><code class="ros functions">set </code><code class="ros value">force-backup-booter</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

也可以通过按下 RESET 按钮打开设备来使用备份引导程序。 只能升级主RouterBOOT，所以万一失败，可以使用备份启动器启动设备，降级主加载器。 有关升级说明，请按照 [RouterBOARD#UpgradingRouterBOOT](https://help.mikrotik.com/docs/display/ROS/RouterBOARD#RouterBOARD-UpgradingRouterBOOT) 中的说明进行操作

## RouterBOARD 复位按钮

RouterBOOT 复位按钮具有三个功能：

- 在启动期间按住此按钮直到 LED 灯开始闪烁，松开按钮以复位 RouterOS 配置（总共 5 秒）
- 再按住 5 秒，LED 变为常亮，现在松开以打开 CAP 模式（总共 10 秒）
- 或者继续按住按钮 5 秒直到 LED 熄灭，然后松开按钮让 RouterBOARD 寻找 Netinstall 服务器（总共 15 秒）

如果在通电之前按住按钮，除了上述所有操作外，还将使用备用 RouterBOOT。 要在不加载备份加载器的情况下执行上述操作，请在设备通电后立即按下按钮。

  

[Reset the password](https://help.mikrotik.com/docs/display/RKB/Reset+the+password)

[https://www.youtube.com/watch?v=6Unz92rABs8](https://www.youtube.com/watch?v=6Unz92rABs8) 

## 复位**无线**套件的配置

复位按钮具有与其他设备相同的功能，详细解释请参考 [https://help.mikrotik.com/docs/display/ROS/Reset+Button](https://help.mikrotik.com/docs/display/ROS/Reset+Button)

启动时按住按钮 5 秒（USR LED 灯开始闪烁）- 重置为密码保护状态。

启动时按住按钮 10 秒（USR LED 闪烁后常亮）- 完全删除配置。

## 配置

对于具有串行控制台连接器的 RouterBOARD 设备，可以访问 RouterBOOT 加载程序配置菜单。 [串行控制台](https://help.mikrotik.com/docs/display/ROS/Serial+Console)手册中描述了所需的电缆。 RouterBOARD串口配置为115200bit/s，8个数据位，1个停止位，无奇偶校验。 我们建议禁用硬件流控。

此示例显示了 RouterBOOT 7.4beta4 中可用的菜单：

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">RouterBOOT booter 7.4beta4</code></div><div class="line number2 index1 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">CRS328-24P-4S+</code></div><div class="line number4 index3 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">built by build at Jun</code><code class="ros constants">/15/2022 11:34:09 from revision 73B4521C</code></div><div class="line number6 index5 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">CPU frequency</code><code class="ros constants">: 800 MHz</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">Memory size</code><code class="ros constants">: 512 MiB</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">Storage size</code><code class="ros constants">:&nbsp; 16 MiB</code></div><div class="line number10 index9 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros plain">Press Ctrl+E to enter etherboot mode</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros plain">Press any key within 2 seconds to enter setup</code></div><div class="line number13 index12 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number14 index13 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number15 index14 alt2" data-bidi-marker="true"><code class="ros plain">RouterBOOT-7.4beta4</code></div><div class="line number16 index15 alt1" data-bidi-marker="true"><code class="ros plain">What </code><code class="ros functions">do </code><code class="ros plain">you want to configure?</code></div><div class="line number17 index16 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros plain">d - boot delay</code></div><div class="line number18 index17 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros plain">k - boot key</code></div><div class="line number19 index18 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros plain">s - serial console</code></div><div class="line number20 index19 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros plain">n - silent boot</code></div><div class="line number21 index20 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros plain">o - boot device</code></div><div class="line number22 index21 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros plain">z - extra kernel parameters</code></div><div class="line number23 index22 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros plain">r - </code><code class="ros functions">reset </code><code class="ros plain">booter configuration</code></div><div class="line number24 index23 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros plain">e - format storage</code></div><div class="line number25 index24 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros plain">w - repartition nand</code></div><div class="line number26 index25 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros plain">g - </code><code class="ros functions">upgrade </code><code class="ros plain">firmware</code></div><div class="line number27 index26 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros plain">i - board info</code></div><div class="line number28 index27 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros plain">p - boot protocol</code></div><div class="line number29 index28 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros plain">b - booter options</code></div><div class="line number30 index29 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros plain">j - boot os</code></div><div class="line number31 index30 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros plain">t - hardware tests</code></div><div class="line number32 index31 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros plain">l - erase license</code></div><div class="line number33 index32 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros plain">x - exit setup</code></div><div class="line number34 index33 alt1" data-bidi-marker="true"><code class="ros plain">your choice</code><code class="ros constants">:</code></div></div></td></tr></tbody></table>

这些选项是不言自明的。


| 字母 | 说明           | 含义                                                                                     |
| ---- | -------------- | ---------------------------------------------------------------------------------------- |
| d    | 启动延迟       | 延迟RouterOS启动，以初始化接口                                                           |
| k    | 启动密钥       | 打开配置菜单按钮                                                                         |
| s    | 串行控制台     | 设置串口波特率                                                                           |
| n    | 静默启动       | 限制串口上的所有输出，以防某些设备连接到它(如GPS设备或温度监视器)                        |
| o    | 启动设备       | 允许启用Netinstall引导                                                                   |
| z    | 额外的内核参数 |
|      |
| r    | 重启启动配置   | 重置此菜单中的设置。**警告，没有确认**                                                   |
| e    | 格式化存储器   | 销毁NAND上的所有数据，包括RouterOS的配置和许可证                                         |
| w    | nand重新分区   | 请查看[Partitions](https://help.mikrotik.com/docs/display/ROS/Partitions) 文档的更多信息 |
| y    | 激活分区       | 选择一个活动分区，从中尝试加载RouterOS                                                   |
| g    | 升级固件       | 支持通过网络或XModem协议升级RouterBOOT版本                                               |
| i    | 板卡信息       |
|      |
| p    | 启动协议       |
|      |
| b    | 引导器选项     | 选择默认情况下要使用的引导加载程序                                                       |
| t    | 执行内存测试   | 引导器选项                                                                               |
| j    | 启动系统       | 执行内存测试                                                                             |
| t    | 硬件测试       |                                                                                          |
| l    | 擦除许可证     |                                                                                          |
| x    | 退出设置       |                                                                                          |

按下相应的键盘字母，你会看到更多的选项，如下所示：

```
# d - boot delay:

Select boot delay:
   1 - 1s
 * 2 - 2s
   3 - 3s
   4 - 4s
   5 - 5s
   6 - 6s
   7 - 7s
   8 - 8s
   9 - 9s

# k - boot key:

Select key which will enter setup on boot:
 * 1 - any key
   2 - <Delete> key only

# s - serial console:

Select baud rate for serial console:
 * 1 - 115200
   2 - 57600
   3 - 38400
   4 - 19200
   5 - 9600
   6 - 4800
   7 - 2400
   8 - 1200
   9 - off

# n - silent boot:

Silent boot:
   0 - off
 * 1 - on

# o - boot device:

Select boot device:
   e - boot over Ethernet
 * n - boot from NAND, if fail then Ethernet
   1 - boot Ethernet once, then NAND
   o - boot from NAND only
   b - boot chosen device
   f - boot Flash Configure Mode
   3 - boot Flash Configure Mode once, then NAND


# f - cpu frequency:

Select CPU frequency:
   a -  200MHz
   b -  400MHz
   c -  600MHz
   d -  800MHz
   e - 1000MHz
 * f - 1200MHz

# r - reset booter configuration:

# e - format nand:

Do you realy want to format your storage device?
that would result in losing all your data
type "yes" to confirm: 

# w - repartition nand:

Select parititon count:
   1 - partition
 * 2 - partitions
   3 - partitions
   4 - partitions

# y - active partition:

Select active partiton:
 * 0 - partition
   1 - partition

# g - upgrade firmware:

Upgrade firmware options:
   e - upgrade firmware over ethernet
   s - upgrade firmware over serial port

# i - board info:

Board Info:

        Board type: CCR1009-8G-1S-1S+
     Serial number: 48FF01DDE6FD
  Firmware version: 3.19
     CPU frequency: 1200 MHz
       Memory size: 2048 MiB
         NAND size: 128 MiB
        Build time: 2014-09-23 15:02:34
  eth1 MAC address: 00:0C:42:00:BE:4A
  eth2 MAC address: 00:0C:42:00:BE:4B
  eth3 MAC address: 00:0C:42:00:BE:4C
  eth4 MAC address: 00:0C:42:00:BE:4D
  eth5 MAC address: 00:0C:42:00:BE:4E
  eth6 MAC address: 00:0C:42:00:BE:4F
  eth7 MAC address: 00:0C:42:00:BE:50
  eth8 MAC address: 00:0C:42:00:BE:51
  eth9 MAC address: 00:0C:42:00:BE:52
 eth10 MAC address: 00:0C:42:00:BE:53

# p - boot protocol:

Choose which boot protocol to use:
 * 1 - bootp protocol
   2 - dhcp protocol

# b - booter options:

Select which booter you want to load:
 * 1 - load regular booter
   2 - force backup-booter loading

#t - do memory testing:

launches built in memory test!

# x - exit setup:

Exit bios configuration menu and continues with system startup.

```

  

## 简单升级

RouterBOOT 可以通过以下方式从 RouterOS 升级：

- 运行命令 _/system routerboard upgrade_
- 重新启动路由器以应用升级 (_/system reboot_)]


<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@admin] &gt; system</code><code class="ros constants">/routerboard/</code><code class="ros functions">upgrade</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Do you really want to </code><code class="ros functions">upgrade </code><code class="ros plain">firmware? [y</code><code class="ros constants">/n]</code></div></div></td></tr></tbody></table>

每个 ROS 版本都包含一个新的 RouterBoot 版本，一旦执行 ROS 升级，建议您也升级 RouterBoot。

## 检查RouterBOOT版本
该命令显示当前设备的RouterBOOT版本，以及包含在routerboard中的可用升级.npk包，或者上传了与设备型号对应的FWF文件

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@admin] &gt;&nbsp; system</code><code class="ros constants">/routerboard/</code><code class="ros functions">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">;;; Firmware upgraded successfully, please reboot </code><code class="ros functions">for </code><code class="ros plain">changes</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">to take effect!</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">routerboard</code><code class="ros constants">: yes</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">board-name</code><code class="ros constants">: hAP ac</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">model</code><code class="ros constants">: RouterBOARD 962UiGS-5HacT2HnT</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">serial-number</code><code class="ros constants">: 6737057562DD</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">firmware-type</code><code class="ros constants">: qca9550L</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">factory-firmware</code><code class="ros constants">: 3.29</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">current-firmware</code><code class="ros constants">: 6.49.5</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">upgrade-firmware</code><code class="ros constants">: 7.4beta5</code></div></div></td></tr></tbody></table>

在这种情况下，您会看到在当前的 RouterOS 版本中已经有 **更新版本** 的 Bootloader 固件可用，并且它已经更新并需要重新启动。

也可以通过上传 *.FWF 文件进行降级，联系 MikroTik 支持时可能需要使用旧版本进行故障排除。