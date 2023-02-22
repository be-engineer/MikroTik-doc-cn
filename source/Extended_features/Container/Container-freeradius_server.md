# freeradius服务器介绍

在RouterOS中引入容器功能，使得在路由器内运行各种任务的各种服务器成为可能。这对那些想减少网络中设备数量的人来说尤其重要。与其在一个单独的设备/机器上运行服务器，为什么不在路由器内运行呢？

[Radius](https://help.mikrotik.com/docs/display/ROS/RADIUS) 是远程认证拨入用户服务的简称。RouterOS支持RADIUS客户端功能，可以对HotSpot、[PPP](https://help.mikrotik.com/docs/display/ROS/PPP)、[PPPoE](https://help.mikrotik.com/docs/display/ROS/PPPoE)、[PPTP](https://help.mikrotik.com/docs/display/ROS/PPTP)、[L2TP](https://help.mikrotik.com/docs/display/ROS/L2TP)和ISDN连接进行认证。这个功能可以将RouterOS连接到Radius服务器，然后，利用服务器的用户数据库进行客户端认证。

在这个例子中将展示 **[freeradius/freeradius-server](https://hub.docker.com/r/freeradius/freeradius-server/tags)** 镜像安装。

## 概述

**Sub-menu:** `/container`

**注意**: 需要 **container** 包.

在进行配置之前，请务必研究 [容器](https://help.mikrotik.com/docs/display/ROS/Container) 指南。确保检查 [免责声明](https://help.mikrotik.com/docs/display/ROS/Container#Container-Disclaimer) 和 [要求](https://help.mikrotik.com/docs/display/ROS/Container#Container-Requirements) 部分，以了解风险和可能需要做的必要步骤。

在本指南发布之时，该镜像仅适用于linux/ **amd64** 操作系统/架构。这意味着无法在arm32位和arm64位架构的RouterOS设备上运行这个方案。对于arm64需要从 [FreeRADIUS source](https://github.com/FreeRADIUS/freeradius-server) 制作自己的容器。

**你只能在** [云主机路由器(CHR)](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=18350234)，或x86安装上运行。

为了在 [Virtual Box](https://www.virtualbox.org/) 中设置一个CHR，请查看 [youtube教程](https://www.youtube.com/watch?v=oHXkaHkSVVo)，或 [自己制作x86路由器](https://www.youtube.com/watch?v=JpccW9tYOkQ)。

本指南演示了一个基本例子! 测试是在本地环境下进行的! 本指南用于基本的RADIUS "测试 "目的! 并非所有的 "freeradius "功能都被测试了!

## 配置

## 容器模式：

启用容器模式:

`/system/device-mode/update container=yes`

如果在X86上使用容器，要通过冷重启来确认设备模式。

## 网络

为容器添加 veth 接口：

`/interface/veth/ add name =veth3 address =172.17.0.2/24 gateway =172.17.0.1`。

为容器创建一个网桥，给它分配一个 IP 网络，并将 veth 添加到网桥上：

`/interface/bridge/ add name =dockerfreeradius`

`/ip/address/ add address =172.17.0.1/24 interface =dockerfreeradius`

`/interface/bridge/port add bridge =dockerfreeradius interface =veth3`

如果需要的话，为外发流量设置NAT:

`/ip/firewall/nat/ add chain =srcnat action =masquerade src-address =172.17.0.0/24`

## 获取镜像

为了简化配置，从外部库中获取镜像，也可以通过 [.tar](https://help.mikrotik.com/docs/display/ROS/Container#Container-b)importimagefromPC) 文件导入。

确保有相应的 "注册表URL"设置，限制RAM的使用（如果需要），并为镜像设置一个目录。

用命令拉出镜像:

`/container/ add remote-image =freeradius/freeradius-server:latest interface =veth3 root-dir =freeradius logging =yes cmd = "-X"`

其中 `cmd="-X"` 启用调试日志（根据 "freeradius "文档）。

运行命令后，RouterOS应该开始 "提取"软件包。检查 "文件系统 "是否新创建的文件夹，并使用 `/container/print` 命令监控容器状态。

## 启动容器

确定容器已经添加并且在使用 `/container/print` 后状态变为 `status=stopped` 后，可以启动了。

## 更改服务器的配置文件

为了访问服务器的配置文件（**clients.conf** 和 **authorize**），需要用SFTP（通过SSH传输文件）协议，所以要确保SSH [service](https://help.mikrotik.com/docs/display/ROS/Services) 已启用。

打开命令终端（"CMD"，以管理员身份，适用于Windows用户，或 "Linux Shell或命令终端"，适用于Linux用户），导航到想下载配置文件的目录。例如到 "桌面 "上的 "radius "文件夹。

`C:\WINDOWS\system32> cd C:\Users\Administrator\Desktop\radius`

`C:\Users\Administrator\Desktop\radius>`

启动SFTP到设备的IP地址:

`C:\Users\DenissPC\Desktop\radius>sftp admin@10.55.8.53`

`admin@10.55.8.53's password:`

`Connected to 10.55.8.53.`

`sftp>`

进入服务器的配置文件文件夹（使用 `dir` 或 `ls` 命令查看你所在的文件夹的内容，使用 `cd` 命令进入选择的文件夹）。

第一个文件，"client.conf "可以定义RADIUS客户端。根据 "freeradius "文档，它应该在"/etc/freeradius "目录下......所以，导航到那里并使用 `get` 命令下载它。

`sftp> dir`

`freeradius          pub                     pull                    skins`                  

`sftp> cd freeradius/etc/freeradius`

`sftp> dir`

`README.rst          certs               clients.conf        dictionary          experimental.conf   hints`

`huntgroups          mods -available`      `mods -config`         `mods -enabled`        `panic.gdb           policy.d`

`proxy.conf          radiusd.conf        sites -available`     `sites -enabled`       `templates.conf      trigger.conf`
`users`

`sftp> get clients.conf`

`Fetching /freeradius/etc/freeradius/clients.conf to clients.conf`

`/freeradius/etc/freeradius/clients.conf                                               100% 8323     1.2MB/s   00:00`

用喜欢的文本编辑器（记事本或任何其他）打开 "**clients.conf**"。可以研究这个文件，看看可用的所有选项(另外，请查看 [freeradius.org](https://wiki.freeradius.org/config/Configuration-files))。这个例子显示了一个基本设置，将用下面的行来覆盖整个文件:

```shell
client new {
    ipaddr = 0.0.0.0/0
    secret = client_password
}
```

radius客户端可以使用任何可能的IP地址进行连接（**ipaddr=0.0.0.0/0** 确保了这一点，如果需要，也可以改为radius客户端的实际IP地址/掩码），秘密是 "client/password"（可以改为任何其他秘密）。

保存该文件。

第二个文件，"authorize "允许设置用户。根据 "freeradius "文档，应该在"/etc/freeradius/mods-config/files "下。去那里"找到"该文件:

`sftp> dir`

`freeradius          pub                     pull                    skins`

`sftp> cd freeradius/etc/freeradius/mods -config /files`

`sftp> dir`

`accounting  authorize   dhcp        pre -proxy`

`sftp> get authorize`

`Fetching /freeradius/etc/freeradius/mods -config /files/authorize to authorize`

`/freeradius/etc/freeradius/mods -config /files/authorize                                100% 6594     1.1MB/s   00:00`

用文本编辑器（记事本或任何其他）打开 "**authorize**" 。这个例子显示了一个基本的设置，只需取消注释（删除 "#"符号）下面显示的行（其余的配置/行保持原样）。

`bob Cleartext-Password := "hello"`

创建一个用户名 "bob"，并将密码设置为 "hello"（可以改变用户名和密码）。

保存文件。

用 `put` 命令把两个文件上传覆盖默认文件:

`sftp> dir`

`freeradius          pub                     pull                    skins`

`sftp> cd freeradius/etc/freeradius`

`sftp> dir`

`README.rst          certs               clients.conf        dictionary          experimental.conf   hints`

`huntgroups          mods -available`      `mods -config`         `mods -enabled`        `panic.gdb           policy.d`

`proxy.conf          radiusd.conf        sites -available`     `sites -enabled`       `templates.conf      trigger.conf`

`users`

`sftp> put clients.conf`

`Uploading clients.conf to /freeradius/etc/freeradius/clients.conf`

`clients.conf                                                                          100%   67    22.3KB/s   00:00`

`sftp> cd mods -config /files`

`sftp> dir`

`accounting  authorize   dhcp        pre -proxy`

`sftp> put authorize`

`Uploading authorize to /freeradius/etc/freeradius/mods -config /files/authorize`

`authorize                                                                             100% 6626     1.6MB/s   00:00`

重启容器:

`/container/stop 0`

`/container/start 0`

确保容器已停止（使用 `/container/print` 命令后应显示 `status=stopped`），然后再启动它。

## 结果验证

在RouterOS中，添加一个新的RADIUS客户端配置。

`/radius/ add service =login address =172.17.0.2 secret = "client_password"`.

,其中 `address` 是veth3接口的IP地址，`secret` 是我们在 **clients.conf** 文件中配置的秘密，`service` 是希望使用的服务。

通过命令用RADIUS用户 "登录"。

`/user/aaa/ set use-radius =yes`

已经允许RADIUS的 "登录"服务，可以用ssh/winbox/webfig连接来测试。对于SSH测试，发出命令（要指出设备的管理IP，然后输入bob的密码 "hello"）。

`/system/ssh 10.55.8.53 user=bob`

可以证实终端用户从 "admin@MikroTik "变成了 "bob@MikroTik":

```shell
[admin@MikroTik] > /system/ssh 10.55.8.53 user=bob
password :hello
  MMM      MMM       KKK                          TTTTTTTTTTT      KKK
  MMMM    MMMM       KKK                          TTTTTTTTTTT      KKK
  MMM MMMM MMM  III  KKK  KKK  RRRRRR     OOOOOO      TTT     III  KKK  KKK
  MMM  MM  MMM  III  KKKKK     RRR  RRR  OOO  OOO     TTT     III  KKKKK
  MMM      MMM  III  KKK KKK   RRRRRR    OOO  OOO     TTT     III  KKK KKK
  MMM      MMM  III  KKK  KKK  RRR  RRR   OOOOOO      TTT     III  KKK  KKK
  MikroTik RouterOS 7.8alpha173 (c) 1999-2023       https ://www.mikrotik.com/
Press F1 for help
[bob@MikroTik] >
```

如果发出命令 `/user/active/print`:

`/user/active/ print`

`Flags : R - RADIUS`

`Columns : WHEN, NAME, ADDRESS, VIA`

`0   feb /16/2023 16:31:21  admin  xx.xx.xx.xx  winbox`

`1   feb /16/2023 16:38:46  admin  xx.xx.xx.xx  console`

`2 R feb /16/2023 16:38:53  bob    10.55.8.53  ssh`

可以验证一个新的用户 "bob "是 "活动的"，并且有一个 "R "标志，表明是一个RADIUS用户。
