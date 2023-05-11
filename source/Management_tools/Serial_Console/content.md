# 概述

串行控制台和终端是一种工具，用于和串口相互连接的设备和其他系统进行通信。串行终端可用于监控和配置许多设备-包括调制解调器、网络设备（包括MikroTik路由器），以及任何可以连接到串行（异步）端口的设备。

串行控制台功能用于配置直接访问的配置设施（监视器/键盘和串行端口），这些设施大多用于初始或恢复配置。需要一根特殊的空调制解调器电缆来连接两台主机（如两台PC，或两台路由器；不是调制解调器）。注意，需要一个终端仿真程序（如Windows的HyperTerminal或Linux的minicom）来从另一台计算机访问串行控制台。路由器串口的默认设置为115200比特/秒（x86系统默认为9600比特/秒），8个数据位，1个停止位，无奇偶校验，硬件（RTS/CTS）流量控制。 

一些客户说明了串行终端（管理端）功能的有用情况：

- 在山顶上，MikroTik无线设备与无法进行带内管理（通过IP网络的telnet）的设备（包括交换机和Cisco路由器）相邻。
- 通过串口监控天气报告设备
- 连接到一个高速微波调制解调器，需要通过串口连接进行监控和管理。

利用MikroTik的串行终端，可以监测和控制多达132个（甚至可能更多）设备。

# 串行控制台的连接

设备之间的串行通信是通过RS232完成的，它是计算机世界中最古老和最广泛传播的通信方法之一。用于与调制解调器或其他外围设备DTE/DCE的通信。在现代社会，串行通信的主要用途是DTE/DTE通信（数据终端设备），例如，使用空调制解调器电缆。有几种类型的空调制解调器电缆，其中一些可能不能和RouterBoards一起使用。

## 无握手的空调制解调器

这种电缆完全不使用握手引脚：

| Side1 (DB9f) | Side2 (DB9f) | Function |
| ------------ | ------------ | -------- |
| 2            | 3            | Rx ← Tx  |
| 3            | 2            | Tx → Rx  |
| 5            | 5            | GND      |

允许交叉连接的Rx/Tx线路上只有数据流量。这种类型的电缆不进行硬件流量控制。执行流量控制的唯一方法是使用XOFF和XON字符的软件流量控制。

## 带有回环握手的空调制解调器

第一条电缆的问题是，当连接到一个启用了硬件流量控制的设备上时，软件在检查调制解调器信号线时可能会挂起。 

带有回环握手的空调制解调器电缆可以解决这个问题，它的目的是欺骗定义良好的软件，使其认为有握手功能：

| Side1 (DB9f) | Side2 (DB9f) | Function       |
| ------------ | ------------ | -------------- |
| 2            | 3            | Rx ← Tx        |
| 3            | 2            | Tx → Rx        |
| 5            | 5            | GND            |
| 1+4+6        | -            | DTR → CD + DSR |
| -            | 1+4+6        | DTR → CD + DSR |
| 7+8          | -            | RTS → CTS      |
| -            | 7+8          | RTS → CTS      |

用这种电缆不能实现硬件流控制。此外，如果远程软件不发送自己的准备信号到DTR输出，通信就会中断。

## 带部分握手的空调制解调器

这种电缆可以在启用流量控制时使用，而不会与DTE/DCE通信中使用流量控制的原始方式不兼容。

不建议在RouterOS中使用这种类型的电缆。

| Side1 (DB9f) | Side2 (DB9f) | Function          |
| ------------ | ------------ | ----------------- |
| 1            | 7+8          | RTS2 → CTS2 + CD1 |
| 2            | 3            | Rx ← Tx           |
| 3            | 2            | Tx → Rx           |
| 4            | 6            | DTR → DSR         |
| 5            | 5            | GND               |
| 6            | 4            | DSR ← DTR         |
| 7+8          | 1            | RTS1 → CTS1 + CD2 |

具有完全握手功能的空调制解调器

与特殊软件一起使用，不要与RouterOS一起使用。

| Side1 (DB9f) | Side2 (DB9f) | Function  |
| ------------ | ------------ | --------- |
| 2            | 3            | Rx ← Tx   |
| 3            | 2            | Tx → Rx   |
| 4            | 6            | DTR → DSR |
| 5            | 5            | GND       |
| 6            | 4            | DSR ← DTR |
| 7            | 8            | RTS → CTS |
| 8            | 7            | CTS ← RTS |

## 空调制解调器兼容性

下面的汇总表可以为你的应用选择合适的电缆。

|                            | 无握手 | 回环握手 | 部分握手      | 完全握手 |
| -------------------------- | ------ | -------- | ------------- | -------- |
| 端口功能有限的RouterBoards | Y      | Y        | N<sup>1</sup> | N        |
| 全功能的RouterBoards       | Y      | Y        | Y             | N        |

1. 只有硬件流控禁用时才能工作

  
|                         | 无握手 | 回环握手       | 部分握手       | 完全握手       |
| ----------------------- | ------ | -------------- | -------------- | -------------- |
| 软件流控                | Y      | Y <sup>1</sup> | Y <sup>2</sup> | Y <sup>2</sup> |
| 低速DTE/DCE兼容硬件流控 | N      | Y              | Y <sup>1</sup> | N              |
| 高速DTE/DCE兼容硬件流控 | N      | Y              | Y <sup>2</sup> | N              |
| 使用特殊软件的高速通信  | N      | N              | Y <sup>1</sup> | Y              |

1. 可以作为替代方案使用
2. 可以使用，但不建议使用

## RJ45串口

这种类型的端口用于RouterBOARD 2011、3011、4011、CCR1072、CCR1036 r2、CCR2xxx和CRS系列设备，有时被称为 "思科式"串口。

RJ45到DB9电缆引脚：

![](https://help.mikrotik.com/docs/download/attachments/328139/Rj45-pinout.gif.png?version=1&modificationDate=1570702738344&api=v2)  
  

| Signal | Console Port (DTE)  RJ-45 | RJ-45 Rolled Cable  RJ-45 Pin | Adapter DB-9 Pin | Adapter DB-25 Pin | Signal |
| ------ | ------------------------- | ----------------------------- | ---------------- | ----------------- | ------ |
| RTS    | 1                         | 8                             | 8                | 5                 | CTS    |
| DTR    | 2                         | 7                             | 6                | 6                 | DSR    |
| TxD    | 3                         | 6                             | 2                | 3                 | RxD    |
| Ground | 4                         | 5                             | 5                | 7                 | Ground |
| Ground | 5                         | 4                             | 5                | 7                 | Ground |
| RxD    | 6                         | 3                             | 3                | 2                 | TxD    |
| DSR    | 7                         | 2                             | 4                | 20                | DTR    |
| CTS    | 8                         | 1                             | 7                | 4                 | RTS    |

## RB M33G 额外的串口接头

对于RBM33G，额外的串口接头可以连接到GPIO引脚U3_RXD, GND, U3_TXD, 和3V3上。

需要RouterOS 6.45.1+固件!

## CCR 串口接头

云核心路由器系列设备在PCB板上有一个串口接头，称为J402或100

以下是该连接器的引脚分布：

![](https://help.mikrotik.com/docs/download/attachments/328139/J402.png?version=1&modificationDate=1570702787676&api=v2)

# 串行终端的使用

RouterOS允许使用 `/system serial-terminal` 命令与通过串口连接到路由器的设备和其他系统进行通信。所有的键盘输入将被转发到串口，所有来自串口的数据将被输出到连接的设备。

首先必须有一个空闲的串口，如果设备只有一个串口（像所有的RouterBoards、WRAP/ALIX板等），必须禁用这个串口上的系统控制台，以便能够把它作为 **串口终端** 与其他设备（交换机、调制解调器等）连接：

`/system console disable 0`

请确保只是禁用控制台，而不是删除，当真正删除它时，RouterOS会在下次重启后重新创建控制台。

**注意，有一些注意事项是你应该注意的! 花点时间了解这些限制，以避免在将设备连接到RouterBoard的串行端口时发生奇怪的事情：**

- 通过重新配置RouterBoard上的Serial0端口，如上图所示，你会失去对RouterOS的串行控制台访问。这意味着如果不能再通过网络访问你的RouterBoard，甚至可能不得不重新设置它的整个配置以再次获得访问权。
- 当重启RouterBoard时，启动加载器（RouterBOOT）将始终使用串行控制台（RouterBoards上的Serial0）来发送一些启动信息并提供对RouterBOOT菜单的访问。
    
    让文本从串行端口出来到所连接的设备上，可能会使连接的设备感到困惑。此外，在标准配置中，可以通过按 **任意** 键进入RouterBOOT菜单。因此，如果串行设备在启动时向RouterBoard的串行端口发送任何字符，RouterBoard将进入RouterBOOT菜单，除非手动干预，否则将 **不** 启动RouterOS!
    
    可以重新配置RouterBOOT，使其只在收到 **DEL** 字符时才进入RouterBOOT菜单-用这个方法来减少重启时路由器卡住的机会!
    
    或者如果使用较新的版本 [Silent boot](https://wiki.mikrotik.com/wiki/Silent_boot "Silent boot") 功能，可以用来抑制串行接口上的任何输出，包括去除启动的声音。
    

接下来根据所连接设备的串口设置来配置串口。使用以下命令，把串口设置为19200 Baud 8N1。需要使用什么设置取决于所连接的设备：

`/port set serial0 baud-rate=19200 data-bits=8 parity=none stop-bits=1`

也可以通过设置让RouterOS猜测需要的波特率

`/port set serial0 baud-rate=auto`

现在可以连接设备了，如果还没完成，则必须使用 [空调制解调器电缆](https://help.mikrotik.com/docs/display/ROS/Serial+Console#SerialConsole-NullModemWithoutHandshake) （和以太网的交叉电缆相同）。现在可以开始了：

`/system serial-terminal serial0`

这将使你能够访问你连接到Serial0端口的设备。**Ctrl-A** 是前缀键，这意味着你将进入一个小 "菜单"。如果你需要发送 **Ctrl-A** 字符到远程设备，请按 **Ctrl-A** 两次。

如果你想退出与串行设备的连接，输入 **Ctrl-A**，然后按 **Q**。这将使你回到RouterOS的控制台。

不要以不正确的速度连接设备，避免转储二进制数据。

# 特殊登录

特殊登录用来访问另一个通过串行电缆连接的设备（例如交换机），打开一个telnet/ssh会话，直接进入这个设备（无需先登录RouterOS）。 

为了演示，使用两个RouterBoards和一台PC。 

![](https://help.mikrotik.com/docs/download/attachments/328139/Special-login-setup.jpg?version=2&modificationDate=1657265964296&api=v2)

路由器R1和R2用串行电缆连接，PC通过以太网与R1连接。假设想通过串行电缆从PC访问路由器R2。要做到这一点，必须在R1上设置串行接口代理。可以通过名为 **特殊登录** 功能来完成。

默认情况下，控制台绑定到串行端口。 

第一项任务是取消控制台与串口的绑定，只需禁用/系统控制台菜单中的条目：

```shell
[admin@MikroTik] /system console> print
Flags: X - disabled, U - used, F - free
 #   PORT                                                                    TERM
 0 X serial0                                                                 vt102
```

下一步是添加新用户，在这里是 _serial_，并将它和串口绑定。

```shell
[admin@MikroTik] > /user add name=serial group=full
[admin@MikroTik] > /special-login add user=serial port=serial0 disabled=no
[admin@MikroTik] > /special-login print
Flags: X - disabled
 #   USER                                                                    PORT
 0   serial                                                                  serial0
```

现在已经准备好从PC上访问R2。

```shell
maris@bumba:/$ ssh serial@10.1.101.146
 
[Ctrl-A is the prefix key]
R2 4.0beta4
R2 Login:
 
[admin@R2] >
```

要退出特殊登录模式，请按Ctrl+A和Q

```shell
[admin@MikroTik] >
[Q - quit connection]      [B - send break]
[A - send Ctrl-A prefix]   [R - autoconfigure rate]
 
 
Connection to 10.1.101.146 closed.
```


路由器重启，连接串行电缆后，路由器可能会卡在启动器主菜单上。

要解决这个问题，需要允许<any>键到<delete>键访问bootloader主菜单：

- 进入bootloader菜单
- 按'k'键查看启动键选项
- 按'2'将键改为<删除>。

```shell
What do you want to configure?                                                   
d - boot delay                                                                
k - boot key                                                                  
s - serial console                                                            
n - silent boot                                                              
o - boot device                                                               
u - cpu mode                                                                 
f - cpu frequency                                                             
r - reset booter configuration                                                 
e - format nand                                                               
g - upgrade firmware                                                         
i - board info                                                                
p - boot protocol                                                            
b - booter options                                                            
t - call debug code                                                           
l - erase license                                                             
x - exit setup                         
your choice: k - boot key

Select key which will enter setup on boot:
 * 1 - any key
   2 - <Delete> key only

your chaoice: 2
```