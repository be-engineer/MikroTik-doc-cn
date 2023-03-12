# 摘要

RouterBOARD 2011U和CCR系列设备配备了一个电阻式触摸屏，用于快速访问设备的统计数据和简单的配置选项。触摸屏需要对表面施加压力来记录触摸动作，因此轻扫和快速/短击可能不会记录（与手机上常见的电容式触摸屏相反）。如果你发现用手指操作屏幕有困难，也可以尝试用手写笔，或者用笔的另一端。

## 配置

**Sub-menu:** `/lcd`

| 属性                                                                                                                                           | 说明                                                                     |
| ---------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| **backlight-timeout** (_ime interval: 5m...2h \| never_; Default: **30m*)                                                                      | LCD触摸屏关闭时间。                                                      |
| **color-scheme** (_dark \| light_; Default: 取决于RouterBoard型号)                                                                             | 更改为深色或浅色背景。                                                   |
| **default-screen** (_informative-slideshow \| interfaces \| log \| main-menu \| stat-slideshow \| stats \| stats-all_; Default: **main-menu**) | 启动后显示的默认屏幕。                                                   |
| **enabled** (_yes \| no_; Default: **yes**)                                                                                                    | 打开/关闭LCD触摸屏。关闭时，将停止和重置统计数据的收集，并关闭LCD程序。  |
| **read-only-mode** (_yes\|no_; Default: **yes**)                                                                                               | 启用或禁用只读模式。如果启用了只读模式，那么可以改变配置的菜单将被隐藏。 |
| **time-interval** (_min \| hour \| daily \| weekly_; Default: **min**)                                                                         | 在Stats屏幕上显示接口统计的时间间隔。                                    |
| **touch-screen** (_enabled \| disabled_, Default: **enabled**)                                                                                 | 启用/禁用触摸屏输入。                                                    |

可用功能：

- **backlight** - 打开/关闭 LCD 触摸屏背光，LCD 程序保持工作。
- **recalibrate** - 开始 LCD 触摸屏校准过程；
- **show** - 设置LCD显示的画面；
- **take-screenshot** - 截取当前显示的 LCD 屏幕的图像。

### LCD触摸屏校准

在使用LCD触摸屏之前，需要至少校准一次。在第一次成功校准后，数据会存储在路由器上。如果没有校准值，校准过程将自动开始。
  
在校准/重新校准期间，必须触摸屏幕上画的4个点。其中三个点用于计算校准变量，第四个点用于测试校准是否成功。如果校准不成功，校准变量不会保存。结束时（触摸第4个点后），会显示校准结果信息。

### LCD屏幕截图

屏幕截图功能允许创建当前显示的LCD屏幕的BMP图像，并保存在文件列表中的指定名称。没有文件名的截图不会保存，已有文件名的截图会被覆盖。

例子:

```shell
[admin@MikroTik]  /lcd take-screenshot file-name=screen-1
Screenshot taken
[admin@MikroTik] >
```

## LCD接口

**Sub-menu:** `/lcd interface`

接口菜单为Stat Slideshow中的接口显示时间提供配置。最多可以在LCD上增加10个额外的（非物理的）接口。

| 属性                                                                             | 说明                                                                                |
| -------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| **disabled** (_yes                                      \| no_; Default: **no**) | 设置界面是否在统计幻灯片中显示                                                      |
| **max-speed** (_integer                                 \| auto_; Default:)      | 最大的接口速度，用来确定所有接口图和接口屏幕中的带宽。"auto "值只能为物理接口设置。 |
| **timeout** (_time interval: 1s..1m_; Default: **10s**)                          | 显示接口幻灯片时间                                                                  |
  
可用的功能。

- **display** - 在Stats屏幕上显示接口。

### 所有接口图表屏幕

**Sub-menu:** `/lcd interface pages`

一个页面是一个屏幕，最多可以包含12个接口图表。子菜单允许配置在一个页面中显示哪些接口。在所有的接口图上最多可以添加5个页面，每页最多可以有12个接口。要把一个接口添加到一个页面，首先必须在/lcd interfaces子菜单下添加。

| 属性                                       | 说明                                  |
| ------------------------------------------ | ------------------------------------- |
| **interfaces** (interface names; Default:) | 屏幕中显示的接口。必须至少有1个接口。 |

## LCD信息屏幕

**Sub-menu:** `/lcd screen`

屏幕菜单为信息幻灯片显示时间提供配置。

| 属性                                                    | 说明                  |
| ------------------------------------------------------- | --------------------- |
| **disabled** (_yes                                      | no_; Default: **no**) | 定义项目是否被忽略或在信息幻灯片中使用 |
| **timeout** (_time interval: 1s..1m_; Default: **10s**) | 显示信息幻灯片的时间  |

## LCD PIN码

**Sub-menu:** `/lcd pin`

![](https://help.mikrotik.com/docs/download/attachments/130220194/Pin.jpg?version=1&modificationDate=1654085550157&api=v2)   

PIN码用来保护LCD屏幕上的敏感菜单。如果禁用只读模式，并且添加了一个IP地址，重置或重启路由器，将询问PIN码。默认的PIN码是 **1234**。

| 属性                                              | 说明                                          |
| ------------------------------------------------- | --------------------------------------------- |
| **pin-number** (_number_; Default: **1234**)      | PIN 保护码                                    |
| **hide-pin-number** (_yes\| no_; Default: **no**) | 是否在LCD屏幕上显示输入的数字或用星号隐藏它们 |

## LCD屏幕/模式

从6.0版开始，LCD有一个菜单结构。屏幕菜单由用于导航菜单的按钮组成。如果在实际显示中不适合，屏幕的右侧会显示一个滚动条。如果有更多的选项，可以向上或向下拖动屏幕来访问。在每个菜单屏幕的顶部有一个 "返回 "按钮，可以跳转到上一个屏幕。

### 开始

 ![](https://help.mikrotik.com/docs/download/attachments/130220194/Startup.jpg?version=1&modificationDate=1654085635213&api=v2)

如果路由器有默认配置-用户名为 "admin"，没有密码，那么LCD上会出现一个警告。这个屏幕显示分配给接口的IP，用来连接到路由器。否则，开机后会显示主菜单。

### 接口

接口菜单显示所有的以太网和无线接口。带宽使用情况的显示类似于所有接口图。在接口屏幕上，可以查看一个特定的接口。以下是可用的选项：

- 信息（仅适用于物理接口） - 显示接口信息。
- 注册表（仅适用于无线接口）- 菜单显示该无线接口的所有注册客户和它们各自的信号强度。
- 地址 - 列出分配给接口的所有地址。
- 统计 - 允许跳转到 "统计 "屏幕中的选定接口。可以直接选择显示带宽或数据包。

![](https://help.mikrotik.com/docs/download/thumbnails/130220194/Info.jpg?version=1&modificationDate=1654085729260&api=v2)![](https://help.mikrotik.com/docs/download/thumbnails/130220194/Regtable.jpg?version=1&modificationDate=1654085735056&api=v2)![](https://help.mikrotik.com/docs/download/thumbnails/130220194/Addresses.jpg?version=1&modificationDate=1654085739430&api=v2)![](https://help.mikrotik.com/docs/download/thumbnails/130220194/Stats.jpg?version=1&modificationDate=1654085744118&api=v2)

### 统计资料

统计屏幕显示RX和TX的单界面图表。数值从右到左更新（从最新的到最旧的）。显示的信息：RX/TX速率和数据包。

![](https://help.mikrotik.com/docs/download/attachments/130220194/Intstats.jpg?version=1&modificationDate=1654085764591&api=v2)

界面名称显示在右上角，如果太长会被裁剪（最后一个字符会剪掉）。右上角显示数值的时间间隔。以下时间值可用：

- **Min（分钟）** - 显示最后一分钟的数值。单位=秒。竖线将前30秒分开。总的数值。30 + 24;
- **Hour** - 显示过去几个小时的数值。单位=5分钟。垂直线分开1小时。总数值。12 + 12 + 3;
- **Daily** - 显示过去几天的数值。单位=小时。垂直线分开1天。总数值。12 + 12 + 3;
- **Weekly** - 显示过去几周的数值。单位=天。垂直线分开1周。总数值。7 + 7 + 4;

动作：

- 敲击 - 用手指敲击触摸屏，但不做过多的移动。
  - 如果轻击屏幕右上角（屏幕高度的1/4的方块），信息时间间隔就会改变。Min -> Hour -> Daily -> Weekly -> Min......。
  - 否则点一下就会循环浏览图表信息：rate -> packets -> rate....
- 刷/拖 - 手指按住时向任何方向移动。在拖动过程中，变化被突出显示。
  - 向上 - 转到主菜单
  - 向下 - 选择所有界面图屏幕
  - 左 - 下一个界面
  - 右 - 上一个界面

### 所有界面图表屏幕

 ![](https://help.mikrotik.com/docs/download/attachments/130220194/Allintstats.jpg?version=1&modificationDate=1654085792436&api=v2)

所有接口图表屏幕显示所有接口的RX/TX带宽使用情况。最大值是这样计算的-对于以太网接口是协商的速率或设定的速度。对于无线接口来说，是通过使用的频段、信道宽度和链数的理论值来计算的。这个屏幕的目的是要查看单个接口的数值是如何相互关联的。

动作：

- 轻扫/拖动。
  - 向上 - 返回（到统计屏幕）。
  - 左 - 下一页。
  - 右 - 上一页。

### 统计幻灯片

统计幻灯片屏幕与 "Stats "屏幕类似，但接口在超时后会被切换。幻灯片的设置保存在RouterOS的子菜单/lcd interface中。

### 信息幻灯片

子菜单/lcd screen 信息幻灯片屏幕循环播放各种系统信息。

- 聚合流量。
- 聚合数据包。
- 资源。
- 系统。
- 健康。
- 日期和时间。

![](https://help.mikrotik.com/docs/download/thumbnails/130220194/System.jpg?version=1&modificationDate=1654085824845&api=v2)![](https://help.mikrotik.com/docs/download/thumbnails/130220194/Resources.jpg?version=1&modificationDate=1654085829711&api=v2)![](https://help.mikrotik.com/docs/download/thumbnails/130220194/Health.jpg?version=1&modificationDate=1654085834271&api=v2)

### 日志

![](https://help.mikrotik.com/docs/download/attachments/130220194/Log.jpg?version=1&modificationDate=1654085839694&api=v2)   

日志屏幕显示最后5条日志，其中日志动作=echo。

### 重新启动和重置配置

这些屏幕只有在禁用 "只读 "模式时才可用。要访问任何一个屏幕，必须输入Pin码。如果Pin认证成功，用户必须按 "Yes "按钮确认所需的操作，或者按 "No "取消。
