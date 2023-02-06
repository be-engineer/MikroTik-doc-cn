# 介绍

如果硬件是 RouterBOARD，则只能通过重新安装路由器操作系统或使用重置按钮（或跳线孔）来重置 RouterOS 密码。 对于 X86(CHR) 设备，只有完全重装才能清除密码以及其他配置。 对于 RouterBOARD 设备，有多种方法，具体取决于设备型号。

如果你仍然可以访问你的路由器并希望恢复其默认配置，那可以按下面操作：

- 从命令行界面运行命令 **“/system reset-configuration”**；

- 从图形用户界面中的 **System -> Reset Configuration** 菜单执行此操作；

## 使用复位按钮

RouterBOARD 设备配有一个多功能的复位按钮：

- **RouterBOOT备份加载器**
     通电前按住此按钮，通电三秒后松开，加载备份引导加载程序。 如果设备因 RouterBOOT 升级失败而无法运行则可能需要这样做。 当使用备份加载程序启动设备时，你可以在 RouterBOARD 设置中将 RouterOS 设置为 _force backup loader_，这样有机会从“.fwf”文件重新安装失败的 RouterBOOT（总共 **3 秒**）

- **重置 RouterOS 配置**
     按住此按钮直到 LED 灯开始闪烁，松开按钮将 RouterOS 配置重置为默认值。

- **启用 CAP 模式**
     要将此设备连接到由 CAPsMAN 管理的无线网络，再按住按钮 5 秒钟，LED 常亮，然后松开以打开 CAPs 模式。

- **在网络安装模式下启动 RouterBOARD**
     继续按住按钮 5 秒直到 LED 熄灭，然后松开按钮让 RouterBOARD 寻找 Netinstall 服务器。 也可以简单地按住按钮，直到设备出现在 Windows 的 Netinstall 程序中。

> 也可以在不运行备份加载器的情况下执行前三个功能，只需在通电后立即按下按钮即可。 可能需要另一个人的帮助才能按下按钮并同时插入电源！

## 如何重置配置

1) 拔下设备电源；

2) 通电后立即按住按钮；

     _注意：按住按钮直到 LED 开始闪烁；_

3) 松开按钮清除配置；

> 如果等到 LED 停止闪烁才松开按钮 - 这将改为启动 Netinstall 模式，重新安装 RouterOS。

![](https://help.mikrotik.com/docs/download/attachments/24805498/262_hi_res.png?version=1&modificationDate=1587634648643&api=v2)

## 跳线复位

所有 RouterBOARD 还配备了复位跳线。 有些设备可能需要打开外壳，RB750/RB951/RB751 在外壳的一个橡胶脚下有跳线。

用金属螺丝刀短路跳线，然后启动电路板直到配置被清除： 
![](https://help.mikrotik.com/docs/download/attachments/24805498/Resethole.jpg?version=1&modificationDate=1587635038753&api=v2)![](https://help.mikrotik.com/docs/download/attachments/24805498/Passw.jpg?version=1&modificationDate=1587635043758&api=v2)  

## 旧型号的跳线重置

**下面** 的图显示了 RB133C 等较旧 RouterBOARD 上复位跳线的位置：

![](https://help.mikrotik.com/docs/download/attachments/24805498/CRW_5184.jpg?version=1&modificationDate=1587635093645&api=v2)  

重置配置后不要忘记断开跳线，否则每次重启都会重置！
