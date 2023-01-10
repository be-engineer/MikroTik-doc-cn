## 概述

本文描述了一组用于配置管理的命令。

## 配置 撤消/重做

在 GUI 中完成的任何操作或从 CLI 执行的任何命令都记录在“/system history”中。 可以通过从 CLI 运行撤消或重做命令或通过单击 GUI 中的撤消和重做按钮来撤消或重做任何操作。

用一个简单的例子来演示添加防火墙规则以及如何撤消和重做操作：

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="text plain">[admin@v7_ccr_bgp] /ip/firewall/filter&gt; add chain=forward action=drop</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="text plain">[admin@v7_ccr_bgp] /ip/firewall/filter&gt; print</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="text plain">Flags: X - disabled, I - invalid; D - dynamic</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="text plain">0 X chain=input action=drop protocol=icmp src-address=10.155.101.1 log=no</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="text plain">log-prefix=""</code></div><div class="line number6 index5 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="text plain">1 chain=forward action=drop</code></div><div class="line number8 index7 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="text plain">[admin@v7_ccr_bgp] /ip/firewall/filter&gt; /system/history/print</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="text plain">Flags: U - undoable, R - redoable, F - floating-undo</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="text plain">Columns: ACTION, BY, POLICy</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="text plain">ACTION BY POLIC</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="text plain">F filter rule added admin write</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="text plain">U --- write</code></div><div class="line number15 index14 alt2" data-bidi-marker="true"><code class="text plain">[admin@v7_ccr_bgp] /ip/firewall/filter&gt;</code></div></div></td></tr></tbody></table>

  

我们添加了防火墙规则，在“/system history”中我们可以看到所做的一切。

让我们撤消一切：

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="text plain">[admin@v7_ccr_bgp] /ip/firewall/filter&gt; /undo</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="text plain">[admin@v7_ccr_bgp] /ip/firewall/filter&gt; print</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="text plain">Flags: X - disabled, I - invalid; D - dynamic</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="text plain">0 X chain=input action=drop protocol=icmp src-address=10.155.101.1 log=no</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="text plain">log-prefix=""</code></div><div class="line number6 index5 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="text plain">[admin@v7_ccr_bgp] /ip/firewall/filter&gt;</code></div></div></td></tr></tbody></table>

如您所见，防火墙规则消失了。
现在重做最后的改变：

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="text plain">[admin@v7_ccr_bgp] /ip/firewall/filter&gt; /redo</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="text plain">[admin@v7_ccr_bgp] /ip/firewall/filter&gt; print</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="text plain">Flags: X - disabled, I - invalid; D - dynamic</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="text plain">0 X chain=input action=drop protocol=icmp src-address=10.155.101.1 log=no</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="text plain">log-prefix=""</code></div><div class="line number6 index5 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="text plain">1 chain=forward action=drop</code></div><div class="line number8 index7 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="text plain">[admin@v7_ccr_bgp] /ip/firewall/filter&gt;</code></div></div></td></tr></tbody></table>

  
系统历史能够显示在撤消或重做操作期间将执行的确切 CLI 命令，即使我们从 GUI 执行操作。例如，从 WinBox 添加 TCP 接受规则后的详细历史输出：

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="text plain">[admin@v7_ccr_bgp] /system/history&gt; print detail</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="text plain">Flags: U - undoable, R - redoable, F - floating-undo</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;</code><code class="text plain">F redo=</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">/ip firewall filter add action=accept chain=forward disabled=no log=no \</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">log-prefix="" protocol=tcp</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">undo=/ip firewall filter remove *4 action="filter rule added" by="admin"</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">policy=write time=oct/10/2019 18:51:05</code></div><div class="line number8 index7 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;</code><code class="text plain">F redo=/ip firewall filter add action=accept chain=forward</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">undo=/ip firewall filter remove *3 action="filter rule added" by="admin"</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">policy=write time=oct/10/2019 18:49:03</code></div><div class="line number12 index11 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number13 index12 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="text plain">U redo="" undo="" action="---" by="" policy=write time=sep/27/2019 13:07:35</code></div><div class="line number15 index14 alt2" data-bidi-marker="true"><code class="text plain">[admin@v7_ccr_bgp] /system/history&gt;</code></div></div></td></tr></tbody></table>

## 安全模式

有时，路由器配置的更改会导致路由器无法访问（本地控制台除外）。 通常，这是意外，但是当与路由器的连接已经断开时，没有办法撤消最后的更改。 安全模式可用于将此类风险降至最低。

按 **Ctrl-X** 进入安全模式。 要保存更改并退出安全模式，请再次按 **Ctrl-X**。 要退出而不保存所做的更改，请按 **Ctrl-D**

```
[admin@MikroTik] ip route>[CTRL]+[X]
[Safe Mode taken]

[admin@MikroTik] ip route<SAFE>

```

![](https://help.mikrotik.com/docs/download/attachments/328155/winbox-safe-mode.png?version=2&modificationDate=1570721399597&api=v2)

显示消息 **Safe Mode taken** 并提示更改以反映该会话现在处于安全模式。 在 WinBox 中，通过切换工具栏左侧的 **Safe Mode** 切换按钮启用安全模式。

当路由器处于安全模式时，如果安全模式会话异常终止，所做的所有配置更改（也来自其他登录会话）将自动撤消。 您可以在系统历史记录中看到所有这些将自动撤消并标有 **F** 标志的更改：

```
[admin@MikroTik] ip route>
[Safe Mode taken]

[admin@MikroTik] ip route<SAFE> add
[admin@MikroTik] ip route<SAFE> /system history print
Flags: U - undoable, R - redoable, F - floating-undo
  ACTION                                   BY                 POLICY
F route added                              admin              write    

```

现在，如果 telnet 连接、WinBox 终端（如果在 WinBox 终端窗口上启用了安全模式）或 WinBox 连接被切断，则在一段时间后（TCP 超时为 **9** 分钟）所有安全模式下的更改将被撤销。 通过 **Ctrl-D** 退出会话也会撤消所有安全模式更改，而 **/quit** 则不会。

如果另一个用户试图进入安全模式，他会收到以下消息：

```
[admin@MikroTik] >
Hijacking Safe Mode from someone - unroll/release/don't take it [u/r/d]:

```

- [u] - 撤消所有安全模式更改，并将当前会话置于安全模式。
- [r] - 保留所有当前安全模式更改，并将当前会话置于安全模式。 安全模式的前所有者会收到有关此的通知：

```
 
     [admin@MikroTik] ip firewall rule input
     [Safe mode released by another user]

```

- [d] - 让一切保持原样。

如果在安全模式下进行了太多更改，并且历史记录中没有空间容纳所有这些更改（当前历史记录最多可保留 100 个最近的操作），则会话会自动退出安全模式，并且不会自动进行任何更改撤消。 因此，最好在安全模式下逐步更改配置。 按 **Ctrl**\-**X** 两次是清空安全模式操作列表的简单方法。

## 系统备份/恢复

系统备份是以二进制格式完全克隆路由器配置的方法。 备份文件不仅包含配置，还包含统计数据、日志等。备份文件最好用在同一台设备上保存和恢复配置，如果要将配置移动到其他设备，请改用导出文件。

备份文件包含敏感信息（密码、密钥、证书）。 该文件可以加密，但即便如此，备份也应仅存储在安全位置。

恢复备份文件应仅在同一路由器或当先前路由器发生故障时在类似路由器上进行。 不得使用备份来克隆多个网络路由器上的配置。

保存和加载备份文件的示例：

```
[admin@MikroTik] > system backup save name=test password=123Configuration backup saved[admin@MikroTik] > file print# NAME TYPE SIZE CREATION-TIME0 test.backup backup 12567 sep/08/2004 21:07:50[admin@MikroTik] >[admin@MikroTik] > system backup load name=test password=123Restore and reboot? [y/N]:yRestoring system configurationSystem configuration restored, rebooting now
```

## 导入/导出

RouterOS 允许以纯文本格式导出和导入部分配置。 此方法可用于在不同设备之间复制配置，例如，将整个防火墙从一台路由器克隆到另一台路由器。

可以从每个单独的菜单执行导出命令（结果仅从此特定菜单及其所有子菜单导出配置）或从根菜单执行完整的配置导出。

接受以下命令参数：

| 属性               | 说明                                                          |
| ------------------ | ------------------------------------------------------------- |
| **compact**        | 仅输出修改后的配置，默认行为                                  |
| **file**           | 将配置导出到指定文件。 当未指定文件时，导出信息将打印到终端   |
| **hide-sensitive** | 隐藏敏感信息，如密码、密钥等。                                |
| **verbose**        | 使用此参数，export 命令将输出整个配置参数和项目，包括默认值。 |

例如，从 `/ip address` 菜单导出配置并将其保存到文件中：

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="text plain">[admin@MikroTik] &gt; /ip address print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="text plain">Flags: X - disabled, I - invalid, D - dynamic</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="text plain">#&nbsp;&nbsp; ADDRESS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; NETWORK&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; BROADCAST&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; INTERFACE</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="text plain">0&nbsp;&nbsp; 10.1.0.172/24&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 10.1.0.0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 10.1.0.255&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; bridge1</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="text plain">1&nbsp;&nbsp; 10.5.1.1/24&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 10.5.1.0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 10.5.1.255&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ether1</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="text plain">[admin@MikroTik] &gt; /ip address export file=address</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="text plain">[admin@MikroTik] &gt; /file print</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="text plain"># NAME&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; TYPE&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; SIZE&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; CREATION-TIME</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="text plain">0&nbsp; address.rsc&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; script&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 315&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; dec/23/2003 13:21:48</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="text plain">[admin@MikroTik] &gt;</code></div></div></td></tr></tbody></table>

默认情况下，export 命令只写入用户编辑的配置，RouterOS 默认值被省略。

例如，不会导出 IPSec 默认策略，如果我们更改一个属性，则只会导出更改：


<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="text plain">[admin@rack1_b4] /ip ipsec policy&gt; print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="text plain">Flags: T - template, X - disabled, D - dynamic, I - inactive, * - default</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="text plain">0 T * group=default src-address=::/0 dst-address=::/0 protocol=all</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">proposal=default template=yes</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="text plain">[admin@rack1_b4] /ip ipsec policy&gt; export</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="text plain"># apr/02/1970 17:59:14 by RouterOS 6.22</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="text plain"># software id = DB0D-LK67</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="text plain">#</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="text plain">[admin@rack1_b4] /ip ipsec policy&gt; set 0 protocol=gre</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="text plain">[admin@rack1_b4] /ip ipsec policy&gt; export</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="text plain"># apr/02/1970 17:59:30 by RouterOS 6.22</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="text plain"># software id = DB0D-LK67</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="text plain">#</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="text plain">/ip ipsec policy</code></div><div class="line number15 index14 alt2" data-bidi-marker="true"><code class="text plain">set 0 protocol=gre</code></div></div></td></tr></tbody></table>

注意 **\*** 标志，它表示该条目是系统默认的，无法手动删除。

这是包含默认系统条目的所有菜单的列表
| 菜单                                      | 默认入口                                                                                                                                                            |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **/interface wireless security-profiles** | default                                                                                                                                                             |
| **/ppp profile**                          | "default", "default-encryption"                                                                                                                                     |
| **/ip hotspot profile**                   | default                                                                                                                                                             |
| **/ip hotspot user profile**              | default                                                                                                                                                             |
| **/ip ipsec policy**                      | default                                                                                                                                                             |
| **/ip ipsec policy group**                | default                                                                                                                                                             |
| **/ip ipsec proposal**                    | default                                                                                                                                                             |
| **/ip ipsec mode-conf**                   | read-only                                                                                                                                                           |
| **/ip smb shares**                        | pub                                                                                                                                                                 |
| **/ip smb users**                         | guest                                                                                                                                                               |
| **/ipv6 nd**                              | any                                                                                                                                                                 |
| **/mpls interface**                       | all                                                                                                                                                                 |
| **/routing bfd interface**                | all                                                                                                                                                                 |
| **/routing bgp instance**                 | default                                                                                                                                                             |
| **/routing ospf instance**                | default                                                                                                                                                             |
| **/routing ospf area**                    | backbone                                                                                                                                                            |
| **/routing ospf-v3 instance**             | defailt                                                                                                                                                             |
| **/routing ospf-v3 area**                 | backbone                                                                                                                                                            |
| **/snmp community**                       | public                                                                                                                                                              |
| **/tool mac-server mac-winbox**           | all                                                                                                                                                                 |
| **/tool mac-server**                      | all                                                                                                                                                                 |
| **/system logging**                       | "info", "error", "warning", "critical"                                                                                                                              |
| **/system logging action**                | "memory", "disk", "echo", "remote"                                                                                                                                  |
| **/queue type**                           | "default", "ethernet-default", "wireless-default", "synchronous-default", "hotspot-default", "only-hardware-queue", "multi-queue-ethernet-default", "default-small" |

  
### 配置导入

根菜单命令导入允许从指定文件运行配置脚本。 脚本文件（扩展名为“.rsc”）可以包含任何控制台命令，包括复杂的脚本。

例如加载保存的配置文件

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="text plain">[admin@MikroTik] &gt; import address.rsc</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="text plain">Opening script file address.rsc</code></div><div class="line number3 index2 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="text plain">Script file loaded and executed successfully</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="text plain">[admin@MikroTik] &gt;</code></div></div></td></tr></tbody></table>

  

导入命令允许指定以下参数：

| 属性          | 说明                                                           |
| ------------- | -------------------------------------------------------------- |
| **from-line** | 从指定行号开始执行脚本                                         |
| **file-name** | 要执行的脚本 (.rsc) 文件的名称。                               |
| **verbose**   | 从文件中读取每一行并单独执行，允许更轻松地调试语法或其他错误。 |

### 自动导入

也可以使用 FTP 或 SFTP 上传到路由器后**自动**执行脚本。 脚本文件必须以扩展名 \*.auto.rsc 命名。 执行文件中的命令后，将创建一个新的 \*.auto.log 文件，其中包含导入成功或失败的信息。

文件名中的“.auto.rsc”是自动执行文件所必需的。
## 配置重置

RouterOS 允许使用“/system reset-configuration”命令重置配置

此命令清除路由器的所有配置并将其设置为出厂默认设置，包括登录名和密码（“admin”密码为空，对于某些型号，检查标签上的用户和无线密码）。 有关默认配置的更多详细信息[请参阅表](https://help.mikrotik.com/docs/display/ROS/Default+configurations)。

执行配置重置命令后，路由器将重新启动并加载默认配置。

  

现有配置的备份文件在重置前存储。 这样，如果错误地进行了重置，您可以轻松地恢复任何以前的配置。

如果路由器已使用 [Netinstall](https://help.mikrotik.com/docs/display/ROS/Netinstall) 安装并指定了脚本作为初始配置，则重置命令会在清除配置后执行此脚本。 要阻止它这样做，您将必须重新安装路由器。

可以使用以下参数覆盖默认重置行为：

| 属性                | 说明                                                      |
| ------------------- | --------------------------------------------------------- |
| **keep-users**      | 不要从配置中删除现有用户                                  |
| **no-defaults**     | 不加载默认配置，清除配置即可                              |
| **skip-backup**     | 跳过重置前自动备份文件生成                                |
| **run-after-reset** | 重置后运行指定的 .rsc 文件。 这样您就可以加载自定义配置。 |
  
例如，不加载默认配置和跳过备份文件的硬重置配置：

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="text plain">[admin@MikroTik] &gt; /system reset-configuration no-defaults=yes skip-backup=yes</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="text plain">Dangerous! Reset anyway? [y/N]: y</code></div></div></td></tr></tbody></table>

同样，使用 Winbox：

![](https://help.mikrotik.com/docs/download/attachments/328155/reset_config.png?version=1&modificationDate=1569852334652&api=v2&effects=drop-shadow)