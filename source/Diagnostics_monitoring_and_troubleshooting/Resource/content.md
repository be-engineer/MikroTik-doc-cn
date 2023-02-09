# 资源

`/system resource`

一般资源菜单显示总体资源使用情况和路由器统计数据，如正常运行时间、内存用量、磁盘用量、版本等。

还有几个子菜单用于更详细的硬件统计，如PCI、IRQ和USB:

```shell
[admin@RB1100test] /system resource> print
uptime: 2w1d23h34m57s
version: "5.0rc1"
free-memory: 385272KiB
total-memory: 516708KiB
cpu: "e500v2"
cpu-count: 1
cpu-frequency: 799MHz
cpu-load: 9%
free-hdd-space: 466328KiB
total-hdd-space: 520192KiB
write-sect-since-reboot: 1411
write-sect-total: 70625
bad-blocks: 0.2%
architecture-name: "powerpc"
board-name: "RB1100"
platform: "MikroTik"
```

属性

所有属性只读

| 属性                                    | 说明                                                                                                                                            |
| --------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| **architecture-name** (_string_)        | CPU架构。可以是 _powerpc_、_x86_、_mipsbe_ 或 _mipsle_。                                                                                        |
| **bad-blocks** (_percent_)              | 显示NAND上坏块的百分比。                                                                                                                        |
| **board-name** (_string_)               | RouterBOARD型号名称                                                                                                                             |
| **cpu** (_string_)                      | 板上的Cpu型号。                                                                                                                                 |
| **cpu-count** (_integer_)               | 系统上有多少个CPU。每个核心是一个独立的CPU，Intel HT也是一个独立的CPU。                                                                         |
| **cpu-frequency** (_string_)            | 当前的CPU频率。                                                                                                                                 |
| **cpu-load** (_percent_)                | 已用CPU资源的百分比。结合所有的CPU。每个核心的CPU使用情况可以在 [CPU子菜单](https://wiki.mikrotik.com/wiki/Manual:System/Resource#CPU) 中看到。 |
| **free-hdd-space** (_string_)           | 硬盘或NAND上的可用空间。                                                                                                                        |
| **free-memory** (_string_)              | 未使用的RAM数量。                                                                                                                               |
| **platform** (_string_)                 | 平台名称，通常是 "MikroTik"。                                                                                                                   |
| **total-hdd-space** (_string_)          | 硬盘或NAND的大小。                                                                                                                              |
| **total-memory** (_string_)             | 安装的RAM的数量                                                                                                                                 |
| **uptime** (_time_)                     | 开机后经过的时间间隔。                                                                                                                          |
| **version** (_string_)                  | 安装的RouterOS版本号。                                                                                                                          |
| **write-sect-since-reboot** (_integer_) | 自路由器上次启动以来在HDD或NAND中写入的扇区数                                                                                                   |

## CPU

`/system resource cpu`

这个子菜单显示每个CPU的使用情况，以及IRQ和磁盘的使用情况。

```shell
[admin@RB1100test] /system resource cpu> print
CPU LOAD IRQ DISK
0 5% 0% 0%
[admin@RB1100test] /system resource cpu>
```

属性

只读属性

| 属性                 | 说明                      |
| -------------------- | ------------------------- |
| **cpu** (_integer_)  | 显示CPU使用情况的标识号。 |
| **load** (_percent_) | CPU的使用率百分比         |
| **irq** (_percent_)  | IRQ使用率百分比           |
| **disk** (_percent_) | 磁盘使用率百分比          |

## IRQ

`/system resource irq`
  
菜单显示路由器上所有使用的IRQ。可以在多核系统上设置 [IRQ负载均衡](https://wiki.mikrotik.com/wiki/Manual:System/Resource#IRQ_Load_Balancing)，将IRQ分配给特定的核。IRQ的分配是由硬件完成的，不能从RouterOS中改变。例如，如果所有以太网都被分配到一个IRQ，那么你必须处理硬件问题：升级主板BIOS，在BIOS中手动重新分配IRQ，如果上述方法都没有用，那就只能改硬件。

属性

| 属性                                   | 说明                                                                                                                                                          |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **cpu** (_auto \| integer_; Default: ) | 指定哪个CPU分配到IRQ。<br>- **auto** - 根据中断数量来选择CPU。使用 [NAPI](http://www.linuxfoundation.org/collaborate/workgroups/networking/napi) 来优化中断。 |

**Read-only 属性**

| 属性                       | 说明                                       |
| -------------------------- | ------------------------------------------ |
| **active-cpu** (_integer_) | 在多核系统中显示活跃的CPU。                |
| **count** (_integer_)      | 中断数量。在以太网接口上interrupt=packet。 |
| **irq** (_integer_)        | IRQ识别号                                  |
| **users** (_string_)       | 分配给IRQ的进程                            |

## IRQ负载均衡

### USB

`/system resource usb`

该菜单显示电路板上所有可用的USB控制器。至少有一个USB控制器存在时该菜单才可用。

```shell
[admin@MikroTik] /system resource usb> print detail
0 device="2:1" name="RB400 EHCI" serial-number="rb400_usb" vendor-id="0x1d6b"
device-id="0x0002" speed="480 Mbps" ports=2 usb-version="2.00"
1 device="1:1" name="RB400 OHCI" serial-number="rb400_usb" vendor-id="0x1d6b"
 device-id="0x0001" speed="12 Mbps" ports=2 usb-version="1.10"
```

属性

| 属性                         | 说明                                                  |
| ---------------------------- | ----------------------------------------------------- |
| **device** (_string_)        |
| **device-id** (_hex_)        | 十六进制的设备ID                                      |
| **name** (_string_)          | 从驱动中检索到的设备描述名称                          |
| **ports** (_integer_)        | USB控制器支持多少个端口                               |
| **serial-number** (_string_) |
| **speed** (_string_)         | 可以使用的最大USB速度（USBv2为480Mbps，USBv1为12Mbps) |
| **usb-version** (_string_)   | 标明最大支持的USB版本                                 |
| **vendor** (_string_)        | 设备制造商的名称。                                    |
| **vendor-id** (_hex_)        | 十六进制的厂商ID                                      |

## PCI

`/system resource pci`

PCI子菜单显示板卡上所有PCI设备的信息

```shell
[admin@RB1100test] /system resource pci> print
# DEVICE VENDOR NAME IRQ
0 06:00.0 Attansic Technology Corp. unknown device (rev: 192) 18
1 05:00.0 Freescale Semiconductor Inc MPC8544 (rev: 17) 0
2 04:00.0 Attansic Technology Corp. unknown device (rev: 192) 17
3 03:00.0 Freescale Semiconductor Inc MPC8544 (rev: 17) 0
4 02:00.0 Attansic Technology Corp. unknown device (rev: 192) 16
5 01:00.0 Freescale Semiconductor Inc MPC8544 (rev: 17) 0
6 00:00.0 Freescale Semiconductor Inc MPC8544 (rev: 17) 0
```

属性

所有属性只读

| 属性                    | 说明                              |
| ----------------------- | --------------------------------- |
| **category** (_string_) | PCI设备类型，例如，_以太网控制器_ |
| **device** (_string_)   |
| **device-id** (_hex_)   | 十六进制的设备ID                  |
| **io** (_hex-hex_)      | I/O内存范围                       |
| **irq** (_integer_)     | 分配给该设备的IRQ                 |
| **memory** (_hex-hex_)  | 内存范围                          |
| **name** (_string_)     | 从驱动程序中检索到的设备描述名称  |
| **vendor** (_string_)   | 设备制造商的名称。                |
| **vendor-id** (_hex_)   | 十六进制的厂商ID                  |
