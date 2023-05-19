# 概述

在ARM、ARM64、MIPS、TILE和PowerPC RouterBOARD类型的设备上支持分区。

可以对NAND闪存进行分区，允许在每个分区上安装自己的操作系统，并指定主分区和备用分区。

如果一个分区由于某种原因(升级失败、引入了有问题的配置、软件问题)而失败，则会引导下一个分区。这可以用作交互式备份，在其中保留经过验证的工作安装，并仅升级某些辅助分区。如果您升级了配置，并且它被证明是好的，您可以使用“保存配置”按钮将其复制到其他分区。

NAND的重新分区需要最新的引导加载程序版本

最小分区大小:

- 在MIPS上为32MB
- PowerPC上为40MB
- TILE上为48MB

允许的最大分区数是8。

```shell
[admin@1009up] > /partitions/print
Flags: A - ACTIVE; R - RUNNING
Columns: NAME, FALLBACK-TO, VERSION, SIZE
# NAME FALL VERSION SIZE
0 AR part0 next RouterOS v7.1beta4 Dec/15/2020 15:55:11 128MiB
```

# 命令

| 属性                                      | 说明                                                             |
| ----------------------------------------- | ---------------------------------------------------------------- |
| **repartition** (_integer_)               | 将重启路由器并重新格式化NAND，只留下活动分区。                   |
| **copy-to** (_\<partition\>_)             | 将运行的操作系统克隆到指定分区。以前存储在分区上的数据将被擦除。 |
| **save-config-to** (_\<partition\>_)      | 在指定分区上克隆 **running-config** 。其他的不动。               |
| **restore-config-from** (_\<partition\>_) | 从指定分区复制配置到运行的分区                                   |

# 属性

| 属性                                                                              | 属性                                                                                                              |
| --------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| **name** (_string_; Default: )                                                    | 分区名称                                                                                                          |
| **fallback-to** (_etherboot    \| next \| \<partition-name\>_; Default: **next**) | 如果活动分区启动失败怎么办:<br>- **etherboot** -切换到etherboot<br>- **next** -尝试下一个分区<br>- 回退到指定分区 |

**只读属性**

| 属性                      | 说明                         |
| ------------------------- | ---------------------------- |
| **active** (_yes \| no_)  | 分区激活                     |
| **running** (_yes\| no_)  | 当前正在运行的分区           |
| **size** (_integer[MiB]_) | 分区大小                     |
| **version** (_string_)    | 分区上安装的当前RouterOS版本 |