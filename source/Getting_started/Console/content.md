# 概述

控制台用于使用文本终端访问 MikroTik 路由器的配置和管理功能，可以远程使用串行端口、telnet、SSH 或 Winbox 中的控制台，也可以直接使用监视器和键盘。 控制台还用于编写脚本。 本手册描述了控制台的一般操作原则。 请参阅脚本手册了解一些高级控制台命令以及如何编写脚本。

## 菜单分级

控制台允许使用文本命令配置路由器的设置。 由于有很多可用的命令，它们被分为分层菜单级别的组。 菜单级别的名称反映了相关部分中可访问的配置信息，例如。 **/ip hotspot**。

### 示例

例如，您可以执行 **/ip route print** 命令：

`[admin@MikroTik] > ip route` `print`

`Flags` `: X - disabled, A - active, D - dynamic,`

`C - connect, S - static, r - rip, b - bgp, o - ospf, m - mme,`

`B - blackhole, U - unreachable, P - prohibit`

`0 A S` `0.0.0.0/0` `r 10.0.3.1 1 bridge1`

`1 ADC` `1.0.1.0/24` `1.0.1.1 0 bridge1`

`2 ADC` `1.0.2.0/24` `1.0.2.1 0 ether3`

`3 ADC` `10.0.3.0/24` `10.0.3.144 0 bridge1`

`4 ADC` `10.10.10.0/24` `10.10.10.1 0 wlan1`

`[admin@MikroTik] >`

无需在每个命令前输入 /**ip route** 路径，只需输入一次路径即可进入层次结构的这个特定分支。 因此，上面的例子也可以这样执行：

`[admin@MikroTik] > ip route`

`[admin@MikroTik] ip route>` `print`

`Flags` `: X - disabled, A - active, D - dynamic,`

`C - connect, S - static, r - rip, b - bgp, o - ospf, m - mme,`

 `B - blackhole, U - unreachable, P - prohibit`

`DST-ADDRESS PREF-SRC G GATEWAY DIS INTE...`

`0 A S` `0.0.0.0/0` `r 10.0.3.1 1 bridge1`

`1 ADC` `1.0.1.0/24` `1.0.1.1 0 bridge1`

`2 ADC` `1.0.2.0/24` `1.0.2.1 0 ether3`

`3 ADC` `10.0.3.0/24` `10.0.3.144 0 bridge1`

`4 ADC` `10.10.10.0/24` `10.10.10.1 0 wlan1 [`

`admin@MikroTik] ip route>`

请注意，提示会发生变化，以反映您此时在菜单层次结构中所处的位置。 要移动到顶层，请输入“**/**”

`[admin@MikroTik] > ip route`

`[admin@MikroTik] ip route>` `/`

`[admin@MikroTik] >`

要向上移动一级，请键入“**..**”

`[admin@MikroTik] ip route> ..`

`[admin@MikroTik] ip>`

您还可以使用 **/** 和 **..** 从其他菜单级别执行命令而不更改当前级别：

`[admin@MikroTik] ip route>` `/` `ping` `10.0.0.1`

`10.0.0.1` `ping` `timeout`

`2 packets transmitted, 0 packets received, 100% packet loss`

`[admin@MikroTik] ip firewall nat> .. service-port print`

`Flags` `: X - disabled, I - invalid`

`0 ftp 21`

`1 tftp 69`

`2 irc 6667`

`3 h323`

`4 sip`

`5 pptp`

`[admin@MikroTik] ip firewall nat>`

## 项目名称和编号

许多命令级别使用项目数组进行操作：接口、路由、用户等。此类数组显示在类似的列表中。 列表中的所有项目都有一个项目编号，后接标志和参数值。

要更改项目的属性，您必须使用 **set** 命令并指定项目的名称或编号。

### 项目名称

一些列表中的项目具有分配给每个项目的特定名称。 例如**interface**或**user**级别。 那里可以使用项目名称而不是项目编号。

在按名称访问项目之前，不必使用 **print** 命令，与数字相反，名称不是由控制台内部分配的，而是项目的属性。 因此，他们不会自行改变。 然而，当多个用户同时更改路由器的配置时，可能会出现各种难以理解的情况。 通常，项目名称比数字更“稳定”，也更能提供信息，因此在编写控制台脚本时您应该更喜欢它们而不是数字。

### 项目编号

项目编号由打印命令分配并且不是固定的 - 两个连续的打印命令可能会对项目进行不同的排序。 但是最后打印命令的结果会被记住，因此，一旦分配，即使在**添加**、**删除**和**移动**操作之后（自版本 3 起，**移动** 操作不会对项目重新编号）。 项目编号是在每个会话的基础上分配的，它们将保持不变，直到退出控制台或执行下一个打印命令。 此外，会为每个项目列表单独分配编号，因此 **ip address print** 不会更改接口列表的编号。

从版本 3 开始，无需运行 **print** 命令即可使用项目编号。 就像执行了 **print** 命令一样分配数字。

您可以将多个项目指定为某些命令的目标。 几乎在任何地方你都可以写项目的数量，也可以写一个数字列表。

`[admin@MikroTik] > interface` `print`

`Flags` `: X - disabled, D - dynamic, R - running`

`0 R ether1 ether 1500`

`1 R ether2 ether 1500`

`2 R ether3 ether 1500`

`3 R ether4 ether 1500`

`[admin@MikroTik] > interface` `set` `0,1,2` `mtu` `=1460`

`[admin@MikroTik] > interface print`

 `Flags` `: X - disabled, D - dynamic, R - running`

`0 R ether1 ether 1460`

`1 R ether2 ether 1460`

`2 R ether3 ether 1460`

`3 R ether4 ether 1500`

`[admin@MikroTik] >`

**警告：**不要在脚本中使用项目编号，这不是**scheduler. scripts**中编辑项目的可靠方法。最好使用查找命令。 更多信息见[此处](https://wiki.mikrotik.com/wiki/Manual:Scripting "Manual:Scripting")。另请参阅[脚本示例](https://wiki.mikrotik.com/wiki/Manual:Scripting-examples)。

## 快速输入

控制台中有两个功能可以帮助更快更轻松地输入命令 - [Tab] 键完成命令的缩写。 工作方式类似于 UNIX 中的 bash shell。 如果在单词的一部分后按 [Tab] 键，控制台会尝试在当前上下文中查找以该单词开头的命令。 如果只有一个匹配项，则会自动添加，后跟一个空格：

_/inte_**[Tab]_** 变成 **/interface _**

如果有多个匹配，但它们都有一个相同的开头，比你输入的长，那么这个词就完成到这个共同的部分，并且不附加空格：

_/interface set e_**[Tab\]_** 变成 **/interface set ether_**

如果您只输入了公共部分，则按一次 Tab 键无效。 但是第二次按下它会以紧凑的形式显示所有可能的补全：

`[admin@MikroTik] > interface` `set` `e[Tab]_`

`[admin@MikroTik] > interface` `set` `ether[Tab]_`

`[admin@MikroTik] > interface` `set` `ether[Tab]_`

`ether1 ether5`

`[admin@MikroTik] > interface` `set` `ether_`

**[Tab]** 键几乎可以在控制台可能有线索的任何上下文中使用 - 命令名称、参数名称、只有几个可能值的参数（例如某些列表中的项目名称或 防火墙和 NAT 规则中的协议名称）。 您不能填写数字、IP 地址和类似值。

另一种在键入时减少按键的方法是缩写的命令和参数名称。 您只要键入命令名称的开头，如果它没有歧义，控制台将接受它作为全名。 所以输入：

`[admin@MikroTik] > pi 10.1 c 3 si 100`

等于:

`[admin@MikroTik] >` `ping` `10.0.0.1 count 3 size 100`

不仅可以补全名称的开头，还可以补全名称的任何子字符串：如果没有完全匹配，控制台将开始查找将字符串并补全为多个单词名称的第一个字母的单词，或者仅包含 此字符串的字母。 如果找到单个这样的词，则在光标位置完成。 例如：

`[admin@MikroTik] > interface x[TAB]_`

`[admin@MikroTik] > interface` `export` `_`

`[admin@MikroTik] > interface mt[TAB]_`

`[admin@MikroTik] > interface monitor-traffic _`

## 常规命令

几乎所有菜单级别都有一些通用命令，即：**print, set, remove, add, find, get, export, enable, disable, comment, move**。 这些命令在不同的菜单级别上具有相似的行为。

- **add** - 通常具有与**set** 相同的所有参数，除了项目编号参数。 它添加一个具有指定值的新项目，通常在项目列表的末尾，在项目相关的地方。 必须提供一些必需的属性，例如新地址的接口，而其他属性将设置为默认值，除非明确指定它们。
  - 通用参数
         - _copy-from_ \- 复制现有项目。 它从另一个项目中获取新项目属性的默认值。 如果不想进行精确复制，可以为某些属性指定新值。 复制有名称的项目时，通常必须为副本指定一个新名称
         - _place-before_ \- 将新项目放在具有指定位置的现有项目之前。 不需要在将项目添加到列表后使用移动命令。
         - _disabled_ \- 控制新添加项目的禁用/启用状态（-s）
         - _comment_ \- 保存新创建项目的注释
  - 返回值
         - 添加命令返回它添加的项目的内部编号

- **edit** \- 此命令与 **set** 命令相关联。 它可用于编辑包含大量文本的属性值，例如脚本，但它适用于所有可编辑的属性。 根据终端的功能，启动全屏编辑器或单行编辑器来编辑指定属性的值。
- **find** \- find 命令具有与 set 相同的参数，加上标志参数，如 _disabled_ 或 _active_ 取值 _yes_ 或 _no_ 取决于各自标志的值。 要查看所有标志及其名称，请查看 **print** 命令输出的顶部。 **find** 命令返回具有与指定参数值相同的所有项目的内部编号。
- **move** \- 更改列表中项目的顺序。
  - 参数
    - 第一个参数指定要移动的项目。
    - 第二个参数指定要放置所有被移动项目的条目（如果省略第二个参数，它们将被放置在列表的末尾）。
- **print** \- 显示可从特定命令级别访问的所有信息。 因此，**/system clock print** 显示系统日期和时间，**/ip route print** 显示所有路由等。如果当前级别有项目列表并且不是只读的，即你可以更改/删除它们（只读项目列表的示例是 /system history，它显示已执行操作的历史记录），则print 命令还会分配所有操作此列表中项目的命令所使用的编号。
  - 通用参数
    - _from_ \- 只显示指定的项目，按照给定的顺序。
    - _where_ \- 仅显示符合指定条件的项目。 _where_ 属性的语法类似于 **find** 命令。
    - _brief_ \- 强制打印命令使用表格输出形式
    - _detail_ \- 强制打印命令使用 property=value 输出形式
    - _count-only_ \- 显示项目数
    - _file_ \- 将特定子菜单的内容打印到路由器上的文件中。
    - _interval_ \- 每隔 interval 秒更新 _print_ 命令的输出。
    - _oid_ \- 打印可从 SNMP 访问的属性的 OID 值
    - _without-paging_ \- 在每屏之后不停止地打印输出。
- **remove** \- 从列表中删除指定的项目。
- **set** \- 允许您更改一般参数或项目参数的值。 set 命令的参数名称与您可以更改的值相对应。 利用?或双击 [Tab] 查看所有参数的列表。 如果此命令级别中有一个项目列表，则 set 有一个操作参数，该参数接受您要设置的项目（或数字列表）的数量。 此命令不返回任何内容。
- **reset** - 将参数重置为默认值

!!! note 您可以组合命令，这里是同一命令的两个变体，它们将通过查找注释来设置新的防火墙过滤器条目：<br> /ip firewall/filter/add chain=forward place-before=[find where comment=CommentX\]  <br> /ip/firewall/filter/add chain=forward place-before="CommentX"

## 模式

控制台编辑器在多行模式或单行模式下工作。 在多行模式编辑器中显示完整的输入行，即使它比单个行长。 使用全屏编辑器来编辑大文本，例如脚本。 在单行模式下，只有一个终端行用于行编辑，长行在光标周围被截断。 在此模式下不使用全屏编辑器。

模式的选择取决于检测到的终端能力。

## 键列表

Control-C 中断; Control-D 注销（如果输入行为空）; Control-K 从光标清除到行尾; Control-X 切换安全模式; Control-V 切换热锁模式; F6切换窗口; F1 或?显示上下文相关的帮助。 如果前一个字符是\，则插入?;Tab 执行自动补全。 第二次按下时，显示可能的补全。Delete 删除光标处的字符 Control-H 或 Backspace 删除光标前的字符并将光标移回一个位置。Control-\ 在光标处分行， 在光标位置插入换行符， 显示两个结果行中的第二行。Control-B 或左键向后一个字符; Control-F 或右键向前移动一个字符; Control-P 或上键转到上一行， 如果这是第一行输入，则从历史记录中调用之前的输入。 Control-N 或 下键转到下一行， 如果这是最后一行输入，则从历史读取下一条输入。Control-A 或 Home 将光标移动到该行的开头。 如果光标已经在行首，则转到当前输入的第一行的开头。Control-E 或 End 将光标移动到行尾。 如果光标已经在行尾，则将其移动到当前输入的最后一行的末尾。Control-L 或 F5 重置终端并重绘屏幕。

**向上**、**向下**和**分割**键将光标留在行尾。

### 内置帮助

控制台有一个内置的帮助，可以通过键入 **?** 来访问。 一般规则是，帮助显示您可以在按下 **?** 的位置输入的内容（类似于按两次 **[Tab]** 键，但解释更详细）。

### 安全模式

有时可能会以某种方式更改路由器配置，使路由器无法访问（本地控制台除外）。 通常这是意外造成的，但是当与路由器的连接已经断开时，无法撤消上次更改。 安全模式可用于将此类风险降至最低。

按 **[CTRL]+[X]** 进入安全模式。 要保存更改并退出安全模式，请再次按 **[CTRL]+[X]**。 要退出而不保存所做的更改，请按 **[CTRL]+[D]**

`[admin@MikroTik] ip route>[CTRL]+[X]`

`[Safe Mode taken]`

`[admin@MikroTik] ip route<SAFE>`

[![](https://help.mikrotik.com/docs/download/attachments/8978498/703px-2009-04-06_1317%20%281%29.png?version=1&modificationDate=1602153910731&api=v2)](https://wiki.mikrotik.com/wiki/File:2009-04-06_1317.png)

显示消息**Safe Mode Taken**并提示更改以反映该会话现在处于安全模式。 当路由器处于安全模式时，如果安全模式会话异常终止，所做的所有配置更改（也来自其他登录会话）将自动撤消。 您可以在系统历史记录中看到所有这些将被自动撤消标记为 **F** 标志的更改：

`[admin@MikroTik] ip route>`

`[Safe Mode taken]`

`[admin@MikroTik] ip route<SAFE>` `add`

`[admin@MikroTik] ip route<SAFE>` `/system history` `print`

`Flags` `: U - undoable, R - redoable, F - floating-` `undo`

`ACTION BY POLICY`

`F route added admin write`

现在，如果 telnet 连接（或 winbox 终端）被切断，一段时间后（TCP 超时为 **9** 分钟）所有在安全模式下所做的更改都将被撤消。 通过 **[Ctrl]+[D]** 退出会话也会撤消所有安全模式更改，而 **/quit** 则不会。

如果另一个用户试图进入安全模式，他会收到以下消息：

`[admin@MikroTik] >`

`Hijacking Safe Mode from someone - unroll` `/release/don't take it [u/r/d]:`

- [u] - 撤消所有安全模式更改，并将当前会话置于安全模式。
- [r] - 保留所有当前安全模式更改，并将当前会话置于安全模式。 安全模式的前所有者会收到有关此的通知：

`[admin@MikroTik] ip firewall rule input`

`[Safe mode released by another user]`

- [d] - 让一切保持原样。

如果在安全模式下进行了太多更改，并且历史记录中没有空间容纳所有这些更改（当前历史记录最多保留 100 个最近的操作），则会话会自动退出安全模式，不会自动撤消任何更改。 因此，最好在安全模式下小步更改配置。 按 [Ctrl]+[X] 两次是清空安全模式操作列表的简单方法。

### HotLokc模式

当启用 HotLock 模式时，命令将自动完成。

要进入/退出HotLock模式，请按 **[CTRL]+[V]**。

`[admin@MikroTik]` `/ip address> [CTRL]+[V]`

`[admin@MikroTik]` `/ip address>>`

Double`>>` 表示已启用 HotLock 模式。 例如，如果输入`/in e`，它将自动完成为

`[admin@MikroTik]` `/ip address>> /interface ethernet`

F6 键在终端底部启用一个菜单，其中显示了常用的组合键及其用法。

`[admin@RB493G] >`

 `tab compl ? F1 help ^V hotlk ^X safe ^C brk ^D` `quit`