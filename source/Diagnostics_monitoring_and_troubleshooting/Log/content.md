# 概述

RouterOS可以记录各种系统事件和状态信息。日志保存在路由器的内存（RAM）、磁盘、文件中，或通过电子邮件发送，甚至可以发送到远程系统日志服务器（RFC 3164）。

## 日志信息

**Sub-menu:** `/log`

所有存储在路由器本地存储器中的信息都可以从`/log`菜单中打印出来。每条都包含事件发生的时间和日期、消息所属的主题和消息本身。

```shell
[admin@MikroTik] /log> print
jan/02/1970 02:00:09 system,info router rebooted
sep/15 09:54:33 system,info,account user admin logged in from 10.1.101.212 via winbox
sep/15 12:33:18 system,info item added by admin
sep/15 12:34:26 system,info mangle rule added by admin
sep/15 12:34:29 system,info mangle rule moved by admin
sep/15 12:35:34 system,info mangle rule changed by admin
sep/15 12:42:14 system,info,account user admin logged in from 10.1.101.212 via telnet
sep/15 12:42:55 system,info,account user admin logged out from 10.1.101.212 via telnet
01:01:58 firewall,info input: in:ether1 out:(none), src-mac 00:21:29:6d:82:07, proto UDP,
10.1.101.1:520->10.1.101.255:520, len 452
```

如果日志是在添加日志的同一日期打印的，那么只显示时间。在上面的例子中，可以看到第二条信息是在今年9月15日添加的（没有添加年份），最后一条信息是在今天添加的，所以只显示时间。

_Print_ 命令接受几个参数，允许检测新的日志，只打印必要的信息等等。

例如，以下命令将打印所有主题为信息的日志，并检测新的日志，直到按下Ctrl+C。

```shell
[admin@MikroTik] /log > print follow where topics~".info"
12:52:24 script,info hello from script
-- Ctrl-C to quit.
```

 如果打印处于跟随模式，你可以在键盘上按下 "空格 "来插入分隔符：

```shell
[admin@MikroTik] /log > print follow where topics~".info"
12:52:24 script,info hello from script
 
= = = = = = = = = = = = = = = = = = = = = = = = = = =
 
-- Ctrl-C to quit.
```

## 日志配置

**Sub-menu level:** `/system logging`

| 属性                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | 说明                                                                                                                                                                                           |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **action** (_name_; Default: **memory**)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | 指定动作菜单中列出的系统默认动作或用户指定动作之一。                                                                                                                                           |
| **prefix** (_string_; Default: )                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | 在日志信息的开头添加前缀                                                                                                                                                                       |
| **topics** (_account, bfd, caps, ddns, dns, error, gsm, info, iscsi, l2tp, manager, ntp, packet, pppoe, radvd, rip, script, smb, sstp, system, timer, vrrp, web-proxy, async, bgp, certificate, debug, dot1x, dude, event, hotspot, interface, isdn, ldp, mme, ospf, pim, pptp, raw, route, sertcp, snmp, state, telephony, upnp, warning, wireless, backup, calc, critical, dhcp, e-mail, firewall, igmp-proxy, ipsec, kvm, lte, mpls, ovpn, ppp, radius, read, rsvp, simulator, ssh, store, tftp, ups, watchdog, write_; Default: **info**) | 记录所有指定主题或主题列表的消息。<br>**'！'** 字符可以在主题前使用，以排除属于该主题的信息。例如，我们想记录NTP的调试信息，但没有太多细节：<br>`/system logging add topics=ntp,debug,!packet` |

### 动作

**Sub-menu level:** `/system logging action`

| 属性                                                                                                                                                                                                                                             | 说明                                                                                                                                                                                                                       |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **bsd-syslog** (_yes                                                                                                                                                                           \| no_; Default: )                                | 是否使用RFC 3164中定义的bsd-syslog                                                                                                                                                                                         |
| **disk-file-count** (_integer [1..65535]_; Default: **2**)                                                                                                                                                                                       | 指定用于存储日志信息的文件数量，仅在action=disk时适用。                                                                                                                                                                    |
| **disk-file-name** (_string_; Default: **log**)                                                                                                                                                                                                  | 用于存储日志信息的文件名，仅在action=disk时适用。                                                                                                                                                                          |
| **disk-lines-per-file** (_integer [1..65535]_; Default: **100**)                                                                                                                                                                                 | 指定文件的最大行数，仅在 action=disk 时适用。                                                                                                                                                                              |
| **disk-stop-on-full** (_yes                                                                                                                                                                    \| no_; Default: **no**)                          | 在达到指定的disk-lines-per-file和disk-file-count数量后，是否停止保存日志信息到磁盘，仅在action=disk时适用。                                                                                                                |
| **email-start-tls** (_yes                                                                                                                                                                      \| no_; Default: **no**)                          | 发送电子邮件时是否使用tls，仅在action=email时适用。                                                                                                                                                                        |
| **email-to** (_string_; Default: )                                                                                                                                                                                                               | 发送日志的电子邮件地址，仅在action=email时适用。                                                                                                                                                                           |
| **memory-lines** (_integer [1..65535]_; Default: **100**)                                                                                                                                                                                        | 本地缓冲区的记录数，仅适用于 action=memory                                                                                                                                                                                 |
| **memory-stop-on-full** (_yes                                                                                                                                                                                           \| no_; Default: **no**) | 在达到指定的内存行数后，是否停止在本地缓冲区保存日志信息。                                                                                                                                                                 |
| **name** (_string_; Default: )                                                                                                                                                                                                                   | 动作名称                                                                                                                                                                                                                   |
| **remember** (_yes                                                                                                                                                                             \| no_; Default: )                                | 是否保留尚未在控制台显示的日志信息，action=echo则适用。                                                                                                                                                                    |
| **remote** (_IP\/IPv6 Address[:Port]_; Default: **0.0.0.0:514**)                                                                                                                                                                                 | 远程日志服务器的IP/IPv6地址和UDP端口，action=remote则适用。                                                                                                                                                                |
| **src-address** (_IP address_; Default: **0.0.0.0**)                                                                                                                                                                                             | 向远程服务器发送数据包时使用的源地址                                                                                                                                                                                       |
| **syslog-facility** (_auth, authpriv, cron, daemon, ftp, kern, local0, local1, local2, local3, local4, local5, local6, local7, lpr, mail, news, ntp, syslog, user, uucp_; Default: **daemon**)                                                   |
| **syslog-severity** (_alert, auto, critical, debug, emergency, error, info, notice, warning_; Default: **auto**)                                                                                                                                 | RFC 3164中定义的严重程度： <br>- 紧急情况：系统无法使用<br>- 警报：必须立即采取行动<br>- 危急：危急情况<br>- 错误：错误状况<br>- 警告：警告条件<br>- 通知：正常但重要的状况<br>- 信息性：信息性消息<br>- Debug: 调试级信息 |
| **target** (_disk, echo, email, memory, remote_; Default: **memory**)                                                                                                                                                                            | 日志信息的存储设施或目标:<br>- disk - 日志保存到硬盘中。<br>- echo - 日志显示在控制台屏幕上<br>- email - 通过电子邮件发送日志<br>- memory - 日志存储在本地内存缓冲区中<br>- remote - 日志发送到远程主机上                  |

### 主题

每条日志都有描述日志信息来源的主题。可以有一个以上的主题分配给日志信息。例如，OSPF调试日志有四个不同的主题：路由、OSPF、调试和原始。

```shell
11:11:43 route,ospf,debug SEND: Hello Packet 10.255.255.1 -> 224.0.0.5 on lo0
11:11:43 route,ospf,debug,raw PACKET:
11:11:43 route,ospf,debug,raw 02 01 00 2C 0A FF FF 03 00 00 00 00 E7 9B 00 00
11:11:43 route,ospf,debug,raw 00 00 00 00 00 00 00 00 FF FF FF FF 00 0A 02 01
11:11:43 route,ospf,debug,raw 00 00 00 28 0A FF FF 01 00 00 00 00
```

####  设备独立主题列表 

| 主题         | 说明                                                     |
| ------------ | -------------------------------------------------------- |
| **critical** | 标记为重要的日志，这些日志在每次登录时都会打印到控制台。 |
| **debug**    | 调试日志                                                 |
| **error**    | 错误信息                                                 |
| **info**     | 信息性的日志                                             |
| **packet**   | 显示收发数据包内容的日志                                 |
| **raw**      | 显示接发数据包的原始内容的日志                           |
| **warning**  | 警告信息。                                               |  |

###  各种RouterOS设备使用的主题 

| 主题            | 说明                                                                                                                                                                                                            |
| --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **account**     | 由账户产生的日志信息。                                                                                                                                                                                          |            | **async**      | 由异步设备产生的日志信息。 |
| **backup**      | 由备份创建设施产生的日志信息。                                                                                                                                                                                  |
| **bfd**         | 由BFD协议产生的日志信息                                                                                                                                                                                         |
| **bgp**         | BGP协议产生的日志信息                                                                                                                                                                                           |
| **calc**        | 路由计算日志信息。                                                                                                                                                                                              |
| **caps**        | CAPsMAN无线设备管理                                                                                                                                                                                             |
| **certificate** | 安全证书                                                                                                                                                                                                        |
| **dns**         | 名称服务器查询相关信息                                                                                                                                                                                          |
| **ddns**        | 动态DNS工具产生的日志信息                                                                                                                                                                                       |
| **dude**        | 与Dude服务器包有关的信息 The Dude工具                                                                                                                                                                           |
| **dhcp**        | DHCP客户端、服务器和中继的日志信息                                                                                                                                                                              |
| **e-mail**      | 电子邮件工具产生的信息。                                                                                                                                                                                        |
| **event**       | 路由事件产生的日志信息。例如，新的路由已经安装在路由表中。                                                                                                                                                      |
| **firewall**    | 防火墙规则中设置了 **action=log** 时产生的防火墙日志信息。                                                                                                                                                      |
| **gsm**         | 由GSM设备产生的日志信息。                                                                                                                                                                                       |
| **hotspot**     | 热点相关的日志                                                                                                                                                                                                  |
| **igmp-proxy**  | IGMP Proxy相关的日志                                                                                                                                                                                            |
| **ipsec**       | IPSec日志                                                                                                                                                                                                       |
| **iscsi**       |
|                 |
| **isdn**        |
|                 |
| **interface**   |
|                 |
| **kvm**         | 与KVM虚拟机功能相关的信息                                                                                                                                                                                       |
| **l2tp**        | 由L2TP客户端和服务器产生的日志                                                                                                                                                                                  |
| **lte**         | 与LTE/4G调制解调器配置相关的消息                                                                                                                                                                                |
| **ldp**         | LDP协议相关信息                                                                                                                                                                                                 |
| **manager**     | 用户管理器日志信息。                                                                                                                                                                                            |
| **mme**         | MME路由协议信息                                                                                                                                                                                                 |
| **mpls**        | MPLS消息                                                                                                                                                                                                        |
| **ntp**         | sNTP客户端生成的日志                                                                                                                                                                                            |
| **ospf**        | OSPF路由协议消息                                                                                                                                                                                                |
| **ovpn**        | OpenVPN隧道消息                                                                                                                                                                                                 |
| **pim**         | 多播PIM-SM相关信息                                                                                                                                                                                              |
| **ppp**         | ppp设施信息                                                                                                                                                                                                     |
| **pppoe**       | PPPoE服务器/客户端相关信息                                                                                                                                                                                      |
| **pptp**        | PPTP服务器/客户端相关信息                                                                                                                                                                                       |
| **radius**      | 由RADIUS客户端生成的日志                                                                                                                                                                                        |
| **radvd**       | IPv6 radv deamon日志信息。                                                                                                                                                                                      |
| **read**        | SMS工具信息                                                                                                                                                                                                     |
| **rip**         | RIP路由协议消息                                                                                                                                                                                                 |
| **route**       | 路由设施日志                                                                                                                                                                                                    |
| **rsvp**        | 资源保留协议生成的消息。                                                                                                                                                                                        |
| **script**      | 脚本生成的日志条目                                                                                                                                                                                              | **sertcp** | 脚本生成的日志 |
| **sertcp**      | 负责"/ports remote-access "的设施相关的日志消息                                                                                                                                                                 |
| **simulator**   |                                                                                                                                                                                                                 |
| **state**       | DHCP客户端和路由状态信息。                                                                                                                                                                                      |
| **store**       | 由Store设施产生的日志。                                                                                                                                                                                         |
| **smb**         | 与SMB文件共享系统有关的消息                                                                                                                                                                                     |
| **snmp**        | 与简单网络管理协议（SNMP）配置有关的消息                                                                                                                                                                        |
| **system**      | 通用的系统信息                                                                                                                                                                                                  |
| **telephony**   | _Obsolete! 以前由IP电话包使用。                                                                                                                                                                                 |
| **tftp**        | TFTP服务器生成的信息                                                                                                                                                                                            |
| **timer**       | 与RouterOS中使用的定时器有关的日志信息。例如bgp keepalive日志:<br>`   12:41:40 route,bgp,debug,timer KeepaliveTimer expired` <br>`12:41:40 route,bgp,debug,timer`   <br>  `RemoteAddress=2001:470:1f09:131::1 ` |
| **ups**         | 由UPS监控工具生成的消息                                                                                                                                                                                         |
| **vrrp**        | 由VRRP产生的信息                                                                                                                                                                                                |
| **watchdog**    | 看门狗产生的日志                                                                                                                                                                                                |
| **web-proxy**   | web代理生成的日志信息                                                                                                                                                                                           |
| **wireless**    | 无线日志。                                                                                                                                                                                                      |
| **write**       | SMS工具信息。                                                                                                                                                                                                   |

## 例子

### 记录日志到文件

想把所有的东西都记录到文件中，请添加新的日志动作。

`/system logging action add name=file target=disk disk-file-name=log`。

然后用这个新的动作来记录一切。

`/system logging add action=file`。

可以通过发布命令只记录错误。

`/system logging add topics=error action=file`。

将记录到 **log.0.txt** 和 **log.1.txt** 文件中。

可以通过指定 _disk-lines-per-file_ 来指定文件的最大行数。**\<file\>.0.txt** 是活动文件，将添加新的日志，一旦大小达到最大值，就成为 **\<file\>.1.txt**，新的空 **\<file\>.0.txt** 将被创建。

可以通过在文件名前指定它的目录名来登录U盘或 _MicroSD/CF_ （在Routerboards）。例如，如果你在 _/files_ 下的 **usb1** 目录下访问u盘，应该发出以下命令。

`/system logging action add name=usb target=disk disk-file-name=usb1/log`。

重新启动后，文件中的日志将被储存在内存中。
