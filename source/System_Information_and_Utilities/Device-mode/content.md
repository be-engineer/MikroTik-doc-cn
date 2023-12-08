# 设备模式

设备模式是一个在设备上设置特定限制或限制访问特定配置选项的功能。
有两种模式:enterprise和home。默认情况下，所有设备都使用enterprise模式，该模式允许除container之外的所有功能。主模式禁用以下功能:scheduler, socks, fetch, bandwidth-test, traffic-gen, sniffer, romon, proxy, hotspot, email, zerotier, container.

`[admin@MikroTik] > system/device-mode/print
mode: enterprise`

用户可以更改设备模式，但远程访问设备不足以更改设备模式。在更改设备模式后，您需要通过按设备上的按钮来确认它，或者执行“冷重启”-即拔掉电源。

```shell
[admin@MikroTik] > system/device-mode/update mode=home
  update: please activate by turning power off or pressing reset or mode button
          in 5m00s
-- [Q quit|D dump|C-z pause]
```

如果在设定的时间内没有下电或按下按钮，则取消模式切换。如果同时运行另一个更新命令，这两个命令都将被取消。

**system/device-mode/** 菜单中有以下命令:

| 属性   | 说明                                         |
| ------ | -------------------------------------------- |
| get    | 返回值，您可以将其赋值给变量或打印在屏幕上。 |
| print  | 显示活动模式及其属性。                       |
| update | 将更改应用于指定的属性，见下文。             |

## 可用属性列表

| 属性                                                                                                                                                                                              | 说明                                                                                                                                                                                                                                                                                                                                                     |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **container, fetch, scheduler, traffic-gen,ipsec, pptp, smb, l2tp, proxy, sniffer, zerotier, bandwidth-test, email, hotspot, romon, socks.** (_yes \| no_; Default: **yes**, for enterprise mode) | 可用特性列表，可以通过 **device-mode** 选项进行控制。                                                                                                                                                                                                                                                                                                    |
| **activation-timeout** (default: **5m**);                                                                                                                                                         | 复位按钮或关机激活超时时间可在00:00:10范围内设置。1d00:00:00。如果在此时间间隔内未按下重置按钮(或未执行冷重启)，则更新将被取消。                                                                                                                                                                                                                         |
| **flagging-enabled** (_yes\| no_; Default: **yes**)                                                                                                                                               | 启用或禁用 _flagged_ 状态。请看下面的详细说明                                                                                                                                                                                                                                                                                                            |
| **flagged** (_yes \| no_;Default:**no**)                                                                                                                                                          | RouterOS使用各种机制来检测对系统文件的篡改。如果系统检测到对RouterOS的未授权访问，则将状态“已标记”设置为yes。如果“标记”设置为“是”，为了您的安全，将设置某些限制。更多信息见下一章。                                                                                                                                                                      |
| **mode:**(home, enterprise;  default: **enterprise**);                                                                                                                                            | 允许从限制设备功能的可用模式中进行选择。在未来，可以添加各种模式。<br>默认情况下，**enterprise** 模式允许除容器之外的所有选项。因此，要使用容器特性，需要通过执行设备模式更新来打开它。<br>默认情况下，**home** 模式禁用以下功能: **scheduler, socks, fetch, bandwidth-test, traffic-gen, sniffer, romon, proxy, hotspot, email, zerotier, container。** |

可以对可用特性进行更具体的控制。由设备模式控制的每个功能都可以被特定地打开或关闭，例如:

```shell
[admin@MikroTik] > system/device-mode/update mode=home email=yes
[admin@MikroTik] > system/device-mode/update mode=enterprise zerotier=no
```

如果update命令指定了任何模式参数，则此更新将替换整个设备模式配置。在这种情况下，除了用该命令指定的设置外，所有“每个特性”的设置都将丢失。例如:

```shell
[admin@MikroTik] > system/device-mode/update mode=home email=yes fetch=yes
[admin@MikroTik] > system/device-mode/print
   mode: home
  fetch: yes
  email: yes
[admin@MikroTik] > system/device-mode/update mode=enterprise sniffer=no
-- reboot --
[admin@MikroTik] > system/device-mode/print
     mode: enterprise
  sniffer: no
```

这里fetch = yes和email = yes丢失了，因为它们被模式更改覆盖了。指定“per-feature”设置只会改变以下内容:

```shell
[admin@MikroTik] > system/device-mode/update hotspot=no
-- reboot --
[admin@MikroTik] > system/device-mode/print
     mode: enterprise
  sniffer: no
  hotspot: no
```

如果该功能被禁用，交互式命令将显示错误消息:

```shell
[admin@MikroTik] > system/device-mode/print
     mode: enterprise
  sniffer: no
  hotspot: no
[admin@MikroTik] > tool/sniffer/quick
failure: not allowed by device-mode
```

可以将配置添加到已禁用的功能中，但是在设备模式中会有一条注释显示已禁用的功能:

```shell
[admin@MikroTik] > ip hotspot/add interface=ether1
[admin@MikroTik] > ip hotspot/print
Flags: X, S - HTTPS
Columns: NAME, INTERFACE, PROFILE, IDLE-TIMEOUT
#   NAME      INTERFACE  PROFILE  IDLE-TIMEOUT
;;; inactivated, not allowed by device-mode
0 X hotspot1  ether1     default  5m
```

# 标记状态

与设备模式特性一起，RouterOS现在可以在系统启动时分析整个配置，以确定是否有任何未经授权访问路由器的迹象。如果检测到可疑配置，将禁用可疑配置，并将 **flagged** 参数设置为“yes”。该设备现在处于标记状态，并强制执行某些限制。 

```shell
[admin@MikroTik] > system/device-mode/print
     mode: enterprise
  flagged: yes
  sniffer: no
  hotspot: no
```

如果系统有此标记状态，则当前配置有效，但无法执行以下操作:

带宽测试，流量生成器，嗅探器，以及为以下程序启用或创建新配置项的配置操作(仍然可以禁用或删除它们): _system scheduler, SOCKS proxy, pptp, l2tp, ipsec, proxy, smb_ 。

当路由器处于标记状态时执行上述操作时，将收到一条错误消息:

```shell
[admin@MikroTik] > /tool sniffer/quick
failure: configuration flagged, check all router configuration for unauthorized changes and update device-mode
[admin@MikroTik] > /int l2tp-client/add connect-to=1.1.1.1 user=user
failure: configuration flagged, check all router configuration for unauthorized changes and update device-mode
```

要退出标记状态，必须执行命令“/system/device-mode/update marked =no”。系统将要求按下按钮，或者发出硬重启(物理切断电源或对虚拟机进行硬重启)。

**重要信息：** 虽然系统已经禁用了恶意规则，这会触发标记状态，但在退出标记状态之前，检查所有的配置是否有其他未知的东西是至关重要的。如果您的系统已被标记，请假设系统被破坏，并在重新启用系统之前对所有设置进行全面审计。审计完成后，请修改所有系统密码，并升级到最新版本的RouterOS。