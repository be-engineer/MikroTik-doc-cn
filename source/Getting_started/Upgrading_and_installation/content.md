## 概述

MikroTik 设备预装了 RouterOS，因此通常不需要安装，除非在 x86 PC 上安装 RouterOS。 已安装设备的升级过程非常简单。

## 版本编号说明

RouterOS版本是按顺序编号的，当用句号来分隔序列时，它不代表小数点，而且序列没有位置意义。例如，2.5的标识符不是 "两个半 "或 "第三个版本的一半"，它是第二个一级版本的第五个二级版本。因此，v5.2比v5.18要老，而v5.18要新。

RouterOS 版本在几个“发布链”中发布：长期版、稳定版和测试版。 升级 RouterOS 时，您可以选择要从中安装新软件包的发布链。

- **长期版**：很少发布，只包含最重要的修复，在一个分支内升级，不添加新功能。 当一个 **稳定版** 版本已经发布了一段时间并且看起来足够稳定时，它会被提升到 Long Term 分支，取代旧版本，然后将其移至 Archive。 这就连续地添加了新特性。
- **稳定版**：每几周发布一次，包括所有经过测试的功能和修复。
- **测试版**：每隔几天发布一次，只进行基本的内部测试，不应在生产中使用。

![](https://help.mikrotik.com/docs/download/attachments/328142/Metro-systemv2.png?version=1&modificationDate=1570173132346&api=v2)

## 标准升级

软件包升级功能连接到 MikroTik 下载服务器，并检查是否有适用于您的设备的新 RouterOS 版本。

单击 QuickSet 或软件包菜单中的升级按钮后，升级窗口将打开，其中包含当前更新日志（如果存在更新版本）以及下载和安装最新版本的按钮。

通过单击“Download & Upgrade”开始下载，下载成功后将重新启动以安装下载的软件包。 即使安装了自定义包，下载程序也会下载所有必要的包。

![](https://help.mikrotik.com/docs/download/attachments/328142/Quickset-upgrade.jpg?version=1&modificationDate=1570170624131&api=v2)

![](https://help.mikrotik.com/docs/download/attachments/328142/Package-upgrade.png?version=1&modificationDate=1570170634222&api=v2)

![](https://help.mikrotik.com/docs/download/attachments/328142/Changelog-upgrade.png?version=1&modificationDate=1570170774194&api=v2)

## 手动升级

您可以通过以下方式升级 RouterOS：

- Winbox – 将文件拖放到**File**菜单
- WebFig - 从**File**菜单上传文件
- FTP - 上传文件到根目录
- The Dude – [在这里查看手册](https://wiki.mikrotik.com/wiki/Upgrading_RouterOS_with_Dude   "Upgrading RouterOS with Dude")

!!! info RouterOS 不能通过串口线升级。 只有 [RouterBOOT](https://wiki.mikrotik.com/index.php?title=Bootloader_upgrade&action=edit&redlink=1 "Bootloader upgrade (page does not exist)") 可使用此方法升级。

### 手动升级过程

- 第一步 - 访问 [www.mikrotik.com](https://www.mikrotik.com/) 并前往下载页面，选择安装 RouterOS 的系统类型。
- 下载**Combined package**，它包括 RouterOS 的所有功能

#### 使用 Winbox

选择您的系统类型，并下载升级包。 使用 Winbox 连接到路由器，用鼠标选择下载的文件，然后将其拖到**File**菜单。 如果已经存在一些文件，请确保将包放在根菜单中，而不是热点文件夹中！ 开始上传。

![](https://help.mikrotik.com/docs/download/attachments/328142/Winb2.jpg?version=1&modificationDate=1585911212956&api=v2)

完成后 - 重新启动设备。 新版本号将显示在 Winbox 标题和包菜单中

#### 使用 FTP

- 打开您最喜欢的 FTP 程序（在本例中为 [Filezilla](https://filezilla.sourceforge.net/)），选择升级包上传到路由器 ( [demo2.mt.lv](https://demo2.mt.lv/) 是本例中我的路由器的地址。请注意，图片中正在上传多个包，在您的情况下 - 将只有一个包含所有包的文件
- 可以检查文件是否已成功传输到路由器上（可选）：

`[normis@Demo_v2.9] >``file` `print`

 `0 supout.rif             .rif` `file`             `285942     nov``/24/2005 15:21:54`

 `1 dhcp-2.9.8.npk         package               138846     nov``/29/2005 09:55:42`

 `2 ppp-2.9.8.npk          package               328636     nov``/29/2005 09:55:43`

 `3 advanced-tools-2.9.... package               142820     nov``/29/2005 09:55:42`

 `4 web-proxy-2.9.8.npk    package               377837     nov``/29/2005 09:55:43`

 `5 wireless-2.9.8.npk     package               534052     nov``/29/2005 09:55:43`

 `6 routerboard-2.9.8.npk  package               192628     nov``/29/2005 09:55:45`

 `7 system-2.9.8.npk       package               5826498    nov``/29/2005 09:55:54`

```

```

-   重启路由器后升级过程开始:

```
[normis@Demo_v2.9] > system reboot
Reboot, yes? [y/N]: y

```

-   重启后，您的路由器将是最新的，您可以在此菜单中查看：

```
/system package print

```

-   如果您的路由器未正确升级，请检查 **log**信息

```
/log print without-paging

```

## RouterOS 批量升级

您只需点击几下即可升级多个 MikroTik 路由器。 让我们看一下具有 3 个路由器的简单网络（同样的方法适用于具有无限数量路由器的网络）

#### RouterOS 自动升级

**Sub-menu:** `/system package update`

您可以通过在系统调度程序中运行脚本来自动执行升级过程。 该脚本向 MikroTik 升级服务器查询新版本，如果收到的响应为“新版本可用”，则该脚本会发出升级命令：

`/system package update`

`check-for-updates once`

`:` `delay` `3s;`

`:` `if` `( [` `get` `status]` `=` `"New version is available"` `)` `do` `=` `{` `install` `}`

___

  
RouterOS 可以从远程 MikroTik 路由器下载软件包。

- 将一个路由器作为网络升级中心点，更新其他路由器上的 MikroTik RouterOS。
- 将必要的 RouterOS 包上传到此路由器（示例中RB751U 的 mipsbe 和 RB1100AHx2 的 PowerPC）。
- 将升级路由器（192.168.100.1）信息添加到要更新的路由器（192.168.100.253），需要设置IP地址/用户名/密码
- 点击刷新查看可用的软件包，下载最新的软件包并重启路由器以完成升级。

#### The Dude 自动升级

Dude 应用程序可以帮助您通过单击每个路由器来升级整个 RouterOS 网络。

- 为您的 Dude 地图上任何您想要自动升级的设备设置类型和 **RouterOS** 的正确密码，
- 将所需的 RouterOS 包上传到 Dude 文件
- 从 RouterOS 列表升级设备上的 RouterOS 版本。 升级过程是自动的，点击升级（或强制升级）后，包将上传，路由器将由 Dude 自动重启。

#### The Dude 分层升级

对于复杂的网络，当路由器依次连接时，最简单的例子就是1router-2router-3router连接。 您可能会遇到一个问题，2router 会在将包上传到 3router 之前重新启动。 解决方案是Dude groups，该功能允许对路由器进行分组并一键升级所有路由器！

- 选择组并单击升级（或强制升级）

## 许可证问题

从旧版本升级时，您的许可证密钥可能会出现问题。 可能的场景：

- 从 RouterOS v2.8 或更早版本升级时，系统可能会抱怨升级时间已过。 请使用 Netinstall 进行升级。 Netinstall 将忽略旧的许可证限制并升级

- 升级到 RouterOS v4 或更新版本时，系统会要求您将许可证更新为新格式。 为此，请确保您的 Winbox PC（而非路由器）具有有效的互联网连接，并且没有任何限制访问 [www.mikrotik.com](https://www.mikrotik.com/)，然后在许可证菜单中单击“update license” 。

## 建议

使用 RouterBOARD 设备时，始终建议在升级 RouterOS 后升级其 RouterBOOT 引导加载程序。 为此，请用命令“_/system routerboard upgrade_”

## 网络安装

[NetInstall](https://help.mikrotik.com/docs/display/ROS/Netinstall)是最常用的安装工具。 它可以在Windows 机器或带有 Wine 的 Linux 上运行（需要超级用户权限）。

您可以在 [www.mikrotik.com](https://www.mikrotik.com/download) 下载 [NetInstall](https://help.mikrotik.com/docs/display/ROS/Netinstall)。

[NetInstall](https://help.mikrotik.com/docs/display/ROS/Netinstall) 也用于在先前安装失败、损坏或访问密码丢失的情况下重新安装 RouterOS。

您的设备必须支持从以太网启动，并且必须有从 [NetInstall](https://help.mikrotik.com/docs/display/ROS/Netinstall) 计算机到目标设备的直接以太网连接。 所有 RouterBOARD 都要支持 PXE 网络启动，如果 RouterOS 可操作，则必须在 RouterOS“routerboard”菜单中启用，或者在引导加载程序设置中启用。 为此，您需要一根串口线。
**注意：**对于没有串口，没有RouterOS接入的RouterBOARD设备，reset键也可以启动PXE启动模式。 有关详细信息，请参阅 RouterBOARD 手册。

[NetInstall](https://help.mikrotik.com/docs/display/ROS/Netinstall) 也可以直接在连接到 Netinstall Windows 机器的磁盘 (USB/CF/IDE/SATA) 上安装 RouterOS。 安装后只需将磁盘移动到路由器机器并从中启动。

#### 用户界面

[NetInstall](https://help.mikrotik.com/docs/display/ROS/Netinstall) 窗口中提供以下选项：

- **路由器/驱动器** - PC 驱动器和 PXE 引导的路由器列表。 从列表中选择要安装 RouterOS 的驱动器或路由器。
- **制作软盘** - 用于为不支持 Etherboot 的 PC 创建可引导的 1.44" 软盘。
- **网络启动** - 用于通过网络启用 PXE 启动。
- **安装/取消** - 选择路由器并选择下面的 RouterOS 包后，开始安装。
- **SoftID** - 在路由器上生成的 SoftID。 用它来购买你的密钥。
- **Key / Browse** - 在此处应用购买的密钥，或留空以安装 24 小时试用版。
- **获取密钥** - 直接从您的 [mikrotik.com](https://mikrotik.com/) 帐户获取密钥。
- **Flashfig** - 启动 Flashfig - 可在全新设备上运行的批量配置实用程序。
- **保留旧配置** - 保留路由器上的配置，只是重新安装软件（不重置）。
- **IP 地址/掩码** - 以 CIDR 表示法输入 IP 地址和网络掩码以在路由器中进行预配置。
- **网关** - 在路由器中预配置的默认网关。
- **波特率** - 在路由器中预先配置的默认串口波特率。
- **配置脚本文件** - 包含直接配置路由器的 RouterOS CLI 命令的文件（例如，由 export 命令生成的命令）。 用于应用默认配置。

  
**注意！** 不要尝试在您的系统驱动器上安装 RouterOS。 这样会格式化您的硬盘驱动器并清除现有的操作系统。

## 光盘安装

## RouterOS 安装包类型

RouterOS 支持许多不同的功能，并且由于每个安装都需要支持一组特定的功能，因此可以使用包系统添加或删除某些功能组。 因此，用户能够控制可用的功能和安装的大小。 安装包仅由 MikroTik 提供，不允许第 3 方制作。

#### 包列表

 | 包名               | 说明                                                                                            |
 | ------------------ | ----------------------------------------------------------------------------------------------- |
 | **advanced tools** | 软件包包含高级工具，如 netwatch、ip 扫描、局域网唤醒等。                                        |
 | **calea**          | 由美国“执法通信援助法”通过的特定用途的数据收集工具。                                            |
 | **dhcp**           | 动态主机控制协议客户端和服务器。                                                                |
 | **hotspot**        |
 | **ipv6**           |
 | **mpls**           | 支持多协议标签交换                                                                              |
 | **multicast**      | 支持多播PIM和IGMP 代理                                                                          |
 | **ntp**            | 网络时间协议服务                                                                                |
 | **ppp**            | 启用所有 ppp 类型隧道支持（pppoe、sstp、pptp 等）                                               |
 | **routerboard**    | 允许访问和管理 RouterBOARD 特定设置。                                                           |
 | **routing**        | 动态路由协议（OSPF、RIP、BGP）                                                                  |
 | **security**       | Ipsec, SSH, 安全 winbox                                                                         |
 | **system**         | RouterOS 核心包，启用基本路由、防火墙、接口驱动程序等。没有此包，RouterOS 无法运行              |
 | **ups**            |
 | **user-manager**   | MikroTik's RADIUS 服务器                                                                        |
 | **wireless**       | 启用无线驱动程序                                                                                |
 | **wireless-fp**    | 启用无线 802.11ac 支持                                                                          |
 | **isdn**           |
 | **lcd**            | 支持第 3 方 LCD 面板                                                                            |
 | **kvm**            | 启用 KVM 虚拟化                                                                                 |
 | **routeros**       | 组合 RouterOS 包。包括系统、热点、无线、ppp、安全、mpls、高级工具、dhcp、路由器板、ipv6、路由。 |

#### 使用包

已执行命令的操作将仅在重新启动时应用。 在此之前，用户可以自由安排或恢复设置的操作。

 | 命令           | 说明                                                               |
 | -------------- | ------------------------------------------------------------------ |
 | **disable**    | 安排包在下次重新启动后禁用。软件包提供的所有功能将无法访问。       |
 | **downgrade**  | 在重启过程中，路由器将尝试强制在路由器上安装上传的包。会提示重启。 |
 | **print**      | 输出有关已安装包的信息（版本、包状态、计划的状态更改、构建日期等） |
 | **enable**     | 计划包在下次重新启动后启用。                                       |
 | **uninstall**  | 安排要从路由器中删除的包。                                         |
 | **unschedule** | 删除计划任务                                                       |

可用包列表示例

```
  [admin@rack1_b3] /system package> print
  Flags: X - disabled
  #   NAME                    VERSION                 SCHEDULED
  0   option                  6.18
  1   routeros-tile           6.18
  2   system                  6.18
  3 X wireless-fp             6.18
  4   ipv6                    6.18
  5   wireless                6.18
  6   hotspot                 6.18
  7   dhcp                    6.18
  8   mpls                    6.18                    计划禁用
  9   routing                 6.18
  10   ppp                     6.18
  11   security                6.18
  12   advanced-tools          6.18
      
```

注意，我们已禁用 wireless-fp 包并计划禁用 mpls 包