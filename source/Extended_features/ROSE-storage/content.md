# 概述  

**Packages required:** `rose-storage`

**ROSE -** 软件包为RouterOS增加了额外的企业数据中心功能-用于支持磁盘监控、改进的格式化、RAID、rsync、iSCSI、NVMe over TCP、NFS和改进的SMB。该功能目前支持 **arm、arm64、x86** 和 **tile** 平台。

## 属性

| 属性                    | 说明 |
| ----------------------- | ---- |
| iscsi-address           |      |
| iscsi-export            |      |
| iscsi-iqn               |      |
| iscsi-port              |      |
| nfs-address             |      |
| nfs-export              |      |
| nfs-share               |      |
| nvme-tcp-address        |      |
| nvme-tcp-export         |      |
| nvme-tcp-name           |      |
| nvme-tcp-port           |      |
| raid-chunk-size         |      |
| raid-device-count       |      |
| raid-master             |      |
| raid-max-component-size |      |
| raid-member-failed      |      |
| raid-role               |      |
| raid-type               |      |
| slot                    |      |
| smb-address             |      |
| smb-export              |      |
| smb-password            |      |
| smb-share               |      |
| smb-user                |      |
| type                    |      |

## 分区

从RouterOS 7.8beta3支持GPT分区。

添加500MB的分区:

`/disk `

`disk add type =partition parent =sata1 partition-size =500M`。

如果下一个分区被添加，将自动分配到开始的可用空间。

分区也可以用偏移量来添加。

`/disk`

`add type =partition parent =sata1 partition-size =500M partition-offset =10G`

如果分区重叠，RouterOS将返回错误。

## RAID

RAID（独立磁盘冗余阵列）技术允许把数据存储在多个驱动器上-通过组合成逻辑单元来提高数据传输性能、数据保护或两者兼备。

## RAID级别

RouterOS支持软件RAID级别0、1、4、5、6、线性和嵌套RAID。

### RAID 0

所有的数据都均匀地写在这个RAID所有的磁盘上，这种配置不提供任何容错，但提供最好的性能。

### RAID 1

相同的数据被写入所有的硬盘（数据是镜像的），这种配置提供了最好的容错能力，但是从性能上讲，写入速度与阵列中最慢的磁盘相同。

### RAID 4
  
块级数据被条带化到专用磁盘上，其中存储有奇偶校验位。性能将被限制在奇偶校验的写入速度上。

### RAID 5
  
区块级数据被均匀地分到可用的磁盘上。可以从一个磁盘故障中恢复。

### RAID 6
  
块级数据在可用的磁盘上被均匀地条带化。可以从2个磁盘的故障中恢复。

### 线性
  
数据添加在多个磁盘上，并合并为一个大磁盘。不提供冗余，并且仅限于单盘读写速度。

### 嵌套式RAID

多个RAID配置组合成其他RAID。例如，RAID 10 (RAID 1+0) 结合了磁盘镜像 (RAID 1) 和磁盘条带化 (RAID 0)

## RAID配置

在这个例子中，用10个磁盘创建RAID 6。 
磁盘必须是相同大小的，或者必须被设置为相同大小的分区，或者使用raid-max-component-size参数来限制更大的卷的大小以匹配其他元素。

理论上，为了优化RAID性能--要用正确的跨度和条带宽度。这些都取决于RAID的 "raid-chunk-size"、文件系统的块大小和磁盘的数量。

`stride =raid-chunk-size/block_size`

`stripe_width =disks*stride`

在格式化本地RAID设备时，RouterOS会自动执行。

创建RAID设备。

`/disk add type =raid raid-type =6 raid-device-count =10 slot =raid1`。

在这个RAID中添加磁盘。

`/disk set pcie1-nvme1 raid-master =raid1 raid-role =0`

`/disk set pcie1-nvme2 raid-master =raid1 raid-role =1`

`/disk set pcie1-nvme3 raid-master =raid1 raid-role =2`

`/disk set pcie1-nvme4 raid-master =raid1 raid-role =3`

`/disk set pcie1-nvme5 raid-master =raid1 raid-role =4`

`/disk set pcie1-nvme6 raid-master =raid1 raid-role =5`

`/disk set pcie1-nvme7 raid-master =raid1 raid-role =6`

`/disk set pcie1-nvme8 raid-master =raid1 raid-role =7`

`/disk set pcie1-nvme9 raid-master =raid1 raid-role =8`

`/disk set pcie1-nvme10 raid-master =raid1 raid-role =9`

其中 pcie1-nvme/* 是本地磁盘插槽名称

强烈建议手动设置 "raid-role "。如果设备以前从未设置过RAID，那么超级区块是空的，RAID-角色将自动假定，如果没有，且该角色已经被占用，那么在使用相同的RAID角色时可能会出现错误。

现在RAID将被同步。

```shell
/disk print detail

...

20 bM      type =raid slot = "raid1" slot-default = "" parent =none device = "md0" uuid = "3b4d4ec9-e7413ae8-37e7e397-9cd9152e"

           fs =ext4 model = "RAID5 1-parity-disk" size =8 641 770 946 560 free =8 572 463 624 192 raid-type =5

           raid-device-count =10 raid-max-component-size =none raid-chunk-size =1M raid-master =none

           raid-state = "clean, resync =  1.8% (17498368/937692160) finish=45.2min speed=339148K/sec"

           nvme-tcp-export =no iscsi-export =no nfs-export =no smb-export =no
```

## iSCSI

[iSCSI](https://en.wikipedia.org/wiki/iSCSI "wikipedia:iSCSI") 允许通过基于IP的网络访问存储。在启动器上，iSCSI设备将显示为块设备。RouterOS同时支持目标和启动器模式。

目标（主机）配置。

`/disk`

`set pcie1-nvme1 iscsi-export =yes`

发起人（客户）:

`/disk`

`add type =iscsi iscsi-address =192.168.1.1 iscsi-iqn =pcie1-nvme1`

iscsi-iqn要和目标设备的插槽名称相匹配，iscsi-address是目标地址。

## NFS

[NFS](https://en.wikipedia.org/wiki/Network_File_System) 允许通过网络共享本地目录。RouterOS目前只支持NFS v4模式。

主机配置。

`/disk`

`set pcie1-nvme1 nfs-export =yes`

发起人（客户）:  

**RouterOS**

`/disk`

`add type =nfs nfs-address =192.168.1.1`

**Linux:**

`mkdir /mnt/files`

`mount -t nfs 192.168.1.1:/ /mnt/files`

## SMB

[SMB](https://en.wikipedia.org/wiki/Network_File_System) 是流行的文件共享协议。ROSE软件包目前支持SMB2.1 SMB3.0, SMB3.1.1方言（由于安全漏洞，不支持SMB1）。

RouterOS还支持没有ROSE包的旧版SMB-- [SMB](https://help.mikrotik.com/docs/display/RKB/SMB)，支持传统的协议。
  
主机配置:

`/disk`

`set pcie1-nvme1 smb-export =yes`

发起人（客户）:

`/disk`

`add type =smb smb-address =192.168.1.1 smb-share =pcie1-nvme1`

smb-share需要与目标设备上的插槽名称匹配，smb-address是目标地址。

## NVMe over TCP

[nvme-tcp](https://en.wikipedia.org/wiki/Network_File_System) 允许在启动器侧作为NVMe块设备通过网络访问存储。在目标端，该设备可以是硬盘/ssd/nvme，甚至是raid阵列。

目标（主机）配置:

`/disk`

`set pcie1-nvme2 nvme-tcp-export =yes nvme-tcp-port =4420`

发起人（客户）: 

**RouterOS**

`/disk`

`add type =nvme-tcp nvme-tcp-address =192.168.1.1 nvme-tcp-name =pcie1-nvme1`

nvme-tcp-name要和目标设备上的插槽名称匹配。

**Linux**

加载内核模块

发现可用的nvme-tcp目标。

`nvme discover -t tcp -a 192.168.1.1 -s 4420`

`Discovery Log Number of Records 1, Generation counter 2`

`=====Discovery Log Entry 0======`

`trtype:  tcp`

`adrfam:  ipv4`

`subtype: nvme subsystem`

`treq:    not specified, sq flow control disable supported`

`portid:  4420`

`trsvcid: 4420`

`subnqn:  pcie1-nvme1`

`traddr:  10.155.166.7`

`sectype: none`

subnqn要和插槽名称相匹配，并作为-n参数使用。:

`nvme connect -t tcp -a 192.168.1.1 -s 4420 -n pcie1-nvme1`

块设备现在可用：

`ls /dev/nvme *`

`/dev/nvme0`  `/dev/nvme0n1`  `/dev/nvme-fabrics`

## RAMdisk

RAMdisk - 允许使用RAM的一部分作为连接设备(块设备)。与tmpfs相比，它允许把RAM作为raid的一部分，或者其他任何需要设备。

`/disk`

`disk add type =ramdisk ramdisk-size =500M`

重启或断电时，RAMdisk将被清空

## 数据加密

目前RouterOS支持SED（自加密驱动器）和dm\_crypt驱动器加密。

## 自加密驱动器

为了使用SED--硬盘必须是 [Opal](https://en.wikipedia.org/wiki/Opal_Storage_Specification) 兼容的。在购买驱动器之前，请查阅驱动器制造商的文档以了解驱动器是否支持这一功能。
RouterOS为支持的驱动器添加了 **o（支持非活动）** 或 **O（支持活动）** 标志。

`/disk print`

`Flags : B - BLOCK-DEVICE; M, F - FORMATTING; o - TCG-OPAL-SELF-ENCRYPTION-SUPPORTED`

`Columns : SLOT, MODEL, SERIAL, INTERFACE, SIZE, FREE, FS, RAID-MASTER`

`0 BMo sata1  Samsung SSD 860 2.5in  S3Z9NX0N414510L  SATA 6.0 Gbps  1 000 204 886 016  983 351 111 680  ext4  none`

`1 BMo sata2  Samsung SSD 860        S5GENG0N307602J  SATA 6.0 Gbps  1 000 204 886 016  983 351 128 064  ext4  none`

`2 BMO sata3  Samsung SSD 860        S5GENG0N307604H  SATA 6.0 Gbps  1 000 204 886 016  983 351 128 064  ext4  none`

`3 BMO sata4  Samsung SSD 860 2.5in  S4CSNX0N838150B  SATA 6.0 Gbps  1 000 204 886 016  983 351 128 064  ext4  none`

设置TCG-OPAL-SELF-ENCRYPTION方法:

`/disk`

`disk set sata1 self-encryption-password =securepassword`

设置:

`/disk`

`disk unset sata1 self-encryption- password`

或

`/disk`

`disk set sata1 !self-encryption- password`

## 块设备加密

...

## 文件同步

ROSE软件包还包括文件上传/下载和同步工具。 
同步（推送）本地文件夹内容到其他RouterOS设备：

`/ file sync add local-path =pcie1-nvme1/myfolder/ remote-addrs =192.168.1.1 mode =upload user =admin password = "" remote-path =test/`。

user/password - 其他设备的用户名和密码。互连时Winbox端口要打开。

或用命令拉取文件：

`/ file sync add local-path =pcie1-nvme1/myfolder/ remote-addrs =192.168.1.1 mode =download user =admin password = "" remote-path =test/`

文件夹现在可以同步了，所有对文件的修改都会在设备之间同步。

文件夹不要下载和上传到同一个目标，避免未定义的行为。
