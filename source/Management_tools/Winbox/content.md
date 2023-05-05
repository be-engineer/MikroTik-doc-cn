# 摘要

Winbox是一个小工具，允许使用快速和简单的GUI来管理MikroTik RouterOS。它是一个原生的Win32二进制文件，但可以使用Wine在 **Linux和macOS（OSX）** 上运行。所有的Winbox界面功能都尽可能地反映了控制台的功能，这就是为什么手册中没有Winbox部分。一些高级和关键的系统配置不可能从Winbox中实现，比如在接口上改变MAC地址 [Winbox changelog](https://wiki.mikrotik.com/wiki/Winbox_changelog)

从Winbox v3.14开始，使用了以下安全特性：

- Winbox.exe由SIA Mikrotīkls（MikroTik）颁发的扩展验证证书签署。
- WinBox使用ECSRP进行密钥交换和认证（需要一个新的Winbox版本）。
- 双方都验证对方是否知道密码（不可能出现中间人攻击）。
- RoMON模式下的Winbox要求代理是最新版本的，以便能够连接到最新版本的路由器。
- Winbox使用AES128-CBC-SHA作为加密算法（需要Winbox 3.14版或以上）。

# 启动Winbox

Winbox加载器可以从 [MikroTik下载页面]（https://www.mikrotik.com/download）下载。当winbox.exe被下载后，双击它，Winbox加载器窗口将弹出。有两种Winbox加载器模式：默认启用的简单模式和高级模式。

## 简单模式

当你第一次打开Winbox加载器时，将使用简单模式布局：

![](https://help.mikrotik.com/docs/download/attachments/328129/winbox_loader_simple_.png?version=1&modificationDate=1570715133744&api=v2)

要连接到路由器，请输入路由器的IP或MAC地址，指定用户名和密码（如果有），然后点击 **连接** 按钮。你也可以在IP地址后面输入端口号，用冒号隔开，像这样192.168.88.1:9999。端口可以在RouterOS的**services** 菜单中改变。

 建议尽可能使用一个IP地址。MAC会话使用网络广播，并非100%可靠。

你也可以使用邻居发现，使用 **邻居** 标签来列出可用的路由器：

![](https://help.mikrotik.com/docs/download/attachments/328129/winbox3_loader_neighbours.png?version=1&modificationDate=1570715282332&api=v2)

在已发现的路由器列表中，点击IP或MAC地址栏来连接到该路由器。如果点击IP地址，那么IP将被用来连接，但如果点击MAC地址，那么MAC地址将被用来连接到路由器。

邻居发现还会显示与Winbox不兼容的设备，如思科路由器或任何其他使用CDP（思科发现协议）的设备。如果试图连接到一个SwOS设备，那么连接将通过网络浏览器建立。

### 按钮/复选框和其他字段

- **连接** - 连接到路由器
- **连接到RoMON** - 连接到 [RoMON](https://wiki.mikrotik.com/wiki/Manual:RoMON "Manual:RoMON")  代理
- **添加/设置** - 保存/编辑 **管理的** 标签中的任何一个已保存的路由器条目。
- **在新窗口打开** - 让加载器在后台打开，并为每个连接的设备打开新窗口。
- **连接到：** - 路由器的目标 IP 或 MAC 地址
- **登录** - 用于验证的用户名
- **密码** - 用于验证的密码
- **保留密码** - 如果不勾选，密码不会被保存到列表中。

### 菜单项目

- **文件**
    - **新建** - 在指定的位置创建一个新的管理路由器列表
    - **打开** - 打开管理的路由器列表文件
    - **另存为** - 将当前管理的路由器列表保存到文件中
    - **退出** - 退出 Winbox 载入器

- **工具**
    - **高级模式** - 启用/禁用高级模式视图
    - **导入** - 导入保存的会话文件
    - **导出** -导出保存的会话文件
    - **移动会话文件夹** - 改变会话文件的存储路径
    - **清除缓存** - 清除Winbox缓存
    - **检查更新** - 检查Winbox加载器的更新。

## 高级模式

当用工具→高级模式启用时，会显示额外的Winbox加载器参数：

![](https://help.mikrotik.com/docs/download/attachments/328129/winbox_loader_advanced.png?version=1&modificationDate=1570715647131&api=v2)

### 按钮/复选框和其他字段

按钮/复选框

- **浏览** - 浏览某些特定会话的文件目录
- **保留密码** - 如果不勾选，密码不会被保存到列表中
- **安全模式** - 如果选中，Winbox将使用DH-1984进行密钥交换，并使用经过修改和加固的RC4-drop3072加密来保证会话的安全。
- **自动保存会话** - 对连接的设备自动保存会话。

字段：

- **Session** - 保存的路由器会话。
- **Note** - 分配给保存路由器条目的注释。
- **组** - 分配给保存的路由器条目的组。
- **RoMON代理** - 从可用设备列表中选择RoMON代理。

被管理的路由器列表是加密的，但如果没有为其设置主密码，仍然可以在其他Winbox中顺利加载

## 命令行

可以使用命令行来自动传递连接到、用户和密码参数：

```
winbox.exe [<connect-to> [<login> [<password>]]]

```

例子 (无密码):

```
winbox.exe 10.5.101.1 admin ""

```

用户 "admin "连接到路由器10.5.101.1，无需密码。

可以用命令行自动传递连接到、用户和密码参数，通过RoMON连接到路由器。在这种情况下，RoMON代理必须保存在被管理的路由器列表中，这样Winbox就会知道这个设备的用户和密码：

```
winbox.exe --romon [<romon-agent> [<connect-to> [<login> [<password>]]]]

```

例子 (无密码):

```
winbox.exe --romon 10.5.101.1 D4:CA:6D:E1:B5:7D admin ""

```

将通过10.5.101.1 RoMON代理连接到路由器D4:CA:6D:E1:B5:7D，用户为 "admin"，没有密码。

## IPv6连接

Winbox支持IPv6连接。要连接到路由器的IPv6地址，必须把它放在方括号里，就像在网络浏览器中连接IPv6服务器时一样。例子： 

  

[2001:db8::1] 。

连接到链路本地地址时，接口索引必须在%之后输入：

[fe80::a00:27ff:fe70:e88c\\%2]

要把Winbox连接到默认之外的其他端口时，端口号设置在方括号之后：

[fe80::a00:27ff:fe70:e88c\\%2]:8299

Winbox邻居发现能够发现支持IPv6的路由器。每个启用IPv6的路由器都有两个条目，一个条目是IPv4地址，另一个是IPv6链路本地地址。你可以很容易地选择你想连接的那一个。

## 在macOS上运行Winbox  

从macOS 10.15 Catalina开始，苹果已经取消了对32位应用程序的支持，这意味着在这个操作系统中不再可能使用普通的Wine和普通的Winbox。Wine已经为macOS提供了一个64位版本，MikroTik也发布了一个特殊的 [Winbox64.exe](https://mt.lv/winbox64)版本。

要运行Winbox64，需要以下步骤。

1.  从 [Wine macOS builds页面](https://github.com/Gcenx/macOS_Wine_builds/releases) 安装最新的Wine ( win-devel-7.X-osx64.tar.xz)，并确保从MikroTik的下载页面下载了 [winbox64.exe](https://mt.lv/winbox64)。
2.  用 "打开文件">Wine64.app启动Winbox64.exe。

## 在Linux上运行Winbox

通过使用Wine仿真软件，可以在Linux上运行Winbox。请确保安装了微软的字体包，否则，你可能会看到失真。

# 界面概述

Winbox的界面设计得很直观，适合大多数用户。该界面由以下部分组成：

- 顶部的主工具栏，用户可以添加各种信息字段，如CPU和内存使用情况。
- 左边的菜单栏 - 所有可用菜单和子菜单的列表。这个列表根据所安装的软件包而变化。例如，如果IPv6软件包被禁用，那么 **IPv6** 菜单和它的所有子菜单将不被显示。
- 工作区 - 所有菜单窗口被打开的一个区域。

![](https://help.mikrotik.com/docs/download/attachments/328129/winbox3.png?version=1&modificationDate=1570716987658&api=v2)

标题栏显示信息确定用哪个路由器打开Winbox会话。信息以下列格式显示：

```
[username]@[Router's IP or MAC] ( [RouterID] ) - Winbox [ROS version] on [RB model] ([platform])

```

从上面的截图可以看到，用户 **krisjanis** 以IPv4/IPv6地址 **[fe80::4e5e:cff:fef6:c0ab%3]** 登录了路由器。路由器的ID是 **3C18-Krisjanis_GW**，当前安装的RouterOS版本是 **v6.36rc6**，RouterBoard是 **CCR1036-12G-4S**，平台是 **tile*。

在主工具条的左边有一个位置：

- **undo**
- **redo**
- **safe mode** 
- 当前加载的会话

更多关于安全模式和撤销已执行的操作，请阅读 [本文]（https://help.mikrotik.com/docs/display/ROS/Configuration+Management）。

右边的位置：

- 显示Winbox会话是否使用加密的指示灯
- Winbox流量指标，显示为绿色条、
- 自定义信息字段，用户可以通过在工具栏上点击右键并从列表中选择可用的信息字段来添加。

# 工作区和子窗口

Winbox有一个MDI界面，所有的菜单配置（子窗口）都附属于主Winbox窗口并显示在工作区。

![](https://help.mikrotik.com/docs/download/attachments/328129/winbox3_work_area.png?version=1&modificationDate=1570717132536&api=v2)

子窗口不能被拖出工作区。注意上面的截图，**界面** 窗口被拖出了可见的工作区，底部出现了一个水平滚动条。如果任何窗口超出了可见工作区的边界，就会出现垂直和水平滚动条。

## 子窗口的菜单栏

每个子窗口都有自己的工具条。大多数窗口都有相同的一组工具条按钮：

- ![](https://help.mikrotik.com/docs/download/attachments/328129/win_add.png?version=1&modificationDate=1570717170050&api=v2) **Add** - 向列表中添加新项目
- ![](https://help.mikrotik.com/docs/download/attachments/328129/win_remove.png?version=1&modificationDate=1570717216908&api=v2) **Remove** - 从列表中删除所选项目
- ![](https://help.mikrotik.com/docs/download/thumbnails/328129/win_enable.png?version=1&modificationDate=1570717241877&api=v2) **Enable** - 启用所选项目（与控制台的 **enable** 命令相同）。
- ![](https://help.mikrotik.com/docs/download/thumbnails/328129/win_disable.png?version=1&modificationDate=1570717256553&api=v2) **Disable** - 禁用所选项目（与控制台的 **disable** 命令相同）。
- ![](https://help.mikrotik.com/docs/download/thumbnails/328129/win_comment.png?version=1&modificationDate=1570717270705&api=v2) **Comment** - 添加或编辑一个注释
- ![](https://help.mikrotik.com/docs/download/thumbnails/328129/win_sort.png?version=1&modificationDate=1570717284913&api=v2) **排序** - 允许根据各种参数对项目进行排序。[阅读全文](https://wiki.mikrotik.com/wiki/Manual:Winbox#Sorting_out_displayed_items)

几乎所有的窗口在工具栏的右侧都有一个快速搜索输入栏。在这个字段中输入的任何文本都会在所有的项目中进行搜索，并突出显示，如下图所示

![](https://help.mikrotik.com/docs/download/attachments/328129/Winbox-window-search.png?version=1&modificationDate=1570717394117&api=v2)

注意，在快速查找输入栏旁边的右侧有一个下拉框。对于当前打开的（IP路由）窗口，这个下拉框允许按路由表快速排序。例如，如果选择了 **main**，那么只有主路由表的路由列出。 
在所有的防火墙窗口中也有一个类似的下拉框，可以按链路快速整理出规则。

## 对显示的项目进行排序

几乎每个窗口都有一个 **排序** 按钮。当点击这个按钮时，会出现几个选项，如截图所示

![](https://help.mikrotik.com/docs/download/attachments/328129/Winbox-window-sort.png?version=1&modificationDate=1570717448154&api=v2)

这个例子显示了如何快速过滤掉10.0.0.0/8范围内的路由

1.  按 **排序** 按钮
2.  从第一个下拉框中选择 **Dst.Address**。
3.  在第二个下拉框中选择 **in**。"in "表示过滤器将检查DST地址值是否在指定网络的范围内。
4.  输入将被比较的网络（在我们的例子中输入 "10.0.0.0/8"）。
5.  这些按钮是为了在堆栈中添加或删除另一个过滤器。
6.  按 **过滤器** 按钮来应用我们的过滤器。

正如你从截图中看到的，Winbox只对10.0.0.0/8范围内的路由进行排序。

比较运算符（截图中的数字 **3**）可能对每个窗口都不同。例如，"Ip Route "窗口只有两个 **is** 和 **in**。其他窗口可能有诸如 "不是"、"包含"、"不包含 "等运算符。

Winbox允许建立一个过滤器的堆栈。例如，如果需要按目标地址和网关过滤，那么

- 设置第一个过滤器，如上面的例子所述、
- 按 **[+]** 按钮，在堆栈中添加另一个过滤器栏。
- 设置第二个过滤器，按网关进行过滤
- 按**过滤器**按钮来应用过滤器。

也可以通过按 **[-]** 按钮从堆栈中删除不必要的过滤器。

## 自定义显示的栏目列表

默认情况下，Winbox显示的是最常用的参数。但有时需要查看其他参数，例如，"BGP AS Path "或其他BGP属性，以监测路由是否被正确选择。

Winbox允许为每个单独的窗口定制显示列。例如，要添加BGP AS路径栏：

- 点击列标题右侧的小箭头按钮（**1**）或在路由列表上点击鼠标右键。
- 从弹出的菜单中移到 **显示列**（**2**），从子菜单中选择所需的列，在我们的例子中点击 **BGP AS路径**（**3**）。

![](https://help.mikrotik.com/docs/download/attachments/328129/Winbox-window-field.png?version=1&modificationDate=1570717546327&api=v2)

对窗口布局所做的改变将被保存，下次打开Winbox时，会应用相同的列序和尺寸。

### 详细模式

也可以启用 **细节模式**。在这种模式下，所有的参数都以列的形式显示，第一列是参数名称，第二列是参数值。

要启用详细模式，请在项目列表上点击鼠标右键，从弹出的菜单中选择 **详细模式**。

![](https://help.mikrotik.com/docs/download/attachments/328129/Winbox-window-detail.png?version=1&modificationDate=1570717649886&api=v2)

### 类别视图

可以按类别列出项目。在这种模式下，所有项目将按字母顺序或按其他类别分组。例如，如果按名称排序，项目可以按字母顺序分类，项目也可以按类型分类，如下面的截图。

要启用类别视图，在项目列表上点击鼠标右键，从弹出的菜单中选择 **显示类别**。

![](https://help.mikrotik.com/docs/download/attachments/328129/Winbox-window-category.png?version=1&modificationDate=1570717682995&api=v2)

## 拖放

可以使用Winbox的拖放功能向路由器上传和下载文件。也可以通过在文件上按下鼠标右键并选择 "下载 "来下载文件。
  
如果Winbox在Linux上使用wine4运行，拖放功能就能发挥作用。在两个Winbox窗口之间拖放可能会失败。

## 流量监控

Winbox可以作为一个工具，实时监控每个接口、队列或防火墙规则的流量。下面的截图显示了以太网流量监控图。

![](https://help.mikrotik.com/docs/download/attachments/328129/Winbox-window-trafmon.png?version=1&modificationDate=1570717937143&api=v2)

## 项目复制

这表明在Winbox中复制一个项目是多么容易。在这个例子中，用复制按钮把一个动态PPPoE服务器接口变成一个静态接口。

这张图片展示了初始状态，正如所看到的，DR表示 "D"，即动态：

![](https://help.mikrotik.com/docs/download/attachments/328129/Winbox-copy-1.PNG?version=1&modificationDate=1570718173146&api=v2)

双击该接口并点击复制：

![](https://help.mikrotik.com/docs/download/attachments/328129/winbox-copy-2.PNG?version=1&modificationDate=1570718191830&api=v2)

出现一个新的接口窗口，会自动创建一个新的名字（在这个例子中是ppo-in1）。

![](https://help.mikrotik.com/docs/download/attachments/328129/winbox-copy-3.PNG?version=1&modificationDate=1570718209792&api=v2)

在Down/Up之后，这个接口变成静态的：

![](https://help.mikrotik.com/docs/download/attachments/328129/winbox-copy-4.PNG?version=1&modificationDate=1570718230700&api=v2)

# 转移设置

- 管理的路由器转移 - 在 "文件 "菜单中，使用 "另存为 "和 "打开 "功能，将管理的路由器列表保存到文件中，并在新的工作站上再次打开它。

- 路由器会话转移 - 在 "工具 "菜单中，使用 "导出 "和 "导入 "功能，将现有会话保存到文件中，并在新工作站上再次导入。

# 故障排除

## Winbox无法连接到路由器的IP地址

确保Windows防火墙被设置为允许Winbox连接，或者禁用Windows防火墙。

## 当连接到路由器的MAC地址时，得到一个错误'20561端口超时'。

如果文件和打印共享被禁用，Windows（7/8）不允许Mac连接。

## 在WinBox IPv4邻居列表中找不到设备，或者MAC连接失败，"ERROR无法连接到XX-XX-XX-XX-XX"

除非主机设备有一个IP配置，否则大多数网络驱动不会启用IP堆栈。需要在主机设备上设置IPv4。

_有时设备会因为缓存而被发现，但MAC连接仍然会失败，"ERROR: could not connect to XX:XX:XX:XX:XX"_。

Winbox的MAC-ADDRESS连接要求MTU值设置为1500，不分片。其他值可能表现不佳，会出现连接丢失。