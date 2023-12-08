## 概述

**Sub-menu:** `/disk`

该菜单列出所有连接的存储设备，假定它们被支持并处于工作状态。这对带有SD/CF/USB/SATA/NVMe插槽的RouterBOARD设备和带有额外的专用存储驱动器的X86系统特别有用-因为内置的存储空间很小，当你想在路由器上建立一个大的用户管理器数据库、代理缓存或SMB共享时，外部驱动器就非常方便。

可以根据自己的需要添加多个外部或辅助驱动器，并为每一个提到的功能用途选择任何数量的驱动器。例如，用户管理器可以在3个磁盘上使用，其中一个是活动数据库，其余的是备份。然后，你可以添加第4个磁盘，将活动数据复制到上面-卸载-拔掉。然后移动到另一个服务器，继续使用实际的数据库。这意味着迁移和备份都变得很容易!

**注意**：从RouterOS 7.7beta9开始，硬盘带有它们物理连接的名称（插槽）。

## 属性

| 属性                                   | 描述                                                                                                                                                                                                       |
| -------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **eject-drive** (_Integer_; Default: ) | 使用分配给它的驱动器ID或NAME，安全地卸载（弹出）你选择的驱动器。发出这个命令后，可以从主机设备上移走。如果驱动器是x86的sata/etc，设备必须事先关闭热插拔SATA接口。                                          |
| **format-drive** ()                    | 命令启动磁盘格式化进程。包含自身的附加属性。如 "文件系统 "和 "标签"。<br>- _file_<br>- _file-system_ ('fat32' or 'ext4') - 用FAT32或EXT4类型格式化磁盘<br>- _interval_<br>- _label_ - 要分配给磁盘的标签。 |
| **monitor-traffic**                    | 监视磁盘的入站和出站流量                                                                                                                                                                                   |
| **reset-counters**                     | 重置 _/interface print stats_ 计数器                                                                                                                                                                       |

## 实例

## 格式化连接的存储单元-简单

1. 磁盘已连接，并且已经被系统自动挂载。

    ```shell
    [admin@MikroTik]  > /disk print
     0 disk1 usb-flash   ext4   00     7.1GiB     7.2GiB
    [admin@MikroTik] > / file print
     2 skins                       directory          jan /01/1970 03:00:01
     3 pub                         directory          feb /04/1970 21:31:40
     4 disk1                       disk               apr /20/2015 14:05:16 
    ```

2. 卸载存储驱动器，以便进行格式化。

    `[admin@MikroTik] > /disk eject-drive 0`。

3. 格式化磁盘，在两个支持的文件系统ext4或fat32中选择一个。

    ```shell
    [admin@MikroTik] > /disk format-drive 0 file-system=ext4 label=flashdrive
      formatted : 100%
    ```

4. 完成! 驱动器已格式化，格式化过程结束后自动安装。

## 格式化连接的存储设备 - 详细

假设你在运行RouterOS的设备上添加了一个存储设备。在这种情况下，如果存储设备是以支持的文件系统和分区记录格式化的，那么在把它插入主机设备后，就会在"/files "菜单中找到它。

如果不是则要做以下工作。

1. 快速打印磁盘菜单，确保路由器看到连接的存储设备。

`[admin@MikroTik] > disk print`
 `0 disk1        NO NAME fat32   00     6.6GiB     7.2GiB`

这里可以看到，系统找到了一个存储驱动器，而且它的格式是已知的文件系统类型。

当运行文件菜单打印输出时，可以看到它安装了。

`[admin@MikroTik] > file print`
 `0 disk1    disk         apr /20/2015 13:44:11`
 `1 skins    directory    jan /01/1970 03:00:01`
 `2 pub      directory    feb /04/1970 21:31:40`

2. 为了格式化硬盘-用以前知道的ID或名称（插槽）和想要的文件系统（ext4或fat32）发布命令，也可以像这个例子中做的那样给设备指定标签。

`[admin@MikroTik] > /disk format-drive 0 file-system=ext4 label=usb-flash`
  `formatted : 100%`

**注意：** 在打印输出中，可以看到格式化过程中有一个进度百分比。对于较大的驱动器，这个过程可能需要更长的时间才能完成，所以要有耐心。

## Web-Proxy 缓存配置示例

在IP-> Proxy菜单下输入代理缓存路径，在文件菜单中自动创建网络代理存储。如果用一个不存在的目录路径，也会自动创建一个额外的子目录。

```shell
[admin@MikroTik] > /ip proxy set cache-path =disk3/cache-n-db/proxy/
...
`[admin@MikroTik] > / file print
 0 skins                                             directory                             mar /02/2015 18:56:23
 1 sys-note.txt                                      .txt file                        23   jul /03/2015 11:40:48
 2 disk3                                             disk                                  jul /03/2015 11:35:05
 3 disk3 /lost+found                                  directory                             jul/03/2015 11:34:56
 4 disk3 /cache-n-db                                  directory                             jul/03/2015 11:41:54
 4 disk3 /cache-n-db/proxy                            web-proxy store                       jul/03/2015 11:42:09
```

## 磁盘上的日志配置示例

当配置磁盘上的日志时，确保手动创建想存储日志文件的目录，因为在这种情况下，不存在的目录将不会被自动创建。

```shell
[admin@MikroTik] > /system logging action set disk disk-file-name =/disk3/log/syslog
...
`[admin@MikroTik] > / file print where name~ "disk3/log"
 0 disk3 / log                                         directory                             jul /03/2015 12:44:09
 1 disk3 /log/syslog.0.txt                            .txt file                         160 jul /03/2015 12:44:11
```

**注意：** 日志主题，如防火墙、网络代理和其他一些倾向于在系统NAND磁盘上保存大量或快速打印日志的主题，可能会导致磁盘更快地磨损，在这种情况下，建议使用一些附加存储或远程日志，或将数据保存在RAM文件夹中。

## 为文件夹分配RAM

从7.7版本开始，可以添加链接到RAM文件夹。文件夹将在重启或断电时被清空。
RAM将被填充到tmpfs-max-size，如果没有提供这个变量，则填充到可用RAM的1/2。

`[admin@MikroTik] > /disk add type =tmpfs tmpfs-max-size =100M slot =RAM`
`[admin@MikroTik] > file print`
`Columns : NAME, TYPE, SIZE, CREATION-TIME`
`0  RAM             disk                dec /12/2022 11:01:48`
