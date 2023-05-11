The console is used for accessing the MikroTik Router's configuration and management features using text terminals, either remotely using a serial port, telnet, SSH, 控制台屏幕在 [WinBox](https://help.mikrotik.com/docs/display/ROS/Winbox) 内，或直接使用显示器和键盘。控制台也可用于编写脚本。本手册描述了一般的控制台操作原则。关于一些高级控制台命令和如何编写脚本，请查阅《脚本手册》。

# 登录选项

控制台登录选项可以启用或禁用各种控制台功能，如颜色、终端检测和许多其他功能。

额外的登录参数可以附加在登录名的 "+"号之后。

```
    login_name ::= user_name [ '+' parameters ]
    parameters ::= parameter [ parameters ]
    parameter ::= [ number ] 'a'..'z'
    number ::= '0'..'9' [ number ]
  
```

如果该参数不存在，则使用默认值。如果数字不存在，则使用该参数的隐含值。

例如：admin+c80w - 将禁用控制台颜色，并将终端宽度设置为80。

| 参数  | 默认 | 隐式 | 说明                 |
| ----- | ---- | ---- | -------------------- |
| **w** | auto | auto | 设置终端宽度         |
| **h** | auto | auto | 设置终端高度         |
| **c** | on   | off  | 禁用启用控制台颜色   |
| **t** | on   | off  | 做终端功能的自动检测 |
| **e** | on   | off  | 启用 "哑巴 "终端模式 |

# 风格和信息

在验证了用户名和密码之后，登录过程将显示MikroTik的横幅和简短的帮助。

```shell
  MMM      MMM       KKK                          TTTTTTTTTTT      KKK
  MMMM    MMMM       KKK                          TTTTTTTTTTT      KKK
  MMM MMMM MMM  III  KKK  KKK  RRRRRR     OOOOOO      TTT     III  KKK  KKK
  MMM  MM  MMM  III  KKKKK     RRR  RRR  OOO  OOO     TTT     III  KKKKK
  MMM      MMM  III  KKK KKK   RRRRRR    OOO  OOO     TTT     III  KKK KKK
  MMM      MMM  III  KKK  KKK  RRR  RRR   OOOOOO      TTT     III  KKK  KKK
 
  MikroTik RouterOS 6.22 (c) 1999-2014       https://www.mikrotik.com/
 
[?]             Gives the list of available commands
command [?]     Gives help on the command and list of arguments
 
[Tab]           Completes the command/word. If the input is ambiguous,
                a second [Tab] gives possible options
 
/               Move up to base level
..              Move up one level
/command        Use command at the base level
```

  

在横幅之后可以打印其他重要信息，如另一个管理员设置的系统说明、最后几条关键日志信息、演示版升级提醒和默认配置说明。

例如，演示版许可证提示和最后的关键信息会打印出来

```shell
UPGRADE NOW FOR FULL SUPPORT
----------------------------
FULL SUPPORT benefits:
- receive technical support
- one year feature support
- one year online upgrades
    (avoid re-installation and re-configuring your router)
To upgrade, register your license "software ID"
on our account server www.mikrotik.com
 
Current installation "software ID": ABCD-456
 
Please press "Enter" to continue!
 
 
dec/10/2007 10:40:06 system,error,critical login failure for user root from 10.0.0.1 via telnet
dec/10/2007 10:40:07 system,error,critical login failure for user root from 10.0.0.1 via telnet
dec/10/2007 10:40:09 system,error,critical login failure for user test from 10.0.0.1 via telnet
```

# 命令提示符

在成功登录时，登录过程会打印出一个显示命令提示符的横幅，并将控制权交给用户。

默认的命令提示由用户名、系统身份和当前的命令路径/>组成。

例如，将当前路径从根目录改为接口，然后再回到根目录

```shell
[admin@MikroTik] > interface [enter]
[admin@MikroTik] /interface> / [enter]
[admin@MikroTik] >
```

使用向上箭头从命令历史中调用以前的命令，**TAB** 键自动完成正在输入的命令中的单词，**ENTER** 键执行命令，**Control-C** 中断当前运行的命令并返回到提示符，**?** 显示内置帮助，在RouterOS v7中，必须使用 **F1** 代替。

退出控制台的最简单方法是在命令行为空时按下 **Control-D** （可以用 **Control-C** 取消当前命令并得到一个空行，所以在大多数情况下，**Control-C** 和 **Control-D** 会退出）。

编写由多行组成的命令是可能的。当输入的行不是一个完整的命令，并且期望有更多的输入时，控制台会显示一个继续提示，列出所有开放的小括号、大括号、小括号和引号，如果前一行以 **反斜线** -空格结束，也会出现尾部反斜线。

```shell
[admin@MikroTik] > {
{... :put (\
{(\... 1+2)}
3
```

当编辑多行条目时，提示显示当前行数和总行数，而不是通常的用户名和系统名称。

```
第2行，共3行> :put (\)
```

有时命令要求用户提供额外的输入。例如，命令 `/password` 要求输入新旧密码。在这种情况下，提示符显示所要求的值的名称，后面是冒号和空格。

```shell
[admin@MikroTik] > /password
old password: ******
new password: **********
retype new password: **********
```

# 层次结构

控制台允许使用文本命令来配置路由器的设置。由于有很多可用的命令，被分成若干组，以分层菜单级别的方式组织。一个菜单级别的名称反映了相关部分可访问的配置信息。

例如， `/ip route print` 命令：

```shell
[admin@MikroTik] > /ip route print
Flags: D - dynamic; X - disabled, I - inactive, A - active;
C - connect, S - static, r - rip, b - bgp, o - ospf, d - dhcp, v - vpn
 #     DST-ADDRESS        GATEWAY            DISTANCE
 0  XS 4.4.4.4            10.155.101.1     
   D o 0.0.0.0/0          10.155.101.1            110
 1  AS 0.0.0.0/0          10.155.101.1              1
   D b 1.0.4.0/24         10.155.101.1             20
   D b 1.0.4.0/24         10.155.101.1             20
   DAb 1.0.4.0/24         10.155.101.1             20
[admin@MikroTik] >
```

而不是在每个命令前键入 `/ip route` 路径，只需键入一次路径就可以进入菜单层次结构的特定分支。因此，上面的例子也可以这样执行：

```shell
[admin@MikroTik] > /ip route
[admin@MikroTik] /ip/route> print
Flags: D - dynamic; X - disabled, I - inactive, A - active;
C - connect, S - static, r - rip, b - bgp, o - ospf, d - dhcp, v - vpn
 #     DST-ADDRESS        GATEWAY            DISTANCE
 0  XS 4.4.4.4            10.155.101.1     
   D o 0.0.0.0/0          10.155.101.1            110
 1  AS 0.0.0.0/0          10.155.101.1              1
   D b 1.0.4.0/24         10.155.101.1             20
   D b 1.0.4.0/24         10.155.101.1             20
   DAb 1.0.4.0/24         10.155.101.1             20
[admin@MikroTik] >
```

路径中的每个字可以用 **空格** （如上面的例子）或用"/"来分隔

```shell
[admin@MikroTik] > /ip/route/
[admin@MikroTik] /ip/route> print
Flags: D - dynamic; X - disabled, I - inactive, A - active;
C - connect, S - static, r - rip, b - bgp, o - ospf, d - dhcp, v - vpn
 #     DST-ADDRESS        GATEWAY            DISTANCE
 0  XS 4.4.4.4            10.155.101.1     
   D o 0.0.0.0/0          10.155.101.1            110
 1  AS 0.0.0.0/0          10.155.101.1              1
   D b 1.0.4.0/24         10.155.101.1             20
   D b 1.0.4.0/24         10.155.101.1             20
   DAb 1.0.4.0/24         10.155.101.1             20
[admin@MikroTik] >
```

注意，提示会变化以反映你目前在菜单层次中的位置。要移动到顶层，输入" / "

```shell
[admin@MikroTik] > ip route
[admin@MikroTik] /ip/route> /
[admin@MikroTik] >
```

要上移一个级别，键入"..."

```shell
[admin@MikroTik] /ip/route> ..
[admin@MikroTik] /ip>
```

也可以使用 **/** 和 **...** 来执行其他菜单级别的命令而不改变当前级别：

```shell
[admin@MikroTik] /ip/route> /ping 10.0.0.1
10.0.0.1 ping timeout
2 packets transmitted, 0 packets received, 100% packet loss
[admin@MikroTik] /ip/firewall/nat> .. service-port print
Flags: X - disabled, I - invalid
#   NAME                                                                PORTS
0   ftp                                                                 21
1   tftp                                                                69
2   irc                                                                 6667
3   h323
4   sip
5   pptp
[admin@MikroTik] /ip/firewall/nat>
```

# 项目名称和编号

许多命令级别的操作都是以项目数组为单位的：接口、路由、用户等等。这样的数组显示在外观相似的列表中。列表中的所有项目都有一个项目编号，后面是标志和参数值。

要改变项目的属性，必须使用set命令并指定项目的名称或编号。

## 项目名称

一些列表中的项目都有特定的名称分配给它们。例如，界面或用户级别。在那里可以使用项目名称而不是项目编号。

在用名字访问项目之前不必使用打印命令，与数字不同的是，名字不是由控制台内部分配的，而是项目的属性。因此，它们不会自行改变。然而，当几个用户同时改变路由器的配置时，有可能出现各种不明显的情况。一般来说，项目名称比数字更 "稳定"，也更有信息量，所以在编写控制台脚本时，应该首选名称而不是数字。

## 项目编号

项目编号是由打印命令分配的，并不是恒定的-两个连续的打印命令有可能对项目进行不同的排序。但是，最后一次打印命令的结果会被记住，因此，一旦分配了项目编号，即使在添加、删除和移动操作之后也可以使用（从第3版开始，移动操作不会对项目重新编号）。项目编号是以每个会话为基础分配的，它们将保持不变，直到退出控制台或执行下一个打印命令。另外，每个项目列表的编号是单独分配的，所以 `iip address print` 不会改变接口列表的编号。

可以指定多个项目作为某些命令的目标。几乎在任何地方，只要能写出项目数量，也可以写出数字列表。

```shell
[admin@MikroTik] > interface print
Flags: X - disabled, D - dynamic, R - running
  #    NAME                 TYPE             MTU
  0  R ether1               ether            1500
  1  R ether2               ether            1500
  2  R ether3               ether            1500
  3  R ether4               ether            1500
[admin@MikroTik] > interface set 0,1,2 mtu=1460
[admin@MikroTik] > interface print
Flags: X - disabled, D - dynamic, R - running
  #    NAME                 TYPE             MTU
  0  R ether1               ether            1460
  1  R ether2               ether            1460
  2  R ether3               ether            1460
  3  R ether4               ether            1500
[admin@MikroTik] >
```

# 一般命令

有些命令在几乎所有的菜单级别中都是通用的，即：打印、设置、删除、添加、查找、导出、启用、禁用、注释、移动： **print, set, remove, add, find, get, export, enable, disable, comment, move.** 这些命令在不同的菜单级别上有类似的行为。

| 属性       | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **add**    | 这个命令的参数通常与集合相同，除了项目编号参数。它用指定的值添加一个新的项目，通常是在项目列表的末尾，在与项目的顺序有关的地方。有些必须提供的属性，比如新地址的接口，而其他属性则被设置为默认值，除非明确指定。<br>常用参数<br>- copy-from -复制一个现有的项目。它从另一个项目中获取一个新项目的属性的默认值。如果不想做一个精确的拷贝，可以为一些属性指定新值。当复制有名字的项目时，通常要给副本一个新名字。<br>- place-before - 把一个新项目放在一个现有的项目之前，并指定位置。不需要在向列表添加项目后使用移动命令。<br>- disabled - 控制新添加项目的禁用/启用状态。<br>- comment - 保存新创建的项目的描述<br>返回值<br>- 添加命令返回添加的项目的内部数量                                                                                                                                                       |
| **edit**   | 此命令与set命令相关。用来编辑包含大量文本的属性值，如脚本，但也适用于所有可编辑的属性。根据终端的能力，会启动一个全屏编辑器或一个单行编辑器来编辑指定属性的值。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| **find**   | 查找命令的参数与集合的参数相同，另外还有一些标志参数，如disabled或active，根据各自的标志值，取值为yes或no。要看到所有的标志和它们的名字，请看打印命令输出的顶部。find命令返回所有具有与指定参数值相同的项目的内部编号。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| **move**   | 改变列表中项目的顺序。参数如下：<br>- 第一个参数指定被移动的项目。<br>- 第二个参数指定所有被移动的项目之前的项目（如果省略第二个参数，它们将被放置在列表的最后）。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| **print**  | 显示所有的信息，可以从一个特定的命令级别访问。因此，`/system clock print` 显示系统日期和时间，`/ip route print` 显示所有路线等。如果当前级别的项目列表不是只读的，也就是说，你可以改变/删除它们（只读项目列表的例子是 `/system history`，显示已执行操作的历史），那么打印命令也会分配数字，这些数字被所有操作该列表中项目的命令所使用。<br>常用参数：<br>- from - 只显示指定的项目，顺序与给定的相同。<br>- where - 只显示符合指定条件的项目。where属性的语法与find命令相似。<br>- brief - 强制打印命令使用表格输出形式<br>- detail - 强制打印命令使用属性=值的输出形式<br>- count-only - 显示项目的数量<br>- file - 将特定子菜单的内容打印到路由器上的一个文件中。<br>- interval - 每隔几秒钟更新一次打印命令的输出。<br>- oid - 打印可以从SNMP访问的属性的OID值<br>- without-paging - 打印输出，在每个屏幕后不停止。 |
| **remove** | 从列表中删除指定的项目。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| **set**    | 允许改变一般参数或项目参数的值。set命令有一些参数，其名称与可改变的值相对应。使用? 或双Tab可以看到所有参数的列表。如果在这个命令层有一个项目列表，那么set有一个动作参数接受想设置的项目数量（或数字列表）。这个命令不返回任何东西。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |


# 输入模式

可以在几种输入模式之间切换：

- **Normal mode** - 以正常的命令提示表示。
- **Safe mode** - 安全模式由命令提示后的SAFE字样表示。在这种模式下，只有在安全模式关闭后，配置才会被保存到磁盘。安全模式可以用 **Ctrl+X或F4** 打开/关闭。 [阅读全文](https://help.mikrotik.com/docs/display/ROS/Configuration+Management#ConfigurationManagement-SafeMode)
- **Hot-lock mode** - 由额外的黄色表示。 热锁模式自动完成命令，可以用 **F7** 打开/关闭。

# 快速打字

控制台中有两个功能可以帮助你更快更容易地输入命令-**Tab** 键的补全和命令名称的缩写。补全键的工作原理类似于UNIX中的bash shell。如果你在一个词的某个部分后按下 **Tab** 键，控制台会尝试在当前上下文中找到以这个词开头的命令。如果只有一个匹配的命令，就会自动附加上，后面是一个空格：

_/inte_ **[Tab]_** 变成 **/interface _**

如果有一个以上的项匹配，但它们有一个共同的开头，而这个开头比输入的内容要长，那么这个词就会完成这个共同的部分，并且不附加空格：

_/interface set e_ **[Tab]_** 变成 **/interface set ether_**

如果你只输入了公共部分，按一次Tab键没有任何效果。然而，第二次按Tab键时，会以紧凑的形式显示所有可能的补语：

```shell
[admin@MikroTik] > interface set e[Tab]_
[admin@MikroTik] > interface set ether[Tab]_
[admin@MikroTik] > interface set ether[Tab]_
ether1 ether5
[admin@MikroTik] > interface set ether_

```

**[Tab]** 键几乎可以用在任何控制台可能提示可能的值的情况下-命令名、参数名、只有几个可能值的参数（如一些列表中的项目名或防火墙和NAT规则中的协议名）。不能完成数字、IP地址和类似的值。

另一个在打字时少按几个键的方法是缩写命令和参数名称。可以只输入命令名称的开头，如果没有混淆，控制台将接受它作为一个完整的名称。所以输入

```shell
[admin@MikroTik] > pi 10.1 c 3 si 100

```

等效于:

```shell
[admin@MikroTik] > ping 10.0.0.1 count 3 size 100

```

不仅可以完成名字的开头，还可以完成名字的任何独特的子串：如果没有精确的匹配，控制台会寻找那些将字符串作为多字名的第一个字母来完成的词，或者仅仅是以相同的顺序包含这个字符串的字母。如果找到一个这样的词，将在光标位置完成。比如

```shell
[admin@MikroTik] > interface x[TAB]_
[admin@MikroTik] > interface export _

[admin@MikroTik] > interface mt[TAB]_
[admin@MikroTik] > interface monitor-traffic _

```

# 控制台搜索

控制台搜索允许在RouterOS菜单列表和历史记录中进行关键词搜索。搜索提示可以通过 **[Ctrl+r]** 快捷键进行。 

# 内部聊天系统

RouterOS控制台有一个内置的内部聊天系统。这允许远程管理员在RouterOS CLI中直接与对方交谈。要开始对话，要在预定的信息前加上#符号，任何在发送信息时已经登录的人都会看到它。

```shell
[admin@MikroTik] > # ready to break internet?
[admin@MikroTik] >
fake_admin: i was born ready
[admin@MikroTik] >
```

```shell
[fake_admin@MikroTik] >
admin: ready to break internet?
[fake_admin@MikroTik] > # i was born ready
[fake_admin@MikroTik] >
```

# 键列表

| 按键                 | 说明                                                                       |
| -------------------- | -------------------------------------------------------------------------- |
| Control-C            | 键盘中断                                                                   |
| Control-D            | 注销（如果输入行是空的）                                                   |
| Control-K            | 从光标到行尾的清零                                                         |
| Control-U            | 从光标到行首的清除                                                         |
| Control-X 或 F4      | 切换安全模式                                                               |
| F7                   | 切换热锁模式模式                                                           |
| Control-R 或 F3      | 切换控制台搜索                                                             |
| F6                   | 切换单元                                                                   |
| F1                   | 显示上下文敏感的帮助                                                       |
| Tab                  | 执行行完成。当第二次按下时，显示可能的完成方式。                           |
| #                    | 发送消息到内部聊天系统                                                     |
| Delete               | 删除光标处的字符                                                           |
| Control-H或Backspace | 删除光标前的字符，并将光标后移一个位置                                     |
| Control-\            | 在光标处分行。在光标位置插入换行。显示产生的两行中的第二行                 |
| Control-B或Left      | 将光标向后移动一个字符                                                     |
| Control-F或Right     | 将光标向前移动一个字符                                                     |
| Control-P或Up        | 转到前一行。如果这是第一行输入，则从历史中调用之前的输入。                 |
| Control-N 或 Down    | 转到下一行。如果这是最后一行输入，则从历史记录中调用下一个输入             |
| Control-A 或 Home    | 将光标移到该行的开头。如果光标已经在行首，则转到当前输入的第一行的开头     |
| Control-E或End       | 将光标移到行尾。如果光标已经在行尾，那么就把它移到当前输入的最后一行的行尾 |
| Control-L或F5        | 重置终端并重新绘制屏幕                                                     |